import uuid
from fastapi import APIRouter
from backend.app.schemas.scenario import ScenarioSimulationRequest, ScenarioSimulationResponse

router = APIRouter()


@router.post(
    "/simulate",
    response_model=ScenarioSimulationResponse,
    tags=["Scenario Simulation"],
)
async def simulate_scenario(request: ScenarioSimulationRequest) -> ScenarioSimulationResponse:
    """
    Simulate impact of hypothetical land use or drainage modifications.
    Note: Decision-support planning tool; not an operational flood forecast.
    """
    return ScenarioSimulationResponse(
        scenario_id=str(uuid.uuid4()),
        impact_summary={
            "study_area": request.study_area,
            "target_zones_count": len(request.target_zone_ids),
            "interventions_count": len(request.interventions),
            "status": "ready_for_pipeline_integration",
        },
    )
