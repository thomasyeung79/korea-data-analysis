from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional, Union


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
    language: str = "en"


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
    language: str = "en"


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
    language: str = "en"


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
    language: str = "en"


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


class StudyProfile(BaseModel):
    nationality: str = "International"
    age: int = Field(22, ge=15, le=70)
    current_education_level: str = "Undergraduate"
    target_study_level: str = "Graduate School"
    target_major: str = "Computer Science"
    korean_level: str = "None"
    english_level: str = "Intermediate"
    annual_budget: float = Field(20_000_000, ge=0)
    preferred_city: str = "Seoul"


class CareerProfile(BaseModel):
    target_role: str = "Data Analyst"
    work_experience: str = "0-2 years"
    technical_skills: List[str] = Field(default_factory=list)
    korean_level: str = "None"
    english_level: str = "Intermediate"
    target_industry: str = "Technology"
    visa_goal: str = "E-7"


class LivingProfile(BaseModel):
    lifestyle: str = "Standard"
    housing_preference: str = "Shared Apartment"
    monthly_budget: float = Field(1_500_000, ge=0)
    preferred_city: str = "Seoul"
    transport_preference: str = "Public Transit"
    community_preference: str = "International Community"


class MBTICityMatchRequest(BaseModel):
    mbti_type: str = "INFJ"
    social_energy: str = "Medium"
    lifestyle_preference: str = "Balanced"
    pace_preference: str = "Moderate"
    budget_sensitivity: str = "Medium"
    career_priority: int = Field(5, ge=1, le=10)
    study_priority: int = Field(5, ge=1, le=10)
    language: str = "en"

    @field_validator("mbti_type", mode="before")
    @classmethod
    def normalize_mbti(cls, value):
        value = str(value or "INFJ").strip().upper()
        valid = {
            "INTJ", "INTP", "ENTJ", "ENTP",
            "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ",
            "ISTP", "ISFP", "ESTP", "ESFP",
        }
        return value if value in valid else "INFJ"


class MBTICityScore(BaseModel):
    city: str
    total_score: float
    personality_fit_score: float
    lifestyle_fit_score: float
    social_fit_score: float
    career_environment_score: float
    study_environment_score: float
    recommendation_reason: str
    potential_challenges: List[str]
    suggested_living_style: str


class MBTICityMatchResult(BaseModel):
    best_city: str
    city_scores: List[MBTICityScore]
    personality_fit_score: float
    lifestyle_fit_score: float
    social_fit_score: float
    career_environment_score: float
    study_environment_score: float
    recommendation_reason: str
    potential_challenges: List[str]
    suggested_living_style: str


class UserProfileCreate(BaseModel):
    display_name: Optional[str] = "Compass User"
    study_profile: StudyProfile = Field(default_factory=StudyProfile)
    career_profile: CareerProfile = Field(default_factory=CareerProfile)
    living_profile: LivingProfile = Field(default_factory=LivingProfile)


class UserProfileResponse(UserProfileCreate):
    id: int
    created_at: Optional[str] = None


class CityScore(BaseModel):
    city: str
    total_score: float
    study_score: float
    career_score: float
    living_score: float
    cost_score: float
    language_fit_score: float
    lifestyle_score: float
    recommendation_reason: str


class CityRecommendationRequest(BaseModel):
    study_profile: StudyProfile = Field(default_factory=StudyProfile)
    career_profile: CareerProfile = Field(default_factory=CareerProfile)
    living_profile: LivingProfile = Field(default_factory=LivingProfile)
    language: str = "en"


class CityRecommendationResponse(BaseModel):
    best_city: str
    rankings: List[CityScore]


class KoreaLifePlanRequest(UserProfileCreate):
    language: str = "en"


class KoreaLifePlanResponse(BaseModel):
    overall_recommendation: str
    best_city: str
    study_path: str
    career_path: str
    living_plan: str
    estimated_annual_study_cost: float
    estimated_monthly_living_cost: float
    budget_gap: float
    language_risk: str
    career_risk: str
    living_risk: str
    visa_pathway: str
    action_plan_3_month: str
    action_plan_6_month: str
    action_plan_12_month: str
    city_recommendations: List[CityScore]
    markdown_report: str


class IntegratedKoreaLifePlanRequest(KoreaLifePlanRequest):
    city_recommendation: Optional[Dict[str, object]] = None
    mbti_city_match: Optional[Dict[str, object]] = None
    topik_goal: Optional[str] = None


class IntegratedKoreaLifePlanResponse(KoreaLifePlanResponse):
    mbti_city_fit: str
    language_learning_plan: str
    budget_analysis: str
    risk_summary: str
    confidence_summary: str
    based_on_available_inputs: List[str] = Field(default_factory=list)


class KoreaLifePlanHistoryResponse(BaseModel):
    id: int
    display_name: str
    overall_recommendation: str
    best_city: str
    budget_gap: float
    plan_json: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class ExploreOverview(BaseModel):
    country_introduction: str
    population: str
    area: str
    capital: str
    currency: str
    time_zone: str
    language: str
    climate: str


class CityInfo(BaseModel):
    name: str
    population: str
    living_cost: str
    study_score: float
    career_score: float
    lifestyle_score: float
    short_description: str
    best_for: List[str]


class CultureSection(BaseModel):
    title: str
    summary: str
    tips: List[str]


class HistoryEvent(BaseModel):
    period: str
    timeframe: str
    summary: str


class LivingCost(BaseModel):
    city: str
    rent: float
    food: float
    transportation: float
    mobile: float
    utilities: float
    entertainment: float
    currency: str = "KRW"


