from pydantic import BaseModel
from typing import Optional


class TravelOrderCreate(BaseModel):
    route: str
    days: int
    budget: str
    interests: Optional[str] = None
    travel_style: Optional[str] = None
    estimated_price: Optional[float] = None
    generate_ai_plan: bool = False
    customer_notes: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class TravelOrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    customer_notes: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class TravelOrderResponse(BaseModel):
    id: int
    user_id: int
    order_id: str
    route: str
    days: int
    budget: str
    interests: Optional[str] = None
    travel_style: Optional[str] = None
    estimated_price: Optional[float] = None
    status: Optional[str] = None
    payment_status: Optional[str] = None
    ai_plan: Optional[str] = None
    itinerary_json: Optional[str] = None
    customer_notes: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
