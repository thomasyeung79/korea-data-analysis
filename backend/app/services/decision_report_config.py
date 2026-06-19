"""
Decision Report Engine — combines study cost + job market analysis into a
personalised recommendation for studying, working, or living in Korea.

Reuses calculation logic from:
  - study_cost_config.py (calculate_costs)
  - job_market_config.py (analyze_job_market)

No external APIs. Rule-based recommendation engine.
"""

from .study_cost_config import CITY_BASE_COST, HOUSING_COST, calculate_costs
from .job_market_config import COMPETITIVENESS, SALARY_GRID, analyze_job_market

GOALS = ["Study", "Work", "Live"]

RECOMMENDATION_LABELS = {
    "strongly_recommended": "Strongly Recommended ✅",
    "recommended_with_prep": "Recommended with Preparation ⚠️",
    "risky": "Risky ❓",
    "not_recommended": "Not Recommended Yet ❌",
}

RECOMMENDATION_LABELS_ZH = {
    "strongly_recommended": "强烈推荐 ✅",
    "recommended_with_prep": "准备充分后推荐 ⚠️",
    "risky": "有一定风险 ❓",
    "not_recommended": "暂不推荐 ❌",
}

ZH_GOAL_LABELS = {"Study": "留学", "Work": "工作", "Live": "生活"}
ZH_CITY_LABELS = {"Seoul": "首尔", "Busan": "釜山", "Daejeon": "大田", "Daegu": "大邱", "Other": "其他城市"}
ZH_ROLE_LABELS = {
    "Data Analyst": "数据分析师",
    "Backend Developer": "后端开发工程师",
    "AI Product Manager": "AI 产品经理",
    "AI Engineer": "AI 工程师",
    "Marketing Specialist": "市场营销专员",
    "Business Analyst": "商业分析师",
    "Operations Specialist": "运营专员",
    "Customer Support Specialist": "客户支持专员",
    "International Sales": "国际销售",
    "Product Manager": "产品经理",
    "Not Applicable": "不适用",
}


def _language(language: str) -> str:
    return "zh" if language == "zh" else "en"


def _zh_goal(goal: str) -> str:
    return ZH_GOAL_LABELS.get(goal, goal)


def _zh_city(city: str) -> str:
    return ZH_CITY_LABELS.get(city, city)


def _zh_role(role: str) -> str:
    return ZH_ROLE_LABELS.get(role, role)


def _financial_risk(monthly_cost: int, monthly_budget: int) -> tuple[str, int, int]:
    """Calculate financial risk and gap."""
    gap = monthly_budget - monthly_cost
    if gap >= 0:
        surplus_pct = round(gap / monthly_cost * 100)
        if surplus_pct >= 20:
            return "Low", gap, surplus_pct
        return "Medium", gap, surplus_pct
    deficit_pct = round(-gap / monthly_cost * 100)
    if deficit_pct <= 20:
        return "Medium", gap, -deficit_pct
    return "High", gap, deficit_pct


def _language_risk(korean_level: str, goal: str, language: str = "en") -> tuple[str, str]:
    """Assess language risk based on goal and current level."""
    level_map = {"None": 0, "TOPIK 3": 3, "TOPIK 4": 4, "TOPIK 5+": 5}
    level = level_map.get(korean_level, 0)

    if _language(language) == "zh":
        thresholds = {
            "Study": {"required": 3, "label": "多数韩语授课项目通常需要 TOPIK 3-4。"},
            "Work": {"required": 4, "label": "多数专业岗位需要 TOPIK 4+ 才能更好融入团队。"},
            "Live": {"required": 2, "label": "日常生活具备基础韩语（TOPIK 2-3）会更稳妥。"},
        }
    else:
        thresholds = {
            "Study": {"required": 3, "label": "Most university programs require TOPIK 3-4 for Korean-track studies."},
            "Work": {"required": 4, "label": "Most professional roles require TOPIK 4+ for team integration."},
            "Live": {"required": 2, "label": "Daily life is manageable with basic Korean (TOPIK 2-3)."},
        }
    info = thresholds.get(goal, thresholds["Live"])

    if level >= info["required"]:
        return "Low", info["label"]
    elif level >= info["required"] - 1:
        return "Medium", info["label"]
    else:
        if _language(language) == "zh":
            return "High", f"{info['label']} 你当前的韩语水平（{korean_level}）低于建议门槛。"
        return "High", f"{info['label']} Your current level ({korean_level}) is below the recommended threshold."


