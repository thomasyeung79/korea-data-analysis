import streamlit as st
import pandas as pd
import json
from api_client import get_api
from ui_style import apply_product_style

st.set_page_config(
    page_title="Korea Tourism Intelligence Module",
    page_icon="🇰🇷",
    layout="wide"
)

apply_product_style()

api = get_api()

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
        "no_key": "OpenAI API key is not set on backend. Itinerary will use fallback template.",
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
        "no_key": "后端未配置 OpenAI API Key，将使用基础路线生成。",
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
    "Seoul": ["Gangnam", "Hongdae", "Myeongdong", "Jamsil", "Itaewon", "Seongsu", "Dongdaemun", "Yeouido", "Insadong", "Bukchon", "Sinchon", "COEX"],
    "Busan": ["Haeundae", "Gwangalli", "Seomyeon", "Nampo", "Gamcheon Culture Village", "Songdo", "Centum City"],
    "Incheon": ["Incheon Airport Area", "Songdo", "Wolmido", "Chinatown", "Bupyeong"],
    "Daegu": ["Dongseongro", "Seomun Market", "Suseong Lake", "Apsan", "Daegu Stadium"],
    "Daejeon": ["Yuseong", "Dunsan", "Expo Science Park", "Daecheong Lake"],
    "Gwangju": ["Dongmyeong-dong", "Asia Culture Center", "Mudeungsan", "Chungjang-ro"],
    "Ulsan": ["Taehwagang", "Daewangam Park", "Jangsaengpo", "Ulsan Grand Park"],
    "Sejong": ["Sejong Lake Park", "Government Complex Area", "National Sejong Arboretum"],
    "Gyeonggi-do": ["Suwon", "Yongin", "Seongnam", "Goyang", "Paju", "Gapyeong", "Anyang", "Bucheon", "Hwaseong", "Namyangju"],
    "Gangwon-do": ["Gangneung", "Sokcho", "Chuncheon", "Pyeongchang", "Yangyang", "Donghae"],
    "Chungcheongbuk-do": ["Cheongju", "Chungju", "Danyang", "Jecheon"],
    "Chungcheongnam-do": ["Cheonan", "Asan", "Gongju", "Boryeong", "Buyeo", "Taean"],
    "Jeollabuk-do": ["Jeonju", "Gunsan", "Namwon", "Iksan", "Muju", "Buan"],
    "Jeollanam-do": ["Yeosu", "Suncheon", "Mokpo", "Boseong", "Damyang", "Wando", "Jindo"],
    "Gyeongsangbuk-do": ["Gyeongju", "Andong", "Pohang", "Gumi", "Ulleungdo"],
    "Gyeongsangnam-do": ["Changwon", "Jinju", "Tongyeong", "Geoje", "Gimhae", "Namhae"],
    "Jeju-do": ["Jeju City", "Seogwipo", "Aewol", "Seongsan", "Jungmun", "Hallasan"]
}

