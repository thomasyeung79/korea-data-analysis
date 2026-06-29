from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def profile_payload(language="en"):
    return {
        "language": language,
        "study_profile": {
            "nationality": "International",
            "age": 23,
            "current_education_level": "Undergraduate",
            "target_study_level": "Graduate School",
            "target_major": "Computer Science",
            "korean_level": "TOPIK 4",
            "english_level": "Advanced",
            "annual_budget": 24_000_000,
            "preferred_city": "Daejeon",
        },
        "career_profile": {
            "target_role": "AI Engineer",
            "work_experience": "0-2 years",
            "technical_skills": ["Python", "SQL"],
            "korean_level": "TOPIK 4",
            "english_level": "Advanced",
            "target_industry": "Technology",
            "visa_goal": "E-7",
        },
        "living_profile": {
            "lifestyle": "Standard",
            "housing_preference": "Shared Apartment",
            "monthly_budget": 1_700_000,
            "preferred_city": "Busan",
            "transport_preference": "Public Transit",
            "community_preference": "International Community",
        },
    }


def test_city_recommendation_returns_ranked_scores():
    response = client.post("/api/v1/city-recommendations", json=profile_payload())
    assert response.status_code == 200
    data = response.json()
    assert data["best_city"]
    assert len(data["rankings"]) >= 7
    scores = [row["total_score"] for row in data["rankings"]]
    assert scores == sorted(scores, reverse=True)
    for field in [
        "study_score",
        "career_score",
        "living_score",
        "cost_score",
        "language_fit_score",
        "lifestyle_score",
        "recommendation_reason",
    ]:
        assert field in data["rankings"][0]


def test_city_recommendation_supports_chinese_reasons():
    response = client.post("/api/v1/city-recommendations", json=profile_payload(language="zh"))
    assert response.status_code == 200
    reason = response.json()["rankings"][0]["recommendation_reason"]
    assert "留学" in reason
    assert "职业" in reason
