from __future__ import annotations

from . import data_loader


def get_study_scenarios() -> list[dict]:
    return data_loader.load_learning("study")


def get_career_scenarios() -> list[dict]:
    return data_loader.load_learning("career")


def get_living_scenarios() -> list[dict]:
    return data_loader.load_learning("living")


def get_topik_planners() -> list[dict]:
    return data_loader.load_learning("topik")


def explain_expression(expression: str, action: str = "explain_expression", context: str | None = None) -> dict:
    clean_expression = (expression or "").strip()
    clean_action = (action or "explain_expression").strip().lower()
    clean_context = (context or "study, work, or daily life in Korea").strip()

    if not clean_expression:
        clean_expression = "안녕하세요."

    translation = _rough_translation(clean_expression)
    natural_rewrite = _natural_rewrite(clean_expression)

    action_intro = {
        "explain_expression": "This expression is useful when you need a polite, practical phrase in a real Korean setting.",
        "rewrite_naturally": "A more natural version should keep the same intention while sounding softer and more context-aware.",
        "translate": "This is a practical meaning-focused translation rather than a word-for-word translation.",
        "grammar_notes": "The key grammar point is how the ending controls politeness, distance, and clarity.",
        "culture_notes": "The cultural point is to sound respectful without over-explaining.",
    }.get(clean_action, "This rule-based helper explains the expression for real-life Korea planning contexts.")

    return {
        "expression": clean_expression,
        "action": clean_action,
        "explanation": f"{action_intro} Context: {clean_context}.",
        "natural_rewrite": natural_rewrite,
        "translation": translation,
        "grammar_notes": _grammar_notes(clean_expression),
        "culture_notes": _culture_notes(clean_expression, clean_context),
    }


def _rough_translation(expression: str) -> str:
    known = {
        "질문이 있습니다.": "I have a question.",
        "다시 설명해 주실 수 있을까요?": "Could you explain it again?",
        "면담 시간을 예약하고 싶습니다.": "I would like to schedule a meeting.",
        "자기소개를 드리겠습니다.": "I will introduce myself.",
        "확인 부탁드립니다.": "Please check / please confirm.",
        "메뉴판 주세요.": "Please give me the menu.",
        "계좌를 개설하고 싶습니다.": "I would like to open a bank account.",
    }
    return known.get(expression, "Meaning depends on context; use it as a polite practical expression.")


def _natural_rewrite(expression: str) -> str:
    if expression.endswith("주세요."):
        return expression.replace("주세요.", "부탁드립니다.")
    if expression.endswith("있나요?"):
        return expression.replace("있나요?", "있을까요?")
    if expression.endswith("싶습니다."):
        return expression
    return expression


def _grammar_notes(expression: str) -> list[str]:
    notes = []
    if "주실 수 있을까요" in expression or "수 있을까요" in expression:
        notes.append("-(으)실 수 있을까요 is a polite ability/request pattern: 'Could you ...?'")
    if "싶습니다" in expression:
        notes.append("-고 싶습니다 expresses 'I would like to...' in a formal polite style.")
    if "주세요" in expression:
        notes.append("-주세요 is a direct but polite request form. In formal contexts, 부탁드립니다 can sound softer.")
    if not notes:
        notes.append("Check the sentence ending first; Korean politeness is often carried by the final verb ending.")
    return notes


def _culture_notes(expression: str, context: str) -> list[str]:
    notes = [
        "Use polite speech first with professors, staff, interviewers, landlords, and service workers.",
        "Short, clear Korean is usually better than a long sentence with uncertain grammar.",
    ]
    if "Professor" in context or "class" in context.lower():
        notes.append("For professors, include your name, class, and purpose before the request.")
    if "interview" in context.lower() or "work" in context.lower():
        notes.append("In career contexts, confident but modest phrasing is usually safest.")
    if "restaurant" in context.lower() or "daily" in context.lower():
        notes.append("In daily life, simple request forms are acceptable and common.")
    return notes
