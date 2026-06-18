import html

import plotly.graph_objects as go
import streamlit as st

from api_client import APIClient
from locales.i18n import language_selector, t
from ui_style import apply_product_style

st.set_page_config(
    page_title=t("community.page_title"),
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

CATEGORY_DISPLAY_KEYS = {
    "Economy": "survey.economy",
    "Technology": "survey.technology",
    "Education": "survey.education",
    "Culture": "survey.culture",
    "Global Influence": "survey.global_influence",
    "Quality of Life": "survey.quality_of_life",
    "economy": "survey.economy",
    "technology": "survey.technology",
    "education": "survey.education",
    "culture": "survey.culture",
    "global_influence": "survey.global_influence",
    "quality_of_life": "survey.quality_of_life",
}


def category_label(category):
    return t(CATEGORY_DISPLAY_KEYS.get(category, category))


def category_ranking_chart(category_averages):
    ranked = sorted(
        category_averages.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    fig = go.Figure(
        go.Bar(
            x=[value for _, value in ranked],
            y=[category_label(key) for key, _ in ranked],
            orientation="h",
            text=[f"{value:.2f}" for _, value in ranked],
            textposition="outside",
            marker_color="#123c9c",
        )
    )
    fig.update_layout(
        xaxis=dict(range=[0, 10], title=t("community.average_score")),
        yaxis=dict(autorange="reversed"),
        height=400,
        margin=dict(l=20, r=40, t=20, b=40),
        showlegend=False,
    )
    return fig


def community_radar_chart(category_averages):
    keys = list(CATEGORY_LABELS)
    labels = [category_label(key) for key in keys]
    values = [category_averages[key] for key in keys]
    fig = go.Figure(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=t("community.average_trace"),
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
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>{t("community.hero_tag")}</div>
        <h1>{t("community.heading")}</h1>
        <p>
            {t("community.subtitle")}
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{t("community.aside_tag")}</div>
            <h3 style="margin-top:1.2rem;">{t("community.aside_title")}</h3>
            <p style="color:#cbd5e1;">
                {t("community.aside_desc")}
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">{t("community.no_auth")}</p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

language_selector("community_language")

try:
    summary = api.get_community_summary()
except Exception as exc:
    st.warning(t("community.api_unavailable", error=exc))
    st.info(t("common.api_start"))
    summary = None

if not summary:
    st.stop()

if summary["total_responses"] == 0:
    st.info(t("community.first"))
    if st.button(t("community.take_survey"), use_container_width=True):
        st.switch_page("pages/2_Perception_Survey.py")
    if st.button(t("common.back_home"), use_container_width=True):
        st.switch_page("app.py")
    st.stop()

st.markdown(f'<div class="section-label">{t("community.snapshot_label")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('community.snapshot')}")

m1, m2, m3, m4 = st.columns(4)
m1.metric(t("community.total"), summary["total_responses"])
m2.metric(t("community.average"), summary["average_score"])
m3.metric(t("community.strongest"), category_label(summary["strongest_category"]))
m4.metric(t("community.weakest"), category_label(summary["weakest_category"]))

category_averages = summary["category_averages"]

left, right = st.columns(2)
with left:
    st.markdown(f"## {t('community.ranking')}")
    st.plotly_chart(
        category_ranking_chart(category_averages),
        use_container_width=True,
    )

with right:
    st.markdown(f"## {t('community.radar')}")
    st.plotly_chart(
        community_radar_chart(category_averages),
        use_container_width=True,
    )

st.markdown(f'<div class="section-label">{t("community.profiles_label")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('community.profile_distribution')}")
st.plotly_chart(
    profile_distribution_chart(summary["profile_distribution"]),
    use_container_width=True,
)

st.markdown(f'<div class="section-label">{t("community.voices_label")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('community.voices')}")

comments = summary.get("recent_comments", [])[:20]
if not comments:
    st.info(t("community.no_comments"))
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

if st.button(t("common.back_home"), use_container_width=True):
    st.switch_page("app.py")