LOCATION_ZH = {
    "Seoul": "首尔", "Busan": "釜山", "Incheon": "仁川", "Daegu": "大邱",
    "Daejeon": "大田", "Gwangju": "光州", "Ulsan": "蔚山", "Sejong": "世宗",
    "Gyeonggi-do": "京畿道", "Gangwon-do": "江原道", "Chungcheongbuk-do": "忠清北道",
    "Chungcheongnam-do": "忠清南道", "Jeollabuk-do": "全罗北道", "Jeollanam-do": "全罗南道",
    "Gyeongsangbuk-do": "庆尚北道", "Gyeongsangnam-do": "庆尚南道", "Jeju-do": "济州道",
    "Gangnam": "江南", "Hongdae": "弘大", "Myeongdong": "明洞", "Jamsil": "蚕室",
    "Itaewon": "梨泰院", "Seongsu": "圣水", "Dongdaemun": "东大门", "Yeouido": "汝矣岛",
    "Insadong": "仁寺洞", "Bukchon": "北村", "Sinchon": "新村", "COEX": "COEX",
    "Haeundae": "海云台", "Gwangalli": "广安里", "Seomyeon": "西面", "Nampo": "南浦",
    "Gamcheon Culture Village": "甘川文化村", "Songdo": "松岛", "Centum City": "Centum City",
    "Incheon Airport Area": "仁川机场区域", "Wolmido": "月尾岛", "Chinatown": "中华街", "Bupyeong": "富平",
    "Dongseongro": "东城路", "Seomun Market": "西门市场", "Suseong Lake": "寿城池", "Apsan": "前山", "Daegu Stadium": "大邱体育场",
    "Yuseong": "儒城", "Dunsan": "屯山", "Expo Science Park": "世博科学公园", "Daecheong Lake": "大清湖",
    "Dongmyeong-dong": "东明洞", "Asia Culture Center": "亚洲文化殿堂", "Mudeungsan": "无等山", "Chungjang-ro": "忠壮路",
    "Taehwagang": "太和江", "Daewangam Park": "大王岩公园", "Jangsaengpo": "长生浦", "Ulsan Grand Park": "蔚山大公园",
    "Sejong Lake Park": "世宗湖水公园", "Government Complex Area": "政府办公区域", "National Sejong Arboretum": "国立世宗树木园",
    "Suwon": "水原", "Yongin": "龙仁", "Seongnam": "城南", "Goyang": "高阳", "Paju": "坡州",
    "Gapyeong": "加平", "Anyang": "安养", "Bucheon": "富川", "Hwaseong": "华城", "Namyangju": "南杨州",
    "Gangneung": "江陵", "Sokcho": "束草", "Chuncheon": "春川", "Pyeongchang": "平昌", "Yangyang": "襄阳", "Donghae": "东海",
    "Cheongju": "清州", "Chungju": "忠州", "Danyang": "丹阳", "Jecheon": "堤川",
    "Cheonan": "天安", "Asan": "牙山", "Gongju": "公州", "Boryeong": "保宁", "Buyeo": "扶余", "Taean": "泰安",
    "Jeonju": "全州", "Gunsan": "群山", "Namwon": "南原", "Iksan": "益山", "Muju": "茂朱", "Buan": "扶安",
    "Yeosu": "丽水", "Suncheon": "顺天", "Mokpo": "木浦", "Boseong": "宝城", "Damyang": "潭阳", "Wando": "莞岛", "Jindo": "珍岛",
    "Gyeongju": "庆州", "Andong": "安东", "Pohang": "浦项", "Gumi": "龟尾", "Ulleungdo": "郁陵岛",
    "Changwon": "昌原", "Jinju": "晋州", "Tongyeong": "统营", "Geoje": "巨济", "Gimhae": "金海", "Namhae": "南海",
    "Jeju City": "济州市", "Seogwipo": "西归浦", "Aewol": "涯月", "Seongsan": "城山", "Jungmun": "中文旅游区", "Hallasan": "汉拿山"
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
BUDGET_ZH = {"Low": "低预算", "Medium": "中等预算", "High": "高预算"}
INTEREST_OPTIONS = ["K-pop", "History", "Food", "Shopping", "Football", "Baseball", "Night View", "Temple", "Nature", "K-drama", "Cafe", "Local Market"]
INTEREST_ZH = {"K-pop": "K-pop", "History": "历史", "Food": "美食", "Shopping": "购物", "Football": "足球", "Baseball": "棒球", "Night View": "夜景", "Temple": "寺庙", "Nature": "自然", "K-drama": "韩剧", "Cafe": "咖啡馆", "Local Market": "传统市场"}
STYLE_OPTIONS = ["Relaxed", "Efficient", "Culture-focused", "Shopping-focused", "K-pop focused", "Family-friendly", "Budget-saving"]
STYLE_ZH = {"Relaxed": "轻松慢游", "Efficient": "高效率路线", "Culture-focused": "文化体验", "Shopping-focused": "购物导向", "K-pop focused": "K-pop导向", "Family-friendly": "家庭友好", "Budget-saving": "省钱模式"}

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

CITY_COST = {
    "Seoul": 130, "Busan": 110, "Jeju-do": 150, "Gyeongju": 90,
    "Gangneung": 100, "Sokcho": 95, "Chuncheon": 85, "Suwon": 85,
    "Incheon": 95, "Daegu": 90, "Daejeon": 85, "Gwangju": 85,
    "Jeonju": 90, "Andong": 80, "Yeosu": 100, "Suncheon": 85,
    "Pohang": 85, "Gyeonggi-do": 90, "Gangwon-do": 95,
    "Chungcheongbuk-do": 80, "Chungcheongnam-do": 80,
    "Jeollabuk-do": 85, "Jeollanam-do": 90,
    "Gyeongsangbuk-do": 85, "Gyeongsangnam-do": 90
}
BUDGET_MULTIPLIER = {"Low": 0.8, "Medium": 1.0, "High": 1.45}
STYLE_MULTIPLIER = {"Relaxed": 1.0, "Efficient": 1.1, "Culture-focused": 1.15, "Shopping-focused": 1.25, "K-pop focused": 1.25, "Family-friendly": 1.2, "Budget-saving": 0.85}
INTEREST_EXTRA = {"K-pop": 40, "History": 20, "Food": 30, "Shopping": 50, "Football": 35, "Baseball": 30, "Night View": 20, "Temple": 15, "Nature": 20, "K-drama": 30, "Cafe": 15, "Local Market": 15}

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
    interest_cost = sum(INTEREST_EXTRA.get(interest, 0) for interest in interests)
    transport_cost = estimate_transport_cost(travel_route)
    style_multiplier = STYLE_MULTIPLIER.get(travel_style, 1.0)
    budget_multiplier = BUDGET_MULTIPLIER.get(budget, 1.0)
    total = (base_cost + interest_cost + transport_cost) * style_multiplier * budget_multiplier
    return round(total, 2)

def generate_fallback_itinerary(travel_route, days, language):
    plan = []
    for day in range(1, days + 1):
        place = travel_route[(day - 1) % len(travel_route)]
        place_display = display_location(place, language)
        if language == "中文":
            day_label = f"第 {day} 天"
            morning = f"上午：在 {place_display} 进行城市漫步或参观代表性景点。"
            afternoon = "下午：根据兴趣安排美食、购物、历史文化或市场体验。"
            evening = "晚上：安排夜景、咖啡馆、当地餐厅或自由活动。"
        else:
            day_label = f"Day {day}"
            morning = f"Morning: Explore key attractions or local neighbourhoods in {place}."
            afternoon = "Afternoon: Arrange food, shopping, history, culture, or market experience based on interests."
            evening = "Evening: Night view, cafe, local restaurant, or free time."
        plan.append({"Day": day_label, "Place": place_display, "Morning": morning, "Afternoon": afternoon, "Evening": evening})
    return plan

current_language = st.session_state.get("language", "English")
language = st.selectbox(
    "Language / 语言", ["English", "中文"],
    index=0 if current_language == "English" else 1
)
st.session_state["language"] = language

t = TEXT[language]

user_name = api.user.get("username") if api.is_authenticated else None

if not user_name:
    st.warning(
        "Please return to Home and enter your username first."
        if language == "English"
        else "请先返回首页输入用户名。"
    )
    if st.button("🏠 Back to Home" if language == "English" else "🏠 返回首页"):
        st.switch_page("app.py")
    st.stop()

st.markdown(f"""
# {t["title"]}

{t["subtitle"]}
""")

if st.button("🏠 Back to Tourism" if language == "English" else "🏠 返回旅游模块"):
    st.switch_page("pages/7_Tourism.py")

OPENAI_ENABLED = True  # Always try; backend handles the check

tab1, tab2, tab3 = st.tabs([t["planner"], t["orders"], t["analytics"]])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"👤 {user_name}")
        travel_route = st.multiselect(
            t["route"], ROUTE_OPTIONS,
            default=["Seoul", "Busan"],
            format_func=lambda x: display_location(x, language)
        )
        days = st.slider(t["days"], 1, 14, 5)

    with col2:
        budget = st.selectbox(
            t["budget"], BUDGET_OPTIONS,
            format_func=lambda x: display_budget(x, language)
        )
        interests = st.multiselect(
            t["interests"], INTEREST_OPTIONS,
            default=["Food", "Shopping"],
            format_func=lambda x: display_interest(x, language)
        )
        travel_style = st.selectbox(
            t["style"], STYLE_OPTIONS,
            format_func=lambda x: display_style(x, language)
        )

    if st.button(t["generate"], use_container_width=True):
        if not travel_route:
            st.error("Please select at least one location." if language == "English" else "请至少选择一个地点。")
            st.stop()

        estimated_price = estimate_price(travel_route, days, budget, interests, travel_style)

        ai_plan = None
        try:
            route_text = " → ".join([display_location(x, language) for x in travel_route])
            interests_text = ", ".join([display_interest(x, language) for x in interests])

            with st.spinner(
                "Generating AI itinerary..." if language == "English" else "正在生成AI旅行路线..."
            ):
                ai_plan = api.generate_ai("travel_itinerary", {
                    "customer_name": user_name,
                    "route_text": route_text,
                    "days": days,
                    "budget_text": display_budget(budget, language),
                    "interests_text": interests_text,
                    "style_text": display_style(travel_style, language),
                    "language": language,
                })
        except Exception as e:
            error_str = str(e)
            if "not configured" in error_str:
                st.info(t["no_key"])
            else:
                st.warning(f"AI generation failed. Using fallback. ({error_str})")

        fallback_plan = generate_fallback_itinerary(travel_route, days, language)

        st.metric(t["estimated"], f"${estimated_price} AUD")

        st.markdown("### AI Itinerary" if language == "English" else "### AI旅行路线")

        if ai_plan:
            st.markdown(ai_plan)
        else:
            st.dataframe(pd.DataFrame(fallback_plan), use_container_width=True)

        # Save order via API
        try:
            route_json = json.dumps(travel_route)
            interests_json = json.dumps(interests)
            order_data = {
                "route": route_json,
                "days": days,
                "budget": budget,
                "interests": interests_json,
                "travel_style": travel_style,
                "estimated_price": estimated_price,
                "generate_ai_plan": False,  # Already generated above
            }
            created = api.create_travel_order(order_data)

            st.success(
                f'{t["success"]} Order ID: {created["order_id"]}'
            )
        except Exception as e:
            st.error(f"Failed to save order: {e}")

