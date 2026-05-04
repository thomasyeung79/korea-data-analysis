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
    page_title="Understanding South Korea",
    page_icon="🌏",
    layout="wide"
)

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

.card h3 {
    margin-top: 0;
}

.small-text {
    color: #666;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 8])

with col_flag:
    st.image("south_korea.jpg", width=90)

with col_title:
    st.title("Understanding South Korea Through Data")

st.caption(
    "A data-driven project exploring South Korea beyond stereotypes."
)

st.markdown("""
<div style="
    background-color:#f8f9fa;
    padding:20px;
    border-radius:12px;
    border-left:5px solid #0d6efd;
">
South Korea is often seen through simple labels:

- K-pop  
- Technology  
- Economic growth  

👉 But what actually drives its global influence?

This project explores Korea as a <strong>system</strong> across history, economy, technology, culture, sports, society, and tourism.
</div>
""", unsafe_allow_html=True)

st.caption("In this project, 'Korea' refers to South Korea unless otherwise specified.")

st.divider()

show_optional_music(
    "Into The New World",
    "Girls' Generation",
    "https://www.youtube.com/watch?v=0k2Zzkw_-0I",
    start=20
)

st.markdown("## 🚀 Enter the Experience")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📜 History</h3>
        <p class="small-text">Explore Korea’s historical path from state formation to globalisation.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open History", use_container_width=True):
        st.switch_page("pages/1_History.py")

with col2:
    st.markdown("""
    <div class="card">
        <h3>📊 Analysis</h3>
        <p class="small-text">Compare perception with data across economy, innovation, and social pressure.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Analysis", use_container_width=True):
        st.switch_page("pages/2_Analysis.py")

with col3:
    st.markdown("""
    <div class="card">
        <h3>💻 Technology</h3>
        <p class="small-text">Understand Korea’s hard power through semiconductors, digital systems, and global expansion.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Technology", use_container_width=True):
        st.switch_page("pages/3_Technology.py")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="card">
        <h3>🎤 Culture</h3>
        <p class="small-text">Explore K-pop, K-drama, global idol systems, and cultural export power.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Culture", use_container_width=True):
        st.switch_page("pages/4_Kpop.py")

with col5:
    st.markdown("""
    <div class="card">
        <h3>⚽ Sports</h3>
        <p class="small-text">See how Korean athletes contribute to global visibility and national soft power.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Sports", use_container_width=True):
        st.switch_page("pages/5_Sports.py")

with col6:
    st.markdown("""
    <div class="card">
        <h3>🧠 Society</h3>
        <p class="small-text">Understand Korean daily life through pressure, work, lifestyle, and social systems.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Society", use_container_width=True):
        st.switch_page("pages/6_Society.py")

col7, col8 = st.columns(2)

with col7:
    st.markdown("""
    <div class="card">
        <h3>✈️ Tourism</h3>
        <p class="small-text">Experience Korea through travel perception, lifestyle, regional diversity, and accessibility.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Tourism", use_container_width=True):
        st.switch_page("pages/7_Tourism.py")

with col8:
    st.markdown("""
    <div class="card">
        <h3>🏁 Final Evaluation</h3>
        <p class="small-text">Integrate all modules into a system-level conclusion and reflection.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Final Evaluation", use_container_width=True):
        st.switch_page("pages/8_Ending.py")

st.markdown("---")

st.success("""
Version 2.0 expands the project into a full Korea System Analysis Platform:

History → Analysis → Technology → Culture → Sports → Society → Tourism → Final Evaluation
""")

st.subheader("📈 System Data")

st.caption("View saved user perception data and AI insights.")

if st.button("Open User History", use_container_width=True):
    st.switch_page("pages/9_User_History.py")
