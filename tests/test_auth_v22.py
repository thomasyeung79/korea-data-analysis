import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.database import Base, SessionLocal, engine
from backend.app.main import app
from backend.app.models import CityRecommendationHistory, KoreaLifePlanHistory, UserProfile

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def user_payload(email="tester@example.com"):
    return {
        "email": email,
        "display_name": "Auth Tester",
        "password": "strongpass123",
    }


def profile_payload(display_name="Profile Owner"):
    return {
        "display_name": display_name,
        "study_profile": {
            "nationality": "International",
            "age": 22,
            "current_education_level": "Undergraduate",
            "target_study_level": "Graduate School",
            "target_major": "Computer Science",
            "korean_level": "TOPIK 3",
            "english_level": "Intermediate",
            "annual_budget": 20_000_000,
            "preferred_city": "Seoul",
        },
        "career_profile": {
            "target_role": "Data Analyst",
            "work_experience": "0-2 years",
            "technical_skills": ["SQL"],
            "korean_level": "TOPIK 3",
            "english_level": "Intermediate",
            "target_industry": "Technology",
            "visa_goal": "D-10",
        },
        "living_profile": {
            "lifestyle": "Standard",
            "housing_preference": "Shared Apartment",
            "monthly_budget": 1_500_000,
            "preferred_city": "Seoul",
            "transport_preference": "Public Transit",
            "community_preference": "International Community",
        },
    }


def register_user(email="tester@example.com"):
    response = client.post("/api/v1/auth/register", json=user_payload(email))
    assert response.status_code == 200
    return response.json()


def test_register_success():
    data = register_user()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "tester@example.com"
    assert "password_hash" not in data["user"]


def test_duplicate_email_rejected():
    register_user()
    response = client.post("/api/v1/auth/register", json=user_payload())
    assert response.status_code == 409


def test_login_success():
    register_user()
    response = client.post("/api/v1/auth/login", json={"email": "tester@example.com", "password": "strongpass123"})
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_wrong_password_rejected():
    register_user()
    response = client.post("/api/v1/auth/login", json={"email": "tester@example.com", "password": "wrong"})
    assert response.status_code == 401


def test_auth_me_with_token():
    token = register_user()["access_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["display_name"] == "Auth Tester"


def test_auth_me_without_token_rejected():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_profile_can_bind_user_id():
    token = register_user()["access_token"]
    response = client.post(
        "/api/v1/profiles",
        json=profile_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    db = SessionLocal()
    try:
        record = db.query(UserProfile).first()
        assert record.user_id == 1
    finally:
        db.close()


def test_demo_mode_profile_still_works_without_login():
    response = client.post("/api/v1/profiles", json=profile_payload("Demo User"))
    assert response.status_code == 200
    assert response.json()["display_name"] == "Demo User"

    db = SessionLocal()
    try:
        record = db.query(UserProfile).first()
        assert record.user_id is None
    finally:
        db.close()


def test_city_recommendation_and_life_plan_bind_user_id_when_logged_in():
    token = register_user()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    profile = profile_payload()

    city_response = client.post(
        "/api/v1/city-recommendations",
        json={
            "study_profile": profile["study_profile"],
            "career_profile": profile["career_profile"],
            "living_profile": profile["living_profile"],
            "language": "en",
        },
        headers=headers,
    )
    assert city_response.status_code == 200

    plan_response = client.post("/api/v1/korea-life-plan/generate", json={**profile, "language": "en"}, headers=headers)
    assert plan_response.status_code == 200

    db = SessionLocal()
    try:
        city_record = db.query(CityRecommendationHistory).first()
        plan_record = db.query(KoreaLifePlanHistory).first()
        assert city_record.user_id == 1
        assert plan_record.user_id == 1
    finally:
        db.close()
