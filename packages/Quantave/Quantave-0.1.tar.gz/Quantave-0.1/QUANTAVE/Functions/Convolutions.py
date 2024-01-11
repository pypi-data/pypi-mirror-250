import torch
import torch.nn as nn


class Classic(nn.Module):
    def __init__(self,
                 in_channels:int,
                 out_channels:int,
                 kernel_size:int,
                 stride:int=1,
                 padding:int=0,
                 dilation:int=1,
                 groups:int=1,
                 bias:bool=False,
                 padding_mode:str='zeros',
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.Convolution = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding, dilation, groups, bias, padding_mode)
    
    def forward(self, INPUT):
        return self.Convolution(INPUT)

class Depthwise(nn.Module):
    def __init__(self,
                 in_channels:int,
                 out_channels:int,
                 kernel_size:int,
                 stride:int=1,
                 padding:int=0,
                 dilation:int=1,
                 groups:int=1,
                 bias:bool=True,
                 padding_mode:str='zeros',
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.Convolution = nn.Sequential(
            nn.Conv1d(in_channels, in_channels, kernel_size, stride, padding, dilation, in_channels, bias, padding_mode),
            nn.Conv1d(in_channels, out_channels, 1, stride, padding, dilation, groups, bias, padding_mode)
        )
    
    def forward(self, INPUT):
        return self.Convolution(INPUT)

class Lowrank(nn.Module):
    def __init__(self,
                 in_channels:int,
                 out_channels:int,
                 kernel_size:int,
                 rank:int=1,
                 stride:int=1,
                 padding:int=0,
                 dilation:int=1,
                 groups:int=1,
                 bias:bool=True,
                 padding_mode:str='zeros',
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.Convolution = nn.Sequential(
             nn.Conv1d(in_channels, rank, kernel_size, stride, padding, dilation, groups, bias, padding_mode),
             nn.Conv1d(rank, out_channels, 1, stride, padding, dilation, groups, bias, padding_mode)
        )
    
    def forward(self, INPUT):
        return self.Convolution(INPUT)


_Convolutions_ = {
    "classic": Classic,
    "depthwise": Depthwise,
    "lowrank": Lowrank
}

_Normalizations_ = {
    "batchnorm": nn.BatchNorm1d,
    "none": nn.Identity
}

_Activations_ = {
    "relu": nn.ReLU,
    "none": nn.Identity
}

class CNA_(nn.Module):
    def __init__(self,
                 in_channels:int,
                 out_channels:int,
                 kernel_size:int,
                 rank:int=1,
                 stride:int=1,
                 padding:int=0,
                 dilation:int=1,
                 groups:int=1,
                 bias:bool=True,
                 padding_mode:str='zeros',
                 convolution_type:str="classic",
                 activation_type:str="relu",
                 normalization_tpe:str="batchnorm",
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.Convoution = _Convolutions_[convolution_type](in_channels=in_channels,
                                                           out_channels=out_channels,
                                                           kernel_size=kernel_size,
                                                           rank=rank,
                                                           stride=stride,
                                                           padding=padding,
                                                           dilation=dilation,
                                                           groups=groups,
                                                           bias=bias,
                                                           padding_mode=padding_mode,)
        
        self.Normalization = _Normalizations_[normalization_tpe](out_channels)
        
        self.Activation = _Activations_[activation_type]()
        
    def forward(self, INPUT):
        return self.Activation(self.Normalization(self.Convoution(INPUT)))