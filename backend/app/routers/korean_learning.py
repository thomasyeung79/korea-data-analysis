from fastapi import APIRouter

from ..schemas import (
    CareerScenario,
    ExpressionExplanation,
    KoreanHelperRequest,
    LivingScenario,
    StudyScenario,
    TOPIKPlanner,
)
from ..services import korean_learning

router = APIRouter(prefix="/api/v1/korean-learning", tags=["korean learning"])


@router.get("/study", response_model=list[StudyScenario])
def study_scenarios(language: str = "en"):
    return korean_learning.get_study_scenarios("zh" if language == "zh" else "en")


@router.get("/career", response_model=list[CareerScenario])
def career_scenarios(language: str = "en"):
    return korean_learning.get_career_scenarios("zh" if language == "zh" else "en")


@router.get("/living", response_model=list[LivingScenario])
def living_scenarios(language: str = "en"):
    return korean_learning.get_living_scenarios("zh" if language == "zh" else "en")


@router.get("/topik", response_model=list[TOPIKPlanner])
def topik_planners():
    return korean_learning.get_topik_planners()


@router.post("/explain", response_model=ExpressionExplanation)
def explain(request: KoreanHelperRequest):
    return korean_learning.explain_expression(
        expression=request.expression,
        action=request.action,
        context=request.context,
    )
