from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint

from backend.app.database import Base


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
