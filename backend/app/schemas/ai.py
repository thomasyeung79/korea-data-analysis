from pydantic import BaseModel
from typing import Optional, Any


class AIGenerateRequest(BaseModel):
    prompt_type: str  # "kpop_us_analysis", "football_pathway", "travel_itinerary", "perception_report"
    params: dict[str, Any]


class AIGenerateResponse(BaseModel):
    result: str
