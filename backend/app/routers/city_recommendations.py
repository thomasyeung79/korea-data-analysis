import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CityRecommendationHistory, User
from ..schemas import CityRecommendationRequest, CityRecommendationResponse
from ..services.auth_service import get_optional_current_user
from ..services.city_recommendation import recommend_cities

router = APIRouter(prefix="/api/v1/city-recommendations", tags=["city recommendations"])


@router.post("", response_model=CityRecommendationResponse)
def generate_city_recommendations(
    request: CityRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    language = "zh" if request.language == "zh" else "en"
    result = recommend_cities(
        request.study_profile,
        request.career_profile,
        request.living_profile,
        language=language,
    )
    if current_user:
        db.add(
            CityRecommendationHistory(
                user_id=current_user.id,
                best_city=result["best_city"],
                result_json=json.dumps(result, ensure_ascii=False),
            )
        )
        db.commit()
    return result
