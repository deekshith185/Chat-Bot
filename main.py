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
    return f"Hello {name}, I hope you are well today!"


# Free-tier Groq models
FREE_TIER_MODELS = [
    "llama-3.3-70b-versatile",
    "qwen/qwen3.6-27b",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]


def render_user_message(content: str):
    """Renders user message in a right-aligned ChatGPT style blue pill bubble."""
    escaped_content = html.escape(content).replace("\n", "<br>")
    st.markdown(f'''
        <div style="display: flex; justify-content: flex-end; margin: 14px 0 18px 0; width: 100%;">
            <div style="background-color: #1a4a84; color: #ffffff; padding: 10px 18px; border-radius: 22px; max-width: 75%; font-size: 15.5px; line-height: 1.5; word-break: break-word; box-shadow: 0 2px 8px rgba(0,0,0,0.25);">
                {escaped_content}
            </div>
        </div>
    ''', unsafe_allow_html=True)


def render_assistant_actions():
    """Renders ChatGPT style action icons underneath assistant responses."""
    st.markdown('''
        <div style="display: flex; gap: 14px; margin-top: 6px; margin-bottom: 22px; color: #8e8e93; font-size: 15px; opacity: 0.85;">
            <span style="cursor: pointer;" title="Copy response">📋</span>
            <span style="cursor: pointer;" title="Share">📤</span>
            <span style="cursor: pointer;" title="Regenerate">🔄</span>
            <span style="cursor: pointer;" title="More options">•••</span>
        </div>
    ''', unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Dynamo AI - ChatGPT Assistant",
        page_icon="🤖",
        layout="centered"
    )

    # ChatGPT Dark Theme Styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: #ececec;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Hide default Streamlit padding & header elements */
    .block-container {
        max-width: 800px;
        padding-top: 1.5rem;
        padding-bottom: 6rem;
    }

    /* Style select box & text inputs */
    .stTextInput > div > div > input, .stSelectbox > div > div {
        background-color: #171717;
        color: #ffffff;
        border: 1px solid #2e2e2e;
        border-radius: 8px;
    }

    /* Chat input box at bottom */
    div[data-testid="stChatInput"] {
        border-radius: 24px;
        background-color: #212121;
    }

    /* Custom scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0d0d;
    }
    ::-webkit-scrollbar-thumb {
        background: #2a2a2a;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar Settings ---
    st.sidebar.title("🤖 Chatbot Settings")
    
    env_api_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.sidebar.text_input(
        "Groq API Key",
        value=env_api_key,
        type="password",
        help="Enter your Groq API Key (defaults to .env file if available)"
    )

    default_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    if default_model not in FREE_TIER_MODELS:
        default_model = "llama-3.3-70b-versatile"

    model_name = st.sidebar.selectbox(
        "Select Groq Free-Tier Model",
        options=FREE_TIER_MODELS,
        index=FREE_TIER_MODELS.index(default_model)
    )

    if st.sidebar.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # --- Main Header ---
    st.title("🤖 Dynamo AI")
    st.caption(f"Powered by Groq (`{model_name}`) & LangGraph ReAct Agent")
    st.divider()

    # --- Initialize Chat History ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user_message(msg["content"])
        else:
            st.markdown(msg["content"])
            render_assistant_actions()

    # --- Handle Chat Input ---
    user_input = st.chat_input("Ask Dynamo anything...")

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
                prompt="You are Dynamo, a helpful and friendly AI assistant. Use tools when needed."
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
                            response_placeholder.markdown(full_response + " ▌")

            response_placeholder.markdown(full_response)
            render_assistant_actions()
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")


if __name__ == "__main__":
    main()