# Text Editor Accessibility Assistant - Streamlit Demo

This Streamlit application demonstrates the capabilities of the Text Editor Accessibility Assistant by providing a user-friendly interface to interact with the Flask API.

![Streamlit Demo](https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png)

## Features

- **Command Interface**: Send commands to the assistant and view responses
- **Command History**: Track and repeat previous commands
- **Example Commands**: Pre-defined examples organized by category
- **Tool Explorer**: Browse all available tools and their descriptions

## Setup and Installation

1. First, install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure the Flask API is running:

```bash
python api.py
```

3. Launch the Streamlit app:

```bash
streamlit run streamlit_app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Using the Streamlit App

### Command Interface Tab

- Type a command in the input field and click "Send Command"
- View the assistant's response
- Browse your command history
- Repeat previous commands with a single click

### Example Commands Tab

Browse pre-defined example commands organized by category:

- Reading and Navigation
- Text Manipulation
- Formatting
- File Operations
- Text-to-Speech Controls
- General Queries

Click the "Try" button next to any example to execute it.

### Available Tools Tab

Explore all the tools available to the assistant:

- Tool name and description
- Required and optional parameters
- Parameter types and constraints

## Requirements

The Streamlit app requires both the Flask API and the following dependencies:

- streamlit==1.32.0
- requests==2.32.3
- flask==2.3.3
- langchain==0.3.21
- langchain-openai==0.2.14
- langgraph==0.2.61

## Architecture

This demo uses a client-server architecture:

1. The Streamlit app serves as the client interface
2. The Flask API processes commands using the ReAct agent
3. The ReAct agent uses LangChain and LangGraph to select and execute tools
4. Responses are returned to the Streamlit app for display

## Troubleshooting

If you encounter any issues:

- Make sure the Flask API is running at <http://localhost:5000>
- Check that you have set your OpenAI API key in the api.py file
- Verify all dependencies are installed
- Check the console for any error messages

## Screenshots

This demo interface includes:

1. Command interface with history
2. Example commands organized by category
3. Tool explorer showing all available capabilities
