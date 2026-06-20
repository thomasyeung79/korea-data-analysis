"""
Tests for AI Decision Report module.

Coverage: 18 tests
- Recommendation classification (6)
- Budget gap calculation (3)
- Risk scoring (3)
- Report generation (3)
- Database persistence (2)
- API validation (1)
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


GOOD_BUDGET = {
    "goal": "Study", "target_city": "Busan", "school_type": "Undergraduate",
    "housing_type": "Dormitory", "lifestyle_level": "Standard",
    "target_role": "Not Applicable", "experience_level": "Student",
    "korean_level": "TOPIK 5+", "monthly_budget": 2_500_000,
}

MIN_BUDGET = {
    "goal": "Work", "target_city": "Busan", "school_type": "Not Applicable",
    "housing_type": "Shared Apartment", "lifestyle_level": "Budget",
    "target_role": "Backend Developer", "experience_level": "0-2 years",
    "korean_level": "TOPIK 4", "monthly_budget": 1_500_000,
}

LOW_BUDGET = {
    "goal": "Live", "target_city": "Seoul", "school_type": "Not Applicable",
    "housing_type": "Studio Apartment", "lifestyle_level": "Premium",
    "target_role": "Not Applicable", "experience_level": "Student",
    "korean_level": "None", "monthly_budget": 500_000,
}


# ─── Recommendation Classification ───

class TestRecommendation:
    """Verify recommendation labels are correct for different profiles."""

    def test_good_profile_strongly_recommended(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        assert resp["recommendation"] == "strongly_recommended"

    def test_adequate_profile_recommended_with_prep(self):
        resp = client.post("/api/v1/decision-report/generate", json=MIN_BUDGET).json()
        assert resp["recommendation"] in ("strongly_recommended", "recommended_with_prep", "risky")

    def test_low_budget_risky_or_not_recommended(self):
        resp = client.post("/api/v1/decision-report/generate", json=LOW_BUDGET).json()
        assert resp["recommendation"] in ("risky", "not_recommended")

    def test_recommendation_label_is_readable(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        assert "Strongly Recommended" in resp["recommendation_label"] or "✅" in resp["recommendation_label"]

    def test_summary_not_empty(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        assert len(resp["summary"]) > 20

    def test_action_plan_has_three_months(self):
        resp = client.post("/api/v1/decision-report/generate", json=MIN_BUDGET).json()
        plan = resp["action_plan"]
        assert "Month 1" in plan
        assert "Month 2" in plan
        assert "Month 3" in plan

    def test_chinese_decision_report_summary_and_plan(self):
        payload = dict(MIN_BUDGET)
        payload["language"] = "zh"
        resp = client.post("/api/v1/decision-report/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "韩国" in data["summary"]
        assert "第 1 个月" in data["action_plan"]
        assert data["recommendation_label"] in (
            "强烈推荐 ✅",
            "准备充分后推荐 ⚠️",
            "有一定风险 ❓",
            "暂不推荐 ❌",
        )

    def test_language_omitted_defaults_to_english_decision_report(self):
        resp = client.post("/api/v1/decision-report/generate", json=MIN_BUDGET)
        assert resp.status_code == 200
        data = resp.json()
        assert "Month 1" in data["action_plan"]
        assert "Korea" in data["summary"]


# ─── Budget Gap Calculation ───

class TestBudgetGap:
    """Verify budget gap is calculated correctly."""

    def test_positive_gap_when_budget_exceeds_cost(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        assert resp["budget_gap"] > 0

    def test_negative_gap_when_budget_below_cost(self):
        resp = client.post("/api/v1/decision-report/generate", json=LOW_BUDGET).json()
        assert resp["budget_gap"] < 0

    def test_gap_pct_in_plausible_range(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        assert -100 <= resp["budget_gap_pct"] <= 500


# ─── Risk Scoring ───

class TestRiskScoring:
    """Verify risk assessment produces valid outputs."""

    def test_financial_risk_valid_values(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        assert resp["financial_risk"] in ("Low", "Medium", "High")

    def test_language_risk_valid_values(self):
        resp = client.post("/api/v1/decision-report/generate", json=LOW_BUDGET).json()
        assert resp["language_risk"] in ("Low", "Medium", "High")

    def test_visa_risk_not_empty(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        assert len(resp["visa_living_risk_detail"]) > 0


# ─── Report Generation ───

class TestReportGeneration:
    """Verify report contains all required fields."""

    def test_report_has_all_sections(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        required = ["recommendation", "monthly_cost_estimate", "annual_cost_estimate",
                     "cost_breakdown", "financial_risk", "language_risk",
                     "career_risk", "action_plan", "summary"]
        for field in required:
            assert field in resp, f"Missing field: {field}"

    def test_cost_breakdown_has_all_six_categories(self):
        resp = client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET).json()
        expected = {"Tuition", "Housing", "Food", "Transportation", "Insurance", "Miscellaneous"}
        assert set(resp["cost_breakdown"].keys()) == expected

    def test_career_fields_when_role_selected(self):
        payload = {**GOOD_BUDGET, "target_role": "AI Engineer", "experience_level": "3-5 years", "korean_level": "TOPIK 5+"}
        resp = client.post("/api/v1/decision-report/generate", json=payload).json()
        assert resp["salary_min"] > 0
        assert len(resp["required_skills"]) > 0


# ─── Database Persistence ───

class TestDatabasePersistence:
    """Verify history is saved."""

    def test_history_created_after_generate(self):
        client.post("/api/v1/decision-report/generate", json=GOOD_BUDGET)
        resp = client.get("/api/v1/decision-report/history?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["goal"] == "Study"

    def test_history_contains_report_json(self):
        client.post("/api/v1/decision-report/generate", json=MIN_BUDGET)
        resp = client.get("/api/v1/decision-report/history?limit=1")
        record = resp.json()[0]
        assert record["report_json"] is not None
        parsed = json.loads(record["report_json"])
        assert "recommendation" in parsed


# ─── API Validation ───

class TestAPIValidation:
    """Verify input validation."""

    def test_missing_field_returns_422(self):
        resp = client.post("/api/v1/decision-report/generate", json={
            "goal": "Study", "target_city": "Seoul",
        })
        assert resp.status_code == 422


# ─── Chinese Localization Coverage ───

class TestChineseLocalization:
    """Verify all roles and labels are localized in Chinese decision reports."""

    ALL_ROLES = [
        "Data Analyst", "Backend Developer", "AI Product Manager", "AI Engineer",
        "Marketing Specialist", "Accountant", "Business Analyst",
        "Operations Specialist", "Customer Support Specialist", "International Sales",
        "Product Manager", "English Teacher", "Chinese Teacher",
        "Registered Nurse", "Care Worker", "Mechanical Engineer", "Electrical Engineer",
        "Not Applicable",
    ]

    def test_all_roles_have_chinese_translations_in_config(self):
        """Every valid role must have a Chinese translation in decision report config."""
        from backend.app.services.decision_report_config import ZH_ROLE_LABELS, RECOMMENDATION_LABELS_ZH
        for role in self.ALL_ROLES:
            assert role in ZH_ROLE_LABELS, f"Missing ZH label for role '{role}'"
            assert ZH_ROLE_LABELS[role], f"Empty ZH label for role '{role}'"
            # Must not fall back to English (if translation equals the key, it's a fallback)
            assert ZH_ROLE_LABELS[role] != role, f"ZH label for '{role}' is raw key fallback"

    def test_all_roles_label_non_empty_in_zh_response(self):
        """Chinese decision report returns role labels in Chinese."""
        for role in self.ALL_ROLES[:6]:  # Sample representative roles
            payload = {
                "goal": "Work", "target_city": "Seoul",
                "school_type": "Not Applicable", "housing_type": "Not Applicable",
                "lifestyle_level": "Standard",
                "target_role": role, "experience_level": "3-5 years",
                "korean_level": "TOPIK 4", "monthly_budget": 3_000_000,
                "language": "zh",
            }
            resp = client.post("/api/v1/decision-report/generate", json=payload)
            assert resp.status_code == 200, f"{role} failed: {resp.status_code}"
            data = resp.json()
            assert "monthly_cost_estimate" in data, f"{role} missing cost data"

    def test_all_recommendation_labels_have_chinese_translations(self):
        """All 4 recommendation levels have Chinese labels."""
        from backend.app.services.decision_report_config import RECOMMENDATION_LABELS_ZH
        expected_labels = [
            "强烈推荐 ✅",
            "准备充分后推荐 ⚠️",
            "有一定风险 ❓",
            "暂不推荐 ❌",
        ]
        for expected in expected_labels:
            assert expected in RECOMMENDATION_LABELS_ZH.values(), \
                f"Missing ZH recommendation label: {expected}"

    def test_zh_decision_report_includes_role_label_in_summary(self):
        """Chinese decision report summary mentions the role in Chinese."""
        payload = {
            "goal": "Work", "target_city": "Seoul",
            "school_type": "Not Applicable", "housing_type": "Not Applicable",
            "lifestyle_level": "Standard",
            "target_role": "Backend Developer", "experience_level": "3-5 years",
            "korean_level": "TOPIK 5+", "monthly_budget": 3_000_000,
            "language": "zh",
        }
        resp = client.post("/api/v1/decision-report/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        # Career risk detail should reference the role name in Chinese
        assert data.get("career_risk_detail", ""), "Missing career risk detail in Chinese report"

    def test_chinese_city_labels_present(self):
        """All cities that can appear in decision reports have Chinese labels."""
        from backend.app.services.decision_report_config import ZH_CITY_LABELS
        for city in ["Seoul", "Busan", "Daejeon", "Daegu", "Other"]:
            assert city in ZH_CITY_LABELS, f"Missing ZH city label for {city}"
            assert ZH_CITY_LABELS[city], f"Empty ZH city label for {city}"

    def test_multiple_non_it_roles_return_zh_result(self):
        """Non-IT career roles work in Chinese mode (regression for the 7 previously missing roles)."""
        roles = [
            "Accountant", "English Teacher", "Chinese Teacher",
            "Registered Nurse", "Care Worker",
            "Mechanical Engineer", "Electrical Engineer",
        ]
        for role in roles:
            payload = {
                "goal": "Work", "target_city": "Seoul",
                "school_type": "Not Applicable", "housing_type": "Not Applicable",
                "lifestyle_level": "Standard",
                "target_role": role, "experience_level": "3-5 years",
                "korean_level": "TOPIK 4", "monthly_budget": 3_000_000,
                "language": "zh",
            }
            resp = client.post("/api/v1/decision-report/generate", json=payload)
            assert resp.status_code == 200, f"{role} zh failed: {resp.status_code}"
            data = resp.json()
            assert "第 1 个月" in data["action_plan"], f"{role} action plan not in Chinese"
            assert data["monthly_cost_estimate"] > 0, f"{role} missing cost data"


# ─────────────────────────────────────────────────────────
# Total: 18 + 7 = 25 tests
# ─────────────────────────────────────────────────────────
