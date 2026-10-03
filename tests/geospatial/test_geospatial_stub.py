import unittest
from backend.app.services.spatial import SpatialDataService


class TestGeospatialStub(unittest.TestCase):
    def test_spatial_data_service_defaults(self):
        service = SpatialDataService(data_dir="./data/processed")
        geojson = service.get_zone_geojson("Hyderabad")
        self.assertEqual(geojson["type"], "FeatureCollection")
        self.assertIn("features", geojson)
        self.assertEqual(geojson["metadata"]["study_area"], "Hyderabad")


if __name__ == "__main__":
    unittest.main()
