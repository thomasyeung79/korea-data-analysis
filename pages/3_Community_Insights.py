import html

import plotly.graph_objects as go
import streamlit as st

from api_client import APIClient
from ui_style import apply_product_style

st.set_page_config(
    page_title="Community Insights",
    page_icon="👥",
    layout="wide",
)

apply_product_style()
api = APIClient()

CATEGORY_LABELS = {
    "economy": "Economy",
    "technology": "Technology",
    "education": "Education",
    "culture": "Culture",
    "global_influence": "Global Influence",
    "quality_of_life": "Quality of Life",
}


def category_ranking_chart(category_averages):
    ranked = sorted(
        category_averages.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    fig = go.Figure(
        go.Bar(
            x=[value for _, value in ranked],
            y=[CATEGORY_LABELS[key] for key, _ in ranked],
            orientation="h",
            text=[f"{value:.2f}" for _, value in ranked],
            textposition="outside",
            marker_color="#123c9c",
        )
    )
    fig.update_layout(
        xaxis=dict(range=[0, 10], title="Average score"),
        yaxis=dict(autorange="reversed"),
        height=400,
        margin=dict(l=20, r=40, t=20, b=40),
        showlegend=False,
    )
    return fig


def community_radar_chart(category_averages):
    keys = list(CATEGORY_LABELS)
    labels = [CATEGORY_LABELS[key] for key in keys]
    values = [category_averages[key] for key in keys]
    fig = go.Figure(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name="Community average",
            line_color="#d7263d",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        height=450,
        margin=dict(l=30, r=30, t=30, b=30),
        showlegend=False,
    )
    return fig


def profile_distribution_chart(distribution):
    active = [(label, count) for label, count in distribution.items() if count > 0]
    fig = go.Figure(
        go.Pie(
            labels=[label for label, _ in active],
            values=[count for _, count in active],
            hole=0.48,
            textinfo="label+percent",
        )
    )
    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
    )
    return fig


st.markdown(
    """
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>STEP K5 · COMMUNITY ANALYTICS</div>
        <h1>Community Insights</h1>
        <p>
            See how the community perceives Korea across six dimensions, which interpretation
            profiles are emerging, and what respondents say shaped their views.
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>Live survey intelligence</div>
            <h3 style="margin-top:1.2rem;">From individual answers to shared signals</h3>
            <p style="color:#cbd5e1;">
                Every survey response updates this page automatically.
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">No authentication or account data is used.</p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

try:
    summary = api.get_community_summary()
except Exception as exc:
    st.warning(f"Community Insights API unavailable: {exc}")
    st.info("Start the backend: `cd backend && uvicorn app.main:app --reload`")
    summary = None

if not summary:
    st.stop()

if summary["total_responses"] == 0:
    st.info("Be the first participant in the Korea Perception Survey.")
    if st.button("Take Perception Survey", use_container_width=True):
        st.switch_page("pages/2_Perception_Survey.py")
    if st.button("Back to Home", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

st.markdown('<div class="section-label">COMMUNITY SNAPSHOT</div>', unsafe_allow_html=True)
st.markdown("## Community Snapshot")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Responses", summary["total_responses"])
m2.metric("Average Score", summary["average_score"])
m3.metric("Strongest Category", CATEGORY_LABELS[summary["strongest_category"]])
m4.metric("Weakest Category", CATEGORY_LABELS[summary["weakest_category"]])

category_averages = summary["category_averages"]

left, right = st.columns(2)
with left:
    st.markdown("## Category Ranking")
    st.plotly_chart(
        category_ranking_chart(category_averages),
        use_container_width=True,
    )

with right:
    st.markdown("## Community Radar")
    st.plotly_chart(
        community_radar_chart(category_averages),
        use_container_width=True,
    )

st.markdown('<div class="section-label">COMMUNITY PROFILES</div>', unsafe_allow_html=True)
st.markdown("## Profile Distribution")
st.plotly_chart(
    profile_distribution_chart(summary["profile_distribution"]),
    use_container_width=True,
)

st.markdown('<div class="section-label">RECENT VOICES</div>', unsafe_allow_html=True)
st.markdown("## Recent Voices")

comments = summary.get("recent_comments", [])[:20]
if not comments:
    st.info("No comments available yet.")
else:
    for comment in comments:
        st.markdown(
            f"""
<div class="insight-card" style="margin-bottom:0.75rem;">
    <p style="margin:0;font-size:1rem;">“{html.escape(comment)}”</p>
</div>
            """,
            unsafe_allow_html=True,
        )

if st.button("Back to Home", use_container_width=True):
    st.switch_page("app.py")
