import os  # For accessing system environment variables (like API keys)
import warnings  # For managing and suppressing warning messages
from langchain_core.messages import HumanMessage  # For representing messages sent by the user to the model
from langchain_groq import ChatGroq  # For interacting with the Groq LLM API
from langchain_core.tools import tool  # Decorator to define custom tools that the agent can use
from langgraph.prebuilt import create_react_agent  # For creating a ReAct (Reasoning and Acting) agent with tools
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Suppress deprecation warnings for a clean user interface
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()
#load environment variables from .env file

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers"""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"
#A simple calculator tool that takes two numbers as input and returns their sum. The @tool decorator indicates that this function can be used as a tool by the agent.
    
@tool
def say_hello(name: str = "there") -> str:
    """Useful for greeting a user when a name is provided or to say hello"""
    print("Tool has been called.")
    return f"Hello {name}, I hope you are well today"
#A simple greeting tool that takes a name as input and returns a greeting message. The @tool decorator indicates that this function can be used as a tool by the agent.

def main():
    groq_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")
    
    print(f"Initializing Groq model: {model_name}...")
    if not groq_key:
        print("Warning: GROQ_API_KEY is not set in environment.")
        
    model = ChatGroq(model=model_name, temperature=0)

    tools = [calculator, say_hello]
    agent_executor = create_react_agent(
        model,
        tools,
        prompt="You are Preethi, a helpful and friendly AI assistant."
    )
    #Create an agent executor using the REACT framework, which allows the agent to use the defined tools (calculator and say_hello) to perform tasks based on user input.
    
    print("Welcome! I'm Preethi, your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")
    #Print a welcome message to the user, informing them about the capabilities of the assistant and how to exit the program.
    
    while True:#Start an infinite loop to continuously accept user input until the user decides to quit.
        user_input = input("\nYou: ").strip()
        # Prompt the user for input and remove any leading or trailing whitespace.
        
        if user_input == "quit":
            break
        # If the user types "quit", exit the loop and end the program.
        print("\nPreethi: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):#Stream the agent's response in real-time as it processes the user's input. The agent_executor.stream() method takes a dictionary with a "messages" key, which contains a list of messages (in this case, just one HumanMessage with the user's input).
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
            
                    if message.content:
                        print(message.content, end="")#If the chunk contains an "agent" key with "messages", iterate through those messages and print their content without adding a newline (end="") to create a streaming effect.
        print()#Print a newline after the response is complete to separate it from the next user input.
              
# The main function initializes the chatbot, defines the tools it can use, and handles the interaction loop with the user. The agent can perform calculations and greet users based on their input, and it streams responses in real-time.       
if __name__ == "__main__":
    main()