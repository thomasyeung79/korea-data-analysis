from fastapi import APIRouter, HTTPException

from ..schemas import SourceRegistryEntry, SourceRegistryStatus
from ..services.source_registry import get_source, list_sources, validate_source

router = APIRouter(prefix="/api/v1/sources", tags=["sources"])


@router.get("", response_model=list[SourceRegistryEntry])
def sources_list():
    return list_sources()


@router.get("/status", response_model=SourceRegistryStatus)
def sources_status():
    return validate_source()


@router.get("/{name}", response_model=SourceRegistryEntry)
def sources_detail(name: str):
    try:
        return get_source(name)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
