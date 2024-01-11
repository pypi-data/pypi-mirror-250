import torch
from scipy.spatial.distance import squareform

RecursionMatrix = lambda Audio_segment, Max_Value: torch.tensor(
    squareform(torch.where(
        torch.nn.functional.pdist(Audio_segment[:,None]).div(0.10).floor()<Max_Value,
        torch.nn.functional.pdist(Audio_segment[:,None]).div(0.10).floor(),
        Max_Value))
    )