with tab2:
    try:
        all_orders = api.get_travel_orders()
    except Exception:
        all_orders = []

    if not all_orders:
        st.info(t["no_orders"])
    else:
        rows = []
        for o in all_orders:
            route_display = o.get("route", "Unknown")
            try:
                route_list = json.loads(route_display) if route_display.startswith("[") else [route_display]
                route_display = " → ".join(route_list)
            except Exception:
                pass
            rows.append({
                "Order ID": o.get("order_id"),
                "Route": route_display,
                "Days": o.get("days"),
                "Budget": o.get("budget"),
                "Price AUD": o.get("estimated_price"),
                "Status": o.get("status"),
                "Created At": o.get("created_at"),
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        selected_order_id = st.selectbox(
            "Select Order" if language == "English" else "选择订单",
            [o["order_id"] for o in all_orders]
        )

        selected_order = next(o for o in all_orders if o["order_id"] == selected_order_id)

        st.markdown(f"### {t['order_detail']} — {selected_order.get('order_id', '')}")

        status = selected_order.get("status", "Draft")
        payment = selected_order.get("payment_status", "Unpaid")

        # Status badges
        status_badge = f"🟡 {status}"
        if status == "Paid":
            status_badge = f"🔵 {status}"
        elif status == "Confirmed":
            status_badge = f"🟢 {status} ✅"
        elif status == "Completed":
            status_badge = f"✅ {status}"
        elif status in ("Cancelled", "Refunded"):
            status_badge = f"🔴 {status}"

        payment_badge = f"💳 {payment}"

        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("Status", status_badge)
        col_s2.metric("Payment", payment_badge)
        col_s3.metric("Price", f"${selected_order.get('estimated_price', 0)} AUD")

        st.write("Customer:" if language == "English" else "客户：", user_name)
        st.write("Route:" if language == "English" else "路线：", selected_order.get("route", "Unknown"))
        st.write("Budget:" if language == "English" else "预算：", selected_order.get("budget", "Unknown"))

        # ── Workflow Action Buttons ──
        st.markdown("**Actions:**" if language == "English" else "**操作：**")
        action_cols = st.columns(4)

        with action_cols[0]:
            if status == "Draft" and st.button("💳 Mark as Paid" if language == "English" else "💳 标记已付款", key=f"pay_{selected_order_id}", use_container_width=True):
                try:
                    api.update_travel_order(selected_order_id, {"status": "Paid"})
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed: {e}")

        with action_cols[1]:
            if status == "Paid" and st.button("✅ Confirm Order" if language == "English" else "✅ 确认订单", key=f"confirm_{selected_order_id}", use_container_width=True):
                try:
                    api.update_travel_order(selected_order_id, {"status": "Confirmed"})
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed: {e}")

        with action_cols[2]:
            if status == "Confirmed" and st.button("🏁 Mark Completed" if language == "English" else "🏁 标记完成", key=f"complete_{selected_order_id}", use_container_width=True):
                try:
                    api.update_travel_order(selected_order_id, {"status": "Completed"})
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed: {e}")

        with action_cols[3]:
            if status in ("Draft", "Paid") and st.button("❌ Cancel" if language == "English" else "❌ 取消", key=f"cancel_{selected_order_id}", use_container_width=True):
                try:
                    api.update_travel_order(selected_order_id, {"status": "Cancelled"})
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed: {e}")

        st.divider()

        if selected_order.get("ai_plan"):
            st.markdown(selected_order["ai_plan"])
        else:
            itinerary = selected_order.get("itinerary_json")
            if itinerary:
                try:
                    itinerary_data = json.loads(itinerary) if isinstance(itinerary, str) else itinerary
                    st.dataframe(pd.DataFrame(itinerary_data), use_container_width=True)
                except Exception:
                    pass

with tab3:
    try:
        analytics = api.get_travel_analytics()
    except Exception:
        analytics = {}

    if not analytics or analytics.get("total_orders", 0) == 0:
        st.info(t["no_data"])
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Orders" if language == "English" else "订单总数", analytics["total_orders"])
        c2.metric("Total Revenue Estimate" if language == "English" else "预估总收入", f"${analytics['total_revenue']} AUD")
        c3.metric("Average Order Value" if language == "English" else "平均订单金额", f"${analytics['average_order_value']} AUD")

        st.markdown(f"### {t['route_popularity']}")
        route_pop = analytics.get("route_popularity", {})
        if route_pop:
            route_df = pd.DataFrame(list(route_pop.items()), columns=["Route", "Count"]).set_index("Route")
            st.bar_chart(route_df)

        st.markdown(f"### {t['budget_distribution']}")
        budget_dist = analytics.get("budget_distribution", {})
        if budget_dist:
            budget_df = pd.DataFrame(list(budget_dist.items()), columns=["Budget", "Count"]).set_index("Budget")
            st.bar_chart(budget_df)

        st.markdown(f"### {t['raw_data']}")
        try:
            raw_orders = api.get_travel_orders()
            st.dataframe(pd.DataFrame(raw_orders), use_container_width=True)
        except Exception:
            pass

st.divider()
st.caption(t["footer"])
