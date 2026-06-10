from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional


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


class PerceptionSurveyCreate(BaseModel):
    display_name: Optional[str] = "Anonymous"
    economy_score: int = Field(..., ge=1, le=10)
    technology_score: int = Field(..., ge=1, le=10)
    education_score: int = Field(..., ge=1, le=10)
    culture_score: int = Field(..., ge=1, le=10)
    global_influence_score: int = Field(..., ge=1, le=10)
    quality_of_life_score: int = Field(..., ge=1, le=10)
    comment: Optional[str] = None

    @field_validator("display_name", mode="before")
    @classmethod
    def default_display_name(cls, value):
        if value is None:
            return "Anonymous"
        value = str(value).strip()
        return value or "Anonymous"

    @field_validator("comment", mode="before")
    @classmethod
    def clean_comment(cls, value):
        if value is None:
            return None
        value = str(value).strip()
        return value or None


class PerceptionSurveyResponse(BaseModel):
    id: int
    display_name: str
    economy_score: int
    technology_score: int
    education_score: int
    culture_score: int
    global_influence_score: int
    quality_of_life_score: int
    comment: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class PerceptionSurveyStats(BaseModel):
    total_submissions: int
    average_score: Optional[float] = None
    average_by_category: Dict[str, float] = Field(default_factory=dict)
    strongest_category: Optional[str] = None
    weakest_category: Optional[str] = None
    korea_baseline: Dict[str, float]
