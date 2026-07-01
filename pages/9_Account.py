import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import API_BASE_URL, APIClient
from locales.i18n import get_language, language_selector, t
from ui_style import apply_product_style

st.set_page_config(page_title="账号中心" if get_language() == "zh" else "Account", page_icon="👤", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


def current_user() -> dict | None:
    if not st.session_state.get("auth_token"):
        return None
    if st.session_state.get("current_user"):
        return st.session_state["current_user"]
    try:
        user = api.me()
        st.session_state["current_user"] = user
        return user
    except Exception:
        return None


language_selector("account_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V2.2</div>
    <h1>{label("Account", "账号中心")}</h1>
    <p>{label("Log in to save profiles and planning history. You can still use Korea Compass in demo mode without an account.", "登录后可以保存个人画像和历史规划；不登录也可以继续使用演示模式。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Personalization", "个性化")}</h3>
    <p>{label("JWT-based portfolio authentication for profile, city recommendation, and life plan history.", "作品集级 JWT 登录，用于个人画像、城市推荐和发展规划历史。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

if not API_BASE_URL:
    st.warning(
        label(
            "Backend API is required for account login. Demo mode remains available.",
            "账号登录需要后端 API。当前仍可使用演示模式。",
        )
    )

user = current_user()
if user:
    st.success(label("You are logged in.", "你已登录。"))
    c1, c2 = st.columns(2)
    c1.metric(label("Display name", "显示名称"), user["display_name"])
    c2.metric("Email", user["email"])
    if st.button(label("Logout", "退出登录"), type="primary"):
        api.set_token(None)
        st.session_state.pop("current_user", None)
        st.rerun()
else:
    st.info(
        label(
            "Demo mode. Log in to save profiles and planning history.",
            "当前为演示模式。登录后可以保存个人画像和历史规划。",
        )
    )

tab_login, tab_register = st.tabs([label("Login", "登录"), label("Register", "注册")])

with tab_login:
    st.markdown(f"## {label('Login', '登录')}")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input(label("Password", "密码"), type="password", key="login_password")
    if st.button(label("Login", "登录"), use_container_width=True, type="primary", key="login_button"):
        try:
            result = api.login(login_email, login_password)
            st.session_state["current_user"] = result["user"]
            st.success(label("Login successful.", "登录成功。"))
            st.rerun()
        except Exception as exc:
            st.error(label(f"Login failed: {exc}", f"登录失败：{exc}"))

with tab_register:
    st.markdown(f"## {label('Register', '注册')}")
    register_name = st.text_input(label("Display name", "显示名称"), key="register_name")
    register_email = st.text_input("Email", key="register_email")
    register_password = st.text_input(label("Password", "密码"), type="password", key="register_password")
    if st.button(label("Register", "注册"), use_container_width=True, type="primary", key="register_button"):
        try:
            result = api.register(register_email, register_name, register_password)
            st.session_state["current_user"] = result["user"]
            st.success(label("Registration successful.", "注册成功。"))
            st.rerun()
        except Exception as exc:
            st.error(label(f"Registration failed: {exc}", f"注册失败：{exc}"))

st.caption(t("common.footer"))
