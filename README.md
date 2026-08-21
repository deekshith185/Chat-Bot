# 🤖 Dynamo AI — Streamlit ChatGPT Assistant (Groq & LangGraph)

A sleek, modern ChatGPT-style conversational Web AI Assistant powered by **Groq Free-Tier Models** and **LangGraph ReAct Agent**, built with Streamlit.

---

## 🌟 Key Features

- 💬 **ChatGPT UI Experience**: 
  - User prompts rendered in right-aligned dark blue capsule bubbles (`#1a4a84`).
  - Assistant responses aligned cleanly on the left with interactive action controls (`📋 Copy`, `📤 Share`, `🔄 Regenerate`, `•••`).
  - Dark mode design (`#0d0d0d`).
- ⚡ **Groq Free-Tier LLMs**: Supports high-speed streaming inference with top open-weights models:
  - `llama-3.3-70b-versatile` *(Default)*
  - `qwen/qwen3.6-27b`
  - `llama-3.1-8b-instant`
  - `mixtral-8x7b-32768`
  - `gemma2-9b-it`
- 🧠 **LangGraph ReAct Agent**: Reasoning and tool-use capabilities using custom agents.
- 🛠️ **Built-in Agent Tools**:
  - `calculator`: Performs arithmetic computations.
  - `say_hello`: Responds with greetings.
- 🎛️ **Sidebar Controls**: Dynamic model selector, API key input, and instant chat history reset.
- 📜 **Single-File Architecture**: Clean, modular structure maintained inside [`main.py`](main.py).

---

## 📁 Repository Structure

```text
workshop_2026/
├── main.py              # Main Streamlit application & LangGraph agent
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Clone & Navigate to Repository
```bash
git clone https://github.com/deekshith185/Chat-Bot.git
cd Chat-Bot
```

### 2. Activate Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and insert your free Groq API Key:
```bash
cp .env.example .env
```
Inside `.env`:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
*(Note: You can also enter your API key directly in the app sidebar at runtime!)*

### 5. Launch the Streamlit App
```bash
streamlit run main.py
```
Open **`http://localhost:8501`** in your browser.

---

## 🔑 Getting a Free Groq API Key

1. Sign up or log in at [Groq Console](https://console.groq.com/).
2. Navigate to **API Keys** and click **Create API Key**.
3. Paste your key into `.env` or the Streamlit sidebar input.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
