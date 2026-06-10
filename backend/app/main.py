from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import engine, Base
from backend.app.routers import health, countries

app = FastAPI(
    title="Korea Analysis System",
    description="A bilingual data + AI platform for measuring South Korea's global influence.",
    version="0.1.0",
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
    from backend.app.database import SessionLocal
    from backend.app.models import CountryScore
    db = SessionLocal()
    count = db.query(CountryScore).count()
    if count == 0:
        _seed_data(db)
    db.close()


def _seed_data(db):
    from backend.app.models import CountryScore

    seeds = [
        # GDP per capita (USD)
        CountryScore(country="South Korea", year=2024, category="GDP per capita", score=36238, source="World Bank"),
        CountryScore(country="Japan", year=2024, category="GDP per capita", score=32487, source="World Bank"),
        CountryScore(country="China", year=2024, category="GDP per capita", score=13303, source="World Bank"),
        # Innovation Rank (lower = better)
        CountryScore(country="South Korea", year=2024, category="Innovation Rank", score=6, source="WIPO GII"),
        CountryScore(country="Japan", year=2024, category="Innovation Rank", score=13, source="WIPO GII"),
        CountryScore(country="China", year=2024, category="Innovation Rank", score=11, source="WIPO GII"),
        # Cultural Influence (0-10)
        CountryScore(country="South Korea", year=2024, category="Cultural Influence", score=9, source="KAS estimate"),
        CountryScore(country="Japan", year=2024, category="Cultural Influence", score=8, source="KAS estimate"),
        CountryScore(country="China", year=2024, category="Cultural Influence", score=7, source="KAS estimate"),
        # Global Influence (0-10)
        CountryScore(country="South Korea", year=2024, category="Global Influence", score=8, source="KAS estimate"),
        CountryScore(country="Japan", year=2024, category="Global Influence", score=8, source="KAS estimate"),
        CountryScore(country="China", year=2024, category="Global Influence", score=9, source="KAS estimate"),
    ]
    for s in seeds:
        db.add(s)
    db.commit()


# Include routers
app.include_router(health.router)
app.include_router(countries.router)
