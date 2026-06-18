import streamlit as st
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(
    page_title="News & Policy",
    page_icon="📰",
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
        <div class="brand-row"><span class="brand-dot"></span>V2 · MODULE 4</div>
        <h1>Korea News & Policy</h1>
        <p>
            Recent developments in Korea that affect your study, work, visa, economy,
            and technology decisions. Based on curated sources — updated periodically.
        </p>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>Mock data · MVP</div>
            <h3 style="margin-top:1.2rem;">15 curated items</h3>
            <p style="color:#cbd5e1;">
                Covers study, work, visa, economy, and technology categories.
                Live news API integration planned for future release.
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

# ── Search Form ──

st.markdown('<div class="section-label">SEARCH</div>', unsafe_allow_html=True)
st.markdown("## Find relevant news")

col1, col2, col3 = st.columns(3)

with col1:
    keyword = st.text_input("Keyword", placeholder="e.g. visa, AI, scholarship, TOPIK...")

with col2:
    category = st.selectbox("Category", ["All", "Study", "Work", "Visa", "Economy", "Technology"])

with col3:
    time_range = st.selectbox("Time Range", ["Last 7 days", "Last 30 days", "Last 90 days"])

search_clicked = st.button("Search News & Policy", use_container_width=True, type="primary")

st.divider()

# ── Results ──

if search_clicked:
    try:
        result = api.search_news_policy(
            keyword=keyword,
            category=category,
            time_range=time_range,
        )
        st.session_state["news_result"] = result
        st.session_state["news_count"] = result.get("result_count", 0)
    except Exception as e:
        st.error(f"Search failed: {e}")
        st.session_state.pop("news_result", None)

if "news_result" in st.session_state:
    result = st.session_state["news_result"]
    count = result.get("result_count", 0)

    # ── Overview stats ──
    c1, c2, c3 = st.columns(3)
    c1.metric("Results found", count)
    c2.metric("AI Summary", "Generated")
    c3.metric("Suggestions", len(result.get("action_suggestions", [])))

    st.divider()

    # ── AI Trend Summary ──
    st.markdown("### 📈 AI Trend Summary")
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
        st.markdown("### 💡 Action Suggestions")
        for s in suggestions:
            st.markdown(f"- ✅ {s}")

    # ── Charts ──
    results_list = result.get("results", [])
    if results_list:
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            cat_counts = Counter(item["category"] for item in results_list)
            fig_cat = go.Figure(data=[go.Pie(
                labels=list(cat_counts.keys()),
                values=list(cat_counts.values()),
                marker=dict(colors=["#123c9c", "#d7263d", "#0f9f6e", "#f59e0b", "#8b5cf6"]),
                textinfo="label+count",
                hole=0.4,
            )])
            fig_cat.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=20), title="Category Distribution")
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
            fig_score.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=60), title="Relevance Scores",
                                     xaxis_tickangle=-45)
            st.plotly_chart(fig_score, use_container_width=True)

    st.divider()

    # ── Result Cards ──
    results_list = result.get("results", [])

    if not results_list:
        st.info("No items match your search criteria. Try broadening your keywords or time range.")
    else:
        st.markdown(f"### 📄 Results ({count})")

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
                            <span class="module-tag">{item['category']}</span>
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
                            Impact analysis
                        </summary>
                        <p style="margin-top:0.5rem;"><strong>For students:</strong> {item['impact_for_students']}</p>
                        <p><strong>For job seekers:</strong> {item['impact_for_job_seekers']}</p>
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
        "📥 Download Results (TXT)",
        data=summary_text,
        file_name="korea_news_search.txt",
        use_container_width=True,
    )

else:
    st.info("Enter a keyword and click **Search News & Policy** to see results.")

st.divider()
st.caption("Korea Study & Career Decision Agent · News & Policy v1.0 (mock data)")
