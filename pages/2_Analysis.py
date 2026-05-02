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
    page_title="Analysis",
    page_icon="📊",
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

st.title("📊 Understanding Korea Through Data")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

show_optional_music(
    "Next Level",
    "aespa",
    "https://www.youtube.com/watch?v=4TWR90KJl84",
    start=7
)

st.caption("Combining regional comparison, historical transformation, and interactive analysis.")

st.divider()

st.subheader("🌏 East Asia Comparison")

comparison_data = pd.DataFrame({
    "Country": ["South Korea", "Japan", "China"],
    "GDP (Trillion USD)": [1.88, 4.03, 18.74],
    "GDP per capita (USD)": [36238, 32487, 13303],
    "Innovation Rank (2024)": [6, 13, 11]
})

st.dataframe(comparison_data, use_container_width=True)

st.bar_chart(
    comparison_data.set_index("Country")[["GDP per capita (USD)"]]
)

st.info("""
South Korea has a smaller economy than China and Japan,  
but maintains strong innovation and high income levels.
""")

st.divider()

st.subheader("🚀 Before vs After the Miracle on the Han River")

miracle_data = pd.DataFrame({
    "Period": ["1960s", "2024"],
    "GDP per capita (USD)": [158, 36238],
    "Global Influence": [2, 9],
    "Industrial Strength": [2, 9],
    "Cultural Influence": [1, 10]
})

st.dataframe(miracle_data, use_container_width=True)

st.bar_chart(
    miracle_data.set_index("Period")
)

st.success("""
South Korea transformed from a low-income post-war economy  
into a high-income global economy within decades.
""")

st.divider()

st.subheader("🧠 Korea Development Insight Engine")

question = st.selectbox(
    "Choose a question",
    [
        "How did Korea transform so quickly?",
        "Is Korea stronger than its size suggests?",
        "Is Korea only strong in culture?",
        "Is Korean pressure exaggerated?",
        "What makes Korea different from China and Japan?"
    ]
)

analysis_map = {
    "How did Korea transform so quickly?": {
        "answer": "Driven by export-led industrialisation, education, and strong national planning.",
        "insight": "The Miracle on the Han River is a system-level transformation."
    },
    "Is Korea stronger than its size suggests?": {
        "answer": "Yes. Korea has high global influence in tech, culture, and sports.",
        "insight": "Influence is not determined by size, but by system efficiency."
    },
    "Is Korea only strong in culture?": {
        "answer": "No. Korea is strong in semiconductors, cars, electronics, and manufacturing.",
        "insight": "Culture is the visible layer, industry is the foundation."
    },
    "Is Korean pressure exaggerated?": {
        "answer": "Pressure exists, but similar patterns exist across East Asia.",
        "insight": "Korea is competitive, but not uniquely extreme."
    },
    "What makes Korea different from China and Japan?": {
        "answer": "A combination of high income, strong culture, and efficient systems.",
        "insight": "Korea balances hard power and soft power."
    }
}

selected = analysis_map[question]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>📌 Data-Based Answer</h3>
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

st.subheader("📊 Factor Simulator")

economy = st.slider("Economy Strength", 0, 10, 9)
innovation = st.slider("Innovation Strength", 0, 10, 9)
culture = st.slider("Culture Influence", 0, 10, 10)
pressure = st.slider("Social Pressure", 0, 10, 7)

score = (
    economy * 0.3 +
    innovation * 0.3 +
    culture * 0.3 +
    (10 - pressure) * 0.1
)

st.metric("Balanced Development Score", round(score, 2))

if score >= 8:
    st.success("Strong balanced development: Korea combines economy, innovation, culture, and manageable pressure.")
elif score >= 6:
    st.info("Moderate balanced development: Korea shows strengths, but pressure or structural limits affect the score.")
else:
    st.warning("Weak balanced development: one or more core factors may be limiting the overall profile.")

st.caption(
    "This is a simplified model showing how different factors interact."
)

st.divider()

st.subheader("🧠 Key Insight")

st.info("""
South Korea’s development is best understood through:

- Regional comparison (China, Japan, Korea)
- Historical transformation (Miracle on the Han River)
- Structural strength (industry + culture + innovation)

👉 Korea is not defined by one factor  
👉 It is a multi-dimensional system
""")

st.caption("Data sources: World Bank, WIPO Global Innovation Index 2024 (approximate values used for clarity).")
