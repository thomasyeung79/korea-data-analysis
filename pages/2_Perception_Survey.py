import plotly.graph_objects as go
import streamlit as st

from api_client import APIClient
from locales.i18n import language_selector, t
from ui_style import apply_product_style

st.set_page_config(
    page_title=t("survey.page_title"),
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

CATEGORY_DISPLAY_KEYS = {
    "Economy": "survey.economy",
    "Technology": "survey.technology",
    "Education": "survey.education",
    "Culture": "survey.culture",
    "Global Influence": "survey.global_influence",
    "Quality of Life": "survey.quality_of_life",
}


def category_label(category):
    return t(CATEGORY_DISPLAY_KEYS.get(category, category))


def score_summary(survey):
    values = [survey[field] for _, field in CATEGORIES]
    average = round(sum(values) / len(values), 2)
    category_scores = {label: survey[field] for label, field in CATEGORIES}
    strongest = max(category_scores, key=category_scores.get)
    weakest = min(category_scores, key=category_scores.get)
    return average, strongest, weakest, category_scores


def radar_chart(user_scores, baseline):
    labels = [label for label, _ in CATEGORIES]
    display_labels = [category_label(label) for label in labels]
    user_values = [user_scores[label] for label in labels]
    baseline_values = [baseline.get(label, FALLBACK_BASELINE[label]) for label in labels]

    labels_closed = display_labels + [display_labels[0]]
    user_closed = user_values + [user_values[0]]
    baseline_closed = baseline_values + [baseline_values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=user_closed,
            theta=labels_closed,
            fill="toself",
            name=t("survey.your_perception"),
            line_color="#d7263d",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=baseline_closed,
            theta=labels_closed,
            fill="toself",
            name=t("survey.korea_baseline"),
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


def ai_scores_from_survey(survey):
    return {
        "economy": survey["economy_score"],
        "technology": survey["technology_score"],
        "education": survey["education_score"],
        "culture": survey["culture_score"],
        "global_influence": survey["global_influence_score"],
        "quality_of_life": survey["quality_of_life_score"],
    }


def render_ai_report(report):
    provider_label = t("survey.provider_openai") if report.get("provider") == "openai" else t("survey.provider_local")

    st.markdown(f'<div class="section-label">{t("survey.ai_label")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('survey.structured_report')}")
    st.caption(provider_label)

    st.markdown(
        f"""
<div class="insight-card">
    <div class="module-tag">{report["profile_label"]}</div>
    <h3>{t("survey.summary")}</h3>
    <p>{report["perception_summary"]}</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(t("survey.associations"))
        for item in report["strongest_associations"]:
            st.success(item)

        st.markdown(t("survey.baseline_comparison"))
        st.info(report["korea_baseline_comparison"])

    with col_b:
        st.markdown(t("survey.gaps"))
        for item in report["concerns_or_gaps"]:
            st.warning(item)

        st.markdown(t("survey.community_comparison"))
        st.info(report["community_average_comparison"])

    st.markdown(t("survey.interpretation"))
    st.write(report["interpretation_profile"])

    st.markdown(t("survey.next_question"))
    st.success(report["suggested_next_question"])


st.markdown(
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>{t("survey.hero_tag")}</div>
        <h1>{t("survey.heading")}</h1>
        <p>
            {t("survey.subtitle")}
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{t("survey.aside_tag")}</div>
            <h3 style="margin-top:1.2rem;">{t("survey.aside_title")}</h3>
            <p style="color:#cbd5e1;">
                {t("survey.aside_desc")}
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">{t("survey.scale_note")}</p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

language_selector("survey_language")

try:
    stats = api.get_survey_stats()
    api_available = True
except Exception as exc:
    stats = None
    api_available = False
    st.warning(t("survey.api_unavailable", error=exc))
    st.info(t("common.api_start"))

baseline = (stats or {}).get("korea_baseline") or FALLBACK_BASELINE

st.markdown(f'<div class="section-label">{t("survey.input_label")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('survey.submit_heading')}")

with st.form("perception_survey_form"):
    display_name = st.text_input(t("survey.display_name"), value="")

    col1, col2 = st.columns(2)
    with col1:
        economy_score = st.slider(t("survey.economy"), 1, 10, 5)
        technology_score = st.slider(t("survey.technology"), 1, 10, 5)
        education_score = st.slider(t("survey.education"), 1, 10, 5)
    with col2:
        culture_score = st.slider(t("survey.culture"), 1, 10, 5)
        global_influence_score = st.slider(t("survey.global_influence"), 1, 10, 5)
        quality_of_life_score = st.slider(t("survey.quality_of_life"), 1, 10, 5)

    comment = st.text_area(
        t("survey.comment"),
        placeholder=t("survey.comment_placeholder"),
    )

    submitted = st.form_submit_button(t("survey.submit"), use_container_width=True)

if submitted:
    if not api_available:
        st.warning(t("survey.cannot_submit"))
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
            st.success(t("survey.submitted"))
            stats = api.get_survey_stats()
            baseline = stats.get("korea_baseline") or FALLBACK_BASELINE
        except Exception as exc:
            st.warning(t("survey.submit_failed", error=exc))

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

    st.markdown(f'<div class="section-label">{t("survey.result_label")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('survey.profile_heading')}")

    r1, r2, r3 = st.columns(3)
    r1.metric(t("survey.score"), score)
    r2.metric(t("survey.strongest"), category_label(strongest))
    r3.metric(t("survey.weakest"), category_label(weakest))

    st.plotly_chart(radar_chart(category_scores, baseline), use_container_width=True)

    if st.button(t("survey.generate_ai"), use_container_width=True):
        if not api_available:
            st.warning(t("survey.cannot_ai"))
        else:
            try:
                report_payload = {
                    "display_name": latest_survey.get("display_name"),
                    "scores": ai_scores_from_survey(latest_survey),
                    "comment": latest_survey.get("comment"),
                    "korea_baseline": baseline,
                    "community_average": (stats or {}).get("average_by_category"),
                    "total_submissions": (stats or {}).get("total_submissions"),
                }
                report = api.generate_perception_report(report_payload)
                st.session_state["latest_ai_report"] = report
            except Exception as exc:
                st.warning(t("survey.ai_failed", error=exc))

    if st.session_state.get("latest_ai_report"):
        render_ai_report(st.session_state["latest_ai_report"])
else:
    st.info(t("survey.empty"))

st.markdown(f'<div class="section-label">{t("survey.stats_label")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('survey.stats_heading')}")

if not api_available:
    st.warning(t("survey.stats_unavailable"))
elif not stats or stats.get("total_submissions", 0) == 0:
    st.info(t("survey.no_submissions"))
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("survey.total"), stats["total_submissions"])
    c2.metric(t("survey.average"), stats["average_score"])
    c3.metric(t("survey.strongest_perceived"), category_label(stats["strongest_category"]))
    c4.metric(t("survey.weakest_perceived"), category_label(stats["weakest_category"]))

    averages = stats.get("average_by_category") or {}
    st.dataframe(
        [
            {
                t("common.category"): category_label(category),
                t("survey.community_average"): averages.get(category),
                t("survey.korea_baseline"): baseline.get(category),
            }
            for category, _ in CATEGORIES
        ],
        use_container_width=True,
    )

if st.button(t("common.back_home"), use_container_width=True):
    st.switch_page("app.py")
