from pydantic import BaseModel
from typing import Optional


class CountryScoreCreate(BaseModel):
    country: str
    year: int
    category: str
    score: float
    source: Optional[str] = None


class CountryScoreResponse(BaseModel):
    id: int
    country: str
    year: int
    category: str
    score: float
    source: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
