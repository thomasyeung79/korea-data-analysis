import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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


def test_study_scenarios_chinese_situation_is_localized():
    data = korean_learning.get_study_scenarios(language="zh")
    classroom = next(item for item in data if item["scenario"] == "Classroom")

    assert "参加课堂" in classroom["situation"]
    assert "Joining class" not in classroom["situation"]


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


def test_korean_learning_study_api_chinese_query():
    response = client.get("/api/v1/korean-learning/study?language=zh")
    assert response.status_code == 200
    classroom = next(item for item in response.json() if item["scenario"] == "Classroom")
    assert "参加课堂" in classroom["situation"]
    assert "Joining class" not in classroom["situation"]


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


def test_korean_learning_expressions_bilingual():
    """Each expression should have ko / zh / en / romanization."""
    data = korean_learning.get_study_scenarios()
    for item in data:
        for expr in item.get("useful_expressions", []):
            assert "ko" in expr
            assert "zh" in expr
            assert "en" in expr
            assert "romanization" in expr
            break  # just check first scenario


def test_korean_learning_dialogues_bilingual():
    """Each dialogue line should have speaker / ko / zh / en / romanization."""
    data = korean_learning.get_living_scenarios()
    for item in data:
        for d in item.get("sample_dialogue", []):
            assert "ko" in d
            assert "zh" in d
            assert "en" in d
            assert "romanization" in d
            break


def test_korean_learning_vocabulary_bilingual():
    """Vocab should have korean / meaning / zh / note_zh / note_en."""
    data = korean_learning.get_study_scenarios()
    classroom = next(row for row in data if row["scenario"] == "Classroom")
    for v in classroom.get("vocabulary", []):
        assert "zh" in v
        assert "note_zh" in v
        assert "note_en" in v
        break


def test_korean_learning_chinese_expressions_show_zh():
    """Chinese mode should have zh in expressions."""
    data = korean_learning.get_study_scenarios(language="zh")
    classroom = next(row for row in data if row["scenario"] == "Classroom")
    for expr in classroom.get("useful_expressions", []):
        assert expr.get("zh", "") != ""


def test_korean_learning_english_expressions_show_en():
    """English mode should have en in expressions."""
    data = korean_learning.get_study_scenarios(language="en")
    classroom = next(row for row in data if row["scenario"] == "Classroom")
    for expr in classroom.get("useful_expressions", []):
        assert expr.get("en", "") != ""


def test_korean_learning_chinese_situation():
    data = korean_learning.get_study_scenarios(language="zh")
    classroom = next(row for row in data if row["scenario"] == "Classroom")
    assert "参加课堂" in classroom["situation"]
    assert "Joining class" not in classroom["situation"]


def test_korean_learning_career_chinese_tips():
    data = korean_learning.get_career_scenarios(language="zh")
    interview = next(row for row in data if row["scenario"] == "Interview")
    assert any("STAR" in tip for tip in interview["interview_tips"])


def test_korean_learning_living_chinese_culture():
    data = korean_learning.get_living_scenarios(language="zh")
    restaurant = next(row for row in data if row["scenario"] == "Restaurant")
    assert any("自助" in tip for tip in restaurant["culture_tips"])


def test_korean_learning_explain_bilingual():
    """Explain endpoint should return zh and en fields."""
    result = korean_learning.explain_expression(
        "다시 설명해 주실 수 있을까요?",
        action="grammar_notes",
        context="Study Korean - Classroom",
    )
    assert "explanation_zh" in result
    assert "explanation_en" in result
    assert "translation_zh" in result
    assert "grammar_notes_zh" in result
    assert "culture_notes_zh" in result
    assert result["grammar_notes_zh"]
    assert result["culture_notes_zh"]
