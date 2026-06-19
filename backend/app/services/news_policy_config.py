"""
News & Policy — curated mock news items for MVP.

No external API calls. All data is static and directional.
Topics cover study, work, visa, economy, and technology developments in Korea.

Each item:
  - title
  - category: Study / Work / Visa / Economy / Technology
  - source_name
  - published_at (YYYY-MM-DD relative to ~2026-06-01)
  - summary
  - impact_for_students
  - impact_for_job_seekers
  - source_url (placeholder)
  - tags (list of keywords for matching)
"""

from datetime import datetime, timedelta

CATEGORIES = ["Study", "Work", "Visa", "Economy", "Technology"]

TIME_RANGES = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
}

ZH_CATEGORY_LABELS = {
    "Study": "留学",
    "Work": "工作",
    "Visa": "签证",
    "Economy": "经济",
    "Technology": "科技",
}


def _language(language: str) -> str:
    return "zh" if language == "zh" else "en"


def _zh_category(category: str) -> str:
    return ZH_CATEGORY_LABELS.get(category, category)

# Base date for mock items
BASE_DATE = datetime(2026, 6, 1)

RAW_ITEMS = [
    {
        "title": "D-10 Job Seeker Visa Extended to 12 Months for STEM Graduates",
        "category": "Visa",
        "source_name": "Korea Immigration Service",
        "days_ago": 5,
        "summary": "The Korean Ministry of Justice extended the D-10 job seeker visa from 6 to 12 months for graduates in STEM fields (science, technology, engineering, mathematics). Applicants must hold a bachelor's degree or higher from a Korean university.",
        "impact_for_students": "STEM graduates now have double the time to secure employment after graduation. This reduces pressure during the job search period.",
        "impact_for_job_seekers": "Non-STEM graduates still receive 6 months. Consider pursuing additional qualifications or language training to extend eligibility.",
        "tags": ["visa", "D-10", "STEM", "graduate", "job seeker"],
    },
    {
        "title": "2026 GKS Scholarship Applications Open — 2,000 International Slots",
        "category": "Study",
        "source_name": "Korean Ministry of Education",
        "days_ago": 12,
        "summary": "The Global Korea Scholarship (GKS) program announced 2,000 slots for international undergraduate and graduate students for the 2027 academic year. Applications close in October 2026. Benefits include full tuition, monthly stipend, airfare, and Korean language training.",
        "impact_for_students": "Significant funding opportunity. Prepare application materials early — recommendation letters and academic transcripts are critical.",
        "impact_for_job_seekers": "Not directly applicable. However, GKS alumni often receive preferential hiring at Korean government-affiliated organisations.",
        "tags": ["scholarship", "GKS", "international student", "funding", "university"],
    },
    {
        "title": "Topik 4 Now Mandatory for E-7 Visa Sponsorship at SMEs",
        "category": "Visa",
        "source_name": "Ministry of Justice",
        "days_ago": 8,
        "summary": "Starting July 2026, small and medium-sized enterprises (SMEs) sponsoring E-7 foreign workers must verify the applicant has TOPIK 4 or higher. Previously, SMEs could sponsor with TOPIK 3. Large corporations already required TOPIK 4+.",
        "impact_for_students": "Plan Korean language study accordingly. TOPIK 4 should be the minimum target even if not immediately required for your current visa.",
        "impact_for_job_seekers": "This raises the bar for SME employment. TOPIK 4 is now essentially mandatory for most sponsored work visas. Budget 6-12 months of language study.",
        "tags": ["visa", "E-7", "TOPIK", "SME", "language requirement"],
    },
    {
        "title": "NVIDIA and Samsung Partner on AI Semiconductor Research Hub in Seoul",
        "category": "Technology",
        "source_name": "Korea Herald",
        "days_ago": 3,
        "summary": "NVIDIA and Samsung Electronics announced a joint AI semiconductor research centre in Seoul's Gangnam district. The hub will employ 300+ researchers focusing on AI chip design, LLM optimisation, and memory architecture. Hiring begins Q3 2026.",
        "impact_for_students": "New internship and research assistant opportunities for engineering and CS students. Consider specialising in AI/ML hardware.",
        "impact_for_job_seekers": "Strong signal for AI hardware and semiconductor roles. Samsung and NVIDIA will compete for top talent in Seoul. English-friendly R&D environment expected.",
        "tags": ["AI", "semiconductor", "NVIDIA", "Samsung", "tech jobs", "research"],
    },
    {
        "title": "Seoul Metropolitan Area Housing Costs Rise 8% Year-on-Year",
        "category": "Economy",
        "source_name": "KB Kookmin Bank Research",
        "days_ago": 10,
        "summary": "Average monthly rent in Seoul increased 8% compared to Q1 2025. Studio apartments now average 750,000-900,000 KRW/month in popular areas. Goshiwon rates remain stable at 300,000-500,000 KRW/month. Jeonse deposits also increased 5%.",
        "impact_for_students": "Budget an extra 50,000-100,000 KRW/month compared to last year. Consider Goshiwon or shared apartments as cost-saving options.",
        "impact_for_job_seekers": "Housing cost is a significant factor in salary negotiation. If relocating, budget for increased deposit requirements. Consider Bundang or Incheon as lower-cost alternatives.",
        "tags": ["housing", "Seoul", "rent", "cost of living", "economy"],
    },
    {
        "title": "Korean Government Invests 2.3 Trillion KRW in AI Education Programs",
        "category": "Study",
        "source_name": "Ministry of Education",
        "days_ago": 15,
        "summary": "Korea announced a 2.3 trillion KRW investment in AI education over 5 years. Includes AI-focused curriculum at 100+ universities, free online AI courses for international students, and 10,000 AI scholarship positions.",
        "impact_for_students": "Excellent timing for students interested in AI. Free online courses available for international applicants. Scholarship positions specifically for non-Korean students.",
        "impact_for_job_seekers": "Growing AI talent pool in Korea increases competition but also signals strong industry demand. Korean AI education credentials will be increasingly recognised globally.",
        "tags": ["AI", "education", "investment", "scholarship", "university"],
    },
    {
        "title": "Korea IT Hiring Growth: 22% Increase in Foreign Tech Worker Permits",
        "category": "Work",
        "source_name": "Korea Ministry of Employment and Labor",
        "days_ago": 7,
        "summary": "E-7 visas issued for IT professionals increased 22% year-on-year in Q1 2026. Software developers and AI engineers represent the largest categories. The average processing time decreased from 45 to 30 days.",
        "impact_for_students": "Strong job market signals for IT graduates. Consider software engineering or AI specialisation for highest employability.",
        "impact_for_job_seekers": "Faster visa processing and growing quota. Competitive salary ranges for experienced developers. Python and Java remain most in-demand skills.",
        "tags": ["IT", "hiring", "E-7", "foreign workers", "tech jobs"],
    },
    {
        "title": "New TOPIK Speaking Test to Launch in 2027",
        "category": "Study",
        "source_name": "National Institute for International Education",
        "days_ago": 20,
        "summary": "TOPIK will introduce a mandatory speaking section from 2027. The speaking test will be computer-based and scored separately from reading/listening/writing. Existing TOPIK certificates remain valid. No change to current TOPIK 1-6 grading structure.",
        "impact_for_students": "Take the current TOPIK format before 2027 if possible. Speaking section may be challenging for self-taught learners.",
        "impact_for_job_seekers": "Employers will likely require speaking scores from 2027 onward. Start practicing Korean conversation early even if you don't need it yet.",
        "tags": ["TOPIK", "Korean language", "test", "education"],
    },
    {
        "title": "Korea Minimum Wage Set at 10,560 KRW for 2027",
        "category": "Economy",
        "source_name": "Minimum Wage Commission",
        "days_ago": 14,
        "summary": "The 2027 minimum wage was set at 10,560 KRW/hour (approx. 8.80 USD), a 3.2% increase from 2026. Part-time and seasonal workers are included. International students on D-2 visas can work up to 25 hours/week during semesters.",
        "impact_for_students": "Higher part-time wage improves financial sustainability. A student working 20 hrs/week at minimum wage earns approximately 845,000 KRW/month.",
        "impact_for_job_seekers": "Minimum wage increase may affect entry-level salary floors. Full-time positions typically pay well above minimum wage for professional roles.",
        "tags": ["minimum wage", "economy", "part-time", "student work"],
    },
    {
        "title": "Kakao and Naver Expand AI Assistant Offerings for International Users",
        "category": "Technology",
        "source_name": "TechCrunch Korea",
        "days_ago": 6,
        "summary": "Kakao and Naver both launched English-language versions of their AI assistants. Kakao i now supports English-Korean bilingual conversations. Naver's CLOVA X released developer APIs for third-party integration. Both aim to compete with global AI platforms.",
        "impact_for_students": "English-friendly AI tools reduce the language barrier for international students. Useful for translation, study assistance, and daily life.",
        "impact_for_job_seekers": "Growing AI ecosystem creates opportunities for English-speaking PMs and engineers. Korean tech companies are increasingly internationalising their products.",
        "tags": ["AI", "Kakao", "Naver", "English", "tech ecosystem"],
    },
    {
        "title": "Foreign Resident Registration (ARC) Now Digital — No In-Person Visit Required",
        "category": "Visa",
        "source_name": "Korea Immigration Service",
        "days_ago": 4,
        "summary": "Starting June 2026, foreign residents can complete ARC registration and renewal entirely online through the HiKorea portal. Biometric data can be submitted at self-service kiosks at 50 locations nationwide. Processing time reduced from 3 weeks to 5 business days.",
        "impact_for_students": "Significant convenience improvement. No more waiting in long queues at immigration offices. Plan to register immediately after arrival.",
        "impact_for_job_seekers": "Simplifies the administrative burden of visa renewal. Particularly helpful during job transitions between E-7 sponsors.",
        "tags": ["ARC", "immigration", "digital", "visa", "resident"],
    },
    {
        "title": "AII Hubs Opening in Busan and Daejeon — 500+ Tech Jobs Expected",
        "category": "Work",
        "source_name": "Ministry of Science and ICT",
        "days_ago": 9,
        "summary": "The Korean government designated Busan (2030 Expo precinct) and Daejeon (Daedeok Innopolis) as new AI innovation hubs. Tax incentives for foreign tech companies establishing offices in these cities. Expected to create 500+ tech jobs over 2 years.",
        "impact_for_students": "New job opportunities outside Seoul. Lower cost of living makes these cities attractive for recent graduates.",
        "impact_for_job_seekers": "Consider Busan and Daejeon as alternatives to Seoul. Government incentives may mean higher starting salaries relative to local cost of living.",
        "tags": ["AI", "Busan", "Daejeon", "tech jobs", "innovation hub"],
    },
    {
        "title": "Korea-USA Digital Partnership Expanded — Remote Work Visas for Tech Workers",
        "category": "Work",
        "source_name": "Korean Ministry of Foreign Affairs",
        "days_ago": 18,
        "summary": "Under the expanded Korea-USA Digital Partnership, a new remote work visa allows US tech workers to stay in Korea for up to 2 years. Reciprocally, Korean tech workers receive streamlined E-visas for the US. Application opens Q3 2026.",
        "impact_for_students": "Not directly applicable to students, but signals deepening Korea-US tech integration. Internships at Korean-US joint ventures may increase.",
        "impact_for_job_seekers": "New pathway for digital nomads and remote workers. Particularly relevant for software engineers with US clients or employers.",
        "tags": ["remote work", "digital nomad", "visa", "US", "tech"],
    },
    {
        "title": "University Tuition Freeze Extended for 5th Consecutive Year",
        "category": "Study",
        "source_name": "Korean Council for University Education",
        "days_ago": 11,
        "summary": "Major Korean universities extended the tuition freeze for the 5th year, keeping 2027 tuition at 2022 levels. This applies to both domestic and international students at 40+ participating universities, including SKY universities.",
        "impact_for_students": "Tuition stability helps with financial planning. Combined with scholarship opportunities, Korea remains competitively priced vs US/Australia/UK.",
        "impact_for_job_seekers": "Not directly applicable. However, stable education costs mean more graduates entering the workforce without extreme debt burdens.",
        "tags": ["tuition", "university", "freeze", "cost", "education"],
    },
    {
        "title": "Korean Semiconductor Industry Faces Talent Shortage — 5,000 New Roles Unfilled",
        "category": "Technology",
        "source_name": "Korea Semiconductor Industry Association",
        "days_ago": 6,
        "summary": "Korea's semiconductor industry reported 5,000 unfilled positions across design, manufacturing, and packaging. Samsung and SK Hynix are expanding recruitment of foreign engineers. English-language roles available at R&D centres.",
        "impact_for_students": "Strong job prospects for semiconductor and electrical engineering students. Internship opportunities with world-leading companies.",
        "impact_for_job_seekers": "Exceptional demand for experienced semiconductor engineers. Foreign talent with relevant experience can expect competitive offers and visa support.",
        "tags": ["semiconductor", "talent shortage", "Samsung", "SK Hynix", "engineering"],
    },
]


