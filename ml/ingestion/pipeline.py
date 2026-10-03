"""
Master data ingestion pipeline runner for FloodLens AI.
Orchestrates:
1. Geographic zone boundary generation for Hyderabad study area
2. Rainfall data ingestion (IMD / historical meteorology)
3. Elevation & DEM terrain ingestion (SRTM / topography)
4. Drainage and waterway network proximity ingestion (OSM / Musi River / nalas)
5. Land cover proportions ingestion (ESA WorldCover)
6. Historical flood incidents and inundation points matching
7. GeoJSON and Parquet/CSV dataset export into data/raw/ and data/processed/
"""

import os
import json
import logging
from typing import Dict, Any, Optional
import pandas as pd

from ml.ingestion.sources import HYDERABAD_BBOX, PUBLIC_DATA_SOURCES
from ml.ingestion.zones import generate_grid_zones
from ml.ingestion.rainfall import RainfallIngestion
from ml.ingestion.elevation import ElevationIngestion
from ml.ingestion.drainage import DrainageIngestion
from ml.ingestion.land_cover import LandCoverIngestion
from ml.ingestion.historical_floods import HistoricalFloodsIngestion
from ml.ingestion.validation import DataValidator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("FloodLens-Ingestion")


class IngestionPipeline:
    """
    Coordinates end-to-end ingestion across all public data modalities.
    """

    def __init__(
        self,
        output_dir_processed: str = "data/processed",
        output_dir_raw: str = "data/raw",
    ) -> None:
        self.output_dir_processed = output_dir_processed
        self.output_dir_raw = output_dir_raw
        os.makedirs(self.output_dir_processed, exist_ok=True)
        os.makedirs(self.output_dir_raw, exist_ok=True)

        self.rainfall_ingestion = RainfallIngestion()
        self.elevation_ingestion = ElevationIngestion()
        self.drainage_ingestion = DrainageIngestion()
        self.land_cover_ingestion = LandCoverIngestion()
        self.floods_ingestion = HistoricalFloodsIngestion()

    def run(self, grid_rows: int = 10, grid_cols: int = 10, save_files: bool = True) -> Dict[str, Any]:
        """
        Execute full ingestion and feature aggregation.
        """
        logger.info(f"Starting ingestion pipeline for Hyderabad (grid: {grid_rows}x{grid_cols})...")

        # 1. Generate study area zones
        zone_collection = generate_grid_zones(HYDERABAD_BBOX, rows=grid_rows, cols=grid_cols)
        zones = zone_collection["features"]
        logger.info(f"Generated {len(zones)} geographic zones across Hyderabad bounding box.")

        # 2. Ingest Rainfall
        logger.info("Ingesting meteorological rainfall features...")
        zones = self.rainfall_ingestion.ingest_for_zones(zones)

        # 3. Ingest Elevation & Terrain
        logger.info("Ingesting elevation and digital terrain features...")
        zones = self.elevation_ingestion.ingest_for_zones(zones)

        # 4. Ingest Drainage and Waterways
        logger.info("Ingesting drainage network and waterway proximity...")
        zones = self.drainage_ingestion.ingest_for_zones(zones)

        # 5. Ingest Land Cover
        logger.info("Ingesting ESA WorldCover land use proportions...")
        zones = self.land_cover_ingestion.ingest_for_zones(zones)

        # 6. Ingest Historical Flood Incidents
        logger.info("Ingesting historical flood events and documented hotspots...")
        zones = self.floods_ingestion.ingest_for_zones(zones)

        zone_collection["features"] = zones
        zone_collection["metadata"]["data_sources"] = PUBLIC_DATA_SOURCES

        # 7. Validate
        logger.info("Validating aggregated dataset integrity...")
        validation_report = DataValidator.validate_feature_collection(zone_collection)
        if not validation_report["valid"]:
            logger.error(f"Validation failed with {validation_report['invalid_count']} issues: {validation_report['errors']}")
            raise ValueError(f"Dataset validation failed: {validation_report['errors']}")
        logger.info(f"Validation passed: {validation_report['total_features']} zones verified.")

        # 8. Export Data
        if save_files:
            self._save_artifacts(zone_collection)

        return zone_collection

    def _save_artifacts(self, zone_collection: Dict[str, Any]) -> None:
        """
        Save GeoJSON and tabular formats (CSV and Parquet).
        """
        geojson_path = os.path.join(self.output_dir_processed, "hyderabad_zones.geojson")
        with open(geojson_path, "w", encoding="utf-8") as f:
            json.dump(zone_collection, f, indent=2)
        logger.info(f"Saved zone GeoJSON: {geojson_path}")

        # Extract tabular records
        records = [feat["properties"] for feat in zone_collection["features"]]
        df = pd.DataFrame(records)

        csv_path = os.path.join(self.output_dir_processed, "hyderabad_features.csv")
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved tabular features CSV: {csv_path} (Shape: {df.shape})")

        parquet_path = os.path.join(self.output_dir_processed, "hyderabad_features.parquet")
        try:
            df.to_parquet(parquet_path, index=False)
            logger.info(f"Saved tabular features Parquet: {parquet_path}")
        except Exception as e:
            logger.warning(f"Could not save parquet: {e}")

        # Save data sources metadata in raw directory
        manifest_path = os.path.join(self.output_dir_raw, "sources_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(PUBLIC_DATA_SOURCES, f, indent=2)
        logger.info(f"Saved data source manifest: {manifest_path}")


if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()
