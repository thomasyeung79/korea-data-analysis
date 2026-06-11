from fastapi import APIRouter

from ..ai.report_engine import AIReportEngine
from ..schemas import AIReportRequest, AIReportResponse

router = APIRouter(prefix="/api/v1/ai", tags=["ai reports"])


@router.post("/perception-report", response_model=AIReportResponse)
def generate_perception_report(request: AIReportRequest):
    return AIReportEngine().generate(request)
