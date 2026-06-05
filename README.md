# KoreaIntel Pro 🇰🇷

**Korea market and culture intelligence workspace** — 韩国市场与文化智能工作台

A full-stack application that turns Korea-related culture, tourism, technology, sports, and society signals into usable decisions for brands, creators, travel teams, and learners.

## Architecture

```
Streamlit Frontend (refactored pages)
    │  HTTP/JSON + JWT
    ▼
FastAPI Backend (REST API)
    │  SQLAlchemy ORM
    ▼
SQLite Database
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Database | SQLite + SQLAlchemy |
| Auth | JWT (python-jose + bcrypt) |
| AI | OpenAI API (server-side proxy) |
| Data | Pandas (CSV → JSON API) |

## Features

### 📊 Analysis Modules
- **History** — Korea development timeline with impact scores
- **Analysis** — Market signal benchmark (GDP, Innovation Index)
- **Technology** — Tech & industry credibility assessment
- **Culture** — K-pop/K-drama strategy radar
- **Sports** — Multi-sport visibility & football pathway analytics
- **Society** — Perception vs reality check on Korean society
- **Tourism** — Trip builder with AI itinerary generation

### 🔧 Operational Features
- **Travel Order Workflow** — Draft → Paid → Confirmed → Completed
- **AI Chat** — Interactive Korea Q&A assistant
- **User Profile** — Password change, language preferences, activity stats
- **Data Export** — CSV download for analysis results
- **Perception Comparison** — Your scores vs global user averages

### 🔐 Security
- JWT authentication (register/login/logout)
- OpenAI API key stored server-side only (never in frontend)
- User-scoped data isolation
- Password hashing with bcrypt

## Quick Start

### 1. Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env .env.local  # Edit OPENAI_API_KEY and JWT_SECRET_KEY

# Start server
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
# In project root
pip install streamlit pandas requests

# Start Streamlit
streamlit run app.py
```

### 3. Open in browser

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/api/v1/health

## Project Structure

```
south_korea_perception_analysis/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py           # App entry, router includes
│   │   ├── config.py         # Settings from .env
│   │   ├── database.py       # SQLAlchemy engine
│   │   ├── dependencies.py   # JWT auth dependency
│   │   ├── models/           # ORM models (4 tables)
│   │   ├── schemas/          # Pydantic request/response
│   │   ├── routers/          # API endpoints (8 routers)
│   │   └── services/         # Auth, OpenAI, Data services
│   └── scripts/
│       └── migrate_data.py   # JSON → SQLite migration
├── data/                     # CSV data files
├── pages/                    # 12 Streamlit pages
├── app.py                    # Home page with auth
├── api_client.py             # Frontend-backend bridge
└── ui_style.py               # Custom CSS & i18n
```

## API Endpoints

| Router | Endpoints | Auth |
|--------|-----------|------|
| health | GET /api/v1/health | No |
| auth | POST /register, /login, GET /me, PUT /password | Mixed |
| modules | GET/POST /api/v1/modules | Yes |
| perception | GET/POST /api/v1/perception, /averages | Yes |
| travel | GET/POST/PUT/DELETE /api/v1/travel/orders, /analytics | Yes |
| kpop | GET /api/v1/kpop/artists, /metrics, /us-potential, /hit-predictor | No |
| football | GET /api/v1/football/epl, /ucl, /insight | No |
| ai | POST /api/v1/ai/generate, /chat | Yes |

## Data Migration

To import existing data from JSON files:

```bash
python -m backend.scripts.migrate_data
```

## Environment Variables

Create `backend/.env`:

```
DATABASE_URL=sqlite:///./koreaintel.db
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## License

MIT
