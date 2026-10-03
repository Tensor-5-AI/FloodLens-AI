from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FeatureContribution(BaseModel):
    """
    Detailed SHAP factor attribution for a single feature.
    """
    feature_name: str = Field(..., description="Raw internal feature identifier")
    feature_label: str = Field(..., description="Human-friendly feature label")
    raw_value: float = Field(..., description="Original unscaled numeric feature value")
    formatted_value: str = Field(..., description="Formatted feature value with physical unit")
    scaled_value: Optional[float] = Field(default=None, description="Standardized feature value fed to model")
    shap_value: float = Field(..., description="Raw SHAP attribution in probability space")
    contribution_score: float = Field(..., description="Contribution in 0-100 score points (+/-)")
    magnitude: Optional[float] = Field(default=None, description="Absolute magnitude of SHAP attribution")
    direction: str = Field(
        ...,
        description="Directional push: INCREASES_SUSCEPTIBILITY, DECREASES_SUSCEPTIBILITY, or NEUTRAL",
    )
    direction_label: Optional[str] = Field(default=None, description="Descriptive direction summary")


class WaterfallStep(BaseModel):
    """
    Step in the SHAP waterfall progression explaining susceptibility score derivation.
    """
    step_index: int = Field(..., description="Order of feature contribution in waterfall")
    feature_name: str = Field(..., description="Raw internal feature identifier")
    feature_label: str = Field(..., description="Human-friendly feature label")
    raw_value: float = Field(..., description="Original unscaled numeric feature value")
    formatted_value: str = Field(..., description="Formatted feature value with physical unit")
    shap_value: float = Field(..., description="Raw SHAP attribution in probability space")
    contribution_score: float = Field(..., description="Contribution in 0-100 score points (+/-)")
    direction: str = Field(
        ...,
        description="Directional push: INCREASES_SUSCEPTIBILITY, DECREASES_SUSCEPTIBILITY, or NEUTRAL",
    )
    direction_label: Optional[str] = Field(default=None, description="Descriptive direction summary")
    cumulative_score: float = Field(
        ...,
        description="Running cumulative susceptibility score after applying this feature attribution",
    )


class ZoneExplanationResponse(BaseModel):
    """
    Comprehensive local SHAP explanation response for a specific zone.
    """
    zone_id: str = Field(..., description="Unique geographic zone identifier")
    model_name: str = Field(..., description="Name and type of the model producing explanations")
    base_value: float = Field(..., description="Regional baseline expected probability E[f(x)]")
    base_score: float = Field(..., description="Baseline expected score out of 100")
    predicted_probability: float = Field(..., ge=0.0, le=1.0, description="Model predicted flood probability")
    susceptibility_score: float = Field(..., ge=0.0, le=100.0, description="Model susceptibility score (0-100)")
    risk_level: str = Field(..., description="Risk tier (VERY LOW, LOW, MEDIUM, HIGH, VERY HIGH)")
    waterfall: List[WaterfallStep] = Field(
        ...,
        description="Sequential waterfall data showing additive shifts from base score to final prediction",
    )
    all_features: Optional[List[FeatureContribution]] = Field(
        default=None,
        description="Complete list of all evaluated features and their SHAP attributions",
    )
    top_risk_drivers: List[FeatureContribution] = Field(
        default_factory=list,
        description="Features creating the strongest upward push on susceptibility",
    )
    top_mitigating_factors: List[FeatureContribution] = Field(
        default_factory=list,
        description="Features providing the strongest mitigating/downward push on susceptibility",
    )
    summary_text: str = Field(
        ...,
        description="Human-readable synthesis explaining why the model assigned this risk level",
    )
    causality_disclaimer: str = Field(
        ...,
        description="Mandatory disclaimer stating SHAP describes model behavior, not physical causality",
    )


class GlobalFeatureImportance(BaseModel):
    """
    Aggregated global SHAP importance for a single feature across all zones.
    """
    rank: int = Field(..., description="Importance rank (1 = highest influence)")
    feature_name: str = Field(..., description="Feature identifier")
    feature_label: str = Field(..., description="Human-friendly label")
    mean_abs_shap: float = Field(..., description="Mean absolute SHAP value across study area")
    mean_abs_score: float = Field(..., description="Mean absolute score impact (0-100 scale)")
    mean_shap: float = Field(..., description="Mean directional SHAP value across study area")
    min_shap: float = Field(..., description="Minimum observed SHAP attribution")
    max_shap: float = Field(..., description="Maximum observed SHAP attribution")
    general_direction: str = Field(..., description="Dominant directional tendency across the city")


class GlobalExplanationResponse(BaseModel):
    """
    Global SHAP feature importance response summarizing model behavior across the entire study area.
    """
    study_area: str = Field(default="Hyderabad", description="Study area city")
    model_name: str = Field(..., description="Model name and architecture")
    base_value: float = Field(..., description="Base expected probability across study area")
    base_score: float = Field(..., description="Base expected score (0-100)")
    total_zones_analyzed: int = Field(..., description="Total count of geographic zones evaluated")
    feature_importances: List[GlobalFeatureImportance] = Field(
        ...,
        description="Ranked list of feature importances by mean absolute impact",
    )
    summary_text: str = Field(..., description="High-level narrative summarizing primary model drivers")
    causality_disclaimer: str = Field(
        ...,
        description="Mandatory disclaimer stating SHAP describes model behavior, not physical causality",
    )
