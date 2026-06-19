import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from locales.i18n import language_selector, t
from api_client import API_BASE_URL, APIClient

st.set_page_config(
    page_title=t("home.page_title"),
    page_icon="🌏",
    layout="wide",
)

from ui_style import apply_product_style
apply_product_style()

api = APIClient()

# ── Hero ──

st.markdown(
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>{t("home.brand")}</div>
        <h1>{t("home.heading")}</h1>
        <p>
            {t("home.subtitle")}
        </p>
        <div class="hero-kpi">
            <div class="kpi-card"><strong>V2</strong><span>{t("home.kpi.study")}</span></div>
            <div class="kpi-card"><strong>V2+</strong><span>{t("home.kpi.job")}</span></div>
            <div class="kpi-card"><strong>V2+</strong><span>{t("home.kpi.report")}</span></div>
        </div>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{t("home.aside_tag")}</div>
            <h3 style="margin-top:1.2rem;">{t("home.aside_title")}</h3>
            <p style="color:#cbd5e1;">
                {t("home.aside_desc")}
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">
                {t("home.stack")}
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

language_selector("home_language")

col1, col2, col3, col4 = st.columns(4)
col1.metric(t("home.metric.modules"), "4")
col2.metric(t("home.metric.focus"), "Korea")
col3.metric(t("home.metric.exports"), "CSV/TXT/MD/JSON")
try:
    api.health()
    col4.metric(t("home.metric.api"), t("home.api_online"))
except Exception:
    col4.metric(t("home.metric.api"), t("home.api_offline"))

st.divider()

# ── Demo Flow ──

st.markdown(f'<div class="section-label">{t("home.demo_label")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('home.demo_heading')}")

flow_cols = st.columns(4)
flow_steps = [
    ("1", "📚", t("home.flow.study.title"), t("home.flow.study.desc")),
    ("2", "💻", t("home.flow.job.title"), t("home.flow.job.desc")),
    ("3", "🧭", t("home.flow.report.title"), t("home.flow.report.desc")),
    ("4", "📰", t("home.flow.news.title"), t("home.flow.news.desc")),
]
for i, (num, icon, title, desc) in enumerate(flow_steps):
    with flow_cols[i]:
        st.markdown(
            f"""
        <div style="text-align:center; padding:1rem; border:1px solid #dbe3ef; border-radius:8px;
                    background:#ffffff; min-height:180px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#123c9c; color:white;
                        display:flex; align-items:center; justify-content:center; margin:0 auto 0.5rem;
                        font-weight:800;">{num}</div>
            <div style="font-size:1.5rem; margin-bottom:0.3rem;">{icon}</div>
            <div style="font-weight:700; font-size:0.95rem; margin-bottom:0.3rem;">{title}</div>
            <div style="color:#64748b; font-size:0.85rem;">{desc}</div>
        </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ── Navigation ──

st.markdown(f'<div class="section-label">{t("home.tools")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('home.modules')}")

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown(
        f"""
    <div class="module-card">
        <div class="module-tag">{t("home.nav.new")}</div>
        <h3>📚 {t("home.kpi.study")}</h3>
        <p>{t("home.study.desc")}</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t("home.open_calculator"), use_container_width=True, key="nav_study"):
        st.switch_page("pages/1_Study_Cost.py")

with r2:
    st.markdown(
        f"""
    <div class="module-card">
        <div class="module-tag">{t("home.nav.new")}</div>
        <h3>💻 {t("job.page_title")}</h3>
        <p>{t("home.job.desc")}</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t("home.open_analyzer"), use_container_width=True, key="nav_job"):
        st.switch_page("pages/2_Job_Market.py")

with r3:
    st.markdown(
        f"""
    <div class="module-card">
        <div class="module-tag">{t("home.nav.new")}</div>
        <h3>🧭 {t("decision.page_title")}</h3>
        <p>{t("home.report.desc")}</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t("home.open_report"), use_container_width=True, key="nav_decision"):
        st.switch_page("pages/3_Decision_Report.py")

with r4:
    st.markdown(
        f"""
    <div class="module-card">
        <div class="module-tag">{t("home.nav.new")}</div>
        <h3>📰 {t("news.page_title")}</h3>
        <p>{t("home.news.desc")}</p>
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
        t("home.api_caption") if API_BASE_URL else t("home.api_fallback_caption")
    )
