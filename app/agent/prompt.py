def build_system_prompt(products):

    return f"""
    You are Agent-Kairos, a forecasting assistant.

    Available products in the database are: {products}

    IMPORTANT:
    - Always use product values EXACTLY as given above
    - Do NOT include the word "product"
    - Example: use "A", not "product A"
    """


def llm_response_exaplanation_prompt(query, function_name, result_summary):
    second_messages = [
        {
            "role": "system",
            "content": """
            You are Agent-Kairos.

            IMPORTANT:
            - Do NOT call any tools
            - Do NOT generate tool calls
            - Only explain the result in natural language
            - Do not give any unnecessary information, only explain the result
            """
        },
        {
            "role": "user",
            "content": query
        },
        {
            "role": "assistant",
            "content": f"The tool `{function_name}` was executed successfully."
        },
        {
            "role": "user",
            "content": f"Here is the result:\n{result_summary}\n\nExplain this."
        }
    ]
    return second_messages
