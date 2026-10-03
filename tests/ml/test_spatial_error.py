"""
Unit tests for Spatial Error Analysis engine (ml/evaluation/spatial_error.py).
Tests:
- Confusion matrix classification (TP, TN, FP, FN)
- Residual and Brier score calculation
- Quadrant-level error clustering
- Styled GeoJSON generation for map visualization
- Artifact persistence
"""

import unittest
import os
import shutil
import tempfile
import numpy as np
import pandas as pd

from ml.evaluation.spatial_error import SpatialErrorAnalyzer, ERROR_COLOR_MAP, ERROR_DESCRIPTIONS


class TestSpatialErrorAnalyzer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.artifacts_dir = os.path.join(self.temp_dir, "artifacts")
        self.data_dir = os.path.join(self.temp_dir, "data")
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

        # Create reproducible synthetic zones DataFrame
        n = 20
        self.df_zones = pd.DataFrame(
            {
                "zone_id": [f"ZONE_TEST_{i:03d}" for i in range(n)],
                "center_lat": [17.30 + (i // 5) * 0.1 for i in range(n)],
                "center_lon": [78.40 + (i % 5) * 0.1 for i in range(n)],
                "historical_flood_reported": [1 if i in [0, 1, 5, 6, 10] else 0 for i in range(n)],
            }
        )

        # Probabilities: some high, some low
        # Zone 0: actual=1, prob=0.85 -> TP
        # Zone 1: actual=1, prob=0.10 -> FN (missed flood)
        # Zone 2: actual=0, prob=0.75 -> FP (overprediction)
        # Zone 3: actual=0, prob=0.05 -> TN
        self.probabilities = np.array([
            0.85, 0.10, 0.75, 0.05, 0.15,
            0.80, 0.70, 0.10, 0.20, 0.05,
            0.65, 0.25, 0.05, 0.10, 0.05,
            0.15, 0.20, 0.05, 0.10, 0.05,
        ])

        self.analyzer = SpatialErrorAnalyzer(
            decision_threshold=0.30,
            artifacts_dir=self.artifacts_dir,
            data_dir=self.data_dir,
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_evaluate_study_area(self):
        summary = self.analyzer.evaluate_study_area(
            df_zones=self.df_zones,
            probabilities=self.probabilities,
        )

        self.assertEqual(summary["total_zones"], 20)
        self.assertEqual(summary["study_area"], "Hyderabad")
        self.assertEqual(summary["decision_threshold"], 0.30)

        # Confusion counts
        cm = summary["confusion_matrix"]
        self.assertGreater(cm["true_positives"], 0)
        self.assertGreater(cm["true_negatives"], 0)
        self.assertGreater(cm["false_positives"], 0)
        self.assertGreater(cm["false_negatives"], 0)
        self.assertEqual(sum(cm.values()), 20)

        # Metrics
        metrics = summary["metrics"]
        self.assertGreater(metrics["accuracy"], 0.50)
        self.assertIn("brier_score", metrics)

        # Quadrant breakdown
        quadrants = summary["quadrant_breakdown"]
        self.assertEqual(set(quadrants.keys()), {"NW", "NE", "SW", "SE"})

    def test_zone_records_residuals(self):
        summary = self.analyzer.evaluate_study_area(
            df_zones=self.df_zones,
            probabilities=self.probabilities,
        )
        records = summary["zone_errors"]
        self.assertEqual(len(records), 20)

        for rec in records:
            self.assertIn("zone_id", rec)
            self.assertIn(rec["error_category"], ERROR_COLOR_MAP)
            self.assertEqual(rec["color"], ERROR_COLOR_MAP[rec["error_category"]])
            self.assertAlmostEqual(rec["residual_error"], rec["actual_flood"] - rec["predicted_probability"], places=3)
            self.assertAlmostEqual(rec["brier_contribution"], rec["residual_error"] ** 2, places=3)

    def test_generate_error_geojson(self):
        summary = self.analyzer.evaluate_study_area(
            df_zones=self.df_zones,
            probabilities=self.probabilities,
        )
        geojson = self.analyzer.generate_error_geojson(summary)

        self.assertEqual(geojson["type"], "FeatureCollection")
        self.assertIn("metadata", geojson)
        self.assertEqual(geojson["metadata"]["layer_name"], "spatial_errors")
        self.assertIn("legend", geojson["metadata"])

    def test_save_artifacts(self):
        summary = self.analyzer.evaluate_study_area(
            df_zones=self.df_zones,
            probabilities=self.probabilities,
        )
        geojson = self.analyzer.generate_error_geojson(summary)
        paths = self.analyzer.save_artifacts(summary, geojson)

        self.assertTrue(os.path.exists(paths["json_path"]))
        self.assertTrue(os.path.exists(paths["geojson_path"]))


if __name__ == "__main__":
    unittest.main()
