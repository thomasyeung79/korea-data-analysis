import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import API_BASE_URL, APIClient
from locales.i18n import get_language, language_selector, t
from ui_style import apply_product_style

st.set_page_config(
    page_title="Korea Compass",
    page_icon="🧭",
    layout="wide",
)
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


language_selector("home_language")

st.markdown(
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS</div>
        <h1>Korea Compass</h1>
        <p>{label("Your AI Guide to Study, Work & Life in South Korea", "你的韩国留学、求职与生活 AI 指南")}</p>
        <div class="hero-kpi">
            <div class="kpi-card"><strong>Study</strong><span>{label("Plan study path", "规划留学路径")}</span></div>
            <div class="kpi-card"><strong>Career</strong><span>{label("Analyze job outlook", "分析职业前景")}</span></div>
            <div class="kpi-card"><strong>Living</strong><span>{label("Estimate life fit", "评估生活匹配")}</span></div>
        </div>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>V6 · REAL DATA & KNOWLEDGE BASE EDITION</div>
            <h3 style="margin-top:1.2rem;">{label("One profile, one Korea plan", "一个画像，一份韩国规划")}</h3>
            <p style="color:#cbd5e1;">
                {label("Create a reusable profile, compare city fit, estimate costs, review career readiness, and generate an exportable AI Korea Life Plan.", "创建可复用画像，比较城市匹配度，估算成本，评估职业准备度，并生成可导出的 AI 韩国发展规划。")}
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">
                Streamlit · FastAPI · SQLite · Plotly · Knowledge Base · Rule-based AI fallback
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
col1.metric(label("Planning Areas", "规划方向"), "3")
col2.metric(label("Core Modules", "核心模块"), "8")
col3.metric(label("Exports", "导出格式"), "TXT/MD/JSON")
try:
    api.health()
    col4.metric("API", label("Online", "在线"))
except Exception:
    col4.metric("API", label("Local fallback", "本地备用模式"))

st.divider()

st.markdown(f'<div class="section-label">{label("PORTFOLIO DEMO FLOW", "作品集演示流程")}</div>', unsafe_allow_html=True)
st.markdown(f"## {label('Try the Korea planning workflow in 6 steps', '用 6 步体验韩国规划流程')}")

flow_steps = [
    ("1", "🌏", label("Explore Korea", "探索韩国"), label("Browse country basics, cities, culture, history, costs, and quick facts.", "浏览国家概览、城市、文化、历史、成本和实用信息。")),
    ("2", "📚", label("Study Planning", "留学规划"), label("Estimate Korean study costs and budget fit.", "估算韩国留学成本和预算匹配度。")),
    ("3", "💼", label("Career Planning", "职业规划"), label("Review role-specific salary, skills, cities, and visa options.", "查看岗位薪资、技能、城市和签证路径。")),
    ("4", "🏙️", label("Living Guide", "生活指南"), label("Compare city fit across cost, lifestyle, and language readiness.", "比较城市在成本、生活方式和语言匹配上的表现。")),
    ("5", "🗣", label("Korean Learning", "韩语场景支持"), label("Learn Korean expressions for real study, work, and living situations.", "学习真实留学、工作和生活场景中的韩语表达。")),
    ("6", "🧭", label("AI Korea Life Plan", "AI 韩国发展规划"), label("Combine study, work, living, risks, visa, and action plans.", "整合留学、工作、生活、风险、签证和行动计划。")),
]

for row_start in (0, 3):
    cols = st.columns(3)
    for col, (num, icon, title, desc) in zip(cols, flow_steps[row_start:row_start + len(cols)]):
        with col:
            st.markdown(
                f"""
<div style="padding:1rem; border:1px solid #dbe3ef; border-radius:8px; background:#ffffff; min-height:172px;">
    <div style="width:36px; height:36px; border-radius:50%; background:#123c9c; color:white;
                display:flex; align-items:center; justify-content:center; margin-bottom:0.6rem;
                font-weight:800;">{num}</div>
    <div style="font-size:1.5rem; margin-bottom:0.3rem;">{icon}</div>
    <div style="font-weight:800; font-size:1rem; margin-bottom:0.35rem;">{title}</div>
    <div style="color:#64748b; font-size:0.9rem;">{desc}</div>
</div>
                """,
                unsafe_allow_html=True,
            )

st.divider()

st.markdown(f'<div class="section-label">{label("MODULES", "模块")}</div>', unsafe_allow_html=True)
st.markdown(f"## {label('Explore / Study / Work / Live / Korean / AI', '探索 / 留学 / 工作 / 生活 / 韩语 / AI')}")

modules = [
    ("🌏", label("Explore Korea", "探索韩国"), label("Learn the country basics: cities, culture, history, cost of living, and quick facts.", "了解韩国基础信息：城市、文化、历史、生活成本和实用信息。"), "pages/1_Explore_Korea.py", label("Open Explore Korea", "打开探索韩国")),
    ("📚", label("Study in Korea", "韩国留学"), label("Estimate tuition, housing, food, transport, insurance, and annual study cost.", "估算学费、住房、饮食、交通、保险和年度留学成本。"), "pages/1_Study_Cost.py", t("home.open_calculator")),
    ("💼", label("Work in Korea", "韩国求职"), label("Analyze salary ranges, skills, city fit, language requirements, and visa pathways.", "分析薪资范围、技能、城市匹配、语言要求和签证路径。"), "pages/2_Job_Market.py", t("home.open_analyzer")),
    ("🏙️", label("Live in Korea", "韩国生活"), label("Rank Korean cities using study, career, living, cost, language, and lifestyle scores.", "基于留学、职业、生活、成本、语言和生活方式评分推荐城市。"), "pages/5_City_Recommendation.py", label("Open Living Guide", "打开生活指南")),
    ("🗣", label("Korean Learning", "韩语场景支持"), label("Use scene-based Korean support for classrooms, interviews, offices, restaurants, hospitals, banks, and TOPIK planning.", "使用场景式韩语支持，覆盖课堂、面试、办公室、餐厅、医院、银行和 TOPIK 规划。"), "pages/7_Korean_Learning.py", label("Open Korean Learning", "打开韩语支持")),
    ("🧭", label("AI Korea Life Plan", "AI 韩国发展规划"), label("Generate an exportable Korea plan with 3, 6, and 12-month actions.", "生成可导出的韩国规划，包含 3、6、12 个月行动计划。"), "pages/6_AI_Korea_Life_Plan.py", label("Open Life Plan", "打开生活规划")),
]

for row_start in (0, 3):
    cols = st.columns(3)
    for index, (icon, title, desc, page, button) in enumerate(modules[row_start:row_start + len(cols)], start=row_start):
        with cols[index - row_start]:
            st.markdown(
                f"""
<div class="module-card">
    <div class="module-tag">V5</div>
    <h3>{icon} {title}</h3>
    <p>{desc}</p>
</div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(button, use_container_width=True, key=f"nav_{index}"):
                st.switch_page(page)

st.markdown(f"### {label('Planning Utilities', '规划辅助工具')}")
u1, u2 = st.columns(2)
with u1:
    st.markdown(
        f"""
<div class="module-card">
    <div class="module-tag">V3</div>
    <h3>🧩 {label("Profile Center", "个人画像")}</h3>
    <p>{label("Create one reusable profile for every Korea Compass module.", "创建一个可供所有模块复用的个人画像。")}</p>
</div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(label("Open Profile Center", "打开个人画像"), use_container_width=True, key="nav_profile"):
        st.switch_page("pages/0_Profile_Center.py")
with u2:
    st.markdown(
        f"""
<div class="module-card">
    <div class="module-tag">V3</div>
    <h3>📰 {t("news.page_title")}</h3>
    <p>{label("Check curated study, work, visa, economy, and technology updates.", "查看精选留学、工作、签证、经济和科技动态。")}</p>
</div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t("home.open_news"), use_container_width=True, key="nav_news"):
        st.switch_page("pages/4_News_Policy.py")

st.markdown(f'<div class="section-label">{t("home.dev_label")}</div>', unsafe_allow_html=True)
dev1, dev2 = st.columns([1, 2])
with dev1:
    if API_BASE_URL:
        st.link_button(t("home.api_docs"), f"{API_BASE_URL}/docs", use_container_width=True)
    else:
        st.button(t("home.api_docs"), use_container_width=True, disabled=True)
with dev2:
    st.caption(
        label(
            "FastAPI powers profile persistence, city recommendations, Korea Life Plan generation, study cost, career analysis, and news/policy search. On Streamlit Cloud, local fallback keeps the demo usable when a backend is not configured.",
            "FastAPI 支持画像持久化、城市推荐、韩国生活规划生成、留学成本、职业分析和新闻政策搜索。在 Streamlit Cloud 未配置后端时，本地备用模式会保持演示可用。",
        )
    )

st.caption(t("common.footer"))