def _career_risk(role: str, competitiveness: int, language: str = "en") -> tuple[str, str]:
    """Assess career risk based on competitiveness score."""
    if role == "Not Applicable" or not role:
        if _language(language) == "zh":
            return "Low", "你的当前目标不需要职业风险评估。"
        return "Low", "Career assessment not applicable to your goal."
    if competitiveness <= 5:
        if _language(language) == "zh":
            return "Low", f"竞争强度 {competitiveness}/10，岗位市场相对友好。"
        return "Low", f"Competitiveness score {competitiveness}/10 — favourable job market conditions."
    elif competitiveness <= 7:
        if _language(language) == "zh":
            return "Medium", f"竞争强度 {competitiveness}/10，建议强化简历差异化。"
        return "Medium", f"Competitiveness score {competitiveness}/10 — resume differentiation recommended."
    else:
        if _language(language) == "zh":
            return "High", f"竞争强度 {competitiveness}/10，需要更强准备和人脉拓展。"
        return "High", f"Competitiveness score {competitiveness}/10 — requires strong preparation and networking."


def _visa_living_risk(goal: str, monthly_budget: int, monthly_cost: int, language: str = "en") -> tuple[str, str]:
    """Assess visa and living risk."""
    gap = monthly_budget - monthly_cost
    factors = []
    if gap < 0:
        factors.append("月度预算低于估算生活成本。" if _language(language) == "zh" else "Monthly budget is below estimated living costs.")
    if goal == "Work":
        factors.append("E-7 签证需要雇主担保，求职周期可能需要 3-6 个月。" if _language(language) == "zh" else "E-7 visa requires employer sponsorship. Job search can take 3-6 months.")
    elif goal == "Study":
        factors.append("D-2 学生签证通常需要资金证明（常见要求约 20,000 美元以上）。" if _language(language) == "zh" else "D-2 visa requires proof of funds (typically $20,000+ in bank account).")
    if len(factors) == 0:
        if _language(language) == "zh":
            return "Low", "签证和生活安排看起来较可控。"
        return "Low", "Visa and living requirements appear manageable."
    elif len(factors) == 1:
        return "Medium", " ".join(factors)
    return "High", " ".join(factors)


def _recommendation_classifier(
    financial_risk: str, language_risk: str, career_risk: str, visa_risk: str,
    monthly_budget: int, monthly_cost: int,
) -> str:
    """Classify overall recommendation based on risk profile."""
    risks = [financial_risk, language_risk, career_risk, visa_risk]
    high_count = risks.count("High")
    medium_count = risks.count("Medium")

    if high_count == 0 and medium_count <= 1 and monthly_budget >= monthly_cost:
        return "strongly_recommended"
    if high_count == 0 and medium_count <= 2:
        return "recommended_with_prep"
    if high_count <= 1:
        return "risky"
    return "not_recommended"


def generate_decision_report(
    goal: str,
    target_city: str,
    school_type: str,
    housing_type: str,
    lifestyle_level: str,
    target_role: str,
    experience_level: str,
    korean_level: str,
    monthly_budget: int,
    language: str = "en",
) -> dict:
    """Generate a full decision report combining cost + career analysis."""

    # ── 1. Financial analysis ──
    use_school = school_type if school_type != "Not Applicable" else "Undergraduate"
    use_housing = housing_type if housing_type != "Not Applicable" else "Shared Apartment"

    cost_result = calculate_costs(target_city, use_school, use_housing, lifestyle_level)
    monthly_cost = cost_result["monthly_cost"]
    annual_cost = cost_result["annual_cost"]
    breakdown = cost_result["breakdown"]

    fin_risk, gap, gap_pct = _financial_risk(monthly_cost, monthly_budget)

    # ── 2. Career analysis ──
    career_result = None
    if target_role != "Not Applicable":
        career_result = analyze_job_market(target_role, experience_level, korean_level)

    salary_min = career_result["salary_min"] if career_result else 0
    salary_max = career_result["salary_max"] if career_result else 0
    competitiveness = career_result["competitiveness"] if career_result else 0
    skills = career_result["required_skills"] if career_result else []
    language_req = career_result["korean_language_requirement"] if career_result else ""

    # ── 3. Risk assessment ──
    lang_risk, lang_detail = _language_risk(korean_level, goal, language)
    car_risk, car_detail = _career_risk(target_role, competitiveness, language)
    visa_risk, visa_detail = _visa_living_risk(goal, monthly_budget, monthly_cost, language)

    overall = _recommendation_classifier(fin_risk, lang_risk, car_risk, visa_risk, monthly_budget, monthly_cost)

    # ── 4. Action plan ──
    action_plan = _generate_action_plan(goal, fin_risk, lang_risk, korean_level, target_role, language)

    # ── 5. Final summary ──
    summary = _generate_summary(overall, goal, target_city, monthly_cost, monthly_budget, korean_level, language)

    return {
        "recommendation": overall,
        "recommendation_label": RECOMMENDATION_LABELS_ZH[overall] if _language(language) == "zh" else RECOMMENDATION_LABELS[overall],
        "monthly_cost_estimate": monthly_cost,
        "annual_cost_estimate": annual_cost,
        "cost_breakdown": breakdown,
        "budget_gap": gap,
        "budget_gap_pct": gap_pct,
        "financial_risk": fin_risk,
        "language_risk": lang_risk,
        "language_risk_detail": lang_detail,
        "career_risk": car_risk,
        "career_risk_detail": car_detail,
        "visa_living_risk": visa_risk,
        "visa_living_risk_detail": visa_detail,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "required_skills": skills,
        "korean_language_requirement": language_req,
        "competitiveness": competitiveness,
        "action_plan": action_plan,
        "summary": summary,
        "currency": "KRW",
    }


