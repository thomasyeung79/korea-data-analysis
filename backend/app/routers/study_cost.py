import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import StudyCostHistory
from ..schemas import StudyCostRequest, StudyCostResponse, StudyCostHistoryResponse
from ..services.study_cost_config import calculate_costs, generate_cost_explanation

router = APIRouter(prefix="/api/v1/study-cost", tags=["study cost"])

VALID_CITIES = {"Seoul", "Busan", "Daejeon", "Daegu", "Other"}
VALID_SCHOOL_TYPES = {"Language School", "Undergraduate", "Graduate School"}
VALID_HOUSING = {"Dormitory", "Shared Apartment", "Studio Apartment"}
VALID_LIFESTYLES = {"Budget", "Standard", "Premium"}


@router.post("/calculate", response_model=StudyCostResponse)
def calculate_study_cost(
    request: StudyCostRequest,
    db: Session = Depends(get_db),
):
    # Validate inputs
    if request.city not in VALID_CITIES:
        request.city = "Other"
    if request.school_type not in VALID_SCHOOL_TYPES:
        request.school_type = "Undergraduate"
    if request.housing_type not in VALID_HOUSING:
        request.housing_type = "Shared Apartment"
    if request.lifestyle_level not in VALID_LIFESTYLES:
        request.lifestyle_level = "Standard"

    # Calculate
    result = calculate_costs(
        city=request.city,
        school_type=request.school_type,
        housing_type=request.housing_type,
        lifestyle=request.lifestyle_level,
    )

    # Generate AI summary
    ai_summary = generate_cost_explanation(
        city=request.city,
        school_type=request.school_type,
        housing_type=request.housing_type,
        lifestyle=request.lifestyle_level,
        result=result,
    )

    # Save to history
    history = StudyCostHistory(
        city=request.city,
        school_type=request.school_type,
        housing_type=request.housing_type,
        lifestyle_level=request.lifestyle_level,
        monthly_cost=result["monthly_cost"],
        annual_cost=result["annual_cost"],
        cost_breakdown_json=json.dumps(result["breakdown"], ensure_ascii=False),
    )
    db.add(history)
    db.commit()

    return StudyCostResponse(
        monthly_cost=result["monthly_cost"],
        annual_cost=result["annual_cost"],
        breakdown=result["breakdown"],
        ai_summary=ai_summary,
    )


@router.get("/history", response_model=list[StudyCostHistoryResponse])
def list_study_cost_history(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    records = (
        db.query(StudyCostHistory)
        .order_by(StudyCostHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        StudyCostHistoryResponse(
            id=r.id,
            city=r.city,
            school_type=r.school_type,
            housing_type=r.housing_type,
            lifestyle_level=r.lifestyle_level,
            monthly_cost=r.monthly_cost,
            annual_cost=r.annual_cost,
            cost_breakdown_json=r.cost_breakdown_json,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in records
    ]
