from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database import Base


class TravelOrder(Base):
    __tablename__ = "travel_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(String(20), unique=True, nullable=False)
    route = Column(Text, nullable=False)
    days = Column(Integer, nullable=False)
    budget = Column(String(20), nullable=False)
    interests = Column(Text, nullable=True)
    travel_style = Column(String(50), nullable=True)
    estimated_price = Column(Float, nullable=True)
    status = Column(String(20), default="Draft")
    payment_status = Column(String(20), default="Unpaid")
    ai_plan = Column(Text, nullable=True)
    itinerary_json = Column(Text, nullable=True)
    customer_notes = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="travel_orders")
