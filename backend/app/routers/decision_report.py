import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import DecisionReportHistory
from ..schemas import DecisionReportRequest, DecisionReportResponse, DecisionReportHistoryResponse
from decision_report_config import generate_decision_report

router = APIRouter(prefix="/api/v1/decision-report", tags=["decision report"])

VALID_GOALS = ["Study", "Work", "Live"]
VALID_CITIES = ["Seoul", "Busan", "Daejeon", "Daegu", "Other"]
VALID_SCHOOLS = ["Language School", "Undergraduate", "Graduate School", "Not Applicable"]
VALID_HOUSING = ["Dormitory", "Shared Apartment", "Studio Apartment", "Not Applicable"]
VALID_LIFESTYLES = ["Budget", "Standard", "Premium"]
VALID_ROLES = ["Data Analyst", "Backend Developer", "AI Product Manager", "AI Engineer", "Not Applicable"]
VALID_EXPERIENCE = ["Student", "0-2 years", "3-5 years"]
VALID_KOREAN = ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"]


def _clamp(v: str, valid: list[str], default: str) -> str:
    return v if v in valid else default


@router.post("/generate", response_model=DecisionReportResponse)
def generate_decision_report_endpoint(
    request: DecisionReportRequest,
    db: Session = Depends(get_db),
):
    goal = _clamp(request.goal, VALID_GOALS, "Study")
    city = _clamp(request.target_city, VALID_CITIES, "Seoul")
    school = _clamp(request.school_type, VALID_SCHOOLS, "Not Applicable")
    housing = _clamp(request.housing_type, VALID_HOUSING, "Not Applicable")
    lifestyle = _clamp(request.lifestyle_level, VALID_LIFESTYLES, "Standard")
    role = _clamp(request.target_role, VALID_ROLES, "Not Applicable")
    exp = _clamp(request.experience_level, VALID_EXPERIENCE, "0-2 years")
    kl = _clamp(request.korean_level, VALID_KOREAN, "None")
    budget = max(request.monthly_budget, 0)

    result = generate_decision_report(
        goal=goal,
        target_city=city,
        school_type=school,
        housing_type=housing,
        lifestyle_level=lifestyle,
        target_role=role,
        experience_level=exp,
        korean_level=kl,
        monthly_budget=budget,
    )

    history = DecisionReportHistory(
        goal=goal,
        target_city=city,
        monthly_budget=budget,
        recommendation=result["recommendation"],
        financial_risk=result["financial_risk"],
        career_risk=result["career_risk"],
        language_risk=result["language_risk"],
        report_json=json.dumps(result, ensure_ascii=False),
    )
    db.add(history)
    db.commit()

    return DecisionReportResponse(**result)


@router.get("/history", response_model=list[DecisionReportHistoryResponse])
def list_decision_report_history(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    records = (
        db.query(DecisionReportHistory)
        .order_by(DecisionReportHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        DecisionReportHistoryResponse(
            id=r.id,
            goal=r.goal,
            target_city=r.target_city,
            monthly_budget=r.monthly_budget,
            recommendation=r.recommendation,
            financial_risk=r.financial_risk,
            career_risk=r.career_risk,
            language_risk=r.language_risk,
            report_json=r.report_json,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in records
    ]
