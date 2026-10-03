from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends

from backend.app.schemas.susceptibility import SusceptibilityQuery, SusceptibilityResult, SusceptibilityFeatureContribution
from backend.app.api.v1.routes.zones import get_inference_service, get_spatial_service
from backend.app.services.inference import ModelInferenceService
from backend.app.services.spatial import SpatialDataService

router = APIRouter(tags=["Susceptibility"])


@router.get(
    "/susceptibility",
    response_model=List[SusceptibilityResult],
    summary="Get Study Area Susceptibility & SHAP Explanations",
    description="Retrieve susceptibility scores, confidence proxies, and top SHAP explanations for all zones.",
)
async def get_susceptibility(
    study_area: str = "Hyderabad",
    inference_service: ModelInferenceService = Depends(get_inference_service),
    spatial_service: SpatialDataService = Depends(get_spatial_service),
) -> List[SusceptibilityResult]:
    """
    Retrieve susceptibility scores and SHAP explanations for a study area.
    """
    df = spatial_service.get_all_zone_features(study_area=study_area)
    if df.empty or "zone_id" not in df.columns:
        return []

    results: List[SusceptibilityResult] = []

    # Iterate through zones and enrich with predictions & top SHAP factors
    for idx in range(len(df)):
        row = df.iloc[idx]
        zone_id = str(row.get("zone_id", f"ZONE_{idx:03d}"))

        exp = inference_service.explain_zone(zone_id=zone_id, study_area=study_area)
        if exp:
            prob = exp.get("predicted_probability", 0.0)
            risk = exp.get("risk_level", "LOW")
            top_drivers = exp.get("top_risk_drivers", [])
            top_shap = [
                SusceptibilityFeatureContribution(
                    feature_name=d["feature_name"],
                    feature_value=float(d.get("raw_value", 0.0)),
                    shap_value=float(d.get("shap_value", 0.0)),
                )
                for d in top_drivers[:3]
            ]
        else:
            prob = 0.0
            risk = "VERY LOW"
            top_shap = []

        # Confidence proxy calculation
        missing_count = sum(int(row.get(c, 0)) for c in ["rainfall_missing", "elevation_missing", "drainage_missing", "land_cover_missing"] if c in row)
        confidence = round(max(0.4, 1.0 - (missing_count * 0.15)), 2)

        results.append(
            SusceptibilityResult(
                zone_id=zone_id,
                susceptibility_score=prob,
                risk_level=risk,
                confidence_score=confidence,
                top_explanations=top_shap,
                metadata={
                    "center_lat": float(row.get("center_lat", 0.0)),
                    "center_lon": float(row.get("center_lon", 0.0)),
                },
            )
        )

    return results