def _generate_action_plan(goal: str, fin_risk: str, lang_risk: str, korean_level: str, target_role: str, language: str = "en") -> str:
    """Generate a structured 3-month action plan."""
    if _language(language) == "zh":
        lines = ["### 第 1 个月：打好基础"]
        month1 = []
        if fin_risk == "High":
            month1.append("建立详细预算，优先研究 GKS、大学奖学金或其他资助机会。")
            month1.append("如果符合签证条件，了解兼职规则和可行收入。")
        else:
            month1.append("确认预算覆盖主要支出，并预留押金、机票和初始安置费用。")
        if lang_risk == "High":
            month1.append("开始高强度韩语学习，目标是在 3 个月内达到 TOPIK 2-3。")
        elif lang_risk == "Medium":
            month1.append("报名韩语课程或 TOPIK 备考班，补齐沟通短板。")
        if target_role and target_role != "Not Applicable":
            month1.append(f"研究{_zh_role(target_role)}岗位市场，整理目标公司和技能要求。")
        month1.append("调研目标城市住房选择，如考试院、one-room、合租或宿舍。")
        lines.append("\n".join(f"- {item}" for item in month1))

        lines.append("\n### 第 2 个月：集中准备")
        month2 = [
            "如果目标是留学，准备成绩单、个人陈述、推荐信和奖学金材料。",
            "研究签证要求：D-2（留学）、E-7（工作）或 D-10（求职）。",
            "估算第一年总成本，包括机票、押金、保险和初始生活用品。",
        ]
        if goal == "Work":
            month2.insert(1, "打磨中英文简历和作品集，准备 LinkedIn、Wanted 或项目链接。")
            month2.insert(2, "通过校友、行业活动或线上社群建立韩国求职人脉。")
        lines.append("\n".join(f"- {item}" for item in month2))

        lines.append("\n### 第 3 个月：执行落地")
        month3 = []
        if goal == "Study":
            month3.append("提交大学申请，并同步申请奖学金。")
        elif goal == "Work":
            month3.append("开始投递岗位，准备韩国式面试和自我介绍。")
            month3.append("如果韩语达到 TOPIK 4+，可考虑大型企业或本土团队岗位。")
        else:
            month3.append("完善居住、医保、手机、银行和长期预算安排。")
        month3.append("确认住宿、健康保险和签证材料时间表。")
        month3.append("准备抵达后 3 个月清单：ARC 登记、电话卡、银行账户和生活服务。")
        lines.append("\n".join(f"- {item}" for item in month3))
        return "\n".join(lines)

    lines = []
    lines = []

    # Month 1
    lines.append("### Month 1 — Foundation")
    month1 = []
    if fin_risk == "High":
        month1.append("Create a detailed budget. Explore scholarship options (GKS, university-specific).")
        month1.append("Research part-time work options (student visa allows 20-25 hrs/week).")
    else:
        month1.append("Confirm your budget is adequate. Set up a Korean bank account (if in Korea).")

    if lang_risk == "High":
        month1.append(f"Begin intensive Korean language study. Target: TOPIK 2-3 within 3 months.")
    elif lang_risk == "Medium":
        month1.append("Enroll in a Korean language course or TOPIK preparation class.")

    if target_role and target_role != "Not Applicable":
        month1.append(f"Research {target_role} job market — identify target companies and required skills.")

    month1.append("Research housing options in your target city (Goshiwon, one-room, share houses).")
    lines.append("\n".join(f"- {item}" for item in month1))

    # Month 2
    lines.append("\n### Month 2 — Preparation")
    month2 = []
    month2.append("If studying: prepare application documents (transcripts, SOP, recommendation letters).")
    if goal == "Work":
        month2.append("Polish Korean/English resume. Prepare portfolio (GitHub, project links).")
        month2.append("Network via LinkedIn, Wanted, and Korean tech meetups.")
    month2.append("Research visa requirements: D-2 (study), E-7 (work), or D-10 (job seeker).")
    month2.append("Estimate total first-year costs including airfare, deposit, and initial setup.")
    lines.append("\n".join(f"- {item}" for item in month2))

    # Month 3
    lines.append("\n### Month 3 — Execution")
    month3 = []
    if goal == "Study":
        month3.append("Submit university applications. Apply for scholarships.")
    elif goal == "Work":
        month3.append("Start job applications. Prepare for Korean-style interviews.")
        month3.append("If TOPIK 4+, consider applying to chaebols (Samsung, Naver, Kakao).")
    month3.append("Arrange accommodation, health insurance, and visa paperwork.")
    month3.append("Set up a 3-month post-arrival checklist: ARC registration, phone, bank account.")
    lines.append("\n".join(f"- {item}" for item in month3))

    return "\n".join(lines)


