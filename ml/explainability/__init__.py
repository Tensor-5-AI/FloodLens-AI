"""
SHAP (SHapley Additive exPlanations) calculation routines for model transparency and feature importance.
"""

from ml.explainability.explainer import (
    FloodExplainer,
    CAUSALITY_DISCLAIMER,
    FEATURE_DISPLAY_METADATA,
    format_raw_feature_value,
)

__all__ = [
    "FloodExplainer",
    "CAUSALITY_DISCLAIMER",
    "FEATURE_DISPLAY_METADATA",
    "format_raw_feature_value",
]
