# East Asia Perception Lab 🌏

> **v0.2 — Comparison Engine**

A quantitative benchmarking platform that scores six East Asian economies across six dimensions — all normalised to a 0–10 scale for fair comparison.

**Countries:** Korea · Japan · China · Singapore · Vietnam · Thailand  
**Dimensions:** Economy · Technology · Education · Culture · Global Influence · Quality of Life

---

## Architecture

```
Streamlit Frontend     FastAPI Backend      SQLite
  (Comparison Lab)  →  (REST API)       →  (country_scores)
```

---

## Quick start

```bash
# Backend (terminal 1)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (terminal 2)
pip install -r requirements.txt
streamlit run app.py
```

| What | URL |
|------|-----|
| Frontend | http://localhost:8501 |
| API docs | http://localhost:8000/docs |

---

## Pages

| Page | Description |
|------|-------------|
| Home | Dynamic KPIs, country cards, navigation |
| Comparison Lab | Plotly radar chart, bar chart, data table |

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/countries` | GET | List scores (?country, ?year, ?category) |
| `/api/v1/countries/{country}` | GET | Scores for one country |
| `/api/v1/countries` | POST | Create a score |
| `/api/v1/countries` | PUT | Update a score |
| `/api/v1/countries/categories/list` | GET | Distinct categories |
| `/api/v1/countries/countries/list` | GET | Distinct countries |

---

## Project structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI + seed data
│   │   ├── config.py / database.py / models.py / schemas.py
│   │   └── routers/
│   │       ├── health.py
│   │       └── countries.py
│   └── requirements.txt
├── pages/
│   └── 1_Comparison_Lab.py       # Radar + bar charts
├── app.py                        # Home page
├── api_client.py                 # Frontend↔Backend
├── ui_style.py                   # CSS
└── requirements.txt
```
