from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from backend.app.schemas.spatial import SpatialErrorSummary, SpatialErrorMapLayerResponse, ZoneSpatialError
from backend.app.api.v1.routes.zones import get_inference_service, get_spatial_service
from backend.app.services.inference import ModelInferenceService
from backend.app.services.spatial import SpatialDataService

router = APIRouter(tags=["Spatial Error Analysis & Layers"])


@router.get(
    "/spatial/errors",
    response_model=SpatialErrorSummary,
    summary="Get Spatial Error Analysis Summary",
    description="Retrieve study-area wide spatial residuals, confusion matrix (TP/TN/FP/FN), and quadrant error clustering.",
)
async def get_spatial_errors(
    study_area: str = Query("Hyderabad", description="Study area city"),
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> SpatialErrorSummary:
    summary = inference_service.get_spatial_error_analysis(study_area=study_area)
    return SpatialErrorSummary(**summary)


@router.get(
    "/layers/spatial_errors",
    response_model=SpatialErrorMapLayerResponse,
    summary="Get Spatial Error GeoJSON Layer",
    description="Retrieve styled GeoJSON polygons with color-coded classification attributes for MapLibre / Cesium visualization.",
)
async def get_spatial_error_layer(
    study_area: str = Query("Hyderabad", description="Study area city"),
    spatial_service: SpatialDataService = Depends(get_spatial_service),
) -> SpatialErrorMapLayerResponse:
    geojson_data = spatial_service.get_spatial_error_geojson(study_area=study_area)
    return SpatialErrorMapLayerResponse(**geojson_data)


@router.get(
    "/layers/{layer_name}",
    summary="Get Generic Map Layer",
    description="Retrieve available spatial layers (e.g. zones, spatial_errors) in GeoJSON format.",
)
async def get_named_layer(
    layer_name: str,
    study_area: str = Query("Hyderabad", description="Study area city"),
    spatial_service: SpatialDataService = Depends(get_spatial_service),
) -> Dict[str, Any]:
    if layer_name.lower() in ["spatial_errors", "spatial_error", "errors"]:
        return spatial_service.get_spatial_error_geojson(study_area=study_area)
    elif layer_name.lower() in ["zones", "zone"]:
        return spatial_service.get_zone_geojson(study_area=study_area)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Layer '{layer_name}' not found for study area '{study_area}'. Available layers: zones, spatial_errors",
        )


@router.get(
    "/zones/{zone_id}/spatial_error",
    response_model=ZoneSpatialError,
    summary="Get Zone Spatial Error",
    description="Retrieve spatial error classification (TP/TN/FP/FN), residual, and Brier contribution for a specific zone.",
)
async def get_zone_spatial_error(
    zone_id: str,
    study_area: str = Query("Hyderabad", description="Study area city"),
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> ZoneSpatialError:
    error_data = inference_service.get_zone_spatial_error(zone_id=zone_id, study_area=study_area)
    if error_data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Zone '{zone_id}' not found in study area '{study_area}'.",
        )
    return ZoneSpatialError(**error_data)
