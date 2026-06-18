from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import ai, health, countries, surveys, study_cost, job_market, decision_report, news_policy

app = FastAPI(
    title="Korea Analysis System",
    description="A practical decision assistant for students and job seekers considering Korea.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    # Seed data if empty
    from .database import SessionLocal
    from .models import CountryScore
    db = SessionLocal()
    count = db.query(CountryScore).count()
    if count == 0:
        _seed_data(db)
    db.close()


def _seed_data(db):
    from .models import CountryScore

    # 6 countries × 6 categories = 36 scores, all on 0-10 scale
    countries = ["Korea", "Japan", "China", "Singapore", "Vietnam", "Thailand"]
    categories = ["Economy", "Technology", "Education", "Culture", "Global Influence", "Quality of Life"]

    # Score grid [country][category] — directional estimates
    grid = {
        "Korea":     [8, 9, 8, 9, 8, 7],
        "Japan":     [8, 8, 9, 8, 8, 7],
        "China":     [9, 8, 7, 7, 9, 6],
        "Singapore": [9, 9, 9, 7, 7, 9],
        "Vietnam":   [5, 5, 6, 6, 4, 6],
        "Thailand":  [5, 5, 5, 7, 4, 7],
    }

    seeds = []
    for ci, country in enumerate(countries):
        for cj, cat in enumerate(categories):
            seeds.append(CountryScore(
                country=country, year=2024, category=cat,
                score=grid[country][cj],
                source="KAS estimate (directional)",
            ))
    for s in seeds:
        db.add(s)
    db.commit()


# Include routers
app.include_router(health.router)
app.include_router(countries.router)
app.include_router(surveys.router)
app.include_router(ai.router)
app.include_router(study_cost.router)
app.include_router(job_market.router)
app.include_router(decision_report.router)
app.include_router(news_policy.router)
