# Graph Report - FloodLens-AI  (2026-10-03)

## Corpus Check
- 90 files · ~36,123 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 918 nodes · 1463 edges · 72 communities (56 shown, 16 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 218 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a4f3035d`
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
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]

## God Nodes (most connected - your core abstractions)
1. `ModelInferenceService` - 48 edges
2. `FloodSusceptibilityANN` - 39 edges
3. `SpatialDataService` - 33 edges
4. `SpatialDataService` - 27 edges
5. `FloodPredictor` - 22 edges
6. `Definition of Done` - 22 edges
7. `Definition of Done` - 22 edges
8. `FloodExplainer` - 20 edges
9. `str` - 19 edges
10. `LeakageSafePreprocessor` - 19 edges

## Surprising Connections (you probably didn't know these)
- `TestGeospatialStub` --uses--> `SpatialDataService`  [INFERRED]
  tests/geospatial/test_geospatial_stub.py → backend/app/api/v1/routes/spatial.py
- `TestConfidenceEndpoints` --uses--> `ZoneConfidenceResponse`  [INFERRED]
  tests/backend/test_confidence_endpoint.py → backend/app/schemas/confidence.py
- `TestConfidenceEndpoints` --uses--> `StudyAreaConfidenceSummary`  [INFERRED]
  tests/backend/test_confidence_endpoint.py → backend/app/schemas/confidence.py
- `TestExplanationEndpoints` --uses--> `ZoneExplanationResponse`  [INFERRED]
  tests/backend/test_explanation_endpoint.py → backend/app/schemas/explanation.py
- `TestExplanationEndpoints` --uses--> `GlobalExplanationResponse`  [INFERRED]
  tests/backend/test_explanation_endpoint.py → backend/app/schemas/explanation.py

## Communities (72 total, 16 thin omitted)

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
Nodes (9): Enrich zone dictionaries with rainfall metrics., Fetch historical monsoon season rainfall data for a specific coordinate., Compute key rainfall features from daily series., Documented regional monsoon baseline for Hyderabad (GHMC area, ~800-900mm monsoo, Any, bool, float, int (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (14): 1. Environment Setup, 2. Backend Setup, 3. Frontend Setup, 4. Running Tests, code:text (FloodLens-AI/), code:bash (cp .env.example .env), code:bash (# Install backend dependencies), code:bash (cd frontend) (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (43): code:md (# FloodLens AI — Project State), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+35 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (11): ModelInferenceService, Service responsible for loading trained models (PyTorch ANN / Baseline Logistic, Retrieve global SHAP feature importance rankings across all study area zones., Retrieve global SHAP feature importance rankings across all study area zones., Service responsible for loading trained models (PyTorch ANN / Baseline Logistic, Retrieve global SHAP feature importance rankings across all study area zones., Calculate city-wide aggregated confidence metrics across all study area zones., Calculate city-wide aggregated confidence metrics across all study area zones. (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (23): Integration tests for Spatial Error and Map Layer API endpoints. Tests: - GET /s, BaseModel, ConfidenceDimensionScores, Sub-scores (0-100) across key data quality dimensions., FeatureContribution, GlobalFeatureImportance, Step in the SHAP waterfall progression explaining susceptibility score derivatio, Detailed SHAP factor attribution for a single feature. (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (23): code:md (# FloodLens AI — Agent Workflow), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (25): Model evaluation, spatial validation, ROC-AUC / PR-AUC metrics, and spatial erro, evaluate_binary_predictions(), Evaluation metrics calculation module for FloodLens AI models. Computes Recall,, Calculate comprehensive evaluation metrics for flood susceptibility classificati, Spatial Error Analysis Engine for Urban Flood Susceptibility. Evaluates spatial, LogisticRegression, Any, ndarray (+17 more)

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
Cohesion: 0.18
Nodes (10): ElevationIngestion, Ingests elevation and computes terrain-derived variables (elevation, slope, rela, Batch query Open-Elevation API for list of [{'latitude': lat, 'longitude': lon},, Accurate topographic model for the Hyderabad metropolitan plateau.         Hyder, Enrich zones with elevation and terrain characteristics.         Also calculates, Any, bool, float (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.24
Nodes (8): DrainageIngestion, Ingests waterway and drainage network geometries, computing:     1. Distance to, Calculate great-circle distance between two coordinates in meters., Compute distance to nearest drainage and local drainage proximity score., Enrich zones with drainage and waterway proximity features., Any, float, str

### Community 17 - "Community 17"
Cohesion: 0.40
Nodes (3): geistMono, geistSans, metadata

### Community 19 - "Community 19"
Cohesion: 0.40
Nodes (4): code:bash (npm run dev), Deploy on Vercel, Getting Started, Learn More

### Community 20 - "Community 20"
Cohesion: 0.27
Nodes (9): Generate local SHAP explanations for a single zone.         Returns waterfall co, Calculate global feature importances across all zones in the study area., Precompute global feature importance and all zone explanations for instant API s, LeakageSafePreprocessor, Any, DataFrame, int, Series (+1 more)

### Community 21 - "Community 21"
Cohesion: 0.50
Nodes (3): FloodLens AI Data Directory, Principles, Structure

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (9): DataFrame, float, int, str, Partition dataset into train and test sets using spatial blocking to prevent spa, spatial_block_train_test_split(), Model training pipelines, cross-validation, and optimization routines., PyTorch ANN training pipeline for Urban Flood Susceptibility. Trains the FloodSu (+1 more)

### Community 28 - "Community 28"
Cohesion: 0.17
Nodes (12): str, ConfidenceScorer, Evaluates multi-modal data quality and reliability for urban zones., Switch or reload active model (primary_ann vs baseline)., Load model weights and metadata once training pipeline has produced artifacts., Load model weights and metadata once training pipeline has produced artifacts., Initialize both the predictor and explainability engine., Load model weights and metadata once training pipeline has produced artifacts. (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (5): LeakageSafePreprocessor, Leakage-safe Preprocessing Pipeline. Ensures that all scalers, median imputers,, Stateful preprocessor for tabular flood features.     Guarantees zero leakage be, Persist fitted preprocessor state to disk., Load persisted preprocessor state.

### Community 35 - "Community 35"
Cohesion: 0.19
Nodes (9): LandCoverIngestion, Ingests land cover characteristics for zones:     - built_up_pct: Impervious sur, IngestionPipeline, Master data ingestion pipeline runner for FloodLens AI. Orchestrates: 1. Geograp, Coordinates end-to-end ingestion across all public data modalities., RainfallIngestion, Ingests meteorological rainfall data for coordinate points or study area zones., Unit tests for data ingestion modules across all 5 public data modalities: 1. St (+1 more)

### Community 36 - "Community 36"
Cohesion: 0.20
Nodes (11): Save GeoJSON and tabular formats (CSV and Parquet)., Execute full ingestion and feature aggregation., DataValidator, Validates data structures and geospatial attributes., Verify that coordinates lie within the specified geographic bounding box., Any, bool, int (+3 more)

### Community 38 - "Community 38"
Cohesion: 0.19
Nodes (10): Predict susceptibility for a single zone dictionary., Generate predictions for a pandas DataFrame of zones., Predict susceptibility for a single zone dictionary., Predict susceptibility for a single zone dictionary., Generate predictions for a pandas DataFrame of zones., Generate predictions for a pandas DataFrame of zones., Any, bool (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.12
Nodes (8): Drainage and waterways ingestion module. Extracts waterways, rivers (Musi River,, Elevation and terrain feature ingestion module. Fetches SRTM Digital Elevation M, Historical flood incident records and documented waterlogging hotspots ingestion, Data ingestion module for public datasets (IMD rainfall, SRTM DEM, OSM waterways, Land cover and land use ingestion module. Models proportions of built-up/impervi, Rainfall data ingestion module. Fetches daily precipitation metrics for study ar, Data definitions, bounding boxes, schemas, and public source endpoints for Flood, Data validation module. Validates incoming geospatial records and feature frames

### Community 43 - "Community 43"
Cohesion: 0.27
Nodes (7): HistoricalFloodsIngestion, Ingests and matches verified historical flood incident observations to zones., Count incidents that fall inside or within a 1.5 km buffer of zone boundary., Enrich zones with historical incident observations., Any, float, str

### Community 44 - "Community 44"
Cohesion: 0.33
Nodes (5): Estimate ESA WorldCover proportions based on distance to core dense urban center, Enrich zones with land cover proportions., Any, float, str

### Community 45 - "Community 45"
Cohesion: 0.17
Nodes (10): DataFrame, int, Series, str, Data cleaning, CRS normalization, geometry repair, and zone aggregation modules., Spatially-aware train/test splitting module. Prevents spatial autocorrelation le, define_flood_target(), Target variable definition for urban flood susceptibility classification. Formul (+2 more)

### Community 46 - "Community 46"
Cohesion: 0.47
Nodes (4): Validate a single GeoJSON zone feature. Returns list of errors (empty if valid)., Validate an entire GeoJSON FeatureCollection., Any, str

### Community 48 - "Community 48"
Cohesion: 0.33
Nodes (6): DataFrame, ndarray, ndarray, Fit imputer and scaler using training split ONLY., Transform features using previously fitted statistics., Fit on training dataframe and return transformed array.

### Community 49 - "Community 49"
Cohesion: 0.12
Nodes (14): determine_risk_confidence_quadrant(), get_confidence_tier(), Confidence and Data Quality Profiling Engine for Urban Flood Susceptibility. Eva, Classify 0-100 confidence score into standardized quality tiers., Aggregate confidence metrics across all zones in the study area., Categorize zone into the 2x2 Risk vs Confidence Matrix.     Returns (quadrant_co, Evaluate full confidence profile for a single zone record., Confidence and Data Quality evaluation package for FloodLens AI. (+6 more)

### Community 50 - "Community 50"
Cohesion: 0.24
Nodes (6): FeatureBuilder, Feature engineering definitions and matrix builder for FloodLens AI. Extracts, t, Constructs and engineers predictive tabular feature matrices from zone records., Feature engineering pipeline for rainfall, terrain, drainage, and land-use facto, str, str

### Community 51 - "Community 51"
Cohesion: 0.20
Nodes (7): generate_grid_zones(), Grid-based and administrative zone generator for Hyderabad study area. Divides t, Generate regular geographic grid cells across the bounding box.     Returns GeoJ, Any, float, int, str

### Community 52 - "Community 52"
Cohesion: 0.24
Nodes (24): Any, ModelInferenceService, SpatialDataService, str, GlobalExplanationResponse, explain_custom_features(), get_confidence_summary(), get_global_explanation() (+16 more)

### Community 53 - "Community 53"
Cohesion: 0.24
Nodes (11): get_settings(), Application configuration settings loaded from environment variables or .env fil, Settings, create_application(), lifespan(), BaseSettings, FastAPI, HealthResponse (+3 more)

### Community 54 - "Community 54"
Cohesion: 0.12
Nodes (8): Integration tests for SHAP explanation API endpoints. Tests: - GET /zones/{zone_, Verify GET /zones/{zone_id}/explanation returns 200 and matches ZoneExplanationR, Verify GET /api/v1/zones/{zone_id}/explanation works identically., Verify 404 is returned when requesting explanation for a nonexistent zone., Verify GET /zones/explanations/global returns ranked feature importances., Verify POST /zones/explain computes explanation on arbitrary feature dictionary., Verify GET /api/v1/susceptibility includes top SHAP explanations., TestExplanationEndpoints

### Community 55 - "Community 55"
Cohesion: 0.12
Nodes (15): float, int, Unit tests for Primary Model: PyTorch Artificial Neural Network training, compar, TestANNTrainingAndInference, Any, float, int, str (+7 more)

### Community 56 - "Community 56"
Cohesion: 0.50
Nodes (3): FloodPredictor, Inference service for predicting flood susceptibility on raw zone records or Dat, Load model and preprocessor if paths exist. Supports both PyTorch (.pt) and Scik

### Community 57 - "Community 57"
Cohesion: 0.19
Nodes (8): Any, str, Retrieve zone polygons in standardized GeoJSON format (EPSG:4326 for web maps)., List available spatial feature layers (rainfall, elevation, drainage, land cover, List available spatial feature layers (rainfall, elevation, drainage, land cover, Retrieve DataFrame containing tabular features for all zones in the study area., Retrieve raw feature dictionary for a specific zone ID., Retrieve GeoJSON layer representing spatial prediction errors with styled proper

### Community 58 - "Community 58"
Cohesion: 0.18
Nodes (11): TestGeospatialStub, get_inference_service(), get_spatial_service(), SHAP explanation feature contribution structure., Zone-level flood susceptibility result skeleton., Query parameters for retrieving susceptibility data.     The exact geographic un, SusceptibilityFeatureContribution, SusceptibilityQuery (+3 more)

### Community 59 - "Community 59"
Cohesion: 0.18
Nodes (3): Unit tests for Model Explainability Engine (ml/explainability/explainer.py). Ver, Verify SHAP additive property: base_value + sum(shap_values) == predicted_probab, TestFloodExplainer

### Community 60 - "Community 60"
Cohesion: 0.33
Nodes (4): format_raw_feature_value(), Model Explainability Engine for Urban Flood Susceptibility. Implements SHAP (SHa, Helper to format numeric values with appropriate units., SHAP (SHapley Additive exPlanations) calculation routines for model transparency

### Community 62 - "Community 62"
Cohesion: 0.29
Nodes (5): Model inference routines and pipeline integration., get_risk_category(), Inference helper for scoring zone flood susceptibility. Loads trained model and, Standard risk categorizations based on 0-100 susceptibility score., float

### Community 63 - "Community 63"
Cohesion: 0.40
Nodes (4): Derive interaction terms and domain-specific flood susceptibility indices., Produce a clean DataFrame restricted to the designated numeric feature set., Produce a clean DataFrame restricted to the designated numeric feature set., DataFrame

### Community 64 - "Community 64"
Cohesion: 0.17
Nodes (19): Any, ModelInferenceService, SpatialDataService, str, ModelInferenceService, SpatialDataService, str, TestSpatialEndpoints (+11 more)

### Community 65 - "Community 65"
Cohesion: 0.11
Nodes (12): Merge spatial error evaluations with zone polygon boundaries from GeoJSON., Save spatial error JSON report and styled GeoJSON map to artifacts., Computes spatial residuals, confusion categories, quadrant clustering,     and p, Compute full spatial error metrics across all zones., SpatialErrorAnalyzer, Any, DataFrame, float (+4 more)

### Community 66 - "Community 66"
Cohesion: 0.16
Nodes (10): Any, Retrieve zone features and generate susceptibility prediction., Retrieve zone features and generate susceptibility prediction., Retrieve zone features and generate susceptibility prediction., Produce local SHAP explanation for a specific zone.         Uses cached explanat, Produce local SHAP explanation for a specific zone.         Uses cached explanat, Evaluate full multi-modal data confidence profile for a given zone.         Cros, Evaluate full multi-modal data confidence profile for a given zone.         Cros (+2 more)

### Community 67 - "Community 67"
Cohesion: 0.31
Nodes (8): Simulate impact of hypothetical land use or drainage modifications.     Note: De, simulate_scenario(), ScenarioSimulationRequest, ScenarioSimulationResponse, Request payload for hypothetical land-use/construction scenario simulation., Response containing delta impact on flood susceptibility., ScenarioSimulationRequest, ScenarioSimulationResponse

### Community 68 - "Community 68"
Cohesion: 0.22
Nodes (8): float, Generate susceptibility prediction score (0-100) for a given feature vector., Generate susceptibility prediction score for a given feature vector., Generate susceptibility prediction score (0-100) for a given feature vector., Generate susceptibility prediction score (0-100) for a given feature vector., Generate susceptibility prediction score (0-100) for a given feature vector., Generate susceptibility prediction score (0-100) for a given feature vector., Generate susceptibility prediction score (0-100) for a given feature vector.

### Community 69 - "Community 69"
Cohesion: 0.28
Nodes (5): FloodExplainer, SHAP Explainability Engine for PyTorch ANN and Baseline models.     Produces loc, Load artifacts and initialize SHAP KernelExplainer with k-means background summa, Construct probability prediction callable for SHAP KernelExplainer., bool

### Community 70 - "Community 70"
Cohesion: 0.25
Nodes (7): Generate on-the-fly local SHAP explanation for a raw feature dictionary., Generate on-the-fly local SHAP explanation for a raw feature dictionary., Generate on-the-fly local SHAP explanation for a raw feature dictionary., Generate SHAP explanation feature contributions., Generate feature contribution explanation., Generate feature contribution explanation., Generate feature contribution explanation.

### Community 71 - "Community 71"
Cohesion: 0.50
Nodes (3): Load precomputed SHAP explanations if present on disk., Load precomputed SHAP explanations if present on disk., Load precomputed SHAP explanations if present on disk.

## Knowledge Gaps
- **294 isolated node(s):** `eslintConfig`, `nextConfig`, `name`, `version`, `private` (+289 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ModelInferenceService` connect `Community 8` to `Community 64`, `Community 65`, `Community 66`, `Community 68`, `Community 69`, `Community 70`, `Community 71`, `Community 52`, `Community 56`, `Community 58`, `Community 28`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `FloodExplainer` connect `Community 69` to `Community 66`, `Community 68`, `Community 8`, `Community 60`, `Community 20`, `Community 55`, `Community 59`, `Community 28`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `FloodPredictor` connect `Community 56` to `Community 66`, `Community 68`, `Community 38`, `Community 8`, `Community 11`, `Community 55`, `Community 28`, `Community 62`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `ModelInferenceService` (e.g. with `Any` and `ModelInferenceService`) actually correct?**
  _`ModelInferenceService` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `FloodSusceptibilityANN` (e.g. with `FloodExplainer` and `FloodPredictor`) actually correct?**
  _`FloodSusceptibilityANN` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `SpatialDataService` (e.g. with `ModelInferenceService` and `SpatialDataService`) actually correct?**
  _`SpatialDataService` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `SpatialDataService` (e.g. with `Any` and `ModelInferenceService`) actually correct?**
  _`SpatialDataService` has 24 INFERRED edges - model-reasoned connections that need verification._