def get_mock_items() -> list[dict]:
    """Return all mock items with calculated published_at dates."""
    items = []
    for raw in RAW_ITEMS:
        item = dict(raw)
        pub_date = BASE_DATE - timedelta(days=raw["days_ago"])
        item["published_at"] = pub_date.strftime("%Y-%m-%d")
        item["relevance_score"] = 0  # calculated at query time
        item["source_url"] = f"https://example.com/news/{raw['category'].lower()}/{raw['days_ago']}"
        items.append(item)
    return items


def search_items(keyword: str, category: str, time_range: str) -> list[dict]:
    """Search mock news items by keyword, category, and time range."""
    max_days = TIME_RANGES.get(time_range, 90)
    cutoff = BASE_DATE - timedelta(days=max_days)
    keyword_lower = keyword.lower().strip() if keyword else ""

    results = []
    for item in get_mock_items():
        pub = datetime.strptime(item["published_at"], "%Y-%m-%d")
        if pub < cutoff:
            continue
        if category != "All" and item["category"] != category:
            continue
        if keyword_lower:
            searchable = " ".join([
                item["title"].lower(),
                item["summary"].lower(),
                " ".join(item["tags"]).lower(),
            ])
            if keyword_lower not in searchable:
                continue
        results.append(item)

    # Calculate relevance score based on keyword match density
    for item in results:
        score = 50  # base
        if keyword_lower:
            searchable = " ".join([
                item["title"].lower(),
                item["summary"].lower(),
                " ".join(item["tags"]).lower(),
            ])
            count = searchable.count(keyword_lower)
            score += count * 10
            if keyword_lower in item["title"].lower():
                score += 30
            for tag in item["tags"]:
                if keyword_lower in tag.lower():
                    score += 20
        score = min(score, 100)  # cap at 100
        item["relevance_score"] = score

    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results


