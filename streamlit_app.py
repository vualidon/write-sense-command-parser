import streamlit as st
import requests
import json
from datetime import datetime

# API endpoint - adjust if your Flask API is running on a different host/port
API_URL = "http://localhost:5001/api"

def get_tools():
    """Fetch available tools from the API"""
    try:
        response = requests.get(f"{API_URL}/tools")
        if response.status_code == 200:
            return response.json()['tools']
        else:
            st.error(f"Error fetching tools: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

def send_command(command):
    """Send a command to the API and return the response"""
    try:
        payload = {"command": command}
        response = requests.post(f"{API_URL}/command", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: Status code {response.status_code}"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_URL}/health")
        return response.status_code == 200
    except:
        return False

# App title and description
st.title("Text Editor Accessibility Assistant")
st.markdown("""
This demo connects to a Flask API that provides text editor accessibility features 
powered by a ReAct agent. The assistant can understand natural language commands 
and perform various text editing operations.
""")

# Check API connection
api_status = check_api_health()
if api_status:
    st.success("✅ Connected to API")
else:
    st.error("❌ Could not connect to API. Make sure the Flask API is running on http://localhost:5000")
    st.info("Run 'python api.py' to start the API server")
    st.stop()

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Command Interface", "Example Commands", "Available Tools"])

# Tab 1: Command Interface
with tab1:
    st.subheader("Command the Assistant")
    
    # Command input
    command = st.text_input("Enter your command:", placeholder="e.g., Read the current paragraph")
    
    # Add command history to session state if it doesn't exist
    if 'command_history' not in st.session_state:
        st.session_state.command_history = []
    
    # Process command button
    if st.button("Send Command") and command:
        with st.spinner("Processing command..."):
            result = send_command(command)
            
            # Add to history with timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Check if there was an error
            if "error" in result:
                history_item = {
                    "timestamp": timestamp,
                    "command": command,
                    "error": result.get("error")
                }
            else:
                history_item = {
                    "timestamp": timestamp,
                    "command": command,
                    "final_response": result.get("final_response", "No response provided"),
                    "process_details": result.get("process_details", [])
                }
            
            st.session_state.command_history.append(history_item)
        
        # Clear input after sending
        st.rerun()
    
    # Display command history
    if st.session_state.command_history:
        st.subheader("Command History")
        
        for i, item in enumerate(reversed(st.session_state.command_history)):
            # Create a nice display of the command and timestamp
            with st.expander(f"**{item['timestamp']}**: {item['command']}"):
                # If there was an error, show it
                if "error" in item:
                    st.error(f"**Error:** {item['error']}")
                else:
                    # Show full process details
                    st.markdown("### Process Details")
                    
                    for step in item.get("process_details", []):
                        step_type = step.get("type", "unknown")
                        
                        if step_type == "human":
                            st.markdown("**👤 Human:**")
                            st.markdown(f"{step.get('content', '')}")
                            
                        elif step_type == "ai_thinking":
                            st.markdown("**🤔 AI Thinking:**")
                            if step.get('content'):
                                st.markdown(f"{step.get('content', '')}")
                            
                            # Show tool calls
                            for tool_call in step.get("tool_calls", []):
                                st.markdown(f"**🔧 Tool Called:** `{tool_call.get('name', 'unknown')}`")
                                st.code(json.dumps(tool_call.get("args", {}), indent=2), language="json")
                                
                        elif step_type == "tool_response":
                            st.markdown(f"**⚙️ Tool Response ({step.get('name', 'unknown')}):**")
                            st.markdown(f"{step.get('content', '')}")
                            
                        elif step_type == "ai":
                            st.markdown("**🤖 AI Response:**")
                            st.markdown(f"{step.get('content', '')}")
                            
                        st.markdown("---")
                    
                    # Show final response more prominently
                    st.markdown("### Final Response")
                    st.success(item.get("final_response", "No response"))
                
                # Add a button to repeat this command
                if st.button("Repeat Command", key=f"repeat_{i}"):
                    with st.spinner("Processing command..."):
                        result = send_command(item['command'])
                        
                        # Add to history with timestamp
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        # Check if there was an error
                        if "error" in result:
                            history_item = {
                                "timestamp": timestamp,
                                "command": item['command'],
                                "error": result.get("error")
                            }
                        else:
                            history_item = {
                                "timestamp": timestamp,
                                "command": item['command'],
                                "final_response": result.get("final_response", "No response provided"),
                                "process_details": result.get("process_details", [])
                            }
                        
                        st.session_state.command_history.append(history_item)
                    
                    # Update UI
                    st.rerun()
        
        # Clear history button
        if st.button("Clear History"):
            st.session_state.command_history = []
            st.rerun()

# Tab 2: Example Commands
with tab2:
    st.subheader("Example Commands")
    
    # Define example commands by category
    examples = {
        "Reading and Navigation": [
            "Read the current paragraph",
            "Move to the next heading and read it",
            "Find the word 'accessibility' in the document"
        ],
        "Text Manipulation": [
            "Select the current sentence",
            "Delete the selected text",
            "Copy the current line"
        ],
        "Formatting": [
            "Make the selected text bold",
            "Apply heading level 2 to this line",
            "Insert a bulleted list"
        ],
        "File Operations": [
            "Save the current document",
            "Open the file named 'report.txt'",
            "Check if there are unsaved changes"
        ],
        "Text-to-Speech Controls": [
            "Increase the text-to-speech speed to 1.5",
            "Spell the current word",
            "Set the TTS voice to 'David'"
        ],
        "General Queries": [
            "What's the current time?",
            "What is 25 times 4?",
            "Search for information about screen readers"
        ]
    }
    
    # Display examples with Try buttons
    for category, commands in examples.items():
        st.markdown(f"### {category}")
        
        for i, cmd in enumerate(commands):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"• {cmd}")
            with col2:
                if st.button("Try", key=f"try_{category}_{i}"):
                    with st.spinner("Processing command..."):
                        result = send_command(cmd)
                        
                        # Add to history with timestamp
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        # Check if there was an error
                        if "error" in result:
                            history_item = {
                                "timestamp": timestamp,
                                "command": cmd,
                                "error": result.get("error")
                            }
                        else:
                            history_item = {
                                "timestamp": timestamp,
                                "command": cmd,
                                "final_response": result.get("final_response", "No response provided"),
                                "process_details": result.get("process_details", [])
                            }
                        
                        st.session_state.command_history.append(history_item)
                    
                    # Show the output immediately and switch to the command tab
                    tab1.button("See result in Command Interface")
                    st.rerun()

