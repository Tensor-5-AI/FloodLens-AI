"""
Unit tests for baseline model training pipeline and inference predictor:
- BaselineTrainer workflow execution
- Metrics evaluation accuracy (Recall, Precision, F1, ROC-AUC, Confusion Matrix)
- Model artifact creation (baseline_model.joblib, preprocessor.joblib, baseline_metrics.json)
- FloodPredictor zone-level scoring and risk categorization
"""

import unittest
import os
import shutil
import tempfile
import pandas as pd
import numpy as np

from ml.evaluation.metrics import evaluate_binary_predictions
from ml.training.train_baseline import BaselineTrainer
from ml.inference.predictor import FloodPredictor, get_risk_category


class TestBaselinePipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.artifacts_dir = os.path.join(self.temp_dir, "artifacts")
        self.data_path = os.path.join(self.temp_dir, "features.csv")

        # Generate reproducible synthetic feature file with positive and negative records
        np.random.seed(42)
        n = 50
        df = pd.DataFrame(
            {
                "zone_id": [f"ZONE_{i:03d}" for i in range(n)],
                "grid_row": [i // 5 for i in range(n)],
                "grid_col": [i % 5 for i in range(n)],
                "center_lat": 17.20 + np.random.uniform(0, 0.4, n),
                "center_lon": 78.20 + np.random.uniform(0, 0.45, n),
                "avg_daily_rainfall_mm": np.random.uniform(4.0, 7.0, n),
                "max_daily_rainfall_mm": np.random.uniform(80.0, 160.0, n),
                "cumulative_rainfall_mm": np.random.uniform(700.0, 950.0, n),
                "extreme_rain_days_count": np.random.randint(1, 5, n),
                "elevation_m": np.random.uniform(490.0, 600.0, n),
                "slope_deg": np.random.uniform(1.0, 12.0, n),
                "relative_elevation_m": np.random.uniform(-30.0, 40.0, n),
                "dist_to_drainage_m": np.random.uniform(200.0, 5000.0, n),
                "drainage_density_index": np.random.uniform(0.1, 0.9, n),
                "built_up_pct": np.random.uniform(20.0, 90.0, n),
                "vegetation_pct": np.random.uniform(5.0, 50.0, n),
                "water_pct": np.random.uniform(1.0, 15.0, n),
                "open_ground_pct": np.random.uniform(5.0, 30.0, n),
                "historical_flood_reported": [1 if i % 4 == 0 else 0 for i in range(n)],
                "rainfall_missing": [0] * n,
                "elevation_missing": [0] * n,
                "drainage_missing": [0] * n,
                "land_cover_missing": [0] * n,
            }
        )
        df.to_csv(self.data_path, index=False)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_metrics_evaluation(self):
        y_true = [0, 0, 1, 1, 0, 1]
        y_pred = [0, 0, 1, 0, 0, 1]
        y_prob = [0.1, 0.2, 0.8, 0.4, 0.1, 0.9]

        metrics = evaluate_binary_predictions(y_true, y_pred, y_prob)
        self.assertEqual(metrics["true_positives"], 2)
        self.assertEqual(metrics["false_negatives"], 1)
        self.assertEqual(metrics["true_negatives"], 3)
        self.assertEqual(metrics["false_positives"], 0)
        self.assertAlmostEqual(metrics["recall"], 2 / 3, places=2)
        self.assertEqual(metrics["precision"], 1.0)
        self.assertGreater(metrics["roc_auc"], 0.8)

    def test_risk_categories(self):
        self.assertEqual(get_risk_category(85.0), "VERY HIGH")
        self.assertEqual(get_risk_category(65.0), "HIGH")
        self.assertEqual(get_risk_category(45.0), "MEDIUM")
        self.assertEqual(get_risk_category(25.0), "LOW")
        self.assertEqual(get_risk_category(10.0), "VERY LOW")

    def test_baseline_trainer_and_predictor_flow(self):
        trainer = BaselineTrainer(
            data_path=self.data_path,
            artifacts_dir=self.artifacts_dir,
            test_ratio=0.25,
        )
        report = trainer.run()

        # Check report contents
        self.assertEqual(report["model"], "LogisticRegression")
        self.assertIn("test_metrics", report)
        self.assertIn("feature_coefficients", report)

        # Check persisted artifact files
        model_file = os.path.join(self.artifacts_dir, "baseline_model.joblib")
        preprocessor_file = os.path.join(self.artifacts_dir, "preprocessor.joblib")
        metrics_file = os.path.join(self.artifacts_dir, "baseline_metrics.json")

        self.assertTrue(os.path.exists(model_file))
        self.assertTrue(os.path.exists(preprocessor_file))
        self.assertTrue(os.path.exists(metrics_file))

        # Test predictor
        predictor = FloodPredictor(
            model_artifact_path=model_file,
            preprocessor_artifact_path=preprocessor_file,
        )
        self.assertTrue(predictor.is_ready())

        test_zone = {
            "zone_id": "TEST_ZONE_01",
            "avg_daily_rainfall_mm": 6.2,
            "max_daily_rainfall_mm": 140.0,
            "cumulative_rainfall_mm": 880.0,
            "extreme_rain_days_count": 4,
            "elevation_m": 495.0,
            "slope_deg": 1.2,
            "relative_elevation_m": -15.0,
            "dist_to_drainage_m": 350.0,
            "drainage_density_index": 0.8,
            "built_up_pct": 85.0,
            "vegetation_pct": 8.0,
            "water_pct": 2.0,
            "open_ground_pct": 5.0,
        }

        res = predictor.predict_zone(test_zone)
        self.assertEqual(res["zone_id"], "TEST_ZONE_01")
        self.assertIn("susceptibility_score", res)
        self.assertIn("risk_category", res)
        self.assertIn("confidence", res)
        self.assertGreaterEqual(res["susceptibility_score"], 0.0)
        self.assertLessEqual(res["susceptibility_score"], 100.0)


if __name__ == "__main__":
    unittest.main()
