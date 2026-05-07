import pandas as pd
import streamlit as st
from pathlib import Path
from openai import OpenAI

client = OpenAI()

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
    page_title="Football Analytics",
    page_icon="⚽",
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

st.title("⚽ East Asian Football Pathway Analytics")

st.caption(
    "A football analytics module comparing China, Japan, and Korea through Premier League and UEFA Champions League player pathways."
)

if st.button("🏠 Back to Sports"):
    st.switch_page("pages/5_Sports.py")

st.divider()

show_optional_music(
    "Victory Korea",
    "Super Junior",
    "https://www.youtube.com/watch?v=vugcXCEaQsI"
)

BASE_DIR = Path(__file__).resolve().parents[1]

epl_paths = [
    BASE_DIR / "east_asian_epl_appearances.csv",
    BASE_DIR / "data" / "east_asian_epl_appearances.csv"
]

epl_path = next((p for p in epl_paths if p.exists()), None)

if epl_path is None:
    st.error("EPL CSV not found. Put east_asian_epl_appearances.csv in project root or data folder.")
    st.stop()

epl_df = pd.read_csv(epl_path)

epl_required_cols = [
    "player_name",
    "country",
    "player_type",
    "club",
    "competition_type"
]

missing_epl_cols = [col for col in epl_required_cols if col not in epl_df.columns]

if missing_epl_cols:
    st.error(f"EPL data missing columns: {missing_epl_cols}")
    st.stop()

BIG6 = [
    "Manchester United",
    "Manchester City",
    "Liverpool",
    "Arsenal",
    "Chelsea",
    "Tottenham Hotspur"
]

epl_df["big6"] = epl_df["club"].isin(BIG6)

korea_epl_df = epl_df[epl_df["country"] == "Korea"]


ucl_paths = [
    BASE_DIR / "east_asia_ucl_players_dataset_checked_split_by_club.csv",
    BASE_DIR / "data" / "east_asia_ucl_players_dataset_checked_split_by_club.csv"
]

ucl_path = next((p for p in ucl_paths if p.exists()), None)

if ucl_path is None:
    st.warning("UCL CSV file not found. UCL tab will not be available.")
    ucl_df = pd.DataFrame()
else:
    ucl_df = pd.read_csv(ucl_path)

    ucl_required_cols = [
        "country",
        "player_name",
        "club",
        "ucl_status",
        "first_ucl_season",
        "last_ucl_season",
        "confidence",
        "notes",
        "source_url"
    ]

    missing_ucl_cols = [col for col in ucl_required_cols if col not in ucl_df.columns]

    if missing_ucl_cols:
        st.warning(f"UCL data missing columns: {missing_ucl_cols}")
        ucl_df = pd.DataFrame()

if not ucl_df.empty:
    korea_ucl_df = ucl_df[ucl_df["country"] == "Korea"]
else:
    korea_ucl_df = pd.DataFrame()

def generate_next_star_analysis(
    player_name,
    age,
    position,
    current_club,
    speed,
    finishing,
    work_rate,
    tactical_discipline,
    physicality,
    marketability,
    european_readiness
):
    prompt = f"""
You are a football pathway analyst.

Analyse whether the following Korean player is closer to:
1. Park Ji-sung pathway
2. Son Heung-min pathway
3. or a different pathway

Player profile:
- Name: {player_name}
- Age: {age}
- Position: {position}
- Current club: {current_club}
- Speed: {speed}/10
- Finishing: {finishing}/10
- Work rate: {work_rate}/10
- Tactical discipline: {tactical_discipline}/10
- Physicality: {physicality}/10
- Marketability: {marketability}/10
- European readiness: {european_readiness}/10

Park Ji-sung model:
- tactical discipline
- work rate
- big-club adaptability
- team-first role
- Champions League-level system player

Son Heung-min model:
- elite attacking output
- speed
- finishing
- Premier League suitability
- global star power

Return a concise analysis with:
- closest pathway
- EPL potential score
- UCL potential score
- strengths
- risks
- final recommendation
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text

def show_epl_metrics(data):
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Unique Players", data["player_name"].nunique())
    col2.metric("Club Records", len(data))
    col3.metric("Countries", data["country"].nunique())
    col4.metric("Clubs", data["club"].nunique())
    col5.metric(
        "League Records",
        len(data[data["competition_type"] == "League"])
    )

def show_ucl_metrics(data):
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Unique Players", data["player_name"].nunique())
    col2.metric("Club Records", len(data))
    col3.metric("Countries", data["country"].nunique())
    col4.metric("Clubs", data["club"].nunique())
    col5.metric(
        "Appeared Records",
        len(data[data["ucl_status"].str.lower() == "appeared"])
    )

def generate_system_insight(epl_data, ucl_data):
    epl_top_country = epl_data["country"].value_counts().idxmax()
    epl_players = epl_data["player_name"].nunique()
    epl_big6_players = epl_data[epl_data["big6"]]["player_name"].nunique()

    if not ucl_data.empty:
        ucl_top_country = ucl_data["country"].value_counts().idxmax()
        ucl_players = ucl_data["player_name"].nunique()
        appeared_players = ucl_data[ucl_data["ucl_status"].str.lower() == "appeared"]["player_name"].nunique()
    else:
        ucl_top_country = "N/A"
        ucl_players = 0
        appeared_players = 0

    return f"""
