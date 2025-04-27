from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.characters import Character
from db import db
import os
from utils import file_upload

character_bp = Blueprint("characters", __name__)
UPLOAD_FOLDER = 'static/uploads/characters'

@character_bp.route("/api/characters", methods=["GET"])
@jwt_required()
def get_characters():
    user_id = get_jwt_identity()
    characters = Character.query.filter_by(user_id=user_id).all()
    return jsonify([c.to_dict() for c in characters])

@character_bp.route("/api/characters", methods=["POST"])
@jwt_required()
def create_character():
    user_id = get_jwt_identity()

    name = request.form.get("name")
    role = request.form.get("role")
    traits = request.form.get("traits")
    backstory = request.form.get("backstory")
    image = request.files.get("image")

    image_url = None
    if image:
        if not file_upload.allowed_file(image.filename):
            return jsonify({"error": "Invalid file type. Only PNG, JPG, JPEG allowed."}), 400
        if not file_upload.validate_file_size(image):
            return jsonify({"error": "File too large. Max 5MB allowed."}), 400

        filename = file_upload.generate_unique_filename(image.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        file_upload.resize_image(filepath)
        image_url = f"/{filepath}"

    character = Character(
        user_id=user_id,
        name=name,
        role=role,
        traits=traits,
        backstory=backstory,
        image_url=image_url,
    )

    db.session.add(character)
    db.session.commit()
    return jsonify(character.to_dict()), 201

@character_bp.route("/api/characters/<int:char_id>", methods=["PUT"])
@jwt_required()
def update_character(char_id):
    user_id = get_jwt_identity()
    character = Character.query.filter_by(id=char_id, user_id=user_id).first_or_404()

    name = request.form.get("name")
    role = request.form.get("role")
    traits = request.form.get("traits")
    backstory = request.form.get("backstory")
    image = request.files.get("image")

    if name:
        character.name = name
    if role:
        character.role = role
    if traits:
        character.traits = traits
    if backstory:
        character.backstory = backstory

    if image:
        if not file_upload.allowed_file(image.filename):
            return jsonify({"error": "Invalid file type. Only PNG, JPG, JPEG allowed."}), 400
        if not file_upload.validate_file_size(image):
            return jsonify({"error": "File too large. Max 5MB allowed."}), 400

        if character.image_url:
            file_upload.delete_old_file(character.image_url)

        filename = file_upload.generate_unique_filename(image.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        file_upload.resize_image(filepath)
        character.image_url = f"/{filepath}"

    db.session.commit()
    return jsonify(character.to_dict())

@character_bp.route("/api/characters/<int:char_id>", methods=["DELETE"])
@jwt_required()
def delete_character(char_id):
    user_id = get_jwt_identity()
    character = Character.query.filter_by(id=char_id, user_id=user_id).first_or_404()

    if character.image_url:
        file_upload.delete_old_file(character.image_url)

    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Character deleted."})
