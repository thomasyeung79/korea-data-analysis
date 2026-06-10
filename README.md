# Korea Analysis System 🇰🇷

> **v0.1 — Day 1: Minimum vertical slice**

A bilingual data + AI platform that measures South Korea's global influence across economy, innovation, culture, and more — benchmarked against regional peers.

---

## Architecture

```
Streamlit Frontend
    │  HTTP/JSON
    ▼
FastAPI Backend
    │  SQLAlchemy ORM
    ▼
SQLite Database (country_scores)
```

---

## Quick start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
# In project root
pip install -r requirements.txt
streamlit run app.py
```

### 3. Open

| What | URL |
|------|-----|
| Frontend | http://localhost:8501 |
| API docs | http://localhost:8000/docs |

---

## What's inside (Day 1)

### Backend (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/countries` | GET | List scores (filterable by ?country, ?year, ?category) |
| `/api/v1/countries` | POST | Create a score |
| `/api/v1/countries` | PUT | Update a score |
| `/api/v1/countries/{country}` | GET | Scores for one country |
| `/api/v1/countries/categories/list` | GET | All distinct categories |
| `/api/v1/countries/countries/list` | GET | All distinct countries |

### Database (one table)

**`country_scores`** — `country`, `year`, `category`, `score`, `source`

Pre-seeded with East Asia comparison data (South Korea / Japan / China) across:
- GDP per capita
- Innovation Rank
- Cultural Influence
- Global Influence

### Frontend (Streamlit, 2 pages)

1. **Home** — Overview with live API stats
2. **Data Explorer** — Filter, visualise, and add/update scores

---

## Project structure

```
south_korea_perception_analysis/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entry + seed data
│   │   ├── config.py           # Settings
│   │   ├── database.py         # SQLAlchemy engine
│   │   ├── models.py           # CountryScore model
│   │   ├── schemas.py          # Pydantic request/response
│   │   └── routers/
│   │       ├── health.py       # GET /health
│   │       └── countries.py    # CRUD /countries
│   └── requirements.txt
├── pages/
│   ├── 1_Data_Explorer.py      # Explore + edit scores
├── app.py                      # Home page
├── api_client.py               # Frontend↔Backend bridge
├── ui_style.py                 # CSS
└── requirements.txt
```

---

## Coming in V0.2

- Perception survey + AI report generation
- Historical timeline module
- User history (saved reports)
- i18n (中文/English)
- Comparison charts
