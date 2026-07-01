import sys
import json
from pathlib import Path

from fastapi.testclient import TestClient
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.database import Base, engine
from backend.app.main import app
import locales.i18n as i18n

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def sample_profile():
    return {
        "display_name": "V3 Tester",
        "study_profile": {
            "nationality": "Canada",
            "age": 24,
            "current_education_level": "Undergraduate",
            "target_study_level": "Graduate School",
            "target_major": "Business Analytics",
            "korean_level": "TOPIK 3",
            "english_level": "Advanced",
            "annual_budget": 25_000_000,
            "preferred_city": "Seoul",
        },
        "career_profile": {
            "target_role": "Business Analyst",
            "work_experience": "0-2 years",
            "technical_skills": ["SQL", "Excel"],
            "korean_level": "TOPIK 3",
            "english_level": "Advanced",
            "target_industry": "Business",
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


def test_create_profile_persists_three_profile_sections():
    response = client.post("/api/v1/profiles", json=sample_profile())
    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "V3 Tester"
    assert data["study_profile"]["target_major"] == "Business Analytics"
    assert data["career_profile"]["target_role"] == "Business Analyst"
    assert data["living_profile"]["preferred_city"] == "Busan"


def test_latest_profile_returns_most_recent_profile():
    client.post("/api/v1/profiles", json=sample_profile())
    updated = sample_profile()
    updated["display_name"] = "Latest User"
    client.post("/api/v1/profiles", json=updated)

    response = client.get("/api/v1/profiles/latest")
    assert response.status_code == 200
    assert response.json()["display_name"] == "Latest User"


def test_profile_summary_localizes_chinese_values(monkeypatch):
    monkeypatch.setattr(i18n, "st", SimpleNamespace(session_state={}))
    i18n.set_language("zh")
    profile = sample_profile()
    profile["display_name"] = "Compass User"
    profile["study_profile"].update({
        "nationality": "International",
        "current_education_level": "High School",
        "target_study_level": "Language School",
        "target_major": "Computer Science",
        "korean_level": "None",
        "english_level": "Basic",
        "preferred_city": "Seoul",
    })
    profile["career_profile"].update({
        "target_role": "Data Analyst",
        "work_experience": "Student",
        "target_industry": "Technology",
        "visa_goal": "D-2",
    })
    profile["living_profile"].update({
        "lifestyle": "Budget",
        "housing_preference": "Dormitory",
        "transport_preference": "Public Transit",
        "community_preference": "Student Area",
    })

    summary = i18n.profile_summary(profile)
    flat_values = [value for rows in summary.values() for _, value in rows]

    assert "国际学生" in flat_values
    assert "高中" in flat_values
    assert "语言学校" in flat_values
    assert "计算机科学" in flat_values
    assert "无" in flat_values
    assert "首尔" in flat_values
    assert "数据分析师" in flat_values
    assert "学生" in flat_values
    assert "科技" in flat_values
    assert "宿舍" in flat_values


def test_profile_summary_english_mode_stays_english(monkeypatch):
    monkeypatch.setattr(i18n, "st", SimpleNamespace(session_state={}))
    i18n.set_language("en")

    summary = i18n.profile_summary(sample_profile())
    flat_values = [value for rows in summary.values() for _, value in rows]

    assert "Business Analyst" in flat_values
    assert "Graduate School" in flat_values
    assert "Busan" in flat_values


def test_translate_profile_json_localizes_chinese_display_values(monkeypatch):
    monkeypatch.setattr(i18n, "st", SimpleNamespace(session_state={}))
    i18n.set_language("zh")
    profile = sample_profile()
    profile["display_name"] = "Compass User"
    profile["study_profile"].update({
        "nationality": "International",
        "current_education_level": "High School",
        "target_study_level": "Language School",
        "target_major": "Computer Science",
        "korean_level": "None",
        "english_level": "Basic",
        "preferred_city": "Seoul",
    })
    profile["career_profile"].update({
        "target_role": "Data Analyst",
        "work_experience": "Student",
        "technical_skills": ["SQL", "Python"],
        "target_industry": "Technology",
    })
    profile["living_profile"].update({
        "lifestyle": "Budget",
        "housing_preference": "Dormitory",
        "transport_preference": "Public Transport",
        "community_preference": "Student Community",
    })

    display_profile = i18n.translate_profile_json(profile, "zh")
    rendered = json.dumps(display_profile, ensure_ascii=False)

    assert display_profile["display_name"] == "韩国指南用户"
    assert display_profile["study_profile"]["nationality"] == "国际学生"
    assert display_profile["study_profile"]["current_education_level"] == "高中"
    assert display_profile["study_profile"]["target_study_level"] == "语言学校"
    assert display_profile["study_profile"]["target_major"] == "计算机科学"
    assert display_profile["study_profile"]["korean_level"] == "无"
    assert display_profile["study_profile"]["english_level"] == "基础"
    assert display_profile["study_profile"]["preferred_city"] == "首尔"
    assert display_profile["career_profile"]["target_role"] == "数据分析师"
    assert display_profile["career_profile"]["work_experience"] == "学生"
    assert display_profile["career_profile"]["target_industry"] == "科技"
    assert display_profile["living_profile"]["lifestyle"] == "预算型"
    assert display_profile["living_profile"]["housing_preference"] == "宿舍"
    assert display_profile["living_profile"]["transport_preference"] == "公共交通"
    assert display_profile["living_profile"]["community_preference"] == "学生社区"

    assert "High School" not in rendered
    assert "Computer Science" not in rendered
    assert "International" not in rendered
    assert "SQL" in rendered
    assert "Python" in rendered
    assert "TOPIK 3" in rendered


def test_translate_profile_json_english_mode_keeps_raw_values(monkeypatch):
    monkeypatch.setattr(i18n, "st", SimpleNamespace(session_state={}))
    i18n.set_language("en")
    profile = sample_profile()

    display_profile = i18n.translate_profile_json(profile, "en")

    assert display_profile == profile
    assert display_profile is not profile