## 🧠 East Asian Elite Football Pathway Insight

### 📊 EPL Layer
- Top represented EPL country: **{epl_top_country}**
- Unique EPL-related players: **{epl_players}**
- Players with Big 6 experience: **{epl_big6_players}**

### 🏆 UCL Layer
- Top represented UCL country: **{ucl_top_country}**
- Unique UCL-related players: **{ucl_players}**
- Players with confirmed UCL appearances: **{appeared_players}**

### 💡 Interpretation
The Premier League and UEFA Champions League measure different forms of elite football integration.

- **Premier League** shows access to the most commercial and visible domestic league system.
- **UEFA Champions League** shows entry into Europe’s highest competitive club platform.
- **Big 6 experience** shows access to elite club infrastructure and global media visibility.

### 🇰🇷 Korea Focus
Korea is the main focus of this project because the wider system is a Korea analytics platform.

China and Japan are used as comparison groups, while Korea is analysed as the central case of global football export.

### 🎯 Strategic Insight
East Asian football export is not only about producing players.

The real question is:

**Can a football system consistently produce players who enter elite clubs, earn real minutes, and remain competitive in top European environments?**
"""

tabs = st.tabs([
    "🌏 EPL Overview",
    "🇰🇷 Korea Focus",
    "🏆 EPL Big 6",
    "⭐ UCL Analysis",
    "🔍 Player Explorer",
    "🔮 Next Korean Star",
    "🧠 Insight"
])

with tabs[0]:
    st.subheader("🌏 East Asia EPL Overview")

    st.markdown("""
This section compares China, Japan, and Korea through Premier League player records.

The analysis separates:

- **League**: players with Premier League appearances
- **Cup Only**: players who played only in cup competitions
- **No Appearance**: players registered with clubs but did not appear

