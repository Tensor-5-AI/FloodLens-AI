# FloodLens AI Data Directory

This directory stores public geospatial datasets, intermediate processed features, and synthetic test fixtures.

## Structure

- `raw/`: Raw, unaltered public data downloads (e.g., IMD rainfall, SRTM DEM rasters, OSM waterways, ESA WorldCover). Raw data is excluded from git version control.
- `processed/`: Validated, CRS-normalized, and zone-aggregated datasets stored as Parquet, GeoJSON, or CSV. Excluded from git version control.
- `synthetic/`: Explicitly labeled synthetic test fixtures used solely for pipeline infrastructure verification and unit testing.

## Principles

1. **No Data Fabrication:** Real model analysis must strictly use publicly accessible, verifiable data.
2. **Standardized CRS:** All geospatial inputs are transformed to EPSG:4326 (WGS84) for web mapping or appropriate UTM projections for distance/area metric computations.
3. **Reproducibility:** All processing steps from `raw/` to `processed/` are fully scripted via the ML preprocessing pipeline.
