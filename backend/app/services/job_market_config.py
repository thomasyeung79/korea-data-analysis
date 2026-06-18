"""
Career & Job Market Analyzer — configurable salary, skills, and recommendation data.

All amounts in KRW (annual). Based on published salary surveys and job postings analysis.
Sources: LinkedIn Salary, Glassdoor Korea, Startup Jobs Korea, Wanted.co.kr, JobKorea.

Salary ranges are directional estimates for foreign hires at Korean companies.
"""
from typing import Any

ROLES = [
    "Data Analyst",
    "Backend Developer",
    "AI Product Manager",
    "AI Engineer",
    "Marketing Specialist",
    "Business Analyst",
    "Operations Specialist",
    "Customer Support Specialist",
    "International Sales",
    "Product Manager",
]

EXPERIENCE_LEVELS = ["Student", "0-2 years", "3-5 years"]

KOREAN_LEVELS = ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"]

CITIES_BY_ROLE = {
    "Data Analyst": ["Seoul", "Seongnam (Pangyo)", "Busan"],
    "Backend Developer": ["Seoul", "Seongnam (Pangyo)", "Busan", "Daejeon"],
    "AI Product Manager": ["Seoul", "Seongnam (Pangyo)"],
    "AI Engineer": ["Seoul", "Seongnam (Pangyo)", "Daejeon"],
    "Marketing Specialist": ["Seoul", "Busan", "Incheon"],
    "Business Analyst": ["Seoul", "Seongnam (Pangyo)", "Busan"],
    "Operations Specialist": ["Seoul", "Incheon", "Busan"],
    "Customer Support Specialist": ["Seoul", "Busan", "Daegu"],
    "International Sales": ["Seoul", "Incheon", "Busan"],
    "Product Manager": ["Seoul", "Seongnam (Pangyo)", "Busan"],
}

# salary_grid[role][experience] = (min_annual_krw, max_annual_krw)
SALARY_GRID: dict[str, dict[str, tuple[int, int]]] = {
    "Data Analyst": {
        "Student": (20_000_000, 30_000_000),
        "0-2 years": (32_000_000, 45_000_000),
        "3-5 years": (45_000_000, 65_000_000),
    },
    "Backend Developer": {
        "Student": (24_000_000, 35_000_000),
        "0-2 years": (38_000_000, 55_000_000),
        "3-5 years": (55_000_000, 85_000_000),
    },
    "AI Product Manager": {
        "Student": (25_000_000, 36_000_000),
        "0-2 years": (40_000_000, 58_000_000),
        "3-5 years": (60_000_000, 90_000_000),
    },
    "AI Engineer": {
        "Student": (28_000_000, 40_000_000),
        "0-2 years": (45_000_000, 65_000_000),
        "3-5 years": (65_000_000, 100_000_000),
    },
    "Marketing Specialist": {
        "Student": (20_000_000, 28_000_000),
        "0-2 years": (30_000_000, 42_000_000),
        "3-5 years": (42_000_000, 60_000_000),
    },
    "Business Analyst": {
        "Student": (22_000_000, 32_000_000),
        "0-2 years": (34_000_000, 48_000_000),
        "3-5 years": (48_000_000, 70_000_000),
    },
    "Operations Specialist": {
        "Student": (20_000_000, 30_000_000),
        "0-2 years": (32_000_000, 45_000_000),
        "3-5 years": (45_000_000, 62_000_000),
    },
    "Customer Support Specialist": {
        "Student": (18_000_000, 27_000_000),
        "0-2 years": (28_000_000, 38_000_000),
        "3-5 years": (38_000_000, 52_000_000),
    },
    "International Sales": {
        "Student": (22_000_000, 32_000_000),
        "0-2 years": (35_000_000, 52_000_000),
        "3-5 years": (52_000_000, 78_000_000),
    },
    "Product Manager": {
        "Student": (24_000_000, 35_000_000),
        "0-2 years": (38_000_000, 55_000_000),
        "3-5 years": (55_000_000, 82_000_000),
    },
}

