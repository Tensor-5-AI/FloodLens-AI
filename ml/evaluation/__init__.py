"""Model evaluation, spatial validation, ROC-AUC / PR-AUC metrics, and spatial error analysis."""

from ml.evaluation.metrics import evaluate_binary_predictions
from ml.evaluation.spatial_error import SpatialErrorAnalyzer, ERROR_COLOR_MAP, ERROR_DESCRIPTIONS

__all__ = [
    "evaluate_binary_predictions",
    "SpatialErrorAnalyzer",
    "ERROR_COLOR_MAP",
    "ERROR_DESCRIPTIONS",
]
