from typing import Any, Dict, List, Optional
import os
import logging

logger = logging.getLogger(__name__)


class SpatialDataService:
    """
    Service responsible for handling geospatial queries across study area zones.
    Supports GeoJSON, Parquet, and CSV without requiring heavy database infrastructure
    during the initial prototype phase.
    """

    def __init__(self, data_dir: str = "./data/processed") -> None:
        self.data_dir = data_dir

    def get_zone_geojson(self, study_area: str = "Hyderabad") -> Dict[str, Any]:
        """
        Retrieve zone polygons in standardized GeoJSON format (EPSG:4326 for web maps).
        Loads generated hyderabad_zones.geojson from data/processed if present.
        """
        geojson_path = os.path.join(self.data_dir, f"{study_area.lower()}_zones.geojson")
        if os.path.exists(geojson_path):
            try:
                import json
                with open(geojson_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to read zone GeoJSON from {geojson_path}: {e}")

        return {
            "type": "FeatureCollection",
            "features": [],
            "metadata": {
                "study_area": study_area,
                "status": "pending_data_ingestion",
            },
        }

    def list_available_layers(self) -> List[str]:
        """
        List available spatial feature layers (rainfall, elevation, drainage, land cover).
        """
        layers = []
        if os.path.exists(self.data_dir):
            layers = [f for f in os.listdir(self.data_dir) if f.endswith((".geojson", ".parquet", ".csv"))]
        return layers

    def get_all_zone_features(self, study_area: str = "Hyderabad"):
        """
        Retrieve DataFrame containing tabular features for all zones in the study area.
        """
        import pandas as pd

        csv_path = os.path.join(self.data_dir, f"{study_area.lower()}_features.csv")
        parquet_path = os.path.join(self.data_dir, f"{study_area.lower()}_features.parquet")

        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        elif os.path.exists(parquet_path):
            return pd.read_parquet(parquet_path)
        return pd.DataFrame()

    def get_zone_features(self, zone_id: str, study_area: str = "Hyderabad") -> Optional[Dict[str, Any]]:
        """
        Retrieve raw feature dictionary for a specific zone ID.
        """
        df = self.get_all_zone_features(study_area=study_area)
        if df.empty or "zone_id" not in df.columns:
            return None

        match = df[df["zone_id"].astype(str).str.upper() == str(zone_id).upper()]
        if match.empty:
            return None
        return match.iloc[0].to_dict()

