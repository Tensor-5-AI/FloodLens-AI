"""
Drainage and waterways ingestion module.
Extracts waterways, rivers (Musi River, Ese River), major lakes/cheruvus (Hussain Sagar, Osman Sagar, Himayat Sagar),
and stormwater nalas across Hyderabad. Computes distance to nearest drainage and drainage density.
"""

from typing import Dict, List, Any, Tuple
import math
import logging
import requests

logger = logging.getLogger(__name__)

# Key landmark waterbodies and river segments in Hyderabad
# Format: {"name": str, "lat": float, "lon": float, "type": "river" | "lake" | "nala"}
HYDERABAD_WATERWAYS: List[Dict[str, Any]] = [
    # Musi River transect points (flows west to east through center of Hyderabad)
    {"name": "Musi River West", "lat": 17.368, "lon": 78.330, "type": "river"},
    {"name": "Musi River Attapur", "lat": 17.369, "lon": 78.432, "type": "river"},
    {"name": "Musi River City Center (Nayapul/High Court)", "lat": 17.367, "lon": 78.474, "type": "river"},
    {"name": "Musi River Amberpet/Chaderghat", "lat": 17.382, "lon": 78.508, "type": "river"},
    {"name": "Musi River Nagole/Uppal", "lat": 17.385, "lon": 78.567, "type": "river"},
    # Major Lakes / Cheruvus
    {"name": "Hussain Sagar", "lat": 17.424, "lon": 78.474, "type": "lake"},
    {"name": "Osman Sagar (Gandipet)", "lat": 17.380, "lon": 78.300, "type": "lake"},
    {"name": "Himayat Sagar", "lat": 17.323, "lon": 78.358, "type": "lake"},
    {"name": "Durgam Cheruvu (Secret Lake)", "lat": 17.433, "lon": 78.384, "type": "lake"},
    {"name": "Kapra Lake", "lat": 17.495, "lon": 78.563, "type": "lake"},
    {"name": "Fox Sagar Lake (Jeedimetla)", "lat": 17.530, "lon": 78.468, "type": "lake"},
    {"name": "Saroornagar Lake", "lat": 17.355, "lon": 78.530, "type": "lake"},
    {"name": "Mir Alam Tank", "lat": 17.348, "lon": 78.448, "type": "lake"},
    # Major Stormwater Nalas / Tributaries
    {"name": "Picket Nala (Secunderabad to Hussain Sagar)", "lat": 17.445, "lon": 78.490, "type": "nala"},
    {"name": "Balkapur Nala", "lat": 17.408, "lon": 78.445, "type": "nala"},
    {"name": "Murki Nala", "lat": 17.375, "lon": 78.485, "type": "nala"},
    {"name": "Kukatpally Nala", "lat": 17.470, "lon": 78.435, "type": "nala"},
]


class DrainageIngestion:
    """
    Ingests waterway and drainage network geometries, computing:
    1. Distance to nearest drainage / river / lake (in meters)
    2. Drainage density index (waterway proximity score)
    """

    def __init__(self, waterways_data: List[Dict[str, Any]] = HYDERABAD_WATERWAYS) -> None:
        self.waterways = waterways_data

    @staticmethod
    def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate great-circle distance between two coordinates in meters.
        """
        R = 6371000.0  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2.0) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return R * c

    def compute_drainage_metrics(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Compute distance to nearest drainage and local drainage proximity score.
        """
        min_dist_m = float("inf")
        nearest_feature = "unknown"
        feature_type = "waterway"
        count_within_3km = 0

        for feature in self.waterways:
            dist = self.haversine_distance_m(lat, lon, feature["lat"], feature["lon"])
            if dist < min_dist_m:
                min_dist_m = dist
                nearest_feature = feature["name"]
                feature_type = feature["type"]
            if dist <= 3000.0:
                count_within_3km += 1

        # Drainage density metric: features within 3km normalized, inverse distance weighting
        density_index = round(min(1.0, (count_within_3km / 5.0) + (1000.0 / max(500.0, min_dist_m)) * 0.2), 3)

        return {
            "dist_to_drainage_m": round(min_dist_m, 1),
            "nearest_drainage_name": nearest_feature,
            "nearest_drainage_type": feature_type,
            "drainage_density_index": density_index,
            "drainage_missing": 0,
        }

    def ingest_for_zones(self, zones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich zones with drainage and waterway proximity features.
        """
        enriched_zones = []
        for zone in zones:
            props = dict(zone.get("properties", {}))
            lat = props.get("center_lat", 17.385)
            lon = props.get("center_lon", 78.486)

            metrics = self.compute_drainage_metrics(lat, lon)
            props.update(metrics)

            zone_copy = dict(zone)
            zone_copy["properties"] = props
            enriched_zones.append(zone_copy)

        return enriched_zones