def _generate_summary(rec: str, goal: str, city: str, monthly_cost: int, budget: int, korean_level: str, language: str = "en") -> str:
    """Generate a readable final summary."""
    if _language(language) == "zh":
        goal_label = _zh_goal(goal)
        city_label = _zh_city(city)
        summary_map = {
            "strongly_recommended": (
                f"韩国与你的{goal_label}目标高度匹配。你的预算 {budget:,} KRW "
                f"能够覆盖{city_label}约 {monthly_cost:,} KRW/月的估算成本。"
                f"建议继续准备并稳步推进。"
            ),
            "recommended_with_prep": (
                f"韩国对你的{goal_label}目标是可行选择，但仍有一些准备项需要加强。"
                f"你的预算 {budget:,} KRW 接近估算月成本 {monthly_cost:,} KRW。"
                f"建议先处理风险较高的部分，再做最终决定。"
            ),
            "risky": (
                f"韩国仍可能适合你的{goal_label}目标，但当前存在明显风险。"
                f"你的预算 {budget:,} KRW 可能不足以覆盖约 {monthly_cost:,} KRW/月的成本。"
                f"建议提高预算、调整城市/住房预期，或延长准备周期。"
            ),
            "not_recommended": (
                f"目前暂不建议立即推进韩国{goal_label}计划。"
                f"你的预算 {budget:,} KRW 低于{city_label}约 {monthly_cost:,} KRW/月的估算成本，"
                f"且多个风险项偏高。建议条件改善后再重新评估。"
            ),
        }
        return summary_map.get(rec, "请检查你的资料后重新生成报告。")

    summary_map = {
        "strongly_recommended": (
            f"Korea is a strong match for your {goal.lower()} goal. Your budget of {budget:,} KRW "
            f"covers estimated costs of {monthly_cost:,} KRW/month in {city}. "
            f"Continue preparing and proceed with confidence."
        ),
        "recommended_with_prep": (
            f"Korea is a viable option for your {goal.lower()} goal, but some areas need attention. "
            f"Your budget of {budget:,} KRW is close to the estimated {monthly_cost:,} KRW/month. "
            f"Address the identified risk areas before committing."
        ),
        "risky": (
            f"Korea could work for your {goal.lower()} goal, but significant risks exist. "
            f"Your budget of {budget:,} KRW may be insufficient for the estimated {monthly_cost:,} KRW/month. "
            f"Strongly consider increasing budget or adjusting expectations."
        ),
        "not_recommended": (
            f"Korea is not currently recommended for your {goal.lower()} goal. "
            f"Your budget of {budget:,} KRW is below the estimated {monthly_cost:,} KRW/month in {city}, "
            f"and multiple risk factors are elevated. Revisit this decision once conditions improve."
        ),
    }
    return summary_map.get(rec, "Review your profile and try again.")
