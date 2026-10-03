"""
Feature engineering definitions and matrix builder for FloodLens AI.
Extracts, transforms, and standardizes multi-modal geospatial features:
- Rainfall features (daily average, max intensity, cumulative, extreme frequency)
- Topographic features (elevation, slope, relative elevation depression)
- Drainage proximity features (distance to drainage, drainage density, log transforms)
- Land cover features (built-up impervious %, vegetation %, water %, open ground %)
- Explicit data missingness indicators
"""

from typing import List, Tuple, Dict, Any
import numpy as np
import pandas as pd

# Core numeric feature names used for training
NUMERIC_FEATURE_NAMES: List[str] = [
    # Meteorological
    "avg_daily_rainfall_mm",
    "max_daily_rainfall_mm",
    "cumulative_rainfall_mm",
    "extreme_rain_days_count",
    # Topographic / Terrain
    "elevation_m",
    "slope_deg",
    "relative_elevation_m",
    # Drainage / Hydrological
    "dist_to_drainage_m",
    "drainage_density_index",
    # Land Cover / Surface permeability
    "built_up_pct",
    "vegetation_pct",
    "water_pct",
    "open_ground_pct",
    # Engineered interaction features
    "impervious_to_drainage_ratio",
    "depression_slope_index",
    # Explicit Missingness Indicators
    "rainfall_missing",
    "elevation_missing",
    "drainage_missing",
    "land_cover_missing",
]


class FeatureBuilder:
    """
    Constructs and engineers predictive tabular feature matrices from zone records.
    """

    def __init__(self, feature_names: List[str] = NUMERIC_FEATURE_NAMES) -> None:
        self.feature_names = feature_names

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Derive interaction terms and domain-specific flood susceptibility indices.
        """
        data = df.copy()

        # 1. Impervious-to-drainage interaction:
        # High built-up percentage coupled with distant drainage creates highest waterlogging risk
        dist_km = (data["dist_to_drainage_m"] / 1000.0).clip(lower=0.1)
        data["impervious_to_drainage_ratio"] = (data["built_up_pct"] / dist_km).round(2)

        # 2. Depression-slope index:
        # Negative relative elevation (depression) combined with flat slope (< 2 deg) causes water accumulation
        flatness_factor = 1.0 / (data["slope_deg"].clip(lower=0.5))
        depression_factor = (-data["relative_elevation_m"]).clip(lower=0.0)
        data["depression_slope_index"] = (depression_factor * flatness_factor).round(2)

        # 3. Ensure missingness columns exist
        for col in ["rainfall_missing", "elevation_missing", "drainage_missing", "land_cover_missing"]:
            if col not in data.columns:
                data[col] = 0

        return data

    def extract_feature_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Produce a clean DataFrame restricted to the designated numeric feature set.
        """
        engineered = self.engineer_features(df)
        available_cols = [c for c in self.feature_names if c in engineered.columns]
        return engineered[available_cols].copy()
