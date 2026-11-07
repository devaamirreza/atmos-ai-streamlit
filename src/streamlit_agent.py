import os
import json
import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI

from src.weather_tool import get_weather


# 1. Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

# Check Streamlit Cloud secrets
try:
    api_key = st.secrets.get("OPENROUTER_API_KEY", api_key)
except (FileNotFoundError, KeyError):
    pass

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is missing. "
        "Add it to your .env file or Streamlit Cloud secrets."
    )


# 2. Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# 3. Define available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# 4. Define agent instructions
SYSTEM_PROMPT = """
You are a reliable AI weather assistant.

1. Use get_weather for requests about current weather.
2. Never invent temperatures or weather conditions.
3. Use actual weather tool results when answering.
4. Explain errors clearly.
5. Understand English, Hindi, and Hinglish.
6. Respond in the same language as the user.
7. Keep responses concise, friendly, and factual.
8. Use conversation history to understand follow-up questions.
9. Politely redirect unrelated questions to your weather-assistant purpose.
"""


# 5. Main agent function
def run_streamlit_agent(user_query, conversation_history=None):

    if conversation_history is None:
        conversation_history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(conversation_history)

    messages.append({
        "role": "user",
        "content": user_query
    })

    # First API call: Tool selection
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    first_usage = response.usage
    assistant_message = response.choices[0].message

    total_prompt = first_usage.prompt_tokens
    total_completion = first_usage.completion_tokens
    total_tokens = first_usage.total_tokens

    # Check for tool calls
    if assistant_message.tool_calls:

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            if tool_name == "get_weather":

                weather_result = get_weather(
                    arguments["city"]
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(weather_result)
                })

        # Second API call: Generate final answer
        final_response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )

        second_usage = final_response.usage

        total_prompt += second_usage.prompt_tokens
        total_completion += second_usage.completion_tokens
        total_tokens += second_usage.total_tokens

        final_message = final_response.choices[0].message

        messages.append(final_message)

        answer = final_message.content
        model_name = final_response.model

    else:

        messages.append(assistant_message)

        answer = assistant_message.content
        model_name = response.model

    # Return structured result
    return {
        "answer": answer,
        "model": model_name,
        "prompt_tokens": total_prompt,
        "completion_tokens": total_completion,
        "total_tokens": total_tokens,
        "conversation_history": messages[1:]
    }