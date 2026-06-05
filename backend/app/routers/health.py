from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/api/v1/health")
def health_check():
    return {"status": "ok", "message": "KoreaIntel Pro API is running"}
