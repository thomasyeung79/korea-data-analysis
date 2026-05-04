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
    page_title="Society",
    page_icon="🧠",
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

st.title("🧠 Korean Society & Daily Life")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

show_optional_music(
    "Feel My Rhythm",
    "Red Velvet",
    "https://www.youtube.com/watch?v=R9At2ICm4LQ",
    start=14
)

st.caption(
    "Understanding Korean society beyond stereotypes about pressure, competition, and daily life."
)

st.divider()

st.subheader("⚖️ Society Perception vs Reality")

question = st.selectbox(
    "Choose a perception",
    [
        "Korea is extremely stressful",
        "Korea has no work-life balance",
        "Korea is too competitive",
        "Korea is hard for foreigners",
        "Korea only has pressure, not quality of life"
    ]
)

society_map = {
    "Korea is extremely stressful": {
        "reality": "Pressure exists, especially in education and employment, but similar patterns also appear across East Asia.",
        "insight": "Korea is competitive, but it should be understood as part of a broader high-performance system."
    },
    "Korea has no work-life balance": {
        "reality": "Work culture can be demanding, but lifestyle culture, cafés, public spaces, entertainment, and leisure activities are also highly developed.",
        "insight": "Korean society is not one-dimensional. Pressure and lifestyle coexist."
    },
    "Korea is too competitive": {
        "reality": "Competition is real, but it is linked to education, industry, and social mobility.",
        "insight": "Competition becomes part of the system that produces high output."
    },
    "Korea is hard for foreigners": {
        "reality": "Language and cultural barriers exist, but internationalisation, tourism infrastructure, and digital services are improving.",
        "insight": "Korea is not barrier-free, but it is becoming more accessible."
    },
    "Korea only has pressure, not quality of life": {
        "reality": "Korea also offers strong public transport, safety, convenience, food culture, digital services, and urban lifestyle.",
        "insight": "Quality of life should be judged by multiple dimensions, not only social pressure."
    }
}

selected = society_map[question]

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

st.subheader("🏙️ Work & Life System")

society_data = pd.DataFrame({
    "Dimension": [
        "Education Pressure",
        "Employment Competition",
        "Digital Convenience",
        "Urban Lifestyle",
        "Public Safety",
        "Cultural Leisure"
    ],
    "Level (0-10)": [8, 8, 9, 9, 9, 9],
    "Meaning": [
        "Strong academic competition",
        "Competitive job market",
        "Highly digitalised services",
        "Cafés, shopping, nightlife, transport",
        "Generally high urban safety",
        "Music, drama, food, events, sports"
    ]
})

st.dataframe(society_data, use_container_width=True)

st.caption(
    "Scores are conceptual and used to explain the balance between pressure and quality of life."
)

st.divider()

st.subheader("📊 Society Balance Simulator")

efficiency = st.slider("System Efficiency", 0, 10, 9)
pressure = st.slider("Social Pressure", 0, 10, 7)
lifestyle = st.slider("Lifestyle Quality", 0, 10, 8)
accessibility = st.slider("Foreigner Accessibility", 0, 10, 7)

society_score = (
    efficiency * 0.3 +
    (10 - pressure) * 0.2 +
    lifestyle * 0.3 +
    accessibility * 0.2
)

st.metric("Society Balance Score", round(society_score, 2))

if society_score >= 8:
    st.success("Strong society balance: Korea combines efficiency, lifestyle quality, and improving accessibility.")
elif society_score >= 6:
    st.info("Moderate society balance: Korea has strong systems, but pressure remains an important challenge.")
else:
    st.warning("Weak society balance: pressure may outweigh lifestyle and accessibility benefits.")

st.caption(
    "This model is simplified. It shows how efficiency, pressure, lifestyle, and accessibility interact."
)

if "module_scores" not in st.session_state:
    st.session_state["module_scores"] = {}

st.session_state["module_scores"]["Society"] = society_score

st.caption(f"Saved score: {st.session_state['module_scores']}")

st.divider()

st.subheader("🧠 Key Insight")

st.info("""
Korean society should not be reduced to one word: **pressure**.

It is better understood as a system where:

- High competition creates pressure  
- Strong infrastructure improves daily life  
- Digital services increase convenience  
- Cultural life provides balance  

👉 Korea is not simply stressful.  
👉 It is a high-efficiency society with both pressure and lifestyle strength.
""")
