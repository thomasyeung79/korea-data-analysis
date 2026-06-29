from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import (
    KnowledgeBaseCity,
    KnowledgeBaseJob,
    KnowledgeBaseLiving,
    KnowledgeBaseUniversity,
    KnowledgeBaseVisa,
    StudyScenario,
)
from backend.app.services import data_loader, explore_service

client = TestClient(app)


def test_knowledge_base_file_count_and_directories():
    files = data_loader.list_knowledge_files()
    paths = {str(path).replace("\\", "/") for path in files}

    assert data_loader.kb_file_count() >= 40
    for directory in ["cities", "universities", "majors", "visa", "living", "jobs", "culture", "korean"]:
        assert any(f"/{directory}/" in path for path in paths), f"Missing KB directory: {directory}"


def test_load_city_schema_and_single_lookup():
    seoul = data_loader.load_city("Seoul")
    parsed = KnowledgeBaseCity(**seoul)

    assert parsed.city_name == "Seoul"
    assert parsed.average_rent > 0
    assert "Technology" in parsed.major_industries


def test_load_university_schema():
    universities = data_loader.load_university()
    parsed = [KnowledgeBaseUniversity(**item) for item in universities]

    assert len(parsed) >= 4
    assert any(item.name == "KAIST" for item in parsed)
    assert all(item.website.startswith("https://") for item in parsed)


def test_load_visa_schema():
    visa = data_loader.load_visa("E-7")
    parsed = KnowledgeBaseVisa(**visa)

    assert parsed.visa_type == "E-7"
    assert parsed.eligibility
    assert parsed.documents


def test_load_living_and_job_schema():
    housing = KnowledgeBaseLiving(**data_loader.load_living("housing"))
    job = KnowledgeBaseJob(**data_loader.load_job("IT"))

    assert housing.typical_costs["studio"] > housing.typical_costs["dormitory"]
    assert "Python" in job.popular_skills
    assert "Seoul" in job.recommended_regions


def test_load_learning_uses_korean_directory():
    study = data_loader.load_learning("study")
    parsed = [StudyScenario(**item) for item in study]

    assert len(parsed) >= 6
    assert parsed[0].scenario == "Classroom"


def test_explore_service_reads_city_knowledge_base():
    cities = explore_service.get_cities()
    seoul = cities[0]

    assert seoul["name"] == "Seoul"
    assert seoul["study_score"] == data_loader.load_city("Seoul")["study_score"]
    assert "Top universities" in seoul["best_for"]


def test_explore_api_uses_knowledge_base_city_data():
    response = client.get("/api/v1/explore/cities")
    assert response.status_code == 200
    data = response.json()

    assert data[0]["name"] == "Seoul"
    assert any(item["name"] == "Jeju" for item in data)


def test_study_cost_supports_kb_city_not_in_legacy_constants():
    response = client.post(
        "/api/v1/study-cost/calculate",
        json={
            "city": "Jeju",
            "school_type": "Undergraduate",
            "housing_type": "Shared Apartment",
            "lifestyle_level": "Standard",
        },
    )
    assert response.status_code == 200
    assert response.json()["monthly_cost"] > 0


def test_job_database_available_for_career_service_context():
    jobs = data_loader.load_job()
    industries = {item["industry"] for item in jobs}

    assert {"IT", "Engineering", "Business", "Education", "Design", "Marketing", "Healthcare"} <= industries
