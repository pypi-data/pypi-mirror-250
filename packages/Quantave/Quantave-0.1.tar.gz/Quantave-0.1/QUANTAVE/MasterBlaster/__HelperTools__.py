import os
import time
import yaml
import random
import platform
import torch, numpy
from typing import Any
from ..Criterions import *
from ..Optimizers import *
from ..Architectures import *
from ..Dataloaders.Pipeline import *
import torch.distributed as Distributed


Round = lambda A, decimal=4: round(A, ndigits=decimal)

def ReadConfiurations(C:list or dict):    
    if type(C) == dict:
        return C
    elif type(C) == str:
        with open(C, "r") as F: config = yaml.safe_load(F); F.close()
        return config
    
    
class Initialization:
    def __init__(self) -> None:
        pass

    def Set_Seed(self, random_seed:int=5943728):
        torch.manual_seed(random_seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        numpy.random.seed(random_seed)
        random.seed(random_seed)
    
    def Set_device(self, gpu_id:str):
        return torch.device(f"cuda:{gpu_id}")
    
    
        
class Selector:
    def __init__(self) -> None:
        pass
    
    def Dataset(self, task: str, dataset_name:str, configurations:dict):
        if task == "Speaker Verification":
            return SpeakerVerification(dataset_name=dataset_name,
                                       configurations=configurations)
    
    def Architectures(self, architecture_name:str, configurations:dict):
        if architecture_name == "ECAPA-TDNN":
            return ECAPA_TDNN(**configurations)


    def Criterions(self, criterion_name:str, configurations:dict):
        if criterion_name == "AAMSoftmax":
            return AAM_Softmax(**configurations)
        
            
    def Optimizers(self, optimizer_name:str, trainable_parameters:Any, configrations:dict):
        if optimizer_name == "Adam":
            return Adam(params=trainable_parameters, **configrations)
        
        
class Timer:
    def __init__(self) -> None:
        self.start_time = None

    def Start(self,):
        self.start_time = time.time()
    
    def Stop(self):
        hours, remaining = divmod(time.time() - self.start_time, 3600)
        minutes, seconds = divmod(remaining, 60)
        o = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds).split(".")[0]
        self.start_time = None
        return o
    
class Multi_GPU:
    def __init__(self) -> None:
        pass
    
    def setup(self,):
        rank = int(os.environ["RANK"])
        local_rank = int(os.environ["LOCAL_RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        Distributed.init_process_group(backend="nccl" if platform.system()=="Linux" else "gloo")
        device = torch.device("cuda:{}".format(local_rank))
        return rank, local_rank, world_size, device