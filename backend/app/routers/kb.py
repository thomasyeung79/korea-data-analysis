from fastapi import APIRouter

from ..schemas import KnowledgeBaseStatus
from ..services.data_loader import validate_metadata

router = APIRouter(prefix="/api/v1/kb", tags=["knowledge base"])


@router.get("/status", response_model=KnowledgeBaseStatus)
def knowledge_base_status():
    return validate_metadata()
