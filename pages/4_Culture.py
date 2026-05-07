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
    page_title="K-pop",
    page_icon="🎤",
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

st.title("🎤 Korean Entertainment Power")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

show_optional_music(
    "Growl",
    "EXO",
    "https://www.youtube.com/watch?v=I3dezFzsNss"
)

st.caption("K-pop is only one part of South Korea’s wider cultural export system.")

st.divider()

st.subheader("🧠 Entertainment System Explorer")

selected_area = st.selectbox(
    "Choose an area to explore",
    [
        "K-pop Industry",
        "K-drama Global Impact",
        "Korean-built Global Groups",
        "Entertainment as Soft Power"
    ]
)

entertainment_map = {
    "K-pop Industry": {
        "meaning": "K-pop is built through training systems, company strategy, digital platforms, and global fandom.",
        "insight": "K-pop is not just music. It is an industrial system."
    },
    "K-drama Global Impact": {
        "meaning": "K-dramas reach global audiences through streaming platforms and strong storytelling.",
        "insight": "K-drama expands Korea’s cultural influence beyond music."
    },
    "Korean-built Global Groups": {
        "meaning": "Korean companies create groups targeting Japan, China, the US, and other markets.",
        "insight": "Korea exports not only artists, but also the idol production model."
    },
    "Entertainment as Soft Power": {
        "meaning": "Entertainment strengthens Korea’s image, tourism, language interest, and brand value.",
        "insight": "Cultural exports turn national image into global influence."
    }
}

selected = entertainment_map[selected_area]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>📌 What It Means</h3>
        <p>{selected["meaning"]}</p >
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>💡 Insight</h3>
        <p>{selected["insight"]}</p >
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("🎤 K-pop Industry Intelligence")

st.markdown("""
K-pop is one of the most visible parts of Korea's cultural export system.

A dedicated K-pop analytics module explores:

- company strategy
- generation trends
- global market focus
- US market potential
- next global hit prediction
""")

if st.button("🎤 Open K-pop Industry Analysis"):
    st.switch_page("pages/4a_Kpop.py")

st.divider()

st.subheader("🎬 K-drama as Cultural Export")

drama_data = pd.DataFrame({
    "Drama": ["Squid Game", "The Glory", "Crash Landing on You", "Kingdom"],
    "Global Impact": [10, 9, 9, 8],
    "Main Strength": [
        "Global streaming breakthrough",
        "Strong storytelling and social themes",
        "Romance and cross-border appeal",
        "Genre expansion"
    ]
})

st.dataframe(drama_data, use_container_width=True)

st.bar_chart(
    drama_data.set_index("Drama")["Global Impact"]
)

st.caption(
    "Scores are approximate and reflect global reach (streaming popularity), cultural impact, and storytelling innovation."
)

st.success("""
K-drama strengthens Korea’s soft power by making Korean language, lifestyle, fashion, food, and social themes more visible worldwide.
""")

st.divider()

st.subheader("🌍 Korean-built Global Groups")

global_groups = pd.DataFrame({
    "Group": ["NiziU", "&TEAM", "WayV", "GIRLSET"],
    "Target Market": ["Japan", "Japan", "China", "USA"],
    "Company": ["JYP", "HYBE", "SM", "JYP"],
    "Meaning": [
        "Japanese group built with Korean idol system",
        "Japan-focused group under Korean company system",
        "China-focused group built under SM/NCT system",
        "US-focused group using K-pop training model"
    ]
})

st.dataframe(global_groups, use_container_width=True)

st.info("""
This shows that Korea is not only exporting Korean artists.

It is exporting the production method itself:
training, concept planning, performance design, marketing, and fandom management.
""")

st.divider()

st.subheader("📊 Cultural Export Simulator")

music = st.slider("Music Influence", 0, 10, 9)
drama = st.slider("Drama Influence", 0, 10, 9)
global_groups_score = st.slider("Global Group Strategy", 0, 10, 8)
platform = st.slider("Digital Platform Power", 0, 10, 9)

culture_score = (
    music * 0.3 +
    drama * 0.3 +
    global_groups_score * 0.2 +
    platform * 0.2
)

st.metric("Korean Entertainment Power Score", round(culture_score, 2))

if culture_score >= 8:
    st.success("Strong cultural export system: music, drama, global groups, and platforms work together effectively.")
elif culture_score >= 6:
    st.info("Moderate cultural export system: strong influence exists, but some areas may need further development.")
else:
    st.warning("Limited cultural export system: influence may depend too much on one area.")

st.caption(
    "This simplified score shows how multiple cultural industries combine to create global influence."
)

if "module_scores" not in st.session_state:
    st.session_state["module_scores"] = {}

st.session_state["module_scores"]["Culture"] = culture_score

st.caption(f"Saved score: {st.session_state['module_scores']}")

st.divider()

st.subheader("🧠 Key Takeaway")

st.info("""
Korea’s entertainment power is not limited to K-pop.

It is a system made of:

- 🎤 K-pop
- 🎬 K-drama
- 🌍 Global idol production
- 📱 Digital platforms
- 💬 Global fandoms

👉 The real strength is not one song, one group, or one company.  
👉 The real strength is the system behind them.
""")    "https://www.youtube.com/watch?v=I3dezFzsNss"
)

st.caption("K-pop is only one part of South Korea’s wider cultural export system.")

st.divider()

