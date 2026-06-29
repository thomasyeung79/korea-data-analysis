from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
REGISTRY_PATH = DATA_ROOT / "source_registry.json"


def _normalise(value: str) -> str:
    return value.strip().lower().replace(" ", "-").replace("_", "-")


@lru_cache(maxsize=1)
def _load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def list_sources() -> list[dict]:
    registry = _load_registry()
    return list(registry.get("items", []))


def get_source(name: str) -> dict:
    key = _normalise(name)
    for source in list_sources():
        if _normalise(source.get("name", "")) == key:
            return source
    raise KeyError(f"Unknown source: {name}")


def validate_source() -> dict:
    sources = list_sources()
    missing_name: list[str] = []
    missing_official_url: list[str] = []
    missing_license: list[str] = []
    missing_default_confidence: list[str] = []
    source_names: list[str] = []

    for index, source in enumerate(sources, start=1):
        label = source.get("name") or f"source[{index}]"
        name = str(source.get("name", "")).strip()
        official_url = str(source.get("official_url", "")).strip()
        license_text = str(source.get("license", "")).strip()
        default_confidence = str(source.get("default_confidence", "")).strip()
        if name:
            source_names.append(name)
        else:
            missing_name.append(label)
        if not official_url:
            missing_official_url.append(label)
        if not license_text:
            missing_license.append(label)
        if not default_confidence:
            missing_default_confidence.append(label)

    issue_count = len(set(missing_name + missing_official_url + missing_license + missing_default_confidence))
    return {
        "total_sources": len(sources),
        "valid_sources": len(sources) - issue_count,
        "missing_name": missing_name,
        "missing_official_url": missing_official_url,
        "missing_license": missing_license,
        "missing_default_confidence": missing_default_confidence,
        "source_names": sorted(source_names),
    }
