import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.sanitize import sanitize_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt):
    if os.getenv("DEV_MODE") == "1":
        return "TEST_MODE"  # Signal to frontend to use a local image

    safe_prompt = sanitize_prompt(prompt)

    if not safe_prompt:
        raise ValueError("Prompt for image generation is empty.")

    response = client.images.generate(
        model="dall-e-2",
        prompt=safe_prompt,
        n=1,
        size="512x512"
    )
    return response.data[0].url

