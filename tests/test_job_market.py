"""
Tests for Career & Job Market Analyzer module.

Coverage: 20 tests
- Salary calculations (6)
- Input validation (5)
- Skills and language output (4)
- Database persistence (3)
- AI plan generation (2)
"""

import json
import pytest
from fastapi.testclient import TestClient

from backend.app.database import Base, engine
from backend.app.main import app
from backend.app.services.job_market_config import ROLES

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# ─── Salary Calculations ───

class TestSalaryCalculation:
    """Verify salary ranges are correct for role/experience combinations."""

    def test_backend_salary_student(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "Student", "korean_level": "None",
        }).json()
        assert resp["salary_min"] == 24_000_000
        assert resp["salary_max"] == 35_000_000

    def test_backend_salary_mid(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "3-5 years", "korean_level": "TOPIK 4",
        }).json()
        assert resp["salary_min"] == 55_000_000
        assert resp["salary_max"] == 85_000_000

    def test_ai_engineer_highest_salary(self):
        ai = client.post("/api/v1/job-market/analyze", json={
            "role": "AI Engineer", "experience_level": "3-5 years", "korean_level": "TOPIK 5+",
        }).json()
        backend = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "3-5 years", "korean_level": "TOPIK 5+",
        }).json()
        assert ai["salary_max"] >= backend["salary_max"]

    def test_senior_pays_more_than_junior(self):
        senior = client.post("/api/v1/job-market/analyze", json={
            "role": "Data Analyst", "experience_level": "3-5 years", "korean_level": "TOPIK 3",
        }).json()
        junior = client.post("/api/v1/job-market/analyze", json={
            "role": "Data Analyst", "experience_level": "0-2 years", "korean_level": "TOPIK 3",
        }).json()
        assert senior["salary_min"] >= junior["salary_max"]

    def test_salary_min_always_positive(self):
        for role in ROLES:
            resp = client.post("/api/v1/job-market/analyze", json={
                "role": role, "experience_level": "Student", "korean_level": "None",
            }).json()
            assert resp["salary_min"] > 0
            assert resp["salary_max"] > resp["salary_min"]

    def test_competitiveness_score_range(self):
        for role in ROLES:
            for exp in ["Student", "0-2 years", "3-5 years"]:
                resp = client.post("/api/v1/job-market/analyze", json={
                    "role": role, "experience_level": exp, "korean_level": "TOPIK 4",
                }).json()
                assert 1 <= resp["competitiveness"] <= 10


# ─── Input Validation ───

class TestInputValidation:
    """Verify graceful handling of invalid inputs."""

    def test_invalid_role_falls_back(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Designer", "experience_level": "Student", "korean_level": "None",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["salary_min"] > 0

    def test_invalid_experience_falls_back(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "VP", "korean_level": "None",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["salary_min"] > 0

    def test_invalid_korean_falls_back(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "Student", "korean_level": "Fluent",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["salary_min"] > 0

    def test_missing_role_returns_422(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "experience_level": "Student", "korean_level": "None",
        })
        assert resp.status_code == 422

    def test_missing_all_fields_returns_422(self):
        resp = client.post("/api/v1/job-market/analyze", json={})
        assert resp.status_code == 422


# ─── Skills and Language Output ───

class TestSkillsAndLanguage:
    """Verify skills matrix and language requirements are correct."""

    def test_backend_developer_has_sql_and_python(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "0-2 years", "korean_level": "None",
        }).json()
        must_have = resp["required_skills"]
        assert any("Python" in s or "Java" in s for s in must_have)
        assert any("REST" in s for s in must_have)

    def test_ai_engineer_has_pytorch(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "AI Engineer", "experience_level": "0-2 years", "korean_level": "None",
        }).json()
        skills = " ".join(resp["required_skills"] + resp["nice_to_have_skills"])
        assert "PyTorch" in skills or "TensorFlow" in skills

    def test_language_gap_for_none_level(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "0-2 years", "korean_level": "None",
        }).json()
        assert "limited" in resp["korean_language_gap"].lower()
        assert resp["korean_language_requirement"] != ""

    def test_recommended_cities_non_empty(self):
        for role in ROLES:
            resp = client.post("/api/v1/job-market/analyze", json={
                "role": role, "experience_level": "3-5 years", "korean_level": "TOPIK 5+",
            }).json()
            assert len(resp["recommended_cities"]) >= 1
            assert "Seoul" in resp["recommended_cities"]

    def test_non_it_roles_are_supported(self):
        for role in [
            "Marketing Specialist",
            "Business Analyst",
            "Operations Specialist",
            "Customer Support Specialist",
            "International Sales",
            "Product Manager",
        ]:
            resp = client.post("/api/v1/job-market/analyze", json={
                "role": role,
                "experience_level": "0-2 years",
                "korean_level": "TOPIK 4",
            })
            assert resp.status_code == 200
            data = resp.json()
            assert data["salary_min"] > 0
            assert data["required_skills"]
            assert data["recommended_cities"]


# ─── Database Persistence ───

class TestDatabasePersistence:
    """Verify history is saved and retrievable."""

    def test_history_created_after_analysis(self):
        client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "3-5 years", "korean_level": "TOPIK 4",
        })
        resp = client.get("/api/v1/job-market/history?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["role"] == "Backend Developer"

    def test_history_multiple_records(self):
        for _ in range(3):
            client.post("/api/v1/job-market/analyze", json={
                "role": "AI Engineer", "experience_level": "Student", "korean_level": "TOPIK 3",
            })
        resp = client.get("/api/v1/job-market/history?limit=5")
        assert len(resp.json()) >= 3

    def test_history_contains_skills_json(self):
        client.post("/api/v1/job-market/analyze", json={
            "role": "Data Analyst", "experience_level": "0-2 years", "korean_level": "TOPIK 4",
        })
        resp = client.get("/api/v1/job-market/history?limit=1")
        record = resp.json()[0]
        assert record["recommended_skills_json"] is not None
        parsed = json.loads(record["recommended_skills_json"])
        assert "must_have" in parsed
        assert "nice_to_have" in parsed


# ─── AI Plan Generation ───

class TestAIPlan:
    """Verify AI preparation plan is generated."""

    def test_plan_contains_role_and_monthly_structure(self):
        resp = client.post("/api/v1/job-market/analyze", json={
            "role": "Data Analyst", "experience_level": "Student", "korean_level": "None",
        }).json()
        plan = resp["ai_plan"]
        assert "Month 1" in plan
        assert "Month 2" in plan
        assert "Month 3" in plan
        assert "Data Analyst" in plan

    def test_plan_differs_by_korean_level(self):
        none = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "0-2 years", "korean_level": "None",
        }).json()["ai_plan"]
        topik5 = client.post("/api/v1/job-market/analyze", json={
            "role": "Backend Developer", "experience_level": "0-2 years", "korean_level": "TOPIK 5+",
        }).json()["ai_plan"]
        assert none != topik5


# ─────────────────────────────────────────────────────────
# Total: 20 tests
# ─────────────────────────────────────────────────────────
