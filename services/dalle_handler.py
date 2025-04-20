import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt):
    response = client.images.generate(
        prompt=prompt,
        model="dall-e-2",  # or "dall-e-3" if you're approved
        n=1,
        size="512x512"
    )
    return response.data[0].url
