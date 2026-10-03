"""
Target variable definition for urban flood susceptibility classification.
Formulates the ground-truth target based on verifiable historical incident occurrence,
waterlogging frequency, and localized inundation records.
"""

from typing import Tuple
import pandas as pd
import numpy as np


def define_flood_target(
    df: pd.DataFrame,
    target_column: str = "historical_flood_reported",
    min_incidents: int = 1,
) -> Tuple[pd.Series, pd.DataFrame]:
    """
    Extracts and validates the binary flood susceptibility target.
    Label 1 = Zone has documented flood/waterlogging history or severe hotspot proximity.
    Label 0 = Zone without documented inundation incidents in public records.

    Returns:
        y: Binary target series (0 or 1)
        target_metadata: Class distribution and balance statistics
    """
    if target_column in df.columns:
        y = (df[target_column] >= min_incidents).astype(int)
    elif "historical_incident_count" in df.columns:
        y = (df["historical_incident_count"] >= min_incidents).astype(int)
    else:
        raise KeyError(f"Neither '{target_column}' nor 'historical_incident_count' found in dataframe.")

    value_counts = y.value_counts().to_dict()
    positive_count = int(value_counts.get(1, 0))
    negative_count = int(value_counts.get(0, 0))
    pos_ratio = positive_count / max(1, len(y))

    metadata = {
        "total_samples": len(y),
        "positive_count": positive_count,
        "negative_count": negative_count,
        "positive_ratio": round(pos_ratio, 4),
        "imbalance_ratio": round(negative_count / max(1, positive_count), 2),
    }

    return y, pd.DataFrame([metadata])
