from pydantic import BaseModel
from typing import Optional


class PerceptionResultCreate(BaseModel):
    technology: float
    culture: float
    pressure: float
    global_influence: float
    overall_score: float
    ai_report: Optional[str] = None


class PerceptionResultResponse(BaseModel):
    id: int
    user_id: int
    technology: float
    culture: float
    pressure: float
    global_influence: float
    overall_score: float
    ai_report: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
