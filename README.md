# ✏️ English Writing Bot 小老師

這是一個使用 OpenAI API 建立的英文寫作輔助機器人。  
可以幫助你修正英文句子、提供更自然的寫法、或將中文翻譯成英文。

---

## 🔧 功能特色

- ✅ 文法錯誤提示與說明（繁體中文回覆）
- ✍️ 更自然的英文建議
- 🌐 支援中翻英
- 🧑‍🏫 對話式介面，像和老師聊天一樣
- 🔑 自帶 API Key：在側邊欄輸入你自己的 OpenAI API Key 即可使用，Key 只保存在這次連線的記憶體中，不會被寫入檔案、資料庫或記錄
- 🔒 選用的通關密語保護（部署時設定 `APP_PASSWORD` 才會啟用）

---

## 🚀 使用方式

### ✅ 雲端版本（Streamlit）

本專案部署於 Streamlit Cloud，可透過網址直接開啟應用程式。  
👉 [點我開啟 App](https://english-writing-bot-1branchmainmainfilepathapppy-ebutpqebra9xq.streamlit.app/)

開啟後，請在**左側欄輸入你自己的 OpenAI API Key**（可到 OpenAI 平台申請）即可開始使用。

---

## 🛠 開發技術

- Python
- Streamlit
- OpenAI API（`gpt-4o-mini`）
- GitHub + Streamlit Cloud 自動部署

---

## 🧪 本機測試（可選）

```bash
pip install -r requirements.txt
streamlit run app.py
```

啟動後，在左側欄輸入你的 OpenAI API Key 即可使用。

如果想預先設定 Key，可以建立 `.streamlit/secrets.toml`（已被 `.gitignore` 排除，請勿提交到 Git）：

```toml
OPENAI_API_KEY = "sk-..."
APP_PASSWORD = "your-passphrase"   # 選用；有設定才會啟用通關密語
```
