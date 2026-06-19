import streamlit as st
import csv
import io
import plotly.express as px
import plotly.graph_objects as go
from locales.i18n import display_role, language_selector, t

st.set_page_config(
    page_title=t("job.page_title"),
    page_icon="💻",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()

ROLE_OPTIONS = [
    "Data Analyst",
    "Backend Developer",
    "AI Product Manager",
    "AI Engineer",
    "Marketing Specialist",
    "Business Analyst",
    "Operations Specialist",
    "Customer Support Specialist",
    "International Sales",
    "Product Manager",
]

st.markdown(
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>{t("job.brand")}</div>
        <h1>{t("job.heading")}</h1>
        <p>
            {t("job.subtitle")}
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{t("common.directional_estimates")}</div>
            <h3 style="margin-top:1.2rem;">{t("job.aside_title")}</h3>
            <p style="color:#cbd5e1;">
                {t("job.aside_desc")}
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

language_selector("job_language")

if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.divider()

# ── Form ──

st.markdown(f'<div class="section-label">{t("common.your_profile")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('job.form_heading')}")

col1, col2, col3 = st.columns(3)

with col1:
    role = st.selectbox(t("job.target_role"), ROLE_OPTIONS, format_func=display_role)

with col2:
    experience = st.selectbox(t("job.experience"), ["Student", "0-2 years", "3-5 years"])

with col3:
    korean_level = st.selectbox(t("job.korean_level"), ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"])

analyze_clicked = st.button(t("job.analyze"), use_container_width=True, type="primary")

st.divider()

# ── Results ──

if analyze_clicked:
    if role not in ROLE_OPTIONS:
        role = "Backend Developer"
    try:
        result = api.analyze_job_market(
            role=role,
            experience_level=experience,
            korean_level=korean_level,
        )
        st.session_state["last_job_result"] = result
        st.session_state["last_job_inputs"] = {
            "role": role,
            "experience": experience,
            "korean_level": korean_level,
        }
    except Exception as e:
        st.error(t("job.failed", error=e))
        st.session_state.pop("last_job_result", None)

if "last_job_result" in st.session_state:
    result = st.session_state["last_job_result"]
    inputs = st.session_state["last_job_inputs"]

    st.markdown(f'<div class="section-label">{t("job.analysis_label")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('job.analysis_heading', role=display_role(inputs['role']))}")

    # ── Salary cards ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("job.salary_min"), f"{result['salary_min']:,} ₩")
    c2.metric(t("job.salary_max"), f"{result['salary_max']:,} ₩")
    c3.metric(t("job.competitiveness"), f"{result['competitiveness']}/10")
    c4.metric(t("job.currency"), result["currency"])

    st.caption(t("job.note", note=result["competitiveness_label"]))

    st.divider()

    # ── Salary range chart ──
    st.markdown(t("job.salary_range"))

    fig_salary = go.Figure()
    fig_salary.add_trace(go.Bar(
        x=["Salary Range"],
        y=[result["salary_max"] - result["salary_min"]],
        base=result["salary_min"],
        marker_color="#0f9f6e",
        name=t("job.salary_range_name"),
        text=f"{result['salary_min']:,} - {result['salary_max']:,} KRW",
        textposition="outside",
    ))
    fig_salary.update_layout(
        height=300,
        showlegend=False,
        yaxis_title=t("job.krw_year"),
        margin=dict(l=20, r=20, t=10, b=20),
    )
    fig_salary.update_yaxes(tickformat=",")
    st.plotly_chart(fig_salary, use_container_width=True)

    # ── Recommended cities ──
    st.subheader(t("job.recommended_cities"))
    st.write(", ".join(result["recommended_cities"]))

    st.divider()

    # ── Skills matrix ──
    st.markdown(t("job.skills_matrix"))

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown(t("job.must_have"))
        for skill in result["required_skills"]:
            st.markdown(f"- ✅ {skill}")

    with col_s2:
        st.markdown(t("job.nice_have"))
        for skill in result["nice_to_have_skills"]:
            st.markdown(f"- ⭐ {skill}")

    st.divider()

    # ── Korean language section ──
    st.markdown(t("job.language_req"))
    st.info(result["korean_language_requirement"])

    if result.get("korean_language_gap"):
        with st.expander(t("job.level_expander")):
            st.write(result["korean_language_gap"])

    # ── Visa pathway ──
    with st.expander(t("job.visa_pathway")):
        st.write(result["visa_pathway"])

    st.divider()

    # ── AI preparation plan ──
    st.markdown(f'<div class="section-label">{t("job.plan_label")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('job.plan_heading')}")

    with st.container():
        st.markdown(
            f"""
        <div class="card" style="background:#f8fafc; min-height:auto;">
            <p style="white-space:pre-wrap; line-height:1.7;">{result['ai_plan']}</p>
        </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Export ──
    st.markdown(f'<div class="section-label">{t("common.export")}</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        summary_text = (
            f"Korea Career & Job Market Analysis\n"
            f"Role: {inputs['role']}\n"
            f"Experience: {inputs['experience']}\n"
            f"Korean Level: {inputs['korean_level']}\n"
            f"Salary Range: {result['salary_min']:,} - {result['salary_max']:,} KRW\n"
            f"Competitiveness: {result['competitiveness']}/10\n"
            f"Cities: {', '.join(result['recommended_cities'])}\n"
        )
        st.download_button(
            t("job.download_analysis"),
            data=summary_text,
            file_name="korea_job_market_analysis.txt",
            use_container_width=True,
        )
    with col_e2:
        csv_out = io.StringIO()
        csv_w = csv.writer(csv_out)
        csv_w.writerow(["Field", "Value"])
        csv_w.writerow(["Role", inputs['role']])
        csv_w.writerow(["Experience", inputs['experience']])
        csv_w.writerow(["Korean Level", inputs['korean_level']])
        csv_w.writerow(["Salary Min", result['salary_min']])
        csv_w.writerow(["Salary Max", result['salary_max']])
        csv_w.writerow(["Competitiveness", f"{result['competitiveness']}/10"])
        csv_w.writerow(["Cities", ", ".join(result['recommended_cities'])])
        csv_w.writerow(["Must-Have Skills", ", ".join(result['required_skills'])])
        csv_w.writerow(["Nice-to-Have Skills", ", ".join(result['nice_to_have_skills'])])
        st.download_button(
            t("common.download_csv"),
            data=csv_out.getvalue(),
            file_name="korea_job_market_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    st.info(t("job.empty"))

st.divider()
st.caption(t("job.footer"))
