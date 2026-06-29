from __future__ import annotations

import streamlit as st

SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh": "简体中文",
}

_LANGUAGE_BY_LABEL = {label: code for code, label in SUPPORTED_LANGUAGES.items()}

OPTION_LABELS: dict[str, dict[str, dict[str, str]]] = {
    "role": {
        "Data Analyst": {"en": "Data Analyst", "zh": "数据分析师"},
        "Backend Developer": {"en": "Backend Developer", "zh": "后端开发工程师"},
        "AI Product Manager": {"en": "AI Product Manager", "zh": "AI 产品经理"},
        "AI Engineer": {"en": "AI Engineer", "zh": "AI 工程师"},
        "Marketing Specialist": {"en": "Marketing Specialist", "zh": "市场营销专员"},
        "Business Analyst": {"en": "Business Analyst", "zh": "商业分析师"},
        "Operations Specialist": {"en": "Operations Specialist", "zh": "运营专员"},
        "Customer Support Specialist": {"en": "Customer Support Specialist", "zh": "客户支持专员"},
        "International Sales": {"en": "International Sales", "zh": "国际销售"},
        "Product Manager": {"en": "Product Manager", "zh": "产品经理"},
        "Accountant": {"en": "Accountant", "zh": "会计师"},
        "English Teacher": {"en": "English Teacher", "zh": "英语教师"},
        "Chinese Teacher": {"en": "Chinese Teacher", "zh": "中文教师"},
        "Registered Nurse": {"en": "Registered Nurse", "zh": "注册护士"},
        "Care Worker": {"en": "Care Worker", "zh": "护理员"},
        "Mechanical Engineer": {"en": "Mechanical Engineer", "zh": "机械工程师"},
        "Electrical Engineer": {"en": "Electrical Engineer", "zh": "电气工程师"},
        "Not Applicable": {"en": "Not Applicable", "zh": "不适用"},
    },
    "experience": {
        "Student": {"en": "Student", "zh": "学生"},
        "0-2 years": {"en": "0-2 years", "zh": "0-2 年经验"},
        "3-5 years": {"en": "3-5 years", "zh": "3-5 年经验"},
    },
    "korean_level": {
        "None": {"en": "None", "zh": "无"},
        "TOPIK 3": {"en": "TOPIK 3", "zh": "TOPIK 3"},
        "TOPIK 4": {"en": "TOPIK 4", "zh": "TOPIK 4"},
        "TOPIK 5+": {"en": "TOPIK 5+", "zh": "TOPIK 5+"},
    },
    "city": {
        "Seoul": {"en": "Seoul", "zh": "首尔"},
        "Busan": {"en": "Busan", "zh": "釜山"},
        "Incheon": {"en": "Incheon", "zh": "仁川"},
        "Daejeon": {"en": "Daejeon", "zh": "大田"},
        "Daegu": {"en": "Daegu", "zh": "大邱"},
        "Seongnam (Pangyo)": {"en": "Seongnam (Pangyo)", "zh": "城南（板桥）"},
        "Gwangju": {"en": "Gwangju", "zh": "光州"},
        "Ulsan": {"en": "Ulsan", "zh": "蔚山"},
        "Changwon": {"en": "Changwon", "zh": "昌原"},
        "Pohang": {"en": "Pohang", "zh": "浦项"},
        "Other": {"en": "Other", "zh": "其他"},
    },
    "school_type": {
        "Language School": {"en": "Language School", "zh": "语言学校"},
        "Undergraduate": {"en": "Undergraduate", "zh": "本科"},
        "Graduate School": {"en": "Graduate School", "zh": "研究生院"},
        "Not Applicable": {"en": "Not Applicable", "zh": "不适用"},
    },
    "housing_type": {
        "Dormitory": {"en": "Dormitory", "zh": "宿舍"},
        "Shared Apartment": {"en": "Shared Apartment", "zh": "合租公寓"},
        "Studio Apartment": {"en": "Studio Apartment", "zh": "单间公寓"},
        "Not Applicable": {"en": "Not Applicable", "zh": "不适用"},
    },
    "lifestyle": {
        "Budget": {"en": "Budget", "zh": "节省型"},
        "Standard": {"en": "Standard", "zh": "标准型"},
        "Premium": {"en": "Premium", "zh": "高品质"},
    },
    "goal": {
        "Study": {"en": "Study", "zh": "留学"},
        "Work": {"en": "Work", "zh": "工作"},
        "Live": {"en": "Live", "zh": "生活"},
    },
    "news_category": {
        "All": {"en": "All", "zh": "全部"},
        "Study": {"en": "Study", "zh": "留学"},
        "Work": {"en": "Work", "zh": "工作"},
        "Visa": {"en": "Visa", "zh": "签证"},
        "Economy": {"en": "Economy", "zh": "经济"},
        "Technology": {"en": "Technology", "zh": "科技"},
    },
    "time_range": {
        "Last 7 days": {"en": "Last 7 days", "zh": "过去 7 天"},
        "Last 30 days": {"en": "Last 30 days", "zh": "过去 30 天"},
        "Last 90 days": {"en": "Last 90 days", "zh": "过去 90 天"},
    },
    "cost_category": {
        "Tuition": {"en": "Tuition", "zh": "学费"},
        "Housing": {"en": "Housing", "zh": "住房"},
        "Food": {"en": "Food", "zh": "饮食"},
        "Transportation": {"en": "Transportation", "zh": "交通"},
        "Insurance": {"en": "Insurance", "zh": "保险"},
        "Miscellaneous": {"en": "Miscellaneous", "zh": "杂项"},
    },
    "period": {
        "Monthly": {"en": "Monthly", "zh": "月度"},
        "Annual": {"en": "Annual", "zh": "年度"},
    },
}

