import streamlit as st
import csv
import io
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="IT Job Market Analyzer",
    page_icon="💻",
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
        <div class="brand-row"><span class="brand-dot"></span>V2 · MODULE 2</div>
        <h1>Korea IT Job Market Analyzer</h1>
        <p>
            Analyse salary ranges, skill requirements, and visa pathways for tech roles in Korea.
            Get a personalised 3-month preparation plan based on your profile.
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>Directional estimates</div>
            <h3 style="margin-top:1.2rem;">Salary data in KRW</h3>
            <p style="color:#cbd5e1;">
                Based on published salary surveys, LinkedIn data, and Korean job platforms.
                Actual offers vary by company size, equity, and negotiation.
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
st.markdown("## Tell us about your background")

col1, col2, col3 = st.columns(3)

with col1:
    role = st.selectbox("Target Role", [
        "Data Analyst",
        "Backend Developer",
        "AI Product Manager",
        "AI Engineer",
    ])

with col2:
    experience = st.selectbox("Experience Level", ["Student", "0-2 years", "3-5 years"])

with col3:
    korean_level = st.selectbox("Korean Language Level", ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"])

analyze_clicked = st.button("Analyze Job Market", use_container_width=True, type="primary")

st.divider()

# ── Results ──

VALID_ROLES = ["Data Analyst", "Backend Developer", "AI Product Manager", "AI Engineer"]

if analyze_clicked:
    if role not in VALID_ROLES:
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
        st.error(f"Analysis failed: {e}")
        st.session_state.pop("last_job_result", None)

if "last_job_result" in st.session_state:
    result = st.session_state["last_job_result"]
    inputs = st.session_state["last_job_inputs"]

    st.markdown('<div class="section-label">YOUR ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown(f"## Market analysis for {inputs['role']}")

    # ── Salary cards ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Salary Min (KRW)", f"{result['salary_min']:,} ₩")
    c2.metric("Salary Max (KRW)", f"{result['salary_max']:,} ₩")
    c3.metric("Competitiveness", f"{result['competitiveness']}/10")
    c4.metric("Currency", result["currency"])

    st.caption(f"**Competitiveness note:** {result['competitiveness_label']}")

    st.divider()

    # ── Salary range chart ──
    st.markdown("### 💰 Salary Range")

    fig_salary = go.Figure()
    fig_salary.add_trace(go.Bar(
        x=["Salary Range"],
        y=[result["salary_max"] - result["salary_min"]],
        base=result["salary_min"],
        marker_color="#0f9f6e",
        name="Salary range",
        text=f"{result['salary_min']:,} - {result['salary_max']:,} KRW",
        textposition="outside",
    ))
    fig_salary.update_layout(
        height=300,
        showlegend=False,
        yaxis_title="KRW / year",
        margin=dict(l=20, r=20, t=10, b=20),
    )
    fig_salary.update_yaxes(tickformat=",")
    st.plotly_chart(fig_salary, use_container_width=True)

    # ── Recommended cities ──
    st.subheader("🏙️ Recommended Cities")
    st.write(", ".join(result["recommended_cities"]))

    st.divider()

    # ── Skills matrix ──
    st.markdown("### 🛠️ Skills Matrix")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("**Must-Have**")
        for skill in result["required_skills"]:
            st.markdown(f"- ✅ {skill}")

    with col_s2:
        st.markdown("**Nice-to-Have**")
        for skill in result["nice_to_have_skills"]:
            st.markdown(f"- ⭐ {skill}")

    st.divider()

    # ── Korean language section ──
    st.markdown("### 🗣️ Korean Language Requirements")
    st.info(result["korean_language_requirement"])

    if result.get("korean_language_gap"):
        with st.expander("📌 How your current level affects your options"):
            st.write(result["korean_language_gap"])

    # ── Visa pathway ──
    with st.expander("🛂 Visa Pathway"):
        st.write(result["visa_pathway"])

    st.divider()

    # ── AI preparation plan ──
    st.markdown('<div class="section-label">PREPARATION PLAN</div>', unsafe_allow_html=True)
    st.markdown("## Your personalised plan")

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
    st.markdown('<div class="section-label">EXPORT</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        summary_text = (
            f"Korea IT Job Market Analysis\n"
            f"Role: {inputs['role']}\n"
            f"Experience: {inputs['experience']}\n"
            f"Korean Level: {inputs['korean_level']}\n"
            f"Salary Range: {result['salary_min']:,} - {result['salary_max']:,} KRW\n"
            f"Competitiveness: {result['competitiveness']}/10\n"
            f"Cities: {', '.join(result['recommended_cities'])}\n"
        )
        st.download_button(
            "📥 Download Analysis (TXT)",
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
            "📥 Download CSV",
            data=csv_out.getvalue(),
            file_name="korea_job_market_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    st.info("Select your profile above and click **Analyze Job Market** to see results.")

st.divider()
st.caption("Korea Study & Career Decision Agent · IT Job Market Analyzer v1.0")
