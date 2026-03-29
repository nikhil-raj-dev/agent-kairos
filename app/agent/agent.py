import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from app.tools.data_tool import get_data
from app.tools.forecast_tool import forecast_product
from app.tools.anomaly_tool import detect_product_anomalies
from app.database.queries import get_all_products
from app.agent.prompt import build_system_prompt, llm_response_exaplanation_prompt

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
    )

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_data",
            "description": "Fetches and preprocesses sales data for a given product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product to fetch data for."
                    },
                    "n_days": {
                        "type": "integer",
                        "description": "Number of recent days to fetch data for (default is 90)."
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "forecast_product",
            "description": "Generates sales forecast for a given product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product to forecast."
                    },
                    "forecast_periods": {
                        "type": "integer",
                        "description": "Number of future periods to forecast (default is 30)."
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_product_anomalies",
            "description": "Detects anomalies in the sales data for a given product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Name of the product to analyze for anomalies."
                    }
                },
                "required": ["product_name"]
            }
        }
    }
]


function_mapping = {
    "get_data": get_data,
    "forecast_product": forecast_product,
    "detect_product_anomalies": detect_product_anomalies
}

chat_history = []

def run_agent(query: str):
    
    logs = []
    logs.append(f"Received query: {query}")

    global chat_history

    products = get_all_products()

    system_prompt = build_system_prompt(products)
    

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages = [{"role": "system", "content": system_prompt}] + chat_history + [{"role": "user", "content": query}],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    chat_history.append({"role": "user", "content": query})

    if message.tool_calls:

        tool_call = message.tool_calls[0]

        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        logs.append(f"Selected tool: {function_name}")
        logs.append(f"Arguments: {arguments}")

        print(f"\n[Agent] Calling tool: {function_name} with args {arguments}\n")

        logs.append("Executing tool...")
        result = function_mapping[function_name](**arguments)
        logs.append("Tool execution complete")


        chat_history.append({
            "role": "assistant",
            "tool_calls": message.tool_calls
        })

        chat_history.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,   # 🔥 VERY IMPORTANT
            "content": str(result.head(10))
        })


        second_messages = llm_response_exaplanation_prompt(query, function_name, result)

        second_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=second_messages
        )

        final_response = second_response.choices[0].message.content

        chat_history.append({
            "role": "assistant",
            "content": final_response
        })

        chat_history = chat_history[-3:]


        return {
            "response": final_response,
            "tool_used": function_name,
            "tool_args": arguments,
            "logs": logs
        }

    else:
        logs.append("No tool required")
        final_response = message.content

        chat_history.append({
            "role": "assistant",
            "content": final_response
        })

        chat_history = chat_history[-3:]

        return {
            "response": final_response,
            "tool_used": None,
            "tool_args": {},
            "logs": logs
        }
    
chat_history = chat_history[-3:]