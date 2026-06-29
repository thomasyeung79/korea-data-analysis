import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import APIClient
from locales.i18n import get_language, language_selector, t, translate_option, display_role, profile_summary
from ui_style import apply_product_style

st.set_page_config(page_title="Profile Center", page_icon="🧩", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


language_selector("profile_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V3</div>
    <h1>{label("Profile Center", "画像中心")}</h1>
    <p>{label("Create one reusable profile for study, career, living, city recommendations, and AI Korea Life Plan.", "创建一个可复用画像，用于留学、职业、生活、城市推荐和 AI 韩国生活规划。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Study / Career / Living", "留学 / 职业 / 生活")}</h3>
    <p>{label("Your profile is saved in session state and can also be persisted through the API when a backend is configured.", "画像会保存在当前会话中；如配置后端，也可通过 API 持久化。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(f"## {label('Create Profile', '创建画像')}")
display_name = st.text_input(label("Display name", "显示名称"), value="Compass User")

study_col, career_col, living_col = st.columns(3)

with study_col:
    st.markdown(f"### {label('Study Profile', '留学画像')}")
    nationality = st.text_input(label("Nationality", "国籍"), value="International")
    age = st.number_input(label("Age", "年龄"), min_value=15, max_value=70, value=22)
    current_education_level = st.selectbox(label("Current Education Level", "当前学历"), ["High School", "Undergraduate", "Graduate School", "Working Professional"], format_func=lambda v: translate_option("education_level", v))
    target_study_level = st.selectbox(label("Target Study Level", "目标学历"), ["Language School", "Undergraduate", "Graduate School"], format_func=lambda v: translate_option("education_level", v))
    target_major = st.text_input(label("Target Major", "目标专业"), value="Computer Science")
    study_korean_level = st.selectbox(label("Korean Level", "韩语水平"), ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"], format_func=lambda v: translate_option("korean_level", v))
    study_english_level = st.selectbox(label("English Level", "英语水平"), ["Basic", "Intermediate", "Advanced", "Native"], format_func=lambda v: translate_option("english_level", v))
    annual_budget = st.number_input(label("Annual Budget (KRW)", "年度预算（韩元）"), min_value=0, value=20_000_000, step=1_000_000)
    study_city = st.selectbox(label("Preferred City", "偏好城市"), ["Seoul", "Busan", "Incheon", "Daejeon", "Daegu", "Gwangju", "Other"], format_func=lambda v: translate_option("city", v))

with career_col:
    st.markdown(f"### {label('Career Profile', '职业画像')}")
    target_role = st.selectbox(
        label("Target Role", "目标岗位"),
        ["Data Analyst", "Backend Developer", "AI Product Manager", "AI Engineer", "Marketing Specialist", "Accountant", "Business Analyst", "Product Manager", "English Teacher", "Registered Nurse", "Mechanical Engineer", "Electrical Engineer"],
        format_func=display_role,
    )
    work_experience = st.selectbox(label("Work Experience", "工作经验"), ["Student", "0-2 years", "3-5 years"], format_func=lambda v: translate_option("experience", v))
    technical_skills = st.multiselect(label("Technical / Professional Skills", "技能"), ["SQL", "Python", "Marketing", "Accounting", "Teaching", "Nursing", "CAD", "Product Management"], default=["SQL"])
    career_korean_level = st.selectbox(label("Career Korean Level", "职业韩语水平"), ["None", "TOPIK 3", "TOPIK 4", "TOPIK 5+"], index=1, format_func=lambda v: translate_option("korean_level", v))
    career_english_level = st.selectbox(label("Career English Level", "职业英语水平"), ["Basic", "Intermediate", "Advanced", "Native"], index=1, format_func=lambda v: translate_option("english_level", v))
    target_industry = st.selectbox(label("Target Industry", "目标行业"), ["Technology", "Business", "Education", "Healthcare", "Engineering"], format_func=lambda v: translate_option("industry", v))
    visa_goal = st.selectbox(label("Visa Goal", "签证目标"), ["D-2", "D-10", "E-7", "F-2"])

with living_col:
    st.markdown(f"### {label('Living Profile', '生活画像')}")
    lifestyle = st.selectbox(label("Lifestyle", "生活方式"), ["Budget", "Standard", "Premium"], format_func=lambda v: translate_option("lifestyle", v))
    housing_preference = st.selectbox(label("Housing Preference", "住房偏好"), ["Dormitory", "Shared Apartment", "Studio Apartment"], format_func=lambda v: translate_option("housing_type", v))
    monthly_budget = st.number_input(label("Monthly Budget (KRW)", "月度预算（韩元）"), min_value=0, value=1_500_000, step=100_000)
    living_city = st.selectbox(label("Living Preferred City", "生活偏好城市"), ["Seoul", "Busan", "Incheon", "Daejeon", "Daegu", "Gwangju", "Other"], format_func=lambda v: translate_option("city", v))
    transport_preference = st.selectbox(label("Transport Preference", "交通偏好"), ["Public Transit", "Walking", "Car", "Bike"], format_func=lambda v: translate_option("transport", v))
    community_preference = st.selectbox(label("Community Preference", "社区偏好"), ["International Community", "Quiet Neighborhood", "Student Area", "Career Network"], format_func=lambda v: translate_option("community", v))

payload = {
    "display_name": display_name,
    "study_profile": {
        "nationality": nationality,
        "age": age,
        "current_education_level": current_education_level,
        "target_study_level": target_study_level,
        "target_major": target_major,
        "korean_level": study_korean_level,
        "english_level": study_english_level,
        "annual_budget": annual_budget,
        "preferred_city": study_city,
    },
    "career_profile": {
        "target_role": target_role,
        "work_experience": work_experience,
        "technical_skills": technical_skills,
        "korean_level": career_korean_level,
        "english_level": career_english_level,
        "target_industry": target_industry,
        "visa_goal": visa_goal,
    },
    "living_profile": {
        "lifestyle": lifestyle,
        "housing_preference": housing_preference,
        "monthly_budget": monthly_budget,
        "preferred_city": living_city,
        "transport_preference": transport_preference,
        "community_preference": community_preference,
    },
}

if st.button(label("Save Profile", "保存画像"), use_container_width=True, type="primary"):
    saved = api.create_profile(payload)
    st.session_state["compass_profile"] = payload
    st.success(label("Profile saved. You can now generate city recommendations and a Korea Life Plan.", "画像已保存。现在可以生成城市推荐和韩国生活规划。"))
    st.markdown(f"## {t('profile.saved')}")
    summary = profile_summary(payload)
    cols = st.columns(3)
    for col, (section, rows) in zip(cols, summary.items()):
        with col:
            st.markdown(f"### {section}")
            for key, value in rows:
                st.markdown(f"- **{key}：** {value}")
    with st.expander(t("profile.raw_data"), expanded=False):
        st.json(saved)

if "compass_profile" in st.session_state:
    st.info(label("Current profile is ready for Korea Compass modules.", "当前画像已可用于 Korea Compass 模块。"))
