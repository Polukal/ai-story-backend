from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.storytellers import db, Storyteller
import logging

storyteller_bp = Blueprint("storyteller", __name__)

@storyteller_bp.route("/api/storytellers", methods=["GET"])
@jwt_required()
def get_storytellers():
    user_id = get_jwt_identity()
    storytellers = Storyteller.query.filter_by(user_id=user_id).all()
    result = [s.to_dict() for s in storytellers]
    return jsonify(result)

@storyteller_bp.route("/api/storytellers", methods=["POST"])
@jwt_required()
def create_storyteller():
    user_id = get_jwt_identity()
    data = request.json
    try:
        storyteller = Storyteller(
            user_id=user_id,
            title=data.get("title"),
            genre=data.get("genre"),
            tone=data.get("tone"),
            plot_setup=data.get("plot_setup"),
            visual_style=data.get("visual_style"),
        )
        db.session.add(storyteller)
        db.session.commit()
        return jsonify(storyteller.to_dict()), 201
    except Exception as e:
        logging.error(f"[STORYTELLER] Creation error: {e}")
        return jsonify({"error": "Failed to create storyteller"}), 500

@storyteller_bp.route("/api/storytellers/<int:id>", methods=["PUT"])
@jwt_required()
def update_storyteller(id):
    user_id = get_jwt_identity()
    data = request.json
    storyteller = Storyteller.query.filter_by(id=id, user_id=user_id).first()
    if not storyteller:
        return jsonify({"error": "Storyteller not found"}), 404
    try:
        storyteller.title = data.get("title", storyteller.title)
        storyteller.genre = data.get("genre", storyteller.genre)
        storyteller.tone = data.get("tone", storyteller.tone)
        storyteller.plot_setup = data.get("plot_setup", storyteller.plot_setup)
        storyteller.visual_style = data.get("visual_style", storyteller.visual_style)
        db.session.commit()
        return jsonify(storyteller.to_dict())
    except Exception as e:
        logging.error(f"[STORYTELLER] Update error: {e}")
        return jsonify({"error": "Failed to update storyteller"}), 500

@storyteller_bp.route("/api/storytellers/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_storyteller(id):
    user_id = get_jwt_identity()
    storyteller = Storyteller.query.filter_by(id=id, user_id=user_id).first()
    if not storyteller:
        return jsonify({"error": "Storyteller not found"}), 404
    try:
        db.session.delete(storyteller)
        db.session.commit()
        return jsonify({"message": "Storyteller deleted"})
    except Exception as e:
        logging.error(f"[STORYTELLER] Delete error: {e}")
        return jsonify({"error": "Failed to delete storyteller"}), 500
