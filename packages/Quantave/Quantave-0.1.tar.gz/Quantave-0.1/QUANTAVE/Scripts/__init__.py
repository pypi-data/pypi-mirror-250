import subprocess, os

class DatasetDownloader:
    def __init__(self,
                 dataset_name:str="voxceleb") -> None:
        
        if dataset_name == "voxceleb":
            self.voxceleb_downloader()


        # subprocess.run(args=["mkdir", "DATA"])
        # subprocess.run(args=["mkdir", f"DATA/{dataset_name}"])
        # subprocess.run(args=["ls"])
        
    def voxceleb_downloader(self,):
        subprocess.run(args=["echo", "Download Voxceleb data and rename folders in this format:"]) 