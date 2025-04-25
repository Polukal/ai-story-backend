import time
from flask import Blueprint, request, jsonify
from services.openai_handler import generate_story
from services.dalle_handler import generate_image
from flask_jwt_extended import jwt_required
import logging
import os

story_bp = Blueprint("story", __name__)

@story_bp.route("/generate_story", methods=["POST"])
@jwt_required()
def story_route():
    user_input = request.json.get("message")
    context = request.json.get("context", [])
    storyteller = request.json.get("storyteller")
    character = request.json.get("character")

    print("[DEBUG] Incoming request payload:")
    print(f"user_input: {user_input}")
    print(f"context: {context}")
    print(f"storyteller: {storyteller}")
    print(f"character: {character}")

    if os.getenv("DEV_MODE") == "1":
        context = context[-6:] if len(context) > 6 else context
        time.sleep(10)

    if storyteller and character:
        master_prompt = f"""
You are the narrator of a cinematic and immersive RPG story.

The main character is **the player** — referred to only as *you*. Their personality and fate will be shaped entirely by the player’s choices.

You are narrating in the tone of **"{storyteller['title']}"**, known for its **{storyteller['tone']}** tone and **{storyteller['genre']}** genre.

The player’s:
- Role: {character['role']}
- Traits: {character['traits']}
- Backstory: {character['backstory']}

Start the story with a dramatic, grounded scene based on the character’s backstory and the world’s current tension. Present a vivid moment of conflict or choice.

**Important: Always refer to the player as “you”. Never use their name. Avoid cultural bias. Keep responses cinematic, emotionally immersive, and under 200 words.**

At the end of each scene, present 2–3 clear open-ended choices the player can pick from.

Ready? Begin the story.
""".strip()

        prompt_to_send = master_prompt
        context = []
    else:
        # Follow-up input with clear AI continuation guidance
        prompt_to_send = f"""{user_input.strip()}

Continue the story in second-person (“you”) with cinematic detail and clear pacing. Limit to 3 paragraphs and include 2–3 clear choices the player can take next. End your thought fully — avoid trailing off."""
    
    print("[DEBUG] Final prompt sent to AI:")
    print(prompt_to_send)

    logging.info(f"[STORY] Prompt to AI: {prompt_to_send}")
    story_response = generate_story(prompt_to_send, context)
    logging.info(f"[STORY] AI Response Preview: {story_response[:120]}...")
    print("[DEBUG] Full AI Response:")
    print(story_response)

    return jsonify({"response": story_response})




@story_bp.route("/generate_image", methods=["POST"])
@jwt_required()
def image_route():
    try:
        raw_prompt = request.json.get("prompt", "")
        storyteller = request.json.get("storyteller")
        character = request.json.get("character")

        if not raw_prompt:
            return jsonify({"error": "Missing prompt"}), 400

        # Explicit prompt structure with clear "no text" instruction
        if storyteller and character:
            visual_prompt = f"""
Illustrate a cinematic scene — do not include any words or text in the image.

Style: {storyteller['visual_style']}
Genre: {storyteller['genre']}
Tone: {storyteller['tone']}

Depict a character with:
- Role: {character['role']}
- Traits: {character['traits']}
- Backstory elements: {character['backstory']}

Scene Description: {raw_prompt}
""".strip()
        else:
            visual_prompt = f"Illustrate a cinematic fantasy scene. Do not include any words or text. {raw_prompt}"

        print(f"[DEBUG] Image generation prompt: {visual_prompt}")
        logging.info(f"[IMAGE] Prompt: {visual_prompt}")

        if os.getenv("DEV_MODE") == "1":
            time.sleep(10)
            return jsonify({"image_url": "TEST_MODE"})

        image_url = generate_image(visual_prompt)
        logging.info(f"[IMAGE] URL: {image_url}")
        print(f"[DEBUG] Image URL returned: {image_url}")

        return jsonify({"image_url": image_url})
    except Exception as e:
        logging.error(f"[IMAGE] Error: {e}")
        print(f"[DEBUG] Image generation error: {e}")
        return jsonify({"error": str(e)}), 500
