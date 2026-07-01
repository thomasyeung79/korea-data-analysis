import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.main import app
from backend.app.services import data_loader

client = TestClient(app)


def test_v21_university_dataset_has_required_official_entries():
    universities = data_loader.load_university()
    names = {item["name"] for item in universities}

    assert {
        "Seoul National University",
        "Korea University",
        "Yonsei University",
        "KAIST",
        "POSTECH",
        "Hanyang University",
        "Sungkyunkwan University",
        "Kyung Hee University",
        "Ewha Womans University",
        "Pusan National University",
    } <= names


def test_v21_priority_kb_metadata_has_source_urls():
    priority_dirs = {"universities", "visa", "cities"}
    for path in data_loader.list_knowledge_files():
        relative = path.relative_to(data_loader.DATA_ROOT)
        if relative.parts[0] not in priority_dirs:
            continue

        payload = json.loads(path.read_text(encoding="utf-8"))
        metadata = payload["metadata"]

        assert metadata["source_name"]
        assert metadata["source_url"].startswith("https://")
        assert metadata["retrieved_at"] == "2026-06-30"
        assert metadata["last_updated"] == "2026-06-30"
        assert metadata["verification_status"] in {"Official", "Verified"}


def test_v21_required_visa_types_are_present():
    visas = data_loader.load_visa()
    visa_types = {item["visa_type"] for item in visas}

    assert {"D-2", "D-4", "D-10", "E-7", "F-2", "F-5"} <= visa_types


def test_v21_mock_count_does_not_increase():
    status = data_loader.validate_metadata()

    assert status["source_coverage"].get("Mock", 0) <= 3


def test_v21_kb_status_api_remains_healthy():
    response = client.get("/api/v1/kb/status")

    assert response.status_code == 200
    data = response.json()
    assert data["valid_files"] == data["total_files"]
    assert data["source_coverage"]["Official"] >= 18
    assert data["source_coverage"]["Mock"] <= 3
