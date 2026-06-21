# Changelog

All notable changes to Korea Study & Career Decision Agent are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses semantic versioning for portfolio releases.

## [2.2.0] - 2026-06-21

### Added
- Regression tests for Chinese role display mappings (all 18 career roles verified, no English fallbacks).
- Decision report Chinese localization tests covering role labels, city labels, recommendation level labels, and non-IT career role paths.
- Expanded test coverage from 136 to 144 tests.

### Changed
- Bumped version to 2.2.0 to reflect test and localization improvements.

## [2.0.0] - 2026-06-18

### Added
- Repositioned the product as a Korea study and career decision assistant.
- Added Study Cost Calculator with city, school type, housing, lifestyle, cost breakdown charts, export, and persisted history.
- Added Career & Job Market Analyzer with role, experience, Korean level, salary range, skill requirements, visa pathway, competitiveness score, and preparation plan.
- Added AI Decision Report pipeline combining study cost and job market inputs into recommendation, budget gap, risk profile, and 3-month action plan outputs.
- Added News & Policy search with category filtering, relevance scoring, impact summaries, charts, and action suggestions.
- Added V2 Streamlit pages, API client methods, FastAPI routers, Pydantic schemas, and SQLite persistence for the new decision modules.
- Added V2 README positioning, screenshots, data provenance, and decision-use disclaimer.

### Changed
- Promoted V2 decision modules as the main demo flow.
- Reframed V1 comparison, survey, AI perception report, and community insights as supporting legacy modules.
- Updated portfolio messaging around traceable decision support rather than general country perception analytics.

### Documentation
- The original V2 implementation plan remains in `KOREA_ANALYSIS_V2.md` as an implemented planning reference.

## [1.0.0] - 2026-06-11

### Added
- Created Streamlit frontend and FastAPI backend.
- Added SQLite, SQLAlchemy, configuration, and health checks.
- Added six-country and six-category benchmark data.
- Added Comparison Lab with radar and category charts.
- Added persistent perception survey submissions and community summary aggregation.
- Added structured AI perception report endpoint with OpenAI-compatible provider and deterministic local fallback.
- Added shared frontend API client and visual system.
