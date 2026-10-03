"""
Confidence and Data Quality Profiling Engine for Urban Flood Susceptibility.
Evaluates multi-modal data completeness, sensor coverage, and observation reliability.
Crucially decouples SUSCEPTIBILITY RISK from DATA CONFIDENCE to identify:
- Prioritized Action Zones (High Risk, High Confidence)
- Ground Verification Zones (High Risk, Low Confidence)
- Data Blindspots (Low Risk, Low Confidence)
- Verified Safe Zones (Low Risk, High Confidence)
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd


def get_confidence_tier(score_pct: float) -> str:
    """Classify 0-100 confidence score into standardized quality tiers."""
    if score_pct >= 80.0:
        return "VERY HIGH"
    elif score_pct >= 65.0:
        return "HIGH"
    elif score_pct >= 45.0:
        return "MEDIUM"
    elif score_pct >= 25.0:
        return "LOW"
    else:
        return "VERY LOW"


def determine_risk_confidence_quadrant(
    susceptibility_score: float,
    confidence_score: float,
) -> Tuple[str, str]:
    """
    Categorize zone into the 2x2 Risk vs Confidence Matrix.
    Returns (quadrant_code, strategic_recommendation).
    """
    is_high_risk = susceptibility_score >= 50.0
    is_high_confidence = confidence_score >= 0.60

    if is_high_risk and is_high_confidence:
        quadrant = "PRIORITIZED_ACTION_ZONE"
        recommendation = (
            "High flood susceptibility supported by reliable, complete data coverage. "
            "Prioritize immediate municipal drainage upgrades and emergency flood barriers."
        )
    elif is_high_risk and not is_high_confidence:
        quadrant = "GROUND_VERIFICATION_REQUIRED"
        recommendation = (
            "Elevated flood susceptibility indicated, but with significant data gaps or sensor sparsity. "
            "Dispatch on-site ground inspection and install localized rain/water-level telemetry."
        )
    elif not is_high_risk and not is_high_confidence:
        quadrant = "DATA_BLINDSPOT"
        recommendation = (
            "Low susceptibility predicted, but confidence is low due to missing observations. "
            "Caution: lack of reported historical incidents may mask hidden vulnerabilities."
        )
    else:
        quadrant = "VERIFIED_SAFE_ZONE"
        recommendation = (
            "Low susceptibility supported by high-quality multi-modal data. "
            "Suitable for standard routine maintenance and urban infrastructure planning."
        )

    return quadrant, recommendation


class ConfidenceScorer:
    """
    Evaluates multi-modal data quality and reliability for urban zones.
    """

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
    ) -> None:
        self.weights = weights or {
            "feature_completeness": 0.40,
            "sensor_proximity": 0.25,
            "historical_evidence": 0.20,
            "spatial_coverage": 0.15,
        }

    def evaluate_zone(
        self,
        zone_record: Dict[str, Any],
        susceptibility_score: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate full confidence profile for a single zone record.
        """
        zone_id = str(zone_record.get("zone_id", "ZONE_UNKNOWN"))
        missing_modalities: List[str] = []
        quality_notes: List[str] = []

        # 1. Feature Completeness Evaluation
        missing_flags = {
            "Rainfall Meteorology": int(zone_record.get("rainfall_missing", 0)),
            "Elevation & Terrain": int(zone_record.get("elevation_missing", 0)),
            "Drainage Infrastructure": int(zone_record.get("drainage_missing", 0)),
            "Land Cover & Imperviousness": int(zone_record.get("land_cover_missing", 0)),
            "Historical Flood Records": int(zone_record.get("flood_history_missing", 0)),
        }

        total_modalities = len(missing_flags)
        present_count = 0
        for modality, is_missing in missing_flags.items():
            if is_missing == 1:
                missing_modalities.append(modality)
            else:
                present_count += 1

        completeness_score = (present_count / total_modalities) * 100.0
        if missing_modalities:
            quality_notes.append(f"Missing observation inputs for: {', '.join(missing_modalities)}.")
        else:
            quality_notes.append("All primary data modalities successfully ingested.")

        # 2. Sensor Proximity & Feature Granularity Evaluation
        dist_drainage = float(zone_record.get("dist_to_drainage_m", 5000.0))
        drainage_density = float(zone_record.get("drainage_density_index", 0.0))

        # Closer to known waterways (< 3000m) and higher density yields higher confidence in drainage modeling
        if dist_drainage < 1000.0 or drainage_density > 0.3:
            sensor_score = 95.0
        elif dist_drainage < 3000.0 or drainage_density > 0.1:
            sensor_score = 80.0
        elif dist_drainage < 10000.0:
            sensor_score = 60.0
            quality_notes.append("Moderate distance from mapped primary drainage networks.")
        else:
            sensor_score = 40.0
            quality_notes.append("Remote from mapped drainage channels (>10 km); unmapped local canals possible.")

        # 3. Historical Flood Evidence Quality
        incidents = int(zone_record.get("historical_incident_count", 0))
        reported = int(zone_record.get("historical_flood_reported", 0))
        hist_missing = int(zone_record.get("flood_history_missing", 0))

        if hist_missing == 1:
            hist_score = 30.0
            quality_notes.append("Historical incident archives unavailable or incomplete for this zone.")
        elif incidents > 0 or reported == 1:
            hist_score = 100.0
            quality_notes.append(f"Confirmed historical flood incident records available (n={incidents}).")
        else:
            hist_score = 75.0
            quality_notes.append("Zero historical flood incidents documented in public registries.")

        # 4. Spatial Geometry & Coordinate Coverage
        has_coords = ("center_lat" in zone_record and "center_lon" in zone_record)
        area = float(zone_record.get("area_sqkm", 1.0))

        if has_coords and 0.1 <= area <= 50.0:
            spatial_score = 100.0
        elif has_coords:
            spatial_score = 80.0
        else:
            spatial_score = 40.0
            quality_notes.append("Centroid coordinates absent or anomalous polygon area.")

        # Composite Confidence Score
        composite_score_pct = (
            completeness_score * self.weights["feature_completeness"]
            + sensor_score * self.weights["sensor_proximity"]
            + hist_score * self.weights["historical_evidence"]
            + spatial_score * self.weights["spatial_coverage"]
        )
        composite_score_pct = round(max(5.0, min(100.0, composite_score_pct)), 1)
        composite_score = round(composite_score_pct / 100.0, 3)

        confidence_tier = get_confidence_tier(composite_score_pct)

        # Risk vs Confidence Quadrant
        s_score = float(susceptibility_score) if susceptibility_score is not None else float(zone_record.get("susceptibility_score", 0.0))
        quadrant, recommendation = determine_risk_confidence_quadrant(
            susceptibility_score=s_score,
            confidence_score=composite_score,
        )

        return {
            "zone_id": zone_id,
            "confidence_score": composite_score,
            "confidence_percentage": composite_score_pct,
            "confidence_tier": confidence_tier,
            "dimension_scores": {
                "feature_completeness": round(completeness_score, 1),
                "sensor_proximity": round(sensor_score, 1),
                "historical_evidence": round(hist_score, 1),
                "spatial_coverage": round(spatial_score, 1),
            },
            "missing_modalities": missing_modalities,
            "susceptibility_score": s_score,
            "risk_level": zone_record.get("risk_level", "UNKNOWN"),
            "risk_confidence_quadrant": quadrant,
            "recommendation": recommendation,
            "data_quality_notes": quality_notes,
        }

    def evaluate_study_area(self, df_zones: pd.DataFrame) -> Dict[str, Any]:
        """
        Aggregate confidence metrics across all zones in the study area.
        """
        if df_zones.empty:
            return {
                "study_area": "Hyderabad",
                "total_zones": 0,
                "mean_confidence": 0.0,
                "quadrant_distribution": {},
            }

        zone_results = []
        for idx in range(len(df_zones)):
            row = df_zones.iloc[idx].to_dict()
            res = self.evaluate_zone(row)
            zone_results.append(res)

        conf_scores = [z["confidence_score"] for z in zone_results]
        quadrants = [z["risk_confidence_quadrant"] for z in zone_results]
        quadrant_counts = pd.Series(quadrants).value_counts().to_dict()

        return {
            "study_area": "Hyderabad",
            "total_zones": len(df_zones),
            "mean_confidence": round(float(np.mean(conf_scores)), 3),
            "mean_confidence_percentage": round(float(np.mean(conf_scores) * 100.0), 1),
            "high_confidence_zones_count": sum(1 for s in conf_scores if s >= 0.70),
            "low_confidence_zones_count": sum(1 for s in conf_scores if s < 0.50),
            "data_blindspot_zones_count": quadrant_counts.get("DATA_BLINDSPOT", 0),
            "priority_action_zones_count": quadrant_counts.get("PRIORITIZED_ACTION_ZONE", 0),
            "quadrant_distribution": quadrant_counts,
        }
