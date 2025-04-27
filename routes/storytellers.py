from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.storytellers import db, Storyteller
import os
import logging
from utils import file_upload

storyteller_bp = Blueprint("storyteller", __name__)
UPLOAD_FOLDER = 'static/uploads/storytellers'

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
    try:
        title = request.form.get("title")
        genre = request.form.get("genre")
        tone = request.form.get("tone")
        plot_setup = request.form.get("plot_setup")
        visual_style = request.form.get("visual_style")
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

        storyteller = Storyteller(
            user_id=user_id,
            title=title,
            genre=genre,
            tone=tone,
            plot_setup=plot_setup,
            visual_style=visual_style,
            image_url=image_url,
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
    storyteller = Storyteller.query.filter_by(id=id, user_id=user_id).first()
    if not storyteller:
        return jsonify({"error": "Storyteller not found"}), 404
    try:
        title = request.form.get("title")
        genre = request.form.get("genre")
        tone = request.form.get("tone")
        plot_setup = request.form.get("plot_setup")
        visual_style = request.form.get("visual_style")
        image = request.files.get("image")

        if title:
            storyteller.title = title
        if genre:
            storyteller.genre = genre
        if tone:
            storyteller.tone = tone
        if plot_setup:
            storyteller.plot_setup = plot_setup
        if visual_style:
            storyteller.visual_style = visual_style

        if image:
            if not file_upload.allowed_file(image.filename):
                return jsonify({"error": "Invalid file type. Only PNG, JPG, JPEG allowed."}), 400
            if not file_upload.validate_file_size(image):
                return jsonify({"error": "File too large. Max 5MB allowed."}), 400

            if storyteller.image_url:
                file_upload.delete_old_file(storyteller.image_url)

            filename = file_upload.generate_unique_filename(image.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)

            file_upload.resize_image(filepath)
            storyteller.image_url = f"/{filepath}"

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
        if storyteller.image_url:
            file_upload.delete_old_file(storyteller.image_url)

        db.session.delete(storyteller)
        db.session.commit()
        return jsonify({"message": "Storyteller deleted"})
    except Exception as e:
        logging.error(f"[STORYTELLER] Delete error: {e}")
        return jsonify({"error": "Failed to delete storyteller"}), 500
