import os
from typing import List, Tuple
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import BaseTool

# Import tools from separate file
# Original tools
from tools import search_web, calculator, get_current_time

# Text editor accessibility tools
from tools import (
    # Reading and navigation
    read_text, move_cursor, find_text, report_status,
    # Text manipulation
    modify_selection, edit_text, clipboard_action, history_action,
    # Formatting and file management
    apply_formatting, manage_file,
    # TTS and app features
    control_tts, manage_app_feature, get_help
)
from dotenv import load_dotenv

load_dotenv()


# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Optional: Enable LangSmith tracing for debugging
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"

def main():
    # Create a custom system message for the accessibility assistant
    system_message = """You are an intelligent voice-controlled text editor assistant designed to help users 
with accessibility needs. Your primary focus is to provide accurate and helpful responses to voice commands 
for navigating, editing, and interacting with text documents.

When a user asks you to perform an action:
1. Identify the most appropriate tool to use based on the user's request
2. Use the tool with the correct parameters
3. Provide concise, helpful responses about what action was taken

Important: Users may have visual impairments, so your responses should be clear and 
easy to understand when read aloud by a screen reader."""
    
    # Initialize the LLM with system message
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    llm_with_system = llm.bind(messages=[SystemMessage(content=system_message)])
    
    # Define the tools list - group them by category for easier management
    tools = [
        # Original general-purpose tools
        search_web, calculator, get_current_time,
        
        # Reading and navigation tools
        read_text, move_cursor, find_text, report_status,
        
        # Text manipulation tools
        modify_selection, edit_text, clipboard_action, history_action,
        
        # Formatting and file management tools
        apply_formatting, manage_file,
        
        # TTS and app feature tools
        control_tts, manage_app_feature, get_help
    ]
    
    # Create a ReAct agent using LangGraph's prebuilt helper
    agent = create_react_agent(
        llm_with_system,
        tools
    )
    
    # Example user requests for the accessibility-focused agent
    example_requests = [
        "Read the current paragraph",
        "Move to the next heading and read it",
        "Select the current sentence and make it bold",
        "Find the word 'accessibility' in the document",
        "What's the weather today and what time is it?",
        "Increase the text-to-speech speed to 1.5"
    ]
    
    # Process each example request
    for i, user_input in enumerate(example_requests):
        print(f"\n--- Example {i+1} ---")
        print(f"User Request: {user_input}")
        
        try:
            # Create the agent input with messages
            agent_input = {"messages": [HumanMessage(content=user_input)]}
            
            # Run the agent
            response = agent.invoke(agent_input)
            
            # Print all messages to show the full process
            print(f"\nProcess:")
            for idx, message in enumerate(response["messages"]):
                if hasattr(message, "tool_calls") and message.tool_calls:
                    print(f"\nAI thinking:")
                    print(f"- {message.content if message.content else 'Deciding to use a tool...'}")
                    
                    for tool_call in message.tool_calls:
                        print(f"\nTool Called: {tool_call['name']}")
                        print(f"Tool Arguments: {tool_call['args']}")
                elif hasattr(message, "name") and message.name:
                    # This is typically a ToolMessage (response from a tool)
                    print(f"\nTool Response ({message.name}):")
                    print(f"- {message.content}")
                else:
                    # Human or AI message without tool calls
                    role = "Human" if isinstance(message, HumanMessage) else "AI"
                    print(f"\n{role}:")
                    print(f"- {message.content}")
            
            # Also print just the final response for clarity
            final_response = response["messages"][-1].content
            print(f"\nFinal Response: {final_response}")
        except KeyboardInterrupt:
            print("\nProcess interrupted by user.")
            break
        except Exception as e:
            print(f"\nError processing request: {str(e)}")

    # Interactive mode
    print("\n--- Interactive Mode ---")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYour request: ")
        if user_input.lower() == 'exit':
            break
            
        try:
            # Create the agent input with messages
            agent_input = {"messages": [HumanMessage(content=user_input)]}
            
            # Run the agent
            response = agent.invoke(agent_input)
            
            # Print all messages to show the full process
            print(f"\nProcess:")
            for idx, message in enumerate(response["messages"]):
                if hasattr(message, "tool_calls") and message.tool_calls:
                    print(f"\nAI thinking:")
                    print(f"- {message.content if message.content else 'Deciding to use a tool...'}")
                    
                    for tool_call in message.tool_calls:
                        print(f"\nTool Called: {tool_call['name']}")
                        print(f"Tool Arguments: {tool_call['args']}")
                elif hasattr(message, "name") and message.name:
                    # This is typically a ToolMessage (response from a tool)
                    print(f"\nTool Response ({message.name}):")
                    print(f"- {message.content}")
                else:
                    # Human or AI message without tool calls
                    role = "Human" if isinstance(message, HumanMessage) else "AI"
                    print(f"\n{role}:")
                    print(f"- {message.content}")
            
            # Also print just the final response for clarity
            final_response = response["messages"][-1].content
            print(f"\nFinal Response: {final_response}")
        except KeyboardInterrupt:
            print("\nProcess interrupted by user.")
            break
        except Exception as e:
            print(f"\nError processing request: {str(e)}")

if __name__ == "__main__":
    main() 