"""
Model Explainability Engine for Urban Flood Susceptibility.
Implements SHAP (SHapley Additive exPlanations) attribution for:
- Local feature attribution vectors per zone with waterfall progression
- Directional push towards or away from flood susceptibility
- Global feature importance rankings across all zones in the study area
- Prominent distinction between model explanation and physical causality
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
import numpy as np
import pandas as pd
import shap

# Suppress benign joblib CPU count warning on Windows
os.environ["LOKY_MAX_CPU_COUNT"] = str(os.cpu_count() or 4)

from ml.preprocessing.pipeline import LeakageSafePreprocessor
from ml.inference.predictor import get_risk_category

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("FloodExplainer")

CAUSALITY_DISCLAIMER = (
    "SHAP attributions describe the internal statistical behavior and factor contributions "
    "of the machine learning model. They must not be interpreted as definitive physical real-world causation."
)

FEATURE_DISPLAY_METADATA: Dict[str, Dict[str, str]] = {
    "avg_daily_rainfall_mm": {
        "label": "Average Daily Rainfall",
        "unit": "mm",
        "format": "{:.1f} mm",
    },
    "max_daily_rainfall_mm": {
        "label": "Maximum Daily Rainfall",
        "unit": "mm",
        "format": "{:.1f} mm",
    },
    "cumulative_rainfall_mm": {
        "label": "Cumulative Monsoon Rainfall",
        "unit": "mm",
        "format": "{:.1f} mm",
    },
    "extreme_rain_days_count": {
        "label": "Extreme Rainfall Days",
        "unit": "days",
        "format": "{:d} days",
    },
    "elevation_m": {
        "label": "Elevation",
        "unit": "m",
        "format": "{:.1f} m",
    },
    "slope_deg": {
        "label": "Terrain Slope",
        "unit": "deg",
        "format": "{:.1f}°",
    },
    "relative_elevation_m": {
        "label": "Relative Elevation / Low-lying Depth",
        "unit": "m",
        "format": "{:.1f} m",
    },
    "dist_to_drainage_m": {
        "label": "Distance to Primary Drainage",
        "unit": "m",
        "format": "{:.0f} m",
    },
    "drainage_density_index": {
        "label": "Drainage Density Index",
        "unit": "",
        "format": "{:.3f}",
    },
    "built_up_pct": {
        "label": "Built-up / Impervious Surface",
        "unit": "%",
        "format": "{:.1f}%",
    },
    "vegetation_pct": {
        "label": "Vegetation Cover",
        "unit": "%",
        "format": "{:.1f}%",
    },
    "water_pct": {
        "label": "Surface Water Body Cover",
        "unit": "%",
        "format": "{:.1f}%",
    },
    "open_ground_pct": {
        "label": "Open Ground / Permeable Land",
        "unit": "%",
        "format": "{:.1f}%",
    },
    "impervious_to_drainage_ratio": {
        "label": "Impervious to Drainage Proximity Ratio",
        "unit": "",
        "format": "{:.4f}",
    },
    "depression_slope_index": {
        "label": "Low-lying Flat Depression Index",
        "unit": "",
        "format": "{:.3f}",
    },
    "rainfall_missing": {
        "label": "Rainfall Data Missing Indicator",
        "unit": "",
        "format": "{:d}",
    },
    "elevation_missing": {
        "label": "Elevation Data Missing Indicator",
        "unit": "",
        "format": "{:d}",
    },
    "drainage_missing": {
        "label": "Drainage Data Missing Indicator",
        "unit": "",
        "format": "{:d}",
    },
    "land_cover_missing": {
        "label": "Land Cover Data Missing Indicator",
        "unit": "",
        "format": "{:d}",
    },
}


def format_raw_feature_value(feature_name: str, value: Any) -> str:
    """Helper to format numeric values with appropriate units."""
    if value is None:
        return "N/A"
    try:
        val_float = float(value)
        meta = FEATURE_DISPLAY_METADATA.get(feature_name)
        if meta and "format" in meta:
            if "d" in meta["format"]:
                return meta["format"].format(int(val_float))
            return meta["format"].format(val_float)
        return f"{val_float:.2f}"
    except (ValueError, TypeError):
        return str(value)


class FloodExplainer:
    """
    SHAP Explainability Engine for PyTorch ANN and Baseline models.
    Produces local waterfall attributions and global feature rankings.
    """

    def __init__(
        self,
        model_artifact_path: str = "ml/artifacts/ann_model.pt",
        preprocessor_artifact_path: str = "ml/artifacts/preprocessor.joblib",
        background_data_path: str = "data/processed/hyderabad_features.csv",
        n_background_kmeans: int = 15,
        model: Optional[Any] = None,
        preprocessor: Optional[LeakageSafePreprocessor] = None,
        background_df: Optional[pd.DataFrame] = None,
    ) -> None:
        self.model_path = model_artifact_path
        self.preprocessor_path = preprocessor_artifact_path
        self.background_data_path = background_data_path
        self.n_background_kmeans = n_background_kmeans

        self.model = model
        self.preprocessor = preprocessor
        self.feature_names: List[str] = []
        self.explainer: Optional[shap.KernelExplainer] = None
        self.base_value: float = 0.0
        self.model_name: str = "Primary ANN (PyTorch)" if "ann" in str(model_artifact_path) else "Baseline Logistic Regression"

        self._initialize(background_df)

    def _initialize(self, background_df: Optional[pd.DataFrame] = None) -> None:
        """Load artifacts and initialize SHAP KernelExplainer with k-means background summary."""
        # 1. Load Preprocessor
        if self.preprocessor is None and os.path.exists(self.preprocessor_path):
            self.preprocessor = LeakageSafePreprocessor.load(self.preprocessor_path)

        if self.preprocessor is not None:
            self.feature_names = list(self.preprocessor.fitted_feature_names)

        # 2. Load Model
        if self.model is None and os.path.exists(self.model_path):
            if self.model_path.endswith(".pt"):
                import torch
                from ml.models.ann import FloodSusceptibilityANN
                checkpoint = torch.load(self.model_path, map_location="cpu")
                ann = FloodSusceptibilityANN(
                    input_dim=checkpoint["input_dim"],
                    hidden_dims=checkpoint.get("hidden_dims", [32, 16]),
                    dropout_rate=checkpoint.get("dropout_rate", 0.2),
                )
                ann.load_state_dict(checkpoint["state_dict"])
                ann.eval()
                self.model = ann
                self.model_name = "Primary ANN (PyTorch)"
            else:
                import joblib
                model_data = joblib.load(self.model_path)
                self.model = model_data.get("model", model_data)
                self.model_name = "Baseline Logistic Regression"

        # 3. Load and summarize Background Data
        if self.is_ready():
            df_bg = background_df
            if df_bg is None and os.path.exists(self.background_data_path):
                df_bg = pd.read_csv(self.background_data_path)

            if df_bg is not None and len(df_bg) > 0:
                X_bg = self.preprocessor.transform(df_bg)
                k = min(self.n_background_kmeans, len(X_bg))
                background_summary = shap.kmeans(X_bg, k) if k < len(X_bg) else X_bg

                predict_fn = self._build_predict_fn()
                self.explainer = shap.KernelExplainer(predict_fn, background_summary)
                expected_val = self.explainer.expected_value
                if isinstance(expected_val, (list, np.ndarray)):
                    self.base_value = float(np.mean(expected_val))
                else:
                    self.base_value = float(expected_val)
                logger.info(
                    f"Initialized FloodExplainer for {self.model_name}. "
                    f"Base susceptibility probability E[f(x)] = {self.base_value:.4f}"
                )

    def _build_predict_fn(self):
        """Construct probability prediction callable for SHAP KernelExplainer."""
        if hasattr(self.model, "forward"):  # PyTorch model
            import torch
            self.model.eval()

            def _torch_predict(x_arr: np.ndarray) -> np.ndarray:
                if len(x_arr.shape) == 1:
                    x_arr = x_arr.reshape(1, -1)
                with torch.no_grad():
                    t = torch.tensor(x_arr, dtype=torch.float32)
                    out = self.model(t).squeeze().numpy()
                    if out.ndim == 0:
                        out = np.array([float(out)])
                    return out

            return _torch_predict

        elif hasattr(self.model, "predict_proba"):
            return lambda x_arr: self.model.predict_proba(x_arr)[:, 1]
        elif hasattr(self.model, "predict"):
            return lambda x_arr: self.model.predict(x_arr).astype(float)
        else:
            raise ValueError(f"Unsupported model type: {type(self.model)}")

    def is_ready(self) -> bool:
        return self.model is not None and self.preprocessor is not None

    def explain_instance(
        self,
        zone_data: Union[Dict[str, Any], pd.Series, pd.DataFrame],
        nsamples: int = 60,
    ) -> Dict[str, Any]:
        """
        Generate local SHAP explanations for a single zone.
        Returns waterfall contribution vectors, directional push, and qualitative synthesis.
        """
        if self.explainer is None:
            raise RuntimeError("FloodExplainer is not initialized. Check model and preprocessor artifacts.")

        if isinstance(zone_data, dict):
            df_instance = pd.DataFrame([zone_data])
            zone_id = str(zone_data.get("zone_id", "ZONE_UNKNOWN"))
        elif isinstance(zone_data, pd.Series):
            df_instance = pd.DataFrame([zone_data])
            zone_id = str(zone_data.get("zone_id", "ZONE_UNKNOWN"))
        elif isinstance(zone_data, pd.DataFrame):
            df_instance = zone_data.iloc[[0]]
            zone_id = str(df_instance.iloc[0].get("zone_id", "ZONE_UNKNOWN"))
        else:
            raise ValueError("Input zone_data must be a dict, Series, or DataFrame.")

        # Transform features
        X_scaled = self.preprocessor.transform(df_instance)
        feature_names = self.feature_names

        # Compute SHAP values
        raw_shap = self.explainer.shap_values(X_scaled, nsamples=nsamples)
        if isinstance(raw_shap, list):
            shap_vec = np.array(raw_shap[0]).flatten()
        else:
            shap_vec = np.array(raw_shap).flatten()

        # Compute prediction
        predict_fn = self._build_predict_fn()
        pred_prob = float(predict_fn(X_scaled)[0])
        pred_score = round(pred_prob * 100.0, 1)
        base_score = round(self.base_value * 100.0, 1)

        # Extract raw input feature values for display
        raw_row = df_instance.iloc[0]
        feature_contributions = []

        for idx, feat in enumerate(feature_names):
            s_val = float(shap_vec[idx])
            raw_val = raw_row.get(feat, None)
            if raw_val is not None:
                try:
                    raw_val_num = float(raw_val)
                except (ValueError, TypeError):
                    raw_val_num = 0.0
            else:
                raw_val_num = 0.0

            meta = FEATURE_DISPLAY_METADATA.get(feat, {})
            label = meta.get("label", feat.replace("_", " ").title())
            formatted_val = format_raw_feature_value(feat, raw_val_num)

            # Directional classification
            if s_val > 0.0005:
                direction = "INCREASES_SUSCEPTIBILITY"
                direction_label = "Pushes susceptibility HIGHER"
            elif s_val < -0.0005:
                direction = "DECREASES_SUSCEPTIBILITY"
                direction_label = "Lowers susceptibility (Mitigating)"
            else:
                direction = "NEUTRAL"
                direction_label = "Neutral / Minimal impact"

            contrib_score = round(s_val * 100.0, 2)
            magnitude = round(abs(s_val), 5)

            feature_contributions.append(
                {
                    "feature_name": feat,
                    "feature_label": label,
                    "raw_value": round(raw_val_num, 4),
                    "formatted_value": formatted_val,
                    "scaled_value": round(float(X_scaled[0, idx]), 4),
                    "shap_value": round(s_val, 5),
                    "contribution_score": contrib_score,
                    "magnitude": magnitude,
                    "direction": direction,
                    "direction_label": direction_label,
                }
            )

        # Sort features by absolute contribution magnitude for the waterfall
        sorted_contributions = sorted(feature_contributions, key=lambda x: x["magnitude"], reverse=True)

        # Build sequential waterfall steps
        waterfall_steps = []
        running_score = base_score

        for step_idx, item in enumerate(sorted_contributions):
            start_score = running_score
            step_contrib = item["contribution_score"]
            end_score = round(start_score + step_contrib, 2)
            running_score = end_score

            waterfall_steps.append(
                {
                    "step_index": step_idx + 1,
                    "feature_name": item["feature_name"],
                    "feature_label": item["feature_label"],
                    "raw_value": item["raw_value"],
                    "formatted_value": item["formatted_value"],
                    "shap_value": item["shap_value"],
                    "contribution_score": item["contribution_score"],
                    "direction": item["direction"],
                    "cumulative_score": end_score,
                }
            )

        # Separate top risk drivers vs mitigating factors
        top_positive = [c for c in sorted_contributions if c["direction"] == "INCREASES_SUSCEPTIBILITY"][:5]
        top_mitigating = [c for c in sorted_contributions if c["direction"] == "DECREASES_SUSCEPTIBILITY"][:5]

        # Natural language synthesis
        risk_cat = get_risk_category(pred_score)
        summary_parts = [
            f"Zone {zone_id} has a model-predicted susceptibility score of {pred_score}% ({risk_cat}), "
            f"compared to the regional baseline expectation of {base_score}%."
        ]
        if top_positive:
            pos_desc = ", ".join(f"{p['feature_label']} ({p['formatted_value']}: +{p['contribution_score']}%)" for p in top_positive[:2])
            summary_parts.append(f"Top factors elevating susceptibility are {pos_desc}.")
        if top_mitigating:
            neg_desc = ", ".join(f"{m['feature_label']} ({m['formatted_value']}: {m['contribution_score']}%)" for m in top_mitigating[:2])
            summary_parts.append(f"Partially mitigating factors include {neg_desc}.")

        summary_text = " ".join(summary_parts)

        return {
            "zone_id": zone_id,
            "model_name": self.model_name,
            "base_value": round(self.base_value, 4),
            "base_score": base_score,
            "predicted_probability": round(pred_prob, 4),
            "susceptibility_score": pred_score,
            "risk_level": risk_cat,
            "waterfall": waterfall_steps,
            "all_features": feature_contributions,
            "top_risk_drivers": top_positive,
            "top_mitigating_factors": top_mitigating,
            "summary_text": summary_text,
            "causality_disclaimer": CAUSALITY_DISCLAIMER,
        }

    def explain_global(
        self,
        df_dataset: Optional[pd.DataFrame] = None,
        nsamples: int = 50,
    ) -> Dict[str, Any]:
        """
        Calculate global feature importances across all zones in the study area.
        Aggregates mean absolute SHAP values, directional biases, and feature ranking.
        """
        if self.explainer is None:
            raise RuntimeError("FloodExplainer is not initialized.")

        df = df_dataset
        if df is None:
            if not os.path.exists(self.background_data_path):
                raise FileNotFoundError(f"Feature dataset not found at {self.background_data_path}")
            df = pd.read_csv(self.background_data_path)

        X = self.preprocessor.transform(df)
        n_zones = len(df)
        logger.info(f"Computing global SHAP feature importances across {n_zones} zones...")

        raw_shap_matrix = self.explainer.shap_values(X, nsamples=nsamples)
        if isinstance(raw_shap_matrix, list):
            shap_matrix = np.array(raw_shap_matrix[0])
        else:
            shap_matrix = np.array(raw_shap_matrix)

        # Aggregate metrics per feature
        feature_stats = []
        for j, feat in enumerate(self.feature_names):
            vals = shap_matrix[:, j]
            mean_abs = float(np.mean(np.abs(vals)))
            mean_val = float(np.mean(vals))
            min_val = float(np.min(vals))
            max_val = float(np.max(vals))

            meta = FEATURE_DISPLAY_METADATA.get(feat, {})
            label = meta.get("label", feat.replace("_", " ").title())

            if mean_val > 0.005:
                direction_trend = "Generally Increases Susceptibility"
            elif mean_val < -0.005:
                direction_trend = "Generally Decreases Susceptibility"
            else:
                direction_trend = "Mixed / Context Dependent"

            feature_stats.append(
                {
                    "feature_name": feat,
                    "feature_label": label,
                    "mean_abs_shap": round(mean_abs, 5),
                    "mean_abs_score": round(mean_abs * 100.0, 2),
                    "mean_shap": round(mean_val, 5),
                    "min_shap": round(min_val, 5),
                    "max_shap": round(max_val, 5),
                    "general_direction": direction_trend,
                }
            )

        # Sort by mean absolute SHAP (highest impact first)
        feature_stats.sort(key=lambda x: x["mean_abs_shap"], reverse=True)
        for rank, item in enumerate(feature_stats, start=1):
            item["rank"] = rank

        top_drivers = [f"{f['feature_label']} ({f['mean_abs_score']}% mean impact)" for f in feature_stats[:3]]
        summary_text = (
            f"Across {n_zones} study-area zones analyzed by {self.model_name}, the most influential factors "
            f"determining flood susceptibility are {', '.join(top_drivers)}."
        )

        return {
            "study_area": "Hyderabad",
            "model_name": self.model_name,
            "base_value": round(self.base_value, 4),
            "base_score": round(self.base_value * 100.0, 1),
            "total_zones_analyzed": n_zones,
            "feature_importances": feature_stats,
            "summary_text": summary_text,
            "causality_disclaimer": CAUSALITY_DISCLAIMER,
        }

    def precompute_and_save_artifacts(
        self,
        output_dir: str = "ml/artifacts",
        nsamples: int = 50,
    ) -> Dict[str, str]:
        """
        Precompute global feature importance and all zone explanations for instant API serving.
        """
        os.makedirs(output_dir, exist_ok=True)
        if not os.path.exists(self.background_data_path):
            raise FileNotFoundError(f"Data path {self.background_data_path} not found.")

        df = pd.read_csv(self.background_data_path)
        logger.info(f"Precomputing SHAP artifacts for {len(df)} zones in {self.background_data_path}...")

        # 1. Global Importance
        global_explanation = self.explain_global(df_dataset=df, nsamples=nsamples)
        global_path = os.path.join(output_dir, "shap_global_importance.json")
        with open(global_path, "w", encoding="utf-8") as f:
            json.dump(global_explanation, f, indent=2)
        logger.info(f"Saved global SHAP importance to {global_path}")

        # 2. Local Explanations for each zone
        zone_explanations = {}
        for idx in range(len(df)):
            row = df.iloc[idx]
            zone_id = str(row.get("zone_id", f"ZONE_{idx:03d}"))
            local_exp = self.explain_instance(row, nsamples=nsamples)
            zone_explanations[zone_id] = local_exp

        local_path = os.path.join(output_dir, "zone_explanations.json")
        with open(local_path, "w", encoding="utf-8") as f:
            json.dump(zone_explanations, f, indent=2)
        logger.info(f"Saved {len(zone_explanations)} zone explanations to {local_path}")

        return {
            "global_path": global_path,
            "local_path": local_path,
        }


if __name__ == "__main__":
    explainer = FloodExplainer()
    print("Running SHAP precomputation on Hyderabad study area...")
    paths = explainer.precompute_and_save_artifacts()
    print(f"Generated artifacts: {paths}")
