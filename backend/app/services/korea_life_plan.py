from __future__ import annotations

from typing import Any

from .city_recommendation import recommend_cities
from .job_market_config import analyze_job_market
from .study_cost_config import calculate_costs


def _dump(value: Any) -> dict:
    return value.model_dump() if hasattr(value, "model_dump") else dict(value or {})


def _risk_from_gap(gap: float, language: str) -> str:
    if gap >= 2_000_000:
        return "Low" if language != "zh" else "低"
    if gap >= 0:
        return "Medium" if language != "zh" else "中"
    return "High" if language != "zh" else "高"


def _language_risk(korean_level: str, language: str) -> str:
    if korean_level in {"TOPIK 4", "TOPIK 5+"}:
        return "Low" if language != "zh" else "低"
    if korean_level == "TOPIK 3":
        return "Medium" if language != "zh" else "中"
    return "High" if language != "zh" else "高"


def _career_risk(competitiveness: int, language: str) -> str:
    if competitiveness <= 5:
        return "Low" if language != "zh" else "低"
    if competitiveness <= 7:
        return "Medium" if language != "zh" else "中"
    return "High" if language != "zh" else "高"


def _overall(budget_gap: float, language_risk: str, career_risk: str, language: str) -> str:
    high = {"High", "高"}
    medium = {"Medium", "中"}
    if budget_gap >= 0 and language_risk not in high and career_risk not in high:
        return "Recommended with Preparation" if language != "zh" else "准备充分后推荐"
    if language_risk in high or career_risk in high or budget_gap < -3_000_000:
        return "Risky" if language != "zh" else "有一定风险"
    if language_risk in medium or career_risk in medium:
        return "Recommended with Preparation" if language != "zh" else "准备充分后推荐"
    return "Strongly Recommended" if language != "zh" else "强烈推荐"


def generate_korea_life_plan(
    display_name: str,
    study_profile: Any,
    career_profile: Any,
    living_profile: Any,
    language: str = "en",
) -> dict:
    lang = "zh" if language == "zh" else "en"
    study = _dump(study_profile)
    career = _dump(career_profile)
    living = _dump(living_profile)

    city_result = recommend_cities(study, career, living, language=lang)
    best_city = city_result["best_city"]

    housing = living.get("housing_preference", "Shared Apartment")
    lifestyle = living.get("lifestyle", "Standard")
    study_level = study.get("target_study_level", "Graduate School")
    cost = calculate_costs(best_city, study_level if study_level != "Not Applicable" else "Graduate School", housing, lifestyle)
    career_result = analyze_job_market(
        career.get("target_role", "Data Analyst"),
        career.get("work_experience", "0-2 years"),
        career.get("korean_level", study.get("korean_level", "None")),
        language=lang,
    )

    estimated_annual_study_cost = float(cost["annual_cost"])
    estimated_monthly_living_cost = float(cost["monthly_cost"])
    budget_gap = float(study.get("annual_budget", 0)) - estimated_annual_study_cost
    lang_risk = _language_risk(career.get("korean_level", study.get("korean_level", "None")), lang)
    car_risk = _career_risk(int(career_result.get("competitiveness", 6)), lang)
    living_risk = _risk_from_gap(float(living.get("monthly_budget", 0)) - estimated_monthly_living_cost, lang)
    overall = _overall(budget_gap, lang_risk, car_risk, lang)

    if lang == "zh":
        study_path = f"建议以 {best_city} 为核心城市，申请 {study.get('target_major', '目标专业')} 的 {study.get('target_study_level', '研究生')} 项目。"
        career_path = f"目标岗位为 {career.get('target_role', '目标岗位')}，建议优先补齐岗位技能并关注可担保 E-7 的雇主。"
        living_plan = f"按 {living.get('lifestyle', 'Standard')} 生活方式规划，优先选择 {living.get('housing_preference', 'Shared Apartment')}。"
        visa_pathway = f"留学可走 D-2，毕业后可转 D-10 求职，再根据岗位担保规划 {career.get('visa_goal', 'E-7')}。"
        action_3 = "1-3 个月：完善画像、确认目标城市、准备 TOPIK/英语材料、整理预算和申请清单。"
        action_6 = "4-6 个月：提交学校或岗位申请，建立韩国联系人网络，准备签证材料和住宿方案。"
        action_12 = "7-12 个月：完成录取或 offer、确认签证路径、安排搬迁、银行、通信、保险和 ARC。"
    else:
        study_path = f"Use {best_city} as the anchor city and target {study.get('target_major', 'your major')} at {study.get('target_study_level', 'graduate')} level."
        career_path = f"Target {career.get('target_role', 'your role')} roles and prioritise employers able to sponsor {career.get('visa_goal', 'E-7')}."
        living_plan = f"Plan around a {living.get('lifestyle', 'Standard')} lifestyle and prioritise {living.get('housing_preference', 'Shared Apartment')} housing."
        visa_pathway = f"Typical path: D-2 for study, D-10 after graduation, then {career.get('visa_goal', 'E-7')} with employer sponsorship."
        action_3 = "Months 1-3: refine your profile, confirm target city, prepare language materials, budget, and application checklist."
        action_6 = "Months 4-6: submit school or job applications, build Korea contacts, prepare visa documents and housing options."
        action_12 = "Months 7-12: secure admission or offer, confirm visa route, arrange relocation, banking, phone, insurance, and ARC."

    if lang == "zh":
        markdown = f"""# {display_name} 的韩国生活规划

## 总体建议
{overall}

## 最佳城市
{best_city}

## 留学路径
{study_path}

## 职业路径
{career_path}

## 生活规划
{living_plan}

## 签证路径
{visa_pathway}

## 行动计划
- 3 个月：{action_3}
- 6 个月：{action_6}
- 12 个月：{action_12}
"""
    else:
        markdown = f"""# Korea Life Plan for {display_name}

## Overall Recommendation
{overall}

## Best City
{best_city}

## Study Path
{study_path}

## Career Path
{career_path}

## Living Plan
{living_plan}

## Visa Pathway
{visa_pathway}

## Action Plan
- 3 months: {action_3}
- 6 months: {action_6}
- 12 months: {action_12}
"""

    return {
        "overall_recommendation": overall,
        "best_city": best_city,
        "study_path": study_path,
        "career_path": career_path,
        "living_plan": living_plan,
        "estimated_annual_study_cost": estimated_annual_study_cost,
        "estimated_monthly_living_cost": estimated_monthly_living_cost,
        "budget_gap": budget_gap,
        "language_risk": lang_risk,
        "career_risk": car_risk,
        "living_risk": living_risk,
        "visa_pathway": visa_pathway,
        "action_plan_3_month": action_3,
        "action_plan_6_month": action_6,
        "action_plan_12_month": action_12,
        "city_recommendations": city_result["rankings"],
        "markdown_report": markdown,
    }
