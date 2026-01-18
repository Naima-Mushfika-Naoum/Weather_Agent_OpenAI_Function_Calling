# OpenAI Function Calling Example

This project demonstrates how to use OpenAI's function calling feature with with the Groq API and Llama 3.3 to create a real-time weather assistant.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

   ```

2. **Set up your API key:**
   - Create a `.env` file in the project directory
   - Add your Groq and OpenWeatherMap API keys:
     ```
     GROQ_API_KEY=your_groq_key_here
     OPENWEATHER_API_KEY=your_openweather_key_here
     ```

## How it works

The `Weather_agent.py` script demonstrates:

1. **Defining Tools**: A list of JSON schemas (tools) that describe the get_weather and catch_all functions, including strict parameter requirements to ensure valid JSON output.
2. **Function Implementations**: The get_weather() function uses the requests library to fetch live data from the OpenWeatherMap API.
3. **API Calls**: Sends user messages to Groq using the llama-3.3-70b-versatile model along with the available tool definitions.
4. **Tool Execution**: When the model decides to call a function:
   - It outputs a structured tool call.
   - The script parses the function name and arguments using json.loads().
   - The corresponding Python function is executed.
   - The result is sent back to the model as a tool role message.
5. **Looping**: An interactive while loop allows for continuous conversation until the user types 'exit' or 'quit'.
## Key Components

- **tools**: A list defining the get_weather function (for weather queries) and a catch_all function (to stabilize non-weather queries)
- **start_chat()**:  The main entry point that manages the interactive loop and message history.
- **get_weather()**:Handles the technical integration with the external Weather API.
- **Messages**: A list that maintains the conversation context, including system instructions, user prompts, assistant thoughts, and tool results.

## Example Usage

```python
# Run the script
python Weather_agent.py

# Interaction
You: What is the weather like in Jeddah?
[System: Fetching weather for Jeddah...]
Assistant: The current weather in Jeddah is 28°C with clear sky.
```

## Notes

- The script uses llama-3.3-70b-versatile on Groq for high-speed inference and accurate tool calling.
- Strict Mode: strict: True and additionalProperties: False are enabled in the tool definitions to force the model to follow the JSON schema exactly.
- Base URL: The OpenAI client is configured with Groq's endpoint: https://api.groq.com/openai/v1.
-Error Handling: Includes a try-except block to catch API errors or connectivity issues without crashing the script.
