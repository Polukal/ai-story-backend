import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:rootpass@mysql:3306/ai_story"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "yourjwtkey"  # 🔒 replace with something stronger for production
