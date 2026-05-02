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
    "Into The New World",
    "Girls' Generation",
    "https://www.youtube.com/watch?v=0k2Zzkw_-0I",
    start=20
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

st.subheader("📌 What This Project Shows")

st.markdown("""
Across all modules:

- 📜 History → Rapid transformation  
- 📊 Analysis → High-efficiency system  
- 💻 Technology → Industrial and digital foundation  
- 🎤 Culture → Cultural export system  
- ⚽ Sports → Global competitiveness  
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
