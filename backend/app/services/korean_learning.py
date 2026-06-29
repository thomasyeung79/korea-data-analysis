from __future__ import annotations

from . import data_loader


ZH_STUDY = {
    "Classroom": {
        "situation": "参加课堂、提问并确认作业要求。",
        "ai_explanation": "适合课堂互动、向老师确认说明和礼貌提问。",
    },
    "Professor": {
        "situation": "与教授预约面谈、说明问题并请求建议。",
        "ai_explanation": "与教授沟通时应先说明姓名、课程和目的，再提出请求。",
    },
    "Library": {
        "situation": "在图书馆咨询座位、借书、打印或学习空间。",
        "ai_explanation": "图书馆场景适合使用简短、礼貌、直接的请求表达。",
    },
    "Dormitory": {
        "situation": "处理宿舍入住、设施问题、室友沟通和生活规则。",
        "ai_explanation": "宿舍沟通要清楚说明问题，并保持礼貌和合作语气。",
    },
    "Campus": {
        "situation": "在校园中问路、咨询办公室、参加活动或处理行政事项。",
        "ai_explanation": "校园场景常用地点、时间和请求确认表达。",
    },
    "Presentation": {
        "situation": "进行课堂展示、说明观点并回应问题。",
        "ai_explanation": "展示时需要清晰开场、转接观点和礼貌回应问题。",
    },
}

ZH_CAREER = {
    "Interview": "面试中自我介绍、说明经历并回答岗位相关问题。",
    "Resume": "准备简历、说明经历、技能和申请意图。",
    "Office": "在办公室沟通任务、进度、会议和确认事项。",
    "Meeting": "参加会议、表达意见、确认行动项和截止时间。",
    "Email": "撰写职场邮件、请求确认和跟进事项。",
    "Business Phone": "进行商务电话沟通、确认身份、说明目的和约定后续。",
}

ZH_LIVING = {
    "Restaurant": "在餐厅点餐、询问菜单、过敏信息和结账。",
    "Convenience Store": "在便利店购物、询问价格、支付和领取小票。",
    "Hospital": "在医院说明症状、挂号、确认科室和用药。",
    "Pharmacy": "在药店咨询药品、用法、剂量和注意事项。",
    "Bank": "在银行开户、办理银行卡、咨询转账和材料要求。",
    "Apartment": "租房、看房、确认押金、维修和合同事项。",
    "Subway": "乘坐地铁、问路、换乘和确认方向。",
    "Taxi": "打车、说明目的地、请求路线或确认费用。",
}


def get_study_scenarios(language: str = "en") -> list[dict]:
    records = data_loader.load_learning("study")
    if language != "zh":
        return records
    return [_localize_study(record) for record in records]


def get_career_scenarios(language: str = "en") -> list[dict]:
    records = data_loader.load_learning("career")
    if language != "zh":
        return records
    return [_localize_career(record) for record in records]


def get_living_scenarios(language: str = "en") -> list[dict]:
    records = data_loader.load_learning("living")
    if language != "zh":
        return records
    return [_localize_living(record) for record in records]


def get_topik_planners() -> list[dict]:
    return data_loader.load_learning("topik")


def _localize_study(record: dict) -> dict:
    item = dict(record)
    zh = ZH_STUDY.get(item.get("scenario"), {})
    item["situation"] = zh.get("situation", item.get("situation", ""))
    item["ai_explanation"] = zh.get("ai_explanation", item.get("ai_explanation", ""))
    return item


def _localize_career(record: dict) -> dict:
    item = dict(record)
    scenario = item.get("scenario", "")
    summary = ZH_CAREER.get(scenario)
    if summary:
        item["interview_tips"] = [
            summary,
            "保持礼貌、具体，并结合岗位要求说明自己的准备。",
            "如果没有听清问题，可以礼貌请求对方重复或解释。",
        ]
    return item


def _localize_living(record: dict) -> dict:
    item = dict(record)
    scenario = item.get("scenario", "")
    summary = ZH_LIVING.get(scenario)
    if summary:
        item["common_questions"] = [
            summary,
            "请确认价格、时间、材料或下一步操作。",
            "不确定时可以使用礼貌表达请求对方再说明一次。",
        ]
        item["culture_tips"] = [
            "先使用礼貌韩语表达更安全。",
            "说明需求时保持简短清楚。",
            "涉及费用、合同或医疗时，请再次确认关键信息。",
        ]
    return item


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
