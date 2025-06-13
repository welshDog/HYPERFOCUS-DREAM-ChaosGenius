"""
🔐 BROSKI ULTRA JWT MANAGER - LEGENDARY TOKEN FORTRESS 🔐
Advanced JWT token management with military-grade security
"""

import hashlib
import logging
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Optional, Union

import jwt

logger = logging.getLogger(__name__)


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    RESET = "reset"
    VERIFICATION = "verification"


@dataclass
class TokenConfig:
    """JWT Configuration settings"""

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30
    issuer: str = "broski-ultra-system"
    audience: str = "broski-users"


class BroskiJWTManager:
    """
    🚀 LEGENDARY JWT TOKEN MANAGER 🚀
    Military-grade token generation and validation
    """

    def __init__(self, config: TokenConfig):
        self.config = config
        self._validate_config()

    def _validate_config(self):
        """Validate JWT configuration"""
        if not self.config.secret_key or len(self.config.secret_key) < 32:
            raise ValueError("Secret key must be at least 32 characters long")

    def generate_access_token(self, user_data: Dict[str, Any]) -> str:
        """
        🎫 Generate JWT Access Token
        """
        now = datetime.utcnow()
        payload = {
            "user_id": user_data.get("id"),
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "roles": user_data.get("roles", []),
            "permissions": user_data.get("permissions", []),
            "token_type": TokenType.ACCESS.value,
            "iat": now,
            "exp": now + timedelta(minutes=self.config.access_token_expire_minutes),
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "jti": secrets.token_urlsafe(16),  # Unique token ID
        }

        return jwt.encode(
            payload, self.config.secret_key, algorithm=self.config.algorithm
        )

    def generate_refresh_token(self, user_id: str) -> str:
        """
        🔄 Generate JWT Refresh Token
        """
        now = datetime.utcnow()
        payload = {
            "user_id": user_id,
            "token_type": TokenType.REFRESH.value,
            "iat": now,
            "exp": now + timedelta(days=self.config.refresh_token_expire_days),
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "jti": secrets.token_urlsafe(16),
        }

        return jwt.encode(
            payload, self.config.secret_key, algorithm=self.config.algorithm
        )

    def generate_reset_token(self, user_id: str, expire_minutes: int = 15) -> str:
        """
        🔒 Generate Password Reset Token
        """
        now = datetime.utcnow()
        payload = {
            "user_id": user_id,
            "token_type": TokenType.RESET.value,
            "iat": now,
            "exp": now + timedelta(minutes=expire_minutes),
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "jti": secrets.token_urlsafe(16),
        }

        return jwt.encode(
            payload, self.config.secret_key, algorithm=self.config.algorithm
        )

    def validate_token(
        self, token: str, token_type: Optional[TokenType] = None
    ) -> Dict[str, Any]:
        """
        ✅ Validate JWT Token with military precision
        """
        try:
            payload = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                issuer=self.config.issuer,
                audience=self.config.audience,
            )

            # Validate token type if specified
            if token_type and payload.get("token_type") != token_type.value:
                raise jwt.InvalidTokenError(
                    f"Invalid token type. Expected {token_type.value}"
                )

            # Check if token is expired
            if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
                raise jwt.ExpiredSignatureError("Token has expired")

            logger.info(
                f"Token validated successfully for user: {payload.get('user_id')}"
            )
            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: Token expired")
            raise
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {str(e)}")
            raise jwt.InvalidTokenError("Token validation failed")

    def refresh_access_token(
        self, refresh_token: str, user_data: Dict[str, Any]
    ) -> str:
        """
        🔄 Refresh Access Token using Refresh Token
        """
        try:
            # Validate refresh token
            payload = self.validate_token(refresh_token, TokenType.REFRESH)

            # Generate new access token
            return self.generate_access_token(user_data)

        except Exception as e:
            logger.error(f"Token refresh failed: {str(e)}")
            raise

    def revoke_token(self, token_id: str) -> bool:
        """
        🚫 Revoke Token (add to blacklist)
        """
        # In production, this would add the token JTI to a blacklist in Redis/DB
        logger.info(f"Token revoked: {token_id}")
        return True

    def decode_token_without_verification(self, token: str) -> Dict[str, Any]:
        """
        🔍 Decode token without verification (for debugging)
        """
        return jwt.decode(token, options={"verify_signature": False})

    def generate_secure_secret(self, length: int = 64) -> str:
        """
        🔐 Generate cryptographically secure secret key
        """
        return secrets.token_urlsafe(length)

    def hash_password(
        self, password: str, salt: Optional[str] = None
    ) -> tuple[str, str]:
        """
        🔒 Hash password with secure salt
        """
        if not salt:
            salt = secrets.token_urlsafe(32)

        # Use PBKDF2 with SHA-256
        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000,  # 100k iterations
        )

        return password_hash.hex(), salt

    def verify_password(self, password: str, hash_hex: str, salt: str) -> bool:
        """
        ✅ Verify password against hash
        """
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )

        return password_hash.hex() == hash_hex