RESULT_LABELS: dict[str, dict[str, str]] = {
    "Strongly Recommended": {"en": "Strongly Recommended", "zh": "强烈推荐"},
    "Strongly Recommended ✅": {"en": "Strongly Recommended ✅", "zh": "强烈推荐 ✅"},
    "Recommended with Preparation": {"en": "Recommended with Preparation", "zh": "准备充分后推荐"},
    "Recommended with Preparation ⚠️": {"en": "Recommended with Preparation ⚠️", "zh": "准备充分后推荐 ⚠️"},
    "Risky": {"en": "Risky", "zh": "有一定风险"},
    "Risky ❓": {"en": "Risky ❓", "zh": "有一定风险 ❓"},
    "Not Recommended Yet": {"en": "Not Recommended Yet", "zh": "暂不推荐"},
    "Not Recommended Yet ❌": {"en": "Not Recommended Yet ❌", "zh": "暂不推荐 ❌"},
    "Low": {"en": "Low", "zh": "低"},
    "Medium": {"en": "Medium", "zh": "中"},
    "High": {"en": "High", "zh": "高"},
    "Very Low — strong demand, few qualified candidates": {
        "en": "Very Low — strong demand, few qualified candidates",
        "zh": "很低：需求强，合格候选人较少",
    },
    "Low": {"en": "Low", "zh": "低"},
    "Below Average": {"en": "Below Average", "zh": "低于平均"},
    "Average — competitive but achievable with right skills": {
        "en": "Average — competitive but achievable with right skills",
        "zh": "中等：有竞争，但技能匹配即可争取",
    },
    "Above Average": {"en": "Above Average", "zh": "高于平均"},
    "Moderately High": {"en": "Moderately High", "zh": "较高"},
    "High — requires differentiation": {"en": "High — requires differentiation", "zh": "较高：需要差异化优势"},
    "Very High": {"en": "Very High", "zh": "很高"},
    "Extremely Competitive": {"en": "Extremely Competitive", "zh": "竞争极高"},
    "Saturated": {"en": "Saturated", "zh": "趋于饱和"},
}


