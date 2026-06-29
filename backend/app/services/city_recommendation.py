from __future__ import annotations

from typing import Any


CITIES = ["Seoul", "Busan", "Incheon", "Daejeon", "Daegu", "Gwangju", "Other"]

CITY_TRAITS = {
    "Seoul": {
        "study": 94,
        "career": 96,
        "living": 78,
        "cost": 52,
        "international": 95,
        "tech": 96,
        "business": 95,
        "education": 88,
        "healthcare": 88,
        "engineering": 72,
        "quiet": 48,
    },
    "Busan": {
        "study": 82,
        "career": 76,
        "living": 86,
        "cost": 76,
        "international": 78,
        "tech": 72,
        "business": 76,
        "education": 80,
        "healthcare": 82,
        "engineering": 84,
        "quiet": 70,
    },
    "Incheon": {
        "study": 76,
        "career": 78,
        "living": 82,
        "cost": 78,
        "international": 84,
        "tech": 72,
        "business": 82,
        "education": 76,
        "healthcare": 76,
        "engineering": 78,
        "quiet": 68,
    },
    "Daejeon": {
        "study": 88,
        "career": 82,
        "living": 84,
        "cost": 82,
        "international": 68,
        "tech": 88,
        "business": 66,
        "education": 86,
        "healthcare": 78,
        "engineering": 86,
        "quiet": 82,
    },
    "Daegu": {
        "study": 74,
        "career": 68,
        "living": 80,
        "cost": 86,
        "international": 58,
        "tech": 62,
        "business": 70,
        "education": 76,
        "healthcare": 80,
        "engineering": 74,
        "quiet": 78,
    },
    "Gwangju": {
        "study": 72,
        "career": 62,
        "living": 82,
        "cost": 88,
        "international": 54,
        "tech": 58,
        "business": 62,
        "education": 74,
        "healthcare": 78,
        "engineering": 68,
        "quiet": 84,
    },
    "Other": {
        "study": 60,
        "career": 58,
        "living": 76,
        "cost": 90,
        "international": 42,
        "tech": 54,
        "business": 56,
        "education": 62,
        "healthcare": 70,
        "engineering": 70,
        "quiet": 86,
    },
}

ROLE_INDUSTRY = {
    "Data Analyst": "tech",
    "Backend Developer": "tech",
    "AI Product Manager": "tech",
    "AI Engineer": "tech",
    "Marketing Specialist": "business",
    "Accountant": "business",
    "Business Analyst": "business",
    "Operations Specialist": "business",
    "Customer Support Specialist": "business",
    "International Sales": "business",
    "Product Manager": "business",
    "English Teacher": "education",
    "Chinese Teacher": "education",
    "Registered Nurse": "healthcare",
    "Care Worker": "healthcare",
    "Mechanical Engineer": "engineering",
    "Electrical Engineer": "engineering",
}

KOREAN_LEVEL_SCORE = {"None": 45, "TOPIK 3": 68, "TOPIK 4": 82, "TOPIK 5+": 94}
ZH_CITY_LABELS = {
    "Seoul": "首尔",
    "Busan": "釜山",
    "Incheon": "仁川",
    "Daejeon": "大田",
    "Daegu": "大邱",
    "Gwangju": "光州",
    "Other": "其他城市",
}


def _dump(value: Any) -> dict:
    return value.model_dump() if hasattr(value, "model_dump") else dict(value or {})


def _budget_score(monthly_budget: float, city_cost: int) -> float:
    if monthly_budget <= 0:
        return 35
    ratio = monthly_budget / city_cost
    if ratio >= 1.35:
        return 95
    if ratio >= 1.1:
        return 84
    if ratio >= 0.9:
        return 68
    if ratio >= 0.75:
        return 52
    return 36


def _reason(city: str, scores: dict[str, float], language: str) -> str:
    if language == "zh":
        city_label = ZH_CITY_LABELS.get(city, city)
        return (
            f"{city_label} 在留学、职业和生活三方面综合得分为 {scores['total_score']:.1f}。"
            f"主要优势来自学习资源 {scores['study_score']:.1f}、职业机会 {scores['career_score']:.1f}、"
            f"生活匹配度 {scores['living_score']:.1f}。"
        )
    return (
        f"{city} scores {scores['total_score']:.1f} overall across study, career, and living fit. "
        f"Key drivers are study resources ({scores['study_score']:.1f}), career outlook "
        f"({scores['career_score']:.1f}), and living fit ({scores['living_score']:.1f})."
    )


def recommend_cities(study_profile: Any, career_profile: Any, living_profile: Any, language: str = "en") -> dict:
    study = _dump(study_profile)
    career = _dump(career_profile)
    living = _dump(living_profile)
    role = career.get("target_role", "Data Analyst")
    industry = ROLE_INDUSTRY.get(role, str(career.get("target_industry", "Technology")).lower())
    korean = career.get("korean_level") or study.get("korean_level") or "None"
    monthly_budget = float(living.get("monthly_budget") or 0)
    preferred_city = living.get("preferred_city") or study.get("preferred_city")
    community = living.get("community_preference", "")

    rankings = []
    for city in CITIES:
        traits = CITY_TRAITS[city]
        study_score = traits["study"]
        career_score = (traits["career"] * 0.55) + (traits.get(industry, traits["career"]) * 0.45)
        living_score = traits["living"]
        cost_score = _budget_score(monthly_budget, int(1_100_000 + (100 - traits["cost"]) * 17_000))
        language_fit_score = (KOREAN_LEVEL_SCORE.get(korean, 45) * 0.55) + (traits["international"] * 0.45)
        lifestyle_score = traits["quiet"] if "Quiet" in community or "quiet" in community else traits["international"]
        preference_bonus = 4 if city == preferred_city else 0
        total = (
            study_score * 0.22
            + career_score * 0.27
            + living_score * 0.17
            + cost_score * 0.14
            + language_fit_score * 0.10
            + lifestyle_score * 0.10
            + preference_bonus
        )
        score = {
            "city": city,
            "total_score": round(min(total, 100), 1),
            "study_score": round(study_score, 1),
            "career_score": round(career_score, 1),
            "living_score": round(living_score, 1),
            "cost_score": round(cost_score, 1),
            "language_fit_score": round(language_fit_score, 1),
            "lifestyle_score": round(lifestyle_score, 1),
        }
        score["recommendation_reason"] = _reason(city, score, "zh" if language == "zh" else "en")
        rankings.append(score)

    rankings.sort(key=lambda item: item["total_score"], reverse=True)
    return {"best_city": rankings[0]["city"], "rankings": rankings}
