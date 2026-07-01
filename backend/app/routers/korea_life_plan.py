import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import KoreaLifePlanHistory, User
from ..schemas import IntegratedKoreaLifePlanRequest, IntegratedKoreaLifePlanResponse, KoreaLifePlanHistoryResponse
from ..services.auth_service import get_optional_current_user
from ..services.korea_life_plan import generate_korea_life_plan

router = APIRouter(prefix="/api/v1/korea-life-plan", tags=["korea life plan"])


@router.post("/generate", response_model=IntegratedKoreaLifePlanResponse)
def generate_plan(
    request: IntegratedKoreaLifePlanRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    language = "zh" if request.language == "zh" else "en"
    display_name = (request.display_name or "Compass User").strip() or "Compass User"
    result = generate_korea_life_plan(
        display_name=display_name,
        study_profile=request.study_profile,
        career_profile=request.career_profile,
        living_profile=request.living_profile,
        language=language,
        city_recommendation=request.city_recommendation,
        mbti_city_match=request.mbti_city_match,
        topik_goal=request.topik_goal,
    )
    history = KoreaLifePlanHistory(
        user_id=current_user.id if current_user else None,
        display_name=display_name,
        overall_recommendation=result["overall_recommendation"],
        best_city=result["best_city"],
        budget_gap=result["budget_gap"],
        plan_json=json.dumps(result, ensure_ascii=False),
    )
    db.add(history)
    db.commit()
    return result


@router.get("/history", response_model=list[KoreaLifePlanHistoryResponse])
def list_history(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    query = db.query(KoreaLifePlanHistory)
    if current_user:
        query = query.filter(KoreaLifePlanHistory.user_id == current_user.id)
    else:
        query = query.filter(KoreaLifePlanHistory.user_id.is_(None))
    records = query.order_by(KoreaLifePlanHistory.created_at.desc()).limit(limit).all()
    return [
        KoreaLifePlanHistoryResponse(
            id=record.id,
            display_name=record.display_name,
            overall_recommendation=record.overall_recommendation,
            best_city=record.best_city,
            budget_gap=record.budget_gap,
            plan_json=record.plan_json,
            created_at=record.created_at.isoformat() if record.created_at else None,
        )
        for record in records
    ]
