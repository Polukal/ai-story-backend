from flask import Flask
from flask_cors import CORS
from routes.story import story_bp
import logging

app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Register routes
app.register_blueprint(story_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
