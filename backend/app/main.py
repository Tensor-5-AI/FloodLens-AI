from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import get_settings
from backend.app.api.v1.routes.health import router as health_router
from backend.app.api.v1.routes.susceptibility import router as susceptibility_router
from backend.app.api.v1.routes.simulation import router as simulation_router
from backend.app.api.v1.routes.zones import router as zones_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup tasks (if needed in future: load model caches, verify data dirs)
    yield
    # Shutdown cleanup


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="Explainable Urban Flood Susceptibility & Planning Decision-Support Platform API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS configuration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers - mounted with API version prefix and root aliases for convenience
    api_prefix = settings.API_V1_STR
    application.include_router(health_router, prefix=api_prefix)
    application.include_router(susceptibility_router, prefix=api_prefix)
    application.include_router(simulation_router, prefix=api_prefix)
    application.include_router(zones_router, prefix=api_prefix)
    application.include_router(zones_router)  # Root alias: /zones/{zone_id}/explanation


    @application.get("/", tags=["Root"])
    async def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": "0.1.0",
            "docs": "/docs",
            "health": f"{api_prefix}/health",
        }

    return application


app = create_application()
