from flask import Flask, request, jsonify
import os
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Import all tools
from tools import (
    # Original tools
    search_web, calculator, get_current_time,
    # Reading and navigation
    read_text, move_cursor, find_text, report_status,
    # Text manipulation
    modify_selection, edit_text, clipboard_action, history_action,
    # Formatting and file management
    apply_formatting, manage_file,
    # TTS and app features
    control_tts, manage_app_feature, get_help
)

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize the agent
def initialize_agent():
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
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
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
    
    return agent

# Initialize the agent at startup
agent = initialize_agent()

# API endpoint for processing text commands
@app.route('/api/command', methods=['POST'])
def process_command():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Check if 'command' is in the request
        if 'command' not in data:
            return jsonify({'error': 'No command provided'}), 400
        
        user_input = data['command']
        
        # Create the agent input with messages
        agent_input = {"messages": [HumanMessage(content=user_input)]}
        
        # Run the agent
        response = agent.invoke(agent_input)
        
        # Extract the full process details
        process_details = []
        for message in response["messages"]:
            if hasattr(message, "tool_calls") and message.tool_calls:
                # AI message with tool calls
                step = {
                    "type": "ai_thinking",
                    "content": message.content if message.content else "Deciding to use a tool...",
                    "tool_calls": []
                }
                
                for tool_call in message.tool_calls:
                    step["tool_calls"].append({
                        "name": tool_call['name'],
                        "args": tool_call['args']
                    })
                
                process_details.append(step)
            elif hasattr(message, "name") and message.name:
                # Tool response message
                process_details.append({
                    "type": "tool_response",
                    "name": message.name,
                    "content": message.content
                })
            else:
                # Human or AI message without tool calls
                msg_type = "human" if isinstance(message, HumanMessage) else "ai"
                process_details.append({
                    "type": msg_type,
                    "content": message.content
                })
        
        # Extract the last message which contains the final response
        final_response = response["messages"][-1].content
        
        # Return the detailed response
        return jsonify({
            'command': user_input,
            'final_response': final_response,
            'process_details': process_details
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Optional: Add a health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

# Optional: Add a route to get available tools and their descriptions
@app.route('/api/tools', methods=['GET'])
def get_tools():
    try:
        tools_info = []
        
        # Get all tools used when initializing the agent
        all_tools = [
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
        
        # Format tool information
        for tool in all_tools:
            tool_info = {
                'name': tool.name,
                'description': tool.description,
                'args_schema': str(tool.args_schema) if hasattr(tool, 'args_schema') else None
            }
            tools_info.append(tool_info)
        
        return jsonify({'tools': tools_info})
    except Exception as e:
        return jsonify({'error': f'Error retrieving tools: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 