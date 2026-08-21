# Streamlit AI Chatbot (Groq & LangGraph)

A clean, simple ChatGPT-style web interface powered by **Groq Free-Tier Models** and **LangGraph ReAct Agent**.

## 🌟 Features
- 💬 **Simple ChatGPT UI**: Clean dark-mode conversational UI built with Streamlit.
- 🆓 **Groq Free Tier Models**: Powered by `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, and `gemma2-9b-it`.
- ⚡ **Real-Time Streaming**: Streamed responses directly into the chat interface.
- 🛠️ **ReAct Tools**:
  - `calculator`: Basic arithmetic sum calculation.
  - `say_hello`: Friendly greetings.
- 📜 **Single File Application**: Everything is self-contained cleanly inside `main.py`.

---

## 🚀 How to Run

### 1. Activate Virtual Environment
```bash
.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set API Key
Copy `.env.example` to `.env` and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
*(You can also enter your API key directly in the app sidebar!)*

### 4. Launch the Streamlit App
```bash
streamlit run main.py
```
Open `http://localhost:8501` in your browser.
