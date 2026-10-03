from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SusceptibilityQuery(BaseModel):
    """
    Query parameters for retrieving susceptibility data.
    The exact geographic unit (grid cell vs admin boundary) and resolution are pending.
    """
    study_area: str = Field(default="Hyderabad", description="Target study area / city")
    zone_ids: Optional[List[str]] = Field(default=None, description="Optional filter by specific zone IDs")


class SusceptibilityFeatureContribution(BaseModel):
    """
    SHAP explanation feature contribution structure.
    """
    feature_name: str
    feature_value: float
    shap_value: float


class SusceptibilityResult(BaseModel):
    """
    Zone-level flood susceptibility result skeleton.
    """
    zone_id: str
    susceptibility_score: float = Field(..., ge=0.0, le=1.0, description="Estimated flood susceptibility score")
    risk_level: Optional[str] = Field(default=None, description="Risk category (thresholds pending determination)")
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Data quality / confidence score")
    top_explanations: Optional[List[SusceptibilityFeatureContribution]] = Field(
        default=None,
        description="Top driving factors derived via SHAP",
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)
