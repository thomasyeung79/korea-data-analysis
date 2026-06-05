from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.perception_result import PerceptionResult
from backend.app.schemas.perception_result import PerceptionResultCreate, PerceptionResultResponse

router = APIRouter(prefix="/api/v1/perception", tags=["perception"])


@router.get("", response_model=List[PerceptionResultResponse])
def get_perception_results(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = (
        db.query(PerceptionResult)
        .filter(PerceptionResult.user_id == current_user.id)
        .order_by(PerceptionResult.created_at.desc())
        .all()
    )
    return [
        PerceptionResultResponse(
            id=r.id,
            user_id=r.user_id,
            technology=r.technology,
            culture=r.culture,
            pressure=r.pressure,
            global_influence=r.global_influence,
            overall_score=r.overall_score,
            ai_report=r.ai_report,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in results
    ]


@router.post("", response_model=PerceptionResultResponse)
def save_perception_result(
    data: PerceptionResultCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = PerceptionResult(
        user_id=current_user.id,
        technology=data.technology,
        culture=data.culture,
        pressure=data.pressure,
        global_influence=data.global_influence,
        overall_score=data.overall_score,
        ai_report=data.ai_report,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return PerceptionResultResponse(
        id=result.id,
        user_id=result.user_id,
        technology=result.technology,
        culture=result.culture,
        pressure=result.pressure,
        global_influence=result.global_influence,
        overall_score=result.overall_score,
        ai_report=result.ai_report,
        created_at=result.created_at.isoformat() if result.created_at else None,
    )


@router.get("/latest", response_model=PerceptionResultResponse)
def get_latest_perception(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = (
        db.query(PerceptionResult)
        .filter(PerceptionResult.user_id == current_user.id)
        .order_by(PerceptionResult.created_at.desc())
        .first()
    )
    if not result:
        return PerceptionResultResponse(
            id=0, user_id=current_user.id,
            technology=0, culture=0, pressure=0, global_influence=0,
            overall_score=0, ai_report=None, created_at=None,
        )

    return PerceptionResultResponse(
        id=result.id,
        user_id=result.user_id,
        technology=result.technology,
        culture=result.culture,
        pressure=result.pressure,
        global_influence=result.global_influence,
        overall_score=result.overall_score,
        ai_report=result.ai_report,
        created_at=result.created_at.isoformat() if result.created_at else None,
    )


@router.get("/averages")
def get_perception_averages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get average perception scores across all users, plus the current user's latest."""
    stats = db.query(
        func.avg(PerceptionResult.technology).label("avg_technology"),
        func.avg(PerceptionResult.culture).label("avg_culture"),
        func.avg(PerceptionResult.pressure).label("avg_pressure"),
        func.avg(PerceptionResult.global_influence).label("avg_global_influence"),
        func.avg(PerceptionResult.overall_score).label("avg_overall_score"),
        func.count(PerceptionResult.id).label("total_results"),
        func.count(func.distinct(PerceptionResult.user_id)).label("total_users"),
    ).first()

    latest = (
        db.query(PerceptionResult)
        .filter(PerceptionResult.user_id == current_user.id)
        .order_by(PerceptionResult.created_at.desc())
        .first()
    )

    def _round(v):
        return round(float(v), 2) if v else 0

    return {
        "global_averages": {
            "technology": _round(stats.avg_technology),
            "culture": _round(stats.avg_culture),
            "pressure": _round(stats.avg_pressure),
            "global_influence": _round(stats.avg_global_influence),
            "overall_score": _round(stats.avg_overall_score),
        },
        "total_results": stats.total_results,
        "total_users": stats.total_users,
        "my_latest": {
            "technology": latest.technology if latest else 0,
            "culture": latest.culture if latest else 0,
            "pressure": latest.pressure if latest else 0,
            "global_influence": latest.global_influence if latest else 0,
            "overall_score": latest.overall_score if latest else 0,
        } if latest else None,
    }
