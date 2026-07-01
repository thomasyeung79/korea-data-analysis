import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import APIClient
from locales.i18n import get_language, language_selector, t, translate_option
from ui_style import apply_product_style

st.set_page_config(page_title=t("korean.page_title"), page_icon="🗣", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


def show_expressions(expressions: list[dict]) -> None:
    lang = get_language()
    for ex in expressions:
        ko = ex.get("ko", "")
        zh = ex.get("zh", "")
        en = ex.get("en", "")
        rom = ex.get("romanization", "")
        usage_zh = ex.get("usage_zh", "")
        usage_en = ex.get("usage_en", "")

        lines = [f"**{ko}**"]
        if lang == "zh" and zh:
            lines.append(f"*{zh}*")
        else:
            lines.append(f"*{en}*")
        if rom:
            lines.append(f"📢 {rom}")
        usage = usage_zh if lang == "zh" and usage_zh else usage_en
        if usage:
            lines.append(f"💡 {usage}")
        st.markdown("  \n".join(lines))
        st.markdown("---")


def show_dialogues(dialogues: list[dict]) -> None:
    lang = get_language()
    for d in dialogues:
        speaker = d.get("speaker", "")
        ko = d.get("ko", "")
        zh = d.get("zh", "")
        en = d.get("en", "")
        rom = d.get("romanization", "")
        trans = zh if lang == "zh" and zh else en
        st.markdown(f"**{speaker}：** {ko}  ")
        if trans:
            st.markdown(f"*{trans}*  ")
        if rom:
            st.markdown(f"📢 {rom}")
        st.markdown("---")


def show_vocab_grid(vocab: list[dict]) -> None:
    if not vocab:
        return
    lang = get_language()
    rows = []
    for v in vocab:
        ko = v.get("korean", "")
        rom = v.get("romanization", "")
        zh = v.get("zh", "")
        meaning = v.get("meaning", "")
        note_key = "note_zh" if lang == "zh" else "note_en"
        note = v.get(note_key, "")
        rows.append({
            "한국어": ko,
            "발음": rom,
            label("中文", "English"): zh if lang == "zh" else meaning,
            label("说明", "Note"): note,
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


language_selector("korean_learning_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V5</div>
    <h1>{t("korean.page_title")}</h1>
    <p>{label("Scenario Korean for studying, working, and living in South Korea.", "面向韩国留学、工作和生活的场景韩语支持。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Study / Career / Living Korean", "留学 / 职业 / 生活韩语")}</h3>
    <p>{label("Use expressions, dialogues, vocabulary, and explanations in the context where you need them.", "在真实场景中使用表达、对话、词汇和解析。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

try:
    lang = get_language()
    with st.spinner(t("common.loading_official_data")):
        study_data = api.get_korean_learning_study(lang)
        career_data = api.get_korean_learning_career(lang)
        living_data = api.get_korean_learning_living(lang)
        topik_data = api.get_korean_learning_topik()
except Exception as exc:
    st.error(label(f"Korean Learning data is unavailable: {exc}", f"韩语学习支持数据暂不可用：{exc}"))
    st.stop()

tab_study, tab_career, tab_living, tab_topik = st.tabs(
    [
        t("korean.tab_study"),
        t("korean.tab_career"),
        t("korean.tab_living"),
        t("korean.tab_topik"),
    ]
)

with tab_study:
    selected = st.selectbox(t("korean.scenario"), [item["scenario"] for item in study_data], key="study_scenario", format_func=lambda v: translate_option("korean_scenario", v))
    item = next(row for row in study_data if row["scenario"] == selected)
    st.markdown(f"**{item['situation']}**")
    st.markdown(f"#### {t('korean.useful_expressions')}")
    show_expressions(item.get("useful_expressions", []))
    st.markdown(f"#### {t('korean.dialogue')}")
    show_dialogues(item.get("example_dialogue", []))
    st.markdown(f"#### {t('korean.vocabulary')}")
    show_vocab_grid(item.get("vocabulary", []))
    ai_explanation = item.get("ai_explanation", "")
    if ai_explanation:
        st.markdown(f"#### {t('korean.ai_explanation')}")
        st.write(ai_explanation)

with tab_career:
    selected = st.selectbox(t("korean.scenario"), [item["scenario"] for item in career_data], key="career_scenario", format_func=lambda v: translate_option("korean_scenario", v))
    item = next(row for row in career_data if row["scenario"] == selected)
    st.markdown(f"#### {t('korean.useful_expressions')}")
    show_expressions(item.get("useful_expressions", []))
    st.markdown(f"#### {t('korean.tips')}")
    for tip in item.get("interview_tips", []):
        st.markdown(f"- {tip}")
    st.markdown(f"#### {t('korean.vocabulary')}")
    show_vocab_grid(item.get("business_vocabulary", []))
    st.markdown(f"#### {t('korean.conversation')}")
    show_dialogues(item.get("sample_conversation", []))

with tab_living:
    selected = st.selectbox(t("korean.scenario"), [item["scenario"] for item in living_data], key="living_scenario", format_func=lambda v: translate_option("korean_scenario", v))
    item = next(row for row in living_data if row["scenario"] == selected)
    st.markdown(f"#### {t('korean.useful_expressions')}")
    show_expressions(item.get("useful_expressions", []))
    st.markdown(f"#### {t('korean.common_questions')}")
    for q in item.get("common_questions", []):
        st.markdown(f"- {q}")
    st.markdown(f"#### {t('korean.conversation')}")
    show_dialogues(item.get("sample_dialogue", []))
    st.markdown(f"#### {t('korean.culture_tips')}")
    for tip in item.get("culture_tips", []):
        st.markdown(f"- {tip}")

with tab_topik:
    selected = st.selectbox(t("korean.topik_level"), [item["topik_level"] for item in topik_data])
    item = next(row for row in topik_data if row["topik_level"] == selected)
    c1, c2, c3 = st.columns(3)
    c1.metric(t("korean.current_level"), item["current_level"])
    c2.metric(t("korean.target_level"), item["target_level"])
    c3.metric(t("korean.study_hours"), item["recommended_study_hours"])
    st.markdown(f"#### {t('korean.weekly_plan')}")
    for step in item["weekly_study_plan"]:
        st.markdown(f"- {step}")
    st.markdown(f"#### {t('korean.resources')}")
    for resource in item["suggested_resources"]:
        st.markdown(f"- {resource}")
    st.markdown(f"#### {t('korean.roadmap')}")
    for step in item["learning_roadmap"]:
        st.markdown(f"- {step}")

st.caption(t("common.footer"))
