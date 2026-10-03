from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ConfidenceDimensionScores(BaseModel):
    """
    Sub-scores (0-100) across key data quality dimensions.
    """
    feature_completeness: float = Field(..., ge=0.0, le=100.0, description="Completeness across 5 core sensor modalities")
    sensor_proximity: float = Field(..., ge=0.0, le=100.0, description="Proximity to drainage networks and sensor resolution")
    historical_evidence: float = Field(..., ge=0.0, le=100.0, description="Quality and availability of historical flood incident logs")
    spatial_coverage: float = Field(..., ge=0.0, le=100.0, description="Zone geometry validity and coordinate precision")


class ZoneConfidenceResponse(BaseModel):
    """
    Zone-level data confidence and evidence quality profile.
    """
    zone_id: str = Field(..., description="Unique zone identifier")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Composite confidence score between 0.0 and 1.0")
    confidence_percentage: float = Field(..., ge=0.0, le=100.0, description="Confidence expressed as 0-100%")
    confidence_tier: str = Field(..., description="Quality tier: VERY LOW, LOW, MEDIUM, HIGH, VERY HIGH")
    dimension_scores: ConfidenceDimensionScores = Field(..., description="Breakdown across individual quality dimensions")
    missing_modalities: List[str] = Field(default_factory=list, description="List of unobserved or missing data modalities")
    susceptibility_score: Optional[float] = Field(default=None, description="Current model susceptibility score for risk-confidence matrix")
    risk_level: Optional[str] = Field(default=None, description="Assigned susceptibility risk level")
    risk_confidence_quadrant: str = Field(
        ...,
        description="2x2 Matrix Quadrant: PRIORITIZED_ACTION_ZONE, GROUND_VERIFICATION_REQUIRED, DATA_BLINDSPOT, or VERIFIED_SAFE_ZONE",
    )
    recommendation: str = Field(..., description="Strategic decision recommendation for urban planners")
    data_quality_notes: List[str] = Field(default_factory=list, description="Specific observational notes explaining confidence rating")


class StudyAreaConfidenceSummary(BaseModel):
    """
    City-wide aggregated confidence metrics.
    """
    study_area: str = Field(default="Hyderabad", description="Target study area name")
    total_zones: int = Field(..., description="Total count of evaluated zones")
    mean_confidence: float = Field(..., ge=0.0, le=1.0, description="Average composite confidence score")
    mean_confidence_percentage: float = Field(..., ge=0.0, le=100.0, description="Average confidence percentage")
    high_confidence_zones_count: int = Field(..., description="Count of zones with high confidence coverage")
    low_confidence_zones_count: int = Field(..., description="Count of zones with low data confidence")
    data_blindspot_zones_count: int = Field(..., description="Zones with low predicted risk but low data confidence")
    priority_action_zones_count: int = Field(..., description="Zones with high risk and high data confidence")
    quadrant_distribution: Dict[str, int] = Field(default_factory=dict, description="Zone count per risk-confidence quadrant")
