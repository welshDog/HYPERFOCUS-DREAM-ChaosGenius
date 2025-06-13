import uuid
from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from .models import BlacklistedToken, User, db
from .utils import (
    check_rate_limit,
    get_user_ip,
    hash_password,
    increment_failed_attempts,
    log_login_attempt,
    reset_failed_attempts,
    send_discord_alert,
    validate_password_strength,
    verify_password,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """🚀 BROski$ User Registration - Ultra Clean & Secure"""

    try:
        data = request.get_json()
        if not data:
            return jsonify(msg="No data provided"), 400

        username = data.get("username", "").strip()
        password = data.get("password", "")
        email = data.get("email", "").strip()

        # Validation
        if not username or not password:
            return jsonify(msg="Username and password are required"), 400

        if len(username) < 3:
            return jsonify(msg="Username must be at least 3 characters long"), 400

        # Check password strength
        is_strong, password_msg = validate_password_strength(password)
        if not is_strong:
            return jsonify(msg=password_msg), 400

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify(msg="Username already exists! Try another one 💪"), 409

        if email and User.query.filter_by(email=email).first():
            return (
                jsonify(msg="Email already registered! Try logging in instead 🔥"),
                409,
            )

        # Create new user
        hashed_pw = hash_password(password)
        new_user = User(
            username=username,
            email=email if email else None,
            password_hash=hashed_pw,
            public_id=str(uuid.uuid4()),
        )

        db.session.add(new_user)
        db.session.commit()

        # Send Discord success alert
        send_discord_alert(
            title="New User Registration",
            description=f"🎉 New BROski$ joined HyperFocusZone: **{username}**",
            color=0x00FF00,  # Green for success
            fields=[
                {"name": "👤 Username", "value": username, "inline": True},
                {
                    "name": "📧 Email",
                    "value": email if email else "Not provided",
                    "inline": True,
                },
                {
                    "name": "🎯 Initial Focus Score",
                    "value": "0 (Ready to grow! 🌱)",
                    "inline": True,
                },
            ],
        )

        current_app.logger.info(f"New user registered: {username}")

        return (
            jsonify(
                msg="🎉 Welcome to HyperFocusZone, BROski$! Registration successful! 💪",
                user_id=new_user.public_id,
                username=username,
            ),
            201,
        )

    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify(msg="Registration failed. Please try again."), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """🔑 BROski$ Login & Token Issuing - Ultra Secure"""

    try:
        data = request.get_json()
        if not data:
            return jsonify(msg="No data provided"), 400

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return jsonify(msg="Username and password are required"), 400

        # Check rate limiting
        if not check_rate_limit(username):
            log_login_attempt(username, False)
            return (
                jsonify(msg="Too many failed attempts. Account temporarily locked 🔒"),
                429,
            )

        # Find user
        user = User.query.filter_by(username=username).first()

        if not user or not verify_password(user.password_hash, password):
            log_login_attempt(username, False)
            increment_failed_attempts(username)
            return jsonify(msg="Invalid credentials 🚫"), 401

        if user.account_locked:
            log_login_attempt(username, False)
            return jsonify(msg="Account is locked. Contact support 🔒"), 423

        # Successful login
        reset_failed_attempts(username)
        log_login_attempt(username, True)

        # Create tokens with additional claims
        additional_claims = {
            "user_id": user.public_id,
            "hyperfocus_score": user.hyperfocus_score,
            "productivity_level": user.productivity_level,
            "neurodivergent_mode": user.neurodivergent_mode,
        }

        access_token = create_access_token(
            identity=user.username, additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(identity=user.username)

        # Send success Discord alert
        send_discord_alert(
            title="Successful Login",
            description=f"✅ BROski$ **{username}** logged into HyperFocusZone!",
            color=0x00FF00,
            fields=[
                {"name": "👤 Username", "value": username, "inline": True},
                {
                    "name": "🎯 Focus Score",
                    "value": f"{user.hyperfocus_score}/100",
                    "inline": True,
                },
                {
                    "name": "⚡ Productivity Level",
                    "value": user.productivity_level.replace("_", " ").title(),
                    "inline": True,
                },
            ],
        )

        return (
            jsonify(
                msg=f"🔥 Welcome back, {username}! Let's get focused! 💪",
                access_token=access_token,
                refresh_token=refresh_token,
                user=user.to_dict(),
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify(msg="Login failed. Please try again."), 500


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """🔁 Token Refresh - Modern JWT v4 Style"""

    try:
        current_user_username = get_jwt_identity()

        # Get user data for fresh claims
        user = User.query.filter_by(username=current_user_username).first()
        if not user:
            return jsonify(msg="User not found"), 404

        # Create new access token with updated claims
        additional_claims = {
            "user_id": user.public_id,
            "hyperfocus_score": user.hyperfocus_score,
            "productivity_level": user.productivity_level,
            "neurodivergent_mode": user.neurodivergent_mode,
        }

        new_access_token = create_access_token(
            identity=current_user_username, additional_claims=additional_claims
        )

        return (
            jsonify(
                msg="🔄 Token refreshed successfully!", access_token=new_access_token
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return jsonify(msg="Token refresh failed"), 500


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """🚪 BROski$ Logout - Token Blacklisting for Ultra Security"""

    try:
        current_user = get_jwt_identity()
        jti = get_jwt()["jti"]
        token_type = "access"

        # Decode token to get expiration
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        decoded_token = decode_token(token)
        expires_at = datetime.fromtimestamp(decoded_token["exp"])

        # Add token to blacklist
        BlacklistedToken.add_token(jti, token_type, current_user, expires_at)

        # Send Discord logout alert
        send_discord_alert(
            title="User Logout",
            description=f"👋 BROski$ **{current_user}** logged out of HyperFocusZone",
            color=0xFFAA00,  # Orange for logout
            fields=[
                {"name": "👤 Username", "value": current_user, "inline": True},
                {"name": "🔐 Security", "value": "Token blacklisted", "inline": True},
            ],
        )

        return (
            jsonify(msg=f"🔥 See you later, {current_user}! Keep being awesome! 💪"),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return jsonify(msg="Logout failed"), 500


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """👤 Get User Profile - Protected Route"""

    try:
        current_user_username = get_jwt_identity()
        user = User.query.filter_by(username=current_user_username).first()

        if not user:
            return jsonify(msg="User not found"), 404

        return (
            jsonify(msg="✅ Profile retrieved successfully!", user=user.to_dict()),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Profile error: {str(e)}")
        return jsonify(msg="Failed to get profile"), 500


@auth_bp.route("/update-focus", methods=["POST"])
@jwt_required()
def update_focus_score():
    """🎯 Update HyperFocus Score - Neurodivergent Optimization"""

    try:
        current_user_username = get_jwt_identity()
        user = User.query.filter_by(username=current_user_username).first()

        if not user:
            return jsonify(msg="User not found"), 404

        data = request.get_json()
        new_score = data.get("score")

        if new_score is None or not isinstance(new_score, (int, float)):
            return jsonify(msg="Valid score (0-100) is required"), 400

        if not 0 <= new_score <= 100:
            return jsonify(msg="Score must be between 0 and 100"), 400

        old_score = user.hyperfocus_score
        user.update_hyperfocus_score(new_score)
        db.session.commit()

        # Send focus update alert for significant changes
        if abs(new_score - old_score) >= 10:
            color = 0x00FF00 if new_score > old_score else 0xFFAA00
            trend = "📈 INCREASED" if new_score > old_score else "📉 DECREASED"

            send_discord_alert(
                title=f"Focus Score Update - {trend}",
                description=f"🎯 **{current_user_username}** focus score updated!",
                color=color,
                fields=[
                    {"name": "👤 User", "value": current_user_username, "inline": True},
                    {
                        "name": "📊 Previous Score",
                        "value": f"{old_score}/100",
                        "inline": True,
                    },
                    {
                        "name": "🎯 New Score",
                        "value": f"{new_score}/100",
                        "inline": True,
                    },
                    {
                        "name": "⚡ Productivity Level",
                        "value": user.productivity_level.replace("_", " ").title(),
                        "inline": False,
                    },
                ],
            )

        return (
            jsonify(
                msg=f"🎯 Focus score updated to {new_score}! Keep crushing it! 💪",
                user=user.to_dict(),
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Focus update error: {str(e)}")
        return jsonify(msg="Failed to update focus score"), 500


@auth_bp.route("/security-info", methods=["GET"])
@jwt_required()
def get_security_info():
    """🛡️ Get Security Information - Admin/Self View"""

    try:
        current_user_username = get_jwt_identity()
        user = User.query.filter_by(username=current_user_username).first()

        if not user:
            return jsonify(msg="User not found"), 404

        # Get recent login attempts (last 10)
        from .models import LoginAttempt

        recent_attempts = (
            LoginAttempt.query.filter_by(username=current_user_username)
            .order_by(LoginAttempt.attempted_at.desc())
            .limit(10)
            .all()
        )

        attempts_data = [
            {
                "ip_address": attempt.ip_address,
                "success": attempt.success,
                "attempted_at": attempt.attempted_at.isoformat(),
                "user_agent": (
                    attempt.user_agent[:50] + "..."
                    if len(attempt.user_agent) > 50
                    else attempt.user_agent
                ),
            }
            for attempt in recent_attempts
        ]

        return (
            jsonify(
                msg="🛡️ Security info retrieved successfully!",
                security_info={
                    "failed_attempts": user.failed_login_attempts,
                    "account_locked": user.account_locked,
                    "last_login": (
                        user.last_login.isoformat() if user.last_login else None
                    ),
                    "last_login_ip": user.last_login_ip,
                    "recent_login_attempts": attempts_data,
                },
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Security info error: {str(e)}")
        return jsonify(msg="Failed to get security info"), 500
