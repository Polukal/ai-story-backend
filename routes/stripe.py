from flask import Blueprint, request, jsonify
import stripe
import os
from models.user import db, User

stripe_bp = Blueprint("payment_routes", __name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Replace this with your actual webhook secret from Stripe dashboard
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@stripe_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session["customer_email"]
        metadata = session.get("metadata", {})
        credit_amount = int(metadata.get("credits", 0))

        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.credits += credit_amount
            db.session.commit()

    return jsonify({"status": "success"})
