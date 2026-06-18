"""
Decision Report Engine — combines study cost + job market analysis into a
personalised recommendation for studying, working, or living in Korea.

Reuses calculation logic from:
  - study_cost_config.py (calculate_costs)
  - job_market_config.py (analyze_job_market)

No external APIs. Rule-based recommendation engine.
"""

from study_cost_config import calculate_costs, CITY_BASE_COST, HOUSING_COST
from job_market_config import analyze_job_market, SALARY_GRID, COMPETITIVENESS

GOALS = ["Study", "Work", "Live"]

RECOMMENDATION_LABELS = {
    "strongly_recommended": "Strongly Recommended ✅",
    "recommended_with_prep": "Recommended with Preparation ⚠️",
    "risky": "Risky ❓",
    "not_recommended": "Not Recommended Yet ❌",
}


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


def _language_risk(korean_level: str, goal: str) -> tuple[str, str]:
    """Assess language risk based on goal and current level."""
    level_map = {"None": 0, "TOPIK 3": 3, "TOPIK 4": 4, "TOPIK 5+": 5}
    level = level_map.get(korean_level, 0)

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
        return "High", f"{info['label']} Your current level ({korean_level}) is below the recommended threshold."


def _career_risk(role: str, competitiveness: int) -> tuple[str, str]:
    """Assess career risk based on competitiveness score."""
    if role == "Not Applicable" or not role:
        return "Low", "Career assessment not applicable to your goal."
    if competitiveness <= 5:
        return "Low", f"Competitiveness score {competitiveness}/10 — favourable job market conditions."
    elif competitiveness <= 7:
        return "Medium", f"Competitiveness score {competitiveness}/10 — resume differentiation recommended."
    else:
        return "High", f"Competitiveness score {competitiveness}/10 — requires strong preparation and networking."


def _visa_living_risk(goal: str, monthly_budget: int, monthly_cost: int) -> tuple[str, str]:
    """Assess visa and living risk."""
    gap = monthly_budget - monthly_cost
    factors = []
    if gap < 0:
        factors.append("Monthly budget is below estimated living costs.")
    if goal == "Work":
        factors.append("E-7 visa requires employer sponsorship. Job search can take 3-6 months.")
    elif goal == "Study":
        factors.append("D-2 visa requires proof of funds (typically $20,000+ in bank account).")
    if len(factors) == 0:
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
    lang_risk, lang_detail = _language_risk(korean_level, goal)
    car_risk, car_detail = _career_risk(target_role, competitiveness)
    visa_risk, visa_detail = _visa_living_risk(goal, monthly_budget, monthly_cost)

    overall = _recommendation_classifier(fin_risk, lang_risk, car_risk, visa_risk, monthly_budget, monthly_cost)

    # ── 4. Action plan ──
    action_plan = _generate_action_plan(goal, fin_risk, lang_risk, korean_level, target_role)

    # ── 5. Final summary ──
    summary = _generate_summary(overall, goal, target_city, monthly_cost, monthly_budget, korean_level)

    return {
        "recommendation": overall,
        "recommendation_label": RECOMMENDATION_LABELS[overall],
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


def _generate_action_plan(goal: str, fin_risk: str, lang_risk: str, korean_level: str, target_role: str) -> str:
    """Generate a structured 3-month action plan."""
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


def _generate_summary(rec: str, goal: str, city: str, monthly_cost: int, budget: int, korean_level: str) -> str:
    """Generate a readable final summary."""
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
