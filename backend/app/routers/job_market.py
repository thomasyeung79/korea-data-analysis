import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import JobMarketHistory
from ..schemas import JobMarketRequest, JobMarketResponse, JobMarketHistoryResponse
from ..services.job_market_config import (
    EXPERIENCE_LEVELS,
    KOREAN_LEVELS,
    ROLES,
    analyze_job_market,
    generate_preparation_plan,
)

router = APIRouter(prefix="/api/v1/job-market", tags=["job market"])


@router.post("/analyze", response_model=JobMarketResponse)
def analyze_job_market_endpoint(
    request: JobMarketRequest,
    db: Session = Depends(get_db),
):
    role = request.role if request.role in ROLES else "Backend Developer"
    exp = request.experience_level if request.experience_level in EXPERIENCE_LEVELS else "0-2 years"
    kl = request.korean_level if request.korean_level in KOREAN_LEVELS else "None"

    result = analyze_job_market(role, exp, kl)
    plan = generate_preparation_plan(role, exp, kl)

    history = JobMarketHistory(
        role=role,
        experience_level=exp,
        korean_level=kl,
        salary_min=result["salary_min"],
        salary_max=result["salary_max"],
        competitiveness=result["competitiveness"],
        recommended_skills_json=json.dumps({
            "must_have": result["required_skills"],
            "nice_to_have": result["nice_to_have_skills"],
        }, ensure_ascii=False),
        ai_plan=plan,
    )
    db.add(history)
    db.commit()

    return JobMarketResponse(
        salary_min=result["salary_min"],
        salary_max=result["salary_max"],
        recommended_cities=result["recommended_cities"],
        required_skills=result["required_skills"],
        nice_to_have_skills=result["nice_to_have_skills"],
        korean_language_requirement=result["korean_language_requirement"],
        korean_language_gap=result["korean_language_gap"],
        competitiveness=result["competitiveness"],
        competitiveness_label=result["competitiveness_label"],
        visa_pathway=result["visa_pathway"],
        ai_plan=plan,
        currency=result["currency"],
    )


@router.get("/history", response_model=list[JobMarketHistoryResponse])
def list_job_market_history(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    records = (
        db.query(JobMarketHistory)
        .order_by(JobMarketHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        JobMarketHistoryResponse(
            id=r.id,
            role=r.role,
            experience_level=r.experience_level,
            korean_level=r.korean_level,
            salary_min=r.salary_min,
            salary_max=r.salary_max,
            competitiveness=r.competitiveness,
            recommended_skills_json=r.recommended_skills_json,
            ai_plan=r.ai_plan,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in records
    ]
