import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.main import app
from backend.app.services.mbti_city_match import SUPPORTED_MBTI, match_mbti_city

client = TestClient(app)


def payload(mbti_type="INFJ", language="en"):
    return {
        "mbti_type": mbti_type,
        "social_energy": "Medium",
        "lifestyle_preference": "Balanced",
        "pace_preference": "Moderate",
        "budget_sensitivity": "Medium",
        "career_priority": 6,
        "study_priority": 6,
        "language": language,
    }


def test_mbti_city_match_api_returns_city_scores():
    response = client.post("/api/v1/living/mbti-city-match", json=payload("ENFP"))
    assert response.status_code == 200
    data = response.json()

    assert data["best_city"]
    assert len(data["city_scores"]) >= 7
    assert "personality_fit_score" in data
    assert "potential_challenges" in data


def test_all_16_mbti_types_are_supported():
    for mbti_type in SUPPORTED_MBTI:
        result = match_mbti_city(payload(mbti_type))
        assert result["best_city"]
        assert len(result["city_scores"]) == 7


def test_chinese_mbti_city_match_returns_chinese_reason():
    result = match_mbti_city(payload("INFJ", language="zh"))

    assert "匹配" in result["recommendation_reason"]
    assert result["suggested_living_style"]
    assert any("预算" in challenge or "风险" in challenge or "短住" in challenge for challenge in result["potential_challenges"])


def test_mbti_city_match_invalid_type_falls_back_safely():
    response = client.post("/api/v1/living/mbti-city-match", json=payload("XXXX"))

    assert response.status_code == 200
    assert response.json()["best_city"]
