"""
Evaluation metrics calculation module for FloodLens AI models.
Computes Recall, F1 Score, ROC-AUC, Precision, Accuracy, and Confusion Matrix.
Avoids relying solely on Accuracy due to inherent spatial class imbalance in flood records.
"""

from typing import Dict, Any, Union, Optional
import numpy as np
from sklearn.metrics import (
    recall_score,
    f1_score,
    roc_auc_score,
    precision_score,
    accuracy_score,
    confusion_matrix,
    brier_score_loss,
)


def evaluate_binary_predictions(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
    y_prob: Optional[Union[np.ndarray, list]] = None,
) -> Dict[str, Any]:
    """
    Calculate comprehensive evaluation metrics for flood susceptibility classification.

    Parameters:
        y_true: Ground truth binary labels (0 or 1)
        y_pred: Predicted binary labels (0 or 1)
        y_prob: Predicted susceptibility probabilities in [0.0, 1.0]

    Returns:
        Dictionary of performance metrics including confusion matrix breakdown.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)

    # Confusion matrix elements: tn, fp, fn, tp
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    metrics: Dict[str, Any] = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
        "confusion_matrix": {
            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn),
        },
        "total_samples": int(len(y_true)),
        "positive_ground_truth": int(np.sum(y_true)),
    }

    if y_prob is not None:
        y_prob = np.asarray(y_prob, dtype=float)
        # Handle cases where all y_true are of one class
        try:
            metrics["roc_auc"] = round(float(roc_auc_score(y_true, y_prob)), 4)
        except ValueError:
            metrics["roc_auc"] = 0.5  # Undefined when only 1 class is present

        metrics["brier_score"] = round(float(brier_score_loss(y_true, y_prob)), 4)

    return metrics
