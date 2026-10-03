"""
Integration tests for Confidence & Data Quality API endpoints.
Tests:
- GET /zones/{zone_id}/confidence
- GET /api/v1/zones/{zone_id}/confidence
- GET /zones/confidence/summary
- 404 on nonexistent zone
- Schema validation against ZoneConfidenceResponse and StudyAreaConfidenceSummary
"""

import unittest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.confidence import ZoneConfidenceResponse, StudyAreaConfidenceSummary


class TestConfidenceEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.valid_zone_id = "ZONE_HYD_001"

    def test_get_zone_confidence_root_route(self):
        response = self.client.get(f"/zones/{self.valid_zone_id}/confidence")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = ZoneConfidenceResponse(**data)
        self.assertEqual(validated.zone_id, self.valid_zone_id)
        self.assertGreater(validated.confidence_score, 0.0)
        self.assertIn(validated.confidence_tier, ["VERY LOW", "LOW", "MEDIUM", "HIGH", "VERY HIGH"])
        self.assertIn(
            validated.risk_confidence_quadrant,
            [
                "PRIORITIZED_ACTION_ZONE",
                "GROUND_VERIFICATION_REQUIRED",
                "DATA_BLINDSPOT",
                "VERIFIED_SAFE_ZONE",
            ],
        )
        self.assertGreater(len(validated.recommendation), 10)

    def test_get_zone_confidence_api_v1_route(self):
        response = self.client.get(f"/api/v1/zones/{self.valid_zone_id}/confidence")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["zone_id"], self.valid_zone_id)

    def test_get_confidence_summary(self):
        response = self.client.get("/zones/confidence/summary")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = StudyAreaConfidenceSummary(**data)
        self.assertEqual(validated.study_area, "Hyderabad")
        self.assertEqual(validated.total_zones, 100)
        self.assertGreater(validated.mean_confidence, 0.0)

    def test_get_zone_confidence_404_invalid_zone(self):
        response = self.client.get("/zones/ZONE_NONEXISTENT_9999/confidence")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"].lower())


if __name__ == "__main__":
    unittest.main()
