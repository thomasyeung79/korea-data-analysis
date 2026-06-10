import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Comparison Lab",
    page_icon="📊",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()

st.title("📊 East Asia Comparison Lab")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

st.caption(
    "Compare six countries across six dimensions. "
    "All scores are normalised to a 0–10 scale."
)

st.divider()

# ── Load data ──

try:
    scores = api.get_country_scores()
except Exception as e:
    st.error(f"Cannot connect to backend: {e}")
    st.info("Run: `cd backend && uvicorn app.main:app --reload`")
    st.stop()

if not scores:
    st.info("No data available.")
    st.stop()

df = pd.DataFrame(scores)
CATEGORIES = ["Economy", "Technology", "Education", "Culture", "Global Influence", "Quality of Life"]
COUNTRIES = ["Korea", "Japan", "China", "Singapore", "Vietnam", "Thailand"]

# ── Radar Chart ──

st.subheader("🕸️ Radar Comparison")

selected_radar = st.multiselect(
    "Select countries to compare",
    options=COUNTRIES,
    default=["Korea", "Japan", "China"],
)

if selected_radar:
    radar_df = df[df["country"].isin(selected_radar)]

    fig = go.Figure()
    colors = ["#123c9c", "#d7263d", "#0f9f6e", "#f59e0b", "#8b5cf6", "#ec4899"]

    for idx, country in enumerate(selected_radar):
        country_data = radar_df[radar_df["country"] == country]
        r_values = []
        for cat in CATEGORIES:
            match = country_data[country_data["category"] == cat]
            r_values.append(match["score"].iloc[0] if not match.empty else 0)
        # Close the loop
        r_values.append(r_values[0])
        theta = CATEGORIES + [CATEGORIES[0]]

        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=theta,
            name=country,
            fill="toself",
            line_color=colors[idx % len(colors)],
            opacity=0.5,
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickvals=[0, 2, 4, 6, 8, 10],
            )
        ),
        height=500,
        margin=dict(l=80, r=80, t=20, b=80),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Select at least one country to show the radar chart.")

st.divider()

# ── Bar Chart Comparison ──

st.subheader("📊 Category Breakdown")

sel_cat = st.selectbox("Select a category", options=CATEGORIES)

cat_df = df[df["category"] == sel_cat].copy()
if not cat_df.empty:
    cat_df = cat_df.sort_values("score", ascending=True)

    fig_bar = px.bar(
        cat_df,
        x="score",
        y="country",
        orientation="h",
        text="score",
        color="country",
        color_discrete_sequence=colors[: len(cat_df)],
        labels={"score": "Score (0–10)", "country": ""},
        range_x=[0, 10],
    )
    fig_bar.update_layout(
        height=350,
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20),
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info(f"No data for category: {sel_cat}")

st.divider()

# ── Full Data Table ──

st.subheader("📋 Raw Data")

col_f1, col_f2 = st.columns(2)
with col_f1:
    filter_country = st.multiselect("Country", options=COUNTRIES, default=COUNTRIES)
with col_f2:
    filter_cat = st.multiselect("Category", options=CATEGORIES, default=CATEGORIES)

filtered = df[
    df["country"].isin(filter_country) &
    df["category"].isin(filter_cat)
]

st.dataframe(
    filtered[["country", "category", "score", "source"]],
    use_container_width=True,
    hide_index=True,
)
