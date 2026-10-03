"""
Unit tests for Primary Model: PyTorch Artificial Neural Network training,
comparative benchmarking against baseline, and inference integration.
"""

import unittest
import os
import shutil
import tempfile
import torch
import pandas as pd
import numpy as np

from ml.models.ann import FloodSusceptibilityANN
from ml.training.train_ann import ANNTrainer
from ml.inference.predictor import FloodPredictor


class TestANNTrainingAndInference(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.artifacts_dir = os.path.join(self.temp_dir, "artifacts")
        self.data_path = os.path.join(self.temp_dir, "features.csv")

        # Generate reproducible synthetic feature file with balanced positive signals
        np.random.seed(42)
        n = 60
        df = pd.DataFrame(
            {
                "zone_id": [f"ZONE_{i:03d}" for i in range(n)],
                "grid_row": [i // 6 for i in range(n)],
                "grid_col": [i % 6 for i in range(n)],
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

    def test_ann_model_architecture(self):
        model = FloodSusceptibilityANN(input_dim=19, hidden_dims=[32, 16], dropout_rate=0.1)
        x = torch.randn(4, 19)
        out = model(x)
        self.assertEqual(out.shape, (4, 1))
        # Sigmoid bounded between 0 and 1
        self.assertTrue((out >= 0.0).all() and (out <= 1.0).all())

    def test_ann_training_and_comparison_flow(self):
        trainer = ANNTrainer(
            data_path=self.data_path,
            artifacts_dir=self.artifacts_dir,
            test_ratio=0.25,
            hidden_dims=[32, 16],
            epochs=100,  # Fast run for unit test
            batch_size=8,
        )
        report = trainer.run()

        # Check report structure
        self.assertIn("primary_model", report)
        self.assertIn("comparison", report)
        self.assertEqual(report["primary_model"]["name"], "Artificial Neural Network (PyTorch)")
        self.assertIn("roc_auc", report["primary_model"]["test_metrics"])

        # Check saved model file
        ann_file = os.path.join(self.artifacts_dir, "ann_model.pt")
        comp_file = os.path.join(self.artifacts_dir, "model_comparison.json")
        self.assertTrue(os.path.exists(ann_file))
        self.assertTrue(os.path.exists(comp_file))

        # Check inference using saved PyTorch model
        preprocessor_file = os.path.join("ml/artifacts", "preprocessor.joblib")
        if os.path.exists(preprocessor_file):
            predictor = FloodPredictor(
                model_artifact_path=ann_file,
                preprocessor_artifact_path=preprocessor_file,
            )
            self.assertTrue(predictor.is_ready())
            test_zone = {
                "zone_id": "TEST_ANN_01",
                "avg_daily_rainfall_mm": 6.5,
                "max_daily_rainfall_mm": 150.0,
                "cumulative_rainfall_mm": 900.0,
                "extreme_rain_days_count": 5,
                "elevation_m": 492.0,
                "slope_deg": 1.1,
                "relative_elevation_m": -18.0,
                "dist_to_drainage_m": 250.0,
                "drainage_density_index": 0.85,
                "built_up_pct": 88.0,
                "vegetation_pct": 5.0,
                "water_pct": 2.0,
                "open_ground_pct": 5.0,
            }
            res = predictor.predict_zone(test_zone)
            self.assertEqual(res["zone_id"], "TEST_ANN_01")
            self.assertIn("susceptibility_score", res)
            self.assertIn("risk_category", res)


if __name__ == "__main__":
    unittest.main()
