import html
import os
import warnings
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Load environment variables
load_dotenv()

# --- Custom Agent Tools ---

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with two numbers (sum)."""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str = "there") -> str:
    """Useful for greeting a user when a name is provided or to say hello."""
    return f"Hello {name}, I hope you are having an exceptional day!"


# Free-tier Groq models
FREE_TIER_MODELS = [
    "llama-3.3-70b-versatile",
    "qwen/qwen3.6-27b",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]


def render_user_message(content: str):
    """Renders user prompt in a right-aligned gradient pill bubble with soft glow."""
    escaped_content = html.escape(content).replace("\n", "<br>")
    st.markdown(f'''
        <div style="display: flex; justify-content: flex-end; margin: 16px 0 20px 0; width: 100%;">
            <div style="
                background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
                color: #ffffff;
                padding: 12px 20px;
                border-radius: 24px;
                max-width: 78%;
                font-size: 15.5px;
                line-height: 1.55;
                font-weight: 400;
                word-break: break-word;
                border: 1px solid rgba(255, 255, 255, 0.18);
                box-shadow: 0 6px 20px rgba(29, 78, 216, 0.35);
            ">
                {escaped_content}
            </div>
        </div>
    ''', unsafe_allow_html=True)


def render_assistant_actions():
    """Renders sleek interactive action buttons underneath Dynamo AI responses."""
    st.markdown('''
        <div style="display: flex; align-items: center; gap: 16px; margin-top: 10px; margin-bottom: 24px; padding-left: 4px;">
            <button style="background: none; border: none; color: #94a3b8; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all 0.2s;" title="Copy response">
                📋 <span style="font-size: 13px;">Copy</span>
            </button>
            <button style="background: none; border: none; color: #94a3b8; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all 0.2s;" title="Share">
                📤 <span style="font-size: 13px;">Share</span>
            </button>
            <button style="background: none; border: none; color: #94a3b8; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all 0.2s;" title="Regenerate">
                🔄 <span style="font-size: 13px;">Retry</span>
            </button>
            <button style="background: none; border: none; color: #94a3b8; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all 0.2s;" title="Good response">
                👍
            </button>
            <button style="background: none; border: none; color: #94a3b8; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all 0.2s;" title="More actions">
                •••
            </button>
        </div>
    ''', unsafe_allow_html=True)


def render_welcome_hero():
    """Renders a welcome hero section when chat history is empty."""
    st.markdown('''
        <div style="
            text-align: center;
            padding: 40px 20px;
            margin: 20px 0 35px 0;
            background: radial-gradient(circle at center, rgba(99, 102, 241, 0.08) 0%, rgba(13, 13, 18, 0) 70%);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        ">
            <div style="font-size: 48px; margin-bottom: 12px; filter: drop-shadow(0 0 16px rgba(99, 102, 241, 0.4));">⚡</div>
            <h2 style="
                font-family: 'Outfit', sans-serif;
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 8px;
                background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">Welcome to Dynamo AI</h2>
            <p style="color: #94a3b8; font-size: 16px; max-width: 500px; margin: 0 auto 28px auto; line-height: 1.6;">
                Your intelligent, ultra-fast Web Assistant powered by Groq & LangGraph ReAct Agents.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; max-width: 700px; margin: 0 auto;">
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px; text-align: left; cursor: pointer;">
                    <div style="font-size: 20px; margin-bottom: 6px;">🧮 Tool Integration</div>
                    <div style="color: #64748b; font-size: 13.5px;">Perform arithmetic with custom agent tools</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px; text-align: left; cursor: pointer;">
                    <div style="font-size: 20px; margin-bottom: 6px;">⚡ Ultra-Fast Streaming</div>
                    <div style="color: #64748b; font-size: 13.5px;">Real-time responses powered by Groq free tier</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 16px; text-align: left; cursor: pointer;">
                    <div style="font-size: 20px; margin-bottom: 6px;">💡 Problem Solving</div>
                    <div style="color: #64748b; font-size: 13.5px;">Ask code, logic, or conversational queries</div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Dynamo AI - Intelligent Web Assistant",
        page_icon="⚡",
        layout="centered"
    )

    # --- Custom Modern Aesthetic Styling ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, .stApp {
        background-color: #0b0c10;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container constraints */
    .block-container {
        max-width: 820px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* Main Title Styling */
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 34px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
    }

    /* Sidebar Theme Styling */
    section[data-testid="stSidebar"] {
        background-color: #111319 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .stSidebar .stSelectbox > div > div, .stSidebar .stTextInput > div > div > input {
        background-color: #1a1d26 !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
    }

    .stSidebar .stButton > button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
    }

    .stSidebar .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.35);
    }

    /* Chat input styling */
    div[data-testid="stChatInput"] {
        border-radius: 28px;
        background-color: #161821;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3) !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0c10;
    }
    ::-webkit-scrollbar-thumb {
        background: #272a37;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar Settings ---
    st.sidebar.markdown('''
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="font-size: 28px;">⚡</div>
            <div>
                <h3 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 20px; color: #ffffff;">Dynamo AI</h3>
                <span style="font-size: 12px; color: #64748b;">Control Panel</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Safe helper to fetch configuration from os env or Streamlit secrets
    def get_config_val(key: str, default: str = "") -> str:
        val = os.getenv(key, "")
        if not val and hasattr(st, "secrets"):
            try:
                val = st.secrets.get(key, default)
            except Exception:
                val = default
        return val if val else default

    env_api_key = get_config_val("GROQ_API_KEY", "")
    api_key = st.sidebar.text_input(
        "🔑 Groq API Key",
        value=env_api_key,
        type="password",
        help="Enter your Groq API Key (defaults to secrets or .env file if available)"
    )

    default_model = get_config_val("GROQ_MODEL", "llama-3.3-70b-versatile")
    if default_model not in FREE_TIER_MODELS:
        default_model = "llama-3.3-70b-versatile"

    model_name = st.sidebar.selectbox(
        "🧠 Select AI Model",
        options=FREE_TIER_MODELS,
        index=FREE_TIER_MODELS.index(default_model)
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # --- Main Header ---
    st.markdown(f'''
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="
                    background: linear-gradient(135deg, #6366f1, #a855f7);
                    width: 42px; height: 42px;
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 22px;
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
                ">⚡</div>
                <div>
                    <h1 class="main-title">Dynamo AI</h1>
                    <div style="font-size: 13px; color: #94a3b8; font-weight: 500;">Next-Gen Web Assistant & Tool Engine</div>
                </div>
            </div>
            <div style="
                background: rgba(99, 102, 241, 0.1);
                border: 1px solid rgba(99, 102, 241, 0.25);
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 12.5px;
                color: #a5b4fc;
                font-weight: 600;
                display: flex; align-items: center; gap: 6px;
            ">
                <span style="width: 7px; height: 7px; background: #22c55e; border-radius: 50%; display: inline-block;"></span>
                {model_name}
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # --- Initialize Chat History ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display welcome hero if no messages
    if not st.session_state.messages:
        render_welcome_hero()
    else:
        # Display existing chat messages
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                render_user_message(msg["content"])
            else:
                st.markdown(f'''
                    <div style="
                        background: rgba(22, 24, 33, 0.7);
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 18px;
                        padding: 18px 22px;
                        margin: 14px 0;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                        line-height: 1.6;
                        color: #f1f5f9;
                    ">
                        {msg["content"]}
                    </div>
                ''', unsafe_allow_html=True)
                render_assistant_actions()

    # --- Handle Chat Input ---
    user_input = st.chat_input("Ask Dynamo AI anything...")

    if user_input:
        # Check API Key
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar or set `GROQ_API_KEY` in `.env` file.")
            return

        # Render user message on the RIGHT side
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_user_message(user_input)

        # Generate Assistant Response on the LEFT side
        try:
            # Initialize Model & Agent
            model = ChatGroq(
                model=model_name,
                temperature=0,
                groq_api_key=api_key
            )
            tools = [calculator, say_hello]
            agent_executor = create_react_agent(
                model=model,
                tools=tools,
                prompt="You are Dynamo AI, a powerful, friendly, and intelligent AI assistant. Use tools when needed."
            )

            # Format conversation history for LangGraph
            history = []
            for m in st.session_state.messages[:-1]:
                if m["role"] == "user":
                    history.append(HumanMessage(content=m["content"]))
                elif m["role"] == "assistant":
                    history.append(AIMessage(content=m["content"]))
            history.append(HumanMessage(content=user_input))

            response_placeholder = st.empty()
            full_response = ""

            # Stream response chunks
            for chunk in agent_executor.stream({"messages": history}):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for message in chunk["agent"]["messages"]:
                        if message.content:
                            full_response += message.content
                            response_placeholder.markdown(f'''
                                <div style="
                                    background: rgba(22, 24, 33, 0.7);
                                    border: 1px solid rgba(255, 255, 255, 0.08);
                                    border-radius: 18px;
                                    padding: 18px 22px;
                                    margin: 14px 0;
                                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                                    line-height: 1.6;
                                    color: #f1f5f9;
                                ">
                                    {full_response} ▌
                                </div>
                            ''', unsafe_allow_html=True)

            response_placeholder.markdown(f'''
                <div style="
                    background: rgba(22, 24, 33, 0.7);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 18px;
                    padding: 18px 22px;
                    margin: 14px 0;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                    line-height: 1.6;
                    color: #f1f5f9;
                ">
                    {full_response}
                </div>
            ''', unsafe_allow_html=True)
            render_assistant_actions()
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")


if __name__ == "__main__":
    main()