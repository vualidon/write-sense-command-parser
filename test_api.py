import requests
import json

# API endpoint
API_URL = "http://127.0.0.1:5000/api/command"

def send_command(command):
    """Send a command to the API endpoint and print the response."""
    try:
        # Prepare the request payload
        payload = {
            "command": command
        }
        
        # Send the POST request
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print(f"Command: {data['command']}")
            print(f"Response: {data['response']}")
            print("-" * 50)
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
            print("-" * 50)
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

def main():
    # Example commands to test
    commands = [
        "Read the current paragraph",
        "Move to the next heading",
        "Select the current line and make it bold",
        "Find the word 'accessibility' in the document",
        "What's the current time?",
        "Increase the text-to-speech speed to 1.5"
    ]
    
    print("Testing Text Editor Accessibility API")
    print("=" * 50)
    
    # Test each command
    for command in commands:
        send_command(command)
    
    # Interactive mode
    print("\nInteractive Mode (type 'exit' to quit):")
    while True:
        user_input = input("\nYour command: ")
        if user_input.lower() == 'exit':
            break
        
        send_command(user_input)

if __name__ == "__main__":
    main() 