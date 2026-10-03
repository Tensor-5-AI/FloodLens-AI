# Graph Report - FloodLens-AI  (2026-10-03)

## Corpus Check
- 64 files · ~21,792 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 549 nodes · 672 edges · 47 communities (27 shown, 20 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fba20600`
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

## God Nodes (most connected - your core abstractions)
1. `Definition of Done` - 22 edges
2. `Definition of Done` - 22 edges
3. `TestDataIngestionPipeline` - 19 edges
4. `RainfallIngestion` - 18 edges
5. `DrainageIngestion` - 17 edges
6. `ElevationIngestion` - 17 edges
7. `HistoricalFloodsIngestion` - 17 edges
8. `compilerOptions` - 16 edges
9. `LandCoverIngestion` - 15 edges
10. `IngestionPipeline` - 15 edges

## Surprising Connections (you probably didn't know these)
- `TestGeospatialStub` --uses--> `SpatialDataService`  [INFERRED]
  tests/geospatial/test_geospatial_stub.py → backend/app/services/spatial.py
- `TestDataIngestionPipeline` --uses--> `DrainageIngestion`  [INFERRED]
  tests/ml/test_ingestion.py → ml/ingestion/drainage.py
- `TestDataIngestionPipeline` --uses--> `ElevationIngestion`  [INFERRED]
  tests/ml/test_ingestion.py → ml/ingestion/elevation.py
- `TestDataIngestionPipeline` --uses--> `HistoricalFloodsIngestion`  [INFERRED]
  tests/ml/test_ingestion.py → ml/ingestion/historical_floods.py
- `TestDataIngestionPipeline` --uses--> `LandCoverIngestion`  [INFERRED]
  tests/ml/test_ingestion.py → ml/ingestion/land_cover.py

## Communities (47 total, 20 thin omitted)

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
Cohesion: 0.09
Nodes (17): Any, float, str, Any, str, TestGeospatialStub, ModelInferenceService, Load model weights and metadata once training pipeline has produced artifacts. (+9 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (29): get_settings(), Application configuration settings loaded from environment variables or .env fil, Settings, create_application(), lifespan(), BaseModel, BaseSettings, FastAPI (+21 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (23): code:md (# FloodLens AI — Agent Workflow), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.11
Nodes (14): LogisticRegression, float, int, float, int, Test ANN initialization and forward pass using synthetic tensor fixture, TestMLModels, FloodSusceptibilityANN (+6 more)

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
Cohesion: 0.83
Nodes (4): str, get_susceptibility(), Retrieve susceptibility scores and explanations for a study area.     Implementa, SusceptibilityResult

### Community 21 - "Community 21"
Cohesion: 0.50
Nodes (3): FloodLens AI Data Directory, Principles, Structure

### Community 36 - "Community 36"
Cohesion: 0.07
Nodes (38): DrainageIngestion, Drainage and waterways ingestion module. Extracts waterways, rivers (Musi River,, Ingests waterway and drainage network geometries, computing:     1. Distance to, ElevationIngestion, Elevation and terrain feature ingestion module. Fetches SRTM Digital Elevation M, Ingests elevation and computes terrain-derived variables (elevation, slope, rela, HistoricalFloodsIngestion, Historical flood incident records and documented waterlogging hotspots ingestion (+30 more)

### Community 43 - "Community 43"
Cohesion: 0.33
Nodes (5): Count incidents that fall inside or within a 1.5 km buffer of zone boundary., Enrich zones with historical incident observations., Any, float, str

### Community 44 - "Community 44"
Cohesion: 0.33
Nodes (5): Estimate ESA WorldCover proportions based on distance to core dense urban center, Enrich zones with land cover proportions., Any, float, str

### Community 45 - "Community 45"
Cohesion: 0.47
Nodes (4): Validate a single GeoJSON zone feature. Returns list of errors (empty if valid)., Validate an entire GeoJSON FeatureCollection., Any, str

### Community 46 - "Community 46"
Cohesion: 0.50
Nodes (3): Verify that coordinates lie within the specified geographic bounding box., bool, float

## Knowledge Gaps
- **279 isolated node(s):** `float`, `Any`, `eslintConfig`, `nextConfig`, `name` (+274 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RainfallIngestion` connect `Community 36` to `Community 3`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `ElevationIngestion` connect `Community 36` to `Community 15`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `DrainageIngestion` connect `Community 36` to `Community 16`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `TestDataIngestionPipeline` (e.g. with `DrainageIngestion` and `ElevationIngestion`) actually correct?**
  _`TestDataIngestionPipeline` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `RainfallIngestion` (e.g. with `IngestionPipeline` and `Any`) actually correct?**
  _`RainfallIngestion` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `DrainageIngestion` (e.g. with `IngestionPipeline` and `Any`) actually correct?**
  _`DrainageIngestion` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `FloodLens AI Backend Root Package.`, `Application configuration settings loaded from environment variables or .env fil`, `FloodLens AI Backend Application Package.` to the rest of the system?**
  _354 weakly-connected nodes found - possible documentation gaps or missing edges._