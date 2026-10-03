"""
Spatial Error Analysis Engine for Urban Flood Susceptibility.
Evaluates spatial distribution of model performance, identifying:
- Confusion classifications (True Positives, True Negatives, False Positives, False Negatives)
- Continuous spatial residuals (y - p_hat) and Brier score contributions
- Geographic clustering of prediction errors across study area quadrants
- GeoJSON spatial error layer for MapLibre and Cesium 3D visualization
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger("SpatialErrorAnalyzer")

ERROR_COLOR_MAP = {
    "TRUE_POSITIVE": "#E65100",   # Deep Amber: Confirmed Susceptible Hotspot
    "TRUE_NEGATIVE": "#2E7D32",   # Dark Green: Confirmed Safe
    "FALSE_POSITIVE": "#FBC02D",  # Yellow: Over-prediction / Potential Unreported Vulnerability
    "FALSE_NEGATIVE": "#D32F2F",  # Crimson Red: Missed Flood / Critical Model Error
}

ERROR_DESCRIPTIONS = {
    "TRUE_POSITIVE": "Correctly identified high-susceptibility zone with historical flood evidence.",
    "TRUE_NEGATIVE": "Correctly identified low-susceptibility zone with no documented flooding.",
    "FALSE_POSITIVE": "Model predicted high susceptibility, but no historical flood was recorded (possible unmapped vulnerability or effective local drainage).",
    "FALSE_NEGATIVE": "Model underestimated susceptibility despite documented historical flood incidents (critical under-prediction).",
}


class SpatialErrorAnalyzer:
    """
    Computes spatial residuals, confusion categories, quadrant clustering,
    and produces styled GeoJSON layers for geographic error visualization.
    """

    def __init__(
        self,
        decision_threshold: float = 0.30,
        artifacts_dir: str = "ml/artifacts",
        data_dir: str = "data/processed",
    ) -> None:
        self.decision_threshold = decision_threshold
        self.artifacts_dir = artifacts_dir
        self.data_dir = data_dir

    def evaluate_study_area(
        self,
        df_zones: pd.DataFrame,
        probabilities: np.ndarray,
        target_col: str = "historical_flood_reported",
    ) -> Dict[str, Any]:
        """
        Compute full spatial error metrics across all zones.
        """
        if df_zones.empty:
            raise ValueError("df_zones cannot be empty.")

        y_true = df_zones[target_col].values.astype(int) if target_col in df_zones.columns else np.zeros(len(df_zones))
        y_prob = np.array(probabilities).flatten()
        y_pred = (y_prob >= self.decision_threshold).astype(int)

        tp, fp, tn, fn = 0, 0, 0, 0
        zone_records: List[Dict[str, Any]] = []

        quadrant_stats: Dict[str, Dict[str, int]] = {
            "NW": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "total": 0},
            "NE": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "total": 0},
            "SW": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "total": 0},
            "SE": {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "total": 0},
        }

        # Determine median center for quadrant assignment if not explicit
        mid_lat = df_zones["center_lat"].median() if "center_lat" in df_zones.columns else 17.38
        mid_lon = df_zones["center_lon"].median() if "center_lon" in df_zones.columns else 78.48

        for idx in range(len(df_zones)):
            row = df_zones.iloc[idx]
            zone_id = str(row.get("zone_id", f"ZONE_{idx:03d}"))
            actual = int(y_true[idx])
            pred_prob = float(y_prob[idx])
            pred_binary = int(y_pred[idx])

            # Classify error category
            if actual == 1 and pred_binary == 1:
                category = "TRUE_POSITIVE"
                tp += 1
            elif actual == 0 and pred_binary == 0:
                category = "TRUE_NEGATIVE"
                tn += 1
            elif actual == 0 and pred_binary == 1:
                category = "FALSE_POSITIVE"
                fp += 1
            else:
                category = "FALSE_NEGATIVE"
                fn += 1

            residual = round(actual - pred_prob, 4)
            abs_err = round(abs(actual - pred_prob), 4)
            brier_contrib = round(residual ** 2, 4)

            # Assign quadrant
            c_lat = float(row.get("center_lat", mid_lat))
            c_lon = float(row.get("center_lon", mid_lon))

            if c_lat >= mid_lat and c_lon < mid_lon:
                q = "NW"
            elif c_lat >= mid_lat and c_lon >= mid_lon:
                q = "NE"
            elif c_lat < mid_lat and c_lon < mid_lon:
                q = "SW"
            else:
                q = "SE"

            quadrant_stats[q]["total"] += 1
            if category == "TRUE_POSITIVE":
                quadrant_stats[q]["TP"] += 1
            elif category == "TRUE_NEGATIVE":
                quadrant_stats[q]["TN"] += 1
            elif category == "FALSE_POSITIVE":
                quadrant_stats[q]["FP"] += 1
            elif category == "FALSE_NEGATIVE":
                quadrant_stats[q]["FN"] += 1

            zone_records.append(
                {
                    "zone_id": zone_id,
                    "actual_flood": actual,
                    "predicted_probability": round(pred_prob, 4),
                    "susceptibility_score": round(pred_prob * 100.0, 1),
                    "predicted_binary": pred_binary,
                    "error_category": category,
                    "color": ERROR_COLOR_MAP[category],
                    "residual_error": residual,
                    "absolute_error": abs_err,
                    "brier_contribution": brier_contrib,
                    "quadrant": q,
                    "center_lat": c_lat,
                    "center_lon": c_lon,
                    "description": ERROR_DESCRIPTIONS[category],
                }
            )

        total = len(df_zones)
        accuracy = round((tp + tn) / max(1, total), 4)
        precision = round(tp / max(1, tp + fp), 4)
        recall = round(tp / max(1, tp + fn), 4)
        f1 = round((2 * precision * recall) / max(1e-6, precision + recall), 4)
        brier_score = round(float(np.mean([z["brier_contribution"] for z in zone_records])), 4)

        # Evaluate Quadrant Accuracies
        quadrant_summary = {}
        weakest_quadrant = None
        lowest_acc = 1.0

        for q_name, q_data in quadrant_stats.items():
            q_tot = q_data["total"]
            q_acc = round((q_data["TP"] + q_data["TN"]) / max(1, q_tot), 3) if q_tot > 0 else 0.0
            quadrant_summary[q_name] = {
                "total_zones": q_tot,
                "accuracy": q_acc,
                "true_positives": q_data["TP"],
                "true_negatives": q_data["TN"],
                "false_positives": q_data["FP"],
                "false_negatives": q_data["FN"],
            }
            if q_tot > 0 and q_acc < lowest_acc:
                lowest_acc = q_acc
                weakest_quadrant = q_name

        summary = {
            "study_area": "Hyderabad",
            "decision_threshold": self.decision_threshold,
            "total_zones": total,
            "confusion_matrix": {
                "true_positives": tp,
                "true_negatives": tn,
                "false_positives": fp,
                "false_negatives": fn,
            },
            "metrics": {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "brier_score": brier_score,
            },
            "quadrant_breakdown": quadrant_summary,
            "spatial_clustering": {
                "weakest_quadrant": weakest_quadrant,
                "weakest_quadrant_accuracy": lowest_acc,
                "high_false_positive_clusters": [q for q, s in quadrant_summary.items() if s["false_positives"] >= 3],
                "high_false_negative_clusters": [q for q, s in quadrant_summary.items() if s["false_negatives"] >= 1],
            },
            "zone_errors": zone_records,
        }

        return summary

    def generate_error_geojson(
        self,
        analysis_summary: Dict[str, Any],
        base_geojson_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Merge spatial error evaluations with zone polygon boundaries from GeoJSON.
        """
        geojson_file = base_geojson_path or os.path.join(self.data_dir, "hyderabad_zones.geojson")

        if os.path.exists(geojson_file):
            with open(geojson_file, "r", encoding="utf-8") as f:
                base_geojson = json.load(f)
        else:
            base_geojson = {"type": "FeatureCollection", "features": []}

        # Index errors by zone_id
        error_by_zone = {z["zone_id"].upper(): z for z in analysis_summary.get("zone_errors", [])}

        features = []
        for feature in base_geojson.get("features", []):
            props = dict(feature.get("properties", {}))
            z_id = str(props.get("zone_id", "")).upper()

            err_info = error_by_zone.get(z_id)
            if err_info:
                props.update(
                    {
                        "error_category": err_info["error_category"],
                        "color": err_info["color"],
                        "actual_flood": err_info["actual_flood"],
                        "predicted_probability": err_info["predicted_probability"],
                        "susceptibility_score": err_info["susceptibility_score"],
                        "residual_error": err_info["residual_error"],
                        "description": err_info["description"],
                    }
                )

            features.append(
                {
                    "type": "Feature",
                    "geometry": feature.get("geometry"),
                    "properties": props,
                }
            )

        return {
            "type": "FeatureCollection",
            "metadata": {
                "layer_name": "spatial_errors",
                "study_area": analysis_summary.get("study_area", "Hyderabad"),
                "decision_threshold": analysis_summary.get("decision_threshold", self.decision_threshold),
                "total_features": len(features),
                "legend": {
                    "TRUE_POSITIVE": {"color": ERROR_COLOR_MAP["TRUE_POSITIVE"], "label": "Confirmed Susceptible Hotspot (TP)"},
                    "TRUE_NEGATIVE": {"color": ERROR_COLOR_MAP["TRUE_NEGATIVE"], "label": "Confirmed Safe (TN)"},
                    "FALSE_POSITIVE": {"color": ERROR_COLOR_MAP["FALSE_POSITIVE"], "label": "Over-prediction / High Vulnerability (FP)"},
                    "FALSE_NEGATIVE": {"color": ERROR_COLOR_MAP["FALSE_NEGATIVE"], "label": "Missed Flood / Under-prediction (FN)"},
                },
            },
            "features": features,
        }

    def save_artifacts(
        self,
        analysis_summary: Dict[str, Any],
        geojson_data: Dict[str, Any],
    ) -> Dict[str, str]:
        """Save spatial error JSON report and styled GeoJSON map to artifacts."""
        os.makedirs(self.artifacts_dir, exist_ok=True)
        json_path = os.path.join(self.artifacts_dir, "spatial_errors.json")
        geojson_path = os.path.join(self.artifacts_dir, "spatial_error_map.geojson")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(analysis_summary, f, indent=2)

        with open(geojson_path, "w", encoding="utf-8") as f:
            json.dump(geojson_data, f, indent=2)

        logger.info(f"Saved spatial error analysis to {json_path} and {geojson_path}")
        return {"json_path": json_path, "geojson_path": geojson_path}
