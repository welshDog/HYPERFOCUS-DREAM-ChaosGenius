from datetime import datetime

import bcrypt
import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
from flask import current_app, request
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password):
    """🔐 Hash password with bcrypt ultra security"""
    return generate_password_hash(password, method="pbkdf2:sha256")


def verify_password(password_hash, password):
    """🔓 Verify password against hash"""
    return check_password_hash(password_hash, password)


def send_discord_alert(title, description, color=0x00FF00, fields=None):
    """🔔 Send Discord webhook alert for BROski$ Auth events"""

    if not current_app.config.get("DISCORD_ALERTS_ENABLED"):
        return False

    webhook_url = current_app.config.get("DISCORD_WEBHOOK_URL")
    if not webhook_url or webhook_url == "your_discord_webhook_url_here":
        return False

    try:
        webhook = DiscordWebhook(url=webhook_url)

        embed = DiscordEmbed(
            title=f"🔥 BROski$ Auth Alert: {title}",
            description=description,
            color=color,
            timestamp=datetime.utcnow(),
        )

        # Add HyperFocusZone branding
        embed.set_author(
            name="HyperFocusZone Security System",
            icon_url="https://i.imgur.com/4M34hi2.png",
        )

        # Add fields if provided
        if fields:
            for field in fields:
                embed.add_embed_field(
                    name=field.get("name", "Field"),
                    value=field.get("value", "No value"),
                    inline=field.get("inline", False),
                )

        # Add system info
        embed.add_embed_field(
            name="🕐 Timestamp",
            value=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            inline=True,
        )

        # Add request info if available
        if request:
            embed.add_embed_field(
                name="🌐 IP Address", value=get_user_ip(), inline=True
            )

            embed.add_embed_field(
                name="🔍 User Agent",
                value=request.headers.get("User-Agent", "Unknown")[:100] + "...",
                inline=False,
            )

        embed.set_footer(text="BROski$ Auth System | HyperFocusZone")

        webhook.add_embed(embed)
        response = webhook.execute()

        return response.status_code == 200

    except Exception as e:
        current_app.logger.error(f"Discord webhook failed: {str(e)}")
        return False


def get_user_ip():
    """🌐 Get user's real IP address (Cloudflare compatible)"""
    # Check for Cloudflare headers first
    ip = request.headers.get("CF-Connecting-IP")
    if ip:
        return ip

    # Check for other proxy headers
    ip = request.headers.get("X-Forwarded-For")
    if ip:
        return ip.split(",")[0].strip()

    ip = request.headers.get("X-Real-IP")
    if ip:
        return ip

    # Fallback to remote address
    return request.remote_addr or "Unknown"


def log_login_attempt(username, success, ip_address=None, user_agent=None):
    """📊 Log login attempt for security monitoring"""
    from .models import LoginAttempt, db

    attempt = LoginAttempt(
        username=username,
        ip_address=ip_address or get_user_ip(),
        success=success,
        user_agent=user_agent or request.headers.get("User-Agent", "Unknown"),
    )

    db.session.add(attempt)
    db.session.commit()

    # Send Discord alert for failed attempts
    if not success:
        send_discord_alert(
            title="Failed Login Attempt",
            description=f"Failed login attempt for user: **{username}**",
            color=0xFF0000,  # Red color for failed attempts
            fields=[
                {"name": "👤 Username", "value": username, "inline": True},
                {
                    "name": "🌐 IP Address",
                    "value": ip_address or get_user_ip(),
                    "inline": True,
                },
            ],
        )


def validate_password_strength(password):
    """🛡️ Validate password strength for neurodivergent-friendly security"""

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if score < 3:
        return (
            False,
            "Password must contain at least 3 of: uppercase, lowercase, numbers, special characters",
        )

    return True, "Password strength is good! 💪"


def check_rate_limit(username, max_attempts=5):
    """⚡ Check if user has exceeded login attempts"""
    from .models import User

    user = User.query.filter_by(username=username).first()
    if not user:
        return True  # Allow attempt for non-existent users (to prevent enumeration)

    if user.failed_login_attempts >= max_attempts:
        return False

    return True


def reset_failed_attempts(username):
    """✅ Reset failed login attempts on successful login"""
    from .models import User, db

    user = User.query.filter_by(username=username).first()
    if user:
        user.failed_login_attempts = 0
        user.account_locked = False
        user.last_login = datetime.utcnow()
        user.last_login_ip = get_user_ip()
        db.session.commit()


def increment_failed_attempts(username):
    """❌ Increment failed login attempts"""
    from .models import User, db

    user = User.query.filter_by(username=username).first()
    if user:
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= current_app.config.get(
            "MAX_LOGIN_ATTEMPTS", 5
        ):
            user.account_locked = True
        db.session.commit()
