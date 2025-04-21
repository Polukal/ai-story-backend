from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
from datetime import timedelta
from models.user import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(
        email=data["email"],
        username=data["username"],
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        phone=data.get("phone"),
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    response = make_response(jsonify({"message": "Login successful"}))
    set_access_cookies(response, access_token)
    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logged out"}))
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return jsonify({
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
    })

@auth_bp.route("/check", methods=["GET"])
@jwt_required()
def check_auth():
    return jsonify({"logged_in": True}), 200

