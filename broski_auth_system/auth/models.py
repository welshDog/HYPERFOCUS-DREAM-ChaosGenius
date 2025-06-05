import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """🔥 BROski$ User Model - Ultra Secure User Management 🔥"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # HyperFocus Profile
    hyperfocus_score = db.Column(db.Integer, default=0)
    productivity_level = db.Column(db.String(20), default="getting_started")
    neurodivergent_mode = db.Column(db.Boolean, default=True)

    # Security Features
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_login_ip = db.Column(db.String(45))
    account_locked = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # User ID for JWT
    public_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()))

    def __repr__(self):
        return f"<BROski$ User {self.username}>"

    def to_dict(self):
        """Convert user to dictionary for JSON responses"""
        return {
            "id": self.public_id,
            "username": self.username,
            "email": self.email,
            "hyperfocus_score": self.hyperfocus_score,
            "productivity_level": self.productivity_level,
            "neurodivergent_mode": self.neurodivergent_mode,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }

    def update_hyperfocus_score(self, score):
        """Update user's hyperfocus score"""
        self.hyperfocus_score = max(0, min(100, score))
        if score >= 90:
            self.productivity_level = "ultra_focused"
        elif score >= 70:
            self.productivity_level = "highly_focused"
        elif score >= 50:
            self.productivity_level = "moderately_focused"
        else:
            self.productivity_level = "needs_boost"


class BlacklistedToken(db.Model):
    """🔐 Token Blacklist for Ultra Security 🔐"""

    __tablename__ = "blacklisted_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(80), nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<BlacklistedToken {self.jti}>"

    @classmethod
    def is_blacklisted(cls, jti):
        """Check if a token is blacklisted"""
        return cls.query.filter_by(jti=jti).first() is not None

    @classmethod
    def add_token(cls, jti, token_type, user_identity, expires_at):
        """Add a token to the blacklist"""
        blacklisted_token = cls(
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires_at=expires_at,
        )
        db.session.add(blacklisted_token)
        db.session.commit()


class LoginAttempt(db.Model):
    """🛡️ Track Login Attempts for Security 🛡️"""

    __tablename__ = "login_attempts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.Text)

    def __repr__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"<LoginAttempt {self.username} - {status}>"
