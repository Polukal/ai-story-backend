import os
from openai import OpenAI
from utils.sanitize import sanitize_prompt

client = OpenAI()

def generate_image(prompt):
    if os.getenv("DEV_MODE") == "1":
        return "TEST_MODE"

    print('[DEBUG] image prompt to dall-e: {prompt}')
    safe_prompt = sanitize_prompt(prompt)
    if not safe_prompt:
        raise ValueError("Prompt for image generation is empty.")
    
    print('[DEBUG] SANITIZED image prompt to dall-e: {safe_prompt}')
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=safe_prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            response_format="url"
        )
        return response.data[0].url
    except Exception as e:
        print(f"[IMAGE] Generation error: {e}")
        raise
