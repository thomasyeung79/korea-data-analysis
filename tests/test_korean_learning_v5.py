from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import (
    CareerScenario,
    ExpressionExplanation,
    LivingScenario,
    StudyScenario,
    TOPIKPlanner,
)
from backend.app.services import korean_learning

client = TestClient(app)


def test_study_scenarios_service_and_schema():
    data = korean_learning.get_study_scenarios()
    parsed = [StudyScenario(**item) for item in data]
    scenarios = {item.scenario for item in parsed}

    assert {"Classroom", "Professor", "Library", "Dormitory", "Campus", "Presentation"} <= scenarios
    assert parsed[0].useful_expressions
    assert parsed[0].vocabulary[0].korean


def test_career_scenarios_service_and_schema():
    data = korean_learning.get_career_scenarios()
    parsed = [CareerScenario(**item) for item in data]
    scenarios = {item.scenario for item in parsed}

    assert {"Interview", "Resume", "Office", "Meeting", "Email", "Business Phone"} <= scenarios
    assert parsed[0].interview_tips
    assert parsed[0].business_vocabulary


def test_living_scenarios_service_and_schema():
    data = korean_learning.get_living_scenarios()
    parsed = [LivingScenario(**item) for item in data]
    scenarios = {item.scenario for item in parsed}

    assert {"Restaurant", "Convenience Store", "Hospital", "Pharmacy", "Bank", "Apartment", "Subway", "Taxi"} <= scenarios
    assert parsed[0].common_questions
    assert parsed[0].culture_tips


def test_topik_planner_service_and_schema():
    data = korean_learning.get_topik_planners()
    parsed = [TOPIKPlanner(**item) for item in data]

    assert len(parsed) >= 5
    assert any(item.target_level == "TOPIK 4" for item in parsed)
    assert all(item.weekly_study_plan for item in parsed)


def test_expression_explanation_service_and_schema():
    result = korean_learning.explain_expression(
        "다시 설명해 주실 수 있을까요?",
        action="grammar_notes",
        context="Study Korean - Classroom",
    )
    parsed = ExpressionExplanation(**result)

    assert parsed.expression == "다시 설명해 주실 수 있을까요?"
    assert parsed.grammar_notes
    assert any("polite" in note.lower() for note in parsed.grammar_notes)
    assert parsed.culture_notes


def test_korean_learning_study_api():
    response = client.get("/api/v1/korean-learning/study")
    assert response.status_code == 200
    assert len(response.json()) >= 6
    assert response.json()[0]["scenario"] == "Classroom"


def test_korean_learning_career_api():
    response = client.get("/api/v1/korean-learning/career")
    assert response.status_code == 200
    scenarios = {item["scenario"] for item in response.json()}
    assert "Interview" in scenarios
    assert "Business Phone" in scenarios


def test_korean_learning_living_api():
    response = client.get("/api/v1/korean-learning/living")
    assert response.status_code == 200
    scenarios = {item["scenario"] for item in response.json()}
    assert "Restaurant" in scenarios
    assert "Taxi" in scenarios


def test_korean_learning_topik_api():
    response = client.get("/api/v1/korean-learning/topik")
    assert response.status_code == 200
    assert any(item["target_level"] == "TOPIK 5+" for item in response.json())


def test_korean_learning_explain_api():
    response = client.post(
        "/api/v1/korean-learning/explain",
        json={
            "expression": "계좌를 개설하고 싶습니다.",
            "action": "explain_expression",
            "context": "Living Korean - Bank",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["translation"] == "I would like to open a bank account."
    assert data["natural_rewrite"]
    assert data["grammar_notes"]
