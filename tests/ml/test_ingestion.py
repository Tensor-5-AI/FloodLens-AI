"""
Unit tests for data ingestion modules across all 5 public data modalities:
1. Study area zones generation & geographic partitioning
2. Meteorological rainfall feature calculation
3. SRTM elevation & Deccan topography computation
4. Drainage, river network, and waterway proximity metrics
5. Land cover distribution (ESA WorldCover proportions)
6. Historical flood incidents matching & ground truth tagging
7. Data validation checks
8. End-to-end ingestion pipeline execution
"""

import unittest
import os
import shutil
import tempfile
from ml.ingestion.sources import HYDERABAD_BBOX, PUBLIC_DATA_SOURCES
from ml.ingestion.zones import generate_grid_zones
from ml.ingestion.rainfall import RainfallIngestion
from ml.ingestion.elevation import ElevationIngestion
from ml.ingestion.drainage import DrainageIngestion
from ml.ingestion.land_cover import LandCoverIngestion
from ml.ingestion.historical_floods import HistoricalFloodsIngestion
from ml.ingestion.validation import DataValidator
from ml.ingestion.pipeline import IngestionPipeline


class TestDataIngestionPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.raw_dir = os.path.join(self.temp_dir, "raw")
        self.processed_dir = os.path.join(self.temp_dir, "processed")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_sources_and_bbox_configured(self):
        min_lon, min_lat, max_lon, max_lat = HYDERABAD_BBOX
        self.assertLess(min_lon, max_lon)
        self.assertLess(min_lat, max_lat)
        self.assertIn("rainfall", PUBLIC_DATA_SOURCES)
        self.assertIn("elevation", PUBLIC_DATA_SOURCES)
        self.assertIn("drainage", PUBLIC_DATA_SOURCES)
        self.assertIn("land_cover", PUBLIC_DATA_SOURCES)
        self.assertIn("flood_incidents", PUBLIC_DATA_SOURCES)

    def test_grid_zone_generation(self):
        grid = generate_grid_zones(HYDERABAD_BBOX, rows=4, cols=4)
        self.assertEqual(grid["type"], "FeatureCollection")
        self.assertEqual(len(grid["features"]), 16)
        first_zone = grid["features"][0]
        self.assertEqual(first_zone["properties"]["zone_id"], "ZONE_HYD_001")
        self.assertIn("center_lat", first_zone["properties"])
        self.assertIn("center_lon", first_zone["properties"])
        self.assertGreater(first_zone["properties"]["area_sqkm"], 0)

    def test_rainfall_ingestion_baseline(self):
        ingestion = RainfallIngestion()
        stats = ingestion.get_regional_baseline_stats(lat_offset=0.01, lon_offset=-0.01)
        self.assertIn("avg_daily_rainfall_mm", stats)
        self.assertIn("max_daily_rainfall_mm", stats)
        self.assertIn("cumulative_rainfall_mm", stats)
        self.assertGreater(stats["cumulative_rainfall_mm"], 500)
        self.assertGreater(stats["max_daily_rainfall_mm"], 50)

    def test_elevation_ingestion(self):
        ingestion = ElevationIngestion()
        terrain = ingestion.compute_deccan_terrain_model(lat=17.37, lon=78.48)
        self.assertGreaterEqual(terrain["elevation_m"], 480.0)
        self.assertLessEqual(terrain["elevation_m"], 650.0)
        self.assertGreater(terrain["slope_deg"], 0)

    def test_drainage_ingestion(self):
        ingestion = DrainageIngestion()
        # Point right at Musi River city center
        metrics = ingestion.compute_drainage_metrics(lat=17.367, lon=78.474)
        self.assertLess(metrics["dist_to_drainage_m"], 500.0)
        self.assertIn("Musi", metrics["nearest_drainage_name"])
        self.assertGreater(metrics["drainage_density_index"], 0)

    def test_land_cover_ingestion(self):
        ingestion = LandCoverIngestion()
        # High density urban core (Charminar area)
        urban_lc = ingestion.estimate_land_cover(lat=17.3616, lon=78.4747)
        self.assertGreater(urban_lc["built_up_pct"], 70.0)
        self.assertGreater(urban_lc["vegetation_pct"], 0)
        # Sum of fractions should equal ~100%
        total = (
            urban_lc["built_up_pct"]
            + urban_lc["vegetation_pct"]
            + urban_lc["water_pct"]
            + urban_lc["open_ground_pct"]
        )
        self.assertAlmostEqual(total, 100.0, places=1)

    def test_historical_floods_ingestion(self):
        ingestion = HistoricalFloodsIngestion()
        # Around Falaknuma / Al-Jubail Colony (17.332, 78.472)
        metrics = ingestion.compute_incident_metrics(
            min_lat=17.32, max_lat=17.34, min_lon=78.46, max_lon=78.48
        )
        self.assertGreater(metrics["historical_incident_count"], 0)
        self.assertEqual(metrics["historical_flood_reported"], 1)

    def test_data_validator(self):
        grid = generate_grid_zones(HYDERABAD_BBOX, rows=2, cols=2)
        report = DataValidator.validate_feature_collection(grid)
        self.assertTrue(report["valid"])
        self.assertEqual(report["total_features"], 4)

    def test_end_to_end_pipeline_run(self):
        pipeline = IngestionPipeline(
            output_dir_processed=self.processed_dir,
            output_dir_raw=self.raw_dir,
        )
        collection = pipeline.run(grid_rows=3, grid_cols=3, save_files=True)
        self.assertEqual(len(collection["features"]), 9)

        # Check exported files exist
        geojson_file = os.path.join(self.processed_dir, "hyderabad_zones.geojson")
        csv_file = os.path.join(self.processed_dir, "hyderabad_features.csv")
        manifest_file = os.path.join(self.raw_dir, "sources_manifest.json")

        self.assertTrue(os.path.exists(geojson_file))
        self.assertTrue(os.path.exists(csv_file))
        self.assertTrue(os.path.exists(manifest_file))


if __name__ == "__main__":
    unittest.main()
