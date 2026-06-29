from __future__ import annotations

from typing import Any

from .city_recommendation import recommend_cities
from .data_loader import validate_metadata
from .job_market_config import analyze_job_market
from .mbti_city_match import match_mbti_city
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


def _overall(budget_gap: float, language_risk: str, career_risk: str, living_risk: str, language: str) -> str:
    high = {"High", "高"}
    medium = {"Medium", "中"}
    if budget_gap >= 0 and language_risk not in high and career_risk not in high and living_risk not in high:
        return "Recommended with Preparation" if language != "zh" else "准备充分后推荐"
    if language_risk in high or career_risk in high or living_risk in high or budget_gap < -3_000_000:
        return "Risky" if language != "zh" else "有一定风险"
    if language_risk in medium or career_risk in medium or living_risk in medium:
        return "Recommended with Preparation" if language != "zh" else "准备充分后推荐"
    return "Strongly Recommended" if language != "zh" else "强烈推荐"


def _confidence_summary(language: str) -> str:
    status = validate_metadata()
    coverage = status.get("source_coverage", {})
    official = coverage.get("Official", 0)
    verified = coverage.get("Verified", 0)
    mock = coverage.get("Mock", 0)
    total = status.get("total_files", 0)
    if language == "zh":
        return (
            f"Data confidence summary：当前知识库包含 {total} 个 JSON 文件，其中 Official {official} 个、"
            f"Verified {verified} 个、Mock {mock} 个。本报告基于可用输入生成；涉及成本、薪资和城市评分的结论仍为方向性规划建议。"
        )
    return (
        f"Data confidence summary: the Knowledge Base has {total} JSON files, including {official} Official, "
        f"{verified} Verified, and {mock} Mock files. This report is based on available inputs; cost, salary, "
        f"and city scoring conclusions remain directional planning guidance."
    )


def _language_plan(korean_level: str, topik_goal: str | None, language: str) -> str:
    target = topik_goal or ("TOPIK 4" if korean_level in {"None", "TOPIK 3"} else "TOPIK 5+")
    if language == "zh":
        return (
            f"当前韩语水平为 {korean_level}，建议目标设为 {target}。"
            "每周安排 4-6 小时 TOPIK 阅读/听力训练，并补充学校、面试、医院、银行等场景表达。"
        )
    return (
        f"Current Korean level is {korean_level}; recommended target is {target}. "
        "Plan 4-6 hours per week for TOPIK reading/listening plus scenario Korean for school, interviews, hospitals, and banking."
    )


def _budget_analysis(annual_budget: float, annual_cost: float, monthly_budget: float, monthly_cost: float, language: str) -> str:
    annual_gap = annual_budget - annual_cost
    monthly_gap = monthly_budget - monthly_cost
    if language == "zh":
        return (
            f"年度预算差额约为 {annual_gap:,.0f} 韩元，月度生活预算差额约为 {monthly_gap:,.0f} 韩元。"
            "如果差额为负，建议优先调整城市、住房类型或生活方式。"
        )
    return (
        f"Annual budget gap is about {annual_gap:,.0f} KRW and monthly living budget gap is about {monthly_gap:,.0f} KRW. "
        "If the gap is negative, adjust city, housing, or lifestyle assumptions first."
    )


def _risk_summary(language_risk: str, career_risk: str, living_risk: str, language: str) -> str:
    if language == "zh":
        return f"主要风险：语言风险 {language_risk}，职业风险 {career_risk}，生活/预算风险 {living_risk}。建议先处理最高风险项。"
    return f"Main risks: language risk {language_risk}, career risk {career_risk}, living/budget risk {living_risk}. Address the highest-risk item first."


def _input_list(city_recommendation: dict | None, mbti_city_match: dict | None, topik_goal: str | None, language: str) -> list[str]:
    items = [
        "Profile Center" if language != "zh" else "画像中心",
        "Study Cost" if language != "zh" else "留学成本",
        "Career Analyzer" if language != "zh" else "职业分析",
        "Knowledge Base metadata" if language != "zh" else "知识库 metadata",
    ]
    items.append(("City Recommendation" if language != "zh" else "城市推荐") if city_recommendation else ("City Recommendation (generated from profile)" if language != "zh" else "城市推荐（基于画像生成）"))
    items.append(("MBTI City Match" if language != "zh" else "MBTI 城市匹配") if mbti_city_match else ("MBTI City Match missing" if language != "zh" else "缺少 MBTI 城市匹配"))
    items.append(("TOPIK target" if language != "zh" else "TOPIK 目标") if topik_goal else ("TOPIK target inferred" if language != "zh" else "TOPIK 目标为推断值"))
    return items


