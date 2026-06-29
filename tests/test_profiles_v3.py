from fastapi.testclient import TestClient

from backend.app.database import Base, engine
from backend.app.main import app

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
