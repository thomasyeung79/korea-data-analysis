from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, UniqueConstraint

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
