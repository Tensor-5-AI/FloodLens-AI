from fastapi import APIRouter, Depends
from backend.app.config import Settings, get_settings
from backend.app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """
    Health check endpoint returning system status, environment, and version.
    """
    return HealthResponse(
        status="ok",
        environment=settings.ENVIRONMENT,
        version="0.1.0",
        details={
            "service": settings.PROJECT_NAME,
            "api_version": settings.API_V1_STR,
        },
    )
