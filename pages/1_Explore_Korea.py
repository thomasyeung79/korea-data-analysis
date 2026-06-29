import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import APIClient
from locales.i18n import get_language, language_selector, t
from ui_style import apply_product_style

st.set_page_config(page_title="Explore Korea", page_icon="🌏", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


def card(title: str, body: str, footer: str = "") -> None:
    st.markdown(
        f"""
<div class="insight-card" style="min-height:132px;">
  <h3 style="margin-top:0;">{title}</h3>
  <p>{body}</p>
  <p style="color:#64748b;font-size:0.9rem;margin-bottom:0;">{footer}</p>
</div>
""",
        unsafe_allow_html=True,
    )


language_selector("explore_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V4</div>
    <h1>{label("Explore Korea", "探索韩国")}</h1>
    <p>{label("A practical country guide for study, work, and life planning in South Korea.", "面向韩国留学、求职和生活规划的实用国家信息指南。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Explore before you plan", "先了解，再规划")}</h3>
    <p>{label("Browse country basics, cities, culture, history, costs, and quick facts before using the planning tools.", "在使用规划工具前，先浏览国家概览、城市、文化、历史、成本和实用信息。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

try:
    language = get_language()
    overview = api.get_explore_overview(language)
    cities = api.get_explore_cities(language)
    culture = api.get_explore_culture(language)
    history = api.get_explore_history(language)
    living_cost = api.get_explore_living_cost()
    quick_facts = api.get_explore_quick_facts(language)
except Exception as exc:
    st.error(label(f"Explore Korea data is unavailable: {exc}", f"探索韩国数据暂不可用：{exc}"))
    st.stop()

tab_overview, tab_cities, tab_culture, tab_history, tab_cost, tab_facts = st.tabs(
    [
        label("Overview", "概览"),
        label("Cities", "城市"),
        label("Culture", "文化"),
        label("History", "历史"),
        label("Cost of Living", "生活成本"),
        label("Quick Facts", "实用信息"),
    ]
)

with tab_overview:
    st.markdown(f"## {label('Country Introduction', '国家介绍')}")
    st.write(overview["country_introduction"])
    overview_cards = [
        (label("Population", "人口"), overview["population"]),
        (label("Area", "面积"), overview["area"]),
        (label("Capital", "首都"), overview["capital"]),
        (label("Currency", "货币"), overview["currency"]),
        (label("Time Zone", "时区"), overview["time_zone"]),
        (label("Language", "语言"), overview["language"]),
        (label("Climate", "气候"), overview["climate"]),
    ]
    for row_start in range(0, len(overview_cards), 3):
        cols = st.columns(3)
        for col, (title, value) in zip(cols, overview_cards[row_start:row_start + 3]):
            with col:
                card(title, value)

with tab_cities:
    st.markdown(f"## {label('Korean Cities', '韩国城市')}")
    for row_start in range(0, len(cities), 2):
        cols = st.columns(2)
        for col, city in zip(cols, cities[row_start:row_start + 2]):
            with col:
                card(
                    city["name"],
                    city["short_description"],
                    f"{label('Population', '人口')}: {city['population']} · "
                    f"{label('Living Cost', '生活成本')}: {city['living_cost']}",
                )
                st.caption(
                    f"{label('Study', '留学')}: {city['study_score']} · "
                    f"{label('Career', '职业')}: {city['career_score']} · "
                    f"{label('Lifestyle', '生活方式')}: {city['lifestyle_score']}"
                )
                st.write(f"**{label('Best For', '适合')}**: {', '.join(city['best_for'])}")

with tab_culture:
    st.markdown(f"## {label('Culture Guide', '文化指南')}")
    for section in culture:
        with st.expander(section["title"], expanded=False):
            st.write(section["summary"])
            for tip in section["tips"]:
                st.markdown(f"- {tip}")

with tab_history:
    st.markdown(f"## {label('Korea Timeline', '韩国历史时间线')}")
    for event in history:
        st.markdown(
            f"""
<div class="insight-card">
  <div style="color:#123c9c;font-weight:800;">{event['timeframe']}</div>
  <h3 style="margin-top:0.25rem;">{event['period']}</h3>
  <p>{event['summary']}</p>
</div>
""",
            unsafe_allow_html=True,
        )

with tab_cost:
    st.markdown(f"## {label('Cost of Living', '生活成本')}")
    cost_df = pd.DataFrame(living_cost)
    selected_city = st.selectbox(label("City", "城市"), cost_df["city"].tolist())
    city_cost = cost_df[cost_df["city"] == selected_city].iloc[0]
    chart_df = pd.DataFrame(
        {
            "category": [
                label("Rent", "租金"),
                label("Food", "饮食"),
                label("Transportation", "交通"),
                label("Mobile", "手机"),
                label("Utilities", "水电燃气"),
                label("Entertainment", "娱乐"),
            ],
            "amount": [
                city_cost["rent"],
                city_cost["food"],
                city_cost["transportation"],
                city_cost["mobile"],
                city_cost["utilities"],
                city_cost["entertainment"],
            ],
        }
    )
    fig = px.bar(
        chart_df,
        x="category",
        y="amount",
        title=label(f"Monthly cost estimate in {selected_city}", f"{selected_city} 月度生活成本估算"),
        labels={"category": label("Category", "类别"), "amount": label("Amount (KRW)", "金额（韩元）")},
        color="amount",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(chart_df, use_container_width=True, hide_index=True)

with tab_facts:
    st.markdown(f"## {label('Quick Facts', '实用信息')}")
    for row_start in range(0, len(quick_facts), 3):
        cols = st.columns(3)
        for col, fact in zip(cols, quick_facts[row_start:row_start + 3]):
            with col:
                card(fact["title"], fact["value"], fact["detail"])
