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

    if os.getenv("DEV_MODE") == "1":
        context = context[-6:] if len(context) > 6 else context
        time.sleep(10)

    # Master prompt generation if new story start
    if storyteller and character:
        master_prompt = f"""
I want to play an immersive, cinematic RPG with you. The story should begin with a single main character:

**{character['name']}** — a character whose personality and fate will be shaped entirely by my choices throughout the story.

The storytelling will follow the style of a narrator titled **"{storyteller['title']}"**, known for their **{storyteller['tone']}** tone and **{storyteller['genre']}** genre.

Begin with a dramatic, grounded opening scene tied to the character’s backstory and current state of the world. Present a dilemma or confrontation.

Character Role: {character['role']}
Traits: {character['traits']}
Backstory: {character['backstory']}

I will respond in-character with open-ended answers. You will continue the story based on my actions, escalating consequences, character evolution, and immersive world-building.

Maintain a cinematic tone with emotional depth and narrative weight.

Ready? Begin the story with a cinematic opening scene.
"""
        prompt_to_send = master_prompt.strip()
        context = []  # reset for new story
    else:
        prompt_to_send = user_input

    logging.info(f"[STORY] Prompt to AI: {prompt_to_send}")
    story_response = generate_story(prompt_to_send, context)
    logging.info(f"[STORY] AI Response Preview: {story_response[:120]}...")

    return jsonify({"response": story_response})



@story_bp.route("/generate_image", methods=["POST"])
@jwt_required()
def image_route():
    try:
        prompt = request.json.get("prompt", "")

        if os.getenv("DEV_MODE") == "1":
            time.sleep(10)  # Simulate loading delay for image

        logging.info(f"[IMAGE] Prompt: {prompt}")
        image_url = generate_image(prompt)
        logging.info(f"[IMAGE] URL: {image_url}")

        return jsonify({"image_url": image_url})
    except Exception as e:
        logging.error(f"[IMAGE] Error: {e}")
        return jsonify({"error": str(e)}), 500
