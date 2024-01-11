import torch, torch.nn as nn
import torch.nn.functional as F
from ..Functions.Convolutions import CNA_
from ..Functions.Heterogeneous import Residual


class SSDNet(nn.Module):
    def __init__(self,
                 number_classes:int=2,
                 filter_channels:int=32,
                 number_residuals:int=4,
                 number_fc_layers:int=4,
                 number_residuals_layers:int=4,
                 *args, **kwargs) -> None:
        super().__init__()
        
        conv_channels = torch.linspace(filter_channels, filter_channels*number_residuals*2, number_residuals+1, dtype=torch.int16).requires_grad_(False)
        fc_channels = torch.linspace(conv_channels[-1], number_classes, number_fc_layers+1, dtype=torch.int16).requires_grad_(False)
        
        self.LAYER_1 = CNA_(in_channels=1, out_channels=filter_channels, kernel_size=7, padding=3, bias=False)
        
        self.LAYER_N = nn.ModuleList(
            [Residual(in_channels=conv_channels[i],
                      out_channels=conv_channels[i+1],
                      number_layers=number_residuals_layers) for i in range(number_residuals)]
        )
        
        self.LAYER_FINAL = nn.ModuleList(
            [nn.Linear(in_features=fc_channels[i],
                       out_features=fc_channels[i+1])for i in range(number_fc_layers)]
        )
    
    def forward(self, INPUT, *args, **kwargs):
        OUT = F.max_pool1d(input=self.LAYER_1(INPUT), kernel_size=4)
        
        for idx, conv_layer in enumerate(self.LAYER_N):
            if idx != len(self.LAYER_N)-1:
                OUT = F.max_pool1d(input=conv_layer(OUT), kernel_size=4)
            else:
                OUT = conv_layer(OUT)

        OUT = F.max_pool1d(input=OUT, kernel_size=OUT.shape[-1])
        OUT = torch.flatten(OUT, start_dim=1)

        for idx, fc_layer in enumerate(self.LAYER_FINAL):
            if idx != len(self.LAYER_N)-1:
                OUT = F.relu(fc_layer(OUT))
            else:
                OUT = fc_layer(OUT)
        return OUT