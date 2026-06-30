from __future__ import annotations

from . import data_loader

CITY_ORDER = {"Seoul": 0, "Busan": 1, "Incheon": 2, "Daegu": 3, "Daejeon": 4, "Gwangju": 5, "Jeju": 6}

ZH_OVERVIEW = {
    "country_introduction": "韩国是一个高度互联的东亚国家，以先进科技、密集城市、教育基础设施、流行文化、美食和快速公共交通闻名。",
    "population": "约 5170 万",
    "area": "约 100,400 平方公里",
    "capital": "首尔",
    "currency": "韩元（KRW）",
    "time_zone": "韩国标准时间（UTC+9）",
    "language": "韩语",
    "climate": "四季分明，夏季炎热潮湿，冬季寒冷干燥。",
}

ZH_CITY = {
    "Seoul": "首尔",
    "Busan": "釜山",
    "Incheon": "仁川",
    "Daegu": "大邱",
    "Daejeon": "大田",
    "Gwangju": "光州",
    "Jeju": "济州",
}

ZH_CITY_DESCRIPTIONS = {
    "Seoul": "首都城市，大学、创业、企业和文化资源最集中。",
    "Busan": "海滨大城市，生活节奏相对平衡，适合学习、生活和港口相关产业。",
    "Incheon": "连接国际机场和首都圈的城市，适合重视交通、物流和国际社区的人。",
    "Daegu": "生活成本相对可控，医疗、教育和区域商业资源稳定。",
    "Daejeon": "科研和工程资源较强，适合重视学习、研究和较安静生活节奏的人。",
    "Gwangju": "文化氛围强、生活成本较低，适合偏好创意和较慢生活节奏的人。",
    "Jeju": "自然环境突出、生活节奏较慢，适合重视生活质量和安静环境的人。",
}

ZH_BEST_FOR = {
    "Coastal living": "海滨生活",
    "Lifestyle balance": "生活平衡",
    "Balanced lifestyle": "生活平衡",
    "International access": "国际交通便利",
    "Airport access": "机场交通",
    "Business": "商务",
    "Seoul proximity": "靠近首尔",
    "Regional universities": "地方大学",
    "Everyday living": "日常生活",
    "Graduate study": "研究生学习",
    "Food": "美食",
    "Affordable living": "低成本生活",
    "Lower cost": "低成本生活",
    "Arts": "艺术",
    "Top universities": "顶尖大学",
    "Corporate jobs": "企业岗位",
    "Corporate roles": "企业岗位",
    "Startups": "创业公司",
    "Startup companies": "创业公司",
    "Culture": "文化生活",
    "Cultural life": "文化生活",
    "Research": "研究",
    "Engineering": "工程",
    "Science": "科学",
    "Healthcare": "医疗健康",
    "Logistics": "物流",
    "Tourism": "旅游",
    "Port industries": "港口产业",
    "Port logistics": "港口产业",
    "Manufacturing": "制造业",
    "Quiet living": "安静生活",
    "Creative culture": "创意文化",
    "Budget living": "预算友好生活",
    "Nature": "自然环境",
    "Lifestyle": "生活方式",
    "Remote work": "远程工作",
}


def get_overview(language: str = "en") -> dict:
    if language == "zh":
        return ZH_OVERVIEW
    return {
        "country_introduction": (
            "South Korea is a highly connected East Asian country known for advanced technology, "
            "dense cities, strong education infrastructure, pop culture, food, and fast public transport."
        ),
        "population": "About 51.7 million",
        "area": "About 100,400 km2",
        "capital": "Seoul",
        "currency": "South Korean won (KRW)",
        "time_zone": "Korea Standard Time (UTC+9)",
        "language": "Korean",
        "climate": "Four distinct seasons with hot humid summers and cold dry winters.",
    }


def get_cities(language: str = "en") -> list[dict]:
    cities = sorted(data_loader.load_city(), key=lambda city: CITY_ORDER.get(city["city_name"], 99))
    return [
        {
            "name": ZH_CITY.get(city["city_name"], city["city_name"]) if language == "zh" else city["city_name"],
            "population": _population_label(city["population"], language),
            "living_cost": _living_cost_label(city["average_rent"], language),
            "study_score": city["study_score"],
            "career_score": city["career_score"],
            "lifestyle_score": city["living_score"],
            "short_description": ZH_CITY_DESCRIPTIONS.get(city["city_name"], city["description"]) if language == "zh" else city["description"],
            "best_for": _localized_recommended_for(city["recommended_for"], language),
        }
        for city in cities
    ]


