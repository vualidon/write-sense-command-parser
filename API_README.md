# Text Editor Accessibility API

This API provides text editor accessibility features powered by a ReAct agent that can understand natural language commands and perform various text editing operations.

## Setup and Installation

1. Install the required dependencies:

```bash
pip install flask langchain langchain-openai langgraph requests
```

2. Set your OpenAI API key:

```python
# In api.py, uncomment and add your API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

3. Start the API server:

```bash
python api.py
```

The server will start on `http://localhost:5000`.

## API Endpoints

### 1. Process Commands

**Endpoint:** `/api/command`

**Method:** POST

**Request Format:**

```json
{
  "command": "Your text editor command here"
}
```

**Response Format:**

```json
{
  "command": "The command you sent",
  "response": "The response from the assistant"
}
```

**Example:**

```bash
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "Read the current paragraph"}'
```

### 2. Health Check

**Endpoint:** `/api/health`

**Method:** GET

**Response Format:**

```json
{
  "status": "ok"
}
```

### 3. List Available Tools

**Endpoint:** `/api/tools`

**Method:** GET

**Response Format:**

```json
{
  "tools": [
    {
      "name": "tool_name",
      "description": "tool_description",
      "args_schema": "schema_info"
    },
    ...
  ]
}
```

## Testing the API

You can use the included `test_api.py` script to test the API:

```bash
python test_api.py
```

This script demonstrates:

1. How to send commands to the API
2. How to handle responses
3. Interactive mode for testing custom commands

## Available Commands

The API supports a wide range of text editor commands, including:

### Reading and Navigation

- Reading text (character, word, line, paragraph, etc.)
- Moving the cursor (next/previous word, line, paragraph, etc.)
- Searching for text

### Text Manipulation

- Selecting text
- Editing text (insert, delete, replace)
- Clipboard operations (copy, cut, paste)
- Undo/redo

### Formatting and File Management

- Applying formatting (bold, italic, headings, etc.)
- File operations (open, save, close)

### Text-to-Speech and App Features

- Adjusting TTS settings (speed, voice)
- Managing application features

## Integration Examples

### Web Application

```javascript
async function sendCommand(command) {
  try {
    const response = await fetch('http://localhost:5000/api/command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command: command }),
    });
    
    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Error:', error);
    return 'Error processing command';
  }
}
```

### Python Application

```python
import requests

def send_command(command):
    response = requests.post(
        'http://localhost:5000/api/command',
        json={'command': command}
    )
    return response.json()['response']
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400: Bad Request (e.g., missing command)
- 500: Internal Server Error (with error message)

## Security Considerations

- The API currently doesn't include authentication
- For production, consider adding API keys or other authentication methods
- Consider rate limiting for public-facing deployments
