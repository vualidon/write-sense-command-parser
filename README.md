# WriteSense: Text Editor Accessibility Assistant

This project implements a voice-controlled text editor assistant designed to help users with accessibility needs. It uses LangChain, LangGraph's ReAct agents, and OpenAI's models to provide an intelligent interface for navigating, editing, and formatting text documents through natural language commands.

## Project Structure

- `api.py` - Flask API server implementing the ReAct agent with various accessibility tools
- `tools.py` - Definitions of all the tools the agent can use for text editing operations
- `streamlit_app.py` - Streamlit web interface to interact with the API
- `test_api.py` - Tests for the API endpoints
- `react_agent.py` - Example implementation of a basic LangChain ReAct agent

## Requirements

```
pip install -r requirements.txt
```

Required dependencies:

- flask
- langchain
- langchain-openai
- langgraph
- requests
- streamlit

You'll need to set your OpenAI API key in your environment variables or in the `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

## Running the Application

1. Start the API server:

```
python api.py
```

2. Start the Streamlit web interface:

```
streamlit run streamlit_app.py
```

## Capabilities

The assistant provides the following categories of text editing functionality:

### Reading and Navigation

- Read text by character, word, line, paragraph, etc.
- Move cursor to various positions
- Find specific text in the document

### Text Manipulation

- Select, modify, and clear text selections
- Insert, delete, and replace text
- Copy, cut, and paste operations
- Undo and redo edits

### Formatting and File Management

- Apply various text formatting (bold, italic, etc.)
- Create headings, lists, and tables
- Open, save, and manage files

### Accessibility Features

- Control text-to-speech settings
- Manage editor modes and display options
- Get help with commands and features

## How It Works

The system uses LangGraph's ReAct (Reasoning + Acting) agent pattern:

1. The user inputs a natural language command
2. The AI agent reasons about which tool to use
3. The appropriate tool is executed
4. Results are returned to the user

All interactions are designed to be screen-reader friendly and optimized for accessibility.

## API Documentation

For detailed API documentation, refer to the `API_README.md` file.

## Streamlit Interface

The Streamlit interface provides:

- A command input field
- Command history with detailed execution steps
- Example commands to get started
- List of available tools and their descriptions

For details on the Streamlit interface, refer to the `STREAMLIT_README.md` file.
