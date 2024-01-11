import torchaudio
import torch, torch.nn as nn
from ..Functions.Convolutions import CNA_
from ..Functions.Heterogeneous import ChannelAggregation
from ..Functions.Augmentations import PreEMPHASIS, FilterBankAUGMENT



class Frontend(nn.Module):
    def __init__(self,
                 augmentation:bool=False,
                 *args, **kwargs) -> None:
        super().__init__()        
        
        self.augmention = augmentation
        self.PREEMPHASIS = PreEMPHASIS()
        self.MELSPEC = torchaudio.transforms.MelSpectrogram(sample_rate=16000,
                                                            n_fft=512,
                                                            win_length=400,
                                                            hop_length=160,
                                                            f_min=20,
                                                            f_max=7600,
                                                            window_fn=torch.hamming_window,
                                                            n_mels=80)

    def forward(self, INPUT):
        with torch.no_grad():
            INPUT = self.PREEMPHASIS(INPUT)
            
            INPUT = self.MELSPEC(INPUT.to(torch.float32))
            INPUT += 1e-6
            INPUT = INPUT.log()
            INPUT = INPUT - torch.mean(INPUT, dim=-1, keepdim=True)
            if self.augmention:
                INPUT = FilterBankAUGMENT().forward(INPUT.squeeze(1))
            return INPUT
        
        
class ECAPA_TDNN(nn.Module):
    def __init__(self,
                 C:int=1024,
                 embedding:int=512,
                 frontend:str="spectrogram",
                 number_of_blocks:int=3,
                 training:bool=True,
                 *args, **kwargs) -> None:
        super().__init__()
        
        if frontend == "spectrogram":
            self.FRONTEND = Frontend(augmentation=training)

        elif frontend == "rawaudio":
            self.FRONTEND = nn.Conv1d(in_channels=1,
                                      out_channels=80,
                                      kernel_size=400,
                                      stride=160)
        
        self.RELU = nn.ReLU()
            
        self.LAYER_1 = CNA_(in_channels=80, 
                            out_channels=C,
                            kernel_size=5,
                            stride=1,
                            padding=2)
        self.BLOCKS = nn.ModuleList([ChannelAggregation(in_channels=C,
                                                        se_channel=C,
                                                        kernel_size=3,
                                                        dilation=2+i,
                                                        scale=8) for i in range(number_of_blocks)])
        
        self.LAYER_2 = nn.Conv1d(in_channels=number_of_blocks*C,
                                 out_channels=1536,
                                 kernel_size=1)
        
        self.ATTENTION = nn.Sequential(CNA_(in_channels=4608,
                                            out_channels=256,
                                            kernel_size=1),
                                       nn.Tanh(),
                                       nn.Conv1d(in_channels=256, 
                                                 out_channels=1536,
                                                 kernel_size=1),
                                       nn.Softmax(dim=2))
        self.LAYER_3 = nn.BatchNorm1d(num_features=3072)
        self.LAYER_4 = nn.Linear(in_features=3072, out_features=embedding)
        self.LAYER_5 = nn.BatchNorm1d(embedding)
        
    def forward(self, INPUT, *args, **kwargs):
        O = self.FRONTEND(INPUT)
        O = self.LAYER_1(O)
        
        O_ = []
        O1 = O
        for B in self.BLOCKS:            
            O1 = B(O1)
            O_.append(O1)
            O1 += O1
        
        O = self.RELU(self.LAYER_2(torch.cat(O_, dim=1)))
        T = O.size()[-1]
        GLOBAL_O = torch.cat((O,
                              torch.mean(O, dim=2, keepdim=True).repeat(1,1,T),
                              torch.sqrt(torch.var(O, dim=2, keepdim=True).clamp(min=1e-4)).repeat(1,1,T)),
                             dim=1)
        
        W = self.ATTENTION(GLOBAL_O)
        MU = torch.sum(O*W, dim=2)
        STD = torch.sqrt((torch.sum((O**2)*W, dim=2) - MU**2 ).clamp(min=1e-4))
        
        O = torch.cat((MU, STD), dim=1)
        O = self.LAYER_3(O)
        O = self.LAYER_4(O)
        O = self.LAYER_5(O)
        return O