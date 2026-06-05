from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database import Base


class PerceptionResult(Base):
    __tablename__ = "perception_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    technology = Column(Float, nullable=False)
    culture = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    global_influence = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False)
    ai_report = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="perception_results")
