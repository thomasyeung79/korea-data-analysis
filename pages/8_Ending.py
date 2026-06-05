import streamlit as st
import json
import io
import pandas as pd
from api_client import get_api
from ui_style import apply_product_style, tr


def show_optional_music(title, artist, url, start=0):
    video_id = url.split("v=")[-1].split("&")[0]

    with st.expander("🎵 Optional Music (Official Source)"):
        st.caption(f"Now Playing: {title} - {artist}")

        st.markdown(f"""
        <iframe
            width="360"
            height="203"
            src="https://www.youtube.com/embed/{video_id}?start={start}"
            frameborder="0"
            allowfullscreen>
        </iframe>
        """, unsafe_allow_html=True)

        st.caption("Music via official YouTube embed.")


st.set_page_config(
    page_title="Ending",
    page_icon="🎯",
    layout="wide"
)

apply_product_style()

api = get_api()

st.title(tr("🏁 Decision Report", "🏁 决策报告"))

user_name = api.user.get("username") if api.is_authenticated else None

if not user_name:
    st.warning(
        tr("Please return to Home and enter your username first.", "请先返回首页输入用户名。")
    )
    if st.button(tr("🏠 Back to Home", "🏠 返回首页")):
        st.switch_page("app.py")
    st.stop()

st.info(f"👤 {user_name}")

if st.button(tr("🏠 Back to Home", "🏠 返回首页")):
    st.switch_page("app.py")

show_optional_music(
    "Universe", "EXO",
    "https://www.youtube.com/watch?v=leu-cTvMWTA",
)

st.caption(
    tr("Convert your Korea intelligence journey into a concise strategic report.",
       "把你的韩国智能分析过程转化为一份简洁的战略报告。")
)

st.divider()

st.subheader(tr("🧠 Perception vs Reality", "🧠 认知与现实"))

questions = [
    "Korea is only about K-pop",
    "Korea is too small to matter",
    "Korea is extremely stressful",
    "Korea is only culturally strong"
]

selected = st.selectbox(tr("Choose a perception", "选择一种认知"), questions)

perception_map = {
    "Korea is only about K-pop": {
        "reality": "Korea is also a global leader in semiconductors, cars, shipbuilding, and digital industries.",
        "insight": "Culture is the surface. Industry is the foundation."
    },
    "Korea is too small to matter": {
        "reality": "Korea has a top-tier global presence despite its size.",
        "insight": "Influence is not determined by geography, but by system strength."
    },
    "Korea is extremely stressful": {
        "reality": "Pressure exists, but similar patterns exist across East Asia.",
        "insight": "Korea is competitive, but not uniquely extreme."
    },
    "Korea is only culturally strong": {
        "reality": "Korea combines culture, technology, sports, society, tourism, and industry.",
        "insight": "It is a multi-dimensional system."
    }
}

selected_data = perception_map[selected]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>❌ Perception</h3>
        <p>{selected}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>✅ Reality</h3>
        <p>{selected_data["reality"]}</p>
        <p style="margin-top:10px; color:#0d6efd;">
            <strong>{selected_data["insight"]}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader(tr("📊 System Score Overview", "📊 系统评分概览"))

# Load module scores from backend
try:
    module_scores_list = api.get_module_scores()
    module_scores = {s["module_name"]: s["score"] for s in module_scores_list}
except Exception:
    module_scores = {}

default_scores = {
    "History": 8.5, "Analysis": 8, "Technology": 9,
    "Culture": 9, "Sports": 8, "Society": 7, "Tourism": 8
}

for k, v in default_scores.items():
    module_scores.setdefault(k, v)

df = pd.DataFrame(
    list(module_scores.items()),
    columns=["Module", "Score"]
)

st.bar_chart(df.set_index("Module"))

overall_score = round(sum(module_scores.values()) / len(module_scores), 2)

st.metric("🌐 Overall System Score", overall_score)

st.caption(
    "Scores combine user interaction and system defaults to represent Korea as a multi-dimensional system."
)

# ── Export Module Scores ──
with st.expander(tr("📥 Export Scores as CSV", "📥 导出评分为 CSV")):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label=tr("📥 Download Module Scores CSV", "📥 下载模块评分数据"),
        data=csv_buffer.getvalue(),
        file_name="korea_module_scores.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.divider()

# ── Perception Comparison ──
st.subheader(tr("📊 Your Score vs Global Average", "📊 你的评分 vs 全局平均"))

try:
    averages = api.get_perception_averages()
    my_latest = averages.get("my_latest")
    global_avgs = averages.get("global_averages", {})

    if my_latest:
        compare_data = pd.DataFrame({
            "Dimension": ["Technology", "Culture", "Global Influence", "Overall"],
            "You": [
                my_latest["technology"],
                my_latest["culture"],
                my_latest["global_influence"],
                my_latest["overall_score"],
            ],
            "Average": [
                global_avgs.get("technology", 0),
                global_avgs.get("culture", 0),
                global_avgs.get("global_influence", 0),
                global_avgs.get("overall_score", 0),
            ],
        })

        st.dataframe(compare_data, use_container_width=True)
        st.bar_chart(compare_data.set_index("Dimension"))

        st.caption(
            tr(f"Based on {averages['total_results']} results from {averages['total_users']} users.",
               f"基于 {averages['total_results']} 条结果，来自 {averages['total_users']} 位用户。")
        )
    else:
        st.info(tr("Complete a perception quiz first to see comparison.", "先完成认知测试来查看对比。"))
