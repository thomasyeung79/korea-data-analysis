import streamlit as st
import uuid
from api_client import get_api
from ui_style import apply_product_style, tr

st.set_page_config(
    page_title="Korea Q&A",
    page_icon="💬",
    layout="wide"
)

apply_product_style()

api = get_api()

st.title(tr("💬 Korea Q&A — Ask Anything", "💬 韩国问答 — 想问就问"))

if st.button(tr("🏠 Back to Home", "🏠 返回首页")):
    st.switch_page("app.py")

st.caption(
    tr("Ask questions about Korean culture, technology, travel, sports, society, and more. AI-powered answers.",
       "提问关于韩国文化、科技、旅游、体育、社会等任何问题。AI 智能回答。")
)

st.divider()

# ── Initialize chat history ──
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ── Suggested questions ──
language = st.session_state.get("language", "English")

suggestions_en = [
    "What makes K-pop globally successful?",
    "What are the must-visit places in Seoul?",
    "How did Korea develop so fast economically?",
    "What is Korean work culture like?",
    "Tell me about Korean food culture",
]
suggestions_zh = [
    "K-pop为什么能风靡全球？",
    "首尔有哪些必去的地方？",
    "韩国经济为什么发展这么快？",
    "韩国的职场文化是怎样的？",
    "介绍一下韩国的饮食文化",
]

suggestions = suggestions_zh if language == "中文" else suggestions_en

if not st.session_state.chat_messages:
    st.markdown(f"""
    <div style="text-align:center; padding:2rem; color:#64748b;">
        <p style="font-size:1.1rem;">{tr("Try asking:", "试试问：")}</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(suggestions))
    for i, s in enumerate(suggestions):
        with cols[i]:
            if st.button(s[:20] + "...", use_container_width=True, key=f"suggest_{i}"):
                st.session_state.chat_messages.append({"role": "user", "content": s})
                with st.spinner(tr("Thinking...", "思考中...")):
                    try:
                        reply = api.chat_ai(s, st.session_state.chat_messages[:-1])
                        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": f"⚠️ Error: {e}"
                        })
                st.rerun()

st.divider()

# ── Chat Messages ──
for msg in st.session_state.chat_messages:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; margin-bottom:0.5rem;">
            <div style="background:#123c9c; color:white; padding:0.7rem 1.2rem;
                        border-radius:18px 18px 4px 18px; max-width:70%;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex; margin-bottom:0.5rem;">
            <div style="background:#f1f5f9; color:#111827; padding:0.7rem 1.2rem;
                        border-radius:18px 18px 18px 4px; max-width:70%;
                        border:1px solid #e2e8f0;">
                💡 {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Chat input ──
st.divider()

with st.container():
    col_input, col_btn = st.columns([5, 1])

    with col_input:
        user_input = st.text_input(
            tr("Type your question about Korea...", "输入你关于韩国的提问..."),
            key="chat_input",
            label_visibility="collapsed",
            placeholder=tr("Type your question about Korea...", "输入你关于韩国的提问..."),
        )

    with col_btn:
        send_clicked = st.button(tr("Send", "发送"), use_container_width=True)

    if send_clicked and user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        with st.spinner(tr("Thinking...", "思考中...")):
            try:
                reply = api.chat_ai(user_input, st.session_state.chat_messages[:-1])
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Error: {e}"
                })

        st.rerun()

# ── Clear Chat ──
if st.session_state.chat_messages:
    if st.button(tr("🗑️ Clear Chat History", "🗑️ 清除聊天记录")):
        st.session_state.chat_messages = []
        st.rerun()

st.divider()
st.caption(tr("Powered by KoreaIntel AI • Answers about Korea only", "由 KoreaIntel AI 驱动 • 仅回答韩国相关问题"))
