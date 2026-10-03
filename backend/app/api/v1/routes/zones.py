from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends

from backend.app.schemas.explanation import ZoneExplanationResponse, GlobalExplanationResponse
from backend.app.schemas.confidence import ZoneConfidenceResponse, StudyAreaConfidenceSummary
from backend.app.services.inference import ModelInferenceService

from backend.app.services.spatial import SpatialDataService
from backend.app.config import get_settings

router = APIRouter(tags=["Zones & Explainability"])
settings = get_settings()

_inference_service: Optional[ModelInferenceService] = None
_spatial_service: Optional[SpatialDataService] = None


def get_inference_service() -> ModelInferenceService:
    global _inference_service
    if _inference_service is None:
        _inference_service = ModelInferenceService(
            model_artifacts_dir=settings.MODEL_ARTIFACTS_DIR,
            data_dir=settings.PROCESSED_DATA_DIR,
        )
    return _inference_service


def get_spatial_service() -> SpatialDataService:
    global _spatial_service
    if _spatial_service is None:
        _spatial_service = SpatialDataService(data_dir=settings.PROCESSED_DATA_DIR)
    return _spatial_service


@router.get(
    "/zones/explanations/global",
    response_model=GlobalExplanationResponse,
    summary="Get Global SHAP Feature Importances",
    description="Retrieve study-area wide global feature importance rankings derived via SHAP.",
)
async def get_global_explanation(
    study_area: str = Query("Hyderabad", description="Study area city"),
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> GlobalExplanationResponse:
    explanation = inference_service.get_global_explanation(study_area=study_area)
    return GlobalExplanationResponse(**explanation)


@router.get(
    "/zones/{zone_id}/explanation",
    response_model=ZoneExplanationResponse,
    summary="Get Zone Local SHAP Explanation",
    description="Retrieve detailed local SHAP feature attributions, waterfall data, and directional impact for a zone.",
)
async def get_zone_explanation(
    zone_id: str,
    study_area: str = Query("Hyderabad", description="Target study area / city"),
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> ZoneExplanationResponse:
    explanation = inference_service.explain_zone(zone_id=zone_id, study_area=study_area)
    if explanation is None:
        raise HTTPException(
            status_code=404,
            detail=f"Zone '{zone_id}' not found in study area '{study_area}'.",
        )
    return ZoneExplanationResponse(**explanation)


@router.post(
    "/zones/explain",
    response_model=ZoneExplanationResponse,
    summary="Explain Custom Zone Features",
    description="Generate on-the-fly SHAP explanation for an arbitrary set of input zone features.",
)
async def explain_custom_features(
    features: Dict[str, Any],
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> ZoneExplanationResponse:
    try:
        explanation = inference_service.explain_prediction(features)
        return ZoneExplanationResponse(**explanation)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate explanation for features: {str(e)}",
        )


@router.get(
    "/zones/confidence/summary",
    response_model=StudyAreaConfidenceSummary,
    summary="Get Study Area Confidence Summary",
    description="Retrieve city-wide aggregated data quality and risk-confidence matrix distributions.",
)
async def get_confidence_summary(
    study_area: str = Query("Hyderabad", description="Study area city"),
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> StudyAreaConfidenceSummary:
    summary = inference_service.evaluate_study_area_confidence(study_area=study_area)
    return StudyAreaConfidenceSummary(**summary)


@router.get(
    "/zones/{zone_id}/confidence",
    response_model=ZoneConfidenceResponse,
    summary="Get Zone Data Confidence & Evidence Quality",
    description="Retrieve multi-modal data completeness, sensor coverage, and Risk vs Confidence quadrant for a zone.",
)
async def get_zone_confidence(
    zone_id: str,
    study_area: str = Query("Hyderabad", description="Target study area / city"),
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> ZoneConfidenceResponse:
    profile = inference_service.evaluate_zone_confidence(zone_id=zone_id, study_area=study_area)
    if profile is None:
        raise HTTPException(
            status_code=404,
            detail=f"Zone '{zone_id}' not found in study area '{study_area}'.",
        )
    return ZoneConfidenceResponse(**profile)


@router.get(
    "/zones/{zone_id}/prediction",
    summary="Get Zone Prediction",
    description="Retrieve susceptibility score, risk tier, and confidence for a specific zone.",
)

async def get_zone_prediction(
    zone_id: str,
    study_area: str = Query("Hyderabad", description="Study area city"),
    inference_service: ModelInferenceService = Depends(get_inference_service),
) -> Dict[str, Any]:
    prediction = inference_service.predict_zone(zone_id=zone_id, study_area=study_area)
    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail=f"Zone '{zone_id}' not found in study area '{study_area}'.",
        )
    return prediction


@router.get(
    "/zones/{zone_id}",
    summary="Get Zone Feature Profile",
    description="Retrieve all environmental, terrain, and drainage features for a specific zone.",
)
async def get_zone_details(
    zone_id: str,
    study_area: str = Query("Hyderabad", description="Study area city"),
    spatial_service: SpatialDataService = Depends(get_spatial_service),
) -> Dict[str, Any]:
    features = spatial_service.get_zone_features(zone_id=zone_id, study_area=study_area)
    if features is None:
        raise HTTPException(
            status_code=404,
            detail=f"Zone '{zone_id}' not found in study area '{study_area}'.",
        )
    return features


@router.get(
    "/zones",
    summary="List All Zones",
    description="List all available geographic zone identifiers in the study area.",
)
async def list_zones(
    study_area: str = Query("Hyderabad", description="Study area city"),
    spatial_service: SpatialDataService = Depends(get_spatial_service),
) -> List[Dict[str, Any]]:
    df = spatial_service.get_all_zone_features(study_area=study_area)
    if df.empty or "zone_id" not in df.columns:
        return []

    cols_to_include = [c for c in ["zone_id", "center_lat", "center_lon", "area_sqkm"] if c in df.columns]
    return df[cols_to_include].to_dict(orient="records")
