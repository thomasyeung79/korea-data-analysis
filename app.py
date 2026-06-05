import streamlit as st
from api_client import APIClient, get_api
from ui_style import apply_product_style, language_selector, tr

# ── Auth Guard ──

api = get_api()

if not api.is_authenticated:
    st.set_page_config(
        page_title="KoreaIntel Pro",
        page_icon="🌏",
        layout="wide"
    )
    apply_product_style()

    st.markdown(
        """
    <div class="product-hero" style="margin-bottom: 2rem;">
        <section class="hero-panel">
            <div class="brand-row"><span class="brand-dot"></span>KoreaIntel Pro</div>
            <h1>Korea market and culture intelligence workspace</h1>
            <p>Turn Korea-related culture, tourism, technology, sports, and society signals
            into usable decisions for brands, creators, travel teams, and learners.</p>
        </section>
        <aside class="hero-aside">
            <div>
                <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>Decision cockpit</div>
                <h3 style="margin-top:1.2rem;">From curiosity to action</h3>
                <p style="color:#cbd5e1;">
                    Choose a goal, read the market context, explore the tools,
                    then generate a decision-ready final report.
                </p>
            </div>
        </aside>
    </div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form("login_form"):
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.form_submit_button("Login", use_container_width=True):
                if not login_user or not login_pass:
                    st.error("Please enter username and password.")
                else:
                    try:
                        api.login(login_user, login_pass)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Login failed: {e}")

    with tab_register:
        with st.form("register_form"):
            reg_user = st.text_input("Username", key="reg_user")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2")
            if st.form_submit_button("Register", use_container_width=True):
                if not reg_user or not reg_pass:
                    st.error("Please fill in all fields.")
                elif reg_pass != reg_pass2:
                    st.error("Passwords do not match.")
                elif len(reg_pass) < 4:
                    st.error("Password must be at least 4 characters.")
                else:
                    try:
                        api.register(reg_user, reg_pass)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Registration failed: {e}")

    st.stop()

# ── Authenticated User ──

def show_optional_music(title, artist, url, start=0):
    video_id = url.split("v=")[-1].split("&")[0]

    with st.expander("🎵 Optional Music (Official Source)"):
        st.caption(f"Now Playing: {title} - {artist}")

        st.markdown(f"""
        <iframe
            width="360"
            height="203"
            src="https://www.youtube.com/embed/{video_id}?start={start}"
            frameborder="0"
            allowfullscreen>
        </iframe>
        """, unsafe_allow_html=True)

        st.caption("Music via official YouTube embed.")

st.set_page_config(
    page_title="KoreaIntel Pro",
    page_icon="🌏",
    layout="wide"
)

apply_product_style()

# Language selector with backend sync
lang = language_selector("home_language")
if api.user.get("language_preference") != lang:
    try:
        api.update_language(lang)
    except Exception:
        pass

# Logout button in sidebar-like position
col_logout1, col_logout2, col_logout3 = st.columns([6, 1, 1])
with col_logout2:
    st.caption(f"👤 {api.user['username']}")
with col_logout3:
    if st.button("Logout"):
        api.logout()
        st.rerun()

user_name = api.user["username"]

st.markdown(
    f"""
<div class="product-hero">
    <section class="hero-panel">
        <div class="brand-row"><span class="brand-dot"></span>{tr("KoreaIntel Pro", "KoreaIntel Pro")}</div>
        <h1>{tr("Korea market and culture intelligence workspace", "韩国市场与文化智能工作台")}</h1>
        <p>
            {tr(
                "Turn Korea-related culture, tourism, technology, sports, and society signals into usable decisions for brands, creators, travel teams, and learners.",
                "把韩国相关的文化、旅游、科技、体育与社会信号转化为品牌、创作者、旅游团队和学习者可以直接使用的决策。"
            )}
        </p>
        <div class="hero-kpi">
            <div class="kpi-card"><strong>4</strong><span>{tr("launch use cases", "商业场景")}</span></div>
            <div class="kpi-card"><strong>8</strong><span>{tr("intelligence tools", "智能工具")}</span></div>
            <div class="kpi-card"><strong>AI</strong><span>{tr("reports and itineraries", "报告与路线")}</span></div>
        </div>
    </section>
    <aside class="hero-aside">
        <div>
            <div class="brand-row" style="color:#cbd5e1;"><span class="brand-dot"></span>{tr("Decision cockpit", "决策驾驶舱")}</div>
            <h3 style="margin-top:1.2rem;">{tr("From curiosity to action", "从兴趣到行动")}</h3>
            <p style="color:#cbd5e1;">
                {tr(
                    "Choose a goal, read the market context, explore the tools, then generate a decision-ready final report.",
                    "选择目标，理解市场背景，使用工具模块，最后生成可用于决策的报告。"
                )}
            </p>
        </div>
        <div class="insight-card" style="background:#111c33;border-color:#26344f;">
            <p style="margin:0;color:#dbeafe;">{tr("Product direction: market entry, tourism planning, culture strategy, and education workflows.", "产品方向：市场进入、旅游规划、文化策略与教育学习工作流。")}</p>
        </div>
    </aside>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<div class="section-label">{tr("Workspace setup", "工作区设置")}</div>', unsafe_allow_html=True)
st.subheader(tr("Create a working profile", "创建工作档案"))

profile_col, role_col = st.columns([1, 1])

with profile_col:
    st.text_input(
        tr("Workspace name", "工作区名称"),
        value=user_name,
        disabled=True,
        help=tr("Username from your account", "来自您的账户用户名")
    )

role_options = {
    "brand": tr("Brand / market entry", "品牌 / 市场进入"),
    "travel": tr("Travel planner / tourism operator", "旅行规划 / 旅游运营"),
    "creator": tr("Creator / culture strategist", "创作者 / 文化策略"),
    "learner": tr("Student / researcher", "学生 / 研究者"),
}

with role_col:
    selected_role = st.selectbox(
        tr("Primary goal", "主要目标"),
        list(role_options.keys()),
        format_func=lambda key: role_options[key],
        index=0,
    )
    st.session_state["product_role"] = selected_role

st.success(
    tr(f"{user_name} workspace is ready.", f"{user_name} 工作区已准备好。")
)

role_recommendations = {
    "brand": (
        tr("Recommended path", "推荐路径"),
        tr("Start with Analysis and Technology, then use Culture to design positioning, and finish with Final Evaluation for an executive-style report.", "先看数据分析和科技模块，再用文化模块设计定位，最后进入最终评估生成管理层风格报告。"),
    ),
    "travel": (
        tr("Recommended path", "推荐路径"),
        tr("Start with Tourism, open the AI trip planner, then review Culture and Society to make the experience more realistic.", "先进入旅游模块和 AI 路线规划，再查看文化与社会模块，让体验设计更真实。"),
    ),
    "creator": (
        tr("Recommended path", "推荐路径"),
        tr("Start with Culture and K-pop intelligence, then compare Society and Sports to find stories beyond entertainment.", "先看文化和 K-pop 智能分析，再对比社会与体育，寻找娱乐之外的内容故事。"),
    ),
    "learner": (
        tr("Recommended path", "推荐路径"),
        tr("Start with History, move through Analysis and Society, then use Final Evaluation to test your understanding.", "先从历史开始，再进入数据分析与社会模块，最后用最终评估测试理解。"),
    ),
}

rec_title, rec_body = role_recommendations[selected_role]

st.markdown(
    f"""
<div class="insight-card">
    <div class="module-tag">{rec_title}</div>
    <p style="margin-bottom:0;">{rec_body}</p>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<div class="section-label">{tr("Launch use cases", "上市级使用场景")}</div>', unsafe_allow_html=True)
use1, use2, use3, use4 = st.columns(4)

with use1:
    st.markdown(
        f"""
        <div class="module-card">
            <div class="module-tag">{tr("Go-to-market", "市场进入")}</div>
            <h3>{tr("Brand Strategy", "品牌策略")}</h3>
            <p>{tr("Find cultural hooks, risk signals, and audience narratives before launching Korea-related products.", "在推出韩国相关产品前，找到文化切入点、风险信号和受众叙事。")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with use2:
    st.markdown(
        f"""
        <div class="module-card">
            <div class="module-tag">{tr("Travel ops", "旅游运营")}</div>
            <h3>{tr("Trip Builder", "行程生成")}</h3>
            <p>{tr("Generate city routes, estimate budgets, and store customer travel orders.", "生成城市路线、估算预算，并保存客户旅行订单。")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with use3:
    st.markdown(
        f"""
        <div class="module-card">
            <div class="module-tag">{tr("Culture", "文化")}</div>
            <h3>{tr("Content Radar", "内容雷达")}</h3>
            <p>{tr("Use K-pop, drama, sports, and lifestyle signals to plan campaigns or creator topics.", "利用 K-pop、韩剧、体育和生活方式信号规划活动或创作者选题。")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with use4:
    st.markdown(
        f"""
        <div class="module-card">
            <div class="module-tag">{tr("Learning", "学习")}</div>
            <h3>{tr("Korea Briefing", "韩国简报")}</h3>
            <p>{tr("Turn complex country context into a structured briefing for class, research, or team discussion.", "把复杂的国家背景整理成课堂、研究或团队讨论可用的结构化简报。")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(f'<div class="section-label">{tr("Product tools", "产品工具")}</div>', unsafe_allow_html=True)
st.markdown(f"## {tr('Choose the next tool', '选择下一步工具')}")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Context", "背景")}</div>
        <h3>📜 {tr("Country Context", "国家背景")}</h3>
        <p class="small-text">{tr("Build historical context before making market or culture decisions.", "在做市场或文化决策前建立历史背景。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open History", "打开历史模块"), use_container_width=True):
        st.switch_page("pages/1_History.py")

with col2:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Benchmark", "对标")}</div>
        <h3>📊 {tr("Market Signals", "市场信号")}</h3>
        <p class="small-text">{tr("Compare Korea with regional peers and convert perception into decision context.", "对比韩国与区域竞争者，把认知转化为决策背景。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Analysis", "打开分析模块"), use_container_width=True):
        st.switch_page("pages/2_Analysis.py")

with col3:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Industry", "产业")}</div>
        <h3>💻 {tr("Tech & Industry", "科技与产业")}</h3>
        <p class="small-text">{tr("Assess technology credibility, infrastructure, and industrial strengths.", "评估韩国的科技可信度、基础设施与产业优势。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Technology", "打开科技模块"), use_container_width=True):
        st.switch_page("pages/3_Technology.py")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Demand", "需求")}</div>
        <h3>🎤 {tr("Culture Strategy", "文化策略")}</h3>
        <p class="small-text">{tr("Map culture demand, K-pop systems, drama influence, and brand storytelling angles.", "梳理文化需求、K-pop 系统、韩剧影响与品牌叙事角度。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Culture", "打开文化模块"), use_container_width=True):
        st.switch_page("pages/4_Culture.py")

with col5:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Talent", "人才")}</div>
        <h3>⚽ {tr("Sports Visibility", "体育可见度")}</h3>
        <p class="small-text">{tr("Use football and sports pathways to understand visibility, talent, and national image.", "通过足球与体育路径理解可见度、人才流动和国家形象。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Sports", "打开体育模块"), use_container_width=True):
        st.switch_page("pages/5_Sports.py")

with col6:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Reality check", "现实校准")}</div>
        <h3>🧠 {tr("Society & Users", "社会与用户")}</h3>
        <p class="small-text">{tr("Check lifestyle, work pressure, user expectations, and social trade-offs.", "校准生活方式、工作压力、用户预期与社会取舍。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Society", "打开社会模块"), use_container_width=True):
        st.switch_page("pages/6_Society.py")

col7, col8, col9, col10 = st.columns(4)

with col7:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Operations", "运营")}</div>
        <h3>✈️ {tr("Tourism Builder", "旅游构建器")}</h3>
        <p class="small-text">{tr("Design Korea travel experiences, customer routes, and order records.", "设计韩国旅行体验、客户路线和订单记录。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Tourism", "打开旅游模块"), use_container_width=True):
        st.switch_page("pages/7_Tourism.py")

with col8:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Report", "报告")}</div>
        <h3>🏁 {tr("Decision Report", "决策报告")}</h3>
        <p class="small-text">{tr("Turn module signals into a final strategic brief and saved user profile.", "把模块信号整合成最终战略简报和用户档案。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Final Evaluation", "打开最终评估"), use_container_width=True):
        st.switch_page("pages/8_Ending.py")

with col9:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("AI", "AI")}</div>
        <h3>💬 {tr("Korea Q&A", "韩国问答")}</h3>
        <p class="small-text">{tr("Ask anything about Korea — culture, travel, tech, sports, society.", "提问关于韩国的任何问题——文化、旅游、科技、体育、社会。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Chat", "打开问答"), use_container_width=True):
        st.switch_page("pages/11_AI_Chat.py")

with col10:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-tag">{tr("Account", "账户")}</div>
        <h3>👤 {tr("My Profile", "个人中心")}</h3>
        <p class="small-text">{tr("Change password, update preferences, view activity.", "修改密码、更新偏好、查看活动记录。")}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button(tr("Open Profile", "打开个人中心"), use_container_width=True):
        st.switch_page("pages/10_Profile.py")

st.markdown(f'<div class="section-label">{tr("Customer memory", "客户记忆")}</div>', unsafe_allow_html=True)
st.subheader(tr("Saved workspaces and reports", "已保存工作区与报告"))

st.caption(tr("Review saved profiles, perception scores, and generated AI reports.", "查看已保存的档案、认知评分和 AI 报告。"))

if st.button(tr("Open User History", "打开用户历史"), use_container_width=True):
    st.switch_page("pages/9_User_History.py")
