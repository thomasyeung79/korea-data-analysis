import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="History",
    page_icon="📜",
    layout="wide"
)

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

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}

.card {
    padding: 1.5rem;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    background: white;
    min-height: 170px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

.card h3 {margin-top: 0;}
.card p {color: #444; font-size: 1rem;}
</style>
""", unsafe_allow_html=True)

st.title("📜 Historical Context")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

# 🎵 Music
show_optional_music(
    "History",
    "EXO-K",
    "https://www.youtube.com/watch?v=vdejiaoEhFc",
    start=5
)

st.caption("Understanding how Korea’s past shaped its present global position.")

st.divider()

st.subheader("🕰 Development Timeline")

timeline_steps = [
    "1897 Empire",
    "1910–1945 Colonisation",
    "1945 Liberation",
    "1948 Division",
    "1950–1953 War",
    "1960s–1990s Miracle",
    "2000s–Present Global Korea"
]

selected_index = st.selectbox(
    "Select a stage",
    range(len(timeline_steps)),
    format_func=lambda x: timeline_steps[x]
)

st.progress((selected_index + 1) / len(timeline_steps))
st.caption("Move through each stage to see how Korea developed over time.")

st.divider()

history_data = [
    {"meaning": "Korea began transitioning toward a modern state system.",
     "impact": "Established early foundations of national identity."},

    {"meaning": "Loss of sovereignty under Japanese colonial rule.",
     "impact": "Strengthened nationalism and long-term development urgency."},

    {"meaning": "Liberation after World War II.",
     "impact": "Opened the path for independent state-building."},

    {"meaning": "Division of the Korean Peninsula.",
     "impact": "Created two distinct political and economic systems."},

    {"meaning": "War devastated infrastructure and the economy.",
     "impact": "Triggered reconstruction-driven development strategy."},

    {"meaning": "Rapid industrialisation and export-led growth.",
     "impact": "Transformed Korea into an advanced economy."},

    {"meaning": "Global expansion in culture, technology, and sports.",
     "impact": "Built Korea’s modern global influence."}
]

selected = history_data[selected_index]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>📘 Historical Meaning</h3>
        <p>{selected["meaning"]}</p >
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>🚀 Impact on Modern Korea</h3>
        <p>{selected["impact"]}</p >
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 📊 Impact Scores
st.subheader("📊 System Impact Level")

impact_scores = [
    {"Economy": 2, "Culture": 2, "Global Influence": 1},
    {"Economy": 2, "Culture": 3, "Global Influence": 1},
    {"Economy": 3, "Culture": 3, "Global Influence": 2},
    {"Economy": 4, "Culture": 3, "Global Influence": 2},
    {"Economy": 5, "Culture": 4, "Global Influence": 3},
    {"Economy": 9, "Culture": 7, "Global Influence": 7},
    {"Economy": 9, "Culture": 10, "Global Influence": 10}
]

scores = impact_scores[selected_index]

scores_df = pd.DataFrame(
    list(scores.items()),
    columns=["Category", "Score"]
)

st.bar_chart(scores_df.set_index("Category"))

st.caption(
    "Scores are conceptual and designed to show how historical stages contribute to Korea’s modern capabilities."
)

final_scores = impact_scores[-1]

history_score = round(
    final_scores["Economy"] * 0.3 +
    final_scores["Culture"] * 0.3 +
    final_scores["Global Influence"] * 0.4,
    2
)

st.metric("History System Score", history_score)

if "module_scores" not in st.session_state:
    st.session_state["module_scores"] = {}

st.session_state["module_scores"]["History"] = history_score

st.caption(f"Saved module scores: {st.session_state['module_scores']}")

st.divider()

st.subheader("🧠 Key Takeaway")

st.info("""
Korea’s rise is not accidental.

👉 It is built through sequential historical stages  
👉 Each stage adds structural capability  
👉 The final result is a globally competitive system  

Understanding Korea requires understanding this progression.
""")
