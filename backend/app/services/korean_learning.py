from __future__ import annotations

from . import data_loader


def get_study_scenarios(language: str = "en") -> list[dict]:
    records = data_loader.load_learning("study")
    if language == "zh":
        return [_localize_study(record, "zh") for record in records]
    return [_localize_study(record, "en") for record in records]


def get_career_scenarios(language: str = "en") -> list[dict]:
    records = data_loader.load_learning("career")
    if language == "zh":
        return [_localize_career(record, "zh") for record in records]
    return [_localize_career(record, "en") for record in records]


def get_living_scenarios(language: str = "en") -> list[dict]:
    records = data_loader.load_learning("living")
    if language == "zh":
        return [_localize_living(record, "zh") for record in records]
    return [_localize_living(record, "en") for record in records]


def get_topik_planners() -> list[dict]:
    return data_loader.load_learning("topik")


def _select_lang(item: dict, field: str, lang: str) -> str:
    """Get the language-specific field or fall back to the default."""
    key = f"{field}_{lang}"
    if key in item and item[key]:
        return item[key]
    return item.get(field, "")


def _localize_study(record: dict, lang: str) -> dict:
    item = dict(record)
    item["situation"] = _select_lang(item, "situation", lang)
    item["ai_explanation"] = _select_lang(item, "ai_explanation", lang)
    # Keep expressions/dialogues/vocab — schemas handle fields
    return item


def _localize_career(record: dict, lang: str) -> dict:
    item = dict(record)
    tips_field = f"interview_tips_{lang}"
    if tips_field in item and item[tips_field]:
        item["interview_tips"] = item[tips_field]
    return item


def _localize_living(record: dict, lang: str) -> dict:
    item = dict(record)
    q_field = f"common_questions_zh"
    if lang == "zh" and q_field in item and item[q_field]:
        item["common_questions"] = item[q_field]
    tips_field = f"culture_tips_{lang}"
    if tips_field in item and item[tips_field]:
        item["culture_tips"] = item[tips_field]
    return item


def explain_expression(expression: str, action: str = "explain_expression", context: str | None = None) -> dict:
    clean_expression = (expression or "").strip()
    clean_action = (action or "explain_expression").strip().lower()
    clean_context = (context or "study, work, or daily life in Korea").strip()

    if not clean_expression:
        clean_expression = "안녕하세요."

    translation_en, translation_zh = _bilingual_translation(clean_expression)
    natural_rewrite = _natural_rewrite(clean_expression)

    action_intro_en = {
        "explain_expression": "This expression is useful when you need a polite, practical phrase in a real Korean setting.",
        "rewrite_naturally": "A more natural version should keep the same intention while sounding softer and more context-aware.",
        "translate": "This is a practical meaning-focused translation rather than a word-for-word translation.",
        "grammar_notes": "The key grammar point is how the ending controls politeness, distance, and clarity.",
        "culture_notes": "The cultural point is to sound respectful without over-explaining.",
    }.get(clean_action, "This rule-based helper explains the expression for real-life Korea planning contexts.")

    action_intro_zh = {
        "explain_expression": "这个表达适用于在真实韩国场景中使用礼貌、实用的说法。",
        "rewrite_naturally": "更自然的改写应保留原意，同时更柔和、更符合场景。",
        "translate": "这是基于实用意义的翻译，而非逐字翻译。",
        "grammar_notes": "关键语法点是语尾如何控制礼貌程度、距离感和清晰度。",
        "culture_notes": "文化要点是保持尊重，同时避免过度解释。",
    }.get(clean_action, "该规则辅助工具会解释该表达在韩国真实场景中的用法。")

    grammar_en, grammar_zh, culture_en, culture_zh, polite_level = _bilingual_notes(clean_expression, clean_context)

    return {
        "expression": clean_expression,
        "action": clean_action,
        "explanation": f"{action_intro_en} Context: {clean_context}.",
        "explanation_zh": f"{action_intro_zh} 场景：{clean_context}。",
        "explanation_en": f"{action_intro_en} Context: {clean_context}.",
        "natural_rewrite": natural_rewrite,
        "translation": translation_en,
        "translation_zh": translation_zh,
        "translation_en": translation_en,
        "grammar_notes": grammar_en,
        "grammar_notes_zh": grammar_zh,
        "grammar_notes_en": grammar_en,
        "culture_notes": culture_en,
        "culture_notes_zh": culture_zh,
        "culture_notes_en": culture_en,
        "polite_level": polite_level,
    }


