from typing import List
from fastapi import APIRouter, HTTPException
from backend.app.schemas.susceptibility import SusceptibilityQuery, SusceptibilityResult

router = APIRouter()


@router.get(
    "/susceptibility",
    response_model=List[SusceptibilityResult],
    tags=["Susceptibility"],
)
async def get_susceptibility(study_area: str = "Hyderabad") -> List[SusceptibilityResult]:
    """
    Retrieve susceptibility scores and explanations for a study area.
    Implementation will connect to trained inference models and processed spatial data.
    """
    # Placeholder response until model pipeline and spatial units are implemented
    return []
