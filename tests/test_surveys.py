import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.database import Base, get_db
from backend.app.main import app
from backend.app.schemas import PerceptionSurveyCreate


@pytest.fixture()
def client(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_survey_create_schema_validation():
    valid = PerceptionSurveyCreate(
        display_name="",
        economy_score=5,
        technology_score=5,
        education_score=5,
        culture_score=5,
        global_influence_score=5,
        quality_of_life_score=5,
    )
    assert valid.display_name == "Anonymous"

    with pytest.raises(ValidationError):
        PerceptionSurveyCreate(
            economy_score=0,
            technology_score=5,
            education_score=5,
            culture_score=5,
            global_influence_score=5,
            quality_of_life_score=5,
        )


def test_get_stats_empty(client):
    response = client.get("/api/v1/perception-surveys/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_submissions"] == 0
    assert data["average_score"] is None
    assert data["average_by_category"] == {}
    assert data["korea_baseline"]["Technology"] == 9.0


def test_post_survey(client):
    response = client.post(
        "/api/v1/perception-surveys",
        json={
            "display_name": "Alex",
            "economy_score": 6,
            "technology_score": 9,
            "education_score": 7,
            "culture_score": 8,
            "global_influence_score": 8,
            "quality_of_life_score": 6,
            "comment": "Travel and media shaped my view.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] >= 1
    assert data["display_name"] == "Alex"
    assert data["technology_score"] == 9


def test_get_stats_with_data(client):
    client.post(
        "/api/v1/perception-surveys",
        json={
            "display_name": "A",
            "economy_score": 6,
            "technology_score": 9,
            "education_score": 7,
            "culture_score": 8,
            "global_influence_score": 8,
            "quality_of_life_score": 6,
        },
    )
    client.post(
        "/api/v1/perception-surveys",
        json={
            "display_name": "B",
            "economy_score": 8,
            "technology_score": 10,
            "education_score": 8,
            "culture_score": 9,
            "global_influence_score": 7,
            "quality_of_life_score": 7,
        },
    )

    response = client.get("/api/v1/perception-surveys/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_submissions"] == 2
    assert data["average_score"] == 7.75
    assert data["average_by_category"]["Technology"] == 9.5
    assert data["strongest_category"] == "Technology"
    assert data["weakest_category"] == "Quality of Life"
