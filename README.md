# ⚡ Dynamo AI — Next-Gen Conversational Web Assistant & Tool Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-API-F55034?style=for-the-badge&logo=lightning&logoColor=white)](https://groq.com/)
[![LangChain / LangGraph](https://img.shields.io/badge/LangGraph-ReAct_Agent-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**Dynamo AI** is a sleek, ultra-fast, and modern web AI assistant powered by **Groq Free-Tier Models** and **LangGraph ReAct Agents**. Built with Streamlit, it features a glassmorphic user interface, real-time streaming responses, right-aligned user prompt bubbles, left-aligned AI responses with interactive action controls, built-in tool execution, and seamless deployment support for **Streamlit Community Cloud (Free Tier)**.

---

## 🌟 Features & Highlights

- 🎨 **Modern Glassmorphic Interface**:
  - Dynamic gradient branding badge with custom Google Fonts (`Outfit` & `Plus Jakarta Sans`).
  - **User Prompts**: Right-aligned pill bubbles with glowing gradients (`linear-gradient(135deg, #1d4ed8, #1e40af)`).
  - **Dynamo AI Responses**: Left-aligned glassmorphic card containers with soft drop shadows and real-time streaming output.
  - **Interactive Action Controls**: Embedded action bar (`📋 Copy`, `📤 Share`, `🔄 Retry`, `👍 Like`, `••• More`) underneath AI responses.
  - **Welcome Hero Section**: Interactive prompt suggestions displayed when the chat history is empty.

- ⚡ **High-Speed Groq Free-Tier Models**:
  - `llama-3.3-70b-versatile` *(Default)*
  - `qwen/qwen3.6-27b`
  - `llama-3.1-8b-instant`
  - `mixtral-8x7b-32768`
  - `gemma2-9b-it`

- 🧠 **LangGraph ReAct Agent & Tool Execution**:
  - Seamless agent reasoning with automatic tool calling.
  - **`calculator`**: Solves arithmetic calculations (`sum`).
  - **`say_hello`**: Provides personalized greetings.

- 🎛️ **Sidebar Control Panel & Dual Configuration**:
  - Live model switcher selectbox.
  - Automatic API key resolution from environment variables (`.env`) or **Streamlit Cloud Secrets** (`st.secrets`).
  - Sidebar API Key override for on-the-fly key updates.
  - One-click **Clear Chat History** button.

---

## 📁 Repository Structure

```text
Chat-Bot/
├── main.py                          # Main Streamlit application & LangGraph ReAct agent logic
├── requirements.txt                 # Python dependency specifications
├── .env.example                     # Template for required environment variables
├── .gitignore                       # Git version control ignore configuration (protects .env & secrets)
├── .streamlit/
│   ├── config.toml                  # Streamlit UI theme and server settings
│   └── secrets.toml.example         # Template for Streamlit Community Cloud Secrets configuration
└── README.md                        # Comprehensive project documentation
```

---

## 🚀 Quick Start Guide (Local Development)

### 1. Clone & Navigate to Repository
```bash
git clone https://github.com/deekshith185/Chat-Bot.git
cd Chat-Bot
```

### 2. Activate Virtual Environment
```bash
# Windows (PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and add your Groq API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
# Groq API Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here

# Selected Groq Model (Default: llama-3.3-70b-versatile)
GROQ_MODEL=llama-3.3-70b-versatile
```
*(Note: You can also input or update your API key at runtime inside the Streamlit sidebar!)*

### 5. Run the Application
```bash
streamlit run main.py
```
Open **`http://localhost:8501`** in your browser.

---

## 🌐 Deploy to Streamlit Community Cloud (Free Tier)

Deploying Dynamo AI to Streamlit Community Cloud takes less than 2 minutes:

### Step 1: Sign In & Connect GitHub
1. Go to **[share.streamlit.io](https://share.streamlit.io/)**.
2. Click **Sign in** and authorize with your GitHub account.

### Step 2: Deploy New App
1. Click **Create app** $\rightarrow$ **I already have an app**.
2. Fill in the repository settings:
   - **Repository:** `deekshith185/Chat-Bot`
   - **Branch:** `main`
   - **Main file path:** `main.py`

### Step 3: Add Streamlit Secrets
1. Click **Advanced settings...** (or go to **App Settings > Secrets**).
2. Paste your Groq API credentials in TOML format:
   ```toml
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   ```
3. Click **Save**.

### Step 4: Launch!
1. Click **Deploy!**. Streamlit will build your app and make it live online.

---

## 🔑 Obtaining a Free Groq API Key

1. Sign up or log in at the [Groq Console](https://console.groq.com/).
2. Navigate to **API Keys** section and click **Create API Key**.
3. Copy your key and add it to your `.env` file, Streamlit Secrets, or directly in the sidebar.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit, Custom CSS (Glassmorphism, Google Fonts) |
| **LLM Provider** | Groq LPU (Speed-optimized inference) |
| **Agent Framework**| LangGraph ReAct Agent, LangChain Groq |
| **Hosting / Cloud**| Streamlit Community Cloud (Free Tier) |
| **Language** | Python 3.10+ |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
