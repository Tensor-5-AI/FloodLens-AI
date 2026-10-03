"""
Inference helper for scoring zone flood susceptibility.
Loads trained model and fitted preprocessor from artifacts to produce:
- Susceptibility score (0 to 100)
- Risk category (VERY LOW, LOW, MEDIUM, HIGH, VERY HIGH)
- Susceptibility probability
- Confidence score proxy
"""

from typing import Dict, Any, List, Union, Optional
import os
import joblib
import numpy as np
import pandas as pd

from ml.preprocessing.pipeline import LeakageSafePreprocessor


def get_risk_category(score: float) -> str:
    """
    Standard risk categorizations based on 0-100 susceptibility score.
    """
    if score >= 80.0:
        return "VERY HIGH"
    elif score >= 60.0:
        return "HIGH"
    elif score >= 40.0:
        return "MEDIUM"
    elif score >= 20.0:
        return "LOW"
    else:
        return "VERY LOW"


class FloodPredictor:
    """
    Inference service for predicting flood susceptibility on raw zone records or DataFrames.
    """

    def __init__(
        self,
        model_artifact_path: str = "ml/artifacts/baseline_model.joblib",
        preprocessor_artifact_path: str = "ml/artifacts/preprocessor.joblib",
    ) -> None:
        self.model_path = model_artifact_path
        self.preprocessor_path = preprocessor_artifact_path
        self.model = None
        self.preprocessor: Optional[LeakageSafePreprocessor] = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """
        Load model and preprocessor if paths exist. Supports both PyTorch (.pt) and Scikit-Learn (.joblib).
        """
        if os.path.exists(self.model_path) and os.path.exists(self.preprocessor_path):
            self.preprocessor = LeakageSafePreprocessor.load(self.preprocessor_path)
            if self.model_path.endswith(".pt"):
                import torch
                from ml.models.ann import FloodSusceptibilityANN
                checkpoint = torch.load(self.model_path, map_location="cpu")
                ann = FloodSusceptibilityANN(
                    input_dim=checkpoint["input_dim"],
                    hidden_dims=checkpoint.get("hidden_dims", [64, 32]),
                    dropout_rate=checkpoint.get("dropout_rate", 0.2),
                )
                ann.load_state_dict(checkpoint["state_dict"])
                self.decision_threshold = checkpoint.get("decision_threshold", 0.30)
                self.model = ann
            else:
                model_data = joblib.load(self.model_path)
                self.model = model_data.get("model", model_data)
                self.decision_threshold = 0.50

    def is_ready(self) -> bool:
        return self.model is not None and self.preprocessor is not None

    def predict_zone(self, zone_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict susceptibility for a single zone dictionary.
        """
        df = pd.DataFrame([zone_record])
        predictions = self.predict_dataframe(df)
        return predictions[0]

    def predict_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate predictions for a pandas DataFrame of zones.
        """
        if not self.is_ready():
            raise RuntimeError("Predictor is not ready. Train and persist model artifacts first.")

        X = self.preprocessor.transform(df)

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)[:, 1]
        elif hasattr(self.model, "forward"):  # PyTorch model
            import torch
            self.model.eval()
            with torch.no_grad():
                tensor_X = torch.tensor(X, dtype=torch.float32)
                probs = self.model(tensor_X).squeeze().numpy()
                if probs.ndim == 0:
                    probs = np.array([float(probs)])
        else:
            probs = self.model.predict(X).astype(float)

        results = []
        for idx, prob in enumerate(probs):
            prob_val = float(prob)
            score = round(prob_val * 100.0, 1)
            zone_id = df.iloc[idx].get("zone_id", f"ZONE_{idx:03d}")

            # Confidence proxy based on data completeness (0 missing indicator columns)
            missing_cols = ["rainfall_missing", "elevation_missing", "drainage_missing", "land_cover_missing"]
            missing_count = sum(int(df.iloc[idx].get(c, 0)) for c in missing_cols if c in df.columns)
            confidence = round(max(0.4, 1.0 - (missing_count * 0.15)), 2)

            results.append(
                {
                    "zone_id": zone_id,
                    "susceptibility_score": score,
                    "probability": round(prob_val, 4),
                    "risk_category": get_risk_category(score),
                    "confidence": confidence,
                }
            )

        return results
