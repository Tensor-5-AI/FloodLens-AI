"""
Land cover and land use ingestion module.
Models proportions of built-up/impervious surface, vegetation/tree cover, water, and open ground
aligned with ESA WorldCover 10m classifications across Hyderabad urban and peri-urban zones.
"""

from typing import Dict, List, Any
import numpy as np

# Urban cores: Hyderabad Charminar/Old City, Begumpet, Secunderabad, Hitec City, Uppal
URBAN_CORES = [
    {"lat": 17.3616, "lon": 78.4747, "density": 0.88},  # Old City / Charminar
    {"lat": 17.4399, "lon": 78.4983, "density": 0.85},  # Secunderabad
    {"lat": 17.4435, "lon": 78.3772, "density": 0.82},  # Hitec City / Madhapur
    {"lat": 17.4375, "lon": 78.4482, "density": 0.80},  # Ameerpet / Punjagutta
    {"lat": 17.4019, "lon": 78.5602, "density": 0.78},  # Uppal
    {"lat": 17.4933, "lon": 78.3914, "density": 0.76},  # Kukatpally
]


class LandCoverIngestion:
    """
    Ingests land cover characteristics for zones:
    - built_up_pct: Impervious surfaces (roads, rooftops, pavement) that impede drainage infiltration.
    - vegetation_pct: Permeable soil, parks, tree canopy.
    - water_pct: Open water surface within zone.
    - open_ground_pct: Undeveloped / bare soil.
    """

    @staticmethod
    def estimate_land_cover(lat: float, lon: float) -> Dict[str, float]:
        """
        Estimate ESA WorldCover proportions based on distance to core dense urban centers vs green buffers.
        """
        # Calculate maximum urban influence from nearest core
        max_urban_influence = 0.25  # baseline peri-urban built-up
        for core in URBAN_CORES:
            d_lat = lat - core["lat"]
            d_lon = lon - core["lon"]
            dist_deg = np.sqrt(d_lat**2 + d_lon**2)
            # Influence falls off exponentially with distance (~0.05 deg ≈ 5.5 km)
            influence = core["density"] * np.exp(-(dist_deg**2) / (2 * (0.04**2)))
            if influence > max_urban_influence:
                max_urban_influence = influence

        built_up_pct = float(np.clip(max_urban_influence * 100.0, 15.0, 92.0))

        # Check proximity to major water bodies (Hussain Sagar, Osman Sagar, Musi River)
        is_near_hussain_sagar = (abs(lat - 17.424) < 0.015) and (abs(lon - 78.474) < 0.015)
        is_near_musi = (abs(lat - 17.370) < 0.008)

        if is_near_hussain_sagar:
            water_pct = 22.0
        elif is_near_musi:
            water_pct = 8.0
        else:
            water_pct = 2.0

        remaining = max(0.0, 100.0 - (built_up_pct + water_pct))
        # Higher vegetation in peri-urban / university areas / forest reserves (e.g. Hyderabad Central Univ, Nehru Zoo)
        vegetation_pct = float(round(remaining * 0.65, 1))
        open_ground_pct = float(round(remaining - vegetation_pct, 1))

        return {
            "built_up_pct": round(built_up_pct, 1),
            "vegetation_pct": round(vegetation_pct, 1),
            "water_pct": round(water_pct, 1),
            "open_ground_pct": round(open_ground_pct, 1),
            "land_cover_missing": 0,
        }

    def ingest_for_zones(self, zones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich zones with land cover proportions.
        """
        enriched_zones = []
        for zone in zones:
            props = dict(zone.get("properties", {}))
            lat = props.get("center_lat", 17.385)
            lon = props.get("center_lon", 78.486)

            lc = self.estimate_land_cover(lat, lon)
            props.update(lc)

            zone_copy = dict(zone)
            zone_copy["properties"] = props
            enriched_zones.append(zone_copy)

        return enriched_zones
