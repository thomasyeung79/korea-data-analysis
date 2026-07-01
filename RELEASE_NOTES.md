# Korea Compass Release Notes

## v2.1

Official Data, Deployment, and Portfolio Polish update.

### Changes

* Expanded university Knowledge Base coverage to 10 priority institutions: Seoul National University, Korea University, Yonsei University, KAIST, POSTECH, Hanyang University, Sungkyunkwan University, Kyung Hee University, Ewha Womans University, and Pusan National University.
* Refreshed visa metadata and structured guidance for D-2, D-4, D-10, E-7, F-2, and F-5 using Hi Korea / Korea Immigration Service provenance.
* Updated city metadata for Seoul, Busan, Incheon, Daejeon, Daegu, Gwangju, and Jeju with KOSIS / local-government provenance while keeping cost and recommendation scores marked as planning estimates.
* Added root `.env.example` for Streamlit and backend deployment configuration.
* Made FastAPI CORS origins configurable through `CORS_ORIGINS`.
* Added Screenshot Guide and Video Demo Script for portfolio presentation.
* Updated README, Portfolio Summary, Demo Script, Deployment Guide, and Project Health documentation.

### Data Quality

* Priority university, visa, and city records include `source_name`, `source_url`, `retrieved_at`, `last_updated`, and `verification_status`.
* Mock data count is held at 3 records and did not increase in v2.1.

### Tests

* Added v2.1 official-data quality tests for required universities, visa coverage, source URLs, mock count, and KB status API health.

## v1.0.1

UX, i18n, and integrated planning update.

### Changes

* Improved Simplified Chinese UI coverage across the Home page, Explore Korea, Profile Center, City Recommendation, Korean Learning, AI Korea Life Plan, and Knowledge Base Status.
* Added MBTI City Match inside the Living workflow as a lifestyle preference helper, not a psychological diagnosis tool.
* Added `POST /api/v1/living/mbti-city-match`.
* Upgraded AI Korea Life Plan into a more integrated planning engine that can combine Profile Center, Study Cost, Career Analyzer, City Recommendation, MBTI City Match, TOPIK target, and Knowledge Base confidence metadata.
* Added Data confidence summary to Korea Life Plan output.

### Compatibility

* Existing Korea Life Plan API path remains unchanged.
* Existing profile, study, career, city, Korean Learning, Knowledge Base, and Source Registry flows remain unchanged.
* No database schema changes.

### Tests

* Added MBTI City Match API/service tests.
* Expanded i18n tests for new Chinese labels and option mappings.
* Expanded Korea Life Plan tests for integrated inputs and missing-data handling.

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

## v2.2 ? User Account & Personalization

* Added lightweight JWT account system with register, login, logout, and current user flows.
* Added optional `user_id` binding for profiles, city recommendation history, and AI Korea Life Plan history.
* Preserved demo mode so core planning features continue working without authentication.
* Added standard-library password hashing and JWT signing for deployment-friendly auth.
* Added account deployment variables: `JWT_SECRET_KEY` and `JWT_EXPIRE_MINUTES`.
