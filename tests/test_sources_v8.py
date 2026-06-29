import json

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import KnowledgeMetadata, SourceRegistryEntry, SourceRegistryStatus
from backend.app.services import data_loader
from backend.app.services.source_registry import get_source, list_sources, validate_source

client = TestClient(app)


def test_source_registry_lists_official_sources():
    sources = list_sources()
    names = {source["name"] for source in sources}

    assert len(sources) >= 7
    assert {"Study in Korea", "MOE Korea", "KOSIS", "TOPIK", "Hi Korea"}.issubset(names)
    SourceRegistryEntry(**sources[0])


def test_source_registry_get_source_by_name():
    source = get_source("Study in Korea")

    assert source["organization"]
    assert source["official_url"].startswith("https://")


def test_source_registry_validation_status():
    status = validate_source()
    parsed = SourceRegistryStatus(**status)

    assert parsed.total_sources >= 7
    assert parsed.valid_sources == parsed.total_sources
    assert parsed.missing_name == []
    assert parsed.missing_official_url == []
    assert parsed.missing_license == []
    assert parsed.missing_default_confidence == []


def test_all_kb_metadata_has_v8_source_fields():
    for path in data_loader.list_knowledge_files():
        payload = json.loads(path.read_text(encoding="utf-8"))
        metadata = KnowledgeMetadata(**payload["metadata"])

        assert metadata.official_source
        assert metadata.official_url
        assert metadata.license
        assert metadata.retrieved_at == "2026-06-29"
        assert metadata.cache_expiry_days > 0
        assert metadata.verification_status in {"Official", "Verified", "Community", "Mock"}


def test_kb_status_reports_source_coverage():
    status = data_loader.validate_metadata()

    assert status["total_files"] >= 45
    assert status["valid_files"] == status["total_files"]
    assert status["source_coverage"]["Official"] > 0
    assert status["source_coverage"]["Verified"] > 0
    assert status["source_coverage"]["Mock"] > 0
    assert status["official_source_coverage"] > 0
    assert status["missing_official_source"] == []
    assert status["missing_retrieved_at"] == []
    assert status["missing_verification_status"] == []


def test_sources_api_endpoints():
    list_response = client.get("/api/v1/sources")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 7

    detail_response = client.get("/api/v1/sources/TOPIK")
    assert detail_response.status_code == 200
    assert detail_response.json()["name"] == "TOPIK"

    status_response = client.get("/api/v1/sources/status")
    assert status_response.status_code == 200
    assert status_response.json()["valid_sources"] == status_response.json()["total_sources"]


def test_kb_status_api_includes_v8_quality_report_fields():
    response = client.get("/api/v1/kb/status")
    assert response.status_code == 200
    data = response.json()

    assert "source_coverage" in data
    assert "source_coverage_ratio" in data
    assert "official_source_coverage" in data
    assert "mock_coverage" in data
