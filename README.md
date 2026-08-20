# Chat-bot

A Python AI assistant powered by Groq and LangChain/LangGraph.

## Features
- ReAct Agent with Tool calling capabilities
- Streaming conversational interface
- Preethi AI assistant persona

## Setup
1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your Groq API key:
   ```bash
   copy .env.example .env
   ```
5. Run the application:
   ```bash
   python main.py
   ```
