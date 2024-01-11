import os
import time
import yaml
import random
from typing import Any
import torch, numpy, json
from subprocess import Popen
from datetime import datetime
from QUANTAVE.Criterions import *
from QUANTAVE.Optimizers import *
from QUANTAVE.Architectures import *
from QUANTAVE.Dataloaders.Pipeline import *



Round = lambda A, decimal=4: round(A, ndigits=decimal)


class ChalkBoard(object):
    """ ChalkBoard Class """
    def __init__(self,
                 experiment_name:str) -> None:
        self.details_path = os.path.join(os.path.expanduser("~"), f"Results/{experiment_name.replace(' ', '_').upper()}")
        self.checkpoint_path = os.path.join(os.path.expanduser("~"), f"Results/{experiment_name.replace(' ', '_').upper()}/Checkpoints")
    
        self.file = os.path.join(self.details_path, "board.txt")
        self.experiment = experiment_name
        
        if not os.path.isdir(self.details_path):
            os.makedirs(self.details_path)
        if not os.path.isdir(self.checkpoint_path):
            os.makedirs(self.checkpoint_path)
        if not os.path.isfile(self.file):
            Popen(["touch", self.file])

        self.__initial_headers(self.file)
        
    def __datetime(self):
        data = str(datetime.now()).split()
        return " ".join([data[0], ":".join(data[-1].split(".")[0].split(":")[:2])])
    
    def __initial_headers(self, file:str):
        u = "_______"*16
        h = f"++++    ChalkBoard for Experiment [ {self.experiment} ]    ++++"
        t = self.__datetime()
        with open(file, "a") as F:
            F.write(h.center(120) + "\n")
            F.write(u.center(120) + "\n")
            F.write(t.center(120) + "\n")
            F.write(u.center(120) + "\n")
            F.write("\n")
            F.close()
    
    def scribe(self, *args):
        with open(self.file, "a") as F:
            F.write(f">>  {self.__datetime()}  >> " + ", ".join([str(i) for i in args]) + "\n")
            F.close()
    
    def subheading(self, *args):
        with open(self.file, "a") as F:
            F.write("_______"*16 + "\n")
            F.write(f">>  {self.__datetime()}  >> " + ", ".join([str(i) for i in args]) + "\n")
            F.write("_______"*16 + "\n")
            F.close()
    
    def seperaor(self,):
        with open(self.file, "a") as F: F.write("<|-|-|>"*16+"\n"); F.close()
    
    def write_json(self, json_data):
        with open(self.file, "a") as F: json.dump(json_data, F, ensure_ascii=False, indent=2)


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