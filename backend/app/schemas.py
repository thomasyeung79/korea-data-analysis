from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional


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


class StudyCostRequest(BaseModel):
    city: str
    school_type: str
    housing_type: str
    lifestyle_level: str


class StudyCostResponse(BaseModel):
    monthly_cost: float
    annual_cost: float
    breakdown: Dict[str, float]
    ai_summary: str


class StudyCostHistoryResponse(BaseModel):
    id: int
    city: str
    school_type: str
    housing_type: str
    lifestyle_level: str
    monthly_cost: float
    annual_cost: float
    cost_breakdown_json: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class JobMarketRequest(BaseModel):
    role: str
    experience_level: str
    korean_level: str


class JobMarketResponse(BaseModel):
    salary_min: float
    salary_max: float
    recommended_cities: List[str]
    required_skills: List[str]
    nice_to_have_skills: List[str]
    korean_language_requirement: str
    korean_language_gap: str
    competitiveness: int
    competitiveness_label: str
    visa_pathway: str
    ai_plan: str
    currency: str


class JobMarketHistoryResponse(BaseModel):
    id: int
    role: str
    experience_level: str
    korean_level: str
    salary_min: float
    salary_max: float
    competitiveness: int
    recommended_skills_json: Optional[str] = None
    ai_plan: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class DecisionReportRequest(BaseModel):
    goal: str
    target_city: str
    school_type: str
    housing_type: str
    lifestyle_level: str
    target_role: str
    experience_level: str
    korean_level: str
    monthly_budget: float


class DecisionReportResponse(BaseModel):
    recommendation: str
    recommendation_label: str
    monthly_cost_estimate: float
    annual_cost_estimate: float
    cost_breakdown: Dict[str, float]
    budget_gap: float
    budget_gap_pct: float
    financial_risk: str
    language_risk: str
    language_risk_detail: str
    career_risk: str
    career_risk_detail: str
    visa_living_risk: str
    visa_living_risk_detail: str
    salary_min: float
    salary_max: float
    required_skills: List[str]
    korean_language_requirement: str
    competitiveness: int
    action_plan: str
    summary: str
    currency: str


class DecisionReportHistoryResponse(BaseModel):
    id: int
    goal: str
    target_city: str
    monthly_budget: float
    recommendation: str
    financial_risk: str
    career_risk: str
    language_risk: str
    report_json: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class NewsPolicyRequest(BaseModel):
    keyword: str = ""
    category: str = "All"
    time_range: str = "Last 30 days"


class NewsItem(BaseModel):
    title: str
    category: str
    source_name: str
    published_at: str
    summary: str
    impact_for_students: str
    impact_for_job_seekers: str
    relevance_score: float
    source_url: str
    tags: List[str]


class NewsPolicyResponse(BaseModel):
    results: List[NewsItem]
    ai_summary: str
    action_suggestions: List[str]
    result_count: int


class NewsPolicyHistoryResponse(BaseModel):
    id: int
    keyword: Optional[str] = None
    category: str
    time_range: str
    result_count: int
    ai_summary: Optional[str] = None
    results_json: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class PerceptionScores(BaseModel):
    economy: int = Field(..., ge=1, le=10)
    technology: int = Field(..., ge=1, le=10)
    education: int = Field(..., ge=1, le=10)
    culture: int = Field(..., ge=1, le=10)
    global_influence: int = Field(..., ge=1, le=10)
    quality_of_life: int = Field(..., ge=1, le=10)


class AIReportRequest(BaseModel):
    display_name: Optional[str] = None
    scores: PerceptionScores
    comment: Optional[str] = None
    korea_baseline: Optional[Dict[str, float]] = None
    community_average: Optional[Dict[str, float]] = None
    total_submissions: Optional[int] = None


class AIReportResponse(BaseModel):
    provider: str
    profile_label: str
    perception_summary: str
    strongest_associations: List[str]
    concerns_or_gaps: List[str]
    korea_baseline_comparison: str
    community_average_comparison: str
    interpretation_profile: str
    suggested_next_question: str
