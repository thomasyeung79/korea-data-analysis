import streamlit as st
import csv
import io
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Study Cost Calculator",
    page_icon="📚",
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
        <div class="brand-row"><span class="brand-dot"></span>V2 · MODULE 1</div>
        <h1>Korea Study Cost Calculator</h1>
        <p>
            Estimate your monthly and annual costs for studying in Korea.
            Covers tuition, housing, food, transport, insurance, and miscellaneous expenses.
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>Directional estimates</div>
            <h3 style="margin-top:1.2rem;">All amounts in KRW</h3>
            <p style="color:#cbd5e1;">
                Based on published data from Korean Ministry of Education, Numbeo,
                and university international offices. Actual costs may vary ±20%.
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
st.markdown("## Tell us about your study plan")

col1, col2 = st.columns(2)

with col1:
    city = st.selectbox("City", ["Seoul", "Busan", "Daejeon", "Daegu", "Other"])
    school_type = st.selectbox("School Type", ["Language School", "Undergraduate", "Graduate School"])

with col2:
    housing_type = st.selectbox("Housing Type", ["Dormitory", "Shared Apartment", "Studio Apartment"])
    lifestyle_level = st.selectbox("Lifestyle Level", ["Budget", "Standard", "Premium"],
        help="Budget = frugal student living. Standard = average. Premium = comfortable.")

calculate_clicked = st.button("Calculate Cost", use_container_width=True, type="primary")

st.divider()

# ── Results ──

if calculate_clicked:
    try:
        result = api.calculate_study_cost(
            city=city,
            school_type=school_type,
            housing_type=housing_type,
            lifestyle_level=lifestyle_level,
        )
        st.session_state["last_cost_result"] = result
        st.session_state["last_cost_inputs"] = {
            "city": city,
            "school_type": school_type,
            "housing_type": housing_type,
            "lifestyle_level": lifestyle_level,
        }
    except Exception as e:
        st.error(f"Calculation failed: {e}")
        st.session_state.pop("last_cost_result", None)

if "last_cost_result" in st.session_state:
    result = st.session_state["last_cost_result"]
    inputs = st.session_state.get("last_cost_inputs", {})

    st.markdown('<div class="section-label">YOUR ESTIMATE</div>', unsafe_allow_html=True)
    st.markdown(f"## Cost estimate for {inputs.get('city', 'Seoul')}")

    # ── Summary cards ──
    c1, c2, c3 = st.columns(3)
    monthly_usd = round(result["monthly_cost"] / 1200)
    annual_usd = round(result["annual_cost"] / 1200)
    c1.metric("Monthly (KRW)", f"{result['monthly_cost']:,} ₩")
    c2.metric("Annual (KRW)", f"{result['annual_cost']:,} ₩")
    c3.metric("≈ Monthly (USD)", f"${monthly_usd:,}")

    st.divider()

    # ── Pie chart ──
    st.markdown('<div class="section-label">BREAKDOWN</div>', unsafe_allow_html=True)
    st.markdown("## Where your money goes")

    breakdown = result["breakdown"]
    labels = list(breakdown.keys())
    values = list(breakdown.values())

    colors = ["#123c9c", "#d7263d", "#0f9f6e", "#f59e0b", "#8b5cf6", "#ec4899"]

    fig_pie = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo="label+percent",
            hole=0.45,
        )
    ])
    fig_pie.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # ── Monthly vs Annual bar ──
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        st.caption("**Monthly vs Annual comparison**")
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=["Monthly", "Annual"],
            y=[result["monthly_cost"], result["annual_cost"]],
            marker_color=["#123c9c", "#d7263d"],
            text=[f"{result['monthly_cost']:,} KRW", f"{result['annual_cost']:,} KRW"],
            textposition="outside",
        ))
        fig_comp.update_layout(height=320, showlegend=False, margin=dict(l=20, r=20, t=10, b=20))
        fig_comp.update_yaxes(tickformat=",")
        st.plotly_chart(fig_comp, use_container_width=True)
    with col_ch2:
        st.caption("**Category breakdown amounts**")
        fig_cat = go.Figure()
        cat_names = list(breakdown.keys())
        cat_vals = list(breakdown.values())
        fig_cat = go.Figure(data=[go.Bar(
            x=cat_vals, y=cat_names, orientation="h",
            marker_color=colors[:len(cat_names)],
            text=[f"{v:,} KRW" for v in cat_vals],
            textposition="outside",
        )])
        fig_cat.update_layout(height=320, showlegend=False, margin=dict(l=20, r=20, t=10, b=20))
        fig_cat.update_xaxes(tickformat=",")
        st.plotly_chart(fig_cat, use_container_width=True)

    # ── Detail table ──
    st.subheader("Monthly detail")
    detail_rows = []
    for cat, amount in breakdown.items():
        pct = round(amount / result["monthly_cost"] * 100)
        detail_rows.append({"Category": cat, "Amount (KRW)": f"{amount:,}", "%": f"{pct}%"})
    st.dataframe(detail_rows, use_container_width=True, hide_index=True)

    st.divider()

    # ── AI Explanation ──
    st.markdown('<div class="section-label">AI EXPLANATION</div>', unsafe_allow_html=True)
    st.markdown("## Understanding your estimate")

    with st.container():
        st.markdown(
            f"""
        <div class="card" style="background:#f8fafc; min-height:auto;">
            <p style="white-space:pre-wrap; line-height:1.7;">{result['ai_summary']}</p>
        </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Share / Export ──
    st.markdown('<div class="section-label">EXPORT</div>', unsafe_allow_html=True)
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        summary_text = (
            f"Korea Study Cost Estimate\n"
            f"City: {inputs.get('city', 'Seoul')}\n"
            f"School: {inputs.get('school_type', 'Undergraduate')}\n"
            f"Housing: {inputs.get('housing_type', 'Shared Apartment')}\n"
            f"Lifestyle: {inputs.get('lifestyle_level', 'Standard')}\n"
            f"Monthly: {result['monthly_cost']:,} KRW\n"
            f"Annual: {result['annual_cost']:,} KRW\n"
        )
        st.download_button(
            "📥 Download Summary (TXT)",
            data=summary_text,
            file_name="korea_study_cost_estimate.txt",
            use_container_width=True,
        )
    with col_e2:
        csv_out = io.StringIO()
        csv_w = csv.writer(csv_out)
        csv_w.writerow(["Category", "Amount (KRW)", "Percent"])
        for cat, amount in breakdown.items():
            pct = round(amount / result["monthly_cost"] * 100)
            csv_w.writerow([cat, amount, f"{pct}%"])
        csv_w.writerow(["Total Monthly", result["monthly_cost"], "100%"])
        csv_w.writerow(["Total Annual", result["annual_cost"], ""])
        st.download_button(
            "📥 Download CSV",
            data=csv_out.getvalue(),
            file_name="korea_study_cost.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_e3:
        if st.button("🔄 Recalculate", use_container_width=True):
            st.session_state.pop("last_cost_result", None)
            st.rerun()

else:
    st.info("Fill in your study profile above and click **Calculate Cost** to see your estimate.")

st.divider()
st.caption("Korea Study & Career Decision Agent · Study Cost Calculator v1.0")