def generate_trend_summary(results: list[dict], keyword: str, language: str = "en") -> str:
    """Generate a readable trend summary based on search results."""
    if not results:
        if _language(language) == "zh":
            return f"在所选时间范围内未找到{'与“' + keyword + '”相关的' if keyword else ''}新闻条目。"
        return f"No news items found{' for "' + keyword + '"' if keyword else ''} in the selected period."

    categories_found = {}
    for r in results:
        cat = r["category"]
        categories_found[cat] = categories_found.get(cat, 0) + 1

    top_cat = max(categories_found, key=categories_found.get) if categories_found else ""
    recent_count = sum(1 for r in results if (BASE_DATE - datetime.strptime(r["published_at"], "%Y-%m-%d")).days <= 7)

    if _language(language) == "zh":
        lines = [f"找到 **{len(results)}** 条相关新闻"]
        if keyword:
            lines.append(f"与 **“{keyword}”** 相关")
        lines.append(f"覆盖 {len(categories_found)} 个类别。")
        lines.append("")
        lines.append(f"最活跃类别：**{_zh_category(top_cat)}**（{categories_found.get(top_cat, 0)} 条）。")
        if recent_count > 0:
            lines.append(f"其中 {recent_count} 条发布于最近 7 天。")
        lines.append("")
        lines.append("**关键观察：** 韩国的科技、签证和教育政策仍是影响国际学生与求职者决策的高动态领域。")
        lines.append("AI、半导体、数字基础设施和签证便利化相关更新值得持续关注。")
        return "\n".join(lines)

    lines = [
        f"Found **{len(results)}** relevant news items",
    ]
    if keyword:
        lines.append(f"related to **\"{keyword}\"**")
    lines.append(f"across {len(categories_found)} categories.")
    lines.append(f"")
    lines.append(f"Most active category: **{top_cat}** ({categories_found.get(top_cat, 0)} items).")
    if recent_count > 0:
        lines.append(f"{recent_count} item(s) published in the last 7 days.")
    lines.append(f"")
    lines.append(f"**Key observation:** Korea's technology and visa policies remain the most dynamic areas")
    lines.append(f"for international students and job seekers, with consistent policy updates and growing")
    lines.append(f"investment in AI, semiconductors, and digital infrastructure.")

    return "\n".join(lines)


