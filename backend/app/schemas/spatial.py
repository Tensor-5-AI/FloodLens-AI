from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ZoneSpatialError(BaseModel):
    """
    Spatial residual and error classification for an individual zone.
    """
    zone_id: str = Field(..., description="Unique zone identifier")
    actual_flood: int = Field(..., description="Ground truth historical flood label (0 or 1)")
    predicted_probability: float = Field(..., ge=0.0, le=1.0, description="Model predicted susceptibility probability")
    susceptibility_score: float = Field(..., ge=0.0, le=100.0, description="Susceptibility score (0-100)")
    predicted_binary: int = Field(..., description="Binary classification based on decision threshold (0 or 1)")
    error_category: str = Field(
        ...,
        description="Spatial error category: TRUE_POSITIVE, TRUE_NEGATIVE, FALSE_POSITIVE, or FALSE_NEGATIVE",
    )
    color: str = Field(..., description="Hex color code for map layer rendering")
    residual_error: float = Field(..., description="Signed error residual (actual - predicted_probability)")
    absolute_error: float = Field(..., description="Absolute error residual |actual - predicted_probability|")
    brier_contribution: float = Field(..., description="Squared error residual contribution to Brier score")
    quadrant: str = Field(..., description="Geographic quadrant in study area: NW, NE, SW, or SE")
    center_lat: float = Field(..., description="Centroid latitude")
    center_lon: float = Field(..., description="Centroid longitude")
    description: str = Field(..., description="Human-readable assessment of the classification or error")


class QuadrantErrorStats(BaseModel):
    """
    Performance and error metrics for a specific geographic quadrant.
    """
    total_zones: int = Field(..., description="Total count of zones in quadrant")
    accuracy: float = Field(..., ge=0.0, le=1.0, description="Accuracy in this quadrant")
    true_positives: int = Field(..., description="True positive zone count")
    true_negatives: int = Field(..., description="True negative zone count")
    false_positives: int = Field(..., description="False positive zone count")
    false_negatives: int = Field(..., description="False negative zone count")


class SpatialClusteringSummary(BaseModel):
    """
    Geographic error clustering analysis across study area quadrants.
    """
    weakest_quadrant: Optional[str] = Field(default=None, description="Quadrant with lowest accuracy")
    weakest_quadrant_accuracy: Optional[float] = Field(default=None, description="Accuracy in weakest quadrant")
    high_false_positive_clusters: List[str] = Field(default_factory=list, description="Quadrants with elevated over-prediction")
    high_false_negative_clusters: List[str] = Field(default_factory=list, description="Quadrants with critical missed floods")


class SpatialErrorSummary(BaseModel):
    """
    Complete spatial error evaluation summary for the study area.
    """
    study_area: str = Field(default="Hyderabad", description="Study area city")
    decision_threshold: float = Field(..., description="Binary decision threshold used for classification")
    total_zones: int = Field(..., description="Total zones analyzed")
    confusion_matrix: Dict[str, int] = Field(..., description="Counts of TP, TN, FP, FN")
    metrics: Dict[str, float] = Field(..., description="Overall accuracy, precision, recall, f1, and brier score")
    quadrant_breakdown: Dict[str, QuadrantErrorStats] = Field(..., description="Performance per geographic quadrant")
    spatial_clustering: SpatialClusteringSummary = Field(..., description="Geographic error clustering assessment")
    zone_errors: Optional[List[ZoneSpatialError]] = Field(default=None, description="Optional detailed per-zone error list")


class SpatialErrorMapLayerResponse(BaseModel):
    """
    GeoJSON FeatureCollection formatted response for MapLibre/Cesium rendering.
    """
    type: str = Field(default="FeatureCollection", description="GeoJSON type")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Layer metadata, decision threshold, and styling legend")
    features: List[Dict[str, Any]] = Field(..., description="GeoJSON features with styled spatial error properties")