_TRANSLATIONS: dict[str, dict[str, str]] = {
    "common.language": {"en": "Language", "zh": "语言"},
    "common.back_home": {"en": "Back to Home", "zh": "返回首页"},
    "common.api_start": {
        "en": "Start the backend: `cd backend && uvicorn app.main:app --reload`",
        "zh": "请先启动后端：`cd backend && uvicorn app.main:app --reload`",
    },
    "common.run_backend": {
        "en": "Run: `cd backend && uvicorn app.main:app --reload`",
        "zh": "运行：`cd backend && uvicorn app.main:app --reload`",
    },
    "common.download_csv": {"en": "📥 Download CSV", "zh": "📥 下载 CSV"},
    "common.no_data": {"en": "No data available.", "zh": "暂无数据。"},
    "common.category": {"en": "Category", "zh": "类别"},
    "common.amount_krw": {"en": "Amount (KRW)", "zh": "金额（韩元）"},
    "common.percent": {"en": "Percent", "zh": "占比"},
    "common.generated": {"en": "Generated", "zh": "已生成"},
    "common.export": {"en": "EXPORT", "zh": "导出"},
    "common.your_profile": {"en": "YOUR PROFILE", "zh": "你的资料"},
    "common.directional_estimates": {"en": "Directional estimates", "zh": "方向性估算"},

    "home.page_title": {"en": "Korea Compass", "zh": "韩国指南"},
    "home.brand": {"en": "KOREA COMPASS", "zh": "韩国指南"},
    "home.heading": {"en": "Should I study, work, or live in Korea?", "zh": "我该去韩国留学、工作还是生活？"},
    "home.subtitle": {
        "en": "A practical decision assistant for international students and job seekers considering Korea. Estimate costs, analyse job markets, and get personalised AI reports.",
        "zh": "面向考虑韩国的国际学生和求职者的实用决策助手。估算成本、分析就业市场，并生成个性化 AI 报告。",
    },
    "home.kpi.study": {"en": "Study Cost Calculator", "zh": "留学成本计算器"},
    "home.kpi.job": {"en": "Career & Job Market Analyzer", "zh": "职业与就业市场分析"},
    "home.kpi.report": {"en": "AI Korea Life Plan", "zh": "AI 韩国生活规划"},
    "home.aside_tag": {"en": "V2 · ISSUE #2", "zh": "V2 · 议题 #2"},
    "home.aside_title": {"en": "Study Cost Calculator", "zh": "留学成本计算器"},
    "home.aside_desc": {
        "en": "Curated data · Plotly charts · AI explanations · Persistent history",
        "zh": "精选数据 · Plotly 图表 · AI 解释 · 历史记录保留",
    },
    "home.stack": {"en": "Streamlit · FastAPI · SQLite · Plotly · Dual AI provider", "zh": "Streamlit · FastAPI · SQLite · Plotly · 双 AI 提供方"},
    "home.metric.data_points": {"en": "Data points", "zh": "数据点"},
    "home.metric.countries": {"en": "Countries", "zh": "国家"},
    "home.metric.categories": {"en": "Categories", "zh": "维度"},
    "home.metric.modules": {"en": "Modules", "zh": "模块"},
    "home.metric.focus": {"en": "Focus", "zh": "聚焦"},
    "home.metric.exports": {"en": "Exports", "zh": "导出"},
    "home.metric.api": {"en": "API", "zh": "API"},
    "home.api_online": {"en": "✅ Online", "zh": "✅ 在线"},
    "home.api_offline": {"en": "Offline", "zh": "离线"},
    "home.backend_unreachable": {"en": "Backend not reachable: {error}", "zh": "无法连接后端：{error}"},
    "home.demo_label": {"en": "PORTFOLIO DEMO FLOW", "zh": "作品集演示流程"},
    "home.demo_heading": {"en": "Try the full workflow in 4 steps", "zh": "用 4 步体验完整流程"},
    "home.flow.study.title": {"en": "Calculate Study Cost", "zh": "计算留学成本"},
    "home.flow.study.desc": {"en": "Estimate monthly and annual costs for your Korea study plan.", "zh": "估算你的韩国留学月度与年度成本。"},
    "home.flow.job.title": {"en": "Analyze Career Market", "zh": "分析职业市场"},
    "home.flow.job.desc": {"en": "See salary ranges, required skills, and visa pathways across tech and business roles.", "zh": "查看技术与商业岗位的薪资范围、技能要求和签证路径。"},
    "home.flow.report.title": {"en": "Generate AI Korea Life Plan", "zh": "生成 AI 韩国生活规划"},
    "home.flow.report.desc": {"en": "Combine cost + career into a personalised recommendation with action plan.", "zh": "把成本和职业分析合并成带行动计划的个性化建议。"},
    "home.flow.news.title": {"en": "Check News & Policy", "zh": "查看新闻与政策"},
    "home.flow.news.desc": {"en": "Search recent Korea visa, study, work, and tech policy updates.", "zh": "搜索近期韩国签证、留学、工作和科技政策动态。"},
    "home.tools": {"en": "TOOLS", "zh": "工具"},
    "home.modules": {"en": "Decision modules", "zh": "决策模块"},
    "home.nav.new": {"en": "V2 · NEW", "zh": "V2 · 新增"},
    "home.study.desc": {"en": "Estimate your monthly and annual costs for studying in Korea across different cities and lifestyles.", "zh": "按城市和生活方式估算在韩国学习的月度与年度成本。"},
    "home.job.desc": {"en": "Analyze Korean career options, salary ranges, skill requirements, and visa pathways.", "zh": "分析韩国职业选择、薪资范围、技能要求和签证路径。"},
    "home.report.desc": {"en": "Get a personalised report on studying, working, or living in Korea.", "zh": "获取关于在韩国学习、工作或生活的个性化报告。"},
    "home.news.desc": {"en": "Recent Korea study, work, visa, economy, and technology developments.", "zh": "近期韩国留学、工作、签证、经济与科技动态。"},
    "home.open_calculator": {"en": "Open Calculator", "zh": "打开计算器"},
    "home.open_analyzer": {"en": "Open Analyzer", "zh": "打开分析器"},
    "home.open_report": {"en": "Open Report", "zh": "打开报告"},
    "home.open_news": {"en": "Open News", "zh": "打开新闻"},
    "home.dev_label": {"en": "DEVELOPER ACCESS", "zh": "开发者入口"},
    "home.api_docs": {"en": "Open API Documentation", "zh": "打开 API 文档"},
    "home.api_caption": {
        "en": "FastAPI exposes study cost estimates, career analysis, decision reports, and news/policy search endpoints.",
        "zh": "FastAPI 提供留学成本估算、职业分析、决策报告和新闻政策搜索接口。",
    },
    "home.api_fallback_caption": {
        "en": "Streamlit Cloud is running in local fallback mode. FastAPI docs are available only when API_BASE_URL is configured.",
        "zh": "Streamlit Cloud 正在使用本地 fallback 模式。只有配置 API_BASE_URL 后才会显示 FastAPI 文档。",
    },

    "study.page_title": {"en": "Study Cost Calculator", "zh": "留学成本计算器"},
    "study.brand": {"en": "V2 · MODULE 1", "zh": "V2 · 模块 1"},
    "study.heading": {"en": "Korea Study Cost Calculator", "zh": "韩国留学成本计算器"},
    "study.subtitle": {
        "en": "Estimate your monthly and annual costs for studying in Korea. Covers tuition, housing, food, transport, insurance, and miscellaneous expenses.",
        "zh": "估算在韩国学习的月度与年度成本，覆盖学费、住房、饮食、交通、保险和杂项支出。",
    },
    "study.aside_title": {"en": "All amounts in KRW", "zh": "所有金额均为韩元"},
    "study.aside_desc": {
        "en": "Based on published data from Korean Ministry of Education, Numbeo, and university international offices. Actual costs may vary ±20%.",
        "zh": "基于韩国教育部、Numbeo 和大学国际办公室的公开数据。实际成本可能上下浮动约 20%。",
    },
    "study.form_heading": {"en": "Tell us about your study plan", "zh": "告诉我们你的留学计划"},
    "study.city": {"en": "City", "zh": "城市"},
    "study.school_type": {"en": "School Type", "zh": "学校类型"},
    "study.housing_type": {"en": "Housing Type", "zh": "住房类型"},
    "study.lifestyle_level": {"en": "Lifestyle Level", "zh": "生活方式"},
    "study.lifestyle_help": {"en": "Budget = frugal student living. Standard = average. Premium = comfortable.", "zh": "节省型 = 节俭学生生活。标准型 = 普通。高品质 = 更舒适。"},
    "study.calculate": {"en": "Calculate Cost", "zh": "计算成本"},
    "study.calculation_failed": {"en": "Calculation failed: {error}", "zh": "计算失败：{error}"},
    "study.estimate_label": {"en": "YOUR ESTIMATE", "zh": "你的估算"},
    "study.estimate_heading": {"en": "Cost estimate for {city}", "zh": "{city} 成本估算"},
    "study.monthly_krw": {"en": "Monthly (KRW)", "zh": "月度（韩元）"},
    "study.annual_krw": {"en": "Annual (KRW)", "zh": "年度（韩元）"},
    "study.monthly_usd": {"en": "≈ Monthly (USD)", "zh": "约月度（美元）"},
    "study.breakdown": {"en": "BREAKDOWN", "zh": "成本拆分"},
    "study.money_heading": {"en": "Where your money goes", "zh": "费用流向"},
    "study.monthly_annual": {"en": "**Monthly vs Annual comparison**", "zh": "**月度与年度对比**"},
    "study.category_amounts": {"en": "**Category breakdown amounts**", "zh": "**分类金额拆分**"},
    "study.monthly_detail": {"en": "Monthly detail", "zh": "月度明细"},
    "study.ai_explanation": {"en": "AI EXPLANATION", "zh": "AI 解释"},
    "study.understanding": {"en": "Understanding your estimate", "zh": "理解你的估算"},
    "study.download_summary": {"en": "📥 Download Summary (TXT)", "zh": "📥 下载摘要（TXT）"},
    "study.recalculate": {"en": "🔄 Recalculate", "zh": "🔄 重新计算"},
    "study.empty": {"en": "Fill in your study profile above and click **Calculate Cost** to see your estimate.", "zh": "填写上方留学资料并点击 **计算成本** 查看估算。"},
    "study.footer": {"en": "Korea Compass · Study Cost Calculator v3.0", "zh": "韩国指南 · 留学成本计算器 v3.0"},

    "job.page_title": {"en": "Career & Job Market Analyzer", "zh": "职业与就业市场分析"},
    "job.brand": {"en": "V2 · MODULE 2", "zh": "V2 · 模块 2"},
    "job.heading": {"en": "Korea Career & Job Market Analyzer", "zh": "韩国职业与就业市场分析"},
    "job.subtitle": {
        "en": "Analyse salary ranges, skill requirements, and visa pathways for technology, business, operations, support, sales, and product roles in Korea. Get a personalised 3-month preparation plan based on your profile.",
        "zh": "分析韩国技术、商业、运营、支持、销售和产品岗位的薪资范围、技能要求和签证路径，并根据你的背景生成个性化 3 个月准备计划。",
    },
    "job.aside_title": {"en": "Salary data in KRW", "zh": "薪资数据单位为韩元"},
    "job.aside_desc": {"en": "Based on published salary surveys, LinkedIn data, and Korean job platforms. Actual offers vary by company size, equity, and negotiation.", "zh": "基于公开薪资调查、LinkedIn 数据和韩国招聘平台。实际 offer 会因公司规模、股权和谈判而不同。"},
    "job.form_heading": {"en": "Tell us about your background", "zh": "告诉我们你的背景"},
    "job.target_role": {"en": "Target Role", "zh": "目标岗位"},
    "job.experience": {"en": "Experience Level", "zh": "经验水平"},
    "job.korean_level": {"en": "Korean Language Level", "zh": "韩语水平"},
    "job.analyze": {"en": "Analyze Job Market", "zh": "分析就业市场"},
    "job.failed": {"en": "Analysis failed: {error}", "zh": "分析失败：{error}"},
    "job.analysis_label": {"en": "YOUR ANALYSIS", "zh": "你的分析"},
    "job.analysis_heading": {"en": "Market analysis for {role}", "zh": "{role} 市场分析"},
    "job.salary_min": {"en": "Salary Min (KRW)", "zh": "最低薪资（韩元）"},
    "job.salary_max": {"en": "Salary Max (KRW)", "zh": "最高薪资（韩元）"},
    "job.competitiveness": {"en": "Competitiveness", "zh": "竞争力"},
    "job.currency": {"en": "Currency", "zh": "币种"},
    "job.note": {"en": "**Competitiveness note:** {note}", "zh": "**竞争力说明：** {note}"},
    "job.salary_range": {"en": "### 💰 Salary Range", "zh": "### 💰 薪资范围"},
    "job.salary_range_name": {"en": "Salary range", "zh": "薪资范围"},
    "job.krw_year": {"en": "KRW / year", "zh": "韩元 / 年"},
    "job.recommended_cities": {"en": "🏙️ Recommended Cities", "zh": "🏙️ 推荐城市"},
    "job.skills_matrix": {"en": "### 🛠️ Skills Matrix", "zh": "### 🛠️ 技能矩阵"},
    "job.must_have": {"en": "**Must-Have**", "zh": "**必备技能**"},
    "job.nice_have": {"en": "**Nice-to-Have**", "zh": "**加分技能**"},
    "job.language_req": {"en": "### 🗣️ Korean Language Requirements", "zh": "### 🗣️ 韩语要求"},
    "job.level_expander": {"en": "📌 How your current level affects your options", "zh": "📌 当前水平如何影响你的选择"},
    "job.visa_pathway": {"en": "🛂 Visa Pathway", "zh": "🛂 签证路径"},
    "job.plan_label": {"en": "PREPARATION PLAN", "zh": "准备计划"},
    "job.plan_heading": {"en": "Your personalised plan", "zh": "你的个性化计划"},
    "job.download_analysis": {"en": "📥 Download Analysis (TXT)", "zh": "📥 下载分析（TXT）"},
    "job.empty": {"en": "Select your profile above and click **Analyze Job Market** to see results.", "zh": "选择上方资料并点击 **分析就业市场** 查看结果。"},
    "job.footer": {"en": "Korea Compass · Career & Job Market Analyzer v3.0", "zh": "韩国指南 · 职业与就业市场分析 v3.0"},

    "decision.page_title": {"en": "AI Korea Life Plan", "zh": "AI 韩国生活规划"},
    "decision.brand": {"en": "V2 · MODULE 3", "zh": "V2 · 模块 3"},
    "decision.heading": {"en": "AI Korea Life Plan", "zh": "AI 韩国生活规划"},
    "decision.subtitle": {"en": "Should you study, work, or live in Korea? Tell us about yourself and get a personalised report combining cost analysis, career insights, risk assessment, and a 3-month action plan.", "zh": "你适合去韩国学习、工作还是生活？告诉我们你的情况，获得结合成本、职业洞察、风险评估和 3 个月行动计划的个性化报告。"},
    "decision.aside_tag": {"en": "Rule-based engine", "zh": "规则引擎"},
    "decision.aside_title": {"en": "Combines 4 risk dimensions", "zh": "结合 4 个风险维度"},
    "decision.aside_desc": {"en": "Financial · Language · Career · Visa & Living", "zh": "财务 · 语言 · 职业 · 签证与生活"},
    "decision.form_heading": {"en": "Tell us about your Korea plan", "zh": "告诉我们你的韩国计划"},
    "decision.goal": {"en": "Goal", "zh": "目标"},
    "decision.target_city": {"en": "Target City", "zh": "目标城市"},
    "decision.monthly_budget": {"en": "Monthly Budget (KRW)", "zh": "月度预算（韩元）"},
    "decision.budget_help": {"en": "Your estimated monthly budget in Korean Won (tuition + living expenses).", "zh": "你的韩元月度预算估计（学费 + 生活费）。"},
    "decision.generate": {"en": "Generate AI Korea Life Plan", "zh": "生成 AI 韩国生活规划"},
    "decision.failed": {"en": "Failed to generate report: {error}", "zh": "生成报告失败：{error}"},
    "decision.recommendation": {"en": "RECOMMENDATION", "zh": "建议"},
    "decision.overall": {"en": "OVERALL RECOMMENDATION", "zh": "总体建议"},
    "decision.financial_fit": {"en": "## 💰 Financial Fit", "zh": "## 💰 财务匹配度"},
    "decision.est_monthly": {"en": "Est. Monthly Cost", "zh": "估算月成本"},
    "decision.est_annual": {"en": "Est. Annual Cost", "zh": "估算年成本"},
    "decision.budget_gap": {"en": "Budget Gap", "zh": "预算差额"},
    "decision.financial_risk": {"en": "Financial Risk", "zh": "财务风险"},
    "decision.budget": {"en": "Budget", "zh": "预算"},
    "decision.est_cost": {"en": "Est. Cost", "zh": "估算成本"},
    "decision.budget_chart": {"en": "Monthly Budget vs Estimated Cost", "zh": "月度预算 vs 估算成本"},
    "decision.career_fit": {"en": "## 💻 Career Fit", "zh": "## 💻 职业匹配度"},
    "decision.salary_range": {"en": "Salary Range", "zh": "薪资范围"},
    "decision.career_risk": {"en": "Career Risk", "zh": "职业风险"},
    "decision.required_skills": {"en": "**Required Skills:** {skills}", "zh": "**所需技能：** {skills}"},
    "decision.career_na": {"en": "Career assessment not applicable to your current goal.", "zh": "职业评估不适用于你当前的目标。"},
    "decision.risk_assessment": {"en": "## ⚠️ Risk Assessment", "zh": "## ⚠️ 风险评估"},
    "decision.risk_financial": {"en": "Financial", "zh": "财务"},
    "decision.risk_language": {"en": "Language", "zh": "语言"},
    "decision.risk_career": {"en": "Career", "zh": "职业"},
    "decision.risk_visa": {"en": "Visa & Living", "zh": "签证与生活"},
    "decision.risk_budget_gap": {"en": "Budget gap: {gap:+,} KRW", "zh": "预算差额：{gap:+,} 韩元"},
    "decision.risk_chart": {"en": "Risk Profile (3=Low, 1=High)", "zh": "风险画像（3=低，1=高）"},
    "decision.action_plan": {"en": "## 📋 3-Month Action Plan", "zh": "## 📋 3 个月行动计划"},
    "decision.export": {"en": "## 📥 Export", "zh": "## 📥 导出"},
    "decision.download_summary": {"en": "📥 Download Summary (TXT)", "zh": "📥 下载摘要（TXT）"},
    "decision.download_md": {"en": "📥 Download Markdown", "zh": "📥 下载 Markdown"},
    "decision.download_json": {"en": "📥 Download Full Report (JSON)", "zh": "📥 下载完整报告（JSON）"},
    "decision.empty": {"en": "Fill in your profile above and click **Generate AI Korea Life Plan** to see your personalised report.", "zh": "填写上方资料并点击 **生成 AI 韩国生活规划** 查看你的个性化报告。"},
    "decision.footer": {"en": "Korea Compass · AI Korea Life Plan v3.0", "zh": "韩国指南 · AI 韩国生活规划 v3.0"},

    "news.page_title": {"en": "News & Policy", "zh": "新闻与政策"},
    "news.brand": {"en": "V2 · MODULE 4", "zh": "V2 · 模块 4"},
    "news.heading": {"en": "Korea News & Policy", "zh": "韩国新闻与政策"},
    "news.subtitle": {"en": "Recent developments in Korea that affect your study, work, visa, economy, and technology decisions. Based on curated sources — updated periodically.", "zh": "影响你留学、工作、签证、经济和科技决策的韩国近期动态。基于精选来源，并定期更新。"},
    "news.aside_tag": {"en": "Mock data · MVP", "zh": "模拟数据 · MVP"},
    "news.aside_title": {"en": "15 curated items", "zh": "15 条精选内容"},
    "news.aside_desc": {"en": "Covers study, work, visa, economy, and technology categories. Live news API integration planned for future release.", "zh": "覆盖留学、工作、签证、经济和科技类别。实时新闻 API 计划在未来版本接入。"},
    "news.search_label": {"en": "SEARCH", "zh": "搜索"},
    "news.find_heading": {"en": "Find relevant news", "zh": "查找相关新闻"},
    "news.keyword": {"en": "Keyword", "zh": "关键词"},
    "news.placeholder": {"en": "e.g. visa, AI, scholarship, TOPIK...", "zh": "例如：签证、AI、奖学金、TOPIK..."},
    "news.category": {"en": "Category", "zh": "类别"},
    "news.time_range": {"en": "Time Range", "zh": "时间范围"},
    "news.search_button": {"en": "Search News & Policy", "zh": "搜索新闻与政策"},
    "news.failed": {"en": "Search failed: {error}", "zh": "搜索失败：{error}"},
    "news.results_found": {"en": "Results found", "zh": "找到结果"},
    "news.ai_summary": {"en": "AI Summary", "zh": "AI 摘要"},
    "news.suggestions": {"en": "Suggestions", "zh": "建议"},
    "news.trend": {"en": "### 📈 AI Trend Summary", "zh": "### 📈 AI 趋势摘要"},
    "news.action": {"en": "### 💡 Action Suggestions", "zh": "### 💡 行动建议"},
    "news.category_distribution": {"en": "Category Distribution", "zh": "类别分布"},
    "news.relevance_scores": {"en": "Relevance Scores", "zh": "相关性评分"},
    "news.no_items": {"en": "No items match your search criteria. Try broadening your keywords or time range.", "zh": "没有内容匹配搜索条件。请放宽关键词或时间范围。"},
    "news.results_heading": {"en": "### 📄 Results ({count})", "zh": "### 📄 结果（{count}）"},
    "news.impact": {"en": "Impact analysis", "zh": "影响分析"},
    "news.for_students": {"en": "For students:", "zh": "对学生："},
    "news.for_job_seekers": {"en": "For job seekers:", "zh": "对求职者："},
    "news.download": {"en": "📥 Download Results (TXT)", "zh": "📥 下载结果（TXT）"},
    "news.empty": {"en": "Enter a keyword and click **Search News & Policy** to see results.", "zh": "输入关键词并点击 **搜索新闻与政策** 查看结果。"},
    "news.footer": {"en": "Korea Compass · News & Policy v3.0 (mock data)", "zh": "韩国指南 · 新闻与政策 v3.0（模拟数据）"},

    "legacy.comparison.title": {"en": "📊 East Asia Comparison Lab", "zh": "📊 东亚对比实验室"},
    "legacy.comparison.caption": {"en": "Compare six countries across six dimensions. All scores are normalised to a 0–10 scale.", "zh": "比较六个国家在六个维度上的表现。所有分数均标准化为 0–10 分。"},
    "legacy.comparison.backend": {"en": "Cannot connect to backend: {error}", "zh": "无法连接后端：{error}"},
    "legacy.comparison.radar": {"en": "🕸️ Radar Comparison", "zh": "🕸️ 雷达图对比"},
    "legacy.comparison.select_countries": {"en": "Select countries to compare", "zh": "选择要对比的国家"},
    "legacy.comparison.select_one": {"en": "Select at least one country to show the radar chart.", "zh": "至少选择一个国家以显示雷达图。"},
    "legacy.comparison.breakdown": {"en": "📊 Category Breakdown", "zh": "📊 维度拆分"},
    "legacy.comparison.select_category": {"en": "Select a category", "zh": "选择维度"},
    "legacy.comparison.score": {"en": "Score (0–10)", "zh": "分数（0–10）"},
    "legacy.comparison.no_category": {"en": "No data for category: {category}", "zh": "该维度暂无数据：{category}"},
    "legacy.comparison.raw": {"en": "📋 Raw Data", "zh": "📋 原始数据"},
    "legacy.comparison.country": {"en": "Country", "zh": "国家"},

    "survey.page_title": {"en": "Korea Perception Survey", "zh": "韩国感知调查"},
    "survey.hero_tag": {"en": "DAY 3 · PERCEPTION ENGINE", "zh": "第 3 天 · 感知引擎"},
    "survey.heading": {"en": "Korea Perception Survey", "zh": "韩国感知调查"},
    "survey.subtitle": {"en": "Capture how people perceive Korea across six dimensions, compare each response with the platform baseline, and turn community perception into a live product signal.", "zh": "记录人们在六个维度上如何看待韩国，将每次回答与平台基准对比，并把社区感知转化为实时产品信号。"},
    "survey.aside_tag": {"en": "Interactive product layer", "zh": "互动产品层"},
    "survey.aside_title": {"en": "From benchmark data to user perception", "zh": "从基准数据到用户感知"},
    "survey.aside_desc": {"en": "Repeated submissions are allowed. No login, no authentication, no paid APIs.", "zh": "允许重复提交。无需登录、无需认证、无需付费 API。"},
    "survey.scale_note": {"en": "Scores use a 1–10 scale. Default slider values are valid.", "zh": "分数使用 1–10 分制。默认滑块值也是有效提交。"},
    "survey.api_unavailable": {"en": "Perception Survey API unavailable: {error}", "zh": "感知调查 API 不可用：{error}"},
    "survey.input_label": {"en": "SURVEY INPUT", "zh": "调查输入"},
    "survey.submit_heading": {"en": "Submit a perception response", "zh": "提交一份感知回答"},
    "survey.display_name": {"en": "Display name / nickname", "zh": "显示名称 / 昵称"},
    "survey.economy": {"en": "Economy", "zh": "经济"},
    "survey.technology": {"en": "Technology", "zh": "科技"},
    "survey.education": {"en": "Education", "zh": "教育"},
    "survey.culture": {"en": "Culture", "zh": "文化"},
    "survey.global_influence": {"en": "Global Influence", "zh": "全球影响力"},
    "survey.quality_of_life": {"en": "Quality of Life", "zh": "生活质量"},
    "survey.comment": {"en": "What shaped your perception of Korea?", "zh": "是什么塑造了你对韩国的看法？"},
    "survey.comment_placeholder": {"en": "Optional: media, travel, school, friends, K-pop, work, news...", "zh": "可选：媒体、旅行、学校、朋友、K-pop、工作、新闻..."},
    "survey.submit": {"en": "Submit perception survey", "zh": "提交感知调查"},
    "survey.cannot_submit": {"en": "Cannot submit yet because the backend API is unavailable.", "zh": "后端 API 不可用，暂时无法提交。"},
    "survey.submitted": {"en": "Survey submitted.", "zh": "调查已提交。"},
    "survey.submit_failed": {"en": "Survey submission failed: {error}", "zh": "调查提交失败：{error}"},
    "survey.result_label": {"en": "YOUR RESULT", "zh": "你的结果"},
    "survey.profile_heading": {"en": "Your Korea perception profile", "zh": "你的韩国感知画像"},
    "survey.score": {"en": "Your Korea Perception Score", "zh": "你的韩国感知分数"},
    "survey.strongest": {"en": "Strongest category", "zh": "最强维度"},
    "survey.weakest": {"en": "Weakest category", "zh": "最弱维度"},
    "survey.generate_ai": {"en": "Generate AI Insight", "zh": "生成 AI 洞察"},
    "survey.cannot_ai": {"en": "Cannot generate report because the backend API is unavailable.", "zh": "后端 API 不可用，无法生成报告。"},
    "survey.ai_failed": {"en": "AI insight generation failed: {error}", "zh": "AI 洞察生成失败：{error}"},
    "survey.empty": {"en": "Submit a survey to see your result card and radar comparison.", "zh": "提交调查后可查看结果卡片和雷达图对比。"},
    "survey.stats_label": {"en": "COMMUNITY STATS", "zh": "社区统计"},
    "survey.stats_heading": {"en": "Community perception snapshot", "zh": "社区感知快照"},
    "survey.stats_unavailable": {"en": "Community stats are unavailable until the backend is running.", "zh": "后端运行前社区统计不可用。"},
    "survey.no_submissions": {"en": "No community submissions yet. Be the first to create the perception baseline.", "zh": "还没有社区提交。成为第一个建立感知基准的人。"},
    "survey.total": {"en": "Total submissions", "zh": "提交总数"},
    "survey.average": {"en": "Average perception score", "zh": "平均感知分数"},
    "survey.strongest_perceived": {"en": "Strongest perceived category", "zh": "最强感知维度"},
    "survey.weakest_perceived": {"en": "Weakest perceived category", "zh": "最弱感知维度"},
    "survey.community_average": {"en": "Community average", "zh": "社区平均"},
    "survey.korea_baseline": {"en": "Korea baseline", "zh": "韩国基准"},
    "survey.your_perception": {"en": "Your perception", "zh": "你的感知"},
    "survey.ai_label": {"en": "AI INSIGHT", "zh": "AI 洞察"},
    "survey.structured_report": {"en": "Structured perception report", "zh": "结构化感知报告"},
    "survey.provider_openai": {"en": "Generated with AI provider", "zh": "由 AI 提供方生成"},
    "survey.provider_local": {"en": "Generated with local template", "zh": "由本地模板生成"},
    "survey.summary": {"en": "Perception Summary", "zh": "感知摘要"},
    "survey.associations": {"en": "### Strongest Associations", "zh": "### 最强关联"},
    "survey.baseline_comparison": {"en": "### Korea Baseline Comparison", "zh": "### 韩国基准对比"},
    "survey.gaps": {"en": "### Concerns / Gaps", "zh": "### 顾虑 / 差距"},
    "survey.community_comparison": {"en": "### Community Average Comparison", "zh": "### 社区平均对比"},
    "survey.interpretation": {"en": "### Interpretation Profile", "zh": "### 解读画像"},
    "survey.next_question": {"en": "### Suggested Next Question", "zh": "### 建议的下一个问题"},

    "community.page_title": {"en": "Community Insights", "zh": "社区洞察"},
    "community.hero_tag": {"en": "STEP K5 · COMMUNITY ANALYTICS", "zh": "步骤 K5 · 社区分析"},
    "community.heading": {"en": "Community Insights", "zh": "社区洞察"},
    "community.subtitle": {"en": "See how the community perceives Korea across six dimensions, which interpretation profiles are emerging, and what respondents say shaped their views.", "zh": "查看社区在六个维度上如何看待韩国、正在出现哪些解读画像，以及受访者如何描述他们观点的来源。"},
    "community.aside_tag": {"en": "Live survey intelligence", "zh": "实时调查智能"},
    "community.aside_title": {"en": "From individual answers to shared signals", "zh": "从个人回答到共同信号"},
    "community.aside_desc": {"en": "Every survey response updates this page automatically.", "zh": "每份调查回答都会自动更新本页。"},
    "community.no_auth": {"en": "No authentication or account data is used.", "zh": "不使用认证或账号数据。"},
    "community.api_unavailable": {"en": "Community Insights API unavailable: {error}", "zh": "社区洞察 API 不可用：{error}"},
    "community.first": {"en": "Be the first participant in the Korea Perception Survey.", "zh": "成为韩国感知调查的第一位参与者。"},
    "community.take_survey": {"en": "Take Perception Survey", "zh": "参加感知调查"},
    "community.snapshot_label": {"en": "COMMUNITY SNAPSHOT", "zh": "社区快照"},
    "community.snapshot": {"en": "Community Snapshot", "zh": "社区快照"},
    "community.total": {"en": "Total Responses", "zh": "回答总数"},
    "community.average": {"en": "Average Score", "zh": "平均分"},
    "community.strongest": {"en": "Strongest Category", "zh": "最强维度"},
    "community.weakest": {"en": "Weakest Category", "zh": "最弱维度"},
    "community.ranking": {"en": "Category Ranking", "zh": "维度排名"},
    "community.radar": {"en": "Community Radar", "zh": "社区雷达图"},
    "community.profiles_label": {"en": "COMMUNITY PROFILES", "zh": "社区画像"},
    "community.profile_distribution": {"en": "Profile Distribution", "zh": "画像分布"},
    "community.voices_label": {"en": "RECENT VOICES", "zh": "近期声音"},
    "community.voices": {"en": "Recent Voices", "zh": "近期声音"},
    "community.no_comments": {"en": "No comments available yet.", "zh": "暂无评论。"},
    "community.average_score": {"en": "Average score", "zh": "平均分"},
    "community.average_trace": {"en": "Community average", "zh": "社区平均"},
}


