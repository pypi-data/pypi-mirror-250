import os, json
from datetime import datetime
from subprocess import check_output, Popen



class ChalkBoard(object):
    """ ChalkBoard Class """
    def __init__(self,
                 experiment_name:str) -> None:
        self.details_path = os.path.join(os.getcwd(), f"Results/{experiment_name.upper()}")
        self.checkpoint_path = os.path.join(os.getcwd(), f"Results/{experiment_name.upper()}/Checkpoints")
    
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