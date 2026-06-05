import streamlit as st
import pandas as pd
from api_client import get_api
from ui_style import apply_product_style, tr

st.set_page_config(
    page_title="User History",
    page_icon="📈",
    layout="wide"
)

apply_product_style()

api = get_api()

st.title(tr("📈 User Perception History", "📈 用户认知历史"))

language = st.session_state.get("language", "English")
user_name = api.user.get("username") if api.is_authenticated else None

if not user_name:
    st.warning(
        "Please return to Home and enter your username first."
        if language == "English"
        else "请先返回首页输入用户名。"
    )
    if st.button("🏠 Back to Home" if language == "English" else "🏠 返回首页"):
        st.switch_page("app.py")
    st.stop()

st.info(f"👤 {user_name}")

if st.button(tr("🏠 Back to Home", "🏠 返回首页")):
    st.switch_page("app.py")

# Load results from API
try:
    results = api.get_perception_results()
except Exception:
    results = []

if not results:
    st.warning(tr("No user results saved yet.", "还没有保存的用户结果。"))
else:
    df = pd.DataFrame(results)

    st.subheader(tr("📋 Saved User Results", "📋 已保存的用户结果"))
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader(tr("📊 Average Perception Scores", "📊 平均认知评分"))

    score_columns = ["technology", "culture", "pressure", "global_influence", "overall_score"]
    available_cols = [c for c in score_columns if c in df.columns]

    if available_cols:
        avg_scores = df[available_cols].mean()
        st.bar_chart(avg_scores)

    st.divider()

    st.subheader(tr("🧠 Latest AI Insight", "🧠 最新 AI 洞察"))

    latest = df.iloc[-1]
    ai_report = latest.get("ai_report")

    if ai_report:
        try:
            import json
            report_data = json.loads(ai_report) if isinstance(ai_report, str) else ai_report
            if isinstance(report_data, dict) and "executive_summary" in report_data:
                st.info(report_data["executive_summary"])
            else:
                st.info(ai_report)
        except Exception:
            st.info(ai_report)
    else:
        st.info("No AI report available for the latest entry.")
