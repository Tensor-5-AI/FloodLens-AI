"""Primary Model: Artificial Neural Network (PyTorch) for Urban Flood Susceptibility."""
from typing import List
import torch
import torch.nn as nn


class FloodSusceptibilityANN(nn.Module):
    """
    Multilayer perceptron for non-linear feature interactions in flood susceptibility estimation.
    Accepts tabular environmental, terrain, and drainage features per zone.
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dims: List[int] = [64, 32],
        dropout_rate: float = 0.2,
    ) -> None:
        super().__init__()
        layers: List[nn.Module] = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            prev_dim = hidden_dim

        layers.append(nn.Linear(prev_dim, 1))
        layers.append(nn.Sigmoid())
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)
