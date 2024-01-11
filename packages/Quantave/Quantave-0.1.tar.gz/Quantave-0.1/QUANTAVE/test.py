import os, tqdm
import argparse, torch
from QUANTAVE.__helper__ import *
import torch.multiprocessing as MP
import torch.distributed as Distributed
from torch.utils.data import DataLoader
from QUANTAVE.Functions.Visualization import Graphs
from QUANTAVE.Tools.EvaluationMetrics import EqualErrorRate
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP


P = argparse.ArgumentParser()
P.add_argument("ObjectPath", type=str)
A = P.parse_args()


config = ReadConfiurations(A.ObjectPath)
chalkboard = ChalkBoard(experiment_name=config["Experiment_Name"])


def mgpu_setup(init_method, local_rank, rank, world_size, backend="nccl"):
    Distributed.init_process_group(backend=backend, init_method=init_method, world_size=world_size, rank=rank)
    device = torch.device("cuda:{}".format(local_rank))
    return device

def load_trained_checkpoints(architecture, criterion, optimizer):
    if config["Training"]["Resume_Training_Checkpoint_Path"] != "":
        data = torch.load(f=config["Training"]["Resume_Training_Checkpoint_Path"])
        
        architecture.load_state_dict(state_dict=data["Architecture"])
        criterion.load_state_dict(state_dict=data["Criterion"])
        optimizer.load_state_dict(state_dict=data["Optimizer"])
        return data["Epoch"]
    
    else: return 1

def train(dataloader, architecture, criterion, optimizer, device, model_type:str="embedding"):

    graph_loss, graph_training_metric = [], []
    total_minibatches = len(dataloader)
    E = load_trained_checkpoints(architecture, criterion, optimizer)
    epoch_timer = Timer()
    
    torch.nn.SyncBatchNorm.convert_sync_batchnorm(architecture)
            
    for epoch in tqdm.tqdm(range(E, config["Training"]["Epochs"]+1),
                           desc=" Epochs",
                           position=0,
                           colour="blue") if Distributed.get_rank()==0 else range(E, config["Training"]["Epochs"]+1):

        epoch_timer.Start()
        architecture.train()
        if config["Training"].get("Train_Criterion", False): criterion.train()
        torch.autograd.set_detect_anomaly(True)
        
        EpochLoss, EpochMetric = 0, 0
        
        for minibatch_idx, minibatch in enumerate(tqdm.tqdm(dataloader,
                                                            desc=" Minibatch",
                                                            position=1,
                                                            leave=False,
                                                            colour="cyan") if Distributed.get_rank()==0 else dataloader):

            #-----------------------------------------------#
            DATA, LABEL = minibatch
            DATA, LABEL = DATA.to(device), LABEL.to(device)
            #-----------------------------------------------#
            
            optimizer.zero_grad()
            
            #-----------------------------------------------#
            if model_type == "embedding":
                OUT = architecture.forward(DATA)
                LOSS, PREDICTIONS = criterion.forward(OUT, LABEL)

            elif model_type == "predictions":
                PREDICTIONS = architecture.forward(DATA)
                LOSS = criterion.forward(PREDICTIONS, LABEL)
            #-----------------------------------------------#
 
            LOSS.backward()
            optimizer.step()
            
            #-----------------------------------------------#
            metrics = ["Accuracy"]
            if config["Training"]["Training_Metric"] not in metrics: raise Exception(f"Training metric should be in {metrics}")

            if config["Training"]["Training_Metric"] == "Accuracy":
                METRIC = LABEL.eq(PREDICTIONS.argmax(dim=1)).sum().div(config["Training"]["Batch_Size"]).mul(100)
            #-----------------------------------------------#
             
            
            if Distributed.get_rank() == 0:
                if minibatch_idx % config["Training"]["Log_After_Minibatch"] == 0:
                    chalkboard.scribe(
                        "Epoch - {} :: {}/{}, Minibatch [Loss: {}, {}: {}]".format(
                            epoch,
                            minibatch_idx,
                            total_minibatches,
                            Round(LOSS.item()),
                            config["Training"]["Training_Metric"],
                            Round(METRIC.item()),
                        )
                    )
                    
            EpochLoss += LOSS.item()
            EpochMetric += METRIC.item()
        
        training_epoch_time = epoch_timer.Stop()
        graph_loss.append(Round(EpochLoss/total_minibatches))
        graph_training_metric.append(Round(EpochMetric/total_minibatches))

        if Distributed.get_rank()==0:
            if epoch%config["Evaluation"]["Calulate_After_Epochs"] == 0:
                evaluation_results = evaluate(dataloader.dataset, architecture, criterion, architecture.forward, device=device)
            else: evaluation_results = "Not calculated for this epoch"
            
            chalkboard.scribe(
            "Epoch - {}, Loss - {}, {} - {}, Training Time - {}".format(
                epoch,
                Round(EpochLoss/total_minibatches),
                config["Training"]["Training_Metric"],
                Round(EpochMetric/total_minibatches),
                training_epoch_time,
            ),
            evaluation_results
            )
        
        Graphs().LineGraph(data=graph_loss, title="Loss Graph", x_axis="Epochs", y_axis="Loss Value", line_label="Loss", line_color="#b83535",
                        save_image_path=os.path.join(chalkboard.details_path, "Loss.png"))
        Graphs().LineGraph(data=graph_training_metric, title=config["Training"]["Training_Metric"]+" Graph", x_axis="Epochs", line_color="#2335a8",
                        y_axis=config["Training"]["Training_Metric"]+ " Graph", line_label=config["Training"]["Training_Metric"],
                        save_image_path=os.path.join(chalkboard.details_path, config["Training"]["Training_Metric"]+".png"))
        
        if Distributed.get_rank() == 0:
            torch.save(
            {
                "Epoch": epoch,
                "Architecture": architecture.state_dict(),
                "Criterion": criterion.state_dict(),
                "Optimizer": optimizer.state_dict(),
            },
            f=chalkboard.checkpoint_path + f"/Epoch_{epoch}.pth"
        )           


