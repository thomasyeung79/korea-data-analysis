import streamlit as st

# Page must be first command
st.set_page_config(
    page_title="Korea Analysis System",
    page_icon="🇰🇷",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()

st.markdown(
    """
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>KOREA ANALYSIS SYSTEM</div>
        <h1>Measure. Compare. Understand.</h1>
        <p>
            A bilingual data + AI platform that measures South Korea's global influence
            across economy, innovation, culture, and more — benchmarked against regional peers.
        </p>
        <div class="hero-kpi">
            <div class="kpi-card"><strong>3</strong><span>Countries</span></div>
            <div class="kpi-card"><strong>4+</strong><span>Categories</span></div>
            <div class="kpi-card"><strong>API</strong><span>Data-driven</span></div>
        </div>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>v0.1 · Day 1</div>
            <h3 style="margin-top:1.2rem;">Minimum vertical slice</h3>
            <p style="color:#cbd5e1;">
                Backend · Database · API · Frontend — wired end-to-end.
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">
                Built with FastAPI + SQLite + Streamlit.
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

# ── Quick stats from API ──

try:
    scores = api.get_country_scores()
    countries = set(s["country"] for s in scores)
    categories = set(s["category"] for s in scores)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total data points", len(scores))
    col2.metric("Countries", len(countries))
    col3.metric("Categories", len(categories))
    col4.metric("API status", "✅ Online")
except Exception as e:
    st.warning(f"Backend not reachable: {e}")
    st.info("Start the backend: `cd backend && uvicorn app.main:app --reload`")

# ── Navigation ──

st.markdown(f'<div class="section-label">NAVIGATION</div>', unsafe_allow_html=True)
st.markdown("## Explore the data")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">DATA · DAY 1</div>
        <h3>📊 Data Explorer</h3>
        <p>Browse, filter, and visualise country scores across categories and years.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Data Explorer", use_container_width=True):
        st.switch_page("pages/1_Data_Explorer.py")

with col2:
    st.markdown(
        """
    <div class="module-card">
        <div class="module-tag">API · DAY 1</div>
        <h3>🔌 API Playground</h3>
        <p>FastAPI auto-docs available at <code>/docs</code> — test endpoints directly.</p>
    </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<a href="http://localhost:8000/docs" target="_blank">'
        f'<button style="width:100%;padding:0.5rem;border-radius:8px;border:1px solid #cbd5e1;background:white;font-weight:700;cursor:pointer;">Open API Docs →</button></a>',
        unsafe_allow_html=True,
    )
