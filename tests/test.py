import os
from openai import OpenAI

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_model_and_report(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    usage = response.usage
    print(f"Tokens used — Prompt: {usage.prompt_tokens}, "
          f"Completion: {usage.completion_tokens}, "
          f"Total: {usage.total_tokens}")

    return response.choices[0].message.content

# Example usage:
reply = call_model_and_report("Hello, can you tell me a joke?")
print("Model replied:", reply)