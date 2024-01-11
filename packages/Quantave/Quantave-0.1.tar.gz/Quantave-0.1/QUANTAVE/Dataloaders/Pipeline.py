import os
import torch
import random
import itertools
from torch.utils.data import Dataset
from ..Tools.Audio_Tools import Audio
from ..Scripts import DatasetDownloader


class SpeakerVerification(Dataset):
    def __init__(self,
                 dataset_name:str="voxceleb",
                 configurations:dict={},
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.name = dataset_name
        self.configurations = configurations
        
        DatasetDownloader(dataset_name=self.name)
        
        if self.name == "voxceleb":
            speaker_audios_data = open(self.configurations["training_data_filepath"]).read().splitlines()

            self.speakers_dictionary = {k: v for k, v in zip(list(set([i.split()[0] for i in speaker_audios_data])),
                                                             range(len(list(set([i.split()[0] for i in speaker_audios_data])))))
                                        } 

            self.audios = [os.path.join(self.configurations["training_audios_directory"], i.split()[-1]) for i in speaker_audios_data]
            
            self.evaluation_pair_list = [
                    {k:v for k, v in zip(["match", "path_1", "path_2"], i.replace("\n", "").split())} for i in [i.replace(
                            " ",
                            " "+self.configurations["evaluation_audios_directory"]+"/") for i in open(
                                    self.configurations["evaluation_data_filepath"]).read().splitlines()]
                    ]
            
    
    def __len__(self):
            return len(self.audios)
            
    def __getitem__(self, index):
        path = self.audios[index]
        
        audio, ar = Audio().load(path=path)
        
        return audio, self.speakers_dictionary[path.split("/")[-3]]















# class VoxDataset(Dataset):
#     def __init__(self,
#                  audios_data_path:str,
#                  audios_location_path:str,
#                  audio_duration:int,
#                  augmentation:bool=False,
#                  sample_rate:int=16000,
#                  normalization:bool=False,
#                  musan_data_path:str="",
#                  rirs_data_path:str="") -> None:

        
#         self.train_path = audios_location_path
#         self.audio_duration = audio_duration
#         self.aug = augmentation
#         self.normalization = normalization
#         self.sample_rate = sample_rate
        
#         self.data_list  = []
#         self.data_label = []
        
#         if augmentation:
#             self.augmentation = Augmentation(musan_data_path=musan_data_path, rirs_data_path=rirs_data_path)
        
#         lines = open(audios_data_path).read().splitlines()
    
#         if len(lines[0].split(" ")) == 2:        
#             dictkeys = list(set([x.split()[0] for x in lines]))
#             dictkeys.sort()
#             dictkeys = { key : ii for ii, key in enumerate(dictkeys)}
#             for line in lines:
#                 speaker_label = dictkeys[line.split()[0]]
#                 file_name     = os.path.join(audios_location_path, line.split()[1])
#                 self.data_label.append(speaker_label)
#                 self.data_list.append(file_name)
    
#         elif len(lines[0].split(" ")) == 3:
#             dictkeys = list(set([x.split()[1].split("/")[0] for x in lines]))
#             dictkeys.sort()
#             dictkeys = { key : ii for ii, key in enumerate(dictkeys)}
#             for line in lines:
#                 speaker_label = dictkeys[line.split()[1].split("/")[0]]
#                 file_name = " ".join([audios_data_path + "/" + i for i in line.split()])
#                 self.data_label.append(speaker_label)
#                 self.data_list.append(file_name)
    
#     def __len__(self):
#         return len(self.data_list)
    
#     def __getitem__(self, index):

#         if len(self.data_list[index].split()) == 1:
#             audio, _ = load_audio(path=self.data_list[index],
#                                   full=False,
#                                   audio_duration=self.audio_duration,
#                                   sample_rate=self.sample_rate,
#                                   normalization=self.normalization)
#             if self.aug:
#                 audio = self.augmentation.augment(signal=audio, audio_duration=self.audio_duration)
#             return audio, self.data_label[index]
            

#         elif len(self.data_list[index].split()) == 3:            
#             _pairs = self.data_list[index].split()
#             pos, anchor, neg = _pairs[0], _pairs[1], _pairs[2]
            
#             pos_audio, _ = load_audio(path=pos,
#                                       full=False,
#                                       audio_duration=self.audio_duration,
#                                       sample_rate=self.sample_rate,
#                                       normalization=self.normalization)
#             audio, _ = load_audio(path=anchor,
#                                   full=False,
#                                   audio_duration=self.audio_duration,
#                                   sample_rate=self.sample_rate,
#                                   normalization=self.normalization)
#             neg_audio, _ = load_audio(path=neg,
#                                       full=False,
#                                       audio_duration=self.audio_duration,
#                                       sample_rate=self.sample_rate,
#                                       normalization=self.normalization)

#             if self.aug:
#                 audio = self.augmentation.augment(audio=audio, audio_duration=self.audio_duration)
#             return pos_audio.to(dtype=torch.float32), audio.to(dtype=torch.float32), neg_audio.to(dtype=torch.float32), self.data_label[index]
        

# class Audios_Voxceleb:
#     def __init__(self,
#                  evaluating_audios_file_path:str,
#                  number_classes) -> None:
        
#         with open(evaluating_audios_file_path, "r") as F: self.lines = F.readlines(); F.close()
#         self.lines = [i.replace("\n", "") for i in self.lines]
        
#         self.classes = list(set([i.split("/")[-3] for i in self.lines]))
#         if number_classes > len(self.classes):
#             raise Exception(f"number_classes > available_classes, {number_classes} > {len(self.classes)}")
        
#         self.classes_dict = {k: v for k, v in zip(self.classes, range(len(self.classes)))}
#         self.out_data = list(itertools.chain.from_iterable([[i for i in self.lines if j in i] for j in random.sample(self.classes, number_classes)]))
        
#     def get_data(self,):
#         for i in self.out_data:
#             yield i, i.split("/")[-3]



# class SelectiveDataVoxceleb:
#     def __init__(self,
#                  voxceleb_spkid_audios_file_path,
#                  voxceleb_training_audios_location,
#                  number_classes,
#                  number_samples,
#                  audio_audio_duration) -> None:

#         with open(voxceleb_spkid_audios_file_path, "r") as F:self.lines=[i.replace("\n", "") for i in F.readlines()];F.close()
#         with open("/home/air/DATASETS/DATASET_VOXCELEB/FILE_configurations/Class_100Plus", "r") as F:self.classes=[i.replace("\n", "")for i in F.readlines()];F.close()

#         self.train_audios_location = voxceleb_training_audios_location
#         self.number_samples = number_samples
#         self.audio_duration = audio_audio_duration
        
#         self.total_classes = list(set([i.split()[0] for i in self.lines])) 
#         self.class_dict = {k: v for k, v in zip(sorted(self.total_classes), range(len(self.total_classes)))}

#         self.asked_classes = random.sample(self.classes, k=number_classes)

    
#     def data(self):
#         D = []
#         for i in self.asked_classes:
#             D.append({"ID": i,
#                       "CLASS": self.class_dict[i],
#                       "DATA": random.sample([os.path.join(self.train_audios_location, j.split()[-1]) for j in self.lines if i in j], k=self.number_samples)})
        
#         A, L = [], []
#         for i in D:
#             for j in i["DATA"]:
#                 audio, _ = load_audio(path=j,
#                                       full=False,
#                                       audio_duration=self.audio_duration,
#                                       sample_rate=16000,
#                                       normalization=False)
#                 A.append(audio)
#                 L.append(torch.tensor(i["CLASS"], dtype=torch.int32))
        
#         Z = list(zip(A,L))
#         random.shuffle(Z)
#         A, L = zip(*Z)
#         return torch.vstack(A), torch.vstack(L)
    