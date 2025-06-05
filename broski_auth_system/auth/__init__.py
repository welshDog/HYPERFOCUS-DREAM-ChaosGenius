"""
🔥 BROski$ Auth System - Authentication Module
Ultra-secure, neurodivergent-optimized authentication for HyperFocusZone
"""

from .models import BlacklistedToken, User
from .routes import auth_bp
from .utils import hash_password, send_discord_alert, verify_password

__all__ = [
    "User",
    "BlacklistedToken",
    "auth_bp",
    "hash_password",
    "verify_password",
    "send_discord_alert",
]
