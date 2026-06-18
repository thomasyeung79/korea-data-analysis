from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/api/v1/health")
def health_check():
    return {"status": "ok", "version": "2.0.0", "service": "Korea Study & Career Decision Agent"}
