import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.database import Base, get_db
from backend.app.main import app


@pytest.fixture()
def client(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'community.db'}",
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


def submit(client, scores, comment=None, display_name="Community Test"):
    payload = {
        "display_name": display_name,
        "economy_score": scores[0],
        "technology_score": scores[1],
        "education_score": scores[2],
        "culture_score": scores[3],
        "global_influence_score": scores[4],
        "quality_of_life_score": scores[5],
        "comment": comment,
    }
    response = client.post("/api/v1/perception-surveys", json=payload)
    assert response.status_code == 200


def test_community_summary_empty_database(client):
    response = client.get("/api/v1/perception-surveys/community-summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_responses"] == 0
    assert data["average_score"] == 0.0
    assert all(value == 0.0 for value in data["category_averages"].values())
    assert data["recent_comments"] == []
    assert all(value == 0 for value in data["profile_distribution"].values())


def test_community_summary_one_survey(client):
    submit(client, [5, 5, 5, 5, 5, 5], comment="  First voice  ")
    data = client.get("/api/v1/perception-surveys/community-summary").json()

    assert data["total_responses"] == 1
    assert data["average_score"] == 5.0
    assert data["category_averages"]["economy"] == 5.0
    assert data["strongest_category"] == "economy"
    assert data["weakest_category"] == "economy"
    assert data["profile_distribution"]["Balanced Regional Observer"] == 1
    assert data["recent_comments"] == ["First voice"]


def test_community_summary_multiple_surveys(client):
    submit(client, [8, 8, 6, 6, 6, 6], comment="Market view")
    submit(client, [6, 6, 6, 9, 9, 6], comment="  Culture view  ")
    submit(client, [6, 9, 6, 6, 6, 6], comment="")
    submit(client, [5, 5, 5, 5, 5, 4], comment="   ")
    submit(client, [6, 6, 6, 6, 6, 6], comment="Balanced view")

    response = client.get("/api/v1/perception-surveys/community-summary")
    assert response.status_code == 200
    data = response.json()

    assert data["total_responses"] == 5
    assert data["average_score"] == 6.2
    assert data["category_averages"] == {
        "economy": 6.2,
        "technology": 6.8,
        "education": 5.8,
        "culture": 6.4,
        "global_influence": 6.4,
        "quality_of_life": 5.6,
    }
    assert data["strongest_category"] == "technology"
    assert data["weakest_category"] == "quality_of_life"
    assert data["profile_distribution"] == {
        "Soft Power Enthusiast": 1,
        "Technology-Focused Analyst": 1,
        "Market-Driven Pragmatist": 1,
        "Balanced Regional Observer": 1,
        "Quality-of-Life Skeptic": 1,
    }
    assert data["recent_comments"] == [
        "Balanced view",
        "Culture view",
        "Market view",
    ]
