import streamlit as st
import openai

# ====== 安全驗證：通關密語 ======
PASSWORD = "teacher123"  # 可自行更改
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 請輸入通關密語")
    pwd = st.text_input("密碼", type="password")
    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.experimental_rerun()
    else:
        st.stop()

# ====== 通過密碼後的主程式 ======
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="英文寫作小老師", layout="centered")
st.title("✏️ 英文寫作小老師")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一位專業的英文寫作老師，請用繁體中文回覆學生的問題，協助修改、解釋或翻譯英文句子。"}
    ]

if st.button("🧹 清除對話"):
    st.session_state.messages = [
        {"role": "system", "content": "你是一位專業的英文寫作老師，請用繁體中文回覆學生的問題，協助修改、解釋或翻譯英文句子。"}
    ]
    st.experimental_rerun()

for msg in st.session_state.messages[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

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