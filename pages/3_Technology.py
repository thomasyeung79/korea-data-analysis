import streamlit as st
import pandas as pd

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
    page_title="Technology",
    page_icon="💻",
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

st.title("💻 Korea as a Technology System")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

show_optional_music(
    "Limitless",
    "NCT 127",
    "https://www.youtube.com/watch?v=zmUn7V6uuZM",
)

st.divider()

st.caption(
    "Technology explains how Korea builds scalable systems across industries."
)

st.subheader("🧠 Technology Perception Check")

question = st.selectbox(
    "What do you think about Korean technology?",
    [
        "Korea is only strong in electronics",
        "Korea relies on foreign technology",
        "Korea is not a tech leader like the US",
        "Technology is separate from culture"
    ]
)

tech_map = {
    "Korea is only strong in electronics": {
        "reality": "Korea leads in semiconductors, displays, batteries, and advanced manufacturing.",
        "insight": "Electronics is just the visible layer of a deeper industrial system."
    },
    "Korea relies on foreign technology": {
        "reality": "Korea integrates global supply chains but has strong domestic R&D capabilities.",
        "insight": "Modern tech systems are global, but leadership comes from integration ability."
    },
    "Korea is not a tech leader like the US": {
        "reality": "Korea is a global leader in key hardware sectors such as memory chips and displays.",
        "insight": "Different countries lead in different layers of the tech stack."
    },
    "Technology is separate from culture": {
        "reality": "Korea combines technology with culture (K-pop, gaming, platforms).",
        "insight": "Technology amplifies cultural influence."
    }
}

selected = tech_map[question]

col1, col2 = st.columns(2)

with col1:
    st.warning(f"""
### ❌ Perception

{question}
""")

with col2:
    st.success(f"""
### ✅ Reality

{selected["reality"]}
""")

st.info(f"""
### 💡 Insight

{selected["insight"]}
""")

st.divider()

st.subheader("📊 Core Technology Strength")

tech_data = pd.DataFrame({
    "Sector": ["Semiconductors", "Displays", "Batteries", "Consumer Tech"],
    "Global Level (0-10)": [10, 10, 9, 9]
})

st.dataframe(tech_data, use_container_width=True)

st.bar_chart(
    tech_data.set_index("Sector")
)

st.caption(
    "Scores are conceptual, based on global industry leadership and market influence."
)

st.divider()

st.subheader("🌏 Global Technology Expansion")

expansion_data = pd.DataFrame({
    "Aspect": [
        "Hardware Export",
        "Global Manufacturing",
        "Digital Platforms",
        "Cultural Technology"
    ],
    "Score (0-10)": [10, 9, 8, 9]
})

st.dataframe(expansion_data, use_container_width=True)

st.bar_chart(
    expansion_data.set_index("Aspect")
)

st.caption(
    "These values reflect Korea’s ability to scale technology systems globally."
)

st.success("""
Korea’s strength is not only in innovation,  
but in scaling systems across global markets.
""")

st.divider()

st.subheader("⚙️ System Model (Android Analogy)")

st.markdown("""
Korea’s system can be understood like Android:

- **Core system** → Technology, training, production  
- **Custom layer** → Different markets, languages, content  

👉 Same system, different outputs  
👉 Scalable across regions  
""")

st.info("""
This is why Korean systems work globally:
they are modular and adaptable.
""")

st.divider()

st.subheader("📊 Technology Power Simulator")

innovation = st.slider("Innovation", 0, 10, 9)
industry = st.slider("Industrial Strength", 0, 10, 9)
global_scale = st.slider("Global Expansion", 0, 10, 9)
integration = st.slider("System Integration", 0, 10, 9)

tech_score = (
    innovation * 0.25 +
    industry * 0.25 +
    global_scale * 0.25 +
    integration * 0.25
)

st.metric("Korea Technology Power Score", round(tech_score, 2))

st.caption(
    "This simplified model shows how different factors combine into a scalable system."
)

if "module_scores" not in st.session_state:
    st.session_state["module_scores"] = {}

st.session_state["module_scores"]["Technology"] = tech_score

st.caption(f"Saved score: {st.session_state['module_scores']}")

st.divider()

st.subheader("🧠 Key Takeaway")

st.info("""
Korea’s strength is not just technology.

👉 It is the ability to build systems that scale globally.

- Hardware + Industry  
- Culture + Platforms  
- Local system → Global expansion  

👉 Korea exports systems, not just products.
""")
