import streamlit as st
import openai

# 使用 Streamlit 的 secrets 儲存 API 金鑰（請在 Streamlit 部署時設定）
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="英文寫作小老師", layout="centered")
st.title("✏️ 英文寫作小老師")
st.markdown("請輸入你的英文句子，我會幫你檢查、翻譯或潤飾。")

# 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一位專業的英文寫作老師，請用繁體中文回覆學生的問題，協助修改、解釋或翻譯英文句子。"}
    ]

# 使用者輸入表單
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("輸入你的句子...", height=100)
    submitted = st.form_submit_button("送出")

# 呼叫 GPT
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("小老師思考中..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ 發生錯誤：{e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

# 顯示聊天紀錄
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"🧑‍🎓 **你：** {msg['content']}")
    else:
        st.markdown(f"👩‍🏫 **小老師：** {msg['content']}")