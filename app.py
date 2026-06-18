import streamlit as st

st.set_page_config(
    page_title="Korea Analysis",
    page_icon="🌏",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()

# ── Hero ──

st.markdown(
    """
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>KOREA STUDY & CAREER DECISION AGENT</div>
        <h1>Should I study, work, or live in Korea?</h1>
        <p>
            A practical decision assistant for international students and job seekers considering Korea.
            Estimate costs, analyse job markets, and get personalised AI reports.
        </p>
        <div class="hero-kpi">
            <div class="kpi-card"><strong>V2</strong><span>Study Cost Calculator</span></div>
            <div class="kpi-card"><strong>V2+</strong><span>Job Market Analyzer</span></div>
            <div class="kpi-card"><strong>V2+</strong><span>AI Decision Report</span></div>
        </div>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>V2 · ISSUE #2</div>
            <h3 style="margin-top:1.2rem;">Study Cost Calculator</h3>
            <p style="color:#cbd5e1;">
                Curated data · Plotly charts · AI explanations · Persistent history
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">
                Streamlit · FastAPI · SQLite · Plotly · Dual AI provider
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

# ── Dynamic KPIs ──

try:
    scores = api.get_country_scores()
    all_countries = sorted(set(s["country"] for s in scores))
    all_categories = sorted(set(s["category"] for s in scores))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Data points", len(scores))
    col2.metric("Countries", len(all_countries))
    col3.metric("Categories", len(all_categories))
    col4.metric("API", "✅ Online")
except Exception as e:
    st.warning(f"Backend not reachable: {e}")
    st.info("Start the backend: `cd backend && uvicorn app.main:app --reload`")
    scores = []
    all_countries = ["Korea", "Japan", "China", "Singapore", "Vietnam", "Thailand"]
    all_categories = [
        "Economy", "Technology", "Education",
        "Culture", "Global Influence", "Quality of Life",
    ]

st.divider()

# ── Country Cards ──

st.markdown('<div class="section-label">REGIONAL CONTEXT</div>', unsafe_allow_html=True)
st.markdown("## Korea in its East Asian context")
st.caption("Six economies and six shared dimensions provide the benchmark behind the product.")

FLAGS = {
    "Korea": "🇰🇷", "Japan": "🇯🇵", "China": "🇨🇳",
    "Singapore": "🇸🇬", "Vietnam": "🇻🇳", "Thailand": "🇹🇭",
}

cols = st.columns(3)
for i, country in enumerate(all_countries):
    flag = FLAGS.get(country, "🌏")
    with cols[i % 3]:
        count = sum(1 for s in scores if s["country"] == country) if scores else 0
        st.markdown(
            f"""
        <div class="module-card" style="min-height:120px;">
            <div class="module-tag">{flag} {country}</div>
            <h3 style="font-size:1.5rem;margin:0.5rem 0;">{country}</h3>
            <p>{count} data points · 6 categories</p>
        </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ── Demo Flow ──

st.markdown('<div class="section-label">PORTFOLIO DEMO FLOW</div>', unsafe_allow_html=True)
st.markdown("## Try the full workflow in 4 steps")

flow_cols = st.columns(4)
flow_steps = [
    ("1", "📚", "Calculate Study Cost", "Estimate monthly and annual costs for your Korea study plan."),
    ("2", "💻", "Analyze Job Market", "See salary ranges, required skills, and visa pathways for tech roles."),
    ("3", "🧭", "Generate Decision Report", "Combine cost + career into a personalised recommendation with action plan."),
    ("4", "📰", "Check News & Policy", "Search recent Korea visa, study, work, and tech policy updates."),
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

st.markdown('<div class="section-label">TOOLS</div>', unsafe_allow_html=True)
st.markdown("## Decision modules")

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">V2 · NEW</div>
        <h3>📚 Study Cost Calculator</h3>
        <p>Estimate your monthly and annual costs for studying in Korea across different cities and lifestyles.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Calculator", use_container_width=True, key="nav_study"):
        st.switch_page("pages/1_Study_Cost.py")

with r2:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">V2 · NEW</div>
        <h3>💻 IT Job Market Analyzer</h3>
        <p>Analyze Korean tech job requirements, salary ranges, and visa pathways.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Analyzer", use_container_width=True, key="nav_job"):
        st.switch_page("pages/2_Job_Market.py")

with r3:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">V2 · NEW</div>
        <h3>🧭 AI Decision Report</h3>
        <p>Get a personalised report on studying, working, or living in Korea.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Report", use_container_width=True, key="nav_decision"):
        st.switch_page("pages/3_Decision_Report.py")

with r4:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">V2 · NEW</div>
        <h3>📰 News & Policy</h3>
        <p>Recent Korea study, work, visa, economy, and technology developments.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open News", use_container_width=True, key="nav_news"):
        st.switch_page("pages/4_News_Policy.py")

st.markdown('<div class="section-label">LEGACY MODULES</div>', unsafe_allow_html=True)
st.markdown("## V1 features (still active)")

legacy1, legacy2, legacy3, legacy4 = st.columns(4)
with legacy1:
    if st.button("📊 Comparison Lab", use_container_width=True):
        st.switch_page("pages/1_Comparison_Lab.py")
with legacy2:
    if st.button("🧭 Perception Survey", use_container_width=True):
        st.switch_page("pages/2_Perception_Survey.py")
with legacy3:
    if st.button("✨ AI Insight", use_container_width=True):
        st.switch_page("pages/2_Perception_Survey.py")
with legacy4:
    if st.button("👥 Community Insights", use_container_width=True):
        st.switch_page("pages/3_Community_Insights.py")

st.markdown('<div class="section-label">DEVELOPER ACCESS</div>', unsafe_allow_html=True)
dev1, dev2 = st.columns([1, 2])
with dev1:
    st.link_button("Open API Documentation", "http://localhost:8000/docs", use_container_width=True)
with dev2:
    st.caption(
        "FastAPI exposes country benchmarks, survey submissions, community summaries, "
        "and structured perception reports."
    )
