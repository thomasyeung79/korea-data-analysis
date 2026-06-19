"""
Career & Job Market Analyzer — configurable salary, skills, and recommendation data.

All amounts in KRW (annual). Based on published salary surveys and job postings analysis.
Sources: LinkedIn Salary, Glassdoor Korea, Startup Jobs Korea, Wanted.co.kr, JobKorea.

Salary ranges are directional estimates for foreign hires at Korean companies.
"""
from typing import Any

ROLES = [
    # IT (keep existing)
    "Data Analyst",
    "Backend Developer",
    "AI Product Manager",
    "AI Engineer",
    # Business (keep existing + new)
    "Marketing Specialist",
    "Accountant",
    "Business Analyst",
    "Operations Specialist",
    "Customer Support Specialist",
    "International Sales",
    "Product Manager",
    # Education (new)
    "English Teacher",
    "Chinese Teacher",
    # Medical (new)
    "Registered Nurse",
    "Care Worker",
    # Engineering (new)
    "Mechanical Engineer",
    "Electrical Engineer",
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
    "Accountant": ["Seoul", "Busan", "Daegu"],
    "English Teacher": ["Seoul", "Busan", "Daegu", "Daejeon"],
    "Chinese Teacher": ["Seoul", "Busan", "Daegu"],
    "Registered Nurse": ["Seoul", "Busan", "Daegu", "Daejeon", "Incheon"],
    "Care Worker": ["Seoul", "Busan", "Daegu", "Daejeon", "Incheon"],
    "Mechanical Engineer": ["Seoul", "Busan", "Daegu", "Daejeon", "Ulsan"],
    "Electrical Engineer": ["Seoul", "Busan", "Daegu", "Daejeon", "Ulsan"],
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
    "Accountant": {
        "Student": (22_000_000, 30_000_000),
        "0-2 years": (32_000_000, 45_000_000),
        "3-5 years": (45_000_000, 65_000_000),
    },
    "English Teacher": {
        "Student": (20_000_000, 28_000_000),
        "0-2 years": (25_000_000, 35_000_000),
        "3-5 years": (32_000_000, 45_000_000),
    },
    "Chinese Teacher": {
        "Student": (20_000_000, 28_000_000),
        "0-2 years": (25_000_000, 35_000_000),
        "3-5 years": (32_000_000, 45_000_000),
    },
    "Registered Nurse": {
        "Student": (22_000_000, 30_000_000),
        "0-2 years": (30_000_000, 42_000_000),
        "3-5 years": (40_000_000, 55_000_000),
    },
    "Care Worker": {
        "Student": (18_000_000, 25_000_000),
        "0-2 years": (24_000_000, 32_000_000),
        "3-5 years": (30_000_000, 42_000_000),
    },
    "Mechanical Engineer": {
        "Student": (24_000_000, 34_000_000),
        "0-2 years": (35_000_000, 50_000_000),
        "3-5 years": (50_000_000, 72_000_000),
    },
    "Electrical Engineer": {
        "Student": (24_000_000, 34_000_000),
        "0-2 years": (36_000_000, 52_000_000),
        "3-5 years": (52_000_000, 75_000_000),
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
    "Accountant": "TOPIK 5+ generally required for Korean accounting certifications and tax work. Some foreign firms may accept TOPIK 4.",
    "English Teacher": "TOPIK 3 minimum. Native English proficiency is the primary requirement. Korean ability helps with school communication.",
    "Chinese Teacher": "TOPIK 3 minimum. Native Chinese proficiency is the primary requirement. Korean ability helps with school communication.",
    "Registered Nurse": "TOPIK 5+ typically required for Korean nursing license and patient communication. English-only roles very limited.",
    "Care Worker": "TOPIK 4+ recommended for daily care communication. Demand growing due to aging population policy.",
    "Mechanical Engineer": "TOPIK 3 minimum. English-friendly R&D roles exist at chaebols. TOPIK 4 preferred for production coordination.",
    "Electrical Engineer": "TOPIK 3 minimum. English-friendly R&D roles exist at chaebols. TOPIK 4 preferred for production coordination.",
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
    "Accountant": {
        "must_have": [
            "Financial accounting",
            "Tax reporting",
            "Excel / ERP systems",
            "Korean accounting standards (K-IFRS)",
            "Detail-oriented documentation",
        ],
        "nice_to_have": [
            "CPA / AICPA / Korean tax accountant license",
            "Audit experience",
            "SAP / Oracle Financials",
            "Korean language (TOPIK 5+)",
        ],
    },
    "English Teacher": {
        "must_have": [
            "Native English proficiency",
            "TEFL / TESOL / CELTA certification",
            "Lesson planning",
            "Classroom management",
            "Cross-cultural communication",
        ],
        "nice_to_have": [
            "Experience with Korean students",
            "Kindergarten or adult education experience",
            "Curriculum development",
            "Korean language (TOPIK 3+)",
        ],
    },
    "Chinese Teacher": {
        "must_have": [
            "Native Chinese proficiency (Putonghua)",
            "Chinese language teaching certification",
            "Lesson planning",
            "Classroom management",
            "Cross-cultural communication",
        ],
        "nice_to_have": [
            "Experience with Korean students",
            "HSK / TCSOL certification",
            "Curriculum development",
            "Korean language (TOPIK 3+)",
        ],
    },
    "Registered Nurse": {
        "must_have": [
            "Registered Nurse license (eligible for Korean reciprocity)",
            "Patient care experience",
            "Clinical documentation",
            "Medical terminology",
            "Emergency response skills",
        ],
        "nice_to_have": [
            "Korean nursing license (Korean exam required)",
            "ICU / ER / surgical experience",
            "Bilingual medical communication",
            "Korean language (TOPIK 5+)",
        ],
    },
    "Care Worker": {
        "must_have": [
            "Caregiving experience",
            "Elderly or disability care",
            "Daily living support",
            "Basic first aid",
            "Patience and empathy",
        ],
        "nice_to_have": [
            "Korean Care Worker certification (Yoyangbohosa)",
            "Korean language (TOPIK 4+)",
            "Driving license (Korean or international)",
            "Experience with Korean elderly",
        ],
    },
    "Mechanical Engineer": {
        "must_have": [
            "CAD / SolidWorks / CATIA",
            "Mechanical design principles",
            "Manufacturing process knowledge",
            "FEA / simulation tools",
            "Technical documentation",
        ],
        "nice_to_have": [
            "Automotive or semiconductor equipment experience",
            "Korean engineering standards (KS)",
            "Project management (PMP)",
            "Korean language (TOPIK 3+)",
        ],
    },
    "Electrical Engineer": {
        "must_have": [
            "Circuit design",
            "PCB layout / Altium / OrCAD",
            "Embedded systems",
            "Signal integrity analysis",
            "Technical documentation",
        ],
        "nice_to_have": [
            "Semiconductor or display industry experience",
            "Korean engineering standards (KS)",
            "PLC / automation experience",
            "Korean language (TOPIK 3+)",
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
    "Accountant": {"Student": 7, "0-2 years": 6, "3-5 years": 5},
    "English Teacher": {"Student": 6, "0-2 years": 5, "3-5 years": 4},
    "Chinese Teacher": {"Student": 5, "0-2 years": 4, "3-5 years": 4},
    "Registered Nurse": {"Student": 8, "0-2 years": 7, "3-5 years": 6},
    "Care Worker": {"Student": 6, "0-2 years": 5, "3-5 years": 4},
    "Mechanical Engineer": {"Student": 7, "0-2 years": 6, "3-5 years": 5},
    "Electrical Engineer": {"Student": 7, "0-2 years": 6, "3-5 years": 5},
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
    "Accountant": "会计师",
    "English Teacher": "英语教师",
    "Chinese Teacher": "中文教师",
    "Registered Nurse": "注册护士",
    "Care Worker": "护理员",
    "Mechanical Engineer": "机械工程师",
    "Electrical Engineer": "电气工程师",
}

ZH_EXPERIENCE_LABELS = {
    "Student": "学生",
    "0-2 years": "0-2 年经验",
    "3-5 years": "3-5 年经验",
}

ZH_CITY_LABELS = {
    "Seoul": "首尔",
    "Busan": "釜山",
    "Incheon": "仁川",
    "Daejeon": "大田",
    "Daegu": "大邱",
    "Seongnam (Pangyo)": "城南（板桥）",
    "Ulsan": "蔚山",
}

ZH_COMPETITIVENESS_LABELS = {
    1: "很低：需求强，合格候选人较少",
    2: "低",
    3: "低于平均",
    4: "中等：有竞争，但技能匹配即可争取",
    5: "高于平均",
    6: "较高",
    7: "高：需要差异化优势",
    8: "很高",
    9: "竞争极高",
    10: "趋于饱和",
}


def _language(language: str) -> str:
    return "zh" if language == "zh" else "en"


def _zh_role(role: str) -> str:
    return ZH_ROLE_LABELS.get(role, role)


def _zh_exp(experience: str) -> str:
    return ZH_EXPERIENCE_LABELS.get(experience, experience)


def _localize_job_text(role: str, experience: str, korean_level: str, language: str) -> tuple[str, str, str]:
    if _language(language) != "zh":
        return (
            KOREAN_REQUIREMENTS.get(role, KOREAN_REQUIREMENTS["Backend Developer"]),
            KOREAN_GAP.get(korean_level, KOREAN_GAP["None"]),
            VISA_INFO.get(experience, VISA_INFO["0-2 years"]),
        )

    role_label = _zh_role(role)
    requirement = {
        "Data Analyst": "多数岗位至少需要 TOPIK 4。部分大型企业或外资公司存在英语友好岗位。",
        "Backend Developer": "通常建议 TOPIK 3 起步。科技创业公司和国际团队对英文更友好。",
        "AI Product Manager": "强烈建议 TOPIK 5+，因为需要大量韩语 stakeholder 沟通。",
        "AI Engineer": "TOPIK 3 起步较合适，许多研发团队可用英文协作，TOPIK 4 更有优势。",
        "Marketing Specialist": "建议 TOPIK 4+，常涉及韩文内容、市场调研和代理商协作。",
        "Business Analyst": "建议 TOPIK 4。英语友好岗位存在，但韩语访谈和需求沟通很常见。",
        "Operations Specialist": "建议 TOPIK 4+，便于供应商、物流和内部流程沟通。",
        "Customer Support Specialist": "面向韩国客户的支持岗位通常需要 TOPIK 4+。",
        "International Sales": "建议 TOPIK 3-4。英语或第三语言能力可弥补部分韩语不足。",
        "Product Manager": "建议 TOPIK 4-5，跨团队协作通常需要韩文文档和会议能力。",
        "Accountant": "会计类岗位通常需要 TOPIK 5+ 才能应对韩语会计认证和税务工作，部分外资企业可接受 TOPIK 4。",
        "English Teacher": "以母语英语能力为主，建议 TOPIK 3 以上，便于与学校沟通和日常生活。",
        "Chinese Teacher": "以母语中文能力为主，建议 TOPIK 3 以上，便于与学校沟通和日常生活。",
        "Registered Nurse": "护士岗位通常需要 TOPIK 5+，以获得韩国护士执照并与患者有效沟通。英语岗位非常有限。",
        "Care Worker": "建议 TOPIK 4+，日常护理需要与老人和家属顺畅沟通。韩国养老护理需求持续增长。",
        "Mechanical Engineer": "建议 TOPIK 3 起步，大型企业研发岗位有英语环境。TOPIK 4 更有利于生产管理岗位。",
        "Electrical Engineer": "建议 TOPIK 3 起步，大型企业研发岗位有英语环境。TOPIK 4 更有利于生产管理岗位。",
    }.get(role, f"{role_label} 岗位建议具备可工作的韩语沟通能力。")

    gap = {
        "None": "你目前更适合优先寻找英语优先的创业公司、外资企业或研究团队。若想进入更多韩国本土公司，建议尽快规划 TOPIK 学习。",
        "TOPIK 3": "你已有基础沟通能力，适合英语友好团队。提升到 TOPIK 4 会明显扩大可申请范围。",
        "TOPIK 4": "你具备中级韩语能力，适合多数中型公司的协作场景。大型企业可能仍偏好 TOPIK 5+。",
        "TOPIK 5+": "你的韩语能力较强，可竞争大型企业、产品管理和客户沟通类岗位。",
    }.get(korean_level, "建议根据目标岗位补齐韩语沟通能力。")

    visa = {
        "Student": "常见路径：D-2 学生签证 → D-10 求职签证 → E-7 特定活动签证。D-10 可提供毕业后的求职缓冲期。",
        "0-2 years": "常见路径：由雇主担保 E-7 特定活动签证。多数公司偏好 TOPIK 4+，之后可考虑 F-2 积分制居留。",
        "3-5 years": "常见路径：E-7 或 F-2 积分制居留。F-2 通常提供更高的就业流动性，长期可规划 F-5。",
    }.get(experience, "建议提前确认目标岗位是否支持签证担保。")
    return requirement, gap, visa


def analyze_job_market(role: str, experience: str, korean_level: str, language: str = "en") -> dict[str, Any]:
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
    korean_req, korean_gap, visa_info = _localize_job_text(role, experience, korean_level, language)
    comp_label = (
        ZH_COMPETITIVENESS_LABELS.get(competitiveness, "中等")
        if _language(language) == "zh"
        else COMPETITIVENESS_LABELS.get(competitiveness, "Average")
    )

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


def generate_preparation_plan(role: str, experience: str, korean_level: str, language: str = "en") -> str:
    """Generate a 3-month preparation plan."""
    if _language(language) == "zh":
        role_label = _zh_role(role)
        exp_label = _zh_exp(experience)
        lines = [
            f"## 3 个月准备计划：{role_label}（{exp_label}）",
            "",
            f"### 当前韩语水平：{korean_level}",
            "",
        ]
        if korean_level == "None":
            lines += [
                "**第 1 个月：** 启动 TOPIK 学习，报名线上或线下韩语课程。",
                "  - 重点：韩文字母、基础语法、日常会话（约 60 小时）。",
                "  - 目标：达到 TOPIK 1-2 的基础水平。",
                "",
                "**第 2 个月：** 继续语言学习，同时开始准备岗位相关作品集。",
                "  - 完成 2-3 个与韩国场景相关的项目或案例。",
                "  - 把项目整理到 GitHub、Notion 或个人作品集中。",
                "",
                "**第 3 个月：** 打磨简历并优先申请英语友好岗位。",
                "  - 目标：首尔英语优先创业公司、外资企业或国际团队。",
                "  - 渠道：LinkedIn、Wanted、RocketPunch 等。",
                "",
            ]
        elif korean_level in ("TOPIK 3", "TOPIK 4"):
            lines += [
                "**第 1 个月：** 强化岗位相关韩语表达，并更新面向韩国市场的简历。",
                "  - 准备韩文简历或让母语者审阅。",
                "  - 熟悉韩国面试和岗位沟通常见表达。",
                f"  - {'准备冲刺 TOPIK 4' if korean_level == 'TOPIK 3' else '可以考虑继续冲刺 TOPIK 5+'}。",
                "",
                "**第 2 个月：** 主动建立人脉并补齐技能差距。",
                "  - 参加韩国行业活动、线上社群或校友网络。",
                "  - 对照目标公司的岗位要求补齐 1-2 个关键技能。",
                "  - 整理目标公司名单和申请节奏。",
                "",
                "**第 3 个月：** 开始投递并准备面试。",
                "  - 通过 Wanted.co.kr、LinkedIn Korea、JobKorea 等渠道申请。",
                "  - 练习韩语自我介绍和岗位相关问答。",
                "  - 如果已在韩国，可关注 D-10 求职签证时间安排。",
                "",
            ]
        else:
            lines += [
                "**第 1 个月：** 打磨韩语表达和高价值人脉。",
                "  - 参加行业活动、技术分享或产品/商业社群。",
                "  - 准备韩语版作品集介绍。",
                "",
                "**第 2 个月：** 定向申请一线公司和高匹配岗位。",
                "  - 关注大型企业、头部创业公司和国际化团队。",
                "  - 请韩语母语者审阅简历和申请材料。",
                "  - 准备多轮面试：技能、业务理解、团队协作。",
                "",
                "**第 3 个月：** 比较 offer 并准备落地事项。",
                "  - 评估薪资、奖金、住房支持和签证担保。",
                "  - 确认 E-7 或 F-2 等签证路径。",
                "  - 规划住房、银行、医保和入职手续。",
                "",
            ]

        lines += [
            "### 关键洞察",
            f"- 薪资范围：{SALARY_GRID[role][experience][0]:,} - {SALARY_GRID[role][experience][1]:,} KRW/年",
            f"- 竞争强度：{COMPETITIVENESS.get(role, COMPETITIVENESS['Backend Developer'])[experience]}/10",
            "- 技能匹配度是获得面试和 offer 的关键因素。",
            "- 韩语能力会显著扩大职业选择空间。",
        ]
        return "\n".join(lines)

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
