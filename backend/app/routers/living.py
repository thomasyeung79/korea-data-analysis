from fastapi import APIRouter

from ..schemas import MBTICityMatchRequest, MBTICityMatchResult
from ..services.mbti_city_match import match_mbti_city

router = APIRouter(prefix="/api/v1/living", tags=["living"])


@router.post("/mbti-city-match", response_model=MBTICityMatchResult)
def mbti_city_match(request: MBTICityMatchRequest):
    return match_mbti_city(request)
