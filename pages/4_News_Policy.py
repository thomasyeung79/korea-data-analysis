import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from locales.i18n import display_news_category, display_time_range, get_language, language_selector, t, translate_option

st.set_page_config(
    page_title=t("news.page_title"),
    page_icon="📰",
    layout="wide",
)

from ui_style import apply_product_style
from api_client import APIClient

apply_product_style()

api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en

st.markdown(
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>{t("news.brand")}</div>
        <h1>{t("news.heading")}</h1>
        <p>
            {t("news.subtitle")}
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{t("news.aside_tag")}</div>
            <h3 style="margin-top:1.2rem;">{t("news.aside_title")}</h3>
            <p style="color:#cbd5e1;">
                {t("news.aside_desc")}
            </p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

language_selector("news_language")

if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.divider()

tab_policy, tab_mbti = st.tabs([label("News & Policy", "新闻与政策"), label("MBTI City Match", "MBTI 城市匹配")])

with tab_policy:
    # ── Search Form ──

    st.markdown(f'<div class="section-label">{t("news.search_label")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {t('news.find_heading')}")

    col1, col2, col3 = st.columns(3)

    with col1:
        keyword = st.text_input(t("news.keyword"), placeholder=t("news.placeholder"))

    with col2:
        category = st.selectbox(
            t("news.category"),
            ["All", "Study", "Work", "Visa", "Economy", "Technology"],
            format_func=display_news_category,
        )

    with col3:
        time_range = st.selectbox(
            t("news.time_range"),
            ["Last 7 days", "Last 30 days", "Last 90 days"],
            format_func=display_time_range,
        )

    search_clicked = st.button(t("news.search_button"), use_container_width=True, type="primary")

    st.divider()

    # ── Results ──

    if search_clicked:
        try:
            result = api.search_news_policy(
                keyword=keyword,
                category=category,
                time_range=time_range,
                language=get_language(),
            )
            st.session_state["news_result"] = result
            st.session_state["news_count"] = result.get("result_count", 0)
        except Exception as e:
            st.error(t("news.failed", error=e))
            st.session_state.pop("news_result", None)

    if "news_result" in st.session_state:
        result = st.session_state["news_result"]
        count = result.get("result_count", 0)

        # ── Overview stats ──
        c1, c2, c3 = st.columns(3)
        c1.metric(t("news.results_found"), count)
        c2.metric(t("news.ai_summary"), t("common.generated"))
        c3.metric(t("news.suggestions"), len(result.get("action_suggestions", [])))

        st.divider()

        # ── AI Trend Summary ──
        st.markdown(t("news.trend"))
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

        # ── Action Suggestions ──
        suggestions = result.get("action_suggestions", [])
        if suggestions:
            st.markdown(t("news.action"))
            for s in suggestions:
                st.markdown(f"- ✅ {s}")

        # ── Charts ──
        results_list = result.get("results", [])
        if results_list:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                cat_counts = Counter(item["category"] for item in results_list)
                fig_cat = go.Figure(data=[go.Pie(
                    labels=[translate_option("news_category", category) for category in cat_counts.keys()],
                    values=list(cat_counts.values()),
                    marker=dict(colors=["#123c9c", "#d7263d", "#0f9f6e", "#f59e0b", "#8b5cf6"]),
                    textinfo="label+value",
                    hole=0.4,
                )])
                fig_cat.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=20), title=t("news.category_distribution"))
                st.plotly_chart(fig_cat, use_container_width=True)
            with col_chart2:
                scores = [item.get("relevance_score", 0) for item in results_list]
                titles = [item["title"][:30] + "..." for item in results_list]
                fig_score = go.Figure(data=[go.Bar(
                    x=titles, y=scores,
                    marker_color=["#0f9f6e" if s >= 70 else "#f59e0b" if s >= 40 else "#94a3b8" for s in scores],
                    text=scores,
                    textposition="outside",
                )])
                fig_score.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=60), title=t("news.relevance_scores"),
                                         xaxis_tickangle=-45)
                st.plotly_chart(fig_score, use_container_width=True)

        st.divider()

        # ── Result Cards ──
        results_list = result.get("results", [])

        if not results_list:
            st.info(t("news.no_items"))
        else:
            st.markdown(t("news.results_heading", count=count))

            for item in results_list:
                score = item.get("relevance_score", 0)
                score_bar = "🟢" if score >= 70 else "🟡" if score >= 40 else "⚪"
                impact = item.get("impact_for_students", "")

                with st.container():
                    st.markdown(
                        f"""
                    <div class="card" style="margin-bottom:1rem;">
                        <div style="display:flex; justify-content:space-between;">
                            <div>
                                <span class="module-tag">{translate_option('news_category', item['category'])}</span>
                                <span style="color:#94a3b8; font-size:0.85rem; margin-left:0.5rem;">
                                    {item['source_name']} · {item['published_at']}
                                </span>
                            </div>
                            <div style="font-size:0.85rem;">{score_bar} {score}/100</div>
                        </div>
                        <h3 style="margin:0.5rem 0;">{item['title']}</h3>
                        <p style="color:#475569;">{item['summary']}</p>
                        <details>
                            <summary style="cursor:pointer; color:#123c9c; font-weight:600;">
                                {t("news.impact")}
                            </summary>
                            <p style="margin-top:0.5rem;"><strong>{t("news.for_students")}</strong> {item['impact_for_students']}</p>
                            <p><strong>{t("news.for_job_seekers")}</strong> {item['impact_for_job_seekers']}</p>
                        </details>
                    </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.divider()

        # ── Export ──
        summary_text = (
            f"Korea News & Policy Search Results\n"
            f"Keyword: {keyword or '(all)'}\n"
            f"Category: {category}\n"
            f"Time Range: {time_range}\n"
            f"Results: {count}\n\n"
        )
        for item in results_list[:10]:
            summary_text += f"- [{item['category']}] {item['title']} ({item['published_at']})\n  {item['summary'][:120]}...\n\n"

        st.download_button(
            t("news.download"),
            data=summary_text,
            file_name="korea_news_search.txt",
            use_container_width=True,
        )

    else:
        st.info(t("news.empty"))

    st.divider()
    st.caption(t("news.footer"))

with tab_mbti:
    st.markdown(f'<div class="section-label">{label("LIVING PREFERENCE", "生活偏好")}</div>', unsafe_allow_html=True)
    st.markdown(f"## {label('MBTI City Match', 'MBTI 城市匹配')}")
    st.caption(label("This is a lifestyle preference helper, not a psychological diagnosis.", "这是生活偏好辅助推荐，不是心理诊断工具。"))

    mbti_types = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    m1, m2, m3 = st.columns(3)
    with m1:
        mbti_type = st.selectbox("MBTI", mbti_types, index=mbti_types.index("INFJ"))
        social_energy = st.selectbox(label("Social Energy", "社交能量"), ["Low", "Medium", "High"], format_func=lambda v: translate_option("mbti_preference", v))
        lifestyle_preference = st.selectbox(label("Lifestyle Preference", "生活方式偏好"), ["Quiet", "Balanced", "Urban", "Creative"], format_func=lambda v: translate_option("mbti_preference", v))
    with m2:
        pace_preference = st.selectbox(label("Pace Preference", "节奏偏好"), ["Slow", "Moderate", "Fast"], format_func=lambda v: translate_option("mbti_preference", v))
        budget_sensitivity = st.selectbox(label("Budget Sensitivity", "预算敏感度"), ["Low", "Medium", "High"], index=1, format_func=lambda v: translate_option("mbti_preference", v))
    with m3:
        career_priority = st.slider(label("Career Priority", "职业优先级"), 1, 10, 6)
        study_priority = st.slider(label("Study Priority", "留学优先级"), 1, 10, 6)

    mbti_payload = {
        "mbti_type": mbti_type,
        "social_energy": social_energy,
        "lifestyle_preference": lifestyle_preference,
        "pace_preference": pace_preference,
        "budget_sensitivity": budget_sensitivity,
        "career_priority": career_priority,
        "study_priority": study_priority,
        "language": get_language(),
    }
    if st.button(label("Match My City", "匹配我的城市"), use_container_width=True, type="primary"):
        try:
            match = api.match_mbti_city(mbti_payload)
            st.session_state["mbti_city_match"] = match
            st.success(label("MBTI city match generated.", "MBTI 城市匹配已生成。"))
        except Exception as exc:
            st.error(label(f"MBTI city match failed: {exc}", f"MBTI 城市匹配失败：{exc}"))

    match = st.session_state.get("mbti_city_match")
    if match:
        best_city = match.get("best_city", "")
        st.markdown(f"### {label('Recommended City', '推荐城市')}: {translate_option('city', best_city)}")
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric(label("Personality Fit", "人格匹配"), f"{match.get('personality_fit_score', 0):.1f}")
        mc2.metric(label("Lifestyle Fit", "生活方式匹配"), f"{match.get('lifestyle_fit_score', 0):.1f}")
        mc3.metric(label("Social Fit", "社交匹配"), f"{match.get('social_fit_score', 0):.1f}")
        mc4.metric(label("Career Environment", "职业环境"), f"{match.get('career_environment_score', 0):.1f}")
        mc5.metric(label("Study Environment", "学习环境"), f"{match.get('study_environment_score', 0):.1f}")

        scores = match.get("city_scores", [])
        if scores:
            fig = go.Figure(data=[go.Bar(
                x=[item["total_score"] for item in scores],
                y=[translate_option("city", item["city"]) for item in scores],
                orientation="h",
                marker_color="#123c9c",
            )])
            fig.update_layout(
                title=label("MBTI City Match Scores", "MBTI 城市匹配分数"),
                xaxis_title=label("Total Score", "??"),
                yaxis_title=label("City", "??"),
                height=360,
                margin=dict(l=20, r=20, t=60, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"#### {label('Why it fits', '适合原因')}")
        st.write(match.get("recommendation_reason", ""))
        st.markdown(f"#### {label('Potential Challenges', '潜在挑战')}")
        for challenge in match.get("potential_challenges", []):
            st.markdown(f"- {challenge}")
        st.markdown(f"#### {label('Suggested Living Style', '建议生活方式')}")
        st.info(match.get("suggested_living_style", ""))
    else:
        st.info(label("Choose your preferences and click **Match My City**.", "选择你的偏好并点击 **匹配我的城市**。"))