def get_language() -> str:
    language = st.session_state.get("language", "en")
    return language if language in SUPPORTED_LANGUAGES else "en"


def set_language(language: str) -> None:
    st.session_state["language"] = language if language in SUPPORTED_LANGUAGES else "en"


def t(key: str, **kwargs) -> str:
    language = get_language()
    entry = _TRANSLATIONS.get(key, {})
    text = entry.get(language) or entry.get("en") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def language_selector(key: str = "language_selector") -> str:
    current = get_language()
    labels = list(SUPPORTED_LANGUAGES.values())
    selected_label = st.selectbox(
        t("common.language"),
        labels,
        index=list(SUPPORTED_LANGUAGES).index(current),
        key=key,
    )
    selected_language = _LANGUAGE_BY_LABEL[selected_label]
    if selected_language != current:
        set_language(selected_language)
        st.rerun()
    return selected_language


def _display_value(labels: dict[str, dict[str, str]], value: str) -> str:
    entry = labels.get(value, {})
    return entry.get(get_language()) or entry.get("en") or value


def translate_option(category: str, value: str) -> str:
    return _display_value(OPTION_LABELS.get(category, {}), value)


def option_value_from_label(category: str, label: str) -> str:
    labels = OPTION_LABELS.get(category, {})
    language = get_language()
    for value, entry in labels.items():
        if label in (entry.get(language), entry.get("en")):
            return value
    return label


def translate_result_label(value: str) -> str:
    return _display_value(RESULT_LABELS, value)


def display_role(role: str) -> str:
    return translate_option("role", role)


def display_goal(goal: str) -> str:
    return translate_option("goal", goal)


def display_news_category(category: str) -> str:
    return translate_option("news_category", category)


def display_time_range(time_range: str) -> str:
    return translate_option("time_range", time_range)


def translation_key_count() -> int:
    return len(_TRANSLATIONS)