def generate_korea_life_plan(
    display_name: str,
    study_profile: Any,
    career_profile: Any,
    living_profile: Any,
    language: str = "en",
    city_recommendation: dict | None = None,
    mbti_city_match: dict | None = None,
    topik_goal: str | None = None,
) -> dict:
    lang = "zh" if language == "zh" else "en"
    study = _dump(study_profile)
    career = _dump(career_profile)
    living = _dump(living_profile)
    provided_city_recommendation = city_recommendation is not None
    provided_mbti_city_match = mbti_city_match is not None

    generated_city_result = recommend_cities(study, career, living, language=lang)
    city_result = city_recommendation or generated_city_result
    best_city = str(city_result.get("best_city") or generated_city_result["best_city"])

    if mbti_city_match is None:
        mbti_city_match = match_mbti_city({
            "mbti_type": "INFJ",
            "social_energy": "Medium",
            "lifestyle_preference": "Balanced",
            "pace_preference": "Moderate",
            "budget_sensitivity": "Medium",
            "career_priority": 5,
            "study_priority": 5,
            "language": lang,
        })

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
    annual_budget = float(study.get("annual_budget", 0))
    monthly_budget = float(living.get("monthly_budget", 0))
    budget_gap = annual_budget - estimated_annual_study_cost
    korean_level = career.get("korean_level", study.get("korean_level", "None"))
    lang_risk = _language_risk(korean_level, lang)
    car_risk = _career_risk(int(career_result.get("competitiveness", 6)), lang)
    living_risk = _risk_from_gap(monthly_budget - estimated_monthly_living_cost, lang)
    overall = _overall(budget_gap, lang_risk, car_risk, living_risk, lang)
    mbti_best_city = str(mbti_city_match.get("best_city", ""))

    if lang == "zh":
        study_path = f"建议以 {best_city} 为核心城市，申请 {study.get('target_major', '目标专业')} 的 {study.get('target_study_level', '研究生')} 项目。"
        career_path = f"目标岗位为 {career.get('target_role', '目标岗位')}，建议优先补齐岗位技能并关注可担保 E-7 的雇主。"
        living_plan = f"按 {living.get('lifestyle', 'Standard')} 生活方式规划，优先选择 {living.get('housing_preference', 'Shared Apartment')}。"
        mbti_city_fit = f"MBTI 城市匹配推荐 {mbti_best_city}；当前综合最佳城市为 {best_city}。如两者不同，建议把 {mbti_best_city} 作为生活方式备选城市。"
        visa_pathway = f"留学可走 D-2，毕业后可转 D-10 求职，再根据岗位担保规划 {career.get('visa_goal', 'E-7')}。"
        action_3 = "1-3 个月：完善画像、确认目标城市、准备 TOPIK/英语材料、整理预算、申请清单和 MBTI 城市偏好。"
        action_6 = "4-6 个月：提交学校或岗位申请，建立韩国联系人网络，准备签证材料、住宿方案和场景韩语。"
        action_12 = "7-12 个月：完成录取或 offer、确认签证路径、安排搬迁、银行、通信、保险、ARC 和长期城市落点。"
        report_title = f"# {display_name} 的综合韩国生活规划"
    else:
        study_path = f"Use {best_city} as the anchor city and target {study.get('target_major', 'your major')} at {study.get('target_study_level', 'graduate')} level."
        career_path = f"Target {career.get('target_role', 'your role')} roles and prioritise employers able to sponsor {career.get('visa_goal', 'E-7')}."
        living_plan = f"Plan around a {living.get('lifestyle', 'Standard')} lifestyle and prioritise {living.get('housing_preference', 'Shared Apartment')} housing."
        mbti_city_fit = f"MBTI City Match recommends {mbti_best_city}; the current integrated best city is {best_city}. If they differ, treat {mbti_best_city} as a lifestyle-fit alternative."
        visa_pathway = f"Typical path: D-2 for study, D-10 after graduation, then {career.get('visa_goal', 'E-7')} with employer sponsorship."
        action_3 = "Months 1-3: refine profile, confirm target city, prepare TOPIK/English materials, budget, application checklist, and MBTI city preference."
        action_6 = "Months 4-6: submit school or job applications, build Korea contacts, prepare visa documents, housing options, and scenario Korean."
        action_12 = "Months 7-12: secure admission or offer, confirm visa route, arrange relocation, banking, phone, insurance, ARC, and long-term city base."
        report_title = f"# Integrated Korea Life Plan for {display_name}"

    language_learning_plan = _language_plan(korean_level, topik_goal, lang)
    budget_analysis = _budget_analysis(annual_budget, estimated_annual_study_cost, monthly_budget, estimated_monthly_living_cost, lang)
    risk_summary = _risk_summary(lang_risk, car_risk, living_risk, lang)
    confidence_summary = _confidence_summary(lang)
    available_inputs = _input_list(
        city_recommendation if provided_city_recommendation else None,
        mbti_city_match if provided_mbti_city_match else None,
        topik_goal,
        lang,
    )

    if lang == "zh":
        markdown = f"""{report_title}

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

## MBTI 城市匹配
{mbti_city_fit}

## 语言学习计划
{language_learning_plan}

## 预算分析
{budget_analysis}

## 签证路径
{visa_pathway}

## 风险总结
{risk_summary}

## Data confidence summary
{confidence_summary}

## 行动计划
- 3 个月：{action_3}
- 6 个月：{action_6}
- 12 个月：{action_12}

## 可用输入
{", ".join(available_inputs)}
"""
    else:
        markdown = f"""{report_title}

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

## MBTI City Fit
{mbti_city_fit}

## Language Learning Plan
{language_learning_plan}

## Budget Analysis
{budget_analysis}

## Visa Pathway
{visa_pathway}

## Risk Summary
{risk_summary}

## Data confidence summary
{confidence_summary}

## Action Plan
- 3 months: {action_3}
- 6 months: {action_6}
- 12 months: {action_12}

## Available Inputs
{", ".join(available_inputs)}
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
        "city_recommendations": city_result.get("rankings", generated_city_result["rankings"]),
        "mbti_city_fit": mbti_city_fit,
        "language_learning_plan": language_learning_plan,
        "budget_analysis": budget_analysis,
        "risk_summary": risk_summary,
        "confidence_summary": confidence_summary,
        "based_on_available_inputs": available_inputs,
        "markdown_report": markdown,
    }
