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

ZH_NEWS_ITEMS = {
    "D-10 Job Seeker Visa Extended to 12 Months for STEM Graduates": {
        "title": "STEM 毕业生 D-10 求职签证延长至 12 个月",
        "source_name": "韩国出入境管理局",
        "summary": "韩国法务部将 STEM 领域毕业生的 D-10 求职签证期限从 6 个月延长至 12 个月。申请人需持有韩国大学本科或以上学历。",
        "impact_for_students": "STEM 毕业生毕业后有更充足的时间寻找工作，可降低求职期压力。",
        "impact_for_job_seekers": "非 STEM 毕业生仍为 6 个月。可考虑补充资格证书或韩语培训，以提升签证与就业竞争力。",
    },
    "2026 GKS Scholarship Applications Open — 2,000 International Slots": {
        "title": "2026 年 GKS 奖学金开放申请：面向国际学生 2,000 个名额",
        "source_name": "韩国教育部",
        "summary": "Global Korea Scholarship（GKS）宣布为 2027 学年本科和研究生国际学生提供 2,000 个名额。申请截止至 2026 年 10 月，福利包括全额学费、月度生活补贴、机票和韩语培训。",
        "impact_for_students": "这是重要的资助机会。建议尽早准备推荐信、成绩单和申请材料。",
        "impact_for_job_seekers": "对求职者不直接适用，但 GKS 校友在韩国政府相关机构中通常更具认可度。",
    },
    "Topik 4 Now Mandatory for E-7 Visa Sponsorship at SMEs": {
        "title": "中小企业 E-7 签证担保将强制要求 TOPIK 4",
        "source_name": "韩国法务部",
        "summary": "自 2026 年 7 月起，为外籍员工担保 E-7 签证的韩国中小企业需确认申请人达到 TOPIK 4 或以上。此前部分中小企业可接受 TOPIK 3，大型企业已普遍要求 TOPIK 4+。",
        "impact_for_students": "应提前规划韩语学习，即使当前签证暂不要求，也建议把 TOPIK 4 作为最低目标。",
        "impact_for_job_seekers": "中小企业就业门槛提高。多数担保类工作签证现在基本需要 TOPIK 4，建议预留 6-12 个月学习时间。",
    },
    "NVIDIA and Samsung Partner on AI Semiconductor Research Hub in Seoul": {
        "title": "NVIDIA 与三星将在首尔共建 AI 半导体研究中心",
        "source_name": "Korea Herald",
        "summary": "NVIDIA 与三星电子宣布在首尔江南区建立联合 AI 半导体研究中心。该中心将雇用 300 多名研究人员，聚焦 AI 芯片设计、LLM 优化和存储架构，招聘预计于 2026 年第三季度开始。",
        "impact_for_students": "工程和计算机专业学生将获得新的实习与研究助理机会，可考虑聚焦 AI/ML 硬件方向。",
        "impact_for_job_seekers": "这释放出 AI 硬件和半导体岗位增长信号。三星与 NVIDIA 将在首尔争夺高端人才，预计研发环境对英语更友好。",
    },
    "Seoul Metropolitan Area Housing Costs Rise 8% Year-on-Year": {
        "title": "首都圈住房成本同比上涨 8%",
        "source_name": "KB 国民银行研究院",
        "summary": "首尔平均月租较 2025 年第一季度上涨 8%。热门区域单间公寓月租约 75-90 万韩元，考试院价格相对稳定在 30-50 万韩元，全租押金也上涨约 5%。",
        "impact_for_students": "相比去年，每月预算建议增加 5-10 万韩元。可考虑考试院或合租公寓降低成本。",
        "impact_for_job_seekers": "住房成本会影响薪资谈判和迁居预算。可考虑盆唐或仁川等较低成本区域。",
    },
    "Korean Government Invests 2.3 Trillion KRW in AI Education Programs": {
        "title": "韩国政府将投入 2.3 万亿韩元发展 AI 教育项目",
        "source_name": "韩国教育部",
        "summary": "韩国宣布未来 5 年向 AI 教育投入 2.3 万亿韩元，包括在 100 多所大学建设 AI 课程、为国际学生提供免费在线 AI 课程，并设立 10,000 个 AI 奖学金名额。",
        "impact_for_students": "对 AI 方向学生是良好时机。国际申请者可关注免费课程和奖学金机会。",
        "impact_for_job_seekers": "韩国 AI 人才池扩大可能增加竞争，同时也说明产业需求强劲。韩国 AI 教育背景将更受认可。",
    },
    "Korea IT Hiring Growth: 22% Increase in Foreign Tech Worker Permits": {
        "title": "韩国 IT 招聘增长：外籍技术人员许可同比增加 22%",
        "source_name": "韩国雇佣劳动部",
        "summary": "2026 年第一季度，面向 IT 专业人士的 E-7 签证发放量同比增长 22%。软件开发者和 AI 工程师占最大类别，平均处理时间从 45 天缩短至 30 天。",
        "impact_for_students": "IT 毕业生就业信号强劲。软件工程或 AI 方向仍是就业能力最高的选择之一。",
        "impact_for_job_seekers": "签证处理更快、配额增长。有经验开发者薪资竞争力较强，Python 和 Java 仍是高需求技能。",
    },
    "New TOPIK Speaking Test to Launch in 2027": {
        "title": "TOPIK 将于 2027 年新增口语考试",
        "source_name": "国立国际教育院",
        "summary": "TOPIK 将从 2027 年起加入强制口语部分。口语考试采用机考，并与听读写分开评分。现有 TOPIK 证书仍有效，当前 1-6 级结构不变。",
        "impact_for_students": "如有可能，可在 2027 年前参加现行 TOPIK。口语部分对自学者可能更具挑战。",
        "impact_for_job_seekers": "雇主可能从 2027 年起更重视口语分数。即使短期不需要，也建议提前练习韩语会话。",
    },
    "Korea Minimum Wage Set at 10,560 KRW for 2027": {
        "title": "韩国 2027 年最低时薪定为 10,560 韩元",
        "source_name": "最低工资委员会",
        "summary": "2027 年最低工资定为每小时 10,560 韩元，较 2026 年上涨 3.2%。兼职和季节性劳动者适用。D-2 学生签证持有人学期中每周最多可工作 25 小时。",
        "impact_for_students": "更高兼职工资有助于缓解生活成本。每周工作 20 小时的学生月收入约 84.5 万韩元。",
        "impact_for_job_seekers": "最低工资上涨可能影响入门薪资底线。专业全职岗位通常显著高于最低工资。",
    },
    "Kakao and Naver Expand AI Assistant Offerings for International Users": {
        "title": "Kakao 与 Naver 面向国际用户扩展 AI 助手服务",
        "source_name": "TechCrunch Korea",
        "summary": "Kakao 和 Naver 均推出英文版 AI 助手。Kakao i 支持英韩双语对话，Naver CLOVA X 发布面向第三方集成的开发者 API，双方都在与全球 AI 平台竞争。",
        "impact_for_students": "英文友好的 AI 工具可降低国际学生语言门槛，可用于翻译、学习辅助和日常生活。",
        "impact_for_job_seekers": "AI 生态扩张为英语 PM 和工程师创造机会。韩国科技公司正加速产品国际化。",
    },
    "Foreign Resident Registration (ARC) Now Digital — No In-Person Visit Required": {
        "title": "外国人登陆证（ARC）登记全面数字化，无需现场办理",
        "source_name": "韩国出入境管理局",
        "summary": "自 2026 年 6 月起，外国居民可通过 HiKorea 门户在线完成 ARC 登记与续签。生物识别信息可在全国 50 个自助终端提交，处理时间由 3 周缩短至 5 个工作日。",
        "impact_for_students": "便利性显著提升，无需在出入境办公室长时间排队。建议抵达后尽快登记。",
        "impact_for_job_seekers": "简化签证续签与行政流程，尤其有利于 E-7 雇主转换期间的求职者。",
    },
    "AII Hubs Opening in Busan and Daejeon — 500+ Tech Jobs Expected": {
        "title": "釜山和大田将开放 AI 创新中心，预计创造 500+ 科技岗位",
        "source_name": "科学技术信息通信部",
        "summary": "韩国政府将釜山和大田指定为新的 AI 创新中心，并为在这些城市设立办公室的外资科技公司提供税收激励。预计未来 2 年创造 500 多个科技岗位。",
        "impact_for_students": "首尔以外的就业机会增加。较低生活成本使这些城市对毕业生更有吸引力。",
        "impact_for_job_seekers": "可把釜山和大田作为首尔以外的选择。政府激励可能带来相对当地生活成本更高的起薪。",
    },
    "Korea-USA Digital Partnership Expanded — Remote Work Visas for Tech Workers": {
        "title": "韩美数字伙伴关系扩展：科技工作者远程工作签证上线",
        "source_name": "韩国外交部",
        "summary": "在扩展后的韩美数字伙伴关系下，新远程工作签证允许美国科技工作者在韩国停留最长 2 年。韩国科技工作者赴美也将获得更便利的 E 类签证流程，申请预计 2026 年第三季度开放。",
        "impact_for_students": "对学生不直接适用，但显示韩美科技合作深化，韩美合资企业实习机会可能增加。",
        "impact_for_job_seekers": "为数字游民和远程工作者提供新路径，尤其适合拥有美国客户或雇主的软件工程师。",
    },
    "University Tuition Freeze Extended for 5th Consecutive Year": {
        "title": "韩国大学学费连续第 5 年冻结",
        "source_name": "韩国大学教育协会",
        "summary": "韩国主要大学连续第 5 年延长学费冻结政策，将 2027 年学费维持在 2022 年水平。该政策适用于 40 多所参与大学的本地和国际学生，包括 SKY 大学。",
        "impact_for_students": "学费稳定有助于财务规划。结合奖学金机会，韩国相较美国、澳洲和英国仍具价格竞争力。",
        "impact_for_job_seekers": "不直接适用，但稳定教育成本意味着更多毕业生不会背负极高债务进入就业市场。",
    },
    "Korean Semiconductor Industry Faces Talent Shortage — 5,000 New Roles Unfilled": {
        "title": "韩国半导体行业面临人才短缺：5,000 个新岗位空缺",
        "source_name": "韩国半导体产业协会",
        "summary": "韩国半导体行业报告称，设计、制造和封装环节共有 5,000 个岗位空缺。三星和 SK 海力士正在扩大外籍工程师招聘，研发中心提供英文岗位。",
        "impact_for_students": "半导体和电气工程学生就业前景强劲，可关注全球领先企业的实习机会。",
        "impact_for_job_seekers": "经验丰富的半导体工程师需求极高。具备相关经验的外籍人才可期待有竞争力的 offer 和签证支持。",
    },
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


def localize_items(results: list[dict], language: str = "en") -> list[dict]:
    """Return display-localized news items without changing search keys."""
    if _language(language) != "zh":
        return [dict(item) for item in results]

    localized = []
    for item in results:
        item_copy = dict(item)
        zh = ZH_NEWS_ITEMS.get(item["title"])
        if zh:
            item_copy.update(zh)
        localized.append(item_copy)
    return localized


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