def evaluate(dataset, architecture, criterion, architecture_forward, device:torch.device or int):
        timer = Timer()
        
        if config["Dataset"]["Name"] == "voxceleb":
            pair_list = dataset.evaluation_pair_list
        
        if config["Evaluation"]["Metric"] == "EER":
            timer.Start()
                
            architecture.eval()
            criterion.eval()
            
            eer, min_dcf = EqualErrorRate(forward_fn=architecture_forward,
                                          evaluation_pair_list=pair_list,
                                          device=device)
            evaluation_time = timer.Stop()
            return f"EER - {Round(eer)}, Min_DCF - {Round(min_dcf)}, Evaluation Time - {evaluation_time}"
        
        if config["Evaluation"]["Metric"] == "Accuracy":
            return "Not Implemented"
    

def main(local_rank, ngpus_per_node, mgpu_arguments):
    
    mgpu_arguments.local_rank = local_rank
    mgpu_arguments.rank = mgpu_arguments.node_rank * ngpus_per_node + local_rank

    device = mgpu_setup(init_method=mgpu_arguments.dist_url,
                        local_rank=mgpu_arguments.local_rank,
                        rank=mgpu_arguments.rank,
                        world_size=mgpu_arguments.world_size)
    
    dataset = Selector().Dataset(task=config["Dataset"]["Task"],
                                 dataset_name=config["Dataset"]["Name"],
                                 configurations=config["Dataset"]["Configurations"])
    
    bs = config["Training"]["Batch_Size"]//mgpu_arguments.world_size
    dataloader = DataLoader(dataset=dataset,
                            batch_size=bs,
                            sampler=DistributedSampler(dataset, shuffle=False))
    
    architecture = Selector().Architectures(architecture_name=config["Architecture"]["Name"],
                                            configurations=config["Architecture"]["Configurations"])
    architecture = architecture.to(device)
    architecture = DDP(module=architecture,
                       device_ids=[mgpu_arguments.local_rank])
    
    criterion = Selector().Criterions(criterion_name=config["Criterion"]["Name"],
                                      configurations=config["Criterion"]["configurations"])
    
    optimizer = Selector().Optimizers(optimizer_name=config["Optimizer"]["Name"],
                                      trainable_parameters=list(architecture.parameters())+list(criterion.parameters()) \
                                                   if config["Training"].get("Train_Criterion", False) else architecture.parameters(),
                                      configrations=config["Optimizer"]["Configurations"])
    
    train(dataloader=dataloader,
          architecture=architecture,
          criterion=criterion,
          optimizer=optimizer,
          device=device,
          model_type=config["Training"]["Model_Type"])
    Distributed.destroy_process_group()



if __name__ == "__main__":
    mgpu_arguments = argparse.Namespace()
    mgpu_arguments.nodes = config["Training"]["MGPU_Configurations"]["nodes"]
    mgpu_arguments.ngpus_per_node = config["Training"]["MGPU_Configurations"]["ngpus_per_node"]
    mgpu_arguments.dist_url = "tcp://127.0.0.1:23500"
    mgpu_arguments.node_rank = 0
    mgpu_arguments.world_size = mgpu_arguments.ngpus_per_node * mgpu_arguments.nodes
    
    MP.spawn(main,
                   nprocs=mgpu_arguments.ngpus_per_node,
                   args=(mgpu_arguments.ngpus_per_node, mgpu_arguments,))




