except Exception:
    st.info(tr("Login and save a perception result to see comparison.", "登录并保存认知结果后可查看对比。"))

st.divider()

st.subheader(tr("🧠 Your Korea Perception", "🧠 你的韩国认知"))

st.caption(tr("Rate your personal view before seeing the final analysis.", "在查看最终分析前，为你的个人认知打分。"))

st.info(f"👤 {user_name}")

q1 = st.slider("How strong is Korea in technology?", 0, 10, 5)
q2 = st.slider("How strong is Korea in culture?", 0, 10, 5)
q3 = st.slider("How stressful do you think Korea is?", 0, 10, 5)
q4 = st.slider("How globally influential is Korea?", 0, 10, 5)

score = q1 * 0.3 + q2 * 0.3 + (10 - q3) * 0.2 + q4 * 0.2

st.metric(tr("Your Korea Understanding Score", "你的韩国理解评分"), round(score, 2))

if st.button(tr("Generate AI Insight", "生成 AI 洞察")):
    with st.spinner(tr("Analyzing your perception...", "正在分析你的认知...")):
        try:
            result = api.generate_ai("perception_report", {
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "q4": q4,
                "score": round(score, 2),
                "module_scores": module_scores,
            })
        except Exception as e:
            result = json.dumps({"error": f"AI insight not available: {e}"})

        try:
            clean_result = result.strip()
            clean_result = clean_result.replace("```json", "")
            clean_result = clean_result.replace("```", "")
            report = json.loads(clean_result)
        except (json.JSONDecodeError, Exception):
            report = {"error": "AI returned non-JSON content.", "raw_text": result}

        st.subheader(tr("📄 AI Strategic Report", "📄 AI 战略报告"))

        if "error" in report:
            st.warning(report["error"])
            if "raw_text" in report:
                st.markdown(f"### {tr('Raw AI Output', 'AI 原始输出')}")
                st.write(report["raw_text"])
        else:
            st.markdown(f"### {tr('🧠 Executive Summary', '🧠 执行摘要')}")
            st.info(report["executive_summary"])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {tr('💪 System Strengths', '💪 系统优势')}")
                for item in report["system_strengths"]:
                    st.success(f"✅ {item}")

            with col2:
                st.markdown(f"### {tr('⚠️ Structural Risks', '⚠️ 结构风险')}")
                for item in report["structural_risks"]:
                    st.warning(f"⚠️ {item}")

            st.markdown(f"### {tr('🌏 Comparative Position', '🌏 比较位置')}")
            st.write(report["comparative_position"])

            st.markdown(f"### {tr('🔗 System Interaction', '🔗 系统互动')}")
            st.info(report["system_interaction"])

            st.markdown(f"### {tr('🎯 Strategic Insight', '🎯 战略洞察')}")
            st.success(report["strategic_insight"])

        # Save perception result via API
        try:
            api.save_perception_result({
                "technology": q1,
                "culture": q2,
                "pressure": q3,
                "global_influence": q4,
                "overall_score": round(score, 2),
                "ai_report": result,
            })
        except Exception:
            pass

        st.caption(tr("Your perception profile has been saved.", "你的认知档案已保存。"))

st.divider()

st.subheader(tr("📌 What This Project Shows", "📌 这个项目说明了什么"))

st.markdown("""
Across all modules:

- 📜 History → Rapid transformation
- 📊 Analysis → High-efficiency system
- 💻 Technology → Industrial and digital foundation
- 🎤 Culture → Cultural export system
- 🏅 Sports → Multi-sport competitiveness
- 🧠 Society → Pressure and lifestyle balance
- ✈️ Tourism → Real-world experience layer
""")

st.success("""
Korea's global influence is not accidental.

👉 It is the result of a coordinated system across:
history, economy, technology, culture, sports, society, and tourism.

This is not a single success story —
it is a system-level outcome.
""")

st.divider()

st.subheader(tr("🎯 Final Thought", "🎯 最终思考"))

st.markdown("""
Korea is not a "perfect country".
But it is a **high-performance system**.

It demonstrates that:

- Scale is not a prerequisite for influence
- Cultural and industrial power can reinforce each other
- Rapid transformation is achievable under the right structure

👉 The real question is not:

**"Is Korea good or bad?"**

👉 The real question is:

**"What can we learn from its system design?"**
""")

st.divider()

st.subheader(tr("💬 Reflection", "💬 反思"))

st.info("""
After exploring this project, consider:

- What drives a country's global influence?
- Can rapid development be replicated elsewhere?
- How important is system efficiency compared to size?

👉 The goal of this project is not to judge, but to understand.
""")

st.caption(tr("This project is not an answer — it is a framework for thinking.",
               "这个项目不是一个标准答案，而是一套思考框架。"))
