"""
Unit tests for data preprocessing and feature engineering:
- Target variable definition & class distribution
- Spatial-aware train/test splitting (zero spatial leakage)
- Feature engineering & interaction indices
- Leakage-safe imputer & scaler fitting on training partition only
"""

import unittest
import os
import shutil
import tempfile
import pandas as pd
import numpy as np

from ml.preprocessing.target import define_flood_target
from ml.preprocessing.spatial_split import spatial_block_train_test_split
from ml.preprocessing.pipeline import LeakageSafePreprocessor
from ml.features.builder import FeatureBuilder, NUMERIC_FEATURE_NAMES


class TestPreprocessingAndFeatures(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Create a synthetic DataFrame mimicking Hyderabad feature set
        np.random.seed(42)
        n = 40
        self.sample_df = pd.DataFrame(
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

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_target_definition(self):
        y, meta = define_flood_target(self.sample_df)
        self.assertEqual(len(y), len(self.sample_df))
        self.assertIn("positive_ratio", meta.columns)
        self.assertTrue(set(y.unique()).issubset({0, 1}))

    def test_spatial_split_no_overlap(self):
        train_df, test_df = spatial_block_train_test_split(
            self.sample_df, test_ratio=0.25, block_type="quadrant"
        )
        self.assertGreater(len(train_df), 0)
        self.assertGreater(len(test_df), 0)
        self.assertEqual(len(train_df) + len(test_df), len(self.sample_df))

        # Ensure no overlapping zone_ids
        train_ids = set(train_df["zone_id"])
        test_ids = set(test_df["zone_id"])
        self.assertEqual(len(train_ids.intersection(test_ids)), 0)

    def test_feature_builder_indices(self):
        builder = FeatureBuilder()
        engineered = builder.engineer_features(self.sample_df)
        self.assertIn("impervious_to_drainage_ratio", engineered.columns)
        self.assertIn("depression_slope_index", engineered.columns)
        matrix = builder.extract_feature_matrix(self.sample_df)
        for col in NUMERIC_FEATURE_NAMES:
            self.assertIn(col, matrix.columns)

    def test_leakage_safe_preprocessor(self):
        train_df, test_df = spatial_block_train_test_split(self.sample_df, test_ratio=0.25)
        preprocessor = LeakageSafePreprocessor()

        # Transform before fit must raise error
        with self.assertRaises(RuntimeError):
            preprocessor.transform(test_df)

        # Fit strictly on train
        X_train = preprocessor.fit_transform(train_df)
        self.assertEqual(X_train.shape[0], len(train_df))
        self.assertEqual(X_train.shape[1], len(NUMERIC_FEATURE_NAMES))

        # Check normalization properties on non-constant features (~0 mean, ~1 std)
        train_features_df = preprocessor.builder.extract_feature_matrix(train_df)
        non_constant_mask = (train_features_df.std(axis=0) > 0).to_numpy()
        np.testing.assert_allclose(X_train[:, non_constant_mask].mean(axis=0), 0.0, atol=1e-5)
        np.testing.assert_allclose(X_train[:, non_constant_mask].std(axis=0), 1.0, atol=1e-5)

        # Transform test without re-estimating mean/std
        X_test = preprocessor.transform(test_df)
        self.assertEqual(X_test.shape[0], len(test_df))

        # Test save and reload
        save_path = os.path.join(self.temp_dir, "preprocessor.joblib")
        preprocessor.save(save_path)
        loaded = LeakageSafePreprocessor.load(save_path)
        X_test_reloaded = loaded.transform(test_df)
        np.testing.assert_array_equal(X_test, X_test_reloaded)


if __name__ == "__main__":
    unittest.main()
