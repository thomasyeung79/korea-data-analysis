import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
from openai import OpenAI

st.set_page_config(
    page_title="Korea Tourism Intelligence Module",
    page_icon="🇰🇷",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
[data-testid="collapsedControl"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    max-width: 1100px;
    padding-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )
    OPENAI_ENABLED = True

except Exception:
    client = None
    OPENAI_ENABLED = False

ORDER_FILE = "korea_travel_orders.json"

TEXT = {
    "English": {
        "title": "🇰🇷 Korea Tourism Intelligence Module",
        "subtitle": "AI multi-city itinerary planner, travel order system, and tourism analytics.",
        "planner": "🧭 AI Travel Planner",
        "orders": "📦 Order Management",
        "analytics": "📊 Tourism Analytics",
        "customer": "Customer Name",
        "route": "Travel Route",
        "days": "Trip Days",
        "budget": "Budget Level",
        "interests": "Travel Interests",
        "style": "Travel Style",
        "generate": "✨ Generate AI Itinerary",
        "estimated": "Estimated Price",
        "no_key": "OpenAI API key is not set. Fallback itinerary will be used.",
        "success": "Travel order saved.",
        "order_detail": "Order Detail",
        "route_popularity": "Route Popularity",
        "budget_distribution": "Budget Distribution",
        "raw_data": "Raw Order Data",
        "no_orders": "No orders yet.",
        "no_data": "No data for analytics yet.",
        "footer": "Korea System | Tourism Intelligence Module"
    },
    "中文": {
        "title": "🇰🇷 韩国旅游智能模块",
        "subtitle": "AI多城市路线规划、旅游订单系统与旅游数据分析。",
        "planner": "🧭 AI旅行路线规划",
        "orders": "📦 订单管理",
        "analytics": "📊 旅游数据分析",
        "customer": "客户姓名",
        "route": "旅行路线",
        "days": "旅行天数",
        "budget": "预算等级",
        "interests": "旅行兴趣",
        "style": "旅行风格",
        "generate": "✨ 生成AI旅行路线",
        "estimated": "预估价格",
        "no_key": "未设置 OpenAI API Key，将使用基础路线生成。",
        "success": "旅游订单已保存。",
        "order_detail": "订单详情",
        "route_popularity": "路线热度",
        "budget_distribution": "预算分布",
        "raw_data": "原始订单数据",
        "no_orders": "暂无订单。",
        "no_data": "暂无可分析数据。",
        "footer": "韩国系统 | 旅游智能模块"
    }
}

KOREA_LOCATIONS = {
    "Seoul": [
        "Gangnam", "Hongdae", "Myeongdong", "Jamsil",
        "Itaewon", "Seongsu", "Dongdaemun", "Yeouido",
        "Insadong", "Bukchon", "Sinchon", "COEX"
    ],
    "Busan": [
        "Haeundae", "Gwangalli", "Seomyeon", "Nampo",
        "Gamcheon Culture Village", "Songdo", "Centum City"
    ],
    "Incheon": [
        "Incheon Airport Area", "Songdo", "Wolmido",
        "Chinatown", "Bupyeong"
    ],
    "Daegu": [
        "Dongseongro", "Seomun Market", "Suseong Lake",
        "Apsan", "Daegu Stadium"
    ],
    "Daejeon": [
        "Yuseong", "Dunsan", "Expo Science Park",
        "Daecheong Lake"
    ],
    "Gwangju": [
        "Dongmyeong-dong", "Asia Culture Center",
        "Mudeungsan", "Chungjang-ro"
    ],
    "Ulsan": [
        "Taehwagang", "Daewangam Park",
        "Jangsaengpo", "Ulsan Grand Park"
    ],
    "Sejong": [
        "Sejong Lake Park", "Government Complex Area",
        "National Sejong Arboretum"
    ],
    "Gyeonggi-do": [
        "Suwon", "Yongin", "Seongnam", "Goyang",
        "Paju", "Gapyeong", "Anyang", "Bucheon",
        "Hwaseong", "Namyangju"
    ],
    "Gangwon-do": [
        "Gangneung", "Sokcho", "Chuncheon",
        "Pyeongchang", "Yangyang", "Donghae"
    ],
    "Chungcheongbuk-do": [
        "Cheongju", "Chungju", "Danyang", "Jecheon"
    ],
    "Chungcheongnam-do": [
        "Cheonan", "Asan", "Gongju", "Boryeong",
        "Buyeo", "Taean"
    ],
    "Jeollabuk-do": [
        "Jeonju", "Gunsan", "Namwon", "Iksan",
        "Muju", "Buan"
    ],
    "Jeollanam-do": [
        "Yeosu", "Suncheon", "Mokpo", "Boseong",
        "Damyang", "Wando", "Jindo"
    ],
    "Gyeongsangbuk-do": [
        "Gyeongju", "Andong", "Pohang",
        "Gumi", "Ulleungdo"
    ],
    "Gyeongsangnam-do": [
        "Changwon", "Jinju", "Tongyeong",
        "Geoje", "Gimhae", "Namhae"
    ],
    "Jeju-do": [
        "Jeju City", "Seogwipo", "Aewol",
        "Seongsan", "Jungmun", "Hallasan"
    ]
}

LOCATION_ZH = {
    "Seoul": "首尔",
    "Busan": "釜山",
    "Incheon": "仁川",
    "Daegu": "大邱",
    "Daejeon": "大田",
    "Gwangju": "光州",
    "Ulsan": "蔚山",
    "Sejong": "世宗",
    "Gyeonggi-do": "京畿道",
    "Gangwon-do": "江原道",
    "Chungcheongbuk-do": "忠清北道",
    "Chungcheongnam-do": "忠清南道",
    "Jeollabuk-do": "全罗北道",
    "Jeollanam-do": "全罗南道",
    "Gyeongsangbuk-do": "庆尚北道",
    "Gyeongsangnam-do": "庆尚南道",
    "Jeju-do": "济州道",

    "Gangnam": "江南",
    "Hongdae": "弘大",
    "Myeongdong": "明洞",
    "Jamsil": "蚕室",
    "Itaewon": "梨泰院",
    "Seongsu": "圣水",
    "Dongdaemun": "东大门",
    "Yeouido": "汝矣岛",
    "Insadong": "仁寺洞",
    "Bukchon": "北村",
    "Sinchon": "新村",
    "COEX": "COEX",

    "Haeundae": "海云台",
    "Gwangalli": "广安里",
    "Seomyeon": "西面",
    "Nampo": "南浦",
    "Gamcheon Culture Village": "甘川文化村",
    "Songdo": "松岛",
    "Centum City": "Centum City",

    "Incheon Airport Area": "仁川机场区域",
    "Wolmido": "月尾岛",
    "Chinatown": "中华街",
    "Bupyeong": "富平",

    "Dongseongro": "东城路",
    "Seomun Market": "西门市场",
    "Suseong Lake": "寿城池",
    "Apsan": "前山",
    "Daegu Stadium": "大邱体育场",

    "Yuseong": "儒城",
    "Dunsan": "屯山",
    "Expo Science Park": "世博科学公园",
    "Daecheong Lake": "大清湖",

    "Dongmyeong-dong": "东明洞",
    "Asia Culture Center": "亚洲文化殿堂",
    "Mudeungsan": "无等山",
    "Chungjang-ro": "忠壮路",

    "Taehwagang": "太和江",
    "Daewangam Park": "大王岩公园",
    "Jangsaengpo": "长生浦",
    "Ulsan Grand Park": "蔚山大公园",

    "Sejong Lake Park": "世宗湖水公园",
    "Government Complex Area": "政府办公区域",
    "National Sejong Arboretum": "国立世宗树木园",

    "Suwon": "水原",
    "Yongin": "龙仁",
    "Seongnam": "城南",
    "Goyang": "高阳",
    "Paju": "坡州",
    "Gapyeong": "加平",
    "Anyang": "安养",
    "Bucheon": "富川",
    "Hwaseong": "华城",
    "Namyangju": "南杨州",

    "Gangneung": "江陵",
    "Sokcho": "束草",
    "Chuncheon": "春川",
    "Pyeongchang": "平昌",
    "Yangyang": "襄阳",
    "Donghae": "东海",

    "Cheongju": "清州",
    "Chungju": "忠州",
    "Danyang": "丹阳",
    "Jecheon": "堤川",

    "Cheonan": "天安",
    "Asan": "牙山",
    "Gongju": "公州",
    "Boryeong": "保宁",
    "Buyeo": "扶余",
    "Taean": "泰安",

    "Jeonju": "全州",
    "Gunsan": "群山",
    "Namwon": "南原",
    "Iksan": "益山",
    "Muju": "茂朱",
    "Buan": "扶安",

    "Yeosu": "丽水",
    "Suncheon": "顺天",
    "Mokpo": "木浦",
    "Boseong": "宝城",
    "Damyang": "潭阳",
    "Wando": "莞岛",
    "Jindo": "珍岛",

    "Gyeongju": "庆州",
    "Andong": "安东",
    "Pohang": "浦项",
    "Gumi": "龟尾",
    "Ulleungdo": "郁陵岛",

    "Changwon": "昌原",
    "Jinju": "晋州",
    "Tongyeong": "统营",
    "Geoje": "巨济",
    "Gimhae": "金海",
    "Namhae": "南海",

    "Jeju City": "济州市",
    "Seogwipo": "西归浦",
    "Aewol": "涯月",
    "Seongsan": "城山",
    "Jungmun": "中文旅游区",
    "Hallasan": "汉拿山"
}

def build_route_options():
    options = []

    for region, places in KOREA_LOCATIONS.items():
        options.append(region)

        for place in places:
            options.append(f"{place} ({region})")

    return options

ROUTE_OPTIONS = build_route_options()

BUDGET_OPTIONS = ["Low", "Medium", "High"]

BUDGET_ZH = {
    "Low": "低预算",
    "Medium": "中等预算",
    "High": "高预算"
}

INTEREST_OPTIONS = [
    "K-pop", "History", "Food", "Shopping",
    "Football", "Baseball", "Night View",
    "Temple", "Nature", "K-drama",
    "Cafe", "Local Market"
]

INTEREST_ZH = {
    "K-pop": "K-pop",
    "History": "历史",
    "Food": "美食",
    "Shopping": "购物",
    "Football": "足球",
    "Baseball": "棒球",
    "Night View": "夜景",
    "Temple": "寺庙",
    "Nature": "自然",
    "K-drama": "韩剧",
    "Cafe": "咖啡馆",
    "Local Market": "传统市场"
}

STYLE_OPTIONS = [
    "Relaxed",
    "Efficient",
    "Culture-focused",
    "Shopping-focused",
    "K-pop focused",
    "Family-friendly",
    "Budget-saving"
]

STYLE_ZH = {
    "Relaxed": "轻松慢游",
    "Efficient": "高效率路线",
    "Culture-focused": "文化体验",
    "Shopping-focused": "购物导向",
    "K-pop focused": "K-pop导向",
    "Family-friendly": "家庭友好",
    "Budget-saving": "省钱模式"
}

def display_location(value, language):
    if language != "中文":
        return value

    if "(" in value and ")" in value:
        place = value.split(" (")[0]
        region = value.split(" (")[1].replace(")", "")
        return f"{LOCATION_ZH.get(place, place)}（{LOCATION_ZH.get(region, region)}）"

    return LOCATION_ZH.get(value, value)

def display_budget(value, language):
    return BUDGET_ZH.get(value, value) if language == "中文" else value

def display_interest(value, language):
    return INTEREST_ZH.get(value, value) if language == "中文" else value

def display_style(value, language):
    return STYLE_ZH.get(value, value) if language == "中文" else value

def load_orders():
    if not os.path.exists(ORDER_FILE):
        return []

    try:
        with open(ORDER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_order(order):
    orders = load_orders()
    orders.append(order)

    with open(ORDER_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

CITY_COST = {
    "Seoul": 130,
    "Busan": 110,
    "Jeju-do": 150,
    "Gyeongju": 90,
    "Gangneung": 100,
    "Sokcho": 95,
    "Chuncheon": 85,
    "Suwon": 85,
    "Incheon": 95,
    "Daegu": 90,
    "Daejeon": 85,
    "Gwangju": 85,
    "Jeonju": 90,
    "Andong": 80,
    "Yeosu": 100,
    "Suncheon": 85,
    "Pohang": 85,
    "Gyeonggi-do": 90,
    "Gangwon-do": 95,
    "Chungcheongbuk-do": 80,
    "Chungcheongnam-do": 80,
    "Jeollabuk-do": 85,
    "Jeollanam-do": 90,
    "Gyeongsangbuk-do": 85,
    "Gyeongsangnam-do": 90
}

BUDGET_MULTIPLIER = {
    "Low": 0.8,
    "Medium": 1.0,
    "High": 1.45
}

STYLE_MULTIPLIER = {
    "Relaxed": 1.0,
    "Efficient": 1.1,
    "Culture-focused": 1.15,
    "Shopping-focused": 1.25,
    "K-pop focused": 1.25,
    "Family-friendly": 1.2,
    "Budget-saving": 0.85
}

INTEREST_EXTRA = {
    "K-pop": 40,
    "History": 20,
    "Food": 30,
    "Shopping": 50,
    "Football": 35,
    "Baseball": 30,
    "Night View": 20,
    "Temple": 15,
    "Nature": 20,
    "K-drama": 30,
    "Cafe": 15,
    "Local Market": 15
}


def extract_region_from_location(location):
    if "(" in location and ")" in location:
        return location.split("(")[1].replace(")", "").strip()

    return location.strip()


def estimate_transport_cost(travel_route):
    if len(travel_route) <= 1:
        return 0

    transport_cost = 0

    for i in range(len(travel_route) - 1):
        current_region = extract_region_from_location(travel_route[i])
        next_region = extract_region_from_location(travel_route[i + 1])

        if current_region == next_region:
            transport_cost += 10
        else:
            transport_cost += 45

    return transport_cost


def estimate_price(travel_route, days, budget, interests, travel_style):
    if not travel_route:
        return 0

    route_costs = []

    for location in travel_route:
        region = extract_region_from_location(location)
        route_costs.append(CITY_COST.get(region, 90))

    avg_daily_city_cost = sum(route_costs) / len(route_costs)

    base_cost = avg_daily_city_cost * days

    interest_cost = 0
    for interest in interests:
        interest_cost += INTEREST_EXTRA.get(interest, 0)

    transport_cost = estimate_transport_cost(travel_route)

    style_multiplier = STYLE_MULTIPLIER.get(travel_style, 1.0)
    budget_multiplier = BUDGET_MULTIPLIER.get(budget, 1.0)

    total = (
        base_cost
        + interest_cost
        + transport_cost
    ) * style_multiplier * budget_multiplier

    return round(total, 2)

def generate_fallback_itinerary(travel_route, days, interests, language):
    plan = []

    for day in range(1, days + 1):
        place = travel_route[(day - 1) % len(travel_route)]
        place_display = display_location(place, language)

        if language == "中文":
            morning = f"上午：在 {place_display} 进行城市漫步或参观代表性景点。"
            afternoon = "下午：根据兴趣安排美食、购物、历史文化或市场体验。"
            evening = "晚上：安排夜景、咖啡馆、当地餐厅或自由活动。"
            day_label = f"第 {day} 天"
        else:
            morning = f"Morning: Explore key attractions or local neighbourhoods in {place}."
            afternoon = "Afternoon: Arrange food, shopping, history, culture, or market experience based on interests."
            evening = "Evening: Night view, cafe, local restaurant, or free time."
            day_label = f"Day {day}"

        plan.append({
            "Day": day_label,
            "Place": place_display,
            "Morning": morning,
            "Afternoon": afternoon,
            "Evening": evening
        })

    return plan

def generate_ai_itinerary(
    customer_name,
    travel_route,
    days,
    budget,
    interests,
    travel_style,
    language
):
    route_text = " → ".join(
        [display_location(x, language) for x in travel_route]
    )

    interests_text = ", ".join(
        [display_interest(x, language) for x in interests]
    )

    budget_text = display_budget(budget, language)
    style_text = display_style(travel_style, language)

    if language == "中文":
        prompt_language = "简体中文"
        output_rule = """
非常重要：
请全部使用简体中文输出。
不要使用英文标题。
除非是必要的英文地名或品牌名，否则不要混入英文。
请用中文标题，例如：基本信息、每日路线、交通建议、美食建议、预算说明、文化提示。
"""
    else:
        prompt_language = "English"
        output_rule = """
IMPORTANT:
Please write the whole output in English.
Use clear English headings.
"""

    prompt = f"""
You are a Korea travel intelligence planner.

Please generate a practical Korea multi-city travel itinerary.

Customer name: {user_name}
Travel route: {route_text}
Trip days: {days}
Budget level: {budget_text}
Interests: {interests_text}
Travel style: {style_text}
Output language: {prompt_language}

Requirements:
1. Create a day-by-day itinerary.
2. Each day should include morning, afternoon, and evening.
3. If the route includes multiple cities, include transportation between cities.
4. Include KTX / bus / flight recommendation where suitable.
5. Include hotel transition advice.
6. Include food suggestions.
7. Include budget notes.
8. Include one local cultural insight.
9. If K-pop is selected, include K-pop related areas or activities.
10. If sports is selected, include K League, baseball, or sports viewing ideas.
11. Keep it practical and suitable for a travel product demo.

{output_rule}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text

language = st.selectbox(
    "Language / 语言",
    ["English", "中文"]
)

t = TEXT[language]

user_name = st.session_state.get("user_name")

if not user_name:

    st.warning(
        "Please return to Home and enter your username first."
        if language == "English"
        else "请先返回首页输入用户名。"
    )

    if st.button(
        "🏠 Back to Home"
        if language == "English"
        else "🏠 返回首页"
    ):
        st.switch_page("app.py")

    st.stop()

st.markdown(f"""
# {t["title"]}

{t["subtitle"]}
""")

if st.button("🏠 Back to Tourism"):
    st.switch_page("pages/7_Tourism.py")

if not OPENAI_ENABLED:
    st.warning(t["no_key"])

tab1, tab2, tab3 = st.tabs([
    t["planner"],
    t["orders"],
    t["analytics"]
])

with tab1:
    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"👤 {user_name}"
        )

        travel_route = st.multiselect(
            t["route"],
            ROUTE_OPTIONS,
            default=["Seoul", "Busan"],
            format_func=lambda x: display_location(x, language)
        )

        days = st.slider(
            t["days"],
            1,
            14,
            5
        )

    with col2:
        budget = st.selectbox(
            t["budget"],
            BUDGET_OPTIONS,
            format_func=lambda x: display_budget(x, language)
        )

        interests = st.multiselect(
            t["interests"],
            INTEREST_OPTIONS,
            default=["Food", "Shopping"],
            format_func=lambda x: display_interest(x, language)
        )

        travel_style = st.selectbox(
            t["style"],
            STYLE_OPTIONS,
            format_func=lambda x: display_style(x, language)
        )

    if st.button(t["generate"], use_container_width=True):
        if not user_name:
            st.error(
                "Please enter customer name."
                if language == "English"
                else "请输入客户姓名。"
            )
            st.stop()

        if not travel_route:
            st.error(
                "Please select at least one location."
                if language == "English"
                else "请至少选择一个地点。"
            )
            st.stop()

        estimated_price = estimate_price(
            travel_route,
            days,
            budget,
            interests,
            travel_style
        )

        ai_plan = None

        if OPENAI_ENABLED:
            try:
                with st.spinner(
                    "Generating AI itinerary..."
                    if language == "English"
                    else "正在生成AI旅行路线..."
                ):
                    ai_plan = generate_ai_itinerary(
                        user_name,
                        travel_route,
                        days,
                        budget,
                        interests,
                        travel_style,
                        language
                    )
            except Exception as e:
                st.warning(
                    f"OpenAI generation failed. Fallback itinerary will be used. Error: {e}"
                    if language == "English"
                    else f"OpenAI生成失败，将使用基础路线。错误：{e}"
                )

        fallback_plan = generate_fallback_itinerary(
            travel_route,
            days,
            interests,
            language
        )

        st.metric(
            t["estimated"],
            f"${estimated_price} AUD"
        )

        st.markdown(
            "### AI Itinerary"
            if language == "English"
            else "### AI旅行路线"
        )

        if ai_plan:
            st.markdown(ai_plan)
        else:
            st.dataframe(
                pd.DataFrame(fallback_plan),
                use_container_width=True
            )

        order = {
            "order_id": str(uuid.uuid4())[:8].upper(),
            "user_name": user_name,

            "travel_route": travel_route,
            "travel_route_display": [
                display_location(x, language)
                for x in travel_route
            ],
            "main_route": " → ".join(travel_route),
            "main_route_display": " → ".join([
                display_location(x, language)
                for x in travel_route
            ]),

            "days": days,
            "budget": budget,
            "budget_display": display_budget(budget, language),

            "interests": interests,
            "interests_display": [
                display_interest(x, language)
                for x in interests
            ],

            "travel_style": travel_style,
            "travel_style_display": display_style(travel_style, language),

            "estimated_price_aud": estimated_price,
            "payment_status": "Unpaid",
            "order_status": "Draft",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "language": language,
            "ai_plan": ai_plan,
            "itinerary": fallback_plan
        }

        save_order(order)

        st.success(
            f'{t["success"]} Order ID: {order["order_id"]}'
        )

with tab2:
    all_orders = load_orders()

    orders = [
        o for o in all_orders
        if o.get("user_name") == user_name
    ]

    if not orders:
        st.info(t["no_orders"])

    else:
        rows = []

        for o in orders:
            rows.append({
                "Order ID": o.get("order_id"),
                "Customer": o.get("user_name"),
                "Route": o.get("main_route_display", o.get("main_route", "Unknown")),
                "Days": o.get("days"),
                "Budget": o.get("budget_display", o.get("budget")),
                "Price AUD": o.get("estimated_price_aud"),
                "Payment": o.get("payment_status"),
                "Status": o.get("order_status"),
                "Created At": o.get("created_at")
            })

        df_orders = pd.DataFrame(rows)

        st.dataframe(
            df_orders,
            use_container_width=True
        )

        selected_order_id = st.selectbox(
            "Select Order" if language == "English" else "选择订单",
            [o["order_id"] for o in orders]
        )

        selected_order = next(
            o for o in orders
            if o["order_id"] == selected_order_id
        )

        st.markdown(f"### {t['order_detail']}")

        st.write(
            "Customer:" if language == "English" else "客户：",
            selected_order.get("customer_name", "")
        )

        st.write(
            "Route:" if language == "English" else "路线：",
            selected_order.get("main_route_display", selected_order.get("main_route", "Unknown"))
        )

        st.write(
            "Interests:" if language == "English" else "兴趣：",
            ", ".join(
                selected_order.get(
                    "interests_display",
                    selected_order.get("interests", [])
                )
            )
        )

        st.write(
            "Budget:" if language == "English" else "预算：",
            selected_order.get("budget_display", selected_order.get("budget", "Unknown"))
        )

        st.write(
            "Estimated Price:" if language == "English" else "预估价格：",
            f"${selected_order.get('estimated_price_aud', 0)} AUD"
        )

        if selected_order.get("ai_plan"):
            st.markdown(selected_order["ai_plan"])
        else:
            st.dataframe(
                pd.DataFrame(selected_order.get("itinerary", [])),
                use_container_width=True
            )

with tab3:
    all_orders = load_orders()

    orders = [
        o for o in all_orders
        if o.get("user_name") == user_name
    ]

    if not orders:
        st.info(t["no_data"])

    else:
        df = pd.DataFrame(orders)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Orders" if language == "English" else "订单总数",
            len(df)
        )

        if "estimated_price_aud" in df.columns:
            total_revenue = df["estimated_price_aud"].sum()
            avg_order = round(df["estimated_price_aud"].mean(), 2)
        else:
            total_revenue = 0
            avg_order = 0

        c2.metric(
            "Total Revenue Estimate" if language == "English" else "预估总收入",
            f"${total_revenue} AUD"
        )

        c3.metric(
            "Average Order Value" if language == "English" else "平均订单金额",
            f"${avg_order} AUD"
        )

        st.markdown(
            f"### {t['route_popularity']}"
        )

        if "main_route_display" in df.columns:
            st.bar_chart(
                df["main_route_display"].value_counts()
            )
        elif "main_route" in df.columns:
            st.bar_chart(
                df["main_route"].value_counts()
            )
        else:
            st.warning(
                "No route data available yet."
                if language == "English"
                else "暂无路线数据。"
            )

        st.markdown(
            f"### {t['budget_distribution']}"
        )

        if "budget_display" in df.columns:
            st.bar_chart(
                df["budget_display"].value_counts()
            )
        elif "budget" in df.columns:
            st.bar_chart(
                df["budget"].value_counts()
            )
        else:
            st.warning(
                "No budget data available yet."
                if language == "English"
                else "暂无预算数据。"
            )

        st.markdown(
            f"### {t['raw_data']}"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

st.divider()
st.caption(t["footer"])
