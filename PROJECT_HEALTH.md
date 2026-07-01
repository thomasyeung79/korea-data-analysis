# Korea Compass Project Health

## v2.1 Status

Korea Compass v2.1 is deployment-ready for a portfolio demo. It supports Streamlit-only fallback mode and full-stack mode with a separately deployed FastAPI backend.

## Data Quality

Priority universities, visas, and cities now include official or verified provenance metadata. Remaining mock records are intentionally limited and visible through Knowledge Base Status.

## Deployment Readiness

* Root `.env.example` is available.
* `API_BASE_URL` supports Streamlit Cloud full-stack configuration.
* `OPENAI_API_KEY` is optional.
* `CORS_ORIGINS` is configurable for hosted FastAPI deployments.
* Local fallback keeps Streamlit demos usable without a backend.

## Current Status

Korea Compass v1.0 is portfolio-ready. The product includes Explore Korea, Study, Work, Live, Korean Learning, AI Korea Life Plan, Knowledge Base, Source Registry, and Official Data Integration Foundation capabilities.

## Tests

Latest local verification:

```text
192 passed, 302 warnings
```

The warnings are primarily framework deprecation warnings from Pydantic, FastAPI startup events, and SQLAlchemy datetime defaults. They do not currently block the v1.0 release.

## Warnings

* Pydantic class-based `Config` deprecation warnings should be migrated to `ConfigDict` later.
* FastAPI `on_event` startup handling should eventually move to lifespan handlers.
* SQLAlchemy datetime defaults should eventually use timezone-aware UTC timestamps.

## Known Limitations

* Cost, salary, city, and risk scoring values are directional planning estimates.
* Some Knowledge Base records are still mock or verified planning data rather than live official API records.
* Streamlit Cloud requires either fallback mode or a separately deployed FastAPI backend.
* The AI provider is optional; local fallback output is deterministic and template-based.

## Data Quality

The Knowledge Base includes metadata for source name, source URL, update date, language, version, confidence, license, retrieval date, cache expiry, and verification status.

Current V8 quality snapshot:

* Knowledge Base JSON files: 45
* Valid files: 45
* Source Registry entries: 9
* Official source coverage: 17.8%
* Source statuses: Official, Verified, Community, Mock

## Security Notes

* No authentication or user accounts are included.
* No secrets are required for the local fallback demo.
* `OPENAI_API_KEY` is optional and should be configured through environment variables or deployment secrets.
* The app does not provide legal, immigration, financial, or professional advice.

## Deployment Readiness

Ready for:

* GitHub portfolio review
* Local full-stack demo
* Streamlit-only demo mode
* Streamlit Cloud frontend deployment with fallback behavior
* Full-stack cloud deployment when an external FastAPI host is configured

Recommended before production:

* Deploy backend to a stable host.
* Configure `API_BASE_URL` in Streamlit Secrets.
* Replace mock Knowledge Base records with official or verified records.
* Add scheduled data refresh and validation workflows.
