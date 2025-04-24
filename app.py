from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from db import db, bcrypt  # ✅ Use this shared db instance
from routes.auth import auth_bp
from routes.story import story_bp
from routes.stripe import stripe_bp
from routes.storytellers import storyteller_bp
from config import Config
import logging
import time
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load .env values
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# JWT config for cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_SECURE"] = False  # True only with HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Enable later if needed

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Extensions
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
db.init_app(app)
bcrypt.init_app(app)
JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(story_bp, url_prefix="/api")
app.register_blueprint(stripe_bp, url_prefix="/api/payment")
app.register_blueprint(storyteller_bp)

# Retry DB connection on startup (max 10 attempts)
MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        with app.app_context():
            db.create_all()
        logging.info("✅ Database tables created successfully.")
        break
    except OperationalError:
        logging.warning(f"⏳ DB not ready yet. Retrying ({i + 1}/{MAX_RETRIES})...")
        time.sleep(2)
else:
    logging.error("❌ Could not connect to the database after several attempts.")
    exit(1)

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
