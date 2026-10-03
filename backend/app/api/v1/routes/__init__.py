from backend.app.api.v1.routes.health import router as health_router
from backend.app.api.v1.routes.susceptibility import router as susceptibility_router
from backend.app.api.v1.routes.simulation import router as simulation_router

__all__ = ["health_router", "susceptibility_router", "simulation_router"]
