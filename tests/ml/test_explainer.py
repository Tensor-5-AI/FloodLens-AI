"""
Unit tests for Model Explainability Engine (ml/explainability/explainer.py).
Verifies:
- SHAP KernelExplainer integration with PyTorch ANN and Baseline models
- Additive efficiency: E[f(x)] + sum(phi) == f(x)
- Local waterfall step sequencing, directional push classification, and formatting
- Global feature importance ranking by mean absolute SHAP attribution
- Causality disclaimer presence across all outputs
"""

import unittest
import os
import shutil
import tempfile
import numpy as np
import pandas as pd
import torch

from ml.models.ann import FloodSusceptibilityANN
from ml.preprocessing.pipeline import LeakageSafePreprocessor
from ml.explainability.explainer import (
    FloodExplainer,
    CAUSALITY_DISCLAIMER,
    format_raw_feature_value,
)


class TestFloodExplainer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.artifacts_dir = os.path.join(self.temp_dir, "artifacts")
        os.makedirs(self.artifacts_dir, exist_ok=True)
        self.data_path = os.path.join(self.temp_dir, "features.csv")

        # Generate synthetic feature dataset
        np.random.seed(42)
        n = 30
        df = pd.DataFrame(
            {
                "zone_id": [f"ZONE_TEST_{i:03d}" for i in range(n)],
                "grid_row": [i // 5 for i in range(n)],
                "grid_col": [i % 5 for i in range(n)],
                "center_lat": 17.30 + np.random.uniform(0, 0.2, n),
                "center_lon": 78.40 + np.random.uniform(0, 0.2, n),
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
                "rainfall_missing": [0] * n,
                "elevation_missing": [0] * n,
                "drainage_missing": [0] * n,
                "land_cover_missing": [0] * n,
            }
        )
        df.to_csv(self.data_path, index=False)
        self.df = df

        # Fit and persist preprocessor
        self.preprocessor = LeakageSafePreprocessor()
        self.preprocessor.fit(df)
        self.preprocessor_path = os.path.join(self.artifacts_dir, "preprocessor.joblib")
        self.preprocessor.save(self.preprocessor_path)

        # Build and persist miniature ANN
        input_dim = len(self.preprocessor.fitted_feature_names)
        self.ann = FloodSusceptibilityANN(input_dim=input_dim, hidden_dims=[16, 8], dropout_rate=0.0)
        self.ann_path = os.path.join(self.artifacts_dir, "ann_model.pt")
        torch.save(
            {
                "input_dim": input_dim,
                "hidden_dims": [16, 8],
                "dropout_rate": 0.0,
                "state_dict": self.ann.state_dict(),
            },
            self.ann_path,
        )

        # Initialize explainer
        self.explainer = FloodExplainer(
            model_artifact_path=self.ann_path,
            preprocessor_artifact_path=self.preprocessor_path,
            background_data_path=self.data_path,
            n_background_kmeans=10,
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_explainer_initialization(self):
        self.assertTrue(self.explainer.is_ready())
        self.assertIsNotNone(self.explainer.explainer)
        self.assertGreater(self.explainer.base_value, 0.0)
        self.assertLess(self.explainer.base_value, 1.0)
        self.assertEqual(len(self.explainer.feature_names), 19)

    def test_local_explanation_structure(self):
        sample = self.df.iloc[0]
        exp = self.explainer.explain_instance(sample, nsamples=40)

        # Check required fields
        self.assertEqual(exp["zone_id"], sample["zone_id"])
        self.assertIn("base_value", exp)
        self.assertIn("base_score", exp)
        self.assertIn("predicted_probability", exp)
        self.assertIn("susceptibility_score", exp)
        self.assertIn("risk_level", exp)
        self.assertIn("waterfall", exp)
        self.assertIn("top_risk_drivers", exp)
        self.assertIn("top_mitigating_factors", exp)
        self.assertIn("summary_text", exp)
        self.assertEqual(exp["causality_disclaimer"], CAUSALITY_DISCLAIMER)

        # Check waterfall steps
        waterfall = exp["waterfall"]
        self.assertEqual(len(waterfall), len(self.explainer.feature_names))
        for step in waterfall:
            self.assertIn("step_index", step)
            self.assertIn("feature_name", step)
            self.assertIn("feature_label", step)
            self.assertIn("raw_value", step)
            self.assertIn("formatted_value", step)
            self.assertIn("shap_value", step)
            self.assertIn("contribution_score", step)
            self.assertIn(step["direction"], ["INCREASES_SUSCEPTIBILITY", "DECREASES_SUSCEPTIBILITY", "NEUTRAL"])
            self.assertIn("cumulative_score", step)

    def test_additive_efficiency(self):
        """Verify SHAP additive property: base_value + sum(shap_values) == predicted_probability."""
        sample = self.df.iloc[2]
        exp = self.explainer.explain_instance(sample, nsamples=50)

        shap_sum = sum(f["shap_value"] for f in exp["waterfall"])
        reconstructed_prob = exp["base_value"] + shap_sum
        actual_prob = exp["predicted_probability"]

        self.assertAlmostEqual(reconstructed_prob, actual_prob, places=2)

    def test_directional_classification(self):
        sample = self.df.iloc[1]
        exp = self.explainer.explain_instance(sample, nsamples=40)

        for driver in exp["top_risk_drivers"]:
            self.assertEqual(driver["direction"], "INCREASES_SUSCEPTIBILITY")
            self.assertGreater(driver["shap_value"], 0.0)

        for mitigator in exp["top_mitigating_factors"]:
            self.assertEqual(mitigator["direction"], "DECREASES_SUSCEPTIBILITY")
            self.assertLess(mitigator["shap_value"], 0.0)

    def test_global_feature_importance(self):
        global_exp = self.explainer.explain_global(df_dataset=self.df.iloc[:15], nsamples=30)

        self.assertEqual(global_exp["study_area"], "Hyderabad")
        self.assertEqual(global_exp["total_zones_analyzed"], 15)
        self.assertIn("feature_importances", global_exp)
        self.assertIn("summary_text", global_exp)
        self.assertEqual(global_exp["causality_disclaimer"], CAUSALITY_DISCLAIMER)

        importances = global_exp["feature_importances"]
        self.assertEqual(len(importances), len(self.explainer.feature_names))

        # Check rankings are sorted descending by mean_abs_shap
        ranks = [f["rank"] for f in importances]
        self.assertEqual(ranks, list(range(1, len(importances) + 1)))

        mean_abs_values = [f["mean_abs_shap"] for f in importances]
        self.assertEqual(mean_abs_values, sorted(mean_abs_values, reverse=True))

    def test_format_raw_feature_value(self):
        self.assertEqual(format_raw_feature_value("built_up_pct", 75.4), "75.4%")
        self.assertEqual(format_raw_feature_value("avg_daily_rainfall_mm", 12.34), "12.3 mm")
        self.assertEqual(format_raw_feature_value("elevation_m", 512.67), "512.7 m")
        self.assertEqual(format_raw_feature_value("extreme_rain_days_count", 3), "3 days")

    def test_precompute_and_save_artifacts(self):
        save_dir = os.path.join(self.temp_dir, "saved_artifacts")
        paths = self.explainer.precompute_and_save_artifacts(output_dir=save_dir, nsamples=25)

        self.assertTrue(os.path.exists(paths["global_path"]))
        self.assertTrue(os.path.exists(paths["local_path"]))


if __name__ == "__main__":
    unittest.main()
