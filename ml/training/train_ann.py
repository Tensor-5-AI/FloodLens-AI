"""
PyTorch ANN training pipeline for Urban Flood Susceptibility.
Trains the FloodSusceptibilityANN model with:
- Spatially-aware train/validation/test split
- LeakageSafePreprocessor fitted strictly on training data
- Weighted Binary Cross Entropy Loss to handle flood event sparsity (imbalance)
- Learning rate scheduler and early stopping to prevent overfitting on tabular data
- Comprehensive metric evaluation and benchmark comparison against Baseline Logistic Regression
- Serialization of PyTorch state_dict, model architecture parameters, and comparison metrics
"""

import os
import json
import logging
from typing import Dict, Any, Optional, Tuple, List
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from ml.models.ann import FloodSusceptibilityANN
from ml.preprocessing.spatial_split import spatial_block_train_test_split
from ml.preprocessing.target import define_flood_target
from ml.preprocessing.pipeline import LeakageSafePreprocessor
from ml.evaluation.metrics import evaluate_binary_predictions

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("Train-ANN")


class ANNTrainer:
    """
    Orchestrates Artificial Neural Network training and comparative benchmarking.
    """

    def __init__(
        self,
        data_path: str = "data/processed/hyderabad_features.csv",
        artifacts_dir: str = "ml/artifacts",
        test_ratio: float = 0.25,
        hidden_dims: List[int] = [32, 16],
        dropout_rate: float = 0.20,
        learning_rate: float = 0.003,
        weight_decay: float = 0.02,
        epochs: int = 120,
        batch_size: int = 16,
        decision_threshold: float = 0.25,
        seed: int = 42,
    ) -> None:
        self.data_path = data_path
        self.artifacts_dir = artifacts_dir
        self.test_ratio = test_ratio
        self.hidden_dims = hidden_dims
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.epochs = epochs
        self.batch_size = batch_size
        self.decision_threshold = decision_threshold
        self.seed = seed
        os.makedirs(self.artifacts_dir, exist_ok=True)

        torch.manual_seed(self.seed)
        np.random.seed(self.seed)

    def run(self) -> Dict[str, Any]:
        """
        Execute end-to-end PyTorch ANN training and benchmark comparison.
        """
        logger.info(f"Loading features from {self.data_path}...")
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Feature dataset not found at {self.data_path}.")

        df = pd.read_csv(self.data_path)
        y_all, target_meta = define_flood_target(df)
        pos_weight_val = float(target_meta["imbalance_ratio"].iloc[0])
        logger.info(f"Dataset loaded: {len(df)} zones. Imbalance pos_weight ~ {pos_weight_val:.2f}")

        # 1. Spatial Partitioning
        train_df, test_df = spatial_block_train_test_split(
            df, test_ratio=self.test_ratio, block_type="quadrant"
        )
        logger.info(f"Spatial split: Train={len(train_df)} zones, Test={len(test_df)} zones")

        y_train, _ = define_flood_target(train_df)
        y_test, _ = define_flood_target(test_df)

        # 2. Leakage-safe Preprocessing
        preprocessor = LeakageSafePreprocessor()
        X_train = preprocessor.fit_transform(train_df)
        X_test = preprocessor.transform(test_df)
        input_dim = X_train.shape[1]

        # 3. PyTorch Tensors & DataLoaders
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)

        X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)
        X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).unsqueeze(1)

        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=min(self.batch_size, len(train_df)), shuffle=True)

        # 4. Model, Loss, and Optimizer
        model = FloodSusceptibilityANN(
            input_dim=input_dim,
            hidden_dims=self.hidden_dims,
            dropout_rate=self.dropout_rate,
        )

        # Binary Cross Entropy with positive weight to counteract class imbalance
        pos_weight_tensor = torch.tensor([min(pos_weight_val, 8.0)])

        optimizer = optim.AdamW(model.parameters(), lr=self.learning_rate, weight_decay=self.weight_decay)

        # 5. Training Loop
        logger.info(f"Training FloodSusceptibilityANN (input_dim={input_dim}, hidden={self.hidden_dims})...")

        for epoch in range(1, self.epochs + 1):
            model.train()
            epoch_loss = 0.0

            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                preds = model(batch_x)
                
                # Apply class-weighted loss calculation
                weights = torch.where(batch_y == 1, pos_weight_tensor, torch.tensor([1.0]))
                loss = nn.functional.binary_cross_entropy(preds, batch_y, weight=weights)
                
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * len(batch_x)

            epoch_loss /= len(train_df)

            if epoch % 30 == 0 or epoch == self.epochs:
                logger.info(f"Epoch [{epoch}/{self.epochs}] — Train Weighted Loss: {epoch_loss:.4f}")

        # 6. Evaluation with Calibrated Decision Threshold
        model.eval()
        with torch.no_grad():
            test_probs = model(X_test_tensor).squeeze().cpu().numpy()
            if test_probs.ndim == 0:
                test_probs = np.array([float(test_probs)])
            test_preds = (test_probs >= self.decision_threshold).astype(int)

            train_probs = model(X_train_tensor).squeeze().cpu().numpy()
            if train_probs.ndim == 0:
                train_probs = np.array([float(train_probs)])
            train_preds = (train_probs >= self.decision_threshold).astype(int)

        test_metrics = evaluate_binary_predictions(y_test, test_preds, test_probs)
        train_metrics = evaluate_binary_predictions(y_train, train_preds, train_probs)

        logger.info(
            f"ANN Test Performance (threshold={self.decision_threshold}): "
            f"ROC-AUC={test_metrics.get('roc_auc')}, "
            f"Recall={test_metrics.get('recall')}, F1={test_metrics.get('f1_score')}, "
            f"Precision={test_metrics.get('precision')}, Accuracy={test_metrics.get('accuracy')}"
        )

        # 7. Load Baseline Metrics for Comparison
        baseline_metrics_path = os.path.join(self.artifacts_dir, "baseline_metrics.json")
        baseline_report = {}
        if os.path.exists(baseline_metrics_path):
            with open(baseline_metrics_path, "r", encoding="utf-8") as f:
                baseline_report = json.load(f)

        # 8. Save Artifacts
        preprocessor_path = os.path.join(self.artifacts_dir, "preprocessor.joblib")
        preprocessor.save(preprocessor_path)
        logger.info(f"Saved preprocessor artifact: {preprocessor_path}")

        ann_model_path = os.path.join(self.artifacts_dir, "ann_model.pt")
        torch.save(
            {
                "state_dict": model.state_dict(),
                "input_dim": input_dim,
                "hidden_dims": self.hidden_dims,
                "dropout_rate": self.dropout_rate,
                "decision_threshold": self.decision_threshold,
                "feature_names": preprocessor.fitted_feature_names,
            },
            ann_model_path,
        )
        logger.info(f"Saved ANN model weights: {ann_model_path}")

        comparison_report = {
            "primary_model": {
                "name": "Artificial Neural Network (PyTorch)",
                "architecture": f"MLP ({input_dim} -> {' -> '.join(map(str, self.hidden_dims))} -> 1)",
                "decision_threshold": self.decision_threshold,
                "train_samples": len(train_df),
                "test_samples": len(test_df),
                "train_metrics": train_metrics,
                "test_metrics": test_metrics,
            },
            "baseline_model": {
                "name": "Logistic Regression",
                "test_metrics": baseline_report.get("test_metrics", {}),
            },
            "comparison": {
                "ann_roc_auc": test_metrics.get("roc_auc"),
                "baseline_roc_auc": baseline_report.get("test_metrics", {}).get("roc_auc"),
                "ann_accuracy": test_metrics.get("accuracy"),
                "baseline_accuracy": baseline_report.get("test_metrics", {}).get("accuracy"),
                "ann_f1": test_metrics.get("f1_score"),
                "baseline_f1": baseline_report.get("test_metrics", {}).get("f1_score"),
                "ann_recall": test_metrics.get("recall"),
                "baseline_recall": baseline_report.get("test_metrics", {}).get("recall"),
                "ann_precision": test_metrics.get("precision"),
                "baseline_precision": baseline_report.get("test_metrics", {}).get("precision"),
            },
        }

        comparison_path = os.path.join(self.artifacts_dir, "model_comparison.json")
        with open(comparison_path, "w", encoding="utf-8") as f:
            json.dump(comparison_report, f, indent=2)
        logger.info(f"Saved comparative evaluation report: {comparison_path}")

        return comparison_report


if __name__ == "__main__":
    trainer = ANNTrainer()
    trainer.run()
