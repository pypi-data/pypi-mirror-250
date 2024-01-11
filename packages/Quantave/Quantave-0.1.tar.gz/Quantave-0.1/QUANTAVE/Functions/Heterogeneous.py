import torch, math
import torch.nn as nn
from .Convolutions import CNA_
from .Augmentations import AlphaFeatureMapScaling


class SqueezeExcite(nn.Module):
    def __init__(self,
                 in_channels:int,
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.SE = nn.Sequential(nn.AdaptiveAvgPool1d(1),
                                CNA_(in_channels=in_channels,
                                     out_channels=int(in_channels/2),
                                     kernel_size=1,
                                     padding=0,
                                     normalization_tpe="batchnorm"),
                                nn.Conv1d(in_channels=int(in_channels/2),
                                          out_channels=in_channels,
                                          kernel_size=1,
                                          padding=0),
                                nn.Sigmoid())
    def forward(self, INPUT):
        return INPUT * self.SE(INPUT)

    
class ChannelAggregation(nn.Module):
    def __init__(self,
                 in_channels:int,
                 se_channel:int,
                 kernel_size:int,
                 dilation:int,
                 scale:int,
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.width = int(math.floor(se_channel/scale))
        self.LAYER_1 = CNA_(in_channels=in_channels,
                            out_channels=self.width*scale,
                            kernel_size=1)
        self.number = scale - 1
        padding_ = math.floor(kernel_size/2)*dilation
        
        self.LAYER_N = nn.ModuleList([CNA_(in_channels=self.width,
                                           out_channels=self.width,
                                           kernel_size=kernel_size,
                                           dilation=dilation,
                                           padding=padding_) for _ in  range(self.number)])
        
        self.LAYER_2 = CNA_(in_channels=self.width*scale,
                            out_channels=se_channel,
                            kernel_size=1)

        self.LAYER_SE = SqueezeExcite(se_channel)
        
    def forward(self, INPUT):
        RES = INPUT
        O = self.LAYER_1(INPUT)
        
        S = torch.split(O, self.width, 1)
        for i in range(self.number):
            if i == 0:
                S_ = S[i]
            else:
                S_ = S_ + S[i]
            S_ = self.LAYER_N[i](S_)
            if i == 0:
                O = S_
            else:
                O = torch.cat((O, S_), 1)
        O = torch.cat((O, S[self.number]), 1)
        O = self.LAYER_2(O)
        O = self.LAYER_SE(O)
        return O.add(RES)
    
    
class ParallelConvolution(nn.Module):
    def __init__(self,
                 in_channels:int,
                 out_channels:int,
                 kernel_size:int=None,
                 dilation:int=None,
                 scale:int=4,
                 pool:bool=False,
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.width = int(math.floor(out_channels / scale))

        self.LAYER_1 = CNA_(in_channels=in_channels,
                            out_channels=self.width*scale,
                            kernel_size=1)

        self.LAYER_N = nn.ModuleList([CNA_(in_channels=self.width,
                                           out_channels=self.width,
                                           kernel_size=kernel_size,
                                           dilation=dilation,
                                           padding=math.floor(kernel_size / 2) * dilation) for _ in range(scale-1)])

        self.LAYER_2 = CNA_(in_channels=self.width*scale,
                            out_channels=out_channels,
                            kernel_size=1)

        self.LAYER_MP = nn.MaxPool1d(pool) if pool else nn.Identity()
        self.LAYER_AFMS = AlphaFeatureMapScaling(dimension=out_channels)

        self.RESIDUAL = nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=1, bias=False) if in_channels != out_channels else nn.Identity()
        

    def forward(self, INPUT):
        RESIDUAL = self.RESIDUAL(INPUT)

        OUT = self.LAYER_1(INPUT)
        
        SPLITS = torch.split(OUT, self.width, 1)

        for i in range(len(self.LAYER_N)):
            if i == 0:
                SP_ = SPLITS[i]
            else:
                SP_ = SP_ + SPLITS[i]
            SP_ = self.LAYER_N[i](SP_)
            if i == 0:
                OUT = SP_
            else:
                OUT = torch.cat((OUT, SP_), 1)

        OUT = torch.cat((OUT, SPLITS[len(self.LAYER_N)]), 1)

        OUT = self.LAYER_2(OUT)

        OUT += RESIDUAL
        OUT = self.LAYER_MP(OUT)
        OUT = self.LAYER_AFMS(OUT)
        return OUT
    

class Residual(nn.Module):
    def __init__(self,
                 in_channels:int=4,
                 out_channels:int=20,
                 number_layers:int=4,
                 kernel_size:list or int=3,
                 padding:list or int=1,
                 normalization_type:list or int="batchnorm",
                 activation_type:list or int="relu",
                 *args, **kwargs) -> None:
        super().__init__()
        channels = torch.linspace(in_channels, out_channels, number_layers+1, dtype=torch.int16).requires_grad_(False)
        
        self.LAYER_N = nn.Sequential(
            *[CNA_(in_channels=channels[i],
                   out_channels=channels[i+1],
                   kernel_size=kernel_size[i] if type(kernel_size)==list else kernel_size,
                   padding=padding[i] if type(padding)==list else padding,
                   normalization_tpe=normalization_type[i] if type(normalization_type)==list else normalization_type,
                   activation_type=activation_type[i] if type(activation_type)==list else activation_type) for i in range(number_layers)]
        )
        
        self.RESIDUAL = CNA_(in_channels=in_channels,
                             out_channels=out_channels,
                             kernel_size=1,
                             bias=False,)
        
    def forward(self, INPUT):
        OUT = self.LAYER_N(INPUT)
        RESIDUAL = self.RESIDUAL(INPUT)
        return OUT+RESIDUAL