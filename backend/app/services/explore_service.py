from __future__ import annotations

from . import data_loader

CITY_ORDER = {"Seoul": 0, "Busan": 1, "Incheon": 2, "Daegu": 3, "Daejeon": 4, "Gwangju": 5, "Jeju": 6}


def get_overview() -> dict:
    return {
        "country_introduction": (
            "South Korea is a highly connected East Asian country known for advanced technology, "
            "dense cities, strong education infrastructure, pop culture, food, and fast public transport."
        ),
        "population": "About 51.7 million",
        "area": "About 100,400 km2",
        "capital": "Seoul",
        "currency": "South Korean won (KRW)",
        "time_zone": "Korea Standard Time (UTC+9)",
        "language": "Korean",
        "climate": "Four distinct seasons with hot humid summers and cold dry winters.",
    }


def get_cities() -> list[dict]:
    cities = sorted(data_loader.load_city(), key=lambda city: CITY_ORDER.get(city["city_name"], 99))
    return [
        {
            "name": city["city_name"],
            "population": city["population"],
            "living_cost": _living_cost_label(city["average_rent"]),
            "study_score": city["study_score"],
            "career_score": city["career_score"],
            "lifestyle_score": city["living_score"],
            "short_description": city["description"],
            "best_for": city["recommended_for"],
        }
        for city in cities
    ]


def get_culture() -> list[dict]:
    return data_loader.load_culture("overview")["sections"]


def get_history() -> list[dict]:
    return data_loader.load_culture("history")["events"]


def get_living_cost() -> list[dict]:
    cities = sorted(data_loader.load_city(), key=lambda city: CITY_ORDER.get(city["city_name"], 99))
    return [
        {
            "city": city["city_name"],
            "rent": city["average_rent"],
            "food": city["average_food_cost"],
            "transportation": city["transport_cost"],
            "mobile": 55000,
            "utilities": 120000 if city["city_name"] != "Seoul" else 130000,
            "entertainment": 180000 if city["city_name"] != "Seoul" else 220000,
        }
        for city in cities
    ]


def get_quick_facts() -> list[dict]:
    return data_loader.load_culture("quick_facts")["facts"]


def _living_cost_label(average_rent: float) -> str:
    if average_rent >= 700000:
        return "Very high"
    if average_rent >= 580000:
        return "Medium-high"
    if average_rent >= 500000:
        return "Medium"
    return "Medium-low"
