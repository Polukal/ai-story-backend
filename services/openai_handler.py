import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_story(user_input, context=[]):
    if os.getenv("DEV_MODE") == "1":
        return f"[MOCKED RESPONSE] The AI would now continue your story with: '{user_input}'..."

    messages = context + [{"role": "user", "content": user_input}]

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        messages=messages,
        temperature=0.8,
        max_tokens=500
    )

    print(f"[GPT] Tokens used: {response.usage.total_tokens}")
    return response.choices[0].message.content
