import json
from typing import Any


def profile_to_json(profile: Any) -> str:
    if hasattr(profile, "model_dump"):
        return json.dumps(profile.model_dump(), ensure_ascii=False)
    return json.dumps(profile, ensure_ascii=False)


def profile_from_json(raw: str) -> dict:
    return json.loads(raw or "{}")
