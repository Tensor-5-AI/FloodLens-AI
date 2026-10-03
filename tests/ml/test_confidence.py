"""
Unit tests for Confidence & Data Quality Scorer (ml/confidence/engine.py).
Tests:
- Multi-modal completeness scoring and missingness penalties
- Sensor proximity and historical evidence evaluation
- Confidence tier classification
- 2x2 Risk-Confidence Quadrant categorization
- Study-area aggregate summary calculation
"""

import unittest
import pandas as pd

from ml.confidence.engine import (
    ConfidenceScorer,
    get_confidence_tier,
    determine_risk_confidence_quadrant,
)


class TestConfidenceScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ConfidenceScorer()
        self.complete_zone = {
            "zone_id": "ZONE_TEST_001",
            "rainfall_missing": 0,
            "elevation_missing": 0,
            "drainage_missing": 0,
            "land_cover_missing": 0,
            "flood_history_missing": 0,
            "dist_to_drainage_m": 450.0,
            "drainage_density_index": 0.55,
            "historical_incident_count": 4,
            "historical_flood_reported": 1,
            "area_sqkm": 2.5,
            "center_lat": 17.38,
            "center_lon": 78.48,
        }

    def test_complete_zone_high_confidence(self):
        profile = self.scorer.evaluate_zone(self.complete_zone, susceptibility_score=75.0)

        self.assertEqual(profile["zone_id"], "ZONE_TEST_001")
        self.assertGreaterEqual(profile["confidence_score"], 0.85)
        self.assertEqual(profile["confidence_tier"], "VERY HIGH")
        self.assertEqual(len(profile["missing_modalities"]), 0)
        self.assertEqual(profile["dimension_scores"]["feature_completeness"], 100.0)
        self.assertEqual(profile["risk_confidence_quadrant"], "PRIORITIZED_ACTION_ZONE")
        self.assertIn("prioritize", profile["recommendation"].lower())

    def test_missing_modalities_penalize_score(self):
        degraded_zone = dict(self.complete_zone)
        degraded_zone["rainfall_missing"] = 1
        degraded_zone["drainage_missing"] = 1
        degraded_zone["flood_history_missing"] = 1

        profile = self.scorer.evaluate_zone(degraded_zone, susceptibility_score=20.0)

        self.assertLess(profile["confidence_score"], 0.70)
        self.assertEqual(len(profile["missing_modalities"]), 3)
        self.assertIn("Rainfall Meteorology", profile["missing_modalities"])
        self.assertIn("Drainage Infrastructure", profile["missing_modalities"])

    def test_risk_confidence_quadrants(self):
        # 1. High Risk, High Confidence -> PRIORITIZED_ACTION_ZONE
        q1, rec1 = determine_risk_confidence_quadrant(susceptibility_score=85.0, confidence_score=0.85)
        self.assertEqual(q1, "PRIORITIZED_ACTION_ZONE")

        # 2. High Risk, Low Confidence -> GROUND_VERIFICATION_REQUIRED
        q2, rec2 = determine_risk_confidence_quadrant(susceptibility_score=80.0, confidence_score=0.40)
        self.assertEqual(q2, "GROUND_VERIFICATION_REQUIRED")

        # 3. Low Risk, Low Confidence -> DATA_BLINDSPOT
        q3, rec3 = determine_risk_confidence_quadrant(susceptibility_score=15.0, confidence_score=0.35)
        self.assertEqual(q3, "DATA_BLINDSPOT")

        # 4. Low Risk, High Confidence -> VERIFIED_SAFE_ZONE
        q4, rec4 = determine_risk_confidence_quadrant(susceptibility_score=15.0, confidence_score=0.90)
        self.assertEqual(q4, "VERIFIED_SAFE_ZONE")

    def test_confidence_tiers(self):
        self.assertEqual(get_confidence_tier(90.0), "VERY HIGH")
        self.assertEqual(get_confidence_tier(70.0), "HIGH")
        self.assertEqual(get_confidence_tier(50.0), "MEDIUM")
        self.assertEqual(get_confidence_tier(30.0), "LOW")
        self.assertEqual(get_confidence_tier(10.0), "VERY LOW")

    def test_study_area_aggregation(self):
        df_zones = pd.DataFrame(
            [
                dict(self.complete_zone, zone_id=f"ZONE_{i:03d}", susceptibility_score=10.0 * i)
                for i in range(10)
            ]
        )
        summary = self.scorer.evaluate_study_area(df_zones)

        self.assertEqual(summary["total_zones"], 10)
        self.assertGreater(summary["mean_confidence"], 0.70)
        self.assertIn("quadrant_distribution", summary)


if __name__ == "__main__":
    unittest.main()
