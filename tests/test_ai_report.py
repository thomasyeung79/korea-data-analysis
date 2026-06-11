import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.ai.local_provider import LocalReportProvider
from backend.app.main import app
from backend.app.schemas import AIReportRequest


def make_request(**scores):
    defaults = {
        "economy": 5,
        "technology": 5,
        "education": 5,
        "culture": 5,
        "global_influence": 5,
        "quality_of_life": 5,
    }
    defaults.update(scores)
    return AIReportRequest(
        display_name="Test User",
        scores=defaults,
        comment="Test comment",
        korea_baseline={
            "Economy": 8,
            "Technology": 9,
            "Education": 8,
            "Culture": 9,
            "Global Influence": 8,
            "Quality of Life": 7,
        },
        community_average=None,
        total_submissions=1,
    )


def test_local_fallback_works_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    report = LocalReportProvider().generate(make_request())
    assert report.provider == "local"
    assert report.profile_label == "Balanced Regional Observer"
    assert report.perception_summary
    assert report.strongest_associations


def test_profile_label_market_driven_pragmatist():
    report = LocalReportProvider().generate(make_request(economy=8, technology=8))
    assert report.profile_label == "Market-Driven Pragmatist"


def test_profile_label_soft_power_enthusiast():
    report = LocalReportProvider().generate(make_request(culture=8, global_influence=8))
    assert report.profile_label == "Soft Power Enthusiast"


def test_profile_label_quality_of_life_skeptic():
    report = LocalReportProvider().generate(make_request(quality_of_life=4))
    assert report.profile_label == "Quality-of-Life Skeptic"


def test_endpoint_returns_valid_response_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = TestClient(app)
    response = client.post(
        "/api/v1/ai/perception-report",
        json={
            "display_name": "Endpoint Test",
            "scores": {
                "economy": 8,
                "technology": 8,
                "education": 6,
                "culture": 7,
                "global_influence": 7,
                "quality_of_life": 6,
            },
            "comment": "Testing endpoint",
            "total_submissions": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "local"
    assert data["profile_label"] == "Market-Driven Pragmatist"
    assert "You are among the first respondents." in data["community_average_comparison"]
    assert data["suggested_next_question"]
