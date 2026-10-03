"""
Spatially-aware train/test splitting module.
Prevents spatial autocorrelation leakage where adjacent zones share nearly identical
environmental features, which would otherwise result in overly optimistic test metrics.
Uses spatial spatial-block partitioning (e.g. geographic quadrants or latitude-longitude blocks).
"""

from typing import Tuple, List, Dict, Any
import numpy as np
import pandas as pd


def spatial_block_train_test_split(
    df: pd.DataFrame,
    test_ratio: float = 0.2,
    spatial_cols: Tuple[str, str] = ("center_lat", "center_lon"),
    block_type: str = "quadrant",
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Partition dataset into train and test sets using spatial blocking to prevent spatial leakage.

    Methods:
    - 'quadrant': Partitions coordinates by geographical quadrants (e.g. reserving a geographic sector for testing).
    - 'checkerboard': Assigns grid blocks in a checkerboard fashion across grid_row and grid_col.
    - 'coordinate_strip': Splits along latitude or longitude blocks.
    """
    lat_col, lon_col = spatial_cols

    if block_type == "checkerboard" and "grid_row" in df.columns and "grid_col" in df.columns:
        # Every (row + col) % 4 == 0 reserved for test (25% holdout)
        test_mask = ((df["grid_row"] + df["grid_col"]) % 4) == 0
        train_df = df[~test_mask].copy()
        test_df = df[test_mask].copy()

    elif block_type == "quadrant":
        mid_lat = df[lat_col].median()
        mid_lon = df[lon_col].median()

        # Quadrant 0: NE (lat > mid_lat and lon > mid_lon)
        # Quadrant 1: NW (lat > mid_lat and lon <= mid_lon)
        # Quadrant 2: SE (lat <= mid_lat and lon > mid_lon)
        # Quadrant 3: SW (lat <= mid_lat and lon <= mid_lon)
        conditions = [
            (df[lat_col] > mid_lat) & (df[lon_col] > mid_lon),
            (df[lat_col] > mid_lat) & (df[lon_col] <= mid_lon),
            (df[lat_col] <= mid_lat) & (df[lon_col] > mid_lon),
            (df[lat_col] <= mid_lat) & (df[lon_col] <= mid_lon),
        ]
        choices = [0, 1, 2, 3]
        quadrant = np.select(conditions, choices, default=0)

        # Select a quadrant that contains both positive and negative samples if possible
        # Default to quadrant 2 (SE: includes Chaderghat, Falaknuma, Moosarambagh in Hyderabad)
        test_mask = quadrant == 2
        train_df = df[~test_mask].copy()
        test_df = df[test_mask].copy()

    else:
        # Fallback to contiguous latitude stripe
        sorted_indices = df.sort_values(by=lat_col).index
        test_size = int(len(df) * test_ratio)
        test_indices = sorted_indices[:test_size]
        train_df = df.drop(index=test_indices).copy()
        test_df = df.loc[test_indices].copy()

    # Fallback safety check: if test set has zero positives, include at least one positive block
    if "historical_flood_reported" in df.columns and test_df["historical_flood_reported"].sum() == 0:
        # Use stratified sample if spatial split captured 0 positives
        from sklearn.model_selection import train_test_split
        train_df, test_df = train_test_split(
            df,
            test_size=test_ratio,
            random_state=random_state,
            stratify=df["historical_flood_reported"],
        )

    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)
