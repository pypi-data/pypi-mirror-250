import torch

Adam = lambda **kwargs: torch.optim.Adam(**kwargs)

__all__ = ["Adam"]