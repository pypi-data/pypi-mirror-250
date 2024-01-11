import math
import torch
import numpy
import random
import librosa
import soundfile
import torchaudio
from typing import List, Dict
import torch.nn.functional as F
import scipy.signal as scisignal



class Audio:
    def __init__(self) -> None:
        pass
    
    def load(self,
             path:str,
             audio_duration:int or str=2,
             sample_rate:int=16000,
             backend:str="torchaudio",
             audio_normalization:bool=True,
             audio_concat_srategy:str="flip_n_join"):
        
        if backend not in ["torchaudio", "librosa", "soundfile"]:
            raise Exception(f"Only implemented for (torchaudio, librosa, soundfile)")
        if audio_concat_srategy not in ["flip_n_join", "repeat"]:
            raise Exception(f"Only implemented for (random_concat, flip_n_join, repeat)")
        

        if backend == "torchaudio":
            audio, sr = torchaudio.load(path)
        if backend == "librosa":
            audio, sr = librosa.load(path)
            audio = torch.tensor(audio, dtype=torch.float32).unsqueeze(0)
        if backend == "soundfile":
            audio, sr = soundfile.read(path)
            audio = torch.tensor(audio, dtype=torch.float32).unsqueeze(0)
            
            
        max_frames = audio_duration * sample_rate

        if sample_rate != sr:
            resampler = torchaudio.transforms.Resample(sr, sample_rate, dtype=audio.dtype)
            audio = resampler(audio)
        else: pass
        
        if audio_duration == "full": 
            if audio_normalization:
                audio = torch.nn.functional.normalize(audio)
            else: pass
            return audio, sample_rate
        
        if audio.shape[1] < max_frames:
            if audio_concat_srategy == "flip_n_join":
                audio = torch.cat([audio, audio.flip((1,))]*int(max_frames/audio.shape[1]), dim=1)[0][:max_frames]
            if audio_concat_srategy == "repeat":
                audio = torch.tile(audio, (math.ceil(max_frames/audio.shape[1]),))[0][:max_frames]   
        else:
            start = random.randint(0, audio.shape[1]-max_frames + 1)
            audio = audio[0][start:start+max_frames]

        if audio.shape[-1] != max_frames:
            audio = F.pad(audio, (0, max_frames-audio.shape[-1]))
            
        if audio_normalization:
            if len(audio.shape) == 1:
                audio = torch.nn.functional.normalize(audio.unsqueeze(0))
            else:
                audio = torch.nn.functional.normalize(audio)

        return audio, sample_rate


    def __add_reverberate(self,
                        audio_signal:torch.Tensor,
                        rir_audio_path:str,
                        audio_duration=2) -> torch.Tensor:
        
        rir, sr = torchaudio.load(rir_audio_path)
        max_len = audio_duration * sr
        rir = rir / torch.sqrt(torch.sum(rir**2))
        return torch.tensor(scisignal.convolve(audio_signal, rir, mode='full')[:,:max_len])

    def __add_noise(self,
                  audio_signal:torch.Tensor,
                  noise:List[Dict],
                  audio_duration:int=2) -> torch.Tensor:
        
        clean_db = 10 * torch.log10(torch.mean(audio_signal ** 2) + 1e-4) 
        
        _all_noises = []
        for i in noise:
            _n, _ = self.load(i["path"], full=False, audio_duration=audio_duration)
            _n = numpy.stack([_n], axis=0)
            _n_db = 10 * numpy.log10(numpy.mean(_n ** 2) + 1e-4)
            _n_snr = i["snr"]
            _all_noises.append(numpy.sqrt(10 ** ((clean_db - _n_db - _n_snr) / 10)) * _n)
        _noise = numpy.sum(numpy.concatenate(_all_noises, axis=0), axis=0, keepdims=True)

        try:
            return audio_signal + _noise.squeeze(0)
        except Exception as _:
            if audio_signal.shape[1] > _noise.squeeze(0).shape[1]:
                return audio_signal + F.pad(torch.tensor(_noise.squeeze(0)), (0, audio_signal.shape[1] - _noise.squeeze(0).shape[1]), value=0)
            elif audio_signal.shape[1] < _noise.squeeze(0).shape[1]:
                return _noise.squeeze(0) + F.pad(audio_signal, (0, _noise.squeeze(0).shape[1] - audio_signal.shape[1]), value=0)
            
    def augment(self,
                audio_signal:torch.Tensor,
                musan_data_path:str,
                rirs_data_path:str,
                audio_duration:int=2,):
        
        NoiseSnR = {'noise':[0,15],'speech':[13,20],'music':[5,15]}
        NoiseCount = {'noise':[1,1], 'speech':[3,8], 'music':[1,1]}
        
        with open(musan_data_path) as F: musan_noise = F.readlines();F.close(); musan_noise = [i.replace("\n", "") for i in musan_noise]
        with open(rirs_data_path) as F: rirs_noise = F.readlines();F.close(); rirs_noise = [i.replace("\n", "") for i in rirs_noise]
        
        musan_noise_files = {"noise": [], "speech": [], "music": []}
        for i in musan_noise: musan_noise_files[i.split("/")[-3]].append(i)
    
        musan_noise = lambda noise_type: [
            {
                "path": i,
                "type": noise_type,
                "snr": random.uniform(NoiseSnR[noise_type][0], NoiseSnR[noise_type][1])
            } for i in random.sample(musan_noise_files[noise_type], random.randint(NoiseCount[noise_type][0], NoiseCount[noise_type][1]))
        ]
        
        aug_type = random.choice(["clean", "reverb", "speech", "music", "noise"])
        if aug_type == "clean":
            audio_signal = audio_signal
        if aug_type == "reverb":
            audio_signal = self.__add_reverberate(audio_signal, rir_audio_path=random.choice(rirs_noise), audio_duration=audio_duration)
        if aug_type == "speech":
            audio_signal = self.__add_noise(audio_signal, musan_noise(noise_type="speech"), audio_duration=audio_duration)
        if aug_type == "music":
            audio_signal = self.__add_noise(audio_signal, musan_noise(noise_type="music"), audio_duration=audio_duration)
        if aug_type == "noise":
            audio_signal = self.__add_noise(audio_signal, musan_noise(noise_type="noise"), audio_duration=audio_duration)
        if audio_signal.shape[0] != 1:
            return torch.mean(audio_signal, dim=0).unsqueeze(0)
        return audio_signal