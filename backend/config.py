# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://localhost/off_dashboard"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATELIMIT_DEFAULT = "100/minute"
    RATELIMIT_STORAGE_URI = os.environ.get("REDIS_URL", "memory://")
