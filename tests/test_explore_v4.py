from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import CityInfo, CultureSection, ExploreOverview, HistoryEvent, LivingCost, QuickFact
from backend.app.services import explore_service

client = TestClient(app)


def test_explore_overview_service_and_schema():
    data = explore_service.get_overview()
    parsed = ExploreOverview(**data)

    assert parsed.capital == "Seoul"
    assert "KRW" in parsed.currency
    assert parsed.language == "Korean"


def test_explore_cities_service_has_required_cities_and_schema():
    cities = explore_service.get_cities()
    parsed = [CityInfo(**city) for city in cities]
    names = {city.name for city in parsed}

    assert {"Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Jeju"} <= names
    assert all(city.study_score >= 0 for city in parsed)
    assert all(city.best_for for city in parsed)


def test_explore_culture_history_living_quick_fact_schemas():
    culture = [CultureSection(**item) for item in explore_service.get_culture()]
    history = [HistoryEvent(**item) for item in explore_service.get_history()]
    living = [LivingCost(**item) for item in explore_service.get_living_cost()]
    facts = [QuickFact(**item) for item in explore_service.get_quick_facts()]

    assert len(culture) >= 6
    assert len(history) >= 6
    assert len(living) >= 7
    assert len(facts) >= 7
    assert any(item.period == "Joseon" for item in history)
    assert any(item.city == "Seoul" and item.rent > 0 for item in living)
    assert any(item.title == "Emergency Numbers" for item in facts)


def test_explore_overview_api():
    response = client.get("/api/v1/explore/overview")
    assert response.status_code == 200
    assert response.json()["capital"] == "Seoul"


def test_explore_cities_api():
    response = client.get("/api/v1/explore/cities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 7
    assert data[0]["name"] == "Seoul"


def test_explore_culture_api():
    response = client.get("/api/v1/explore/culture")
    assert response.status_code == 200
    titles = {item["title"] for item in response.json()}
    assert "Etiquette" in titles
    assert "Workplace Culture" in titles


def test_explore_history_api():
    response = client.get("/api/v1/explore/history")
    assert response.status_code == 200
    periods = {item["period"] for item in response.json()}
    assert "Three Kingdoms" in periods
    assert "Modern Korea" in periods


def test_explore_living_cost_api():
    response = client.get("/api/v1/explore/living-cost")
    assert response.status_code == 200
    seoul = next(item for item in response.json() if item["city"] == "Seoul")
    assert seoul["rent"] > seoul["mobile"]


def test_explore_quick_facts_api():
    response = client.get("/api/v1/explore/quick-facts")
    assert response.status_code == 200
    facts = {item["title"] for item in response.json()}
    assert "Visa Types" in facts
    assert "Healthcare" in facts
