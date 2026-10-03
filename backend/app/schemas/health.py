from datetime import datetime, timezone
from typing import Dict
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok", description="Overall health status")
    environment: str = Field(..., description="Active runtime environment")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of the health check",
    )
    details: Dict[str, str] = Field(
        default_factory=dict,
        description="Component-level health details",
    )