def get_culture(language: str = "en") -> list[dict]:
    sections = data_loader.load_culture("overview")["sections"]
    if language != "zh":
        return sections
    translations = {
        "Etiquette": ("礼仪", "韩国日常交流重视礼貌、年龄和场合。", ["初次见面保持礼貌称呼。", "递交物品时可双手递交。"]),
        "Honorifics": ("敬语", "韩语敬语体现关系、场合和尊重程度。", ["面对教授、面试官、工作人员时优先使用敬语。", "不确定时使用更礼貌的表达更安全。"]),
        "Food Culture": ("饮食文化", "韩国饮食重视共享、配菜和集体用餐体验。", ["集体用餐时注意长辈或上级先开始。", "尝试本地食物有助于融入生活。"]),
        "Festivals": ("节日", "传统节日和现代文化活动都很丰富。", ["中秋和春节期间交通和营业时间可能变化。", "城市文化节适合了解本地社区。"]),
        "School Culture": ("学校文化", "课堂参与、教授沟通和小组项目很重要。", ["及时确认作业和考试要求。", "与教授沟通时说明姓名、课程和目的。"]),
        "Workplace Culture": ("职场文化", "韩国职场通常重视团队协作、礼貌沟通和责任边界。", ["会议中表达清晰、态度谦逊。", "确认任务截止时间和汇报方式。"]),
    }
    return [
        {
            "title": translations.get(section["title"], (section["title"], section["summary"], section["tips"]))[0],
            "summary": translations.get(section["title"], (section["title"], section["summary"], section["tips"]))[1],
            "tips": translations.get(section["title"], (section["title"], section["summary"], section["tips"]))[2],
        }
        for section in sections
    ]


def get_history(language: str = "en") -> list[dict]:
    events = data_loader.load_culture("history")["events"]
    if language != "zh":
        return events
    translations = {
        "Three Kingdoms": ("三国时期", "高句丽、百济和新罗形成早期政治与文化基础。"),
        "Goryeo": ("高丽", "高丽王朝推动佛教文化、陶瓷和印刷技术发展。"),
        "Joseon": ("朝鲜王朝", "朝鲜王朝建立儒家制度、行政体系和韩文字母基础。"),
        "Japanese Occupation": ("日本殖民时期", "这一时期对现代韩国身份、政治和社会记忆产生深远影响。"),
        "Republic of Korea": ("大韩民国", "1948 年后韩国逐步建立现代国家制度。"),
        "Modern Korea": ("现代韩国", "韩国发展为高度城市化、科技和文化影响力突出的国家。"),
    }
    return [
        {
            "period": translations.get(event["period"], (event["period"], event["summary"]))[0],
            "timeframe": event["timeframe"],
            "summary": translations.get(event["period"], (event["period"], event["summary"]))[1],
        }
        for event in events
    ]


def get_living_cost() -> list[dict]:
    cities = sorted(data_loader.load_city(), key=lambda city: CITY_ORDER.get(city["city_name"], 99))
    return [
        {
            "city": city["city_name"],
            "rent": city["average_rent"],
            "food": city["average_food_cost"],
            "transportation": city["transport_cost"],
            "mobile": 55000,
            "utilities": 120000 if city["city_name"] != "Seoul" else 130000,
            "entertainment": 180000 if city["city_name"] != "Seoul" else 220000,
        }
        for city in cities
    ]


def get_quick_facts(language: str = "en") -> list[dict]:
    facts = data_loader.load_culture("quick_facts")["facts"]
    if language != "zh":
        return facts
    translations = {
        "Emergency Numbers": ("紧急电话", "报警 112，火警/急救 119", "遇到紧急情况时优先拨打官方紧急电话。"),
        "Visa Types": ("签证类型", "D-2、D-4、D-10、E-7、F-2、F-5", "签证条件会变化，重要决定前请确认官方信息。"),
        "Voltage": ("电压", "220V，60Hz", "韩国常用 C/F 插头类型。"),
        "Internet": ("互联网", "高速宽带和移动网络普及", "公共 Wi-Fi 和手机套餐选择较多。"),
        "Public Transport": ("公共交通", "地铁、公交、高铁和城际交通发达", "T-money 等交通卡可用于多种交通方式。"),
        "Healthcare": ("医疗", "公共和私营医疗体系完善", "长期居住通常需要确认保险和医院路径。"),
        "Banking": ("银行", "开户通常需要身份文件和居留相关材料", "不同银行对外国人开户材料要求可能不同。"),
    }
    return [
        {
            "title": translations.get(fact["title"], (fact["title"], fact["value"], fact["detail"]))[0],
            "value": translations.get(fact["title"], (fact["title"], fact["value"], fact["detail"]))[1],
            "detail": translations.get(fact["title"], (fact["title"], fact["value"], fact["detail"]))[2],
        }
        for fact in facts
    ]




def _localized_recommended_for(value: list[str] | dict, language: str) -> list[str]:
    if isinstance(value, dict):
        items = value.get(language) or value.get("en") or []
        return [_translate_best_for(item, language) for item in items]
    return [_translate_best_for(item, language) for item in value]

def _living_cost_label(average_rent: float, language: str = "en") -> str:
    if average_rent >= 700000:
        return "很高" if language == "zh" else "Very high"
    if average_rent >= 580000:
        return "中高" if language == "zh" else "Medium-high"
    if average_rent >= 500000:
        return "中等" if language == "zh" else "Medium"
    return "中低" if language == "zh" else "Medium-low"


def _population_label(value: str, language: str) -> str:
    if language != "zh":
        return value
    if "9.4 million" in value:
        return "约 940 万"
    return value.replace("About ", "约 ").replace(" million", " 百万")


def _translate_best_for(value: str, language: str) -> str:
    if language != "zh":
        return value
    return ZH_BEST_FOR.get(value, value)

