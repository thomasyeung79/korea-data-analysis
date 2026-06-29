import json

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import KnowledgeBaseCity, KnowledgeBaseStatus, KnowledgeMetadata
from backend.app.services import data_loader

client = TestClient(app)


def test_all_knowledge_json_files_have_metadata():
    files = data_loader.list_knowledge_files()
    assert files

    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(payload, dict), f"{path} must use an object root"
        assert "metadata" in payload, f"{path} missing metadata"
        KnowledgeMetadata(**payload["metadata"])


def test_validate_metadata_reports_full_coverage():
    status = data_loader.validate_metadata()
    parsed = KnowledgeBaseStatus(**status)

    assert parsed.total_files >= 44
    assert parsed.valid_files == parsed.total_files
    assert parsed.metadata_coverage == 1.0
    assert parsed.missing_metadata == []
    assert parsed.missing_source == []
    assert parsed.missing_last_updated == []
    assert parsed.knowledge_base_version == "1.0"


def test_loader_returns_metadata_with_city_record():
    city = data_loader.load_city("Seoul")
    parsed = KnowledgeBaseCity(**city)

    assert parsed.metadata.source_name
    assert parsed.metadata.last_updated == "2026-06-29"
    assert parsed.city_name == "Seoul"


def test_learning_loader_attaches_metadata_to_items():
    records = data_loader.load_learning("study")

    assert records[0]["metadata"]["source_name"]
    assert records[0]["scenario"] == "Classroom"


def test_kb_status_api():
    response = client.get("/api/v1/kb/status")
    assert response.status_code == 200
    data = response.json()

    assert data["total_files"] >= 44
    assert data["valid_files"] == data["total_files"]
    assert data["metadata_coverage"] == 1.0
    assert "cities" in data["directory_counts"]
    assert "Medium" in data["confidence_distribution"] or "Low" in data["confidence_distribution"]
