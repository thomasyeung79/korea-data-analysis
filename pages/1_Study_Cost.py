import streamlit as st
import csv
import io
import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from locales.i18n import get_language, language_selector, t, translate_option

st.set_page_config(
    page_title=t("study.page_title"),
    page_icon="📚",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()

st.markdown(
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>{t("study.brand")}</div>
        <h1>{t("study.heading")}</h1>
        <p>
            {t("study.subtitle")}
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{t("common.directional_estimates")}</div>
            <h3 style="margin-top:1.2rem;">{t("study.aside_title")}</h3>
            <p style="color:#cbd5e1;">
                {t("study.aside_desc")}
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

language_selector("study_language")

if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.divider()

# ── Form ──

st.markdown(f'<div class="section-label">{t("common.your_profile")}</div>', unsafe_allow_html=True)
st.markdown(f"## {t('study.form_heading')}")

col1, col2 = st.columns(2)

with col1:
    city = st.selectbox(t("study.city"), ["Seoul", "Busan", "Daejeon", "Daegu", "Other"],
                        format_func=lambda value: translate_option("city", value))
    school_type = st.selectbox(t("study.school_type"), ["Language School", "Undergraduate", "Graduate School"],
                               format_func=lambda value: translate_option("school_type", value))

with col2:
    housing_type = st.selectbox(t("study.housing_type"), ["Dormitory", "Shared Apartment", "Studio Apartment"],
                                format_func=lambda value: translate_option("housing_type", value))
    lifestyle_level = st.selectbox(t("study.lifestyle_level"), ["Budget", "Standard", "Premium"],
        format_func=lambda value: translate_option("lifestyle", value), help=t("study.lifestyle_help"))

calculate_clicked = st.button(t("study.calculate"), use_container_width=True, type="primary")

st.divider()

# ── Results ──

if calculate_clicked:
    try:
        result = api.calculate_study_cost(
            city=city,
            school_type=school_type,
            housing_type=housing_type,
            lifestyle_level=lifestyle_level,
            language=get_language(),
        )
        st.session_state["last_cost_result"] = result
        st.session_state["last_cost_inputs"] = {
            "city": city,
            "school_type": school_type,
            "housing_type": housing_type,
            "lifestyle_level": lifestyle_level,
        }
    except Exception as e:
        st.error(t("study.calculation_failed", error=e))
        st.session_state.pop("last_cost_result", None)

if "last_cost_result" in st.session_state:
    result = st.session_state["last_cost_result"]
    inputs = st.session_state.get("last_cost_inputs", {})

    st.markdown(f'<div class="section-label">{t("study.estimate_label")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('study.estimate_heading', city=translate_option('city', inputs.get('city', 'Seoul')))}")

    # ── Summary cards ──
    c1, c2, c3 = st.columns(3)
    monthly_usd = round(result["monthly_cost"] / 1200)
    annual_usd = round(result["annual_cost"] / 1200)
    c1.metric(t("study.monthly_krw"), f"{result['monthly_cost']:,} ₩")
    c2.metric(t("study.annual_krw"), f"{result['annual_cost']:,} ₩")
    c3.metric(t("study.monthly_usd"), f"${monthly_usd:,}")

    st.divider()

    # ── Pie chart ──
    st.markdown(f'<div class="section-label">{t("study.breakdown")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('study.money_heading')}")

    breakdown = result["breakdown"]
    labels = [translate_option("cost_category", key) for key in breakdown]
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
        st.caption(t("study.monthly_annual"))
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=[translate_option("period", "Monthly"), translate_option("period", "Annual")],
            y=[result["monthly_cost"], result["annual_cost"]],
            marker_color=["#123c9c", "#d7263d"],
            text=[f"{result['monthly_cost']:,} KRW", f"{result['annual_cost']:,} KRW"],
            textposition="outside",
        ))
        fig_comp.update_layout(height=320, showlegend=False, margin=dict(l=20, r=20, t=10, b=20))
        fig_comp.update_yaxes(tickformat=",")
        st.plotly_chart(fig_comp, use_container_width=True)
    with col_ch2:
        st.caption(t("study.category_amounts"))
        fig_cat = go.Figure()
        cat_names = [translate_option("cost_category", key) for key in breakdown]
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
    st.subheader(t("study.monthly_detail"))
    detail_rows = []
    for cat, amount in breakdown.items():
        pct = round(amount / result["monthly_cost"] * 100)
        detail_rows.append({t("common.category"): translate_option("cost_category", cat), t("common.amount_krw"): f"{amount:,}", "%": f"{pct}%"})
    st.dataframe(detail_rows, use_container_width=True, hide_index=True)

    st.divider()

    # ── AI Explanation ──
    st.markdown(f'<div class="section-label">{t("study.ai_explanation")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('study.understanding')}")

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
    st.markdown(f'<div class="section-label">{t("common.export")}</div>', unsafe_allow_html=True)
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
            t("study.download_summary"),
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
            t("common.download_csv"),
            data=csv_out.getvalue(),
            file_name="korea_study_cost.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_e3:
        if st.button(t("study.recalculate"), use_container_width=True):
            st.session_state.pop("last_cost_result", None)
            st.rerun()

else:
    st.info(t("study.empty"))

st.divider()
st.caption(t("study.footer"))
