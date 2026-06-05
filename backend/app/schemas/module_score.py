from pydantic import BaseModel
from typing import Optional


class ModuleScoreCreate(BaseModel):
    module_name: str
    score: float


class ModuleScoreResponse(BaseModel):
    id: int
    user_id: int
    module_name: str
    score: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
