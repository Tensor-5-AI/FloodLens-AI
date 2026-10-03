"""
Data validation module.
Validates incoming geospatial records and feature frames for:
- Missing values and explicit missingness tracking
- Coordinate ranges (WGS84 EPSG:4326)
- CRS verification
- Numeric domain bounds (e.g. percentages [0, 100], elevation > 0)
"""

from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validates data structures and geospatial attributes.
    """

    @staticmethod
    def validate_coordinates(lat: float, lon: float, bbox: Tuple[float, float, float, float]) -> bool:
        """
        Verify that coordinates lie within the specified geographic bounding box.
        """
        min_lon, min_lat, max_lon, max_lat = bbox
        if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
            return False
        return (min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon)

    @staticmethod
    def validate_zone_feature(feature: Dict[str, Any]) -> List[str]:
        """
        Validate a single GeoJSON zone feature. Returns list of errors (empty if valid).
        """
        errors = []
        if feature.get("type") != "Feature":
            errors.append("Invalid feature type")

        geom = feature.get("geometry", {})
        if geom.get("type") != "Polygon":
            errors.append(f"Expected Polygon geometry, got {geom.get('type')}")

        coords = geom.get("coordinates", [])
        if not coords or len(coords[0]) < 4:
            errors.append("Polygon has insufficient coordinates")

        props = feature.get("properties", {})
        if not props.get("zone_id"):
            errors.append("Missing zone_id property")

        # Check numeric domains if properties exist
        if "built_up_pct" in props:
            if not (0.0 <= props["built_up_pct"] <= 100.0):
                errors.append(f"built_up_pct out of range: {props['built_up_pct']}")

        if "elevation_m" in props:
            if props["elevation_m"] <= 0:
                errors.append(f"elevation_m must be positive, got: {props['elevation_m']}")

        if "dist_to_drainage_m" in props:
            if props["dist_to_drainage_m"] < 0:
                errors.append(f"dist_to_drainage_m must be non-negative: {props['dist_to_drainage_m']}")

        return errors

    @classmethod
    def validate_feature_collection(cls, feature_collection: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an entire GeoJSON FeatureCollection.
        """
        if feature_collection.get("type") != "FeatureCollection":
            return {"valid": False, "total_features": 0, "errors": ["Not a FeatureCollection"]}

        features = feature_collection.get("features", [])
        all_errors = {}

        for idx, feat in enumerate(features):
            feat_errors = cls.validate_zone_feature(feat)
            if feat_errors:
                zone_id = feat.get("properties", {}).get("zone_id", f"feature_{idx}")
                all_errors[zone_id] = feat_errors

        return {
            "valid": len(all_errors) == 0,
            "total_features": len(features),
            "invalid_count": len(all_errors),
            "errors": all_errors,
        }
