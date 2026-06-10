import streamlit as st

st.set_page_config(
    page_title="East Asia Perception Lab",
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
        <div class="brand-row"><span class="brand-dot"></span>EAST ASIA PERCEPTION LAB</div>
        <h1>Measure. Compare. Understand.</h1>
        <p>
            A quantitative benchmarking platform that scores six East Asian economies
            across Economy, Technology, Education, Culture, Global Influence, and Quality of Life.
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>v0.2 · Comparison Engine</div>
            <h3 style="margin-top:1.2rem;">6 countries · 6 dimensions</h3>
            <p style="color:#cbd5e1;">
                All scores normalised to a 0–10 scale for fair comparison.
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">
                Korea · Japan · China · Singapore · Vietnam · Thailand
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
    all_countries = ["Korea", "Japan", "China", "Singapore", "Vietnam", "Thailand"]

st.divider()

# ── Country Cards ──

st.markdown(f'<div class="section-label">COUNTRIES</div>', unsafe_allow_html=True)
st.markdown("## Six economies, one dashboard")

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

st.markdown(f'<div class="section-label">TOOLS</div>', unsafe_allow_html=True)
st.markdown("## Explore the data")

nav1, nav2, nav3 = st.columns(3)

with nav1:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">COMPARE · DAY 2</div>
        <h3>📊 Comparison Lab</h3>
        <p>Radar chart comparison, category explorer, and raw data table.</p>
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
        <div class="module-tag">SURVEY · DAY 3</div>
        <h3>🧭 Perception Survey</h3>
        <p>Collect user perception, compare it with Korea baseline, and show community stats.</p>
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
        <div class="module-tag">API · DAY 2</div>
        <h3>🔌 API Playground</h3>
        <p>FastAPI auto-docs — test every endpoint live.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button("Open API Docs →", "http://localhost:8000/docs", use_container_width=True)
