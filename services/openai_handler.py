import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_story(user_input, context=[]):
    messages = context + [{"role": "user", "content": user_input}]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.8,
        max_tokens=500
    )

    return response.choices[0].message.content
