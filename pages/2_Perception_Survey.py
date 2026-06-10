import plotly.graph_objects as go
import streamlit as st

from api_client import APIClient
from ui_style import apply_product_style

st.set_page_config(
    page_title="Korea Perception Survey",
    page_icon="🧭",
    layout="wide",
)

apply_product_style()

api = APIClient()

CATEGORIES = [
    ("Economy", "economy_score"),
    ("Technology", "technology_score"),
    ("Education", "education_score"),
    ("Culture", "culture_score"),
    ("Global Influence", "global_influence_score"),
    ("Quality of Life", "quality_of_life_score"),
]

FALLBACK_BASELINE = {
    "Economy": 8,
    "Technology": 9,
    "Education": 8,
    "Culture": 9,
    "Global Influence": 8,
    "Quality of Life": 7,
}


def score_summary(survey):
    values = [survey[field] for _, field in CATEGORIES]
    average = round(sum(values) / len(values), 2)
    category_scores = {label: survey[field] for label, field in CATEGORIES}
    strongest = max(category_scores, key=category_scores.get)
    weakest = min(category_scores, key=category_scores.get)
    return average, strongest, weakest, category_scores


def radar_chart(user_scores, baseline):
    labels = [label for label, _ in CATEGORIES]
    user_values = [user_scores[label] for label in labels]
    baseline_values = [baseline.get(label, FALLBACK_BASELINE[label]) for label in labels]

    labels_closed = labels + [labels[0]]
    user_closed = user_values + [user_values[0]]
    baseline_closed = baseline_values + [baseline_values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=user_closed,
            theta=labels_closed,
            fill="toself",
            name="Your perception",
            line_color="#d7263d",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=baseline_closed,
            theta=labels_closed,
            fill="toself",
            name="Korea baseline",
            line_color="#123c9c",
            opacity=0.72,
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        margin=dict(l=24, r=24, t=36, b=24),
        height=470,
        showlegend=True,
    )
    return fig


st.markdown(
    """
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>DAY 3 · PERCEPTION ENGINE</div>
        <h1>Korea Perception Survey</h1>
        <p>
            Capture how people perceive Korea across six dimensions, compare each response
            with the platform baseline, and turn community perception into a live product signal.
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>Interactive product layer</div>
            <h3 style="margin-top:1.2rem;">From benchmark data to user perception</h3>
            <p style="color:#cbd5e1;">
                Repeated submissions are allowed. No login, no authentication, no paid APIs.
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">Scores use a 1–10 scale. Default slider values are valid.</p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

try:
    stats = api.get_survey_stats()
    api_available = True
except Exception as exc:
    stats = None
    api_available = False
    st.warning(f"Perception Survey API unavailable: {exc}")
    st.info("Start the backend: `cd backend && uvicorn app.main:app --reload`")

baseline = (stats or {}).get("korea_baseline") or FALLBACK_BASELINE

st.markdown('<div class="section-label">SURVEY INPUT</div>', unsafe_allow_html=True)
st.markdown("## Submit a perception response")

with st.form("perception_survey_form"):
    display_name = st.text_input("Display name / nickname", value="")

    col1, col2 = st.columns(2)
    with col1:
        economy_score = st.slider("Economy", 1, 10, 5)
        technology_score = st.slider("Technology", 1, 10, 5)
        education_score = st.slider("Education", 1, 10, 5)
    with col2:
        culture_score = st.slider("Culture", 1, 10, 5)
        global_influence_score = st.slider("Global Influence", 1, 10, 5)
        quality_of_life_score = st.slider("Quality of Life", 1, 10, 5)

    comment = st.text_area(
        "What shaped your perception of Korea?",
        placeholder="Optional: media, travel, school, friends, K-pop, work, news...",
    )

    submitted = st.form_submit_button("Submit perception survey", use_container_width=True)

if submitted:
    if not api_available:
        st.warning("Cannot submit yet because the backend API is unavailable.")
    else:
        try:
            result = api.submit_survey(
                display_name=display_name,
                economy_score=economy_score,
                technology_score=technology_score,
                education_score=education_score,
                culture_score=culture_score,
                global_influence_score=global_influence_score,
                quality_of_life_score=quality_of_life_score,
                comment=comment,
            )
            st.session_state["latest_survey"] = result
            st.success("Survey submitted.")
            stats = api.get_survey_stats()
            baseline = stats.get("korea_baseline") or FALLBACK_BASELINE
        except Exception as exc:
            st.warning(f"Survey submission failed: {exc}")

latest_survey = st.session_state.get("latest_survey")
if not latest_survey and api_available and stats and stats.get("total_submissions", 0) > 0:
    try:
        latest = api.get_surveys(limit=1)
        if latest:
            latest_survey = latest[0]
            st.session_state["latest_survey"] = latest_survey
    except Exception:
        latest_survey = None

if latest_survey:
    score, strongest, weakest, category_scores = score_summary(latest_survey)

    st.markdown('<div class="section-label">YOUR RESULT</div>', unsafe_allow_html=True)
    st.markdown("## Your Korea perception profile")

    r1, r2, r3 = st.columns(3)
    r1.metric("Your Korea Perception Score", score)
    r2.metric("Strongest category", strongest)
    r3.metric("Weakest category", weakest)

    st.plotly_chart(radar_chart(category_scores, baseline), use_container_width=True)
else:
    st.info("Submit a survey to see your result card and radar comparison.")

st.markdown('<div class="section-label">COMMUNITY STATS</div>', unsafe_allow_html=True)
st.markdown("## Community perception snapshot")

if not api_available:
    st.warning("Community stats are unavailable until the backend is running.")
elif not stats or stats.get("total_submissions", 0) == 0:
    st.info("No community submissions yet. Be the first to create the perception baseline.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total submissions", stats["total_submissions"])
    c2.metric("Average perception score", stats["average_score"])
    c3.metric("Strongest perceived category", stats["strongest_category"])
    c4.metric("Weakest perceived category", stats["weakest_category"])

    averages = stats.get("average_by_category") or {}
    st.dataframe(
        [
            {
                "Category": category,
                "Community average": averages.get(category),
                "Korea baseline": baseline.get(category),
            }
            for category, _ in CATEGORIES
        ],
        use_container_width=True,
    )

if st.button("Back to Home", use_container_width=True):
    st.switch_page("app.py")
