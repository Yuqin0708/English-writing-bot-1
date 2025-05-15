import streamlit as st
import openai

# ====== 安全驗證：通關密語 ======
PASSWORD = st.secrets["APP_PASSWORD"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.set_page_config(page_title="驗證中", layout="centered")
    st.title("🔒 請輸入通關密語")
    with st.form("password_form"):
        pwd = st.text_input("密碼", type="password")
        submitted = st.form_submit_button("✅ 進入")
        if submitted:
            if pwd == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()  # ✅ 新版 Streamlit 要用 st.rerun()
            else:
                st.error("❌ 密碼錯誤，請再試一次。")
    st.stop()

# ====== 通過密碼後的主程式 ======
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="英文寫作小老師", layout="centered")
st.title("✏️ 英文寫作小老師")

# 初始化訊息
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一位專業的英文寫作老師，請用繁體中文回覆學生的問題，協助修改、解釋或翻譯英文句子。"}
    ]

# 清除對話
if st.button("🧹 清除對話"):
    st.session_state.messages = [
        {"role": "system", "content": "你是一位專業的英文寫作老師，請用繁體中文回覆學生的問題，協助修改、解釋或翻譯英文句子。"}
    ]
    st.rerun()

# 顯示對話紀錄
for msg in st.session_state.messages[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# 使用者輸入
user_input = st.chat_input("請輸入你的英文句子")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("小老師思考中..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ 發生錯誤：{e}"
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
