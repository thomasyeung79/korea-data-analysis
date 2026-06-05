from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.module_score import ModuleScore
from backend.app.schemas.module_score import ModuleScoreCreate, ModuleScoreResponse

router = APIRouter(prefix="/api/v1/modules", tags=["modules"])


@router.get("", response_model=List[ModuleScoreResponse])
def get_module_scores(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    scores = (
        db.query(ModuleScore)
        .filter(ModuleScore.user_id == current_user.id)
        .all()
    )
    return [
        ModuleScoreResponse(
            id=s.id,
            user_id=s.user_id,
            module_name=s.module_name,
            score=s.score,
            created_at=s.created_at.isoformat() if s.created_at else None,
            updated_at=s.updated_at.isoformat() if s.updated_at else None,
        )
        for s in scores
    ]


@router.post("", response_model=ModuleScoreResponse)
def save_module_score(
    data: ModuleScoreCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = (
        db.query(ModuleScore)
        .filter(
            ModuleScore.user_id == current_user.id,
            ModuleScore.module_name == data.module_name,
        )
        .first()
    )

    if existing:
        existing.score = data.score
        db.commit()
        db.refresh(existing)
        score = existing
    else:
        score = ModuleScore(
            user_id=current_user.id,
            module_name=data.module_name,
            score=data.score,
        )
        db.add(score)
        db.commit()
        db.refresh(score)

    return ModuleScoreResponse(
        id=score.id,
        user_id=score.user_id,
        module_name=score.module_name,
        score=score.score,
        created_at=score.created_at.isoformat() if score.created_at else None,
        updated_at=score.updated_at.isoformat() if score.updated_at else None,
    )


@router.get("/{module_name}", response_model=ModuleScoreResponse)
def get_module_score(
    module_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    score = (
        db.query(ModuleScore)
        .filter(
            ModuleScore.user_id == current_user.id,
            ModuleScore.module_name == module_name,
        )
        .first()
    )
    if not score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module score not found")

    return ModuleScoreResponse(
        id=score.id,
        user_id=score.user_id,
        module_name=score.module_name,
        score=score.score,
        created_at=score.created_at.isoformat() if score.created_at else None,
        updated_at=score.updated_at.isoformat() if score.updated_at else None,
    )
