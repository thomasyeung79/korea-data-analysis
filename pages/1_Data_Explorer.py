import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Explorer",
    page_icon="📊",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()

st.title("📊 Country Score Explorer")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

st.caption("Browse, filter, and visualise country scores across categories and years.")

st.divider()

# ── Load data ──

try:
    scores = api.get_country_scores()
except Exception as e:
    st.error(f"Cannot connect to backend: {e}")
    st.info("Run: `cd backend && uvicorn app.main:app --reload`")
    st.stop()

if not scores:
    st.info("No data yet. Add scores via the form below.")
    scores = []

df = pd.DataFrame(scores)

# ── Filters ──

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    all_countries = sorted(df["country"].unique()) if not df.empty else []
    sel_country = st.multiselect("Country", options=all_countries, default=all_countries)

with col_f2:
    all_categories = sorted(df["category"].unique()) if not df.empty else []
    sel_cat = st.multiselect("Category", options=all_categories, default=all_categories)

with col_f3:
    all_years = sorted(df["year"].unique(), reverse=True) if not df.empty else []
    sel_year = st.multiselect("Year", options=all_years, default=all_years)

# ── Filtered table ──

filtered = df[
    df["country"].isin(sel_country) &
    df["category"].isin(sel_cat) &
    df["year"].isin(sel_year)
] if not df.empty else df

st.subheader("📋 Data Table")
st.dataframe(
    filtered[["country", "year", "category", "score", "source"]],
    use_container_width=True,
    hide_index=True,
)

# ── Chart ──

st.subheader("📈 Score Comparison")

if not filtered.empty:
    chart_df = filtered.pivot_table(
        index=["country", "year"],
        columns="category",
        values="score",
        aggfunc="first",
    ).reset_index()

    chart_cols = [c for c in chart_df.columns if c not in ("country", "year")]
    if chart_cols:
        tab1, tab2 = st.tabs(["Bar chart", "Line chart"])
        with tab1:
            st.bar_chart(chart_df, x="country", y=chart_cols, stack=False)
        with tab2:
            st.line_chart(chart_df, x="year", y=chart_cols)
else:
    st.info("No data matches the current filters.")

st.divider()

# ── Add / update score form ──

st.subheader("✏️ Add or Update a Score")

with st.form("score_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        form_country = st.text_input("Country", "South Korea")
    with col2:
        form_year = st.number_input("Year", min_value=2000, max_value=2030, value=2024)
    with col3:
        form_category = st.text_input("Category", "Digital Adoption")

    col4, col5 = st.columns(2)
    with col4:
        form_score = st.number_input("Score (0–10 or actual value)", value=8.0, step=0.5)
    with col5:
        form_source = st.text_input("Source (optional)", "KAS estimate")

    submitted = st.form_submit_button("Save Score", use_container_width=True)

    if submitted:
        try:
            result = api.create_country_score(form_country, form_year, form_category, form_score, form_source)
            st.success(f"Saved: {result['country']} · {result['category']} ({result['year']}) = {result['score']}")
            st.rerun()
        except Exception as e:
            err = str(e)
            if "already exists" in err:
                st.warning("Score exists already. Use edit or delete-first then re-add.")
            else:
                st.error(f"Error: {e}")
