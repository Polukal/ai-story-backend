
# TODO: Connect the frontend payment request to this flask backend before sending to stripe
#These endpoints are not currently being used.
import os
import stripe
from flask import Blueprint, request, jsonify

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "AI Story Credits (100)",
                    },
                    "unit_amount": 500,  # $5.00
                },
                "quantity": 1,
            }],
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )
        return jsonify({ "url": session.url })
    except Exception as e:
        return jsonify(error=str(e)), 500
