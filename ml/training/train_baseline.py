"""
Baseline model training pipeline for Urban Flood Susceptibility.
Trains Logistic Regression with:
- Spatially-aware train/test partition (preventing spatial autocorrelation leakage)
- LeakageSafePreprocessor fitted strictly on training data
- Balanced class weighting to handle historical flood reporting imbalance
- Comprehensive metrics evaluation (Recall, F1-Score, ROC-AUC, Confusion Matrix)
- Model & preprocessor artifact serialization
"""

import os
import json
import logging
from typing import Dict, Any, Optional
import joblib
import pandas as pd

from ml.models.baseline import BaselineFloodModel
from ml.preprocessing.spatial_split import spatial_block_train_test_split
from ml.preprocessing.target import define_flood_target
from ml.preprocessing.pipeline import LeakageSafePreprocessor
from ml.evaluation.metrics import evaluate_binary_predictions

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("Train-Baseline")


class BaselineTrainer:
    """
    Orchestrates baseline Logistic Regression training, evaluation, and artifact storage.
    """

    def __init__(
        self,
        data_path: str = "data/processed/hyderabad_features.csv",
        artifacts_dir: str = "ml/artifacts",
        test_ratio: float = 0.25,
        c_param: float = 1.0,
    ) -> None:
        self.data_path = data_path
        self.artifacts_dir = artifacts_dir
        self.test_ratio = test_ratio
        self.c_param = c_param
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def run(self) -> Dict[str, Any]:
        """
        Execute end-to-end baseline training workflow.
        """
        logger.info(f"Loading feature dataset from {self.data_path}...")
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Feature dataset not found at {self.data_path}. Run ingestion first.")

        df = pd.read_csv(self.data_path)
        logger.info(f"Loaded dataset: shape {df.shape}")

        # 1. Target check
        y_all, target_meta = define_flood_target(df)
        logger.info(f"Target distribution: {target_meta.to_dict(orient='records')[0]}")

        # 2. Spatial Train/Test Split (ensuring no spatial leakage)
        train_df, test_df = spatial_block_train_test_split(
            df, test_ratio=self.test_ratio, block_type="quadrant"
        )
        logger.info(f"Spatial split: Train={len(train_df)} zones, Test={len(test_df)} zones")

        y_train, _ = define_flood_target(train_df)
        y_test, _ = define_flood_target(test_df)

        # 3. Fit Preprocessor STRICTLY on Training Split
        logger.info("Fitting LeakageSafePreprocessor on training partition...")
        preprocessor = LeakageSafePreprocessor()
        X_train = preprocessor.fit_transform(train_df)
        X_test = preprocessor.transform(test_df)

        # 4. Build and Train Model
        logger.info(f"Training Baseline Logistic Regression (C={self.c_param}, class_weight='balanced')...")
        baseline_wrapper = BaselineFloodModel(c_param=self.c_param)
        model = baseline_wrapper.build_model()
        model.fit(X_train, y_train)

        # 5. Evaluate on Test Split
        y_test_pred = model.predict(X_test)
        y_test_prob = model.predict_proba(X_test)[:, 1]

        test_metrics = evaluate_binary_predictions(y_test, y_test_pred, y_test_prob)
        logger.info(
            f"Test Performance: ROC-AUC={test_metrics.get('roc_auc')}, "
            f"Recall={test_metrics.get('recall')}, F1={test_metrics.get('f1_score')}, "
            f"Accuracy={test_metrics.get('accuracy')}"
        )

        # Also evaluate on Train split for overfit assessment
        y_train_pred = model.predict(X_train)
        y_train_prob = model.predict_proba(X_train)[:, 1]
        train_metrics = evaluate_binary_predictions(y_train, y_train_pred, y_train_prob)

        # 6. Save Artifacts
        model_path = os.path.join(self.artifacts_dir, "baseline_model.joblib")
        joblib.dump(
            {
                "model": model,
                "model_type": "LogisticRegression",
                "c_param": self.c_param,
                "feature_names": preprocessor.fitted_feature_names,
                "train_metrics": train_metrics,
                "test_metrics": test_metrics,
            },
            model_path,
        )
        logger.info(f"Saved model artifact: {model_path}")

        preprocessor_path = os.path.join(self.artifacts_dir, "preprocessor.joblib")
        preprocessor.save(preprocessor_path)
        logger.info(f"Saved preprocessor artifact: {preprocessor_path}")

        metrics_report = {
            "model": "LogisticRegression",
            "train_samples": len(train_df),
            "test_samples": len(test_df),
            "test_metrics": test_metrics,
            "train_metrics": train_metrics,
            "feature_coefficients": {
                feat: round(float(coef), 4)
                for feat, coef in zip(preprocessor.fitted_feature_names, model.coef_[0])
            },
        }

        report_path = os.path.join(self.artifacts_dir, "baseline_metrics.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(metrics_report, f, indent=2)
        logger.info(f"Saved evaluation metrics report: {report_path}")

        return metrics_report


if __name__ == "__main__":
    trainer = BaselineTrainer()
    trainer.run()
