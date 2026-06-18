import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Decision Report",
    page_icon="🧭",
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
        <div class="brand-row"><span class="brand-dot"></span>V2 · MODULE 3</div>
        <h1>AI Decision Report</h1>
        <p>
            Should you study, work, or live in Korea? Tell us about yourself and get a
            personalised report combining cost analysis, career insights, risk assessment,
            and a 3-month action plan.
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>Rule-based engine</div>
            <h3 style="margin-top:1.2rem;">Combines 4 risk dimensions</h3>
            <p style="color:#cbd5e1;">
                Financial · Language · Career · Visa & Living
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

st.divider()

# ── Form ──

st.markdown('<div class="section-label">YOUR PROFILE</div>', unsafe_allow_html=True)
st.markdown("## Tell us about your Korea plan")

col1, col2 = st.columns(2)

with col1:
    goal = st.selectbox("Goal", ["Study", "Work", "Live"])
    target_city = st.selectbox("Target City", ["Seoul", "Busan", "Daejeon", "Daegu", "Other"])
    school_type = st.selectbox("School Type", ["Not Applicable", "Language School", "Undergraduate", "Graduate School"])
    housing_type = st.selectbox("Housing Type", ["Not Applicable", "Dormitory", "Shared Apartment", "Studio Apartment"])

with col2:
    lifestyle_level = st.selectbox("Lifestyle Level", ["Budget", "Standard", "Premium"])
    target_role = st.selectbox("Target Role", ["Not Applicable", "Data Analyst", "Backend Developer", "AI Product Manager", "AI Engineer"])
    experience_level = st.selectbox("Experience Level", ["Student", "0-2 years", "3-5 years"])
    korean_level = st.selectbox("Korean Language Level", ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"])

monthly_budget = st.number_input(
    "Monthly Budget (KRW)",
    min_value=0, max_value=15_000_000, value=1_500_000, step=100_000,
    format="%d",
    help="Your estimated monthly budget in Korean Won (tuition + living expenses).",
)

generate_clicked = st.button("Generate Decision Report", use_container_width=True, type="primary")

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
        st.error(f"Failed to generate report: {e}")
        st.session_state.pop("decision_report", None)

if "decision_report" in st.session_state:
    r = st.session_state["decision_report"]

    # ── 1. Recommendation Card ──
    st.markdown('<div class="section-label">RECOMMENDATION</div>', unsafe_allow_html=True)

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
            OVERALL RECOMMENDATION
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
    st.markdown("## 💰 Financial Fit")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Est. Monthly Cost", f"{r['monthly_cost_estimate']:,} ₩")
    c2.metric("Est. Annual Cost", f"{r['annual_cost_estimate']:,} ₩")
    c3.metric("Budget Gap", f"{r['budget_gap']:+,} ₩", delta_color="inverse")
    c4.metric("Financial Risk", r["financial_risk"])

    fin_colors = {"Low": "#0f9f6e", "Medium": "#f59e0b", "High": "#d7263d"}
    st.markdown(f'<div style="height:6px; background:{fin_colors.get(r["financial_risk"], "#ccc")}; border-radius:3px; margin:0.5rem 0 1rem;"></div>',
                unsafe_allow_html=True)

    # Budget gap chart
    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(
        x=["Budget", "Est. Cost"],
        y=[r['monthly_cost_estimate'] + max(r['budget_gap'], 0), r['monthly_cost_estimate']],
        marker_color=["#0f9f6e" if r['budget_gap'] >= 0 else "#d7263d", "#123c9c"],
        text=[f"{r['monthly_cost_estimate'] + max(r['budget_gap'], 0):,} KRW", f"{r['monthly_cost_estimate']:,} KRW"],
        textposition="outside",
    ))
    fig_budget.update_layout(height=300, showlegend=False, margin=dict(l=20, r=20, t=10, b=20),
                              title="Monthly Budget vs Estimated Cost")
    fig_budget.update_yaxes(tickformat=",")
    st.plotly_chart(fig_budget, use_container_width=True)

    st.divider()

    # ── 3. Career Fit ──
    st.markdown("## 💻 Career Fit")

    if target_role != "Not Applicable":
        c1, c2, c3 = st.columns(3)
        c1.metric("Salary Range", f"{r['salary_min']:,} - {r['salary_max']:,} ₩")
        c2.metric("Competitiveness", f"{r['competitiveness']}/10")
        c3.metric("Career Risk", r["career_risk"])

        st.markdown(f"**Required Skills:** {', '.join(r['required_skills'][:5])}")
        if r.get("korean_language_requirement"):
            st.info(f"🗣️ {r['korean_language_requirement']}")
    else:
        st.info("Career assessment not applicable to your current goal.")

    st.divider()

    # ── 4. Risk Factors ──
    st.markdown("## ⚠️ Risk Assessment")

    risk_data = [
        ("Financial", r["financial_risk"], f"Budget gap: {r['budget_gap']:+,} KRW"),
        ("Language", r["language_risk"], r.get("language_risk_detail", "")),
        ("Career", r["career_risk"], r.get("career_risk_detail", "")),
        ("Visa & Living", r["visa_living_risk"], r.get("visa_living_risk_detail", "")),
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
                           title="Risk Profile (3=Low, 1=High)", xaxis=dict(range=[0, 3.5], tickvals=[1, 2, 3]))
    st.plotly_chart(fig_risk, use_container_width=True)

    st.divider()

    # ── 5. Action Plan ──
    st.markdown("## 📋 3-Month Action Plan")
    st.markdown(r["action_plan"])

    st.divider()

    # ── Export ──
    st.markdown("## 📥 Export")
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
            "📥 Download Summary (TXT)",
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
            "📥 Download Markdown",
            data=md_out,
            file_name="korea_decision_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_e3:
        json_str = json.dumps(r, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Download Full Report (JSON)",
            data=json_str,
            file_name="korea_decision_report.json",
            use_container_width=True,
        )

elif "decision_report" not in st.session_state:
    st.info("Fill in your profile above and click **Generate Decision Report** to see your personalised report.")

st.divider()
st.caption("Korea Study & Career Decision Agent · AI Decision Report v1.0")
