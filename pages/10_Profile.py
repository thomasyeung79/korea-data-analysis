import streamlit as st
from api_client import get_api
from ui_style import apply_product_style, tr

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)

apply_product_style()

api = get_api()

st.title(tr("👤 My Profile", "👤 个人中心"))

if st.button(tr("🏠 Back to Home", "🏠 返回首页")):
    st.switch_page("app.py")

st.divider()

# ── Account Info ──
st.subheader(tr("📋 Account Information", "📋 账户信息"))

user = api.user
if user:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>{tr("Username", "用户名")}</h3>
            <p style="font-size:1.4rem; font-weight:700;">{user['username']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        created = user.get("created_at", "")
        if created:
            created = created[:10]
        st.markdown(f"""
        <div class="card">
            <h3>{tr("Member Since", "注册时间")}</h3>
            <p style="font-size:1.4rem; font-weight:700;">{created}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Language Settings ──
st.subheader(tr("🌐 Language Preference", "🌐 语言偏好"))

lang = st.selectbox(
    tr("Interface Language", "界面语言"),
    ["English", "中文"],
    index=0 if user.get("language_preference", "English") == "English" else 1,
    key="profile_language"
)

if st.button(tr("Update Language", "更新语言"), use_container_width=True):
    try:
        api.update_language(lang)
        st.success(tr("Language preference updated!", "语言偏好已更新！"))
    except Exception as e:
        st.error(f"Failed to update language: {e}")

st.divider()

# ── Change Password ──
st.subheader(tr("🔑 Change Password", "🔑 修改密码"))

with st.form("change_password_form"):
    old_pw = st.text_input(tr("Current Password", "当前密码"), type="password")
    new_pw = st.text_input(tr("New Password", "新密码"), type="password")
    confirm_pw = st.text_input(tr("Confirm New Password", "确认新密码"), type="password")

    if st.form_submit_button(tr("Change Password", "修改密码"), use_container_width=True):
        if not old_pw or not new_pw:
            st.error(tr("Please fill in all fields.", "请填写所有字段。"))
        elif new_pw != confirm_pw:
            st.error(tr("New passwords do not match.", "两次输入的新密码不一致。"))
        elif len(new_pw) < 4:
            st.error(tr("Password must be at least 4 characters.", "密码至少需要4个字符。"))
        else:
            try:
                result = api.change_password(old_pw, new_pw)
                st.success(tr("Password changed successfully!", "密码修改成功！"))
            except Exception as e:
                st.error(f"Failed: {e}")

st.divider()

# ── My Activity Stats ──
st.subheader(tr("📊 My Activity", "📊 我的活动"))

try:
    module_scores = api.get_module_scores()
    perception_results = api.get_perception_results()
    travel_orders = api.get_travel_orders()

    col1, col2, col3 = st.columns(3)
    col1.metric(tr("Module Scores Saved", "已保存模块评分"), len(module_scores))
    col2.metric(tr("Perception Reports", "认知报告"), len(perception_results))
    col3.metric(tr("Travel Orders", "旅行订单"), len(travel_orders))
except Exception:
    st.info(tr("Login required to view activity.", "登录后查看活动数据。"))

st.divider()
st.caption(tr("KoreaIntel Pro • User Profile", "KoreaIntel Pro • 用户中心"))
