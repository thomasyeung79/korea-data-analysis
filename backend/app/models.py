from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text, UniqueConstraint

from .database import Base


class CountryScore(Base):
    __tablename__ = "country_scores"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    source = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("country", "year", "category", name="uq_country_year_cat"),
    )


class StudyCostHistory(Base):
    __tablename__ = "study_cost_history"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(50), nullable=False)
    school_type = Column(String(50), nullable=False)
    housing_type = Column(String(50), nullable=False)
    lifestyle_level = Column(String(50), nullable=False)
    monthly_cost = Column(Float, nullable=False)
    annual_cost = Column(Float, nullable=False)
    cost_breakdown_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class JobMarketHistory(Base):
    __tablename__ = "job_market_history"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50), nullable=False)
    experience_level = Column(String(50), nullable=False)
    korean_level = Column(String(50), nullable=False)
    salary_min = Column(Float, nullable=False)
    salary_max = Column(Float, nullable=False)
    competitiveness = Column(Integer, nullable=False)
    recommended_skills_json = Column(Text, nullable=True)
    ai_plan = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DecisionReportHistory(Base):
    __tablename__ = "decision_report_history"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String(50), nullable=False)
    target_city = Column(String(50), nullable=False)
    monthly_budget = Column(Float, nullable=False)
    recommendation = Column(String(50), nullable=False)
    financial_risk = Column(String(50), nullable=False)
    career_risk = Column(String(50), nullable=False)
    language_risk = Column(String(50), nullable=False)
    report_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class NewsPolicyHistory(Base):
    __tablename__ = "news_policy_history"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False)
    time_range = Column(String(50), nullable=False)
    result_count = Column(Integer, nullable=False)
    ai_summary = Column(Text, nullable=True)
    results_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class PerceptionSurvey(Base):
    __tablename__ = "perception_surveys"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(80), nullable=False, default="Anonymous")
    economy_score = Column(Integer, nullable=False)
    technology_score = Column(Integer, nullable=False)
    education_score = Column(Integer, nullable=False)
    culture_score = Column(Integer, nullable=False)
    global_influence_score = Column(Integer, nullable=False)
    quality_of_life_score = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    display_name = Column(String(80), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    display_name = Column(String(80), nullable=False, default="Compass User")
    study_profile_json = Column(Text, nullable=False)
    career_profile_json = Column(Text, nullable=False)
    living_profile_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class KoreaLifePlanHistory(Base):
    __tablename__ = "korea_life_plan_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    display_name = Column(String(80), nullable=False, default="Compass User")
    overall_recommendation = Column(String(80), nullable=False)
    best_city = Column(String(50), nullable=False)
    budget_gap = Column(Float, nullable=False)
    plan_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CityRecommendationHistory(Base):
    __tablename__ = "city_recommendation_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    best_city = Column(String(50), nullable=False)
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
