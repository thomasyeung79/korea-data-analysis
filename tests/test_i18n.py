import sys
from pathlib import Path
from types import SimpleNamespace

import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import locales.i18n as i18n


def reset_language_state(monkeypatch):
    monkeypatch.setattr(i18n, "st", SimpleNamespace(session_state={}))


def test_default_language_is_english(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("en")

    assert i18n.get_language() == "en"


def test_english_translation_lookup(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("en")

    assert i18n.t("home.page_title") == "Korea Analysis"


def test_chinese_translation_lookup(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    assert i18n.t("home.page_title") == "韩国分析"


def test_missing_key_falls_back_to_raw_key(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    assert i18n.t("missing.translation.key") == "missing.translation.key"


def test_missing_language_falls_back_to_english(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("unsupported")

    assert i18n.get_language() == "en"
    assert i18n.t("home.page_title") == "Korea Analysis"


def test_parameter_interpolation(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("en")

    assert i18n.t("study.estimate_heading", city="Seoul") == "Cost estimate for Seoul"


def test_chinese_role_display_mapping(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    assert i18n.display_role("Data Analyst") == "数据分析师"
    assert i18n.display_role("Backend Developer") == "后端开发工程师"
    assert i18n.display_role("Marketing Specialist") == "市场营销专员"
    assert i18n.display_role("Product Manager") == "产品经理"


def test_english_role_display_mapping(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("en")

    assert i18n.display_role("AI Engineer") == "AI Engineer"


def test_display_mapping_unknown_value_falls_back_to_raw(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    assert i18n.display_role("Research Fellow") == "Research Fellow"
    assert i18n.display_news_category("Unknown") == "Unknown"


def test_translate_option_display_values(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    assert i18n.translate_option("experience", "Student") == "学生"
    assert i18n.translate_option("korean_level", "None") == "无"
    assert i18n.translate_option("city", "Seoul") == "首尔"
    assert i18n.translate_option("school_type", "Graduate School") == "研究生院"
    assert i18n.translate_option("housing_type", "Dormitory") == "宿舍"
    assert i18n.translate_option("lifestyle", "Budget") == "节省型"


def test_option_value_from_chinese_label(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    assert i18n.option_value_from_label("role", "后端开发工程师") == "Backend Developer"
    assert i18n.option_value_from_label("experience", "0-2 年经验") == "0-2 years"
    assert i18n.option_value_from_label("city", "釜山") == "Busan"


def test_result_label_translation(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    assert i18n.translate_result_label("Strongly Recommended ✅") == "强烈推荐 ✅"
    assert i18n.translate_result_label("Recommended with Preparation ⚠️") == "准备充分后推荐 ⚠️"
    assert i18n.translate_result_label("Risky ❓") == "有一定风险 ❓"
    assert i18n.translate_result_label("Not Recommended Yet ❌") == "暂不推荐 ❌"
    assert i18n.translate_result_label("Low") == "低"
    assert i18n.translate_result_label("Medium") == "中"
    assert i18n.translate_result_label("High") == "高"


def test_translated_chart_labels_do_not_break(monkeypatch):
    reset_language_state(monkeypatch)
    i18n.set_language("zh")

    labels = [
        i18n.translate_option("cost_category", "Tuition"),
        i18n.translate_option("cost_category", "Housing"),
    ]
    fig = go.Figure(data=[go.Pie(labels=labels, values=[60, 40], textinfo="label+percent")])

    assert fig.data[0].labels == tuple(["学费", "住房"])
