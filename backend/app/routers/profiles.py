from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import UserProfile
from ..schemas import UserProfileCreate, UserProfileResponse
from ..services.profile_service import profile_from_json, profile_to_json

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])


@router.post("", response_model=UserProfileResponse)
def create_profile(request: UserProfileCreate, db: Session = Depends(get_db)):
    profile = UserProfile(
        display_name=(request.display_name or "Compass User").strip() or "Compass User",
        study_profile_json=profile_to_json(request.study_profile),
        career_profile_json=profile_to_json(request.career_profile),
        living_profile_json=profile_to_json(request.living_profile),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return _profile_response(profile)


@router.get("", response_model=list[UserProfileResponse])
def list_profiles(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    records = db.query(UserProfile).order_by(UserProfile.created_at.desc()).limit(limit).all()
    return [_profile_response(record) for record in records]


@router.get("/latest", response_model=Optional[UserProfileResponse])
def latest_profile(db: Session = Depends(get_db)):
    record = db.query(UserProfile).order_by(UserProfile.created_at.desc()).first()
    return _profile_response(record) if record else None


def _profile_response(record: UserProfile) -> dict:
    return {
        "id": record.id,
        "display_name": record.display_name,
        "study_profile": profile_from_json(record.study_profile_json),
        "career_profile": profile_from_json(record.career_profile_json),
        "living_profile": profile_from_json(record.living_profile_json),
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }
