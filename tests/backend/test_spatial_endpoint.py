"""
Integration tests for Spatial Error and Map Layer API endpoints.
Tests:
- GET /spatial/errors
- GET /layers/spatial_errors
- GET /layers/zones
- GET /layers/unknown_layer (404)
- GET /zones/{zone_id}/spatial_error
- 404 on nonexistent zone
"""

import unittest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.spatial import SpatialErrorSummary, SpatialErrorMapLayerResponse, ZoneSpatialError


class TestSpatialEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.valid_zone_id = "ZONE_HYD_001"

    def test_get_spatial_errors_summary(self):
        response = self.client.get("/spatial/errors")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = SpatialErrorSummary(**data)
        self.assertEqual(validated.study_area, "Hyderabad")
        self.assertEqual(validated.total_zones, 100)
        self.assertGreater(validated.metrics["accuracy"], 0.70)
        self.assertIn("true_positives", validated.confusion_matrix)
        self.assertEqual(set(validated.quadrant_breakdown.keys()), {"NW", "NE", "SW", "SE"})

    def test_get_spatial_errors_prefixed(self):
        response = self.client.get("/api/v1/spatial/errors")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_zones"], 100)

    def test_get_spatial_error_layer_geojson(self):
        response = self.client.get("/layers/spatial_errors")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = SpatialErrorMapLayerResponse(**data)
        self.assertEqual(validated.type, "FeatureCollection")
        self.assertGreater(len(validated.features), 0)
        first_props = validated.features[0]["properties"]
        self.assertIn("error_category", first_props)
        self.assertIn("color", first_props)

    def test_get_zones_layer(self):
        response = self.client.get("/layers/zones")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["type"], "FeatureCollection")

    def test_get_unknown_layer_404(self):
        response = self.client.get("/layers/unknown_dummy_layer")
        self.assertEqual(response.status_code, 404)

    def test_get_zone_spatial_error(self):
        response = self.client.get(f"/zones/{self.valid_zone_id}/spatial_error")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        validated = ZoneSpatialError(**data)
        self.assertEqual(validated.zone_id, self.valid_zone_id)
        self.assertIn(validated.error_category, ["TRUE_POSITIVE", "TRUE_NEGATIVE", "FALSE_POSITIVE", "FALSE_NEGATIVE"])

    def test_get_zone_spatial_error_404(self):
        response = self.client.get("/zones/NON_EXISTENT_ZONE_9999/spatial_error")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