def generate_action_suggestions(results: list[dict], keyword: str, language: str = "en") -> list[str]:
    """Generate practical action suggestions based on search results."""
    suggestions = set()

    for r in results:
        cat = r["category"]
        if cat == "Visa":
            suggestions.add("检查你的签证类型，确认近期政策变化是否影响你的申请或居留状态。" if _language(language) == "zh" else "Review your visa type and check if recent policy changes affect your status.")
            suggestions.add("收藏 HiKorea 门户，用于签证、ARC 和在线办理服务。" if _language(language) == "zh" else "Bookmark the HiKorea portal for digital visa and ARC services.")
        if cat == "Study":
            suggestions.add("检查 GKS 和目标大学奖学金截止日期。" if _language(language) == "zh" else "Check GKS and university-specific scholarship deadlines.")
            suggestions.add("尽早准备 TOPIK；多数项目至少应以 TOPIK 4 为目标。" if _language(language) == "zh" else "Begin TOPIK preparation early — TOPIK 4 is the minimum for most programs.")
        if cat == "Work":
            suggestions.add("更新 LinkedIn 和 Wanted.co.kr 资料，方便韩国招聘方了解你的背景。" if _language(language) == "zh" else "Update your LinkedIn and Wanted.co.kr profile for Korean recruiters.")
            suggestions.add("申请前先确认目标公司是否支持签证担保。" if _language(language) == "zh" else "Research target companies' visa sponsorship policies before applying.")
        if cat == "Technology":
            suggestions.add("把技能学习对齐高需求方向：AI、半导体、软件工程。" if _language(language) == "zh" else "Align your skill development with in-demand areas: AI, semiconductors, software engineering.")
            suggestions.add("参加韩国技术 meetup 或会议，建立行业人脉。" if _language(language) == "zh" else "Attend Korean tech meetups or conferences for networking.")
        if cat == "Economy":
            suggestions.add("把近期生活成本变化纳入预算规划。" if _language(language) == "zh" else "Factor recent cost-of-living changes into your budget planning.")
            suggestions.add("比较 offer 时，要结合不同城市的实际生活成本。" if _language(language) == "zh" else "Compare salary offers against city-specific living costs.")

    return list(suggestions)[:6]
