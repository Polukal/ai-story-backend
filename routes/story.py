from flask import Blueprint, request, jsonify
from services.openai_handler import generate_story
from services.dalle_handler import generate_image

story_bp = Blueprint("story", __name__)

@story_bp.route("/generate_story", methods=["POST"])
def story_route():
    user_input = request.json.get("message")
    context = request.json.get("context", [])

    story_response = generate_story(user_input, context)
    return jsonify({"response": story_response})

@story_bp.route("/generate_image", methods=["POST"])
def image_route():
    prompt = request.json.get("prompt")
    image_url = generate_image(prompt)
    return jsonify({"image_url": image_url})
