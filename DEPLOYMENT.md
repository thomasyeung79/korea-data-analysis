# Korea Compass Deployment Guide

## Local Development

Korea Compass has two runtime pieces:

* FastAPI backend
* Streamlit frontend

Install dependencies from the project root:

```bash
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

## Backend

Start the backend from the `backend` directory:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Health check:

```text
http://localhost:8000/api/v1/health
```

API docs:

```text
http://localhost:8000/docs
```

## Frontend

Start Streamlit from the project root:

```bash
streamlit run app.py
```

By default, the frontend uses local fallback behavior when `API_BASE_URL` is not configured.

## Streamlit Cloud Mode

Streamlit Cloud runs the frontend only. It does not automatically run the FastAPI backend.

Two deployment options are supported:

1. Streamlit-only demo mode: leave `API_BASE_URL` unset and use local fallback behavior.
2. Full-stack mode: deploy FastAPI separately and set `API_BASE_URL` in Streamlit Secrets.

## API_BASE_URL

Use this variable when a backend is deployed:

```text
API_BASE_URL=https://your-fastapi-backend.example.com
```

For local backend mode:

```text
API_BASE_URL=http://localhost:8000
```

## OpenAI Optional

The app does not require a paid API key. If configured, the AI report layer can use an OpenAI-compatible provider:

```text
OPENAI_API_KEY=your_key_here
```

If the key is missing or the provider fails, Korea Compass uses local deterministic fallback logic.

## Troubleshooting

### Backend API is not available

For local full-stack mode, start the backend first:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Then restart Streamlit:

```bash
streamlit run app.py
```

### Streamlit Cloud cannot connect to localhost

`localhost:8000` points to the Streamlit Cloud container, not your local computer. Deploy FastAPI separately and set `API_BASE_URL`, or use Streamlit-only fallback mode.

### Import errors on Streamlit Cloud

Run from the repository root and make sure package directories such as `backend/` and `locales/` include `__init__.py` files where needed.

### Data looks directional

The current Knowledge Base includes official, verified, and limited mock planning records. Use Knowledge Base Status to inspect source coverage and confidence levels.
