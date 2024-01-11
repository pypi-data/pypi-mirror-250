import math, torch
import torch.nn as nn
from typing import Tuple
import torch.nn.functional as F


class AAM_Softmax(nn.Module):
    def __init__(self,
                 number_classes:int=5994,
                 margin:float=0.3,
                 scale:int=12,
                 embedding:int=512,
                 *args, **kwargs) -> None:
        super().__init__()

        self.scale = scale
        self.CE = nn.CrossEntropyLoss()

        self.W = torch.nn.Parameter(torch.FloatTensor(number_classes, embedding), requires_grad=True)
        nn.init.xavier_normal_(self.W, gain=1)

        self.COS_margin = math.cos(margin)
        self.SIN_margin = math.sin(margin)
        self.THRESHOLD = math.cos(math.pi - margin)
        self.MM = math.sin(math.pi - margin) * margin

    def forward(self, INPUT:torch.tensor, LABEL:torch.tensor=None) -> Tuple[torch.tensor, float]:
        COSINE = F.linear(F.normalize(INPUT), F.normalize(self.W))
        PHI = COSINE * self.COS_margin - torch.sqrt((1.0 - torch.mul(COSINE, COSINE)).clamp(0, 1)) * self.SIN_margin
        PHI = torch.where((COSINE - self.THRESHOLD) > 0, PHI, COSINE - self.MM)
        
        ONE_HOT = torch.zeros_like(COSINE)
        ONE_HOT.scatter_(1, LABEL.view(-1, 1), 1)
        
        OUT = (ONE_HOT * PHI) + ((1.0 - ONE_HOT) * COSINE)
        OUT = OUT * self.scale
        
        LOSS = self.CE(OUT, LABEL)
        return LOSS, OUT