# LangChain ReAct Agent Implementation

This repository contains examples of ReAct agents implemented using LangChain and LangGraph. The ReAct pattern (Reasoning + Acting) enables agents to reason about tasks and take actions in an iterative process.

## Requirements

```
pip install langchain langchain-openai langgraph
```

You'll need to set your OpenAI API key:

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

## Examples

### 1. Basic ReAct Agent (`react_agent.py`)

A simple implementation of a ReAct agent using LangGraph's prebuilt helper. This agent can:

- Search for information (mock implementation)
- Perform calculations

```
python react_agent.py
```

### 2. Advanced ReAct Agent with RAG (`advanced_react_agent.py`)

A more advanced implementation that incorporates Retrieval Augmented Generation (RAG):

- In-memory document store for knowledge retrieval
- Web search capability (mock implementation)
- Calculator functionality

```
python advanced_react_agent.py
```

### 3. Custom ReAct Agent (`custom_react_agent.py`)

A fully customized implementation that demonstrates:

- Manual control of the ReAct agent's behavior
- Explicit reasoning steps (THINK → TOOL → OBSERVE → RESPOND)
- Custom state management
- Multi-turn conversation handling

```
python custom_react_agent.py
```

## How ReAct Works

The ReAct pattern follows this general flow:

1. The model **reasons** about what step to take in response to a user input
2. The model chooses an **action** (tool) and generates arguments for it
3. The agent execution runtime calls the chosen tool with the generated arguments
4. The results are returned to the model as an observation
5. The process repeats until the agent decides to respond directly to the user

## Differences Between Implementations

- **Basic**: Uses the prebuilt helper for quick implementation
- **Advanced**: Adds RAG capabilities to enhance the agent's knowledge
- **Custom**: Demonstrates full control over the agent's behavior through LangGraph's StateGraph

For more information on LangChain agents and tools, refer to the [LangChain documentation](https://python.langchain.com/docs/concepts/).
