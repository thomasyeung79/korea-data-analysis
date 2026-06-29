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

st.set_page_config(page_title="Korean Learning Support", page_icon="🗣", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


def scenario_card(title: str, description: str = "") -> None:
    st.markdown(
        f"""
<div class="insight-card">
  <h3 style="margin-top:0;">{title}</h3>
  <p style="margin-bottom:0;color:#475569;">{description}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def show_helper(expression: str, context: str, key: str) -> None:
    st.markdown(f"#### {label('AI Korean Helper', 'AI 韩语助手')}")
    action = st.selectbox(
        label("Action", "操作"),
        [
            "explain_expression",
            "rewrite_naturally",
            "translate",
            "grammar_notes",
            "culture_notes",
        ],
        format_func=lambda value: {
            "explain_expression": label("Explain Expression", "解释表达"),
            "rewrite_naturally": label("Rewrite Naturally", "自然改写"),
            "translate": label("Translate", "翻译"),
            "grammar_notes": label("Grammar Notes", "语法说明"),
            "culture_notes": label("Culture Notes", "文化提示"),
        }[value],
        key=f"action_{key}",
    )
    helper_expression = st.text_input(label("Expression", "表达"), value=expression, key=f"expr_{key}")
    if st.button(label("Run Helper", "运行助手"), key=f"run_{key}"):
        result = api.explain_korean_expression(
            {"expression": helper_expression, "action": action, "context": context}
        )
        st.info(result["explanation"])
        st.write(f"**{label('Natural rewrite', '自然改写')}**: {result['natural_rewrite']}")
        st.write(f"**{label('Translation', '翻译')}**: {result['translation']}")
        st.markdown(f"**{label('Grammar Notes', '语法说明')}**")
        for note in result["grammar_notes"]:
            st.markdown(f"- {note}")
        st.markdown(f"**{label('Culture Notes', '文化提示')}**")
        for note in result["culture_notes"]:
            st.markdown(f"- {note}")


def show_vocab(vocabulary: list[dict], heading: str) -> None:
    if vocabulary:
        st.markdown(f"#### {heading}")
        st.dataframe(pd.DataFrame(vocabulary), use_container_width=True, hide_index=True)


language_selector("korean_learning_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V5</div>
    <h1>{label("Korean Learning Support", "韩语场景支持")}</h1>
    <p>{label("Scenario Korean for studying, working, and living in South Korea. This is support for real tasks, not a standalone language-learning app.", "面向韩国留学、工作和生活的场景韩语支持。这是实际任务辅助，不是独立背单词应用。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Study / Career / Living Korean", "留学 / 职业 / 生活韩语")}</h3>
    <p>{label("Use expressions, dialogues, vocabulary, and rule-based explanations in the context where you need them.", "在真实场景中使用表达、对话、词汇和规则式解释。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

try:
    language = get_language()
    study_data = api.get_korean_learning_study(language)
    career_data = api.get_korean_learning_career(language)
    living_data = api.get_korean_learning_living(language)
    topik_data = api.get_korean_learning_topik()
except Exception as exc:
    st.error(label(f"Korean Learning data is unavailable: {exc}", f"韩语学习支持数据暂不可用：{exc}"))
    st.stop()

tab_study, tab_career, tab_living, tab_topik = st.tabs(
    [
        label("Study Korean", "留学韩语"),
        label("Career Korean", "职场韩语"),
        label("Living Korean", "生活韩语"),
        label("TOPIK Planner", "TOPIK 规划"),
    ]
)

with tab_study:
    selected = st.selectbox(label("Scenario", "场景"), [item["scenario"] for item in study_data], key="study_scenario", format_func=lambda v: translate_option("korean_scenario", v))
    item = next(row for row in study_data if row["scenario"] == selected)
    scenario_card(translate_option("korean_scenario", item["scenario"]), item["situation"])
    st.markdown(f"#### {label('Useful Expressions', '实用表达')}")
    for expression in item["useful_expressions"]:
        st.markdown(f"- {expression}")
    st.markdown(f"#### {label('Example Dialogue', '示例对话')}")
    for line in item["example_dialogue"]:
        st.write(line)
    show_vocab(item["vocabulary"], label("Vocabulary", "词汇"))
    st.markdown(f"#### {label('AI Explanation', 'AI 解释')}")
    st.write(item["ai_explanation"])
    show_helper(item["useful_expressions"][0], f"Study Korean - {item['scenario']}", "study")

with tab_career:
    selected = st.selectbox(label("Scenario", "场景"), [item["scenario"] for item in career_data], key="career_scenario", format_func=lambda v: translate_option("korean_scenario", v))
    item = next(row for row in career_data if row["scenario"] == selected)
    scenario_card(translate_option("korean_scenario", item["scenario"]))
    st.markdown(f"#### {label('Useful Expressions', '实用表达')}")
    for expression in item["useful_expressions"]:
        st.markdown(f"- {expression}")
    st.markdown(f"#### {label('Interview Tips', '面试 / 商务提示')}")
    for tip in item["interview_tips"]:
        st.markdown(f"- {tip}")
    show_vocab(item["business_vocabulary"], label("Business Vocabulary", "商务词汇"))
    st.markdown(f"#### {label('Sample Conversation', '示例对话')}")
    for line in item["sample_conversation"]:
        st.write(line)
    show_helper(item["useful_expressions"][0], f"Career Korean - {item['scenario']}", "career")

with tab_living:
    selected = st.selectbox(label("Scenario", "场景"), [item["scenario"] for item in living_data], key="living_scenario", format_func=lambda v: translate_option("korean_scenario", v))
    item = next(row for row in living_data if row["scenario"] == selected)
    scenario_card(translate_option("korean_scenario", item["scenario"]))
    st.markdown(f"#### {label('Useful Expressions', '实用表达')}")
    for expression in item["useful_expressions"]:
        st.markdown(f"- {expression}")
    st.markdown(f"#### {label('Common Questions', '常见问题')}")
    for question in item["common_questions"]:
        st.markdown(f"- {question}")
    st.markdown(f"#### {label('Sample Dialogue', '示例对话')}")
    for line in item["sample_dialogue"]:
        st.write(line)
    st.markdown(f"#### {label('Culture Tips', '文化提示')}")
    for tip in item["culture_tips"]:
        st.markdown(f"- {tip}")
    show_helper(item["useful_expressions"][0], f"Living Korean - {item['scenario']}", "living")

with tab_topik:
    selected = st.selectbox(label("TOPIK Level", "TOPIK 等级"), [item["topik_level"] for item in topik_data])
    item = next(row for row in topik_data if row["topik_level"] == selected)
    scenario_card(item["topik_level"], f"{item['current_level']} → {item['target_level']}")
    c1, c2, c3 = st.columns(3)
    c1.metric(label("Current Level", "当前水平"), item["current_level"])
    c2.metric(label("Target Level", "目标等级"), item["target_level"])
    c3.metric(label("Recommended Study Hours", "建议学习时长"), item["recommended_study_hours"])
    st.markdown(f"#### {label('Weekly Study Plan', '每周学习计划')}")
    for step in item["weekly_study_plan"]:
        st.markdown(f"- {step}")
    st.markdown(f"#### {label('Suggested Resources', '推荐资源')}")
    for resource in item["suggested_resources"]:
        st.markdown(f"- {resource}")
    st.markdown(f"#### {label('Learning Roadmap', '学习路线')}")
    for step in item["learning_roadmap"]:
        st.markdown(f"- {step}")
