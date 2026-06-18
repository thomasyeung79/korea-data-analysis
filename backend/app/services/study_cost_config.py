"""
Study Cost Calculator — configurable cost constants.

All amounts in KRW (South Korean Won) per month unless noted.
Tuition is annual; converted to monthly in calculations.

Source: Directional estimates based on published data from:
  - Korean Ministry of Education
  - Studentyook (university cost guides)
  - Numbeo cost of living
  - Various university international office pages
"""

# ── City base costs (monthly living, excluding tuition/housing) ──
# These cover food + transport + insurance + misc baseline
CITY_BASE_COST = {
    "Seoul": 650_000,
    "Busan": 500_000,
    "Daejeon": 480_000,
    "Daegu": 470_000,
    "Other": 430_000,
}

# ── Housing costs by city × type (monthly, KRW) ──
HOUSING_COST = {
    "Seoul": {
        "Dormitory": 350_000,
        "Shared Apartment": 550_000,
        "Studio Apartment": 750_000,
    },
    "Busan": {
        "Dormitory": 280_000,
        "Shared Apartment": 400_000,
        "Studio Apartment": 550_000,
    },
    "Daejeon": {
        "Dormitory": 250_000,
        "Shared Apartment": 370_000,
        "Studio Apartment": 500_000,
    },
    "Daegu": {
        "Dormitory": 240_000,
        "Shared Apartment": 360_000,
        "Studio Apartment": 480_000,
    },
    "Other": {
        "Dormitory": 200_000,
        "Shared Apartment": 300_000,
        "Studio Apartment": 420_000,
    },
}

# ── Annual tuition by school type (KRW) ──
# Language School: 10-week term × 4 = annual
TUITION_ANNUAL = {
    "Language School": 5_600_000,
    "Undergraduate": 6_500_000,
    "Graduate School": 7_200_000,
}

# ── Lifestyle multipliers (applied to food + misc portion of base cost) ──
LIFESTYLE_FACTOR = {
    "Budget": 0.75,
    "Standard": 1.0,
    "Premium": 1.45,
}

# ── Cost breakdown proportions (percentage of CITY_BASE_COST after lifestyle) ──
BREAKDOWN_RATIOS = {
    "Food": 0.42,
    "Transportation": 0.15,
    "Insurance": 0.13,
    "Miscellaneous": 0.30,
}


def calculate_costs(city: str, school_type: str, housing_type: str, lifestyle: str) -> dict:
    """Calculate monthly and annual costs with breakdown."""
    if city not in CITY_BASE_COST:
        city = "Other"
    if school_type not in TUITION_ANNUAL:
        school_type = "Undergraduate"
    if housing_type not in HOUSING_COST.get(city, HOUSING_COST["Other"]):
        housing_type = "Shared Apartment"
    if lifestyle not in LIFESTYLE_FACTOR:
        lifestyle = "Standard"

    # Base monthly (food + transport + insurance + misc baseline)
    base = CITY_BASE_COST[city]

    # Apply lifestyle factor
    lifestyle_mult = LIFESTYLE_FACTOR[lifestyle]
    living_base = base * lifestyle_mult

    # Monthly tuition
    tuition_monthly = TUITION_ANNUAL[school_type] / 12

    # Monthly housing
    housing_monthly = HOUSING_COST[city][housing_type]

    # Breakdown from living_base
    food = round(living_base * BREAKDOWN_RATIOS["Food"])
    transport = round(living_base * BREAKDOWN_RATIOS["Transportation"])
    insurance = round(living_base * BREAKDOWN_RATIOS["Insurance"])
    misc = round(living_base * BREAKDOWN_RATIOS["Miscellaneous"])

    monthly_total = round(tuition_monthly + housing_monthly + food + transport + insurance + misc)
    annual_total = round(monthly_total * 12)

    breakdown = {
        "Tuition": round(tuition_monthly),
        "Housing": housing_monthly,
        "Food": food,
        "Transportation": transport,
        "Insurance": insurance,
        "Miscellaneous": misc,
    }

    return {
        "monthly_cost": monthly_total,
        "annual_cost": annual_total,
        "breakdown": breakdown,
        "currency": "KRW",
    }


def generate_cost_explanation(city: str, school_type: str, housing_type: str,
                               lifestyle: str, result: dict) -> str:
    """Generate a human-readable explanation of the cost estimate."""
    b = result["breakdown"]
    max_cat = max(b, key=b.get)
    pct = round(b[max_cat] / result["monthly_cost"] * 100)

    lines = [
        f"Your estimated monthly cost for {school_type.lower()} in {city} "
        f"is **{result['monthly_cost']:,} KRW** (≈ {result['monthly_cost'] // 1200:,} USD).",
        "",
        f"The largest expense is **{max_cat}** at {b[max_cat]:,} KRW/month ({pct}% of total).",
        "",
        "### Monthly breakdown",
    ]
    for cat, amount in b.items():
        p = round(amount / result["monthly_cost"] * 100)
        lines.append(f"- **{cat}**: {amount:,} KRW ({p}%)")

    lines.extend([
        "",
        f"### Annual estimate",
        f"**{result['annual_cost']:,} KRW** (≈ {result['annual_cost'] // 1200:,} USD) per year.",
        "",
        "### Notes",
        "- Tuition varies significantly by university and program.",
        "- Housing costs depend on deposit (key money), location, and season.",
        "- Health insurance for international students is mandatory (approx. 70,000–100,000 KRW/month).",
        "- These are directional estimates. Actual costs may vary ±20%.",
    ])

    return "\n".join(lines)
