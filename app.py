import openai
import streamlit as st

MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = "你是一位專業的英文寫作老師，請用繁體中文回覆學生的問題，協助修改、解釋或翻譯英文句子。"

st.set_page_config(page_title="英文寫作小老師", layout="centered")


def get_secret(name):
    """讀取 Streamlit Secrets；沒有設定（或沒有 secrets.toml）時回傳 None。"""
    try:
        return st.secrets[name]
    except Exception:
        return None


# ====== 安全驗證：通關密語（選用，部署時有設定 APP_PASSWORD 才會啟用）======
app_password = get_secret("APP_PASSWORD")

if app_password and not st.session_state.get("authenticated", False):
    st.title("🔒 請輸入通關密語")
    with st.form("password_form"):
        pwd = st.text_input("密碼", type="password")
        submitted = st.form_submit_button("✅ 進入")
        if submitted:
            if pwd == app_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤，請再試一次。")
    st.stop()

# ====== OpenAI API Key：優先使用側邊欄輸入的 Key，其次才是部署時設定的 Secret ======
with st.sidebar:
    st.header("⚙️ 設定")
    user_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Key 只會保存在這次連線的記憶體中，不會被寫入檔案、資料庫或記錄。重新整理頁面後就會清除。",
    )
    st.caption("沒有 Key？可到 OpenAI 平台申請，並建議在後台設定用量上限。")

api_key = user_key.strip() or get_secret("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key) if api_key else None

# ====== 主程式 ======
st.title("✏️ 英文寫作小老師")

if client is None:
    st.info("👈 請先在左側欄輸入你自己的 OpenAI API Key，才能開始使用。")

# 初始化訊息
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 清除對話
if st.button("🧹 清除對話"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.rerun()

# 顯示對話紀錄
for msg in st.session_state.messages[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# 使用者輸入（沒有 Key 時停用輸入框）
user_input = st.chat_input("請輸入你的英文句子", disabled=client is None)
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("小老師思考中..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                )
                reply = response.choices[0].message.content
            except openai.AuthenticationError:
                reply = "⚠️ API Key 無效或已過期，請在左側欄重新輸入。"
            except Exception as e:
                reply = f"⚠️ 發生錯誤：{e}"
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
