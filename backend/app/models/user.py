from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    language_preference = Column(String(10), default="English")
    created_at = Column(DateTime, default=datetime.utcnow)

    module_scores = relationship(
        "ModuleScore", back_populates="user", cascade="all, delete-orphan"
    )
    perception_results = relationship(
        "PerceptionResult", back_populates="user", cascade="all, delete-orphan"
    )
    travel_orders = relationship(
        "TravelOrder", back_populates="user", cascade="all, delete-orphan"
    )
