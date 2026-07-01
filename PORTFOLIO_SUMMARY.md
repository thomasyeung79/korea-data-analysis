# Korea Compass Portfolio Summary

## Problem

International students and job seekers often research Korea across disconnected sources: study costs, universities, jobs, visas, city choice, Korean language needs, living logistics, and policy updates. The decision is multi-factor, but most tools only answer one slice of the problem.

## Solution

Korea Compass brings Study, Work, Live, Korean Learning, and AI planning into one full-stack product. Users can explore Korea, build a reusable profile, compare city fit, estimate costs, analyze career readiness, learn practical Korean for real situations, and generate an exportable Korea Life Plan.

## Features

* Explore Korea country and city information.
* Profile Center for reusable Study, Career, and Living data.
* Study Cost Calculator with charts and exports.
* Career & Job Market Analyzer with role-specific skills and preparation plans.
* City Recommendation scoring engine.
* MBTI City Match for lifestyle-based Korean city fit.
* Scenario-based Korean Learning Support.
* Integrated AI Korea Life Plan with profile, study, career, city, MBTI, language, budget, visa, risk, and data confidence signals.
* Knowledge Base Status dashboard.
* Source Registry for official data integration readiness.
* English and Simplified Chinese UI support.

## Tech Stack

* Streamlit
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* Plotly
* Pytest
* OpenAI-compatible SDK with local fallback

## Architecture

```text
Streamlit Frontend
  -> API Client
  -> FastAPI Backend
  -> Services
  -> SQLite + JSON Knowledge Base
```

The frontend can run against a FastAPI backend or use local fallback behavior for Streamlit-only demos.

## Backend

The backend exposes REST endpoints for health checks, study cost, job market analysis, profiles, city recommendations, Korea Life Plan generation, Explore Korea, Korean Learning, Knowledge Base status, and Source Registry status.

## Frontend

The Streamlit app is organized as a product workflow: Explore Korea, Profile Center, Study, Work, Live, Korean Learning, City Recommendation, AI Korea Life Plan, and Knowledge Base Status. Plotly visualizations are used for ranking, cost breakdowns, and quality dashboards.

## AI

The AI layer is designed with provider fallback. It can use an OpenAI-compatible provider when configured, while local deterministic templates keep the app usable without paid APIs.

The AI Korea Life Plan has been upgraded from a standalone report into an integrated planning engine. It combines available inputs from Profile Center, Study Cost, Career Analyzer, City Recommendation, MBTI City Match, TOPIK target, and Knowledge Base confidence metadata. When an input is missing, the report states that it is based on available inputs instead of pretending the dataset is complete.

## Data Layer

The Knowledge Base stores structured JSON data by domain. V1.0 adds metadata, source coverage, licensing fields, retrieval timestamps, cache expiry, verification status, and a centralized Source Registry.

V2.1 upgrades the data layer for portfolio readiness by expanding official / verified university, visa, and city records. It keeps uncertain costs and scores labeled as planning estimates instead of presenting them as official facts.

## Testing

The test suite covers API endpoints, service logic, schema validation, localization helpers, Streamlit fallback mode, Knowledge Base metadata, Source Registry behavior, and business-rule outputs.

## What I Learned

* How to evolve a prototype into a multi-module product without breaking earlier workflows.
* How to design a lightweight Knowledge Base that can later migrate to official APIs or a database.
* How to keep Streamlit demos usable while still maintaining a FastAPI backend.
* How to test product logic, localization, and data quality in one Python project.

## Future Improvements

* Connect official APIs for selected domains.
* Add scheduled Knowledge Base refresh and validation jobs.
* Improve source citations inside individual result cards.
* Add richer deployment examples for Streamlit Cloud plus external FastAPI hosting.
* Replace remaining mock records with official or verified sources.
* Add scheduled source refresh checks and data-quality reports.
