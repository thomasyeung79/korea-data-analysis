from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CountryScore
from ..schemas import CountryScoreCreate, CountryScoreResponse

router = APIRouter(prefix="/api/v1/countries", tags=["countries"])


@router.get("", response_model=List[CountryScoreResponse])
def list_country_scores(
    country: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(CountryScore)
    if country:
        query = query.filter(CountryScore.country == country)
    if year:
        query = query.filter(CountryScore.year == year)
    if category:
        query = query.filter(CountryScore.category == category)
    results = query.order_by(CountryScore.country, CountryScore.year, CountryScore.category).all()

    return [
        CountryScoreResponse(
            id=r.id,
            country=r.country,
            year=r.year,
            category=r.category,
            score=r.score,
            source=r.source,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in results
    ]


@router.get("/{country}", response_model=List[CountryScoreResponse])
def get_country_scores(
    country: str,
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(CountryScore).filter(CountryScore.country == country)
    if year:
        query = query.filter(CountryScore.year == year)
    results = query.all()

    return [
        CountryScoreResponse(
            id=r.id,
            country=r.country,
            year=r.year,
            category=r.category,
            score=r.score,
            source=r.source,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in results
    ]


@router.post("", response_model=CountryScoreResponse)
def create_country_score(
    data: CountryScoreCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(CountryScore)
        .filter(
            CountryScore.country == data.country,
            CountryScore.year == data.year,
            CountryScore.category == data.category,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Score already exists for {data.country}/{data.year}/{data.category}. Use PUT to update.",
        )

    score = CountryScore(
        country=data.country,
        year=data.year,
        category=data.category,
        score=data.score,
        source=data.source,
    )
    db.add(score)
    db.commit()
    db.refresh(score)

    return CountryScoreResponse(
        id=score.id,
        country=score.country,
        year=score.year,
        category=score.category,
        score=score.score,
        source=score.source,
        created_at=score.created_at.isoformat() if score.created_at else None,
    )


@router.put("", response_model=CountryScoreResponse)
def update_country_score(
    data: CountryScoreCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(CountryScore)
        .filter(
            CountryScore.country == data.country,
            CountryScore.year == data.year,
            CountryScore.category == data.category,
        )
        .first()
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Score not found. Use POST to create.")

    existing.score = data.score
    if data.source is not None:
        existing.source = data.source
    db.commit()
    db.refresh(existing)

    return CountryScoreResponse(
        id=existing.id,
        country=existing.country,
        year=existing.year,
        category=existing.category,
        score=existing.score,
        source=existing.source,
        created_at=existing.created_at.isoformat() if existing.created_at else None,
    )


@router.get("/categories/list", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    results = db.query(CountryScore.category).distinct().all()
    return sorted([r[0] for r in results])


@router.get("/countries/list", response_model=List[str])
def list_countries(db: Session = Depends(get_db)):
    results = db.query(CountryScore.country).distinct().all()
    return sorted([r[0] for r in results])