class QuickFact(BaseModel):
    title: str
    value: str
    detail: str


class KnowledgeMetadata(BaseModel):
    source_name: str
    source_url: str = ""
    last_updated: str
    language: str
    version: str = "1.0"
    confidence_level: str
    notes: str = ""
    official_source: str = ""
    official_url: str = ""
    license: str = ""
    retrieved_at: str = ""
    cache_expiry_days: int = 90
    verification_status: str = "Mock"


class SourceRegistryEntry(BaseModel):
    name: str
    official_url: str
    organization: str
    country: str
    license: str
    default_confidence: str


class SourceRegistryStatus(BaseModel):
    total_sources: int
    valid_sources: int
    missing_name: List[str]
    missing_official_url: List[str]
    missing_license: List[str]
    missing_default_confidence: List[str]
    source_names: List[str]


class VocabularyItem(BaseModel):
    korean: str
    meaning: str
    romanization: Optional[str] = None
    zh: Optional[str] = None
    note_zh: Optional[str] = None
    note_en: Optional[str] = None


class ExpressionItem(BaseModel):
    ko: str
    zh: str = ""
    en: str = ""
    romanization: str = ""
    usage_zh: str = ""
    usage_en: str = ""


class DialogueLine(BaseModel):
    speaker: str = ""
    ko: str
    zh: str = ""
    en: str = ""
    romanization: str = ""


class StudyScenario(BaseModel):
    metadata: Optional[KnowledgeMetadata] = None
    scenario: str
    situation: str
    useful_expressions: List[ExpressionItem] = []
    example_dialogue: List[DialogueLine] = []
    vocabulary: List[VocabularyItem] = []
    ai_explanation: str = ""


class CareerScenario(BaseModel):
    metadata: Optional[KnowledgeMetadata] = None
    scenario: str
    useful_expressions: List[ExpressionItem] = []
    interview_tips: List[str] = []
    business_vocabulary: List[VocabularyItem] = []
    sample_conversation: List[DialogueLine] = []


class LivingScenario(BaseModel):
    metadata: Optional[KnowledgeMetadata] = None
    scenario: str
    useful_expressions: List[ExpressionItem] = []
    common_questions: List[str] = []
    sample_dialogue: List[DialogueLine] = []
    culture_tips: List[str] = []


class TOPIKPlanner(BaseModel):
    metadata: Optional[KnowledgeMetadata] = None
    topik_level: str
    current_level: str
    target_level: str
    recommended_study_hours: str
    weekly_study_plan: List[str]
    suggested_resources: List[str]
    learning_roadmap: List[str]


class KoreanHelperRequest(BaseModel):
    expression: str
    action: str = "explain_expression"
    context: Optional[str] = None


class ExpressionExplanation(BaseModel):
    expression: str
    action: str
    explanation: str
    explanation_zh: str = ""
    explanation_en: str = ""
    natural_rewrite: str
    translation: str
    translation_zh: str = ""
    translation_en: str = ""
    grammar_notes: List[str] = []
    grammar_notes_zh: List[str] = []
    grammar_notes_en: List[str] = []
    culture_notes: List[str] = []
    culture_notes_zh: List[str] = []
    culture_notes_en: List[str] = []
    polite_level: str = ""


class KnowledgeBaseCity(BaseModel):
    metadata: KnowledgeMetadata
    city_name: str
    population: str
    area: str
    climate: str
    average_rent: float
    average_food_cost: float
    transport_cost: float
    top_universities: List[str]
    major_industries: List[str]
    study_score: float
    career_score: float
    living_score: float
    recommended_for: Union[List[str], Dict[str, List[str]]]
    description: str


class KnowledgeBaseUniversity(BaseModel):
    metadata: KnowledgeMetadata
    name: str
    city: str
    ranking: str
    type: str
    website: str
    major_strengths: List[str]
    tuition: Dict[str, object]
    scholarships: List[str]
    international_students: str
    description: str


class KnowledgeBaseVisa(BaseModel):
    metadata: KnowledgeMetadata
    visa_type: str
    description: str
    eligibility: List[str]
    documents: List[str]
    processing_time: str
    renewal: str
    notes: str


class KnowledgeBaseJob(BaseModel):
    metadata: KnowledgeMetadata
    industry: str
    average_salary: Dict[str, object]
    required_language: str
    popular_skills: List[str]
    recommended_regions: List[str]


class KnowledgeBaseLiving(BaseModel):
    metadata: KnowledgeMetadata
    module: str
    summary: str
    typical_costs: Optional[Dict[str, float]] = None
    typical_requirements: Optional[List[str]] = None
    checklist: Optional[List[str]] = None
    tips: Optional[List[str]] = None


class KnowledgeBaseStatus(BaseModel):
    total_files: int
    valid_files: int
    missing_source: List[str]
    missing_last_updated: List[str]
    missing_metadata: List[str]
    knowledge_base_version: str
    metadata_coverage: float
    directory_counts: Dict[str, int]
    last_updated_counts: Dict[str, int]
    confidence_distribution: Dict[str, int]
    source_coverage: Dict[str, int] = Field(default_factory=dict)
    source_coverage_ratio: Dict[str, float] = Field(default_factory=dict)
    official_source_coverage: float = 0.0
    mock_coverage: float = 0.0
    missing_official_source: List[str] = Field(default_factory=list)
    missing_retrieved_at: List[str] = Field(default_factory=list)
    missing_verification_status: List[str] = Field(default_factory=list)

