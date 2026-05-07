import streamlit as st
import pandas as pd
from pathlib import Path

try:
    from openai import OpenAI
    client = OpenAI()
except Exception:
    client = None


st.set_page_config(
    page_title="K-pop Industry Intelligence",
    page_icon="🎤",
    layout="wide"
)


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


st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}

.card {
    padding: 1.4rem;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    background: white;
    min-height: 150px;
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


BASE_DIR = Path(__file__).resolve().parents[1]

csv_paths = [
    BASE_DIR / "kpop_data.csv",
    BASE_DIR / "kpop_data(1).csv",
    BASE_DIR / "data" / "kpop_data.csv",
    BASE_DIR / "data" / "kpop_data(1).csv"
]

csv_path = next((p for p in csv_paths if p.exists()), None)

if csv_path is None:
    st.error("kpop_data.csv not found. Please place it in the project root or data folder.")
    st.stop()

df = pd.read_csv(csv_path)

required_cols = [
    "artist_name",
    "artist_type",
    "company",
    "debut_year",
    "gender",
    "main_market",
    "secondary_market"
]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns in kpop_data.csv: {missing_cols}")
    st.stop()


def get_generation(year):
    if year <= 2003:
        return "1st Gen"
    elif year <= 2011:
        return "2nd Gen"
    elif year <= 2017:
        return "3rd Gen"
    elif year <= 2021:
        return "4th Gen"
    else:
        return "5th Gen"


BIG4 = ["SM", "JYP", "YG", "HYBE"]

df["generation"] = df["debut_year"].apply(get_generation)
df["company_group"] = df["company"].apply(lambda x: x if x in BIG4 else "Others")
df["secondary_market"] = df["secondary_market"].fillna("N/A")


GLOBAL_MAINSTREAM = [
    "BTS",
    "BLACKPINK",
    "Stray Kids",
    "TWICE",
    "SEVENTEEN",
    "aespa",
    "NewJeans"
]

CURRENT_EXPANSION = [
    "TXT",
    "ENHYPEN",
    "LE SSERAFIM",
    "IVE",
    "RIIZE",
    "BABYMONSTER",
    "NMIXX",
    "BOYNEXTDOOR",
    "TWS",
    "ILLIT",
    "ZEROBASEONE"
]

EXPERIMENTAL_GLOBAL = [
    "NiziU",
    "NEXZ",
    "&TEAM",
    "WayV",
    "KATSEYE",
    "VCHA",
    "XG"
]

HISTORICAL_MODELS = [
    "TVXQ",
    "EXO",
    "Girls' Generation",
    "SUPER JUNIOR",
    "SHINee",
    "2PM",
    "2NE1",
    "BIGBANG",
    "Wonder Girls"
]

US_GLOBAL_TARGET_GROUPS = (
    GLOBAL_MAINSTREAM
    + CURRENT_EXPANSION
    + EXPERIMENTAL_GLOBAL
)


def get_expansion_category(name):
    if name in GLOBAL_MAINSTREAM:
        return "Global Mainstream"
    elif name in CURRENT_EXPANSION:
        return "Current Expansion"
    elif name in EXPERIMENTAL_GLOBAL:
        return "Experimental Global"
    elif name in HISTORICAL_MODELS:
        return "Historical Expansion"
    else:
        return "Others"


df["expansion_category"] = df["artist_name"].apply(get_expansion_category)


def show_basic_metrics(data):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Artists", len(data))
    col2.metric("Companies", data["company"].nunique())
    col3.metric("Markets", data["main_market"].nunique())
    col4.metric("Generations", data["generation"].nunique())


def generate_industry_insight(data):
    if data.empty:
        return "No data available."

    top_company = data["company_group"].value_counts().idxmax()
    top_market = data["main_market"].value_counts().idxmax()
    top_generation = data["generation"].value_counts().idxmax()
    top_expansion = data["expansion_category"].value_counts().idxmax()

    group_ratio = round(
        len(data[data["artist_type"] == "group"]) / len(data) * 100,
        1
    )

    company_concentration = round(
        data["company_group"].value_counts(normalize=True).max() * 100,
        1
    )

    return f"""
## 📊 K-pop Industry Insight

### 🏢 Industry Structure
- Leading company group in this view: **{top_company}**
- Top company share: **{company_concentration}%**
- Group-based structure: **{group_ratio}%**

### 🌍 Market Direction
- Main market focus: **{top_market}**
- Leading generation: **{top_generation}**
- Main expansion category: **{top_expansion}**

### 💡 Interpretation
K-pop is not only a music genre.  
It is an entertainment production system built through companies, training models, concept design, fandom platforms, and global market strategy.

### 🎯 Strategic Insight
Different generations of K-pop used different expansion models:

- TVXQ: Japanese market integration
- EXO: China-focused hybrid localisation
- BTS / BLACKPINK: Western mainstream penetration
- Newer groups: global-first and platform-first expansion

The current strategic battlefield is not simply popularity.  
It is whether a group can enter the global mainstream entertainment system.
"""


def calculate_us_potential_by_company(data):
    if data.empty:
        return pd.DataFrame(columns=["company", "us_potential_score"])

    result = []

    superstar_list = [
        "BTS",
        "BLACKPINK",
        "Stray Kids",
        "NewJeans",
        "aespa"
    ]

    for company in data["company_group"].unique():
        sub = data[data["company_group"] == company]

        global_score = len(sub[sub["main_market"].isin(["Global", "USA", "US"])])
        recent_score = len(sub[sub["debut_year"] >= 2018])
        active_global_score = len(sub[sub["artist_name"].isin(US_GLOBAL_TARGET_GROUPS)])

        superstar_score = 0
        for artist in sub["artist_name"]:
            if artist in superstar_list:
                superstar_score += 5

        score = (
            global_score * 2 +
            recent_score * 1.5 +
            active_global_score * 2 +
            superstar_score * 3
        )

        result.append({
            "company": company,
            "us_potential_score": round(score, 2)
        })

    return pd.DataFrame(result).sort_values(
        "us_potential_score",
        ascending=False
    )


def predict_next_global_hit(data):
    if data.empty:
        return pd.DataFrame()

    candidates = []

    for _, row in data.iterrows():
        score = 0

        if row["debut_year"] >= 2018:
            score += 3

        if row["main_market"] in ["Global", "USA", "US"]:
            score += 4

        if row["artist_type"] == "group":
            score += 2

        if row["company_group"] in ["SM", "JYP", "YG", "HYBE"]:
            score += 2

        if row["generation"] == "5th Gen":
            score += 2

        if row["expansion_category"] == "Global Mainstream":
            score += 4
        elif row["expansion_category"] == "Current Expansion":
            score += 3
        elif row["expansion_category"] == "Experimental Global":
            score += 2

        candidates.append({
            "artist_name": row["artist_name"],
            "company": row["company"],
            "company_group": row["company_group"],
            "generation": row["generation"],
            "main_market": row["main_market"],
            "expansion_category": row["expansion_category"],
            "global_hit_score": score
        })

    return pd.DataFrame(candidates).sort_values(
        "global_hit_score",
        ascending=False
    )


def generate_us_strategy_text(
    group_name,
    us_score,
    english,
    performance,
    social_media,
    western_fit,
    fanbase
):
    if us_score >= 8:
        level = "strong"
    elif us_score >= 6:
        level = "moderate"
    else:
        level = "limited"

    return f"""
## 🇺🇸 US Market Prediction Report

### Selected Group
**{group_name}**

### US Market Potential Score
**{round(us_score, 2)} / 10**

### Market Level
This group shows **{level}** potential for the US market.

### Key Factors
- English Accessibility: **{english}/10**
- Performance Impact: **{performance}/10**
- Social Media Power: **{social_media}/10**
- Western Market Compatibility: **{western_fit}/10**
- Global Fanbase Strength: **{fanbase}/10**

### Strategic Interpretation
Japan and China are already established K-pop markets.  
The US market is different because it represents:

- mainstream Western cultural penetration
- Billboard-level visibility
- Spotify and TikTok conversion
- English-language crossover
- global brand influence

### Recommended Strategy
- Increase English or bilingual releases
- Build stronger TikTok and Spotify conversion
- Use short-form content for discovery
- Develop clearer individual member identity
- Collaborate with Western producers, artists, or media platforms
"""


def generate_openai_us_analysis(
    group_name,
    us_score,
    english,
    performance,
    social_media,
    western_fit,
    fanbase
):
    if client is None:
        return "OpenAI client is not available. Please check your API key and package installation."

    prompt = f"""
You are a K-pop global market analyst.

Analyse the US market potential of the following K-pop group.

Group: {group_name}
US Potential Score: {us_score}/10

User-rated factors:
- English Accessibility: {english}/10
- Performance Impact: {performance}/10
- Social Media Power: {social_media}/10
- Western Market Compatibility: {western_fit}/10
- Global Fanbase Strength: {fanbase}/10

Context:
Japan and China are already established K-pop markets.
This analysis focuses on the US because it represents mainstream Western penetration,
Billboard visibility, Spotify conversion, TikTok virality, and global brand value.

Return a concise report with:
- US market potential level
- main strengths
- main risks
- recommended strategy
- final judgement
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text


st.title("🎤 K-pop Industry Intelligence")

if st.button("🏠 Back to Culture"):
    st.switch_page("pages/4_Culture.py")

show_optional_music(
    "Love Shot",
    "EXO",
    "https://www.youtube.com/watch?v=pSudEWBAYRE"
)

st.caption(
    "A dedicated culture sub-module analysing K-pop as a global entertainment industry, with a focus on US market expansion."
)

st.divider()


tabs = st.tabs([
    "🌐 Industry Overview",
    "🏢 Company Analysis",
    "📅 Generation & Market",
    "🇺🇸 US Market Prediction",
    "🌍 Global Hit Predictor",
    "🧠 Insight"
])


with tabs[0]:
    st.subheader("🌐 K-pop Industry Overview")

    st.markdown("""
This module treats K-pop as a structured entertainment industry rather than only a music genre.

The analysis focuses on:

- company systems
- generation changes
- market focus
- expansion category
- global expansion
- US market potential
""")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        selected_type = st.multiselect(
            "Artist Type",
            options=sorted(df["artist_type"].unique()),
            default=sorted(df["artist_type"].unique())
        )

    with col2:
        selected_gender = st.multiselect(
            "Gender",
            options=sorted(df["gender"].unique()),
            default=sorted(df["gender"].unique())
        )

    with col3:
        selected_market = st.multiselect(
            "Main Market",
            options=sorted(df["main_market"].unique()),
            default=sorted(df["main_market"].unique())
        )

    with col4:
        selected_generation = st.multiselect(
            "Generation",
            options=["1st Gen", "2nd Gen", "3rd Gen", "4th Gen", "5th Gen"],
            default=["1st Gen", "2nd Gen", "3rd Gen", "4th Gen", "5th Gen"]
        )

    with col5:
        selected_expansion = st.multiselect(
            "Expansion Category",
            options=sorted(df["expansion_category"].unique()),
            default=sorted(df["expansion_category"].unique())
        )

    base_df = df[
        (df["artist_type"].isin(selected_type)) &
        (df["gender"].isin(selected_gender)) &
        (df["main_market"].isin(selected_market)) &
        (df["generation"].isin(selected_generation)) &
        (df["expansion_category"].isin(selected_expansion))
    ]

    if base_df.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    show_basic_metrics(base_df)

    st.divider()

    st.subheader("📋 Artist Dataset")
    st.dataframe(
        base_df.sort_values(["expansion_category", "company_group", "debut_year", "artist_name"]),
        use_container_width=True,
        height=320
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🏢 Company Group Distribution")
        st.bar_chart(base_df["company_group"].value_counts())

    with col_b:
        st.subheader("🌍 Expansion Category")
        st.bar_chart(base_df["expansion_category"].value_counts())

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("👥 Artist Type")
        st.bar_chart(base_df["artist_type"].value_counts())

    with col_d:
        st.subheader("🌏 Main Market")
        st.bar_chart(base_df["main_market"].value_counts())


with tabs[1]:
    st.subheader("🏢 Company Analysis")

    company_filter = st.multiselect(
        "Select Company Group",
        options=["SM", "JYP", "YG", "HYBE", "Others"],
        default=["SM", "JYP", "YG", "HYBE", "Others"]
    )

    company_df = df[df["company_group"].isin(company_filter)]

    if company_df.empty:
        st.warning("No data available.")
    else:
        show_basic_metrics(company_df)

        st.divider()

        st.subheader("📊 Artist Count by Company Group")
        st.bar_chart(company_df["company_group"].value_counts())

        st.subheader("👥 Group vs Solo by Company")
        pivot_type = pd.crosstab(company_df["company_group"], company_df["artist_type"])
        st.bar_chart(pivot_type)

        st.subheader("🌍 Market Focus by Company")
        pivot_market = pd.crosstab(company_df["company_group"], company_df["main_market"])
        st.bar_chart(pivot_market)

        st.subheader("🚀 Expansion Category by Company")
        pivot_expansion = pd.crosstab(company_df["company_group"], company_df["expansion_category"])
        st.bar_chart(pivot_expansion)

        st.info("""
The Big 4 companies are analysed as system builders.

They do not only manage artists.  
They design training systems, concept strategies, market positioning, platform use, and global fan engagement.
""")


with tabs[2]:
    st.subheader("📅 Generation & Market Evolution")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Debut Year Trend")
        debut_trend = df["debut_year"].value_counts().sort_index()
        st.line_chart(debut_trend)

    with col2:
        st.subheader("🌍 Main Market Distribution")
        st.bar_chart(df["main_market"].value_counts())

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🚀 Expansion Category")
        st.bar_chart(df["expansion_category"].value_counts())

    with col4:
        st.subheader("📅 Generation Distribution")
        st.bar_chart(df["generation"].value_counts())

    st.divider()

    st.subheader("📜 Market Expansion Logic")

    market_cases = pd.DataFrame({
        "Market": ["Japan", "China", "United States"],
        "Representative Case": ["TVXQ", "EXO", "BTS / BLACKPINK"],
        "Strategic Meaning": [
            "Deep localisation into Japan's entertainment system",
            "China-focused hybrid K-pop localisation",
            "Western mainstream penetration and global brand expansion"
        ]
    })

    st.dataframe(market_cases, use_container_width=True)

    st.info("""
Different K-pop generations focused on different strategic markets:

- TVXQ represented deep Japanese market integration.
- EXO represented China-focused hybrid expansion.
- BTS and BLACKPINK accelerated Western mainstream penetration.

This module focuses on the US because Japan and China are already structurally established K-pop markets.
""")


with tabs[3]:
    st.subheader("🇺🇸 US Market Prediction")

    st.markdown("""
This section is designed as a market analysis simulator.

It does not ask which group is simply popular.  
It asks which group has the strongest potential to enter the US mainstream entertainment system.

Only current global or US-targeted groups are included here.
""")

    us_target_df = df[
        (df["artist_name"].isin(US_GLOBAL_TARGET_GROUPS)) &
        (df["artist_type"] == "group")
    ]

    if us_target_df.empty:
        st.warning("No US/global target groups found in the dataset.")
        st.stop()

    available_groups = sorted(us_target_df["artist_name"].unique())

    default_index = available_groups.index("Stray Kids") if "Stray Kids" in available_groups else 0

    selected_group = st.selectbox(
        "Choose a K-pop group",
        options=available_groups,
        index=default_index
    )

    selected_row = df[df["artist_name"] == selected_group].iloc[0]

    col_info1, col_info2, col_info3 = st.columns(3)

    col_info1.metric("Company", selected_row["company"])
    col_info2.metric("Generation", selected_row["generation"])
    col_info3.metric("Expansion Type", selected_row["expansion_category"])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        english = st.slider("English Accessibility", 0, 10, 7)
        performance = st.slider("Performance Impact", 0, 10, 8)
        social_media = st.slider("Social Media Power", 0, 10, 8)

    with col2:
        western_fit = st.slider("Western Market Compatibility", 0, 10, 7)
        fanbase = st.slider("Global Fanbase Strength", 0, 10, 8)

    us_score = (
        english * 0.2 +
        performance * 0.2 +
        social_media * 0.2 +
        western_fit * 0.2 +
        fanbase * 0.2
    )

    st.metric("🇺🇸 US Market Potential Score", round(us_score, 2))

    if us_score >= 8:
        st.success(f"{selected_group} shows strong US market potential.")
    elif us_score >= 6:
        st.info(f"{selected_group} shows moderate US market potential.")
    else:
        st.warning(f"{selected_group} may need stronger localisation or platform strategy for the US market.")

    st.divider()

    st.subheader("📄 Rule-Based Strategy Report")
    st.markdown(
        generate_us_strategy_text(
            selected_group,
            us_score,
            english,
            performance,
            social_media,
            western_fit,
            fanbase
        )
    )

    st.divider()

    st.subheader("🤖 OpenAI US Market Analysis")

    if st.button("Generate AI US Market Report"):
        with st.spinner("Analysing US market potential..."):
            report = generate_openai_us_analysis(
                selected_group,
                round(us_score, 2),
                english,
                performance,
                social_media,
                western_fit,
                fanbase
            )

            st.markdown("""
            <div style="
            padding: 1.5rem;
            border-radius: 20px;
            background: linear-gradient(135deg,#ffffff,#f7f9fc);
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05);
            ">
            <h2>🧠 AI Strategic Insight</h2>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(report)


with tabs[4]:
    st.subheader("🌍 Next Global Hit Predictor")

    hit_df = predict_next_global_hit(df)

    if hit_df.empty:
        st.warning("No prediction data available.")
    else:
        st.dataframe(hit_df, use_container_width=True)

        top_artist = hit_df.iloc[0]["artist_name"]
        top_company = hit_df.iloc[0]["company"]

        st.success(f"""
🔥 Most Likely Next Global Hit Candidate:

**{top_artist}** from **{top_company}**

Why:
- strong market potential
- recent generation advantage
- company-level support
- global expansion readiness
""")

    st.divider()

    st.subheader("🇺🇸 Company US Potential Score")

    us_score_df = calculate_us_potential_by_company(df)

    if us_score_df.empty:
        st.warning("No company score available.")
    else:
        st.dataframe(us_score_df, use_container_width=True)
        st.bar_chart(us_score_df.set_index("company")["us_potential_score"])

        best_company = us_score_df.iloc[0]["company"]

        st.info(f"""
Based on the current dataset, **{best_company}** has the strongest US market potential.

Recommended actions:
- stronger global branding
- English-language or bilingual releases
- TikTok and Spotify growth strategy
- solo/sub-unit development
- Western collaboration strategy
""")


with tabs[5]:
    st.subheader("🧠 K-pop System Insight")

    st.markdown(generate_industry_insight(df))

    st.divider()

    st.subheader("📌 Project Positioning")

    st.success("""
This module is not a K-pop fan page.

It is designed as a culture-industry intelligence system.

The key question is not:

"Which group is the most popular?"

The key question is:

"Which entertainment system can produce artists with global market scalability?"
""")

    st.divider()

    st.subheader("📌 Data Notes")

    st.write("""
- The dataset focuses on selected K-pop artists, groups, solo acts, company systems, generations, and market direction.
- SM, JYP, YG, and HYBE are treated as major company groups.
- Japan and China are treated as established K-pop markets.
- The US is treated as a global mainstream expansion market.
- Historical groups are useful for market history, but current US prediction focuses on more active or global-targeted groups.
- Expansion categories are manually assigned as analytical labels, not official company categories.
""")

