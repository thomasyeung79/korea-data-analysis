from fastapi import APIRouter

from ..schemas import CityRecommendationRequest, CityRecommendationResponse
from ..services.city_recommendation import recommend_cities

router = APIRouter(prefix="/api/v1/city-recommendations", tags=["city recommendations"])


@router.post("", response_model=CityRecommendationResponse)
def generate_city_recommendations(request: CityRecommendationRequest):
    language = "zh" if request.language == "zh" else "en"
    return recommend_cities(
        request.study_profile,
        request.career_profile,
        request.living_profile,
        language=language,
    )
