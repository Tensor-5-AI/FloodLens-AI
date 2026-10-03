# FloodLens AI

**Explainable Urban Flood Susceptibility & Planning Decision-Support Platform**

FloodLens AI leverages publicly accessible geospatial, environmental, terrain, drainage, and historical incident information to assess zone-level urban flood susceptibility. It combines predictive machine learning (baseline Logistic Regression and primary PyTorch Artificial Neural Network) with SHAP explainability, data confidence profiling, spatial error analysis, and 3D geospatial visualization.

---

## Repository Structure

```text
FloodLens-AI/
├── ai_context/              # AI agent operating context & project state tracking
│   ├── project_state.md     # Single source of truth for project development state
│   └── system_prompt.md     # Agent role definition and technical constraints
├── architecture/            # Architectural blueprints and workflows
│   └── agents.md            # Single-agent workflow guidelines (PLAN -> BUILD -> CHECK -> STATE)
├── backend/                 # Python FastAPI backend service
│   ├── app/
│   │   ├── api/v1/          # Versioned REST API endpoints (health, susceptibility, scenario)
│   │   ├── schemas/         # Pydantic data validation schemas
│   │   ├── services/        # Inference and spatial data service layers
│   │   ├── config.py        # Settings and environment configuration
│   │   └── main.py          # FastAPI application entrypoint & middleware
│   └── requirements.txt     # Backend Python dependencies
├── data/                    # Geospatial & environmental data hierarchy
│   ├── raw/                 # Unaltered public source downloads (DEM, rainfall, OSM, land cover)
│   ├── processed/           # CRS-aligned and zone-aggregated datasets (Parquet, GeoJSON, CSV)
│   ├── synthetic/           # Labeled test fixtures for testing and CI
│   └── README.md            # Data guidelines and CRS conventions
├── frontend/                # Next.js + React + TypeScript + Tailwind CSS application
│   ├── src/app/             # Next.js App Router pages and layout
│   └── package.json         # Frontend dependencies and scripts
├── ml/                      # Machine learning and data processing pipelines
│   ├── ingestion/           # Public-data download and extraction routines
│   ├── preprocessing/       # Cleaning, CRS standardization, and geometry validation
│   ├── features/            # Feature engineering modules (terrain, rainfall, drainage, land cover)
│   ├── models/              # Model architectures (Baseline Logistic Regression & PyTorch ANN)
│   ├── training/            # Model training and cross-validation pipelines
│   ├── evaluation/          # Metrics evaluation, spatial error analysis, and validation
│   ├── inference/           # Production inference pipeline
│   ├── explainability/      # SHAP feature importance calculation
│   ├── artifacts/           # Saved model weights and scaler pipelines
│   └── requirements.txt     # ML & geospatial Python dependencies
├── tests/                   # Automated test suite
│   ├── backend/             # API and service unit tests
│   ├── ml/                  # Model instantiation and forward-pass tests
│   └── geospatial/          # Spatial data handling tests
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules for data, models, and node/python artifacts
└── pyproject.toml           # Root Python package definition
```

---

## Quickstart

### Prerequisites

- **Python**: 3.10+ (tested on 3.13)
- **Node.js**: 20+ (tested on v22)
- **npm**: 10+

### 1. Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### 2. Backend Setup

```bash
# Install backend dependencies
pip install -r backend/requirements.txt
pip install -r ml/requirements.txt

# Run the FastAPI development server
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

FastAPI interactive documentation will be available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/v1/health`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The Next.js application will be available at: `http://localhost:3000`.

### 4. Running Tests

```bash
python -m unittest discover -t . -s tests -v
```

---

## Core Product Principles

1. **No Data Fabrication:** Model inputs rely exclusively on publicly verifiable datasets.
2. **Transparent Limitations:** Clearly distinguish estimated susceptibility from physical flood forecasts.
3. **Explainability First:** All predictions are paired with SHAP-based factor contributions and data confidence indicators.