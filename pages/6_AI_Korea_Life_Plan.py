import json
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import APIClient
from locales.i18n import format_krw, get_language, language_selector, t, translate_option, translate_result_label
from ui_style import apply_product_style

st.set_page_config(page_title="AI 韩国发展规划" if get_language() == "zh" else "AI Korea Life Plan", page_icon="🧭", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


def default_profile() -> dict:
    return {
        "display_name": "Compass User",
        "study_profile": {
            "nationality": "International",
            "age": 22,
            "current_education_level": "Undergraduate",
            "target_study_level": "Graduate School",
            "target_major": "Computer Science",
            "korean_level": "TOPIK 3",
            "english_level": "Intermediate",
            "annual_budget": 20_000_000,
            "preferred_city": "Seoul",
        },
        "career_profile": {
            "target_role": "Data Analyst",
            "work_experience": "0-2 years",
            "technical_skills": ["SQL", "Python"],
            "korean_level": "TOPIK 3",
            "english_level": "Intermediate",
            "target_industry": "Technology",
            "visa_goal": "D-10",
        },
        "living_profile": {
            "lifestyle": "Standard",
            "housing_preference": "Shared Apartment",
            "monthly_budget": 1_500_000,
            "preferred_city": "Seoul",
            "transport_preference": "Public Transit",
            "community_preference": "International Community",
        },
    }


language_selector("life_plan_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

current_user = st.session_state.get("current_user")
if not current_user and st.session_state.get("auth_token"):
    try:
        current_user = api.me()
        st.session_state["current_user"] = current_user
    except Exception:
        current_user = None

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V3</div>
    <h1>{label("AI Korea Life Plan", "AI 韩国发展规划")}</h1>
    <p>{label("Generate a combined study, career, living, budget, language, visa, and action plan for Korea.", "生成覆盖留学、职业、生活、预算、语言、签证与行动计划的韩国规划报告。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Exportable planning report", "可导出的规划报告")}</h3>
    <p>{label("Markdown, TXT, and JSON exports are available after generation.", "生成后可导出 Markdown、TXT 和 JSON。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

profile = st.session_state.get("compass_profile")
if not profile:
    try:
        profile = api.get_latest_profile()
    except Exception:
        profile = None
if not profile:
    profile = default_profile()
    st.info(label("No saved profile found. Using a sample profile for the demo.", "尚未找到已保存个人画像。当前使用示例画像演示。"))
elif current_user:
    st.success(label(
        f"Using the latest profile for {current_user['display_name']}.",
        f"正在使用 {current_user['display_name']} 的最新个人画像。",
    ))
else:
    st.info(label(
        "Demo mode. Log in to save profiles and planning history.",
        "当前为演示模式。登录后可以保存个人画像和历史规划。",
    ))

topik_goal = st.selectbox(
    label("TOPIK Target", "TOPIK 目标"),
    ["TOPIK 3", "TOPIK 4", "TOPIK 5+"],
    index=1,
)

payload = {
    **profile,
    "language": get_language(),
    "city_recommendation": st.session_state.get("city_recommendation"),
    "mbti_city_match": st.session_state.get("mbti_city_match"),
    "topik_goal": topik_goal,
}

if st.button(label("Generate AI Korea Life Plan", "生成 AI 韩国发展规划"), use_container_width=True, type="primary"):
    try:
        with st.spinner(t("common.generating_ai_plan")):
            result = api.generate_korea_life_plan(payload)
        st.session_state["korea_life_plan"] = result
    except Exception as exc:
        st.error(label(f"Life plan generation failed: {exc}", f"生活规划生成失败：{exc}"))

plan = st.session_state.get("korea_life_plan")
if not plan:
    st.info(t("common.no_data"))
    st.stop()

try:
    kb_status = api.get_kb_status()
except Exception:
    kb_status = {}

st.markdown(f"## {label('Report Metadata', '\u62a5\u544a\u4fe1\u606f')}")
m1, m2, m3, m4 = st.columns(4)
m1.metric(label("Generated at", "\u62a5\u544a\u751f\u6210\u65f6\u95f4"), plan.get("generated_at") or datetime.now().strftime("%Y-%m-%d %H:%M"))
m2.metric(label("Knowledge Base Version", "知识库版本"), plan.get("knowledge_base_version") or kb_status.get("knowledge_base_version", "v2.1"))
m3.metric(label("Data Confidence", "数据可信度"), plan.get("data_confidence") or label("Based on available inputs", "\u57fa\u4e8e\u53ef\u7528\u8f93\u5165"))
m4.metric(label("Official Source Count", "官方来源数量"), kb_status.get("source_coverage", {}).get("Official", plan.get("official_source_count", 0)))

st.markdown(f"## {label('Recommendation', '总体建议')}")
c1, c2, c3, c4 = st.columns(4)
c1.metric(label("Overall", "总体"), translate_result_label(plan["overall_recommendation"]))
c2.metric(label("Best City", "最佳城市"), translate_option("city", plan["best_city"]))
c3.metric(label("Annual Study Cost", "\u5e74\u5ea6\u7559\u5b66\u6210\u672c"), format_krw(plan["estimated_annual_study_cost"]))
c4.metric(label("Monthly Living Cost", "\u6708\u5ea6\u751f\u6d3b\u6210\u672c"), format_krw(plan["estimated_monthly_living_cost"]))

st.markdown(f"## {label('Plan Sections', '规划内容')}")
s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(f"### {label('Study Path', '留学路径')}")
    st.write(plan["study_path"])
with s2:
    st.markdown(f"### {label('Career Path', '职业路径')}")
    st.write(plan["career_path"])
with s3:
    st.markdown(f"### {label('Living Plan', '生活规划')}")
    st.write(plan["living_plan"])

st.markdown(f"## {label('Integrated Planning', '综合规划')}")
i1, i2 = st.columns(2)
with i1:
    st.markdown(f"### {label('MBTI City Fit', 'MBTI 城市匹配')}")
    st.write(plan.get("mbti_city_fit", label("No MBTI city match was provided; report is based on available inputs.", "未提供 MBTI 城市匹配；报告基于可用输入生成。")))
    st.markdown(f"### {label('Language Learning Plan', '语言学习计划')}")
    st.write(plan.get("language_learning_plan", ""))
with i2:
    st.markdown(f"### {label('Budget Analysis', '预算分析')}")
    st.write(plan.get("budget_analysis", ""))
    st.markdown(f"### {label('Data Confidence Summary', '数据可信度总结')}")
    st.write(plan.get("confidence_summary", ""))

st.markdown(f"## {label('Risks and Visa', '风险与签证')}")
r1, r2, r3, r4 = st.columns(4)
r1.metric(label("Budget Gap", "\u9884\u7b97\u5dee\u989d"), format_krw(plan["budget_gap"]))
r2.metric(label("Language Risk", "语言风险"), translate_result_label(plan["language_risk"]))
r3.metric(label("Career Risk", "职业风险"), translate_result_label(plan["career_risk"]))
r4.metric(label("Living Risk", "生活风险"), translate_result_label(plan["living_risk"]))
st.info(plan["visa_pathway"])
st.markdown(f"### {label('Risk Summary', '风险总结')}")
st.write(plan.get("risk_summary", ""))

available_inputs = plan.get("based_on_available_inputs", [])
if available_inputs:
    st.caption(label("Based on available inputs:", "基于以下可用输入：") + " " + ", ".join(available_inputs))

st.markdown(f"## {label('Action Plan', '行动计划')}")
with st.expander(label("3-month action plan", "3 个月行动计划"), expanded=True):
    st.markdown(plan["action_plan_3_month"])
with st.expander(label("6-month action plan", "6 个月行动计划")):
    st.markdown(plan["action_plan_6_month"])
with st.expander(label("12-month action plan", "12 个月行动计划")):
    st.markdown(plan["action_plan_12_month"])

st.markdown(f"## {label('Export', '导出')}")
markdown_report = plan.get("markdown_report", "")
ec1, ec2, ec3 = st.columns(3)
ec1.download_button(label("Download Markdown", "下载 Markdown"), markdown_report, "korea_life_plan.md", "text/markdown", use_container_width=True)
ec2.download_button(label("Download TXT", "下载 TXT"), markdown_report, "korea_life_plan.txt", "text/plain", use_container_width=True)
ec3.download_button(label("Download JSON", "下载 JSON"), json.dumps(plan, ensure_ascii=False, indent=2), "korea_life_plan.json", "application/json", use_container_width=True)

st.caption(t("common.footer"))
