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
        <div class="brand-row"><span class="brand-dot"></span>KOREA ANALYSIS</div>
        <h1>Understanding Korea Through Data</h1>
        <p>
            An interactive product for comparing regional benchmarks, measuring public perception,
            generating structured insights, and discovering community views of Korea.
        </p>
        <div class="hero-kpi">
            <div class="kpi-card"><strong>Compare</strong><span>Regional benchmarks</span></div>
            <div class="kpi-card"><strong>Perceive</strong><span>Interactive survey</span></div>
            <div class="kpi-card"><strong>Understand</strong><span>AI and community insights</span></div>
        </div>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>PORTFOLIO RELEASE · K6</div>
            <h3 style="margin-top:1.2rem;">A complete data product workflow</h3>
            <p style="color:#cbd5e1;">
                Explore benchmark data, submit a perception profile, generate a structured report,
                and see how your view compares with the community.
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">
                Streamlit · FastAPI · SQLite · Plotly · OpenAI-compatible fallback architecture
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

# ── Navigation ──

st.markdown('<div class="section-label">PRODUCT WORKFLOW</div>', unsafe_allow_html=True)
st.markdown("## Compare. Perceive. Analyze. Understand.")

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">01 · COMPARE</div>
        <h3>📊 Comparison Lab</h3>
        <p>Benchmark Korea against five East Asian economies across six shared dimensions.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Comparison Lab", use_container_width=True):
        st.switch_page("pages/1_Comparison_Lab.py")

with nav2:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">02 · PERCEIVE</div>
        <h3>🧭 Perception Survey</h3>
        <p>Measure your view of Korea and compare it with the platform baseline.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Take Perception Survey", use_container_width=True):
        st.switch_page("pages/2_Perception_Survey.py")

with nav3:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">03 · ANALYZE</div>
        <h3>✨ AI Insight</h3>
        <p>Generate a structured perception report with OpenAI or the local fallback provider.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Survey & AI Insight", use_container_width=True):
        st.switch_page("pages/2_Perception_Survey.py")

with nav4:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">04 · UNDERSTAND</div>
        <h3>👥 Community Insights</h3>
        <p>Explore category averages, perception profiles, and recent community voices.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Community Insights", use_container_width=True):
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
