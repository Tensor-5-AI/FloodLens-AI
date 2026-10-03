# Graph Report - FloodLens-AI  (2026-10-03)

## Corpus Check
- 80 files · ~31,357 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 784 nodes · 1164 edges · 52 communities (38 shown, 14 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 134 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e57c1b2c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]

## God Nodes (most connected - your core abstractions)
1. `FloodSusceptibilityANN` - 39 edges
2. `ModelInferenceService` - 31 edges
3. `SpatialDataService` - 29 edges
4. `FloodPredictor` - 22 edges
5. `Definition of Done` - 22 edges
6. `Definition of Done` - 22 edges
7. `FloodExplainer` - 20 edges
8. `LeakageSafePreprocessor` - 19 edges
9. `TestDataIngestionPipeline` - 19 edges
10. `RainfallIngestion` - 18 edges

## Surprising Connections (you probably didn't know these)
- `ModelInferenceService` --uses--> `FloodExplainer`  [INFERRED]
  backend/app/services/inference.py → ml/explainability/explainer.py
- `ModelInferenceService` --uses--> `FloodPredictor`  [INFERRED]
  backend/app/services/inference.py → ml/inference/predictor.py
- `str` --uses--> `FloodExplainer`  [INFERRED]
  backend/app/services/inference.py → ml/explainability/explainer.py
- `str` --uses--> `FloodPredictor`  [INFERRED]
  backend/app/services/inference.py → ml/inference/predictor.py
- `Any` --uses--> `FloodExplainer`  [INFERRED]
  backend/app/services/inference.py → ml/explainability/explainer.py

