# Korea Compass Release Notes

## v1.0.0

Portfolio-ready release of Korea Compass: a Study, Work, Live, Korean Learning, and AI planning platform for international users considering South Korea.

### Product Positioning

Korea Compass is an AI-supported Korea planning app. It combines country exploration, study planning, career analysis, living guidance, scenario Korean support, and exportable life planning reports in one full-stack product.

### Core Modules

* Explore Korea: country overview, cities, culture, history, living cost, and quick facts.
* Profile Center: reusable Study, Career, and Living profile data.
* Study: study cost calculator with bilingual explanations and exports.
* Work: career and job market analyzer with role-specific skills, city fit, visa pathway, and preparation plans.
* Live: news and policy tracking plus living guide data.
* Korean Learning: scenario-based Korean support for study, career, and living situations.
* City Recommendation: ranking engine for Korea city fit.
* AI Korea Life Plan: exportable planning report with study, career, living, budget, risk, visa, and action plan sections.
* Knowledge Base Status: metadata and source quality dashboard.

### Technical Architecture

* Frontend: Streamlit multi-page app.
* Backend: FastAPI REST API.
* Database: SQLite with SQLAlchemy models for persisted user-facing workflows.
* Data layer: JSON Knowledge Base with shared loader services.
* Visualization: Plotly charts.
* AI layer: OpenAI-compatible provider plus deterministic local fallback.
* Deployment mode: FastAPI backend plus Streamlit frontend, with Streamlit-only local fallback for demos.

### Knowledge Base

Version 1.0 includes a structured JSON Knowledge Base under `backend/data/` for cities, universities, majors, visas, living topics, jobs, culture, and Korean learning content.

Every Knowledge Base JSON file includes metadata for provenance, freshness, language, confidence, licensing, retrieval date, cache expiry, and verification status.

### Source Registry

The Source Registry centralizes official and verified source definitions, including Study in Korea, MOE Korea, KOSIS, Statistics Korea, Seoul Metropolitan Government, TOPIK, Hi Korea, WorkNet Korea, and Korea.net.

### API Overview

Core endpoint groups include:

* `/api/v1/explore/*`
* `/api/v1/profiles`
* `/api/v1/study-cost/calculate`
* `/api/v1/job-market/analyze`
* `/api/v1/city-recommendations`
* `/api/v1/korea-life-plan/generate`
* `/api/v1/korean-learning/*`
* `/api/v1/news-policy/search`
* `/api/v1/kb/status`
* `/api/v1/sources`

### Test Coverage

The v1.0 release has endpoint, service, schema, localization, data loader, Streamlit fallback, Knowledge Base metadata, Source Registry, and business-rule tests.

Latest local verification:

```text
192 passed, 302 warnings
```

### Known Limitations

* Cost, salary, and scoring outputs are directional planning estimates, not official recommendations.
* Some Knowledge Base records are still verified or mock planning data rather than live official API data.
* Streamlit Cloud runs the frontend only; a separate deployed FastAPI backend is required for backend-backed cloud operation.
* The AI layer has a local deterministic fallback and does not require a paid API key.
* This project does not provide legal, immigration, financial, or professional advice.

### Roadmap

* Replace remaining mock records with official or verified sources.
* Add scheduled Knowledge Base refresh workflows.
* Connect selected official APIs where available.
* Improve city-level job, housing, and university data depth.
* Add more production deployment examples.
