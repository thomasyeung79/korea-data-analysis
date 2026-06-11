# Korea Analysis Architecture

Korea Analysis uses a small, modular architecture designed for local development, portfolio demonstration, and future deployment.

## System Overview

```mermaid
flowchart TB
    subgraph Frontend
        H["Home"]
        CL["Comparison Lab"]
        PS["Perception Survey"]
        CI["Community Insights"]
        AC["APIClient"]
    end

    subgraph Backend
        API["FastAPI application"]
        CR["Countries router"]
        SR["Surveys router"]
        AR["AI report router"]
        ENG["AIReportEngine"]
    end

    subgraph AI Layer
        OP["OpenAI provider"]
        LP["Local fallback provider"]
    end

    DB[("SQLite")]

    H --> AC
    CL --> AC
    PS --> AC
    CI --> AC
    AC --> API
    API --> CR
    API --> SR
    API --> AR
    CR --> DB
    SR --> DB
    AR --> ENG
    ENG --> OP
    ENG --> LP
```

## Frontend

The frontend is a Streamlit multi-page application:

- `app.py`: onboarding, product positioning, and primary navigation
- `pages/1_Comparison_Lab.py`: regional benchmark exploration
- `pages/2_Perception_Survey.py`: survey, radar comparison, and AI report
- `pages/3_Community_Insights.py`: aggregated community analytics
- `api_client.py`: shared HTTP boundary between Streamlit and FastAPI
- `ui_style.py`: shared product styling

Plotly provides radar, horizontal bar, and profile distribution charts.

## Backend

FastAPI exposes versioned REST endpoints under `/api/v1`.

- `countries.py`: benchmark score retrieval and management
- `surveys.py`: survey submission, statistics, and community summaries
- `ai.py`: structured perception report generation
- `health.py`: service health

Pydantic validates request and response structures. SQLAlchemy manages SQLite persistence.

## Database

SQLite stores:

- Country benchmark scores
- Perception survey submissions

AI reports are generated on demand and are not persisted.

## AI Layer

`AIReportEngine` provides a stable provider boundary.

1. If `OPENAI_API_KEY` exists, it attempts the OpenAI provider using `gpt-4o-mini`.
2. If the key is missing or the provider fails, it returns a deterministic local report.
3. Both providers return the same `AIReportResponse` structure.

This keeps local development free and makes the report endpoint resilient.

## Survey Flow

```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant API as FastAPI
    participant DB as SQLite

    User->>Streamlit: Complete six-dimension survey
    Streamlit->>API: POST /perception-surveys
    API->>DB: Save submission
    DB-->>API: Stored survey
    API-->>Streamlit: Survey response
    Streamlit->>API: GET /perception-surveys/stats
    API->>DB: Aggregate survey data
    API-->>Streamlit: Baseline and community statistics
    Streamlit-->>User: Result metrics and radar chart
```

## AI Report Flow

```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant API as FastAPI
    participant Engine as AIReportEngine
    participant OpenAI
    participant Local as Local Provider

    User->>Streamlit: Generate AI Insight
    Streamlit->>API: POST /ai/perception-report
    API->>Engine: Generate structured report
    alt API key available and provider succeeds
        Engine->>OpenAI: Structured JSON prompt
        OpenAI-->>Engine: AI report JSON
    else Missing key or provider failure
        Engine->>Local: Apply profile and comparison rules
        Local-->>Engine: Local report JSON
    end
    Engine-->>API: AIReportResponse
    API-->>Streamlit: Structured report
    Streamlit-->>User: Professional report cards
```

## Design Constraints

- No authentication or user accounts
- No paid API required for local use
- No report persistence
- Repeated survey submissions are allowed
- Community comments are displayed without account identity