## Communities (52 total, 14 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (43): code:md (# FloodLens AI — Project State), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+35 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (23): code:md (# FloodLens AI — Agent Workflow), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (36): code:md (# FloodLens AI — System Prompt), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.23
Nodes (11): RainfallIngestion, Enrich zone dictionaries with rainfall metrics., Ingests meteorological rainfall data for coordinate points or study area zones., Fetch historical monsoon season rainfall data for a specific coordinate., Compute key rainfall features from daily series., Documented regional monsoon baseline for Hyderabad (GHMC area, ~800-900mm monsoo, Any, bool (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (14): 1. Environment Setup, 2. Backend Setup, 3. Frontend Setup, 4. Running Tests, code:text (FloodLens-AI/), code:bash (cp .env.example .env), code:bash (# Install backend dependencies), code:bash (cd frontend) (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (43): code:md (# FloodLens AI — Project State), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+35 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (48): ModelInferenceService, SpatialDataService, str, Any, ModelInferenceService, SpatialDataService, str, Any (+40 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (35): get_settings(), Application configuration settings loaded from environment variables or .env fil, Settings, create_application(), lifespan(), BaseModel, BaseSettings, FastAPI (+27 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (23): code:md (# FloodLens AI — Agent Workflow), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.11
Nodes (13): LogisticRegression, float, int, Test ANN initialization and forward pass using synthetic tensor fixture, TestMLModels, Any, float, str (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.05
Nodes (36): code:md (# FloodLens AI — System Prompt), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+28 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (21): dependencies, next, react, react-dom, devDependencies, eslint, eslint-config-next, tailwindcss (+13 more)

### Community 14 - "Community 14"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.20
Nodes (8): Batch query Open-Elevation API for list of [{'latitude': lat, 'longitude': lon},, Accurate topographic model for the Hyderabad metropolitan plateau.         Hyder, Enrich zones with elevation and terrain characteristics.         Also calculates, Any, bool, float, int, str

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (6): Calculate great-circle distance between two coordinates in meters., Compute distance to nearest drainage and local drainage proximity score., Enrich zones with drainage and waterway proximity features., Any, float, str

### Community 17 - "Community 17"
Cohesion: 0.40
Nodes (3): geistMono, geistSans, metadata

### Community 19 - "Community 19"
Cohesion: 0.40
Nodes (4): code:bash (npm run dev), Deploy on Vercel, Getting Started, Learn More

### Community 20 - "Community 20"
Cohesion: 0.06
Nodes (36): FloodExplainer, format_raw_feature_value(), Model Explainability Engine for Urban Flood Susceptibility. Implements SHAP (SHa, Helper to format numeric values with appropriate units., SHAP Explainability Engine for PyTorch ANN and Baseline models.     Produces loc, Load artifacts and initialize SHAP KernelExplainer with k-means background summa, Construct probability prediction callable for SHAP KernelExplainer., Generate local SHAP explanations for a single zone.         Returns waterfall co (+28 more)

### Community 21 - "Community 21"
Cohesion: 0.50
Nodes (3): FloodLens AI Data Directory, Principles, Structure

### Community 27 - "Community 27"
Cohesion: 0.25
Nodes (4): Data cleaning, CRS normalization, geometry repair, and zone aggregation modules., Leakage-safe Preprocessing Pipeline. Ensures that all scalers, median imputers,, Spatially-aware train/test splitting module. Prevents spatial autocorrelation le, Target variable definition for urban flood susceptibility classification. Formul

### Community 28 - "Community 28"
Cohesion: 0.08
Nodes (22): Any, float, str, Retrieve zone features and generate susceptibility prediction., Generate on-the-fly local SHAP explanation for a raw feature dictionary., Produce local SHAP explanation for a specific zone.         Uses cached explanat, Retrieve global SHAP feature importance rankings across all study area zones., Load model weights and metadata once training pipeline has produced artifacts. (+14 more)

### Community 29 - "Community 29"
Cohesion: 0.32
Nodes (5): str, LeakageSafePreprocessor, Stateful preprocessor for tabular flood features.     Guarantees zero leakage be, Persist fitted preprocessor state to disk., Load persisted preprocessor state.

### Community 35 - "Community 35"
Cohesion: 0.22
Nodes (6): DrainageIngestion, Ingests waterway and drainage network geometries, computing:     1. Distance to, IngestionPipeline, Coordinates end-to-end ingestion across all public data modalities., Unit tests for data ingestion modules across all 5 public data modalities: 1. St, TestDataIngestionPipeline

### Community 36 - "Community 36"
Cohesion: 0.23
Nodes (10): HistoricalFloodsIngestion, Ingests and matches verified historical flood incident observations to zones., LandCoverIngestion, Ingests land cover characteristics for zones:     - built_up_pct: Impervious sur, Save GeoJSON and tabular formats (CSV and Parquet)., Execute full ingestion and feature aggregation., Any, bool (+2 more)

### Community 38 - "Community 38"
Cohesion: 0.07
Nodes (29): Model evaluation, spatial validation, ROC-AUC / PR-AUC metrics, and spatial erro, evaluate_binary_predictions(), Evaluation metrics calculation module for FloodLens AI models. Computes Recall,, Calculate comprehensive evaluation metrics for flood susceptibility classificati, Model inference routines and pipeline integration., FloodPredictor, get_risk_category(), Inference helper for scoring zone flood susceptibility. Loads trained model and (+21 more)

### Community 39 - "Community 39"
Cohesion: 0.17
Nodes (6): Drainage and waterways ingestion module. Extracts waterways, rivers (Musi River,, Historical flood incident records and documented waterlogging hotspots ingestion, Data ingestion module for public datasets (IMD rainfall, SRTM DEM, OSM waterways, Land cover and land use ingestion module. Models proportions of built-up/impervi, Rainfall data ingestion module. Fetches daily precipitation metrics for study ar, Data definitions, bounding boxes, schemas, and public source endpoints for Flood

### Community 43 - "Community 43"
Cohesion: 0.33
Nodes (5): Count incidents that fall inside or within a 1.5 km buffer of zone boundary., Enrich zones with historical incident observations., Any, float, str

### Community 44 - "Community 44"
Cohesion: 0.33
Nodes (5): Estimate ESA WorldCover proportions based on distance to core dense urban center, Enrich zones with land cover proportions., Any, float, str

### Community 45 - "Community 45"
Cohesion: 0.17
Nodes (10): DataFrame, int, Series, str, define_flood_target(), Extracts and validates the binary flood susceptibility target.     Label 1 = Zon, Series, Model training pipelines, cross-validation, and optimization routines. (+2 more)

### Community 46 - "Community 46"
Cohesion: 0.18
Nodes (10): DataValidator, Data validation module. Validates incoming geospatial records and feature frames, Validates data structures and geospatial attributes., Verify that coordinates lie within the specified geographic bounding box., Validate a single GeoJSON zone feature. Returns list of errors (empty if valid)., Validate an entire GeoJSON FeatureCollection., Any, bool (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.16
Nodes (8): DataFrame, float, int, str, Unit tests for data preprocessing and feature engineering: - Target variable def, TestPreprocessingAndFeatures, Partition dataset into train and test sets using spatial blocking to prevent spa, spatial_block_train_test_split()

### Community 48 - "Community 48"
Cohesion: 0.33
Nodes (6): DataFrame, ndarray, ndarray, Fit imputer and scaler using training split ONLY., Transform features using previously fitted statistics., Fit on training dataframe and return transformed array.

### Community 50 - "Community 50"
Cohesion: 0.16
Nodes (9): FeatureBuilder, Feature engineering definitions and matrix builder for FloodLens AI. Extracts, t, Constructs and engineers predictive tabular feature matrices from zone records., Derive interaction terms and domain-specific flood susceptibility indices., Produce a clean DataFrame restricted to the designated numeric feature set., Produce a clean DataFrame restricted to the designated numeric feature set., Feature engineering pipeline for rainfall, terrain, drainage, and land-use facto, DataFrame (+1 more)

### Community 51 - "Community 51"
Cohesion: 0.20
Nodes (7): generate_grid_zones(), Grid-based and administrative zone generator for Hyderabad study area. Divides t, Generate regular geographic grid cells across the bounding box.     Returns GeoJ, Any, float, int, str

### Community 52 - "Community 52"
Cohesion: 0.29
Nodes (4): ElevationIngestion, Elevation and terrain feature ingestion module. Fetches SRTM Digital Elevation M, Ingests elevation and computes terrain-derived variables (elevation, slope, rela, Master data ingestion pipeline runner for FloodLens AI. Orchestrates: 1. Geograp

## Knowledge Gaps
- **290 isolated node(s):** `eslintConfig`, `nextConfig`, `name`, `version`, `private` (+285 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ModelInferenceService` connect `Community 8` to `Community 9`, `Community 20`, `Community 28`, `Community 38`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `FloodPredictor` connect `Community 38` to `Community 8`, `Community 28`, `Community 20`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `FloodSusceptibilityANN` connect `Community 20` to `Community 11`, `Community 45`, `Community 38`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `FloodSusceptibilityANN` (e.g. with `FloodExplainer` and `FloodPredictor`) actually correct?**
  _`FloodSusceptibilityANN` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ModelInferenceService` (e.g. with `ModelInferenceService` and `SpatialDataService`) actually correct?**
  _`ModelInferenceService` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `SpatialDataService` (e.g. with `ModelInferenceService` and `SpatialDataService`) actually correct?**
  _`SpatialDataService` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `FloodPredictor` (e.g. with `Any` and `float`) actually correct?**
  _`FloodPredictor` has 7 INFERRED edges - model-reasoned connections that need verification._