import json
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_weather(location: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The current weather in {location} is {temp}°C with {desc}."
        return f"Error: {data.get('message', 'City not found')}"
    except Exception as e:
        return f"Technical error: {str(e)}"

# ERROR-PROOF TOOL DEFINITIONS
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get real-time weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city name, e.g., Jeddah"}
                },
                "required": ["location"],
                "additionalProperties": False # REQ for Strict Mode
            },
            "strict": True # ENABLES Constrained Decoding
        }
    },
    {
        "type": "function",
        "function": {
            "name": "catch_all",
            "description": "Use this tool ONLY if the request is NOT about weather.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

def start_chat():
    messages = [{
        "role": "system", 
        "content": "You are a research assistant. If a user asks for weather, use the get_weather tool. Output ONLY raw JSON for tool calls."
    }]
    
    print("--- Research Assistant Bot (Type 'exit' to quit) ---")
    
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ["exit", "quit"]: break
            
        messages.append({"role": "user", "content": user_query})
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            assistant_msg = response.choices[0].message
            
            if assistant_msg.tool_calls:
                messages.append(assistant_msg)
                
                for tool_call in assistant_msg.tool_calls:
                    if tool_call.function.name == "get_weather":
                        args = json.loads(tool_call.function.arguments)
                        print(f"[System: Fetching weather for {args['location']}...]")
                        result = get_weather(args['location'])
                    else:
                        # Handle the catch_all tool
                        result = "I understand. How else can I help?"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": result
                    })
                
                final_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages
                )
                print(f"Assistant: {final_response.choices[0].message.content}")
            else:
                print(f"Assistant: {assistant_msg.content}")
                
        except Exception as e:
            print(f"\n[System Error]: {e}")

if __name__ == "__main__":
    start_chat()