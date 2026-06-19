import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import NewsPolicyHistory
from ..schemas import NewsPolicyRequest, NewsPolicyResponse, NewsPolicyHistoryResponse
from ..services.news_policy_config import (
    CATEGORIES,
    TIME_RANGES,
    generate_action_suggestions,
    generate_trend_summary,
    localize_items,
    search_items,
)

router = APIRouter(prefix="/api/v1/news-policy", tags=["news & policy"])


@router.post("/search", response_model=NewsPolicyResponse)
def search_news_policy(
    request: NewsPolicyRequest,
    db: Session = Depends(get_db),
):
    language = "zh" if request.language == "zh" else "en"
    category = request.category if request.category in CATEGORIES or request.category == "All" else "All"
    time_range = request.time_range if request.time_range in TIME_RANGES else "Last 30 days"

    results = search_items(
        keyword=request.keyword,
        category=category,
        time_range=time_range,
    )

    ai_summary = generate_trend_summary(results, request.keyword, language=language)
    action_suggestions = generate_action_suggestions(results, request.keyword, language=language)

    # Serialise for history
    display_results = localize_items(results, language=language)
    results_serialisable = []
    for r in display_results:
        r_copy = dict(r)
        r_copy["relevance_score"] = float(r_copy.get("relevance_score", 0))
        results_serialisable.append(r_copy)

    history = NewsPolicyHistory(
        keyword=request.keyword or None,
        category=category,
        time_range=time_range,
        result_count=len(results),
        ai_summary=ai_summary,
        results_json=json.dumps(results_serialisable, ensure_ascii=False),
    )
    db.add(history)
    db.commit()

    return NewsPolicyResponse(
        results=results_serialisable,
        ai_summary=ai_summary,
        action_suggestions=action_suggestions,
        result_count=len(results),
    )


@router.get("/history", response_model=list[NewsPolicyHistoryResponse])
def list_news_policy_history(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    records = (
        db.query(NewsPolicyHistory)
        .order_by(NewsPolicyHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        NewsPolicyHistoryResponse(
            id=r.id,
            keyword=r.keyword,
            category=r.category,
            time_range=r.time_range,
            result_count=r.result_count,
            ai_summary=r.ai_summary,
            results_json=r.results_json,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in records
    ]
