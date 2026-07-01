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

### Streamlit Cloud Checklist

* App entry point: `app.py`
* Python dependencies: `requirements.txt`
* Optional secret: `API_BASE_URL`
* Optional secret: `OPENAI_API_KEY`
* No backend process is started by Streamlit Cloud automatically.

For a frontend-only portfolio demo, leave `API_BASE_URL` unset. The API client will use local fallback services where available.

## Render / Railway FastAPI Backend

Deploy the `backend` directory as a Python web service.

Example start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Recommended backend environment variables:

```text
CORS_ORIGINS=https://your-streamlit-app.streamlit.app
OPENAI_API_KEY=
AI_PROVIDER=local
```

After deployment, set the Streamlit frontend secret:

```text
API_BASE_URL=https://your-fastapi-service.example.com
```

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

## Environment Variables

See `.env.example` at the repository root.

| Variable | Required | Description |
|---|---:|---|
| `API_BASE_URL` | No | Frontend URL for a deployed FastAPI backend |
| `OPENAI_API_KEY` | No | Optional OpenAI-compatible provider key |
| `AI_PROVIDER` | No | Defaults to local fallback mode |
| `CORS_ORIGINS` | No | Comma-separated frontend origins for backend CORS |

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
