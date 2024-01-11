import torch
import torch.nn as nn
from typing import Tuple
import torch.nn.functional as F

class PreEMPHASIS(nn.Module):
    def __init__(self,
                 coefficient:float = 0.97,
                 *args, **kwargs):
        super().__init__()
        
        self.coefficient = coefficient
        self.register_buffer(
            'flipped_filter', torch.FloatTensor([-self.coefficient, 1.]).unsqueeze(0).unsqueeze(0)
        )

    def forward(self, INPUT: torch.tensor) -> torch.tensor:
        if len(INPUT.shape) == 1:
            return F.conv1d(INPUT.unsqueeze(0), self.flipped_filter).squeeze(0)
        elif len(INPUT.shape) == 2:
            return F.conv1d(INPUT.unsqueeze(1), self.flipped_filter).squeeze()
        elif len(INPUT.shape) == 3:
            return F.conv1d(INPUT, self.flipped_filter)
        
        
class FilterBankAUGMENT(nn.Module):
    def __init__(self,
                 freq_mask_width:Tuple=(0, 8),
                 time_mask_width:Tuple=(0, 10),
                 *args, **kwargs) -> None: 
        super().__init__()
        
        self.time_mask_width = time_mask_width
        self.freq_mask_width = freq_mask_width
       

    def mask_along_axis(self, x:torch.tensor, dim:int):
        original_size = x.shape
        batch, fea, time = x.shape
        if dim == 1:
            D = fea
            width_range = self.freq_mask_width
        else:
            D = time
            width_range = self.time_mask_width

        mask_len = torch.randint(width_range[0], width_range[1], (batch, 1), device=x.device).unsqueeze(2)
        mask_pos = torch.randint(0, max(1, D - mask_len.max()), (batch, 1), device=x.device).unsqueeze(2)
        arange = torch.arange(D, device=x.device).view(1, 1, -1)
        mask = (mask_pos <= arange) * (arange < (mask_pos + mask_len))
        mask = mask.any(dim=1)

        if dim == 1:
            mask = mask.unsqueeze(2)
        else:
            mask = mask.unsqueeze(1)
            
        x = x.masked_fill_(mask, 0.0)
        return x.view(*original_size)

    def forward(self, INPUT:torch.Tensor) -> torch.Tensor:
        INPUT = self.mask_along_axis(INPUT, dim=2)
        INPUT = self.mask_along_axis(INPUT, dim=1)
        return INPUT
    
    
class AlphaFeatureMapScaling(nn.Module):
    def __init__(self,
                 dimension:int,
                 *args, **kwargs) -> None:
        super().__init__()

        self.ALPHA = nn.Parameter(torch.ones((dimension, 1)))
        self.FC = nn.Linear(dimension, dimension)
        self.SIGMOID = nn.Sigmoid()

    def forward(self, INPUT):
        OUT = F.adaptive_avg_pool1d(INPUT, 1).view(INPUT.size(0), -1)
        OUT = self.SIGMOID(self.FC(OUT)).view(INPUT.size(0), INPUT.size(1), -1)

        INPUT = INPUT + self.ALPHA
        INPUT = INPUT * OUT
        return INPUT