This avoids treating all club records as equal.
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_country = st.multiselect(
            "Country",
            options=sorted(epl_df["country"].unique()),
            default=sorted(epl_df["country"].unique())
        )

    with col2:
        selected_player_type = st.multiselect(
            "Player Type",
            options=sorted(epl_df["player_type"].unique()),
            default=sorted(epl_df["player_type"].unique())
        )

    with col3:
        selected_competition_type = st.multiselect(
            "Competition Type",
            options=sorted(epl_df["competition_type"].unique()),
            default=sorted(epl_df["competition_type"].unique())
        )

    filtered_epl_df = epl_df[
        (epl_df["country"].isin(selected_country)) &
        (epl_df["player_type"].isin(selected_player_type)) &
        (epl_df["competition_type"].isin(selected_competition_type))
    ]

    if filtered_epl_df.empty:
        st.warning("No EPL data available for the selected filters.")
        st.stop()

    show_epl_metrics(filtered_epl_df)

    st.divider()

    st.subheader("📋 Filtered EPL Dataset")
    st.dataframe(
        filtered_epl_df.sort_values(by=["country", "player_name", "club"]),
        use_container_width=True
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🌏 Country Distribution")
        st.bar_chart(
            filtered_epl_df.drop_duplicates("player_name")["country"].value_counts()
        )

    with col_b:
        st.subheader("🏟️ Club Distribution")
        st.bar_chart(filtered_epl_df["club"].value_counts())

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("🧬 Player Type")
        st.bar_chart(
            filtered_epl_df.drop_duplicates("player_name")["player_type"].value_counts()
        )

    with col_d:
        st.subheader("🏟️ Competition Type")
        st.bar_chart(filtered_epl_df["competition_type"].value_counts())

with tabs[1]:
    st.subheader("🇰🇷 Korea Focus: Elite Football Pathway")

    st.info("""
Korea is the main focus of this module because the wider project is a Korea analytics system.

The East Asia comparison is used as evidence, while this section explains how Korean football connects to global football pathways.
""")

    st.markdown("## ⚽ Korean EPL Pathway")

    if korea_epl_df.empty:
        st.warning("No Korean EPL records available.")
    else:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Korean EPL Players", korea_epl_df["player_name"].nunique())
        col2.metric("EPL Club Records", len(korea_epl_df))
        col3.metric("EPL Clubs", korea_epl_df["club"].nunique())
        col4.metric(
            "Big 6 Players",
            korea_epl_df[korea_epl_df["big6"]]["player_name"].nunique()
        )

        st.dataframe(
            korea_epl_df.sort_values(by=["player_name", "club"]),
            use_container_width=True
        )

        st.subheader("🏟️ Korean EPL Club Distribution")
        st.bar_chart(korea_epl_df["club"].value_counts())

    st.divider()

    st.markdown("## ⭐ Korean UCL Pathway")

    if korea_ucl_df.empty:
        st.warning("No Korean UCL records available.")
    else:
        show_ucl_metrics(korea_ucl_df)

        st.dataframe(
            korea_ucl_df.sort_values(by=["player_name", "club"]),
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Korean UCL Status")
            st.bar_chart(korea_ucl_df["ucl_status"].value_counts())

        with col2:
            st.subheader("🏟️ Korean UCL Clubs")
            st.bar_chart(korea_ucl_df["club"].value_counts())

    st.divider()

    st.subheader("🧠 Korea Football System Insight")

    st.success("""
Korea's football export system is built on:

- youth development
- early overseas exposure
- tactical adaptability
- physical competitiveness
- elite player visibility
- European club pathway experience

EPL records show Korea's ability to place players into a highly competitive domestic league.

UCL records show whether Korean players entered the highest competitive club platform in Europe.
""")

with tabs[2]:
    st.subheader("🏆 EPL Big 6 Analysis")

    st.markdown("""
Big 6 experience is used as an elite-club indicator.

It does not mean every player became a regular starter, but it shows whether a player entered the highest-profile club environment in English football.
""")

    big6_summary = pd.crosstab(
        epl_df["country"],
        epl_df["big6"]
    )

    st.dataframe(big6_summary, use_container_width=True)

    st.subheader("Players with Big 6 Experience")

    big6_players = epl_df[epl_df["big6"] == True]

    if big6_players.empty:
        st.info("No Big 6 player records available.")
    else:
        st.dataframe(
            big6_players.sort_values(by=["country", "player_name", "club"]),
            use_container_width=True
        )

with tabs[3]:
    st.subheader("⭐ UEFA Champions League Analysis")

    if ucl_df.empty:
        st.warning("UCL dataset is not available.")
    else:
        st.markdown("""
This section compares China, Japan, and Korea through UEFA Champions League records.

The key distinction is:

- **appeared**: player had confirmed UCL appearance
- **registered_only**: player was registered or associated but did not have confirmed appearance

This separates real elite competition participation from squad registration.
""")

        col1, col2, col3 = st.columns(3)

        with col1:
            selected_ucl_country = st.multiselect(
                "UCL Country",
                options=sorted(ucl_df["country"].unique()),
                default=sorted(ucl_df["country"].unique())
            )

        with col2:
            selected_ucl_status = st.multiselect(
                "UCL Status",
                options=sorted(ucl_df["ucl_status"].unique()),
                default=sorted(ucl_df["ucl_status"].unique())
            )

        with col3:
            selected_confidence = st.multiselect(
                "Confidence",
                options=sorted(ucl_df["confidence"].dropna().unique()),
                default=sorted(ucl_df["confidence"].dropna().unique())
            )

        filtered_ucl_df = ucl_df[
            (ucl_df["country"].isin(selected_ucl_country)) &
            (ucl_df["ucl_status"].isin(selected_ucl_status)) &
            (ucl_df["confidence"].isin(selected_confidence))
        ]

        if filtered_ucl_df.empty:
            st.warning("No UCL data available for the selected filters.")
            st.stop()

        show_ucl_metrics(filtered_ucl_df)

        st.divider()

        st.subheader("📋 Filtered UCL Dataset")
        st.dataframe(
            filtered_ucl_df.sort_values(by=["country", "player_name", "club"]),
            use_container_width=True
        )

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("🌏 UCL Country Distribution")
            st.bar_chart(
                filtered_ucl_df.drop_duplicates("player_name")["country"].value_counts()
            )

        with col_b:
            st.subheader("🏆 UCL Status")
            st.bar_chart(filtered_ucl_df["ucl_status"].value_counts())

        col_c, col_d = st.columns(2)

        with col_c:
            st.subheader("🏟️ UCL Club Distribution")
            st.bar_chart(filtered_ucl_df["club"].value_counts())

        with col_d:
            st.subheader("✅ Confidence Level")
            st.bar_chart(filtered_ucl_df["confidence"].value_counts())

        st.info("""
### 💡 UCL Insight

The UEFA Champions League represents the highest competitive club level in Europe.

Compared with the Premier League, UCL participation shows a different layer of elite football integration:

- EPL = commercial league pathway
- UCL = elite European competition pathway
- Big 6 = top-club access indicator
""")

with tabs[4]:
    st.subheader("🔍 Player Explorer")

    dataset_choice = st.radio(
        "Choose Dataset",
        ["EPL", "UCL"],
        horizontal=True
    )

    if dataset_choice == "EPL":
        selected_country = st.selectbox(
            "Choose Country",
            options=["All"] + sorted(epl_df["country"].unique())
        )

        explorer_df = epl_df.copy() if selected_country == "All" else epl_df[epl_df["country"] == selected_country]

        selected_player = st.selectbox(
            "Select Player",
            options=sorted(explorer_df["player_name"].unique())
        )

        player_df = explorer_df[explorer_df["player_name"] == selected_player]

        st.dataframe(player_df, use_container_width=True)

        clubs = ", ".join(player_df["club"].unique())
        country = player_df["country"].iloc[0]
        competition_types = ", ".join(player_df["competition_type"].unique())

        st.success(f"""
**{selected_player}** represented **{country}** and had Premier League club experience with:

**{clubs}**

Competition record type:

**{competition_types}**
""")

    else:
        if ucl_df.empty:
            st.warning("UCL dataset is not available.")
        else:
            selected_country = st.selectbox(
                "Choose Country",
                options=["All"] + sorted(ucl_df["country"].unique())
            )

            explorer_df = ucl_df.copy() if selected_country == "All" else ucl_df[ucl_df["country"] == selected_country]

            selected_player = st.selectbox(
                "Select UCL Player",
                options=sorted(explorer_df["player_name"].unique())
            )

            player_df = explorer_df[explorer_df["player_name"] == selected_player]

            st.dataframe(player_df, use_container_width=True)

            clubs = ", ".join(player_df["club"].unique())
            country = player_df["country"].iloc[0]
            status = ", ".join(player_df["ucl_status"].unique())

            st.success(f"""
**{selected_player}** represented **{country}** and had UEFA Champions League records with:

**{clubs}**

UCL status:

**{status}**
""")

with tabs[5]:
    st.subheader("🔮 Next Korean Star Model")

    st.markdown("""
This section uses AI to analyse whether a Korean player is closer to the:

- **Park Ji-sung pathway**: tactical, disciplined, team-system player
- **Son Heung-min pathway**: elite attacking star with global marketability

The goal is not to predict with certainty, but to model different elite football pathways.
""")

    player_name = st.text_input("Player Name", "Yang Min-hyeok")
    age = st.number_input("Age", min_value=15, max_value=40, value=18)
    position = st.selectbox(
        "Position",
        ["Forward", "Winger", "Midfielder", "Defender", "Goalkeeper"]
    )
    current_club = st.text_input("Current Club", "Tottenham Hotspur")

    col1, col2 = st.columns(2)

    with col1:
        speed = st.slider("Speed", 0, 10, 8)
        finishing = st.slider("Finishing", 0, 10, 7)
        work_rate = st.slider("Work Rate", 0, 10, 8)
        tactical_discipline = st.slider("Tactical Discipline", 0, 10, 7)

    with col2:
        physicality = st.slider("Physicality", 0, 10, 7)
        marketability = st.slider("Global Marketability", 0, 10, 7)
        european_readiness = st.slider("European Readiness", 0, 10, 7)

    park_score = (
        work_rate * 0.3 +
        tactical_discipline * 0.3 +
        physicality * 0.2 +
        european_readiness * 0.2
    )

    son_score = (
        finishing * 0.3 +
        speed * 0.25 +
        marketability * 0.25 +
        european_readiness * 0.2
    )

    col_a, col_b = st.columns(2)

    col_a.metric("Park Ji-sung Pathway Score", round(park_score, 2))
    col_b.metric("Son Heung-min Pathway Score", round(son_score, 2))

    if son_score > park_score:
        st.success(f"{player_name} is closer to the Son Heung-min pathway.")
    elif park_score > son_score:
        st.success(f"{player_name} is closer to the Park Ji-sung pathway.")
    else:
        st.info(f"{player_name} shows a balanced profile between both pathways.")

    if st.button("🤖 Generate AI Star Potential Analysis"):
        with st.spinner("Analysing player pathway..."):
            result = generate_next_star_analysis(
                player_name,
                age,
                position,
                current_club,
                speed,
                finishing,
                work_rate,
                tactical_discipline,
                physicality,
                marketability,
                european_readiness
            )

            st.markdown(result)

with tabs[6]:
    st.subheader("🧠 System Insight")

    st.markdown(generate_system_insight(epl_df, ucl_df))

    st.divider()

    st.subheader("📌 Data Notes")

    st.write("""
- EPL data includes players registered with Premier League clubs.
- EPL competition types: League / Cup Only / No Appearance.
- UCL data includes player-club records split by club.
- UCL status separates confirmed appearances from registration-only records.
- Korea is treated as the main project focus, while China and Japan are used for East Asian comparison.
""")
