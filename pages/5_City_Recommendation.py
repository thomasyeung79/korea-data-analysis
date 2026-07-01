import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import APIClient
from locales.i18n import format_score_100, get_language, language_selector, t, translate_option
from ui_style import apply_product_style

st.set_page_config(page_title="城市推荐" if get_language() == "zh" else "City Recommendation", page_icon="🏙️", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


def default_profile() -> dict:
    return {
        "display_name": "Compass User",
        "study_profile": {
            "nationality": "International",
            "age": 22,
            "current_education_level": "Undergraduate",
            "target_study_level": "Graduate School",
            "target_major": "Computer Science",
            "korean_level": "TOPIK 3",
            "english_level": "Intermediate",
            "annual_budget": 20_000_000,
            "preferred_city": "Seoul",
        },
        "career_profile": {
            "target_role": "Data Analyst",
            "work_experience": "0-2 years",
            "technical_skills": ["SQL", "Python"],
            "korean_level": "TOPIK 3",
            "english_level": "Intermediate",
            "target_industry": "Technology",
            "visa_goal": "D-10",
        },
        "living_profile": {
            "lifestyle": "Standard",
            "housing_preference": "Shared Apartment",
            "monthly_budget": 1_500_000,
            "preferred_city": "Seoul",
            "transport_preference": "Public Transit",
            "community_preference": "International Community",
        },
    }


language_selector("city_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V3</div>
    <h1>{label("City Recommendation", "城市推荐")}</h1>
    <p>{label("Rank Korean cities across study fit, career opportunity, living comfort, cost, language fit, and lifestyle.", "从留学匹配、职业机会、生活舒适度、成本、语言匹配和生活方式维度推荐韩国城市。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Study + Career + Living", "留学 + 职业 + 生活")}</h3>
    <p>{label("Use your saved Profile Center data or run a default Korea Compass profile.", "使用个人画像保存的数据，或用默认个人画像快速体验。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

profile = st.session_state.get("compass_profile") or default_profile()
if "compass_profile" not in st.session_state:
    st.info(label("No saved profile found. Using a sample profile for the demo.", "尚未找到已保存个人画像。当前使用示例画像演示。"))

payload = {
    "study_profile": profile["study_profile"],
    "career_profile": profile["career_profile"],
    "living_profile": profile["living_profile"],
    "language": get_language(),
}

if st.button(label("Generate City Ranking", "生成城市排名"), use_container_width=True, type="primary"):
    try:
        with st.spinner(t("common.analyzing_city")):
            result = api.recommend_cities(payload)
        st.session_state["city_recommendation"] = result
    except Exception as exc:
        st.error(label(f"City recommendation failed: {exc}", f"城市推荐失败：{exc}"))

result = st.session_state.get("city_recommendation")
if not result:
    st.info(t("common.no_data"))
    st.stop()

rankings = result.get("rankings", [])
best = rankings[0] if rankings else {}
best_city = best.get("city", result.get("best_city", ""))

st.markdown(f"## {label('Best City', '最佳城市')}")
st.markdown(
    f"""
<div class="insight-card">
  <h3>{translate_option("city", best_city)}</h3>
  <p>{label("Total score", "总分")}: <strong>{format_score_100(best.get("total_score", 0))}</strong></p>
  <p>{best.get("recommendation_reason", "")}</p>
</div>
""",
    unsafe_allow_html=True,
)

df = pd.DataFrame(rankings)
if not df.empty:
    df["city_label"] = df["city"].apply(lambda value: translate_option("city", value))
    chart = px.bar(
        df.sort_values("total_score"),
        x="total_score",
        y="city_label",
        orientation="h",
        title=label("City Ranking", "城市排名"),
        labels={"total_score": label("Total Score", "总分"), "city_label": label("City", "城市")},
        color="total_score",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(chart, use_container_width=True)

    score_columns = [
        "city_label",
        "total_score",
        "study_score",
        "career_score",
        "living_score",
        "cost_score",
        "language_fit_score",
        "lifestyle_score",
    ]
    renamed = {
        "city_label": label("City", "城市"),
        "total_score": label("Total", "总分"),
        "study_score": label("Study", "留学"),
        "career_score": label("Career", "职业"),
        "living_score": label("Living", "生活"),
        "cost_score": label("Cost", "成本"),
        "language_fit_score": label("Language Fit", "语言匹配"),
        "lifestyle_score": label("Lifestyle", "生活方式"),
    }
    st.markdown(f"## {label('Score Details', '分数明细')}")
    st.dataframe(df[score_columns].rename(columns=renamed), use_container_width=True, hide_index=True)

    st.markdown(f"## {label('Recommendation Reasons', '推荐理由')}")
    for row in rankings:
        st.markdown(f"**{translate_option('city', row['city'])}**: {row['recommendation_reason']}")

st.caption(t("common.footer"))


