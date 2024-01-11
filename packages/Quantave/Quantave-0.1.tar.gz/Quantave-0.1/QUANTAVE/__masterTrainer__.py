import os, tqdm
import argparse, torch
from QUANTAVE.__helper__ import *
from torch.utils.data import DataLoader
from QUANTAVE.Functions.Visualization import Graphs
from QUANTAVE.Tools.EvaluationMetrics import EqualErrorRate



class Objects:
    def __init__(self,
                 configurations:str or dict,
                 *args, **kwargs) -> None:

        self.config = ReadConfiurations(C=configurations)
        self.chalkboard = ChalkBoard(experiment_name=self.config["Experiment_Name"])
        self.MGPU = True if self.config["Training"]["Type"] == "MGPU" else False
        
        if not self.MGPU:
            self.device = Initialization().Set_device(gpu_id=self.config["Training"].get("GPU_ID", 0))

        # Functions Initializations
    
        self.dataset = Selector().Dataset(task=self.config["Dataset"]["Task"],
                                            dataset_name=self.config["Dataset"]["Name"],
                                            configurations=self.config["Dataset"]["Configurations"])

        self.architecture = Selector().Architectures(architecture_name=self.config["Architecture"]["Name"],
                                                     configurations=self.config["Architecture"]["Configurations"])
        
        self.criterion = Selector().Criterions(criterion_name=self.config["Criterion"]["Name"],
                                               configurations=self.config["Criterion"]["Configurations"])
        
        self.optimizer = Selector().Optimizers(optimizer_name=self.config["Optimizer"]["Name"],
                                               trainable_parameters=self.parameter_selector(selection=self.config["Training"].get("Train_Criterion", False)),
                                               configrations=self.config["Optimizer"]["Configurations"])
        
        if not self.MGPU:
            self.move_on_gpu(device=self.device)

    def architecture_forward(self, INPUT, *args, **kwargs):
        return self.architecture.forward(INPUT=INPUT, **kwargs)
    
    def criterion_forward(self, INPUT, LABELS, *args, **kwargs):
        return self.criterion.forward(INPUT=INPUT, LABEL=LABELS, **kwargs)


    def parameter_selector(self, selection:bool):
        if selection:
            return list(self.architecture.parameters())+list(self.criterion.parameters())
        else:
            return self.architecture.parameters()

    def move_on_gpu(self,
                    device:torch.device):    
        self.architecture.to(device)
        self.criterion.to(device)
        
    def load_trained_checkpoints(self,):
        if self.config["Training"]["Resume_Training_Checkpoint_Path"] != "":
            data = torch.load(f=self.config["Training"]["Resume_Training_Checkpoint_Path"])
            
            self.architecture.load_state_dict(state_dict=data["Architecture"])
            self.criterion.load_state_dict(state_dict=data["Criterion"])
            self.optimizer.load_state_dict(state_dict=data["Optimizer"])
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

        self.optimizer.zero_grad()
        LOSS, PREDICTION = self.forward(INPUT=DATA, LABELS=LABEL, Model_Type=self.config["Training"].get("Model_Type", "embedding"))
        LOSS.backward()
        self.optimizer.step()
        
        return LOSS.item(), LABEL.eq(PREDICTION.argmax(dim=1)).sum().div(self.config["Training"]["Batch_Size"]).mul(100).item()

    def train(self, training_dataloader, device:torch.device or int, *args, **kwargs):
        
        graph_loss, graph_training_metric = [], []
        total_minibatches = len(training_dataloader)
        E = self.load_trained_checkpoints()
        epoch_timer = Timer()
                
        for epoch in tqdm.tqdm(range(E, self.config["Training"]["Epochs"]+1),
                               desc=" Epochs",
                               position=0,
                               colour="blue"):

            epoch_timer.Start()
            self.architecture.train()
            self.criterion.train()
            torch.autograd.set_detect_anomaly(True)
            
            EpochLoss, EpochMetric = 0, 0
            
            for minibatch_idx, minibatch in enumerate(tqdm.tqdm(training_dataloader,
                                                                desc=" Minibatch",
                                                                position=1,
                                                                leave=False,
                                                                colour="cyan")):
                
                minibatch_loss, minibatch_metric = self.minibatch_processing_v0(minibatch_data=minibatch, device=device)
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
                evaluation_results = self.evaluate(device=device)
            else: evaluation_results = "Not calculated for this epoch"
            
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
            torch.save(
                {
                    "Epoch": epoch,
                    "Architecture": self.architecture.state_dict(),
                    "Criterion": self.criterion.state_dict(),
                    "Optimizer": self.optimizer.state_dict(),
                },
                f=self.chalkboard.checkpoint_path + f"/Epoch_{epoch}.pth"
            )           
    
    def evaluate(self, device:torch.device or int):
        timer = Timer()
        
        if self.config["Dataset"]["Name"] == "voxceleb":
            pair_list = self.dataset.evaluation_pair_list
        
        if self.config["Evaluation"]["Metric"] == "EER":
            timer.Start()
                
            self.architecture.eval()
            self.criterion.eval()
            
            eer, min_dcf = EqualErrorRate(forward_fn=self.architecture_forward,
                                          evaluation_pair_list=pair_list,
                                          device=device)
            evaluation_time = timer.Stop()
            return f"EER - {Round(eer)}, Min_DCF - {Round(min_dcf)}, Evaluation Time - {evaluation_time}"
        
        if self.config["Evaluation"]["Metric"] == "Accuracy":
            return "Not Implemented"
    



def proceed():
    P = argparse.ArgumentParser()
    P.add_argument("YAMLPath", type=str)
    A = P.parse_args()

    OBJECTS = Objects(configurations=A.YAMLPath)

    if OBJECTS.MGPU:
        _gpu_path = "/".join(__file__.split("/")[:-1])+"/__gpu__.py"
        os.system(" ".join(["python3",
                            _gpu_path,
                            A.YAMLPath]))
        
    else:
        GPUid = OBJECTS.config["Training"]["GPU_ID"]
        print(f"Single GPU Training on GPU {GPUid}")
        training_dataloader = DataLoader(dataset=OBJECTS.dataset,
                                            batch_size=OBJECTS.config["Training"]["Batch_Size"],
                                            shuffle=True,
                                            pin_memory=True,
                                            num_workers=OBJECTS.config["Training"].get("Number_Workers", 8),
                                            drop_last=True)
        OBJECTS.train(training_dataloader=training_dataloader,
                        device=OBJECTS.device)

if __name__ == "__main__":
    proceed()