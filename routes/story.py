from flask import Blueprint, request, jsonify
from services.openai_handler import generate_story
from services.dalle_handler import generate_image
import logging
import os

story_bp = Blueprint("story", __name__)

@story_bp.route("/generate_story", methods=["POST"])
def story_route():
    user_input = request.json.get("message")
    context = request.json.get("context", [])

    if os.getenv("DEV_MODE") == "1":
        context = context[-6:] if len(context) > 6 else context

    logging.info(f"[STORY] User input: {user_input}")
    story_response = generate_story(user_input, context)
    logging.info(f"[STORY] Response (summary): {story_response[:100]}...")

    return jsonify({"response": story_response})


@story_bp.route("/generate_image", methods=["POST"])
def image_route():
    try:
        prompt = request.json.get("prompt", "")
        logging.info(f"[IMAGE] Prompt: {prompt}")

        image_url = generate_image(prompt)
        logging.info(f"[IMAGE] URL: {image_url}")

        return jsonify({"image_url": image_url})
    except Exception as e:
        logging.error(f"[IMAGE] Error: {e}")
        return jsonify({"error": str(e)}), 500
