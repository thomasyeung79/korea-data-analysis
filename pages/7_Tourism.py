import streamlit as st

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
    page_title="Tourism",
    page_icon="✈️",
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

st.title("✈️ Experiencing South Korea")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

show_optional_music(
    "Party",
    "Girls' Generation",
    "https://www.youtube.com/watch?v=HQzu7NYlZNQ",
    start=18
)

st.divider()

st.subheader("🧠 Travel Perception vs Reality")

question = st.selectbox(
    "What do you think about travelling in South Korea?",
    [
        "Korea is too expensive",
        "Korea is only Seoul",
        "Korea is too stressful",
        "Korea is not foreigner-friendly"
    ]
)

travel_map = {
    "Korea is too expensive": {
        "reality": "Korea can be affordable with public transport, convenience stores, street food, and budget accommodation.",
        "insight": "Travel cost depends more on travel style than on the country itself."
    },
    "Korea is only Seoul": {
        "reality": "Korea also offers Busan, Jeju, Gyeongju, Gangneung, Jeonju, and many regional experiences.",
        "insight": "Seoul is the gateway, not the whole travel experience."
    },
    "Korea is too stressful": {
        "reality": "Work culture may be intense, but travel experience can be relaxed, convenient, and enjoyable.",
        "insight": "Daily work pressure and tourist experience are different layers of society."
    },
    "Korea is not foreigner-friendly": {
        "reality": "Korea has improved tourism infrastructure, transport apps, multilingual signs, and international services.",
        "insight": "Barriers still exist, but accessibility is improving."
    }
}

selected = travel_map[question]

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

st.subheader("🌍 Travel Experience Dimensions")

col1, col2, col3 = st.columns(3)

col1.metric("Convenience", "9/10", "Transport & safety")
col2.metric("Culture", "9/10", "History + modern lifestyle")
col3.metric("Lifestyle", "8/10", "Food, cafés, shopping")

st.divider()

st.subheader("📍 Beyond Tourist Spots")

st.markdown("""
South Korea is not only about famous landmarks.

A strong travel experience comes from everyday systems:

- 🚇 Efficient public transport  
- ☕ Café and lifestyle culture  
- 🛍️ Shopping and digital convenience  
- 🌃 Nighttime city atmosphere  
- 🏛️ Historical and regional diversity  

👉 Travel in Korea is not only about where you go, but how the country feels.
""")

st.divider()

st.subheader("📊 Travel Experience Score")

cost = st.slider("Affordability", 0, 10, 7)
convenience = st.slider("Convenience", 0, 10, 9)
culture = st.slider("Cultural Experience", 0, 10, 9)
accessibility = st.slider("Foreigner Accessibility", 0, 10, 8)

travel_score = (
    cost * 0.2 +
    convenience * 0.3 +
    culture * 0.3 +
    accessibility * 0.2
)

st.metric("Korea Travel Experience Score", round(travel_score, 2))

if travel_score >= 8:
    st.success("Strong travel experience: Korea combines convenience, culture, and lifestyle appeal.")
elif travel_score >= 6:
    st.info("Good travel experience: Korea has strong appeal, but cost or accessibility may affect some visitors.")
else:
    st.warning("Limited travel experience: some barriers may reduce the overall experience.")

st.caption(
    "This score is a conceptual model showing how different factors shape the travel experience."
)

st.divider()

st.subheader("🧠 Key Takeaway")

st.markdown("""
Travelling in South Korea is not just about sightseeing.

👉 It is about experiencing a highly connected lifestyle system:  
transport, food, culture, shopping, cities, and regional diversity.

Tourism turns Korea’s national system into something visitors can personally feel.
""")
