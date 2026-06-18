import sys
from pathlib import Path
from types import SimpleNamespace

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