# main(A)
# OBJECTS = Objects(A.ObjectPath)

# def mgpu_setup(rank, world_size):
#     os.environ["MASTER_ADDR"] = "localhost"
#     os.environ["MASTER_PORT"] = "23456"
#     Distributed.init_process_group(backend="nccl", rank=rank, world_size=world_size)
#     torch.cuda.set_device(rank)

# def run(rank, world_size):
#     mgpu_setup(rank, world_size)
#     training_dataloader = DataLoader(dataset=OBJECTS.dataset,
#                                      batch_size=OBJECTS.config["Training"]["Batch_Size"],
#                                      sampler=DistributedSampler(OBJECTS.dataset, shuffle=True),
#                                      pin_memory=True,
#                                      shuffle=False)
#     OBJECTS.train(training_dataloader,
#                   rank,
#                   True) 
#     Distributed.destroy_process_group()

# def main():
#     world_size = OBJECTS.config["Training"]["MGPU_Configurations"]["nodes"] * OBJECTS.config["Training"]["MGPU_Configurations"]["ngpus_per_node"]
#     MP.spawn(run, nprocs=world_size, args=(world_size,))



# if __name__ == "__main__":
#     main()
    # MGPU_CONFIGS = argparse.Namespace()
        
    # if list(OBJECTS.config["Training"]["MGPU_Configurations"].keys()) != ["nodes", "ngpu_per_node"]:
    #     raise Exception("[node, ngpu_per_node] must be available as keys.")
    
    # MGPU_CONFIGS.nodes = OBJECTS.config["Training"]["MGPU_Configurations"]["nodes"]
    # MGPU_CONFIGS.ngpu_per_node = OBJECTS.config["Training"]["MGPU_Configurations"]["ngpu_per_node"]
    # MGPU_CONFIGS.dist_url = "tcp://127.0.0.1:12355"
    # MGPU_CONFIGS.node_rank = 0
    
    # def mgpu_setup(init_method:str, local_rank:int, rank:int, world_size:int, backend:str="nccl"):
    #     Distributed.init_process_group(backend=backend,
    #                                     init_method=init_method,
    #                                     world_size=world_size,
    #                                     rank=rank)
    #     return torch.device(f"cuda:{local_rank}")
    
    # def run(local_rank, ngpus_per_node, mgpu_arguments):

    #     mgpu_arguments.local_rank = local_rank
    #     mgpu_arguments.rank = mgpu_arguments.node * ngpus_per_node + local_rank
        
    #     device = mgpu_setup(init_method=mgpu_arguments.dist_url,
    #                         local_rank=mgpu_arguments.local_rank,
    #                         rank=mgpu_arguments.rank,
    #                         world_size=mgpu_arguments.world_size)
        
    #     bs = OBJECTS.config["Training"]["Batch_Size"] // mgpu_arguments.world_size
    #     data_sampler = DistributedSampler(OBJECTS.dataset, shuffle=True)
    #     training_dataloader = DataLoader(dataset=OBJECTS.dataset,
    #                                         batch_size=bs,
    #                                         sampler=data_sampler)
        
    #     OBJECTS.architecture = OBJECTS.architecture.to(device)
    #     OBJECTS.architecture = DDP(module=OBJECTS.architecture,
    #                                 device_ids=[mgpu_arguments.local_rank],
    #                                 output_device=mgpu_arguments.local_rank)
        
    #     if OBJECTS.config["Training"].get("Train_Criterion", False):
    #         OBJECTS.criterion = OBJECTS.criterion.to(device)
    #         OBJECTS.criterion = DDP(module=OBJECTS.criterion,
    #                                 device_ids=[mgpu_arguments.local_rank],
    #                                 output_device=mgpu_arguments.local_rank)
        
    #     OBJECTS.train(training_dataloader=training_dataloader,
    #                     device=device,
    #                     sampler=True)

    # MGPU_CONFIGS.world_size = MGPU_CONFIGS.ngpu_per_node * MGPU_CONFIGS.nodes

    # MP.spawn(run,
    #          nprocs=MGPU_CONFIGS.ngpu_per_node,
    #          args=(MGPU_CONFIGS.ngpu_per_node, MGPU_CONFIGS),
    #          join=True,
    #          daemon=False,
    #          start_method="spawn")
