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
        "mbti_city_fit",
        "language_learning_plan",
        "budget_analysis",
        "risk_summary",
        "confidence_summary",
        "based_on_available_inputs",
    ]:
        assert field in data


def test_korea_life_plan_chinese_output_uses_chinese_headings():
    response = client.post("/api/v1/korea-life-plan/generate", json=payload(language="zh"))
    assert response.status_code == 200
    data = response.json()
    assert "留学路径" in data["markdown_report"]
    assert "职业路径" in data["markdown_report"]
    assert "行动计划" in data["markdown_report"]
    assert "Data confidence summary" in data["markdown_report"]


def test_korea_life_plan_integrates_city_mbti_and_language_inputs():
    request = payload()
    request["topik_goal"] = "TOPIK 5+"
    request["city_recommendation"] = {
        "best_city": "Daejeon",
        "rankings": [
            {
                "city": "Daejeon",
                "total_score": 91,
                "study_score": 90,
                "career_score": 88,
                "living_score": 86,
                "cost_score": 82,
                "language_fit_score": 74,
                "lifestyle_score": 80,
                "recommendation_reason": "Daejeon has strong study and research fit.",
            }
        ],
    }
    request["mbti_city_match"] = {
        "best_city": "Jeju",
        "city_scores": [],
        "personality_fit_score": 88,
        "lifestyle_fit_score": 90,
        "social_fit_score": 78,
        "career_environment_score": 52,
        "study_environment_score": 58,
        "recommendation_reason": "Jeju fits quiet living.",
        "potential_challenges": ["Lower career density."],
        "suggested_living_style": "Choose a quiet neighborhood.",
    }

    response = client.post("/api/v1/korea-life-plan/generate", json=request)
    assert response.status_code == 200
    data = response.json()

    assert data["best_city"] == "Daejeon"
    assert "Jeju" in data["mbti_city_fit"]
    assert "TOPIK 5+" in data["language_learning_plan"]
    assert "Data confidence summary" in data["confidence_summary"]
    assert "City Recommendation" in data["based_on_available_inputs"]
    assert "MBTI City Match" in data["based_on_available_inputs"]


def test_korea_life_plan_handles_missing_integrated_inputs():
    response = client.post("/api/v1/korea-life-plan/generate", json=payload())
    assert response.status_code == 200
    data = response.json()

    assert data["best_city"]
    assert any("missing" in item.lower() or "inferred" in item.lower() for item in data["based_on_available_inputs"])


def test_korea_life_plan_history_created_after_generation():
    client.post("/api/v1/korea-life-plan/generate", json=payload())
    response = client.get("/api/v1/korea-life-plan/history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["display_name"] == "Compass Tester"
