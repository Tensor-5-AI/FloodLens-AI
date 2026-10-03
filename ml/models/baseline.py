"""Baseline Model: Logistic Regression for Urban Flood Susceptibility."""
from typing import Optional
from sklearn.linear_model import LogisticRegression


class BaselineFloodModel:
    """
    Transparent, linear baseline model serving as benchmark against the Artificial Neural Network.
    """

    def __init__(self, c_param: float = 1.0, max_iter: int = 1000) -> None:
        self.c_param = c_param
        self.max_iter = max_iter
        self.model: Optional[LogisticRegression] = None

    def build_model(self) -> LogisticRegression:
        self.model = LogisticRegression(
            C=self.c_param,
            max_iter=self.max_iter,
            solver="lbfgs",
            class_weight="balanced",
        )
        return self.model
