import os
import argparse
import torch, yaml, dill
from .__HelperTools__ import *
import torch.multiprocessing as MP
from .__Chalkboard__ import ChalkBoard
from torch.utils.data import DataLoader
import torch.distributed as Distributed
from ..Functions.Visualization import Graphs
from ..Tools.EvaluationMetrics import EqualErrorRate
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP




class Trainer:
    def __init__(self,
                 configurations:str or dict,
                 *args, **kwargs) -> None:

        self.config = ReadConfiurations(C=configurations)
        self.chalkboard = ChalkBoard(experiment_name=self.config["Experiment_Name"])
        self.MGPU = True if self.config["Training"]["Type"] == "MGPU" else False
        
        if not self.MGPU:
            self.device = Initialization().Set_device(gpu_id=self.config["Training"].get("GPU_ID", 0))

        # Functions Initializations
    
        self.__dataset = Selector().Dataset(task=self.config["Dataset"]["Task"],
                                            dataset_name=self.config["Dataset"]["Name"],
                                            configurations=self.config["Dataset"]["Configurations"])

        self.__architecture = Selector().Architectures(architecture_name=self.config["Architecture"]["Name"],
                                                     configurations=self.config["Architecture"]["Configurations"])
        
        self.__criterion = Selector().Criterions(criterion_name=self.config["Criterion"]["Name"],
                                               configurations=self.config["Criterion"]["Configurations"])
                
        if self.MGPU:
            self.__architecture = dill.loads(dill.dumps(self.__architecture))
            if self.config["Training"].get("Train_Criterion", False):
                self.__criterion = dill.loads(dill.dumps(self.__criterion))
        
        
        self.__optimizer = Selector().Optimizers(optimizer_name=self.config["Optimizer"]["Name"],
                                               trainable_parameters=self.__parameter_selector(selection=self.config["Training"].get("Train_Criterion", False)),
                                               configrations=self.config["Optimizer"]["Configurations"])
        

        self.architecture_forward = lambda INPUT, *args, **kwargs: self.__architecture.forward(INPUT=INPUT, **kwargs)
        self.criterion_forward = lambda INPUT, LABELS, *args, **kwargs: self.__criterion.forward(INPUT=INPUT, LABEL=LABELS, **kwargs)
        
        if not self.MGPU:
            self.__move_on_gpu(device=self.device)

    def __parameter_selector(self,
                             selection:bool):
        if selection:
            return list(self.__architecture.parameters())+list(self.__criterion.parameters())
        else:
            return self.__architecture.parameters()

    def __move_on_gpu(self,
                    device:torch.device):    
        self.__architecture.to(device)
        self.__criterion.to(device)
        
    def __load_trained_checkpoints(self,):
        if self.config["Training"]["Resume_Training_Checkpoint_Path"] != "":
            data = torch.load(f=self.config["Training"]["Resume_Training_Checkpoint_Path"])
            
            self.__architecture.load_state_dict(state_dict=data["Architecture"])
            self.__criterion.load_state_dict(state_dict=data["Criterion"])
            self.__optimizer.load_state_dict(state_dict=data["Optimizer"])
            return data["Epoch"]
        
        else: return 1

    def forward(self, INPUT:torch.Tensor, LABELS:torch.Tensor, Model_Type:str="embedding"):
        if Model_Type == "embedding":
            OUT = self.architecture_forward(INPUT=INPUT)
            LOSS, PREDICTIONS = self.criterion_forward(INPUT=OUT, LABELS=LABELS)
            return LOSS, PREDICTIONS

        elif Model_Type == "predictions":
            OUT = self.architecture_forward(INPUT=INPUT)
            return self.criterion_forward(INPUT=OUT, LABELS=LABELS), OUT
        
    def minibatch_processing_v0(self, minibatch_data:tuple, device:torch.device or int):
        DATA, LABEL = minibatch_data
        DATA, LABEL = DATA.to(device), LABEL.to(device)

        self.__optimizer.zero_grad()
        LOSS, PREDICTION = self.forward(INPUT=DATA, LABELS=LABEL, Model_Type=self.config["Training"].get("Model_Type", "embedding"))
        LOSS.backward()
        self.__optimizer.step()
        
        return LOSS.item(), LABEL.eq(PREDICTION.argmax(dim=1)).sum().div(self.config["Training"]["Batch_Size"]).mul(100).item()

    def __train(self, training_dataloader, device:torch.device or int, sampler=False, *args, **kwargs):
        
        graph_loss, graph_training_metric = [], []
        total_minibatches = len(training_dataloader)
        E = self.__load_trained_checkpoints()
        epoch_timer = Timer()
                
        for epoch in range(E, self.config["Training"]["Epochs"]+1):
            if sampler:
                training_dataloader.sampler.set_epoch(epoch)
    
            epoch_timer.Start()

            self.__architecture.train()
            self.__criterion.train()
            torch.autograd.set_detect_anomaly(True)
            
            EpochLoss, EpochMetric = 0, 0
            
            for minibatch_idx, minibatch in enumerate(training_dataloader):
                
                minibatch_loss, minibatch_metric = self.minibatch_processing_v0(minibatch_data=minibatch, device=device)
                
                
                if self.MGPU:
                    if (minibatch_idx % self.config["Training"]["Log_After_Minibatch"] == 0) and (Distributed.get_rank() == 0):
                        self.chalkboard.scribe(
                            "Epoch - {} :: {}/{}, Minibatch [Loss: {}, {}: {}]".format(
                                epoch,
                                minibatch_idx,
                                total_minibatches,
                                Round(minibatch_loss),
                                self.config["Training"]["Training_Metric"],
                                Round(minibatch_metric),
                            )
                        )
                else:
                    if minibatch_idx % self.config["Training"]["Log_After_Minibatch"] == 0:
                        self.chalkboard.scribe(
                            "Epoch - {} :: {}/{}, Minibatch [Loss: {}, {}: {}]".format(
                                epoch,
                                minibatch_idx,
                                total_minibatches,
                                Round(minibatch_loss),
                                self.config["Training"]["Training_Metric"],
                                Round(minibatch_metric),
                            )
                        )
                    
                EpochLoss += minibatch_loss
                EpochMetric += minibatch_metric
            
            training_epoch_time = epoch_timer.Stop()
            graph_loss.append(Round(EpochLoss/total_minibatches))
            graph_training_metric.append(Round(EpochMetric/total_minibatches))

            if epoch%self.config["Evaluation"]["Calulate_After_Epochs"] == 0:
                evaluation_results = self.__evaluate(device=device)
            else: evaluation_results = "Not calculated for this epoch"
            
            if self.MGPU:
                if Distributed.get_rank() == 0:
                    self.chalkboard.scribe(
                        "Epoch - {}, Loss - {}, {} - {}, Training Time - {}".format(
                            epoch,
                            Round(EpochLoss/total_minibatches),
                            self.config["Training"]["Training_Metric"],
                            Round(EpochMetric/total_minibatches),
                            training_epoch_time,
                        ),
                        evaluation_results
                    )
            else:
                self.chalkboard.scribe(
                "Epoch - {}, Loss - {}, {} - {}, Training Time - {}".format(
                    epoch,
                    Round(EpochLoss/total_minibatches),
                    self.config["Training"]["Training_Metric"],
                    Round(EpochMetric/total_minibatches),
                    training_epoch_time,
                ),
                evaluation_results
                )
            
            Graphs().LineGraph(data=graph_loss, title="Loss Graph", x_axis="Epochs", y_axis="Loss Value", line_label="Loss", line_color="#b83535",
                            save_image_path=os.path.join(self.chalkboard.details_path, "Loss.png"))
            Graphs().LineGraph(data=graph_training_metric, title=self.config["Training"]["Training_Metric"]+" Graph", x_axis="Epochs", line_color="#2335a8",
                            y_axis=self.config["Training"]["Training_Metric"]+ " Graph", line_label=self.config["Training"]["Training_Metric"],
                            save_image_path=os.path.join(self.chalkboard.details_path, self.config["Training"]["Training_Metric"]+".png"))
            if self.MGPU:
                if Distributed.get_rank() == 0:
                    torch.save(
                        {
                            "Epoch": epoch,
                            "Architecture": self.__architecture.module.state_dict(),
                            "Criterion": self.__criterion.module.state_dict() if self.config["Training"].get("Train_Criterion", False) else self.__criterion.state_dict(),
                            "Optimizer": self.__optimizer.state_dict(),
                        },
                        f=self.chalkboard.checkpoint_path + f"/Epoch_{epoch}.pth"
                    )
            else:
                torch.save(
                    {
                        "Epoch": epoch,
                        "Architecture": self.__architecture.state_dict(),
                        "Criterion": self.__criterion.state_dict(),
                        "Optimizer": self.__optimizer.state_dict(),
                    },
                    f=self.chalkboard.checkpoint_path + f"/Epoch_{epoch}.pth"
                )           
    
    def __evaluate(self, device:torch.device or int):
        timer = Timer()
        
        if self.config["Dataset"]["Name"] == "voxceleb":
            pair_list = self.__dataset.evaluation_pair_list
        
        if self.config["Evaluation"]["Metric"] == "EER":
            timer.Start()
                
            self.__architecture.eval()
            self.__criterion.eval()
            
            eer, min_dcf = EqualErrorRate(forward_fn=self.architecture_forward,
                                          evaluation_pair_list=pair_list,
                                          device=device)
            evaluation_time = timer.Stop()
            return f"EER - {Round(eer)}, Min_DCF - {Round(min_dcf)}, Evaluation Time - {evaluation_time}"
        
        if self.config["Evaluation"]["Metric"] == "Accuracy":
            return "Not Implemented"
    
    def proceed(self,):
        if self.MGPU:
            MGPU_CONFIGS = argparse.Namespace()
            
            if list(self.config["Training"]["MGPU_Configurations"].keys()) != ["nodes", "ngpu_per_node"]:
                raise Exception("[node, ngpu_per_node] must be available as keys.")
            
            MGPU_CONFIGS.nodes = self.config["Training"]["MGPU_Configurations"]["nodes"]
            MGPU_CONFIGS.ngpu_per_node = self.config["Training"]["MGPU_Configurations"]["ngpu_per_node"]
            MGPU_CONFIGS.dist_url = "tcp://127.0.0.1:12355"
            MGPU_CONFIGS.node_rank = 0
            
            def mgpu_setup(init_method:str, local_rank:int, rank:int, world_size:int, backend:str="nccl"):
                Distributed.init_process_group(backend=backend,
                                               init_method=init_method,
                                               world_size=world_size,
                                               rank=rank)
                return torch.device(f"cuda:{local_rank}")
            
            def run(local_rank, ngpus_per_node, mgpu_arguments):

                mgpu_arguments.local_rank = local_rank
                mgpu_arguments.rank = mgpu_arguments.node * ngpus_per_node + local_rank
                
                device = mgpu_setup(init_method=mgpu_arguments.dist_url,
                                    local_rank=mgpu_arguments.local_rank,
                                    rank=mgpu_arguments.rank,
                                    world_size=mgpu_arguments.world_size)
                
                bs = self.config["Training"]["Batch_Size"] // mgpu_arguments.world_size
                data_sampler = DistributedSampler(self.__dataset, shuffle=True)
                training_dataloader = DataLoader(dataset=self.__dataset,
                                                 batch_size=bs,
                                                 sampler=data_sampler)
                
                self.__architecture = self.__architecture.to(device)
                self.__architecture = DDP(module=self.__architecture,
                                          device_ids=[mgpu_arguments.local_rank],
                                          output_device=mgpu_arguments.local_rank)
                
                if self.config["Training"].get("Train_Criterion", False):
                    self.__criterion = self.__criterion.to(device)
                    self.__criterion = DDP(module=self.__criterion,
                                           device_ids=[mgpu_arguments.local_rank],
                                           output_device=mgpu_arguments.local_rank)
                
                self.__train(training_dataloader=training_dataloader,
                             device=device,
                             sampler=True)

            MGPU_CONFIGS.world_size = MGPU_CONFIGS.ngpu_per_node * MGPU_CONFIGS.nodes

            MP.spawn(dill.dumps(run), nprocs=MGPU_CONFIGS.ngpu_per_node, args=(MGPU_CONFIGS.ngpu_per_node, MGPU_CONFIGS))
        
        else:
            training_dataloader = DataLoader(dataset=self.__dataset,
                                             batch_size=self.config["Training"]["Batch_Size"],
                                             shuffle=True,
                                             pin_memory=True,
                                             num_workers=self.config["Training"].get("Number_Workers", 8),
                                             drop_last=True)
            self.__train(training_dataloader=training_dataloader,
                         device=self.device)
        

            
        

class MGPU_TRAINER:
    def __init__(self,
                 configurations:str or dict,
                 *args, **kwargs) -> None:

        if type(configurations) == dict:
            self.config = configurations
        elif type(configurations) == str:
            with open(configurations, "r") as F: self.config = yaml.safe_load(F); F.close()
        
        Initialization().Set_Seed(random_seed=self.config.get("Seed", 5943728))
        gpu_id = self.config["Training"].get("GPU_ID", 0)
        self.device = torch.device(f"cuda:{gpu_id}")

        self.chalkboard = ChalkBoard(experiment_name=self.config["Experiment_Name"])