# Tab 3: Available Tools
with tab3:
    st.subheader("Available Tools")
    
    # Fetch available tools from the API
    tools = get_tools()
    
    if tools:
        # Group tools by category based on naming patterns
        tool_categories = {
            "Reading and Navigation": [],
            "Text Manipulation": [],
            "Formatting and File Management": [],
            "Text-to-Speech and App Features": [],
            "General Purpose": []
        }
        
        for tool in tools:
            name = tool["name"]
            
            if name in ["read_text", "move_cursor", "find_text", "report_status"]:
                tool_categories["Reading and Navigation"].append(tool)
            elif name in ["modify_selection", "edit_text", "clipboard_action", "history_action"]:
                tool_categories["Text Manipulation"].append(tool)
            elif name in ["apply_formatting", "manage_file"]:
                tool_categories["Formatting and File Management"].append(tool)
            elif name in ["control_tts", "manage_app_feature", "get_help"]:
                tool_categories["Text-to-Speech and App Features"].append(tool)
            else:
                tool_categories["General Purpose"].append(tool)
        
        # Display tools by category
        for category, category_tools in tool_categories.items():
            if category_tools:  # Only show categories that have tools
                st.markdown(f"### {category}")
                
                for tool in category_tools:
                    with st.expander(f"**{tool['name']}**"):
                        st.markdown(f"**Description:** {tool['description']}")
                        if tool['args_schema'] and tool['args_schema'] != "None":
                            st.markdown("**Arguments Schema:**")
                            st.code(tool['args_schema'], language="python")
    else:
        st.warning("Could not fetch tools from the API.")
        
# Add a note about the Flask API at the bottom
st.markdown("---")
st.markdown("""
**Note:** This Streamlit app requires the Flask API to be running. 
Make sure to start it with `python api.py` before using this interface.
""")

# Add styling
st.markdown("""
<style>
    div.stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True) 