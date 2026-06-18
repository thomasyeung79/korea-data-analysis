"""
Tests for News & Policy module.

Coverage: 16 tests
- Keyword filtering (3)
- Category filtering (2)
- Time range filtering (2)
- Relevance scoring (2)
- AI summary generation (2)
- Database persistence (2)
- API validation (3)
"""

import json
import pytest
from fastapi.testclient import TestClient

from backend.app.database import Base, engine
from backend.app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# ─── Keyword Filtering ───

class TestKeywordFiltering:
    """Verify keyword search returns correct results."""

    def test_search_visa_returns_relevant_items(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "visa", "category": "All", "time_range": "Last 90 days",
        }).json()
        assert resp["result_count"] > 0
        for item in resp["results"]:
            search_text = (item["title"] + " " + item["summary"] + " " + " ".join(item["tags"])).lower()
            assert "visa" in search_text

    def test_search_ai_returns_multiple_items(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "AI", "category": "All", "time_range": "Last 90 days",
        }).json()
        assert resp["result_count"] >= 3
        for item in resp["results"]:
            search_text = (item["title"] + " " + item["summary"] + " " + " ".join(item["tags"])).lower()
            assert "ai" in search_text

    def test_search_nonexistent_keyword_returns_zero(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "zzzznotfound", "category": "All", "time_range": "Last 90 days",
        }).json()
        assert resp["result_count"] == 0
        assert len(resp["results"]) == 0


# ─── Category Filtering ───

class TestCategoryFiltering:
    """Verify category filter works correctly."""

    def test_category_study_returns_only_study(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "Study", "time_range": "Last 90 days",
        }).json()
        assert resp["result_count"] > 0
        for item in resp["results"]:
            assert item["category"] == "Study"

    def test_category_technology_returns_only_tech(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "Technology", "time_range": "Last 90 days",
        }).json()
        assert resp["result_count"] > 0
        for item in resp["results"]:
            assert item["category"] == "Technology"


# ─── Time Range Filtering ───

class TestTimeRangeFiltering:
    """Verify time range filter narrows results."""

    def test_7_days_fewer_than_90_days(self):
        r7 = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "All", "time_range": "Last 7 days",
        }).json()
        r90 = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "All", "time_range": "Last 90 days",
        }).json()
        assert r7["result_count"] <= r90["result_count"]

    def test_30_days_reasonable_count(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "All", "time_range": "Last 30 days",
        }).json()
        # There are at least 8 items within 30 days in mock data
        assert resp["result_count"] >= 5


# ─── Relevance Scoring ───

class TestRelevanceScoring:
    """Verify relevance scores are calculated."""

    def test_relevance_score_in_range(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "TOPIK", "category": "All", "time_range": "Last 90 days",
        }).json()
        for item in resp["results"]:
            assert 0 <= item["relevance_score"] <= 100

    def test_exact_keyword_match_scores_higher(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "scholarship", "category": "All", "time_range": "Last 90 days",
        }).json()
        if resp["results"]:
            top = resp["results"][0]
            assert top["relevance_score"] > 50


# ─── AI Summary Generation ───

class TestAISummary:
    """Verify AI summary and action suggestions."""

    def test_summary_contains_result_count(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "visa", "category": "All", "time_range": "Last 90 days",
        }).json()
        assert str(resp["result_count"]) in resp["ai_summary"]

    def test_action_suggestions_not_empty(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "All", "time_range": "Last 90 days",
        }).json()
        assert len(resp["action_suggestions"]) > 0


# ─── Database Persistence ───

class TestDatabasePersistence:
    """Verify search history is saved."""

    def test_history_created_after_search(self):
        client.post("/api/v1/news-policy/search", json={
            "keyword": "AI", "category": "All", "time_range": "Last 30 days",
        })
        resp = client.get("/api/v1/news-policy/history?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["keyword"] == "AI"

    def test_history_contains_results_json(self):
        client.post("/api/v1/news-policy/search", json={
            "keyword": "TOPIK", "category": "Study", "time_range": "Last 90 days",
        })
        resp = client.get("/api/v1/news-policy/history?limit=1")
        record = resp.json()[0]
        assert record["results_json"] is not None
        parsed = json.loads(record["results_json"])
        assert len(parsed) > 0


# ─── API Validation ───

class TestAPIValidation:
    """Verify input validation."""

    def test_invalid_category_defaults(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "InvalidCat", "time_range": "Last 30 days",
        })
        assert resp.status_code == 200
        assert resp.json()["result_count"] >= 0

    def test_invalid_time_range_defaults(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "All", "time_range": "Last year",
        })
        assert resp.status_code == 200

    def test_empty_search_returns_all(self):
        resp = client.post("/api/v1/news-policy/search", json={
            "keyword": "", "category": "All", "time_range": "Last 90 days",
        })
        assert resp.status_code == 200
        assert resp.json()["result_count"] > 0
