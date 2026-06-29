from fastapi import APIRouter

from ..schemas import CultureSection, CityInfo, ExploreOverview, HistoryEvent, LivingCost, QuickFact
from ..services import explore_service

router = APIRouter(prefix="/api/v1/explore", tags=["explore korea"])


@router.get("/overview", response_model=ExploreOverview)
def overview(language: str = "en"):
    return explore_service.get_overview("zh" if language == "zh" else "en")


@router.get("/cities", response_model=list[CityInfo])
def cities(language: str = "en"):
    return explore_service.get_cities("zh" if language == "zh" else "en")


@router.get("/culture", response_model=list[CultureSection])
def culture(language: str = "en"):
    return explore_service.get_culture("zh" if language == "zh" else "en")


@router.get("/history", response_model=list[HistoryEvent])
def history(language: str = "en"):
    return explore_service.get_history("zh" if language == "zh" else "en")


@router.get("/living-cost", response_model=list[LivingCost])
def living_cost():
    return explore_service.get_living_cost()


@router.get("/quick-facts", response_model=list[QuickFact])
def quick_facts(language: str = "en"):
    return explore_service.get_quick_facts("zh" if language == "zh" else "en")
