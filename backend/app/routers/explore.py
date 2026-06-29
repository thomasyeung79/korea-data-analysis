from fastapi import APIRouter

from ..schemas import CultureSection, CityInfo, ExploreOverview, HistoryEvent, LivingCost, QuickFact
from ..services import explore_service

router = APIRouter(prefix="/api/v1/explore", tags=["explore korea"])


@router.get("/overview", response_model=ExploreOverview)
def overview():
    return explore_service.get_overview()


@router.get("/cities", response_model=list[CityInfo])
def cities():
    return explore_service.get_cities()


@router.get("/culture", response_model=list[CultureSection])
def culture():
    return explore_service.get_culture()


@router.get("/history", response_model=list[HistoryEvent])
def history():
    return explore_service.get_history()


@router.get("/living-cost", response_model=list[LivingCost])
def living_cost():
    return explore_service.get_living_cost()


@router.get("/quick-facts", response_model=list[QuickFact])
def quick_facts():
    return explore_service.get_quick_facts()
