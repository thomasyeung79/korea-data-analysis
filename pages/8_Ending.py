import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
import pandas as pd

client = OpenAI()


def generate_ai_summary(q1, q2, q3, q4, score, module_scores):
    try:
        prompt = f"""
You are an analyst writing a concise strategic report on Korea.

User perception:
- Technology: {q1}/10
- Culture: {q2}/10
- Social Pressure: {q3}/10
- Global Influence: {q4}/10
- Overall Perception Score: {score}/10

System module scores:
{module_scores}

Return ONLY valid JSON with this structure:

{{
  "executive_summary": "...",
  "system_strengths": ["...", "...", "..."],
  "structural_risks": ["...", "..."],
  "comparative_position": "...",
  "strategic_insight": "...",
  "system_interaction": "..."
}}

Keep it concise, analytical, and suitable for a portfolio project.
"""

        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f'{{"error": "AI insight not available: {e}"}}'


def save_user_result(username, q1, q2, q3, q4, score, ai_result):
    data = {
        "username": username if username else "Anonymous",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "technology": q1,
        "culture": q2,
        "pressure": q3,
        "global_influence": q4,
        "score": score,
        "ai_result": ai_result
    }

    try:
        with open("user_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        results = []

    results.append(data)

    with open("user_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


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

st.title("🏁 Final Evaluation")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

show_optional_music(
    "Universe",
    "EXO",
    "https://www.youtube.com/watch?v=leu-cTvMWTA",
)

st.caption(
    "This final section turns the project into an evaluation system."
)

st.divider()

st.subheader("🧠 Perception vs Reality")

questions = [
    "Korea is only about K-pop",
    "Korea is too small to matter",
    "Korea is extremely stressful",
    "Korea is only culturally strong"
]

selected = st.selectbox("Choose a perception", questions)

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
        <p>{selected}</p >
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>✅ Reality</h3>
        <p>{selected_data["reality"]}</p >
        <p style="margin-top:10px; color:#0d6efd;">
            <strong>{selected_data["insight"]}</strong>
        </p >
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("📊 System Score Overview")

module_scores = st.session_state.get("module_scores", {})

default_scores = {
    "History": 8.5,
    "Analysis": 8,
    "Technology": 9,
    "Culture": 9,
    "K-pop": 8.5,
    "Sports": 8,
    "Football": 8.5,
    "Society": 7,
    "Tourism": 8
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

st.divider()

st.subheader("🧠 Your Korea Perception")

st.caption("Rate your personal view before seeing the final analysis.")

username = st.text_input("Enter your name or nickname (optional)")

q1 = st.slider("How strong is Korea in technology?", 0, 10, 5)
q2 = st.slider("How strong is Korea in culture?", 0, 10, 5)
q3 = st.slider("How stressful do you think Korea is?", 0, 10, 5)
q4 = st.slider("How globally influential is Korea?", 0, 10, 5)

score = (
    q1 * 0.3 +
    q2 * 0.3 +
    (10 - q3) * 0.2 +
    q4 * 0.2
)

st.metric("Your Korea Understanding Score", round(score, 2))

if st.button("Generate AI Insight"):
    with st.spinner("Analyzing your perception..."):
        result = generate_ai_summary(
            q1,
            q2,
            q3,
            q4,
            round(score, 2),
            module_scores
        )

        report = json.loads(result)

        st.subheader("📄 AI Strategic Report")

        if "error" in report:
            st.warning(report["error"])
        else:
            st.markdown("### 🧠 Executive Summary")
            st.info(report["executive_summary"])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 💪 System Strengths")
                for item in report["system_strengths"]:
                    st.success(f"✅ {item}")

            with col2:
                st.markdown("### ⚠️ Structural Risks")
                for item in report["structural_risks"]:
                    st.warning(f"⚠️ {item}")

            st.markdown("### 🌏 Comparative Position")
            st.write(report["comparative_position"])

            st.markdown("### 🔗 System Interaction")
            st.info(report["system_interaction"])

            st.markdown("### 🎯 Strategic Insight")
            st.success(report["strategic_insight"])

        save_user_result(
            username,
            q1,
            q2,
            q3,
            q4,
            round(score, 2),
            result
        )

        st.caption("Your perception profile has been saved locally.")

st.divider()

st.subheader("📌 What This Project Shows")

st.markdown("""
Across all modules:

- 📜 History → Rapid transformation  
- 📊 Analysis → High-efficiency system  
- 💻 Technology → Industrial and digital foundation  
- 🎤 Culture → Cultural export system  
- 🎶 K-pop → Global entertainment market strategy  
- 🏅 Sports → Multi-sport competitiveness  
- ⚽ Football → EPL/UCL pathway and elite player export  
- 🧠 Society → Pressure and lifestyle balance  
- ✈️ Tourism → Real-world experience layer  
""")

st.success("""
Korea’s global influence is not accidental.

👉 It is the result of a coordinated system across:
history, economy, technology, culture, sports, society, and tourism.

This is not a single success story —  
it is a system-level outcome.
""")

st.divider()

st.subheader("🎯 Final Thought")

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

st.subheader("💬 Reflection")

st.info("""
After exploring this project, consider:

- What drives a country's global influence?
- Can rapid development be replicated elsewhere?
- How important is system efficiency compared to size?

👉 The goal of this project is not to judge, but to understand.
""")

st.caption("This project is not an answer — it is a framework for thinking.")
