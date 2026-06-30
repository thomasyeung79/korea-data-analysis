from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"


def _normalise_key(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


@lru_cache(maxsize=256)
def _load_json(relative_path: str) -> Any:
    path = DATA_ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _metadata(envelope: Any) -> dict:
    if isinstance(envelope, dict):
        return envelope.get("metadata", {})
    return {}


def _content(envelope: Any) -> Any:
    if isinstance(envelope, dict) and "items" in envelope:
        return envelope["items"]
    if isinstance(envelope, dict) and "metadata" in envelope:
        return {key: value for key, value in envelope.items() if key != "metadata"}
    return envelope


def _attach_metadata(record: dict, metadata: dict) -> dict:
    return {"metadata": metadata, **record}


@lru_cache(maxsize=64)
def _load_directory(directory: str) -> tuple[tuple[str, Any], ...]:
    folder = DATA_ROOT / directory
    records = []
    for path in sorted(folder.glob("*.json")):
        envelope = _load_json(f"{directory}/{path.name}")
        records.append((path.stem, _attach_metadata(_content(envelope), _metadata(envelope))))
    return tuple(records)


def list_knowledge_files() -> list[Path]:
    return sorted(DATA_ROOT.rglob("*.json"))


def load_city(city_name: str | None = None) -> dict | list[dict]:
    records = [record for _, record in _load_directory("cities")]
    if city_name is None:
        return records
    key = _normalise_key(city_name)
    for record in records:
        if _normalise_key(record["city_name"]) == key:
            return record
    raise KeyError(f"Unknown city: {city_name}")


def load_university(name: str | None = None) -> dict | list[dict]:
    records = [record for _, record in _load_directory("universities")]
    if name is None:
        return records
    key = _normalise_key(name)
    for record in records:
        if _normalise_key(record["name"]) == key:
            return record
    raise KeyError(f"Unknown university: {name}")


def load_major(name: str | None = None) -> dict | list[dict]:
    envelope = _load_json("majors/majors.json")
    metadata = _metadata(envelope)
    records = [_attach_metadata(record, metadata) for record in _content(envelope)]
    if name is None:
        return records
    key = _normalise_key(name)
    for record in records:
        if _normalise_key(record["name"]) == key:
            return record
    raise KeyError(f"Unknown major: {name}")


def load_job(industry: str | None = None) -> dict | list[dict]:
    records = [record for _, record in _load_directory("jobs")]
    if industry is None:
        return records
    key = _normalise_key(industry)
    for record in records:
        if _normalise_key(record["industry"]) == key:
            return record
    raise KeyError(f"Unknown job industry: {industry}")


def load_visa(visa_type: str | None = None) -> dict | list[dict]:
    records = [record for _, record in _load_directory("visa")]
    if visa_type is None:
        return records
    key = visa_type.strip().lower()
    for record in records:
        if record["visa_type"].lower() == key:
            return record
    raise KeyError(f"Unknown visa type: {visa_type}")


def load_living(module: str | None = None) -> dict | list[dict]:
    records = [record for _, record in _load_directory("living")]
    if module is None:
        return records
    key = _normalise_key(module)
    for record in records:
        if _normalise_key(record["module"]) == key:
            return record
    raise KeyError(f"Unknown living module: {module}")


def load_culture(kind: str) -> dict:
    envelope = _load_json(f"culture/{_normalise_key(kind)}.json")
    return _attach_metadata(_content(envelope), _metadata(envelope))


def load_learning(kind: str) -> list[dict]:
    envelope = _load_json(f"korean/{_normalise_key(kind)}.json")
    metadata = _metadata(envelope)
    return [_normalise_learning_record(_attach_metadata(record, metadata)) for record in _content(envelope)]


def _normalise_learning_record(record: dict) -> dict:
    item = dict(record)
    if "situation" not in item and "situation_en" in item:
        item["situation"] = item["situation_en"]
    if "ai_explanation" not in item and "ai_explanation_en" in item:
        item["ai_explanation"] = item["ai_explanation_en"]
    return item


def kb_file_count() -> int:
    return len(list_knowledge_files())


def validate_metadata() -> dict:
    files = list_knowledge_files()
    missing_metadata = []
    missing_source = []
    missing_last_updated = []
    missing_official_source = []
    missing_retrieved_at = []
    missing_verification_status = []
    directory_counts: dict[str, int] = {}
    last_updated_counts: dict[str, int] = {}
    confidence_distribution: dict[str, int] = {}
    source_coverage: dict[str, int] = {"Official": 0, "Verified": 0, "Community": 0, "Mock": 0}
    versions: set[str] = set()

    for path in files:
        rel = path.relative_to(DATA_ROOT).as_posix()
        directory = rel.split("/")[0] if "/" in rel else "root"
        directory_counts[directory] = directory_counts.get(directory, 0) + 1
        envelope = _load_json(rel)
        metadata = _metadata(envelope)
        if not metadata:
            missing_metadata.append(rel)
            continue
        source_name = str(metadata.get("source_name", "")).strip()
        last_updated = str(metadata.get("last_updated", "")).strip()
        confidence = str(metadata.get("confidence_level", "")).strip() or "Unknown"
        version = str(metadata.get("version", "")).strip()
        official_source = str(metadata.get("official_source", "")).strip()
        official_url = str(metadata.get("official_url", "")).strip()
        retrieved_at = str(metadata.get("retrieved_at", "")).strip()
        verification_status = str(metadata.get("verification_status", "")).strip() or "Unknown"
        if not source_name:
            missing_source.append(rel)
        if not last_updated:
            missing_last_updated.append(rel)
        if not official_source or not official_url:
            missing_official_source.append(rel)
        if not retrieved_at:
            missing_retrieved_at.append(rel)
        if verification_status not in {"Official", "Verified", "Community", "Mock"}:
            missing_verification_status.append(rel)
        if last_updated:
            last_updated_counts[last_updated] = last_updated_counts.get(last_updated, 0) + 1
        confidence_distribution[confidence] = confidence_distribution.get(confidence, 0) + 1
        source_coverage[verification_status] = source_coverage.get(verification_status, 0) + 1
        if version:
            versions.add(version)

    issue_files = set(
        missing_metadata
        + missing_source
        + missing_last_updated
        + missing_official_source
        + missing_retrieved_at
        + missing_verification_status
    )
    valid_files = len(files) - len(issue_files)
    coverage = round(valid_files / len(files), 4) if files else 1.0
    source_coverage = dict(sorted(source_coverage.items()))
    source_coverage_ratio = {
        key: round(value / len(files), 4) if files else 0.0
        for key, value in source_coverage.items()
    }
    return {
        "total_files": len(files),
        "valid_files": valid_files,
        "missing_source": missing_source,
        "missing_last_updated": missing_last_updated,
        "missing_metadata": missing_metadata,
        "knowledge_base_version": ", ".join(sorted(versions)) or "unknown",
        "metadata_coverage": coverage,
        "directory_counts": dict(sorted(directory_counts.items())),
        "last_updated_counts": dict(sorted(last_updated_counts.items())),
        "confidence_distribution": dict(sorted(confidence_distribution.items())),
        "source_coverage": source_coverage,
        "source_coverage_ratio": source_coverage_ratio,
        "official_source_coverage": source_coverage_ratio.get("Official", 0.0),
        "mock_coverage": source_coverage_ratio.get("Mock", 0.0),
        "missing_official_source": missing_official_source,
        "missing_retrieved_at": missing_retrieved_at,
        "missing_verification_status": missing_verification_status,
    }
