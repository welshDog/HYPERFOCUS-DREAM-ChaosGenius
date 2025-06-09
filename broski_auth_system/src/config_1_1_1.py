import os
from datetime import timedelta

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """🔥 BROski$ Auth System - Ultra Configuration Class 🔥"""

    # Flask Configuration
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "hyperfocus-fallback-key"

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "hyperfocus-jwt-fallback"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 2592000))
    )
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///broski_auth.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Server Configuration
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = os.environ.get("FLASK_ENV") == "development"

    # Discord Configuration
    DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
    DISCORD_ALERTS_ENABLED = (
        os.environ.get("DISCORD_ALERTS_ENABLED", "True").lower() == "true"
    )

    # Security Configuration
    BCRYPT_LOG_ROUNDS = int(os.environ.get("BCRYPT_LOG_ROUNDS", 12))
    MAX_LOGIN_ATTEMPTS = int(os.environ.get("MAX_LOGIN_ATTEMPTS", 5))
    IP_BIND_TOKENS = os.environ.get("IP_BIND_TOKENS", "False").lower() == "true"

    # HyperFocus Configuration
    HYPERFOCUS_MODE = os.environ.get("HYPERFOCUS_MODE", "True").lower() == "true"
    NEURODIVERGENT_OPTIMIZED = (
        os.environ.get("NEURODIVERGENT_OPTIMIZED", "True").lower() == "true"
    )
    ULTRA_PERFORMANCE = os.environ.get("ULTRA_PERFORMANCE", "True").lower() == "true"
