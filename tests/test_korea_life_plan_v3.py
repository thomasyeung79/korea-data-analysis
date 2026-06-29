from fastapi.testclient import TestClient

from backend.app.database import Base, engine
from backend.app.main import app

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def payload(language="en"):
    return {
        "display_name": "Compass Tester",
        "language": language,
        "study_profile": {
            "nationality": "International",
            "age": 25,
            "current_education_level": "Undergraduate",
            "target_study_level": "Graduate School",
            "target_major": "Data Science",
            "korean_level": "TOPIK 3",
            "english_level": "Advanced",
            "annual_budget": 24_000_000,
            "preferred_city": "Seoul",
        },
        "career_profile": {
            "target_role": "Data Analyst",
            "work_experience": "0-2 years",
            "technical_skills": ["SQL", "Python"],
            "korean_level": "TOPIK 3",
            "english_level": "Advanced",
            "target_industry": "Technology",
            "visa_goal": "D-10",
        },
        "living_profile": {
            "lifestyle": "Standard",
            "housing_preference": "Shared Apartment",
            "monthly_budget": 1_600_000,
            "preferred_city": "Busan",
            "transport_preference": "Public Transit",
            "community_preference": "International Community",
        },
    }


def test_korea_life_plan_generate_contains_required_sections():
    response = client.post("/api/v1/korea-life-plan/generate", json=payload())
    assert response.status_code == 200
    data = response.json()
    for field in [
        "overall_recommendation",
        "best_city",
        "study_path",
        "career_path",
        "living_plan",
        "estimated_annual_study_cost",
        "estimated_monthly_living_cost",
        "budget_gap",
        "language_risk",
        "career_risk",
        "living_risk",
        "visa_pathway",
        "action_plan_3_month",
        "action_plan_6_month",
        "action_plan_12_month",
        "city_recommendations",
        "markdown_report",
    ]:
        assert field in data


def test_korea_life_plan_chinese_output_uses_chinese_headings():
    response = client.post("/api/v1/korea-life-plan/generate", json=payload(language="zh"))
    assert response.status_code == 200
    data = response.json()
    assert "留学路径" in data["markdown_report"]
    assert "职业路径" in data["markdown_report"]
    assert "行动计划" in data["markdown_report"]


def test_korea_life_plan_history_created_after_generation():
    client.post("/api/v1/korea-life-plan/generate", json=payload())
    response = client.get("/api/v1/korea-life-plan/history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["display_name"] == "Compass Tester"
