import torch, torch.nn as nn
from ..Functions.Convolutions import CNA_
from ..Functions.Augmentations import PreEMPHASIS
from asteroid_filterbanks import Encoder, ParamSincFB
from ..Functions.Heterogeneous import ParallelConvolution


class Frontend(nn.Module):
    def __init__(self,
                 C:int=1024,
                 stride:int=10,
                 log_sinc:bool=True,
                 sinc_type:int="mean",
                 *args, **kwargs) -> None:
        super().__init__()
        
        self.LOG_SINC = log_sinc
        self.SINC = sinc_type
        
        self.PREEMPHASIS = nn.Sequential(
            PreEMPHASIS(),
            nn.InstanceNorm1d(1, eps=1e-4, affine=True)
        )
        self.FILTER = Encoder(filterbank=ParamSincFB(
            n_filters=C//4,
            kernel_size=251,
            stride=stride
        ))
    
    def forward(self, INPUT):
        with torch.cuda.amp.autocast(enabled=False):
            INPUT = self.PREEMPHASIS(INPUT)
            INPUT = torch.abs(self.FILTER(INPUT))

            if self.LOG_SINC:
                INPUT = torch.log(INPUT + 1e-6)

            if self.SINC == "mean":
                INPUT = INPUT - torch.mean(INPUT, dim=-1, keepdim=True)

            elif self.SINC == "mean_std":
                MEAN = torch.mean(INPUT, dim=-1, keepdim=True)
                STDV = torch.std(INPUT, dim=-1, keepdim=True)
                STDV[STDV < 0.001] = 0.001
                INPUT = (INPUT - MEAN) / STDV
        
            return INPUT


class RawNet_3(nn.Module):
    def __init__(self,
                 C:int=1024,
                 model_scale:int=8,
                 layers_parameters:list=[
                     {"kernel_size": 3, "dilation": 2, "pool": 5},
                     {"kernel_size": 3, "dilation": 3, "pool": 3},
                     {"kernel_size": 3, "dilation": 4, "pool": False},
                 ],
                 embedding:int=256,
                 encoder_type:str="eca",
                 *args, **kwargs):
        super().__init__()
        
        self.layer_summation = kwargs.get("layer_summation", True)
        self.context = kwargs.get("context", True)
        if self.context:
            attention_input = 4608
        else:
            attention_input = kwargs.get("attention_dimension", 1536)
        
        # attention_output = 1 means encoder is "Attentive Stats Pool"
        attention_output = kwargs.get("attention_dimension", 1536) if encoder_type == "eca" else 1

        self.FRONTEND = Frontend(C=C,
                                 stride=kwargs.get("stride", 10),
                                 log_sinc=kwargs.get("log_sinc", True),
                                 sinc_type=kwargs.get("sinc_type", "mean"))
        
        self.LAYER_N = nn.ModuleList(
            [ParallelConvolution(in_channels=C//4 if idx == 0 else C,
                                 out_channels=C,
                                 kernel_size=P["kernel_size"],
                                 dilation=P["dilation"],
                                 scale=model_scale,
                                 pool=P["pool"]) for idx, P in enumerate(layers_parameters)]
        )

        self.LAYER_2 = CNA_(in_channels=len(layers_parameters)*C,
                            out_channels=kwargs.get("attention_dimension", 1536),
                            kernel_size=1,
                            normalization_tpe="none",
                            activation_type="relu")
        
        self.LAYER_MP = nn.MaxPool1d(kernel_size=3)
        
        self.ATTENTION = nn.Sequential(
            CNA_(in_channels=attention_input, out_channels=int(embedding/2), kernel_size=1),
            CNA_(in_channels=int(embedding/2), out_channels=attention_output, kernel_size=1),
            nn.Softmax(dim=2)
        )

        self.LAYER_FINAL = nn.Sequential(
            nn.BatchNorm1d(3072),
            nn.Linear(3072, embedding),
            nn.BatchNorm1d(embedding) if kwargs.get("output_batchnorm", False) else nn.Identity()
        )
        # print(self.LAYER_FINAL)

    def forward(self, INPUT, *args, **kwargs):
        OUT = self.FRONTEND(INPUT)

        OUT_ = []
        for idx, Layer in enumerate(self.LAYER_N):
            OUT = Layer(OUT)
            if idx == 0: 
                OUT_.append(self.LAYER_MP(OUT))
            else:
                OUT_.append(OUT)
            
            if (idx == len(self.LAYER_N)-1) and (self.layer_summation):
                OUT += OUT_[0]
        OUT = self.LAYER_2(torch.cat(OUT_, dim=1))
        
        T = OUT.size()[-1]
        if self.context:
            GLOBAL_OUT = torch.cat(tensors=[
                OUT,
                torch.mean(OUT, dim=2, keepdim=True).repeat(1, 1, T),
                torch.sqrt(torch.var(OUT, dim=2, keepdim=True).clamp(min=1e-4, max=1e4)).repeat(1, 1, T),
            ], dim=1)
        else:
            GLOBAL_OUT = OUT

        OUT_A = self.ATTENTION(GLOBAL_OUT)
        OUT = self.LAYER_FINAL(
            torch.cat(tensors=[
                torch.sum(OUT*OUT_A, dim=2),
                torch.sqrt((torch.sum((OUT**2)*OUT_A, dim=2)-torch.sum(OUT*OUT_A, dim=2)**2).clamp(min=1e-4, max=1e4))
                ], dim=1)            
            )
        return OUT
        