# Korean language requirements by role
KOREAN_REQUIREMENTS: dict[str, str] = {
    "Data Analyst": "TOPIK 4 minimum for most roles. Some English-only positions at chaebols or foreign companies.",
    "Backend Developer": "TOPIK 3 minimum. Strong English alternatives exist at tech startups and global firms.",
    "AI Product Manager": "TOPIK 5+ strongly recommended. Heavy Korean-language stakeholder communication.",
    "AI Engineer": "TOPIK 3 minimum. Many R&D labs operate in English. TOPIK 4 preferred for collaboration.",
    "Marketing Specialist": "TOPIK 4+ recommended. Korean copy, market research, and agency coordination are common.",
    "Business Analyst": "TOPIK 4 recommended. English-friendly roles exist, but Korean stakeholder interviews are common.",
    "Operations Specialist": "TOPIK 4+ recommended for vendor, logistics, and internal process communication.",
    "Customer Support Specialist": "TOPIK 4+ usually required for Korean customer-facing support teams.",
    "International Sales": "TOPIK 3-4 recommended. English plus another language can offset lower Korean in global accounts.",
    "Product Manager": "TOPIK 4-5 recommended. Cross-functional coordination often requires Korean documentation and meetings.",
}

# Language gap: what missing Korean means
KOREAN_GAP: dict[str, str] = {
    "None": "You will be limited to English-first startups, foreign companies, or research labs. Chaebols and most Korean SMEs require TOPIK 4+.",
    "TOPIK 3": "Entry-level conversational ability. Suitable for tech roles with English-friendly teams. Topik 4+ opens significantly more doors.",
    "TOPIK 4": "Intermediate. Sufficient for most tech roles at mid-size Korean companies. Some chaebols may still prefer TOPIK 5+.",
    "TOPIK 5+": "Advanced. Competitive for most roles including chaebols, product management, and client-facing positions.",
}

# Required skills by role
SKILL_REQUIREMENTS: dict[str, dict[str, list[str]]] = {
    "Data Analyst": {
        "must_have": [
            "SQL",
            "Python (Pandas, NumPy)",
            "Data visualisation (Tableau / Looker / Matplotlib)",
            "Statistical analysis",
            "Excel / Google Sheets",
        ],
        "nice_to_have": [
            "Airflow / ETL pipelines",
            "BigQuery / Snowflake",
            "Machine learning basics",
            "Korean language (TOPIK 4+)",
        ],
    },
    "Backend Developer": {
        "must_have": [
            "Python (Django / FastAPI) or Java (Spring Boot)",
            "REST API design",
            "Database design (PostgreSQL / MySQL)",
            "Git / GitHub Actions / CI-CD",
            "Docker / Kubernetes basics",
        ],
        "nice_to_have": [
            "Cloud (AWS / GCP)",
            "Message queues (Kafka / RabbitMQ)",
            "Microservices architecture",
            "Korean language (TOPIK 3+)",
        ],
    },
    "AI Product Manager": {
        "must_have": [
            "Product management experience (3+ years)",
            "Understanding of ML / AI lifecycle",
            "Data-driven decision-making (A/B testing, metrics)",
            "Stakeholder management",
            "English + Korean bilingual (TOPIK 5+)",
        ],
        "nice_to_have": [
            "Technical background (CS degree or equivalent)",
            "Experience with Korean tech ecosystem",
            "JIRA / Confluence / Notion",
            "Figma / product design tools",
        ],
    },
    "AI Engineer": {
        "must_have": [
            "Python (PyTorch / TensorFlow)",
            "Machine learning fundamentals",
            "Deep learning (NLP / CV / LLMs)",
            "SQL and data pipeline basics",
            "Git, Linux, cloud basics",
        ],
        "nice_to_have": [
            "Published research or open-source contributions",
            "Korean language (TOPIK 3+)",
            "Kubernetes / MLOps (MLflow, Kubeflow)",
            "Experience with large Korean datasets",
        ],
    },
    "Marketing Specialist": {
        "must_have": [
            "Campaign planning",
            "Content marketing",
            "Market research",
            "Google Analytics / GA4",
            "Korean consumer trend awareness",
        ],
        "nice_to_have": [
            "Naver Ads / Kakao Ads",
            "SEO / ASO",
            "CRM tools",
            "Korean language (TOPIK 4+)",
        ],
    },
    "Business Analyst": {
        "must_have": [
            "Excel / Google Sheets",
            "SQL basics",
            "Process mapping",
            "Dashboarding",
            "Stakeholder communication",
        ],
        "nice_to_have": [
            "Tableau / Power BI",
            "Korean market research",
            "Consulting experience",
            "Korean language (TOPIK 4+)",
        ],
    },
    "Operations Specialist": {
        "must_have": [
            "Process operations",
            "Vendor coordination",
            "Excel / reporting",
            "SOP documentation",
            "Problem solving",
        ],
        "nice_to_have": [
            "Logistics / supply chain experience",
            "ERP tools",
            "Project coordination",
            "Korean language (TOPIK 4+)",
        ],
    },
    "Customer Support Specialist": {
        "must_have": [
            "Customer communication",
            "Ticketing systems",
            "Product troubleshooting",
            "Documentation",
            "Empathy and escalation handling",
        ],
        "nice_to_have": [
            "Zendesk / Intercom",
            "Bilingual support experience",
            "SaaS product knowledge",
            "Korean language (TOPIK 4+)",
        ],
    },
    "International Sales": {
        "must_have": [
            "B2B sales process",
            "Lead generation",
            "Pipeline management",
            "Presentation skills",
            "Cross-cultural communication",
        ],
        "nice_to_have": [
            "CRM tools",
            "Export / trade knowledge",
            "Negotiation experience",
            "Korean language (TOPIK 3+)",
        ],
    },
    "Product Manager": {
        "must_have": [
            "Product discovery",
            "Roadmapping",
            "User research",
            "Metrics and experimentation",
            "Cross-functional communication",
        ],
        "nice_to_have": [
            "Figma / prototyping",
            "SQL / analytics",
            "Korean market experience",
            "Korean language (TOPIK 4+)",
        ],
    },
}

