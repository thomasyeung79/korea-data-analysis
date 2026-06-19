import streamlit as st
import json
import plotly.graph_objects as go
from locales.i18n import display_goal, display_role, language_selector, t

st.set_page_config(
    page_title=t("decision.page_title"),
    page_icon="🧭",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()

TARGET_ROLE_OPTIONS = [
    "Not Applicable",
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
        <div class="brand-row"><span class="brand-dot"></span>{t("decision.brand")}</div>
        <h1>{t("decision.heading")}</h1>
        <p>
            {t("decision.subtitle")}
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{t("decision.aside_tag")}</div>
            <h3 style="margin-top:1.2rem;">{t("decision.aside_title")}</h3>
            <p style="color:#cbd5e1;">
                {t("decision.aside_desc")}
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

language_selector("decision_language")

if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.divider()

# ── Form ──

st.markdown(f'<div class="section-label">{t("common.your_profile")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('decision.form_heading')}")

col1, col2 = st.columns(2)

with col1:
    goal = st.selectbox(t("decision.goal"), ["Study", "Work", "Live"], format_func=display_goal)
    target_city = st.selectbox(t("decision.target_city"), ["Seoul", "Busan", "Daejeon", "Daegu", "Other"])
    school_type = st.selectbox(t("study.school_type"), ["Not Applicable", "Language School", "Undergraduate", "Graduate School"])
    housing_type = st.selectbox(t("study.housing_type"), ["Not Applicable", "Dormitory", "Shared Apartment", "Studio Apartment"])

with col2:
    lifestyle_level = st.selectbox(t("study.lifestyle_level"), ["Budget", "Standard", "Premium"])
    target_role = st.selectbox(t("job.target_role"), TARGET_ROLE_OPTIONS, format_func=display_role)
    experience_level = st.selectbox(t("job.experience"), ["Student", "0-2 years", "3-5 years"])
    korean_level = st.selectbox(t("job.korean_level"), ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"])

monthly_budget = st.number_input(
    t("decision.monthly_budget"),
    min_value=0, max_value=15_000_000, value=1_500_000, step=100_000,
    format="%d",
    help=t("decision.budget_help"),
)

generate_clicked = st.button(t("decision.generate"), use_container_width=True, type="primary")

st.divider()

# ── Results ──

if generate_clicked:
    payload = {
        "goal": goal,
        "target_city": target_city,
        "school_type": school_type,
        "housing_type": housing_type,
        "lifestyle_level": lifestyle_level,
        "target_role": target_role,
        "experience_level": experience_level,
        "korean_level": korean_level,
        "monthly_budget": monthly_budget,
    }
    try:
        result = api.generate_decision_report(payload)
        st.session_state["decision_report"] = result
    except Exception as e:
        st.error(t("decision.failed", error=e))
        st.session_state.pop("decision_report", None)

if "decision_report" in st.session_state:
    r = st.session_state["decision_report"]

    # ── 1. Recommendation Card ──
    st.markdown(f'<div class="section-label">{t("decision.recommendation")}</div>', unsafe_allow_html=True)

    rec_colors = {
        "strongly_recommended": "#0f9f6e",
        "recommended_with_prep": "#f59e0b",
        "risky": "#d7263d",
        "not_recommended": "#64748b",
    }
    color = rec_colors.get(r["recommendation"], "#64748b")

    st.markdown(
        f"""
    <div style="text-align:center; padding:2rem; border:3px solid {color};
                border-radius:12px; margin:1rem 0; background:#f8fafc;">
        <div style="font-size:0.85rem; color:#64748b; text-transform:uppercase; font-weight:700;">
            {t("decision.overall")}
        </div>
        <div style="font-size:2rem; font-weight:800; color:{color}; margin-top:0.5rem;">
            {r['recommendation_label']}
        </div>
        <div style="margin-top:1rem; color:#334155; max-width:600px; margin-left:auto; margin-right:auto;">
            {r['summary']}
        </div>
    </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ── 2. Financial Fit ──
    st.markdown(t("decision.financial_fit"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("decision.est_monthly"), f"{r['monthly_cost_estimate']:,} ₩")
    c2.metric(t("decision.est_annual"), f"{r['annual_cost_estimate']:,} ₩")
    c3.metric(t("decision.budget_gap"), f"{r['budget_gap']:+,} ₩", delta_color="inverse")
    c4.metric(t("decision.financial_risk"), r["financial_risk"])

    fin_colors = {"Low": "#0f9f6e", "Medium": "#f59e0b", "High": "#d7263d"}
    st.markdown(f'<div style="height:6px; background:{fin_colors.get(r["financial_risk"], "#ccc")}; border-radius:3px; margin:0.5rem 0 1rem;"></div>',
                unsafe_allow_html=True)

    # Budget gap chart
    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(
        x=[t("decision.budget"), t("decision.est_cost")],
        y=[r['monthly_cost_estimate'] + max(r['budget_gap'], 0), r['monthly_cost_estimate']],
        marker_color=["#0f9f6e" if r['budget_gap'] >= 0 else "#d7263d", "#123c9c"],
        text=[f"{r['monthly_cost_estimate'] + max(r['budget_gap'], 0):,} KRW", f"{r['monthly_cost_estimate']:,} KRW"],
        textposition="outside",
    ))
    fig_budget.update_layout(height=300, showlegend=False, margin=dict(l=20, r=20, t=10, b=20),
                              title=t("decision.budget_chart"))
    fig_budget.update_yaxes(tickformat=",")
    st.plotly_chart(fig_budget, use_container_width=True)

    st.divider()

    # ── 3. Career Fit ──
    st.markdown(t("decision.career_fit"))

    if target_role != "Not Applicable":
        c1, c2, c3 = st.columns(3)
        c1.metric(t("decision.salary_range"), f"{r['salary_min']:,} - {r['salary_max']:,} ₩")
        c2.metric(t("job.competitiveness"), f"{r['competitiveness']}/10")
        c3.metric(t("decision.career_risk"), r["career_risk"])

        st.markdown(t("decision.required_skills", skills=", ".join(r["required_skills"][:5])))
        if r.get("korean_language_requirement"):
            st.info(f"🗣️ {r['korean_language_requirement']}")
    else:
        st.info(t("decision.career_na"))

    st.divider()

    # ── 4. Risk Factors ──
    st.markdown(t("decision.risk_assessment"))

    risk_data = [
        (t("decision.risk_financial"), r["financial_risk"], t("decision.risk_budget_gap", gap=r["budget_gap"])),
        (t("decision.risk_language"), r["language_risk"], r.get("language_risk_detail", "")),
        (t("decision.risk_career"), r["career_risk"], r.get("career_risk_detail", "")),
        (t("decision.risk_visa"), r["visa_living_risk"], r.get("visa_living_risk_detail", "")),
    ]

    for label, level, detail in risk_data:
        dot = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(level, "⚪")
        st.markdown(f"**{dot} {label}: {level}**")
        st.caption(detail)

    # Risk chart
    risk_labels = [d[0] for d in risk_data]
    risk_values = [{"Low": 3, "Medium": 2, "High": 1}.get(d[1], 0) for d in risk_data]
    risk_colors = [{"Low": "#0f9f6e", "Medium": "#f59e0b", "High": "#d7263d"}.get(d[1], "#ccc") for d in risk_data]
    fig_risk = go.Figure(data=[go.Bar(
        x=risk_values, y=risk_labels, orientation="h",
        marker_color=risk_colors,
        text=[d[1] for d in risk_data],
        textposition="outside",
    )])
    fig_risk.update_layout(height=220, showlegend=False, margin=dict(l=20, r=20, t=10, b=20),
                           title=t("decision.risk_chart"), xaxis=dict(range=[0, 3.5], tickvals=[1, 2, 3]))
    st.plotly_chart(fig_risk, use_container_width=True)

    st.divider()

    # ── 5. Action Plan ──
    st.markdown(t("decision.action_plan"))
    st.markdown(r["action_plan"])

    st.divider()

    # ── Export ──
    st.markdown(t("decision.export"))
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        summary_txt = (
            f"Korea Decision Report\n"
            f"Goal: {goal}\n"
            f"Recommendation: {r['recommendation_label']}\n"
            f"City: {target_city}\n"
            f"Monthly Cost: {r['monthly_cost_estimate']:,} KRW\n"
            f"Monthly Budget: {monthly_budget:,} KRW\n"
            f"Budget Gap: {r['budget_gap']:+,} KRW\n"
            f"Financial Risk: {r['financial_risk']}\n"
            f"Language Risk: {r['language_risk']}\n"
            f"Career Risk: {r['career_risk']}\n"
            f"Visa Risk: {r['visa_living_risk']}\n"
        )
        st.download_button(
            t("decision.download_summary"),
            data=summary_txt,
            file_name="korea_decision_report.txt",
            use_container_width=True,
        )
    with col_e2:
        md_out = (
            f"# Korea Decision Report\n\n"
            f"**Goal:** {goal}  \n"
            f"**Recommendation:** {r['recommendation_label']}  \n"
            f"**Target City:** {target_city}  \n\n"
            f"## Summary\n{r['summary']}\n\n"
            f"## Financial Fit\n"
            f"- Monthly Cost: {r['monthly_cost_estimate']:,} KRW  \n"
            f"- Annual Cost: {r['annual_cost_estimate']:,} KRW  \n"
            f"- Budget Gap: {r['budget_gap']:+,} KRW  \n"
            f"- Financial Risk: {r['financial_risk']}  \n\n"
            f"## Risk Profile\n"
            f"- Language: {r['language_risk']}  \n"
            f"- Career: {r['career_risk']}  \n"
            f"- Visa & Living: {r['visa_living_risk']}  \n\n"
            f"## Action Plan\n{r['action_plan']}\n"
        )
        st.download_button(
            t("decision.download_md"),
            data=md_out,
            file_name="korea_decision_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_e3:
        json_str = json.dumps(r, indent=2, ensure_ascii=False)
        st.download_button(
            t("decision.download_json"),
            data=json_str,
            file_name="korea_decision_report.json",
            use_container_width=True,
        )

elif "decision_report" not in st.session_state:
    st.info(t("decision.empty"))

st.divider()
st.caption(t("decision.footer"))
