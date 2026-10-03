"""
Data definitions, bounding boxes, schemas, and public source endpoints for FloodLens AI.
"""

from dataclasses import dataclass
from typing import Dict, Tuple, Any

# Primary study area: Greater Hyderabad Municipal Corporation (GHMC) / Hyderabad Metropolitan Area
# Bounding box in WGS84 (EPSG:4326): [min_lon, min_lat, max_lon, max_lat]
HYDERABAD_BBOX: Tuple[float, float, float, float] = (78.20, 17.20, 78.65, 17.60)

# Study area centroid [latitude, longitude]
HYDERABAD_CENTROID: Tuple[float, float] = (17.3850, 78.4867)

# Public endpoints and references
PUBLIC_DATA_SOURCES: Dict[str, Dict[str, Any]] = {
    "rainfall": {
        "provider": "Open-Meteo Historical Weather API (ERA5/IMD-calibrated ensemble)",
        "endpoint": "https://archive-api.open-meteo.com/v1/archive",
        "description": "Daily total precipitation (mm) and multi-day cumulative extremes for Hyderabad region",
        "doc_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    "elevation": {
        "provider": "Open-Elevation API / USGS SRTM 30m dataset",
        "endpoint": "https://api.open-elevation.com/api/v1/lookup",
        "description": "SRTM Digital Elevation Model (DEM) 30m sampled points across Hyderabad zones",
        "doc_url": "https://open-elevation.com/",
    },
    "drainage": {
        "provider": "OpenStreetMap via Overpass API",
        "endpoints": [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
        ],
        "description": "Natural waterways, rivers (Musi River), canals, drains (nalas), and water bodies",
        "doc_url": "https://wiki.openstreetmap.org/wiki/Overpass_API",
    },
    "land_cover": {
        "provider": "ESA WorldCover 10m / Global Land Cover",
        "description": "Proportions of built-up/urban, tree cover/vegetation, water, and bare ground",
        "doc_url": "https://esa-worldcover.org/",
    },
    "flood_incidents": {
        "provider": "Verifiable Public Records / Municipal Monsoon Flood Logs (GHMC / Telangana Open Data)",
        "description": "Historical inundation points and waterlogging hotspots documented during major flood events (e.g. 2020 Hyderabad deluge)",
        "doc_url": "https://data.telangana.gov.in/",
    }
}
