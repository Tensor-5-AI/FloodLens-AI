"""
Grid-based and administrative zone generator for Hyderabad study area.
Divides the study area into reproducible geographic units (zones) for data ingestion and feature aggregation.
"""

from typing import Dict, List, Any, Tuple
import math
from ml.ingestion.sources import HYDERABAD_BBOX


def generate_grid_zones(
    bbox: Tuple[float, float, float, float] = HYDERABAD_BBOX,
    rows: int = 10,
    cols: int = 10,
) -> Dict[str, Any]:
    """
    Generate regular geographic grid cells across the bounding box.
    Returns GeoJSON FeatureCollection with standardized properties:
    - zone_id (e.g. ZONE_HYD_001)
    - name
    - bounds: [min_lon, min_lat, max_lon, max_lat]
    - center: [center_lon, center_lat]
    - area_sqkm
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    lat_step = (max_lat - min_lat) / rows
    lon_step = (max_lon - min_lon) / cols

    features: List[Dict[str, Any]] = []
    zone_index = 1

    # Approximate 1 degree latitude ~ 111 km; 1 degree longitude at ~17.4 deg lat ~ 111 * cos(17.4°) ≈ 105.9 km
    km_per_lat = 111.0
    km_per_lon = 111.0 * math.cos(math.radians((min_lat + max_lat) / 2))
    cell_area_sqkm = round((lat_step * km_per_lat) * (lon_step * km_per_lon), 2)

    for r in range(rows):
        for c in range(cols):
            cell_min_lat = min_lat + r * lat_step
            cell_max_lat = min_lat + (r + 1) * lat_step
            cell_min_lon = min_lon + c * lon_step
            cell_max_lon = min_lon + (c + 1) * lon_step

            center_lat = round((cell_min_lat + cell_max_lat) / 2, 5)
            center_lon = round((cell_min_lon + cell_max_lon) / 2, 5)

            zone_id = f"ZONE_HYD_{zone_index:03d}"

            # GeoJSON polygon coordinate ring (closed loop: 5 vertices)
            polygon_coords = [
                [
                    [round(cell_min_lon, 5), round(cell_min_lat, 5)],
                    [round(cell_max_lon, 5), round(cell_min_lat, 5)],
                    [round(cell_max_lon, 5), round(cell_max_lat, 5)],
                    [round(cell_min_lon, 5), round(cell_max_lat, 5)],
                    [round(cell_min_lon, 5), round(cell_min_lat, 5)],
                ]
            ]

            feature = {
                "type": "Feature",
                "id": zone_id,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": polygon_coords,
                },
                "properties": {
                    "zone_id": zone_id,
                    "grid_row": r,
                    "grid_col": c,
                    "center_lat": center_lat,
                    "center_lon": center_lon,
                    "min_lat": round(cell_min_lat, 5),
                    "max_lat": round(cell_max_lat, 5),
                    "min_lon": round(cell_min_lon, 5),
                    "max_lon": round(cell_max_lon, 5),
                    "area_sqkm": cell_area_sqkm,
                    "city": "Hyderabad",
                    "state": "Telangana",
                    "country": "India",
                },
            }
            features.append(feature)
            zone_index += 1

    return {
        "type": "FeatureCollection",
        "metadata": {
            "study_area": "Hyderabad, Telangana, India",
            "bbox": bbox,
            "total_zones": len(features),
            "rows": rows,
            "cols": cols,
            "crs": "urn:ogc:def:crs:OGC:1.3:CRS84",
        },
        "features": features,
    }
