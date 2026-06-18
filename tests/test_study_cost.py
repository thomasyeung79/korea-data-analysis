"""
Tests for Study Cost Calculator module.

Coverage:
- Cost calculation accuracy (6+ city/school/housing/lifestyle combinations)
- Invalid input handling (fallback defaults)
- Breakdown proportions
- Database save operation (via API)
- AI explanation generation
"""

import json
import pytest
from fastapi.testclient import TestClient

from backend.app.database import Base, engine
from backend.app.main import app

client = TestClient(app)


# ── Fixtures ──

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# ─── Cost Calculation Accuracy ───

class TestCostCalculation:
    """Verify that calculate_costs returns correct values for known inputs."""

    def test_seoul_standard_undergrad_dorm(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["monthly_cost"] > 0
        assert data["annual_cost"] == data["monthly_cost"] * 12
        assert "Tuition" in data["breakdown"]
        assert "Housing" in data["breakdown"]
        assert "Food" in data["breakdown"]

    def test_busan_budget_undergrad_shared(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Busan", "school_type": "Undergraduate",
            "housing_type": "Shared Apartment", "lifestyle_level": "Budget",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["monthly_cost"] > 0
        # Budget should be cheaper than Standard in same city
        std_resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Busan", "school_type": "Undergraduate",
            "housing_type": "Shared Apartment", "lifestyle_level": "Standard",
        })
        assert data["monthly_cost"] < std_resp.json()["monthly_cost"]

    def test_seoul_vs_busan_cost_difference(self):
        seoul = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Shared Apartment", "lifestyle_level": "Standard",
        }).json()
        busan = client.post("/api/v1/study-cost/calculate", json={
            "city": "Busan", "school_type": "Undergraduate",
            "housing_type": "Shared Apartment", "lifestyle_level": "Standard",
        }).json()
        assert seoul["monthly_cost"] > busan["monthly_cost"]

    def test_premium_vs_budget_significant_difference(self):
        premium = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Studio Apartment", "lifestyle_level": "Premium",
        }).json()
        budget = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Studio Apartment", "lifestyle_level": "Budget",
        }).json()
        assert premium["monthly_cost"] > budget["monthly_cost"] * 1.1  # at least 10% more

    def test_language_school_cheaper_than_graduate(self):
        lang = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Language School",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        }).json()
        grad = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Graduate School",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        }).json()
        assert lang["monthly_cost"] < grad["monthly_cost"]

    def test_housing_cost_order(self):
        """Dormitory < Shared < Studio within same city."""
        dorm = client.post("/api/v1/study-cost/calculate", json={
            "city": "Daejeon", "school_type": "Undergraduate",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        }).json()
        shared = client.post("/api/v1/study-cost/calculate", json={
            "city": "Daejeon", "school_type": "Undergraduate",
            "housing_type": "Shared Apartment", "lifestyle_level": "Standard",
        }).json()
        studio = client.post("/api/v1/study-cost/calculate", json={
            "city": "Daejeon", "school_type": "Undergraduate",
            "housing_type": "Studio Apartment", "lifestyle_level": "Standard",
        }).json()
        assert dorm["monthly_cost"] < shared["monthly_cost"] < studio["monthly_cost"]


# ─── Invalid Input Handling ───

class TestInvalidInput:
    """Verify graceful fallback for invalid inputs."""

    def test_invalid_city_falls_back(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "InvalidCity", "school_type": "Undergraduate",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["monthly_cost"] > 0

    def test_invalid_school_type_falls_back(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "PhD Program",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["monthly_cost"] > 0

    def test_invalid_housing_falls_back(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Mansion", "lifestyle_level": "Standard",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["monthly_cost"] > 0

    def test_invalid_lifestyle_falls_back(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Dormitory", "lifestyle_level": "Luxury",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["monthly_cost"] > 0

    def test_missing_field_returns_422(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "lifestyle_level": "Standard",
        })
        assert resp.status_code == 422


# ─── Breakdown Proportions ───

class TestCostBreakdown:
    """Verify that breakdown sums match total and proportions are reasonable."""

    def test_breakdown_sums_to_total(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Studio Apartment", "lifestyle_level": "Standard",
        }).json()
        breakdown_sum = sum(resp["breakdown"].values())
        assert abs(breakdown_sum - resp["monthly_cost"]) < 50  # within rounding

    def test_breakdown_has_all_six_categories(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Busan", "school_type": "Graduate School",
            "housing_type": "Shared Apartment", "lifestyle_level": "Premium",
        }).json()
        expected = {"Tuition", "Housing", "Food", "Transportation", "Insurance", "Miscellaneous"}
        assert set(resp["breakdown"].keys()) == expected

    def test_tuition_reasonable_proportion(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Dormitory", "lifestyle_level": "Budget",
        }).json()
        tuition_pct = resp["breakdown"]["Tuition"] / resp["monthly_cost"]
        assert 0.15 < tuition_pct < 0.60


# ─── Database Save ───

class TestDatabaseSave:
    """Verify history is saved and retrievable."""

    def test_history_created_after_calculation(self):
        client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        })
        resp = client.get("/api/v1/study-cost/history?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["city"] == "Seoul"

    def test_history_returns_multiple_records(self):
        for _ in range(3):
            client.post("/api/v1/study-cost/calculate", json={
                "city": "Seoul", "school_type": "Undergraduate",
                "housing_type": "Dormitory", "lifestyle_level": "Standard",
            })
        resp = client.get("/api/v1/study-cost/history?limit=5")
        assert len(resp.json()) >= 3

    def test_history_contains_breakdown_json(self):
        client.post("/api/v1/study-cost/calculate", json={
            "city": "Busan", "school_type": "Language School",
            "housing_type": "Shared Apartment", "lifestyle_level": "Budget",
        })
        resp = client.get("/api/v1/study-cost/history?limit=1")
        record = resp.json()[0]
        assert record["cost_breakdown_json"] is not None
        parsed = json.loads(record["cost_breakdown_json"])
        assert "Tuition" in parsed


# ─── AI Explanation ───

class TestAIExplanation:
    """Verify AI summary is generated and contains key information."""

    def test_ai_summary_contains_city_and_cost(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Seoul", "school_type": "Undergraduate",
            "housing_type": "Studio Apartment", "lifestyle_level": "Premium",
        }).json()
        assert "ai_summary" in resp
        assert "Seoul" in resp["ai_summary"]
        assert "KRW" in resp["ai_summary"]

    def test_ai_summary_mentions_largest_expense(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Daegu", "school_type": "Graduate School",
            "housing_type": "Dormitory", "lifestyle_level": "Budget",
        }).json()
        assert "largest" in resp["ai_summary"].lower() or "Tuition" in resp["ai_summary"] or "Housing" in resp["ai_summary"]

    def test_ai_summary_annual_estimate(self):
        resp = client.post("/api/v1/study-cost/calculate", json={
            "city": "Busan", "school_type": "Language School",
            "housing_type": "Dormitory", "lifestyle_level": "Standard",
        }).json()
        assert "annual" in resp["ai_summary"].lower()
        assert "KRW" in resp["ai_summary"]


# ─────────────────────────────────────────────────────────
# Note: Total test count = 20
# (6 calculation + 5 invalid + 3 breakdown + 3 DB + 3 AI)
# ─────────────────────────────────────────────────────────
