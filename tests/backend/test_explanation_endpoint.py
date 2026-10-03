"""
Integration tests for SHAP explanation API endpoints.
Tests:
- GET /zones/{zone_id}/explanation
- GET /api/v1/zones/{zone_id}/explanation
- GET /zones/explanations/global
- POST /zones/explain
- Error handling on unknown zones
- Susceptibility endpoint integration with top SHAP explanations
"""

import unittest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.explanation import ZoneExplanationResponse, GlobalExplanationResponse


class TestExplanationEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.valid_zone_id = "ZONE_HYD_001"

    def test_get_zone_explanation_root_route(self):
        """Verify GET /zones/{zone_id}/explanation returns 200 and matches ZoneExplanationResponse schema."""
        response = self.client.get(f"/zones/{self.valid_zone_id}/explanation")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = ZoneExplanationResponse(**data)
        self.assertEqual(validated.zone_id, self.valid_zone_id)
        self.assertGreater(len(validated.waterfall), 0)
        self.assertIn("causality_disclaimer", data)
        self.assertIn("statistical behavior", validated.causality_disclaimer.lower())
        self.assertIn("causation", validated.causality_disclaimer.lower())


    def test_get_zone_explanation_api_v1_route(self):
        """Verify GET /api/v1/zones/{zone_id}/explanation works identically."""
        response = self.client.get(f"/api/v1/zones/{self.valid_zone_id}/explanation")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["zone_id"], self.valid_zone_id)
        self.assertIn("susceptibility_score", data)

    def test_get_zone_explanation_404_on_invalid_zone(self):
        """Verify 404 is returned when requesting explanation for a nonexistent zone."""
        response = self.client.get("/zones/NON_EXISTENT_ZONE_9999/explanation")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"].lower())

    def test_get_global_explanation(self):
        """Verify GET /zones/explanations/global returns ranked feature importances."""
        response = self.client.get("/zones/explanations/global")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = GlobalExplanationResponse(**data)
        self.assertEqual(validated.study_area, "Hyderabad")
        self.assertGreater(validated.total_zones_analyzed, 0)
        self.assertGreater(len(validated.feature_importances), 0)

        # Check rankings
        ranks = [f.rank for f in validated.feature_importances]
        self.assertEqual(ranks, list(range(1, len(ranks) + 1)))

    def test_post_custom_features_explain(self):
        """Verify POST /zones/explain computes explanation on arbitrary feature dictionary."""
        custom_payload = {
            "avg_daily_rainfall_mm": 6.5,
            "max_daily_rainfall_mm": 130.0,
            "cumulative_rainfall_mm": 880.0,
            "extreme_rain_days_count": 3,
            "elevation_m": 505.0,
            "slope_deg": 2.5,
            "relative_elevation_m": -15.0,
            "dist_to_drainage_m": 350.0,
            "drainage_density_index": 0.45,
            "built_up_pct": 82.0,
            "vegetation_pct": 8.0,
            "water_pct": 2.0,
            "open_ground_pct": 8.0,
            "rainfall_missing": 0,
            "elevation_missing": 0,
            "drainage_missing": 0,
            "land_cover_missing": 0,
        }
        response = self.client.post("/zones/explain", json=custom_payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = ZoneExplanationResponse(**data)
        self.assertGreater(len(validated.waterfall), 0)

    def test_susceptibility_endpoint_enriched_with_shap(self):
        """Verify GET /api/v1/susceptibility includes top SHAP explanations."""
        response = self.client.get("/api/v1/susceptibility")
        self.assertEqual(response.status_code, 200)

        results = response.json()
        self.assertGreater(len(results), 0)
        first = results[0]
        self.assertIn("zone_id", first)
        self.assertIn("susceptibility_score", first)
        self.assertIn("top_explanations", first)
        self.assertIsInstance(first["top_explanations"], list)


if __name__ == "__main__":
    unittest.main()
