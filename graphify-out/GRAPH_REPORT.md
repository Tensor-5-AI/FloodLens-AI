# Graph Report - FloodLens-AI  (2026-10-03)

## Corpus Check
- 54 files · ~17,446 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 425 nodes · 435 edges · 43 communities (22 shown, 21 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e7a7557e`
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

## God Nodes (most connected - your core abstractions)
1. `Definition of Done` - 22 edges
2. `Definition of Done` - 22 edges
3. `compilerOptions` - 16 edges
4. `SpatialDataService` - 9 edges
5. `FloodSusceptibilityANN` - 8 edges
6. `BaselineFloodModel` - 8 edges
7. `Settings` - 7 edges
8. `ScenarioSimulationRequest` - 7 edges
9. `ScenarioSimulationResponse` - 7 edges
10. `ModelInferenceService` - 7 edges

## Surprising Connections (you probably didn't know these)
- `TestGeospatialStub` --uses--> `SpatialDataService`  [INFERRED]
  tests/geospatial/test_geospatial_stub.py → backend/app/services/spatial.py
- `TestMLModels` --uses--> `FloodSusceptibilityANN`  [INFERRED]
  tests/ml/test_models.py → ml/models/ann.py
- `TestMLModels` --uses--> `BaselineFloodModel`  [INFERRED]
  tests/ml/test_models.py → ml/models/baseline.py
- `HealthResponse` --uses--> `Settings`  [INFERRED]
  backend/app/api/v1/routes/health.py → backend/app/config.py
- `Settings` --uses--> `Settings`  [INFERRED]
  backend/app/api/v1/routes/health.py → backend/app/config.py

## Communities (43 total, 21 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (43): code:md (# FloodLens AI — Project State), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+35 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (23): code:md (# FloodLens AI — Agent Workflow), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (22): code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16, code:block17 (+14 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (14): code:md (# FloodLens AI — System Prompt), code:block2, code:block3, code:block4, code:block5, code:block6, Dependencies, Files to Create (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (14): 1. Environment Setup, 2. Backend Setup, 3. Frontend Setup, 4. Running Tests, code:text (FloodLens-AI/), code:bash (cp .env.example .env), code:bash (# Install backend dependencies), code:bash (cd frontend) (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (43): code:md (# FloodLens AI — Project State), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+35 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (16): Any, float, str, Any, str, TestGeospatialStub, ModelInferenceService, Load model weights and metadata once training pipeline has produced artifacts. (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (18): BaseModel, Simulate impact of hypothetical land use or drainage modifications.     Note: De, simulate_scenario(), ScenarioSimulationRequest, ScenarioSimulationResponse, HealthResponse, InterventionParameter, Request payload for hypothetical land-use/construction scenario simulation. (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (23): code:md (# FloodLens AI — Agent Workflow), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.11
Nodes (14): LogisticRegression, float, int, float, int, Test ANN initialization and forward pass using synthetic tensor fixture, TestMLModels, FloodSusceptibilityANN (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (22): code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16, code:block17 (+14 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (21): dependencies, next, react, react-dom, devDependencies, eslint, eslint-config-next, tailwindcss (+13 more)

### Community 14 - "Community 14"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (14): code:md (# FloodLens AI — System Prompt), code:block2, code:block3, code:block4, code:block5, code:block6, Dependencies, Files to Create (+6 more)

### Community 16 - "Community 16"
Cohesion: 0.24
Nodes (11): get_settings(), Application configuration settings loaded from environment variables or .env fil, Settings, create_application(), lifespan(), BaseSettings, FastAPI, HealthResponse (+3 more)

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

## Knowledge Gaps
- **266 isolated node(s):** `float`, `Any`, `eslintConfig`, `nextConfig`, `name` (+261 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Definition of Done` connect `Community 2` to `Community 3`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Why does `Definition of Done` connect `Community 12` to `Community 15`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **What connects `FloodLens AI Backend Root Package.`, `Application configuration settings loaded from environment variables or .env fil`, `FloodLens AI Backend Application Package.` to the rest of the system?**
  _303 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.045454545454545456 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._