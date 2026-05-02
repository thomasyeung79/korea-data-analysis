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
    page_title="Sports",
    page_icon="🏅",
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

st.title("🏅 South Korea in Global Sports")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

show_optional_music(
    "Power",
    "EXO",
    "https://www.youtube.com/watch?v=sGRv8ZBLuW0",
    start=55
)

st.caption(
    "Sport is another important part of Korea’s global visibility and national soft power."
)

st.markdown("""
## Overview

Korea is not only strong in football.  
It has also built global visibility through Olympic sports, combat sports, baseball, golf, and esports.
""")

st.divider()

st.subheader("🧠 Sports Perception Check")

question = st.selectbox(
    "What do you think about Korean sports?",
    [
        "Korea is only strong in football",
        "Korea is not a major sports country",
        "Korea only performs well in Asia",
        "Korea relies on a few star players"
    ]
)

analysis_map = {
    "Korea is only strong in football": {
        "answer": "Korea is strong in multiple sports including archery, baseball, golf, and short track speed skating.",
        "insight": "Football is just the most visible sport globally."
    },
    "Korea is not a major sports country": {
        "answer": "Korea consistently ranks highly in Olympic medal tables relative to its population.",
        "insight": "Korea is a high-efficiency sports nation."
    },
    "Korea only performs well in Asia": {
        "answer": "Korean athletes compete and succeed globally, especially in Europe and international tournaments.",
        "insight": "Korea is globally competitive, not regionally limited."
    },
    "Korea relies on a few star players": {
        "answer": "While stars like Son Heung-min are famous, Korea has a broad pipeline of athletes.",
        "insight": "The system produces talent continuously."
    }
}

selected = analysis_map[question]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>📌 Reality</h3>
        <p>{selected["answer"]}</p >
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

st.subheader("🏅 Multi-Sport Strength")

sports_data = pd.DataFrame({
    "Sport": ["Football", "Archery", "Baseball", "Golf", "Speed Skating"],
    "Global Level (0-10)": [9, 10, 9, 9, 10]
})

st.dataframe(sports_data, use_container_width=True)

col1, col2, col3 = st.columns(3)

col1.metric("Archery", "10")
col2.metric("Speed Skating", "10")
col3.metric("Football", "9")

st.caption(
    "These scores are conceptual and based on general global performance trends, "
    "including Olympic results, professional leagues, and international competitions."
)

st.info("""
Korea’s sports strength is diversified, not concentrated in a single field.
""")

st.divider()

st.subheader("⚽ Korean Football Global Impact")

football_data = pd.DataFrame({
    "Category": [
        "Premier League Players",
        "European League Players",
        "World Cup Performance",
        "Youth Development"
    ],
    "Score (0-10)": [9, 9, 8, 9]
})

st.dataframe(football_data, use_container_width=True)

st.bar_chart(
    football_data.set_index("Category")["Score (0-10)"]
)

st.caption(
    "These scores are conceptual and based on general global performance trends, "
    "including league presence, international tournaments, and player distribution."
)

st.success("""
Korea is one of the most globally integrated Asian football systems.
""")

st.divider()

st.subheader("🌏 East Asia Sports Comparison")

comparison = pd.DataFrame({
    "Country": ["Korea", "Japan", "China"],
    "Olympic Efficiency": [9, 8, 7],
    "Global Athlete Presence": [9, 8, 7],
    "Football Integration": [9, 8, 6]
})

st.dataframe(comparison, use_container_width=True)

st.bar_chart(
    comparison.set_index("Country")
)

st.caption(
    "Scores are conceptual and based on broad indicators such as Olympic performance, "
    "international athlete presence, football development, and global sports visibility."
)

st.info("""
This comparison is not saying one country is absolutely better than another.  
It shows different sports-system strengths:

- Korea: efficiency + global integration
- Japan: stability + infrastructure depth
- China: scale + Olympic investment
""")

st.divider()

st.subheader("🧠 Comparison Insight Engine")

selected_country = st.selectbox(
    "Choose a country to analyse",
    ["South Korea", "Japan", "China"]
)

country_insights = {
    "Korea": {
        "strength": "Efficiency + global integration",
        "explanation": "Korea performs strongly relative to its population size and has high visibility in global football, Olympic sports, golf, and esports."
    },
    "Japan": {
        "strength": "Stability + infrastructure depth",
        "explanation": "Japan has a broad and stable sports system, strong domestic leagues, and consistent international performance across many sports."
    },
    "China": {
        "strength": "Scale + Olympic investment",
        "explanation": "China benefits from population scale, state-backed sports development, and strong Olympic medal performance."
    }
}

selected = country_insights[selected_country]

col1, col2 = st.columns(2)

with col1:
    st.success(f"""
### Main Strength

{selected["strength"]}
""")

with col2:
    st.info(f"""
### Explanation

{selected["explanation"]}
""")

st.divider()

st.subheader("⚖️ Who Leads in What?")

metric = st.selectbox(
    "Select a sports dimension",
    ["Olympic Efficiency", "Global Athlete Presence", "Football Integration"]
)

leaders = {
    "Olympic Efficiency": "Korea",
    "Global Athlete Presence": "Korea",
    "Football Integration": "Korea"
}

st.metric("Current Leader", leaders[metric])

st.caption(
    "This leadership result follows the conceptual scores in the comparison table above."
)

st.subheader("📊 Sports Power Simulator")

football = st.slider("Football Strength", 0, 10, 9)
olympic = st.slider("Olympic Strength", 0, 10, 9)
global_players = st.slider("Global Players", 0, 10, 9)
diversity = st.slider("Sport Diversity", 0, 10, 9)

score = (
    football * 0.3 +
    olympic * 0.3 +
    global_players * 0.2 +
    diversity * 0.2
)

st.metric("Korean Sports Power Score", round(score, 2))

if score >= 9:
    st.success("Top-tier sports profile: Korea combines Olympic efficiency, football visibility, global athletes, and sport diversity.")
elif score >= 7:
    st.info("Strong sports profile: Korea shows broad competitiveness, especially in Olympic sports and football.")
else:
    st.warning("Limited sports profile: Korea may rely too much on specific sports or individual stars.")

st.caption(
    "This model shows how multiple sports contribute to overall national strength."
)

st.divider()

st.subheader("🧠 Final Insight")

st.info("""
Korea is not just a football country.

It is a **multi-sport system** with:

- Olympic dominance (archery, skating)
- Strong global football presence
- Professional leagues (baseball, golf)
- Efficient talent development

👉 Korea’s strength is not size.  
👉 It is system efficiency.
""")
