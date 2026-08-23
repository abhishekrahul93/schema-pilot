from langchain_core.messages import HumanMessage
import os
import json
import openai

def evaluate_exact_match(actual_output: dict, expected_properties: dict):
    if not expected_properties:
        return 1.0, "No expected properties defined for exact match."
    for key, expected_value in expected_properties.items():
        if key not in actual_output:
            return 0.0, f"Missing expected key: '{key}'"
        if actual_output[key] != expected_value:
            return 0.0, f"Value mismatch for '{key}': expected {expected_value}, got {actual_output[key]}"
    return 1.0, "All exact match properties verified successfully."

def evaluate_llm_judge(input_payload: dict, actual_output: dict, rubric: str):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return 0.0, "OpenAI API key not found in environment for LLM judge."
    client = openai.OpenAI(api_key=api_key)
    prompt = f'''
You are an AI evaluation judge. Evaluate the following agent output based on the provided rubric.

Input Payload:
{json.dumps(input_payload, indent=2)}

Actual Output:
{json.dumps(actual_output, indent=2)}

Evaluation Rubric:
{rubric}

Return your response strictly as a JSON object with two keys:
1. "score": a float between 0.0 and 1.0 (1.0 means perfect pass).
2. "reason": a short explanation for the score.
'''
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[HumanMessage(content=prompt)],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return float(result.get("score", 0.0)), result.get("reason", "No reason provided.")
    except Exception as e:
        return 0.0, f"LLM Judge evaluation failed: {str(e)}"
