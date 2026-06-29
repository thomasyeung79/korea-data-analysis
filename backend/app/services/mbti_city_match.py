from __future__ import annotations

from typing import Any


SUPPORTED_MBTI = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]


CITY_ENVIRONMENT = {
    "Seoul": {"social": 96, "pace": 96, "career": 98, "study": 94, "cost": 45, "quiet": 42, "creative": 90},
    "Busan": {"social": 82, "pace": 74, "career": 78, "study": 82, "cost": 74, "quiet": 68, "creative": 78},
    "Incheon": {"social": 80, "pace": 72, "career": 80, "study": 76, "cost": 76, "quiet": 66, "creative": 70},
    "Daejeon": {"social": 66, "pace": 58, "career": 82, "study": 90, "cost": 82, "quiet": 84, "creative": 66},
    "Daegu": {"social": 64, "pace": 62, "career": 68, "study": 74, "cost": 86, "quiet": 78, "creative": 68},
    "Gwangju": {"social": 62, "pace": 54, "career": 62, "study": 72, "cost": 88, "quiet": 86, "creative": 82},
    "Jeju": {"social": 58, "pace": 42, "career": 52, "study": 58, "cost": 72, "quiet": 92, "creative": 88},
}


ZH_CITY = {
    "Seoul": "首尔",
    "Busan": "釜山",
    "Incheon": "仁川",
    "Daejeon": "大田",
    "Daegu": "大邱",
    "Gwangju": "光州",
    "Jeju": "济州",
}


def _dump(value: Any) -> dict:
    return value.model_dump() if hasattr(value, "model_dump") else dict(value or {})


def _target_social(mbti_type: str, social_energy: str) -> int:
    if social_energy == "High":
        return 90
    if social_energy == "Low":
        return 45
    return 78 if mbti_type.startswith("E") else 58


def _target_pace(mbti_type: str, pace_preference: str) -> int:
    if pace_preference == "Fast":
        return 92
    if pace_preference == "Slow":
        return 45
    return 78 if "J" in mbti_type else 66


def _score_distance(actual: float, target: float) -> float:
    return max(35.0, 100 - abs(actual - target) * 1.15)


def _personality_score(mbti_type: str, traits: dict, social_target: int, pace_target: int) -> float:
    intuitive_bonus = traits["creative"] if "N" in mbti_type else traits["quiet"]
    judging_bonus = traits["pace"] if "J" in mbti_type else traits["creative"]
    return (
        _score_distance(traits["social"], social_target) * 0.35
        + _score_distance(traits["pace"], pace_target) * 0.35
        + intuitive_bonus * 0.15
        + judging_bonus * 0.15
    )


def _lifestyle_score(lifestyle_preference: str, budget_sensitivity: str, traits: dict) -> float:
    if lifestyle_preference == "Quiet":
        base = traits["quiet"]
    elif lifestyle_preference == "Creative":
        base = traits["creative"]
    elif lifestyle_preference == "Urban":
        base = (traits["social"] + traits["pace"]) / 2
    else:
        base = (traits["quiet"] + traits["social"] + traits["creative"]) / 3
    budget_weight = {"Low": 0.15, "Medium": 0.25, "High": 0.38}.get(budget_sensitivity, 0.25)
    return base * (1 - budget_weight) + traits["cost"] * budget_weight


def _reason(city: str, score: dict, mbti_type: str, language: str) -> str:
    name = ZH_CITY.get(city, city) if language == "zh" else city
    if language == "zh":
        return (
            f"{name} 与 {mbti_type} 的生活偏好匹配度较高，综合分为 {score['total_score']:.1f}。"
            f"主要优势来自生活方式匹配 {score['lifestyle_fit_score']:.1f}、社交环境 {score['social_fit_score']:.1f}、"
            f"职业环境 {score['career_environment_score']:.1f}。"
        )
    return (
        f"{name} is a strong lifestyle match for {mbti_type}, scoring {score['total_score']:.1f}. "
        f"Key drivers are lifestyle fit ({score['lifestyle_fit_score']:.1f}), social fit "
        f"({score['social_fit_score']:.1f}), and career environment ({score['career_environment_score']:.1f})."
    )