KNOWN_TRANSLATIONS_EN = {
    "질문이 있습니다.": "I have a question.",
    "다시 설명해 주실 수 있을까요?": "Could you explain it again?",
    "면담 시간을 예약하고 싶습니다.": "I would like to schedule a meeting.",
    "자기소개를 드리겠습니다.": "I will introduce myself.",
    "확인 부탁드립니다.": "Please check / please confirm.",
    "메뉴판 주세요.": "Please give me the menu.",
    "계좌를 개설하고 싶습니다.": "I would like to open a bank account.",
}

KNOWN_TRANSLATIONS_ZH = {
    "질문이 있습니다.": "我有一个问题。",
    "다시 설명해 주실 수 있을까요?": "可以再解释一遍吗？",
    "면담 시간을 예약하고 싶습니다.": "我想预约面谈时间。",
    "자기소개를 드리겠습니다.": "我来做自我介绍。",
    "확인 부탁드립니다.": "请确认。",
    "메뉴판 주세요.": "请给我菜单。",
    "계좌를 개설하고 싶습니다.": "我想开一个账户。",
}


def _bilingual_translation(expression: str) -> tuple[str, str]:
    en = KNOWN_TRANSLATIONS_EN.get(expression, "Meaning depends on context.")
    zh = KNOWN_TRANSLATIONS_ZH.get(expression, "含义取决于上下文。")
    return en, zh


def _natural_rewrite(expression: str) -> str:
    if expression.endswith("주세요."):
        return expression.replace("주세요.", "부탁드립니다.")
    if expression.endswith("있나요?"):
        return expression.replace("있나요?", "있을까요?")
    if expression.endswith("싶습니다."):
        return expression
    return expression


POLITE_LEVEL = "해요체 (informal polite) / 하십시오체 (formal polite)"


def _bilingual_notes(expression: str, context: str) -> tuple[list[str], list[str], list[str], list[str], str]:
    grammar_en_list = []
    grammar_zh_list = []
    culture_en_list = [
        "Use polite speech first with professors, staff, interviewers, landlords, and service workers.",
        "Short, clear Korean is usually better than a long sentence with uncertain grammar.",
    ]
    culture_zh_list = [
        "在与教授、职员、面试官、房东和服务人员沟通时，优先使用礼貌用语。",
        "简短清晰的韩语通常比语法不确定的长句更好。",
    ]

    if "주실 수 있을까요" in expression or "수 있을까요" in expression:
        grammar_en_list.append("-(으)실 수 있을까요 is a polite ability/request pattern: 'Could you ...?'")
        grammar_zh_list.append("-(으)실 수 있을까요 是礼貌的能力/请求句式：'可以...吗？'")
    if "싶습니다" in expression:
        grammar_en_list.append("-고 싶습니다 expresses 'I would like to...' in a formal polite style.")
        grammar_zh_list.append("-고 싶습니다 表示 '我想...'，是正式礼貌的说法。")
    if "주세요" in expression:
        grammar_en_list.append("-주세요 is a direct but polite request form. In formal contexts, 부탁드립니다 can sound softer.")
        grammar_zh_list.append("-주세요 是直接但礼貌的请求格式。在正式场合，부탁드립니다 更柔和。")
    if not grammar_en_list:
        grammar_en_list.append("Check the sentence ending first; Korean politeness is often carried by the final verb ending.")
        grammar_zh_list.append("先确认句子结尾；韩语的礼貌程度通常体现在句末语尾。")

    if "Professor" in context or "class" in context.lower():
        culture_en_list.append("For professors, include your name, class, and purpose before the request.")
        culture_zh_list.append("联系教授时，请先说姓名、课程和目的，再提出请求。")
    if "interview" in context.lower() or "work" in context.lower():
        culture_en_list.append("In career contexts, confident but modest phrasing is usually safest.")
        culture_zh_list.append("在职场环境中，自信但谦虚的表达最稳妥。")
    if "restaurant" in context.lower() or "daily" in context.lower():
        culture_en_list.append("In daily life, simple request forms are acceptable and common.")
        culture_zh_list.append("在日常生活中，简单的请求形式即可接受且常见。")

    return grammar_en_list, grammar_zh_list, culture_en_list, culture_zh_list, POLITE_LEVEL
