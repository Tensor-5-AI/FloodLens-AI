from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class InterventionParameter(BaseModel):
    """
    Hypothetical land use or drainage modification parameter.
    """
    parameter_name: str = Field(..., description="e.g., built_up_ratio, permeable_surface, drainage_capacity")
    delta_value: float = Field(..., description="Hypothetical change value or multiplier")


class ScenarioSimulationRequest(BaseModel):
    """
    Request payload for hypothetical land-use/construction scenario simulation.
    """
    study_area: str = Field(default="Hyderabad", description="Target study area / city")
    target_zone_ids: List[str] = Field(..., description="Zones subjected to hypothetical intervention")
    interventions: List[InterventionParameter] = Field(..., description="List of applied hypothetical modifications")


class ScenarioSimulationResponse(BaseModel):
    """
    Response containing delta impact on flood susceptibility.
    """
    scenario_id: str
    impact_summary: Dict[str, Any]
    disclaimer: str = Field(
        default="Hypothetical scenario simulation for decision-support planning only; not a physical flood forecast.",
        description="Mandatory model constraint disclaimer",
    )