st.subheader("🧠 Entertainment System Explorer")

selected_area = st.selectbox(
    "Choose an area to explore",
    [
        "K-pop Industry",
        "K-drama Global Impact",
        "Korean-built Global Groups",
        "Entertainment as Soft Power"
    ]
)

entertainment_map = {
    "K-pop Industry": {
        "meaning": "K-pop is built through training systems, company strategy, digital platforms, and global fandom.",
        "insight": "K-pop is not just music. It is an industrial system."
    },
    "K-drama Global Impact": {
        "meaning": "K-dramas reach global audiences through streaming platforms and strong storytelling.",
        "insight": "K-drama expands Korea’s cultural influence beyond music."
    },
    "Korean-built Global Groups": {
        "meaning": "Korean companies create groups targeting Japan, China, the US, and other markets.",
        "insight": "Korea exports not only artists, but also the idol production model."
    },
    "Entertainment as Soft Power": {
        "meaning": "Entertainment strengthens Korea’s image, tourism, language interest, and brand value.",
        "insight": "Cultural exports turn national image into global influence."
    }
}

selected = entertainment_map[selected_area]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>📌 What It Means</h3>
        <p>{selected["meaning"]}</p >
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>💡 Insight</h3>
        <p>{selected["insight"]}</p >
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("🎶 K-pop Company System")

kpop_companies = pd.DataFrame({
    "Company": ["HYBE", "SM", "JYP", "YG", "Others"],
    "System Strength": [10, 10, 9, 9, 7],
    "Global Strategy": [10, 9, 9, 8, 6],
    "Key Feature": [
        "Global fandom and platform strategy",
        "Training system and concept design",
        "Performance and global group production",
        "Branding and hip-hop influence",
        "Diverse independent and mid-size labels"
    ]
})

st.dataframe(kpop_companies, use_container_width=True)

st.bar_chart(
    kpop_companies.set_index("Company")[["System Strength", "Global Strategy"]]
)

st.caption(
    "Scores are indicative and based on industry influence, global market reach, and company system strength."
)

st.info("""
K-pop is often associated with the Big 4 companies, but the wider ecosystem also includes mid-size agencies, producers, choreographers, stylists, platforms, and fandom communities.
""")

st.divider()

st.subheader("🎬 K-drama as Cultural Export")

drama_data = pd.DataFrame({
    "Drama": ["Squid Game", "The Glory", "Crash Landing on You", "Kingdom"],
    "Global Impact": [10, 9, 9, 8],
    "Main Strength": [
        "Global streaming breakthrough",
        "Strong storytelling and social themes",
        "Romance and cross-border appeal",
        "Genre expansion"
    ]
})

st.dataframe(drama_data, use_container_width=True)

st.bar_chart(
    drama_data.set_index("Drama")["Global Impact"]
)

st.caption(
    "Scores are approximate and reflect global reach (streaming popularity), cultural impact, and storytelling innovation."
)

st.success("""
K-drama strengthens Korea’s soft power by making Korean language, lifestyle, fashion, food, and social themes more visible worldwide.
""")

st.divider()

st.subheader("🌍 Korean-built Global Groups")

global_groups = pd.DataFrame({
    "Group": ["NiziU", "&TEAM", "WayV", "GIRLSET"],
    "Target Market": ["Japan", "Japan", "China", "USA"],
    "Company": ["JYP", "HYBE", "SM", "JYP"],
    "Meaning": [
        "Japanese group built with Korean idol system",
        "Japan-focused group under Korean company system",
        "China-focused group built under SM/NCT system",
        "US-focused group using K-pop training model"
    ]
})

st.dataframe(global_groups, use_container_width=True)

st.info("""
This shows that Korea is not only exporting Korean artists.

It is exporting the production method itself:
training, concept planning, performance design, marketing, and fandom management.
""")

st.divider()

st.subheader("📊 Cultural Export Simulator")

music = st.slider("Music Influence", 0, 10, 9)
drama = st.slider("Drama Influence", 0, 10, 9)
global_groups_score = st.slider("Global Group Strategy", 0, 10, 8)
platform = st.slider("Digital Platform Power", 0, 10, 9)

culture_score = (
    music * 0.3 +
    drama * 0.3 +
    global_groups_score * 0.2 +
    platform * 0.2
)

st.metric("Korean Entertainment Power Score", round(culture_score, 2))

if culture_score >= 8:
    st.success("Strong cultural export system: music, drama, global groups, and platforms work together effectively.")
elif culture_score >= 6:
    st.info("Moderate cultural export system: strong influence exists, but some areas may need further development.")
else:
    st.warning("Limited cultural export system: influence may depend too much on one area.")

st.caption(
    "This simplified score shows how multiple cultural industries combine to create global influence."
)

if "module_scores" not in st.session_state:
    st.session_state["module_scores"] = {}

st.session_state["module_scores"]["Culture"] = culture_score

st.caption(f"Saved score: {st.session_state['module_scores']}")

st.divider()

st.subheader("🧠 Key Takeaway")

st.info("""
Korea’s entertainment power is not limited to K-pop.

It is a system made of:

- 🎤 K-pop
- 🎬 K-drama
- 🌍 Global idol production
- 📱 Digital platforms
- 💬 Global fandoms

👉 The real strength is not one song, one group, or one company.  
👉 The real strength is the system behind them.
""")