def _challenges(city: str, traits: dict, budget_sensitivity: str, language: str) -> list[str]:
    if language == "zh":
        challenges = []
        if traits["cost"] < 60 or budget_sensitivity == "High":
            challenges.append("需要提前规划住房与日常预算。")
        if traits["social"] > 85:
            challenges.append("城市节奏和社交密度可能偏高，需要保留个人恢复时间。")
        if traits["career"] < 65:
            challenges.append("职业机会相对集中度较低，建议远程或跨城市求职。")
        return challenges or ["整体风险较低，但仍建议先短住体验。"]
    challenges = []
    if traits["cost"] < 60 or budget_sensitivity == "High":
        challenges.append("Plan housing and daily budget carefully.")
    if traits["social"] > 85:
        challenges.append("The pace and social density may feel intense; protect recovery time.")
    if traits["career"] < 65:
        challenges.append("Career density is lower, so consider remote or cross-city search.")
    return challenges or ["Overall friction is moderate; try a short stay before committing."]


def _living_style(city: str, lifestyle_preference: str, language: str) -> str:
    if language == "zh":
        if lifestyle_preference == "Quiet":
            return f"建议在{ZH_CITY.get(city, city)}选择安静社区、靠近地铁或校园的住宅。"
        if lifestyle_preference == "Urban":
            return f"建议选择交通便利、靠近职业机会和社交资源的区域。"
        if lifestyle_preference == "Creative":
            return f"建议选择文化、咖啡馆、展览和创意社区较活跃的区域。"
        return "建议先选择交通便利且预算可控的社区，再逐步探索长期居住区域。"
    if lifestyle_preference == "Quiet":
        return f"Choose a quieter neighborhood in {city} with transit access to school or work."
    if lifestyle_preference == "Urban":
        return "Prioritize transit-rich areas close to work opportunities and social infrastructure."
    if lifestyle_preference == "Creative":
        return "Look for areas with culture, cafes, exhibitions, and creative communities."
    return "Start with a transit-friendly, budget-aware neighborhood before choosing a long-term base."


def match_mbti_city(request: Any) -> dict:
    data = _dump(request)
    language = "zh" if data.get("language") == "zh" else "en"
    mbti_type = str(data.get("mbti_type", "INFJ")).upper()
    if mbti_type not in SUPPORTED_MBTI:
        mbti_type = "INFJ"
    social_energy = data.get("social_energy", "Medium")
    lifestyle = data.get("lifestyle_preference", "Balanced")
    pace = data.get("pace_preference", "Moderate")
    budget = data.get("budget_sensitivity", "Medium")
    career_priority = float(data.get("career_priority", 5))
    study_priority = float(data.get("study_priority", 5))
    social_target = _target_social(mbti_type, social_energy)
    pace_target = _target_pace(mbti_type, pace)

    city_scores = []
    for city, traits in CITY_ENVIRONMENT.items():
        personality = _personality_score(mbti_type, traits, social_target, pace_target)
        lifestyle_score = _lifestyle_score(lifestyle, budget, traits)
        social = _score_distance(traits["social"], social_target)
        career = traits["career"]
        study = traits["study"]
        career_weight = 0.12 + career_priority / 100
        study_weight = 0.12 + study_priority / 100
        total = (
            personality * 0.28
            + lifestyle_score * 0.23
            + social * 0.16
            + career * career_weight
            + study * study_weight
            + traits["cost"] * 0.10
        )
        score = {
            "city": city,
            "total_score": round(min(total, 100), 1),
            "personality_fit_score": round(personality, 1),
            "lifestyle_fit_score": round(lifestyle_score, 1),
            "social_fit_score": round(social, 1),
            "career_environment_score": round(career, 1),
            "study_environment_score": round(study, 1),
            "recommendation_reason": "",
            "potential_challenges": _challenges(city, traits, budget, language),
            "suggested_living_style": _living_style(city, lifestyle, language),
        }
        score["recommendation_reason"] = _reason(city, score, mbti_type, language)
        city_scores.append(score)

    city_scores.sort(key=lambda item: item["total_score"], reverse=True)
    best = city_scores[0]
    return {
        "best_city": best["city"],
        "city_scores": city_scores,
        "personality_fit_score": best["personality_fit_score"],
        "lifestyle_fit_score": best["lifestyle_fit_score"],
        "social_fit_score": best["social_fit_score"],
        "career_environment_score": best["career_environment_score"],
        "study_environment_score": best["study_environment_score"],
        "recommendation_reason": best["recommendation_reason"],
        "potential_challenges": best["potential_challenges"],
        "suggested_living_style": best["suggested_living_style"],
    }