# Competitiveness scores (1-10) by role and experience
COMPETITIVENESS: dict[str, dict[str, int]] = {
    "Data Analyst": {"Student": 7, "0-2 years": 6, "3-5 years": 5},
    "Backend Developer": {"Student": 8, "0-2 years": 7, "3-5 years": 5},
    "AI Product Manager": {"Student": 6, "0-2 years": 5, "3-5 years": 4},
    "AI Engineer": {"Student": 7, "0-2 years": 6, "3-5 years": 4},
    "Marketing Specialist": {"Student": 7, "0-2 years": 6, "3-5 years": 5},
    "Business Analyst": {"Student": 7, "0-2 years": 6, "3-5 years": 5},
    "Operations Specialist": {"Student": 6, "0-2 years": 5, "3-5 years": 4},
    "Customer Support Specialist": {"Student": 6, "0-2 years": 5, "3-5 years": 4},
    "International Sales": {"Student": 6, "0-2 years": 5, "3-5 years": 4},
    "Product Manager": {"Student": 7, "0-2 years": 6, "3-5 years": 5},
}

COMPETITIVENESS_LABELS = {
    1: "Very Low — strong demand, few qualified candidates",
    2: "Low",
    3: "Below Average",
    4: "Average — competitive but achievable with right skills",
    5: "Above Average",
    6: "Moderately High",
    7: "High — requires differentiation",
    8: "Very High",
    9: "Extremely Competitive",
    10: "Saturated",
}

# Visa pathways
VISA_INFO = {
    "Student": "D-2 (Student visa) → D-10 (Job seeker) → E-7 (Specific activity). D-10 gives 6-12 months to find a job.",
    "0-2 years": "E-7 (Specific activity) sponsored by employer. Requires TOPIK 4+ for most companies. F-2 (Points-based) possible after 1 year.",
    "3-5 years": "E-7 or F-2 (Points-based residency). F-2 allows job mobility. F-5 (Permanent resident) possible after 5 years.",
}


def analyze_job_market(role: str, experience: str, korean_level: str) -> dict[str, Any]:
    """Analyze job market for given role/experience/korean combination."""
    if role not in SALARY_GRID:
        role = "Backend Developer"
    if experience not in EXPERIENCE_LEVELS:
        experience = "0-2 years"
    if korean_level not in KOREAN_LEVELS:
        korean_level = "None"

    sal_min, sal_max = SALARY_GRID[role][experience]
    skills = SKILL_REQUIREMENTS.get(role, SKILL_REQUIREMENTS["Backend Developer"])
    cities = CITIES_BY_ROLE.get(role, CITIES_BY_ROLE["Backend Developer"])
    competitiveness = COMPETITIVENESS.get(role, COMPETITIVENESS["Backend Developer"])[experience]
    korean_req = KOREAN_REQUIREMENTS.get(role, KOREAN_REQUIREMENTS["Backend Developer"])
    korean_gap = KOREAN_GAP.get(korean_level, KOREAN_GAP["None"])
    visa_info = VISA_INFO.get(experience, VISA_INFO["0-2 years"])
    comp_label = COMPETITIVENESS_LABELS.get(competitiveness, "Average")

    return {
        "salary_min": sal_min,
        "salary_max": sal_max,
        "recommended_cities": cities,
        "required_skills": skills["must_have"],
        "nice_to_have_skills": skills["nice_to_have"],
        "korean_language_requirement": korean_req,
        "korean_language_gap": korean_gap,
        "competitiveness": competitiveness,
        "competitiveness_label": comp_label,
        "visa_pathway": visa_info,
        "currency": "KRW",
    }


