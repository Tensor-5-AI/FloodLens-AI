"""Data ingestion module for public datasets (IMD rainfall, SRTM DEM, OSM waterways, ESA WorldCover, historical incidents)."""

from ml.ingestion.sources import HYDERABAD_BBOX, HYDERABAD_CENTROID, PUBLIC_DATA_SOURCES
from ml.ingestion.zones import generate_grid_zones
from ml.ingestion.rainfall import RainfallIngestion
from ml.ingestion.elevation import ElevationIngestion
from ml.ingestion.drainage import DrainageIngestion
from ml.ingestion.land_cover import LandCoverIngestion
from ml.ingestion.historical_floods import HistoricalFloodsIngestion
from ml.ingestion.validation import DataValidator
from ml.ingestion.pipeline import IngestionPipeline

__all__ = [
    "HYDERABAD_BBOX",
    "HYDERABAD_CENTROID",
    "PUBLIC_DATA_SOURCES",
    "generate_grid_zones",
    "RainfallIngestion",
    "ElevationIngestion",
    "DrainageIngestion",
    "LandCoverIngestion",
    "HistoricalFloodsIngestion",
    "DataValidator",
    "IngestionPipeline",
]
