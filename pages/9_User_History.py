import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="User History",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}

.card {
    padding: 1.5rem;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    background: white;
    min-height: 160px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

.card h3 {
    margin-top: 0;
}

.card p {
    color: #444;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("📈 User Perception History")

language = st.session_state.get("language", "English")
user_name = st.session_state.get("user_name")

if not user_name:
    st.warning(
        "Please return to Home and enter your username first."
        if language == "English"
        else "请先返回首页输入用户名。"
    )

    if st.button(
        "🏠 Back to Home"
        if language == "English"
        else "🏠 返回首页"
    ):
        st.switch_page("app.py")

    st.stop()

st.info(f"👤 {user_name}")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

try:
    with open("user_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)
except FileNotFoundError:
    results = []

results = [
    r for r in results
    if r.get("username") == user_name
]

if not results:
    st.warning("No user results saved yet.")
else:
    df = pd.DataFrame(results)

    st.subheader("📋 Saved User Results")
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("📊 Average Perception Scores")

    score_columns = [
        "technology",
        "culture",
        "pressure",
        "global_influence",
        "score"
    ]

    avg_scores = df[score_columns].mean()

    st.bar_chart(avg_scores)

    st.divider()

    st.subheader("🧠 Latest AI Insight")

    latest = df.iloc[-1]

    st.info(latest["ai_result"])
