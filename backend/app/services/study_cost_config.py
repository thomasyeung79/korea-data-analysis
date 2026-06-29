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
from . import data_loader

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
        city = _add_city_from_knowledge_base(city)
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


def _add_city_from_knowledge_base(city: str) -> str:
    try:
        record = data_loader.load_city(city)
    except Exception:
        return "Other"

    city_name = record["city_name"]
    if city_name not in CITY_BASE_COST:
        insurance = 90000
        misc = 180000
        CITY_BASE_COST[city_name] = int(record["average_food_cost"] + record["transport_cost"] + insurance + misc)
        rent = int(record["average_rent"])
        HOUSING_COST[city_name] = {
            "Dormitory": max(200000, int(rent * 0.55)),
            "Shared Apartment": rent,
            "Studio Apartment": int(rent * 1.25),
        }
    return city_name


ZH_LABELS = {
    "Seoul": "首尔",
    "Busan": "釜山",
    "Daejeon": "大田",
    "Daegu": "大邱",
    "Other": "其他城市",
    "Language School": "语言学校",
    "Undergraduate": "本科",
    "Graduate School": "研究生院",
    "Dormitory": "宿舍",
    "Shared Apartment": "合租公寓",
    "Studio Apartment": "单间公寓",
    "Budget": "节省型",
    "Standard": "标准型",
    "Premium": "高品质",
    "Tuition": "学费",
    "Housing": "住宿",
    "Food": "饮食",
    "Transportation": "交通",
    "Insurance": "保险",
    "Miscellaneous": "其他",
}


def _language(language: str) -> str:
    return "zh" if language == "zh" else "en"


def _zh(value: str) -> str:
    return ZH_LABELS.get(value, value)


def generate_cost_explanation(city: str, school_type: str, housing_type: str,
                               lifestyle: str, result: dict, language: str = "en") -> str:
    """Generate a human-readable explanation of the cost estimate."""
    b = result["breakdown"]
    max_cat = max(b, key=b.get)
    pct = round(b[max_cat] / result["monthly_cost"] * 100)

    if _language(language) == "zh":
        lines = [
            f"你在{_zh(city)}选择{_zh(school_type)}、{_zh(housing_type)}和{_zh(lifestyle)}生活方式时，",
            f"预计月度总成本为 **{result['monthly_cost']:,} KRW**（约 {result['monthly_cost'] // 1200:,} USD）。",
            "",
            f"最大支出项是 **{_zh(max_cat)}**，约 {b[max_cat]:,} KRW/月，占总成本 {pct}%。",
            "",
            "## 月度费用明细",
        ]
        for cat, amount in b.items():
            p = round(amount / result["monthly_cost"] * 100)
            lines.append(f"- **{_zh(cat)}**：{amount:,} KRW（{p}%）")

        lines.extend([
            "",
            "## 年度费用估算",
            f"预计每年约 **{result['annual_cost']:,} KRW**（约 {result['annual_cost'] // 1200:,} USD）。",
            "",
            "## 温馨提示",
            "- 学费会因大学、专业和奖学金情况明显变化。",
            "- 住房成本受押金、地段和入住季节影响较大。",
            "- 国际学生通常需要加入韩国健康保险。",
            "- 以上为方向性估算，实际成本可能上下浮动约 20%。",
        ])
        return "\n".join(lines)

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
