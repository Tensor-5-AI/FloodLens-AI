import os
import json
import logging
from typing import Any, Dict, List, Optional
import pandas as pd

from ml.explainability.explainer import FloodExplainer, CAUSALITY_DISCLAIMER
from backend.app.services.spatial import SpatialDataService

logger = logging.getLogger(__name__)


class ModelInferenceService:
    """
    Service responsible for loading trained models (PyTorch ANN / Baseline Logistic Regression),
    generating zone susceptibility predictions, and providing local & global SHAP explanations.
    """

    def __init__(
        self,
        model_artifacts_dir: str = "./ml/artifacts",
        data_dir: str = "./data/processed",
    ) -> None:
        self.model_artifacts_dir = model_artifacts_dir
        self.data_dir = data_dir
        self.spatial_service = SpatialDataService(data_dir=data_dir)

        self.predictor: Optional[Any] = None
        self.explainer: Optional[FloodExplainer] = None
        self.is_loaded = False

        self._cached_zone_explanations: Optional[Dict[str, Any]] = None
        self._cached_global_explanation: Optional[Dict[str, Any]] = None

        self._initialize_service()

    def _initialize_service(self, model_name: str = "primary_ann") -> None:
        """Initialize both the predictor and explainability engine."""
        try:
            from ml.inference.predictor import FloodPredictor

            ann_path = os.path.join(self.model_artifacts_dir, "ann_model.pt")
            baseline_path = os.path.join(self.model_artifacts_dir, "baseline_model.joblib")
            preprocessor_path = os.path.join(self.model_artifacts_dir, "preprocessor.joblib")

            model_path = ann_path if (model_name == "primary_ann" and os.path.exists(ann_path)) else baseline_path

            if os.path.exists(model_path) and os.path.exists(preprocessor_path):
                self.predictor = FloodPredictor(
                    model_artifact_path=model_path,
                    preprocessor_artifact_path=preprocessor_path,
                )
                self.is_loaded = self.predictor.is_ready()

            # Initialize explainer
            features_csv = os.path.join(self.data_dir, "hyderabad_features.csv")
            if os.path.exists(model_path) and os.path.exists(preprocessor_path):
                self.explainer = FloodExplainer(
                    model_artifact_path=model_path,
                    preprocessor_artifact_path=preprocessor_path,
                    background_data_path=features_csv,
                )

            # Warm caches if precomputed artifacts exist
            self._load_cached_artifacts()
            logger.info("ModelInferenceService initialized successfully.")
        except Exception as e:
            logger.warning(f"Could not fully load inference service: {e}")

    def _load_cached_artifacts(self) -> None:
        """Load precomputed SHAP explanations if present on disk."""
        local_path = os.path.join(self.model_artifacts_dir, "zone_explanations.json")
        global_path = os.path.join(self.model_artifacts_dir, "shap_global_importance.json")

        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    self._cached_zone_explanations = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cached zone explanations: {e}")

        if os.path.exists(global_path):
            try:
                with open(global_path, "r", encoding="utf-8") as f:
                    self._cached_global_explanation = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cached global explanation: {e}")

    def load_model(self, model_name: str = "primary_ann") -> None:
        """Switch or reload active model (primary_ann vs baseline)."""
        logger.info(f"Loading model {model_name} from {self.model_artifacts_dir}")
        self._initialize_service(model_name=model_name)

    def predict_susceptibility(self, features: Dict[str, Any]) -> float:
        """Generate susceptibility prediction score (0-100) for a given feature vector."""
        if self.predictor is not None and self.predictor.is_ready():
            res = self.predictor.predict_zone(features)
            return float(res["susceptibility_score"])
        return 0.0

    def predict_zone(self, zone_id: str, study_area: str = "Hyderabad") -> Optional[Dict[str, Any]]:
        """Retrieve zone features and generate susceptibility prediction."""
        features = self.spatial_service.get_zone_features(zone_id=zone_id, study_area=study_area)
        if features is None:
            return None
        if self.predictor is not None and self.predictor.is_ready():
            return self.predictor.predict_zone(features)
        return None

    def explain_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Generate on-the-fly local SHAP explanation for a raw feature dictionary."""
        if self.explainer is None:
            raise RuntimeError("Explainability engine is not loaded.")
        return self.explainer.explain_instance(features)

    def explain_zone(self, zone_id: str, study_area: str = "Hyderabad") -> Optional[Dict[str, Any]]:
        """
        Produce local SHAP explanation for a specific zone.
        Uses cached explanation if available for instant response, or computes dynamically.
        """
        normalized_id = str(zone_id).upper().strip()

        # Check precomputed cache first for instant sub-millisecond response
        if self._cached_zone_explanations and normalized_id in self._cached_zone_explanations:
            return self._cached_zone_explanations[normalized_id]

        # Case-insensitive match in cache
        if self._cached_zone_explanations:
            for k, v in self._cached_zone_explanations.items():
                if k.upper() == normalized_id:
                    return v

        # Dynamic computation if not in cache
        zone_features = self.spatial_service.get_zone_features(zone_id=zone_id, study_area=study_area)
        if zone_features is None:
            return None

        if self.explainer is not None and self.explainer.is_ready():
            return self.explainer.explain_instance(zone_features)

        return None

    def get_global_explanation(self, study_area: str = "Hyderabad") -> Dict[str, Any]:
        """
        Retrieve global SHAP feature importance rankings across all study area zones.
        """
        if self._cached_global_explanation:
            return self._cached_global_explanation

        if self.explainer is not None and self.explainer.is_ready():
            all_features_df = self.spatial_service.get_all_zone_features(study_area=study_area)
            if not all_features_df.empty:
                return self.explainer.explain_global(df_dataset=all_features_df)

        # Fallback response if explainer has no data
        return {
            "study_area": study_area,
            "model_name": "Unavailable",
            "base_value": 0.0,
            "base_score": 0.0,
            "total_zones_analyzed": 0,
            "feature_importances": [],
            "summary_text": "Global explanation unavailable.",
            "causality_disclaimer": CAUSALITY_DISCLAIMER,
        }
