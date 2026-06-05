import json
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.travel_order import TravelOrder
from backend.app.schemas.travel_order import TravelOrderCreate, TravelOrderUpdate, TravelOrderResponse
from backend.app.services.openai_service import openai_service

router = APIRouter(prefix="/api/v1/travel", tags=["travel"])

# Valid workflow transitions
VALID_STATUS_TRANSITIONS = {
    "Draft": ["Paid", "Cancelled"],
    "Paid": ["Confirmed", "Refunded"],
    "Confirmed": ["Completed", "Refunded"],
    "Completed": [],
    "Cancelled": [],
    "Refunded": [],
}


def _order_to_response(o: TravelOrder) -> TravelOrderResponse:
    return TravelOrderResponse(
        id=o.id,
        user_id=o.user_id,
        order_id=o.order_id,
        route=o.route,
        days=o.days,
        budget=o.budget,
        interests=o.interests,
        travel_style=o.travel_style,
        estimated_price=o.estimated_price,
        status=o.status,
        payment_status=o.payment_status,
        ai_plan=o.ai_plan,
        itinerary_json=o.itinerary_json,
        customer_notes=o.customer_notes,
        phone=o.phone,
        email=o.email,
        created_at=o.created_at.isoformat() if o.created_at else None,
    )


@router.get("/orders", response_model=List[TravelOrderResponse])
def get_travel_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = (
        db.query(TravelOrder)
        .filter(TravelOrder.user_id == current_user.id)
        .order_by(TravelOrder.created_at.desc())
        .all()
    )
    return [_order_to_response(o) for o in orders]


@router.post("/orders", response_model=TravelOrderResponse)
def create_travel_order(
    data: TravelOrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order_id = str(uuid.uuid4())[:8].upper()

    ai_plan = None
    if data.generate_ai_plan and openai_service.is_available():
        try:
            route_parts = json.loads(data.route) if data.route.startswith("[") else [data.route]
            route_text = " → ".join(route_parts) if isinstance(route_parts, list) else data.route
            interests_list = json.loads(data.interests) if data.interests and data.interests.startswith("[") else (data.interests.split(",") if data.interests else [])
            interests_text = ", ".join(interests_list) if isinstance(interests_list, list) else data.interests

            params = {
                "customer_name": current_user.username,
                "route_text": route_text,
                "days": data.days,
                "budget_text": data.budget,
                "interests_text": interests_text,
                "style_text": data.travel_style or "Relaxed",
                "language": current_user.language_preference,
            }
            ai_plan = openai_service.generate("travel_itinerary", params)
        except Exception:
            ai_plan = None

    order = TravelOrder(
        user_id=current_user.id,
        order_id=order_id,
        route=data.route,
        days=data.days,
        budget=data.budget,
        interests=data.interests,
        travel_style=data.travel_style,
        estimated_price=data.estimated_price,
        status="Draft",
        payment_status="Unpaid",
        ai_plan=ai_plan,
        itinerary_json=None,
        customer_notes=data.customer_notes,
        phone=data.phone,
        email=data.email,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return _order_to_response(order)


@router.get("/orders/{order_id}", response_model=TravelOrderResponse)
def get_travel_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = (
        db.query(TravelOrder)
        .filter(
            TravelOrder.order_id == order_id,
            TravelOrder.user_id == current_user.id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return _order_to_response(order)


@router.put("/orders/{order_id}", response_model=TravelOrderResponse)
def update_travel_order(
    order_id: str,
    data: TravelOrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = (
        db.query(TravelOrder)
        .filter(
            TravelOrder.order_id == order_id,
            TravelOrder.user_id == current_user.id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Status transition validation
    if data.status and data.status != order.status:
        allowed = VALID_STATUS_TRANSITIONS.get(order.status, [])
        if data.status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from '{order.status}' to '{data.status}'. Allowed: {allowed}",
            )
        order.status = data.status
        # Auto-update payment_status
        if data.status == "Paid":
            order.payment_status = "Paid"
        elif data.status == "Refunded":
            order.payment_status = "Refunded"
        elif data.status == "Cancelled":
            order.payment_status = "Cancelled"

    if data.payment_status:
        order.payment_status = data.payment_status
    if data.customer_notes is not None:
        order.customer_notes = data.customer_notes
    if data.phone is not None:
        order.phone = data.phone
    if data.email is not None:
        order.email = data.email

    db.commit()
    db.refresh(order)
    return _order_to_response(order)


@router.delete("/orders/{order_id}")
def delete_travel_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = (
        db.query(TravelOrder)
        .filter(
            TravelOrder.order_id == order_id,
            TravelOrder.user_id == current_user.id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.status not in ("Draft", "Cancelled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete order in '{order.status}' status. Only Draft or Cancelled orders can be deleted.",
        )

    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}


@router.get("/analytics")
def get_travel_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = (
        db.query(TravelOrder)
        .filter(TravelOrder.user_id == current_user.id)
        .all()
    )

    total_orders = len(orders)
    total_revenue = sum(o.estimated_price or 0 for o in orders)
    avg_order = round(total_revenue / total_orders, 2) if total_orders > 0 else 0
    paid_orders = sum(1 for o in orders if o.payment_status == "Paid")

    route_counts: dict[str, int] = {}
    budget_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for o in orders:
        route = o.route
        route_counts[route] = route_counts.get(route, 0) + 1
        budget_counts[o.budget] = budget_counts.get(o.budget, 0) + 1
        status_counts[o.status] = status_counts.get(o.status, 0) + 1

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "average_order_value": avg_order,
        "paid_orders": paid_orders,
        "route_popularity": route_counts,
        "budget_distribution": budget_counts,
        "status_distribution": status_counts,
    }
