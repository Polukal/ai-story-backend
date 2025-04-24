from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.characters import Character
from db import db

character_bp = Blueprint("characters", __name__)

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
    data = request.json

    character = Character(
        user_id=user_id,
        name=data.get("name"),
        role=data.get("role"),
        traits=data.get("traits"),
        backstory=data.get("backstory"),
    )

    db.session.add(character)
    db.session.commit()
    return jsonify(character.to_dict()), 201

@character_bp.route("/api/characters/<int:char_id>", methods=["PUT"])
@jwt_required()
def update_character(char_id):
    user_id = get_jwt_identity()
    character = Character.query.filter_by(id=char_id, user_id=user_id).first_or_404()

    data = request.json
    character.name = data.get("name", character.name)
    character.role = data.get("role", character.role)
    character.traits = data.get("traits", character.traits)
    character.backstory = data.get("backstory", character.backstory)

    db.session.commit()
    return jsonify(character.to_dict())

@character_bp.route("/api/characters/<int:char_id>", methods=["DELETE"])
@jwt_required()
def delete_character(char_id):
    user_id = get_jwt_identity()
    character = Character.query.filter_by(id=char_id, user_id=user_id).first_or_404()

    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Character deleted."})