def generate_preparation_plan(role: str, experience: str, korean_level: str) -> str:
    """Generate a 3-month preparation plan."""
    lines = [
        f"## 3-Month Preparation Plan: {role} ({experience})",
        "",
        f"### Korean Level: {korean_level}",
        "",
    ]

    if korean_level == "None":
        lines += [
            "**Month 1:** Begin TOPIK preparation. Join a Korean language class (online or local).",
            "  - Focus: Hangul, basic grammar, daily conversation (60 hours).",
            "  - Goal: TOPIK 1-2 level proficiency.",
            "",
            "**Month 2:** Continue language study + start portfolio projects.",
            "  - Build 2-3 Korean-relevant projects (e.g., Korean data analysis using public datasets).",
            "  - Contribute to open-source projects visible to Korean companies.",
            "",
            "**Month 3:** Polish portfolio + apply to English-friendly roles.",
            "  - Target: English-first startups in Seoul (e.g., Channel Talk, Sendbird).",
            "  - Apply through LinkedIn, Wanted, and RocketPunch.",
            "",
        ]
    elif korean_level in ("TOPIK 3", "TOPIK 4"):
        lines += [
            "**Month 1:** Strengthen Korean technical vocabulary + update resume for Korean market.",
            "  - Translate resume/CV to Korean (professional review recommended).",
            "  - Study Korean tech interview questions (available on Naver Blog, JobKorea).",
            f"  - {'Prepare TOPIK 4 exam' if korean_level == 'TOPIK 3' else 'Consider TOPIK 5+ for chaebol eligibility'}.",
            "",
            "**Month 2:** Active networking + skills alignment.",
            "  - Join Korean tech meetups (Seoul Global Center, Startup Alliance).",
            "  - Complete 1-2 Korean-language technical courses (K-MOOC or Fast Campus).",
            "  - Research target companies and their tech stacks.",
            "",
            "**Month 3:** Start applications + interview preparation.",
            "  - Apply through Wanted.co.kr, LinkedIn Korea, JobKorea.",
            "  - Practice Korean technical interviews with native speakers.",
            "  - Leverage D-10 job seeker visa if already in Korea.",
            "",
        ]
    else:  # TOPIK 5+
        lines += [
            "**Month 1:** Polish Korean fluency + high-value networking.",
            "  - Join industry-specific groups (Naver D2, Kakao Tech Meetups).",
            "  - Attend Korean tech conferences (DEVIEW, IF KAKAO, NVIDIA GTC Korea).",
            "  - Prepare Korean-language portfolio presentation.",
            "",
            "**Month 2:** Targeted applications to tier-1 companies.",
            "  - Apply to chaebols (Samsung, LG, SK, Naver, Kakao) and top startups.",
            "  - Have a Korean speaker review all application materials.",
            "  - Prepare for multi-round interviews (coding + culture + presentation).",
            "",
            "**Month 3:** Negotiate offers + prepare relocation.",
            "  - Compare total compensation (housing, stock options, bonuses).",
            "  - Secure visa sponsorship (E-7 or F-2 points-based).",
            "  - Plan housing, banking, and healthcare setup in Seoul.",
            "",
        ]

    lines += [
        "### Key insights",
        f"- Salary range: {SALARY_GRID[role][experience][0]:,} - {SALARY_GRID[role][experience][1]:,} KRW/year",
        f"- Competitiveness: {COMPETITIVENESS.get(role, COMPETITIVENESS['Backend Developer'])[experience]}/10",
        "- Skills alignment is the strongest predictor of job offer success.",
        "- Korean language ability is the largest unlock factor for career growth.",
    ]

    return "\n".join(lines)
