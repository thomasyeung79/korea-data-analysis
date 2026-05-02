import streamlit as st

st.markdown("""
<style>
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

st.set_page_config(
    page_title="Understanding South Korea",
    page_icon="🌏",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

col_flag, col_title = st.columns([1, 8])

with col_flag:
    st.image("south_korea.jpg", width=90)

with col_title:
    st.title("Understanding South Korea Through Data")

st.caption(
    "A cross-cultural data project exploring South Korea beyond stereotypes."
)

st.markdown("## 🚀 Enter the Experience")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📜 History</h3>
        <p class="small-text">Explore Korea’s historical path from modern state formation to globalisation.</p >
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
        <h3>🎤 K-pop</h3>
        <p class="small-text">Understand K-pop as a global cultural and industrial system.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open K-pop", use_container_width=True):
        st.switch_page("pages/3_Kpop.py")

col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div class="card">
        <h3>⚽ Sports</h3>
        <p class="small-text">See how Korean athletes and footballers contribute to global visibility.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Sports", use_container_width=True):
        st.switch_page("pages/4_Sports.py")

with col5:
    st.markdown("""
    <div class="card">
        <h3>🏁 Final Evaluation</h3>
        <p class="small-text">Use a simple scoring model to summarise South Korea’s overall profile.</p >
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Ending", use_container_width=True):
        st.switch_page("pages/5_Ending.py")

st.markdown("---")

st.info("""
Version 1.0 focuses on structure, storytelling, and core analysis.  
Version 2.0 can add deeper datasets, stronger visual design, and expanded country comparison.
""")