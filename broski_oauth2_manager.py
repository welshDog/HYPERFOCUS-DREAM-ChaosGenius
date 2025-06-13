#!/usr/bin/env python3
"""
🚀💥 BROSKI OAUTH2 AUTHENTICATION SYSTEM 💥🚀
LEGENDARY OAuth2 flow with PKCE for Discord and all integrations
By Command of Chief Lyndz - BROski∞ Security Edition
"""

import base64
import hashlib
import os
import secrets
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class BROskiOAuth2Manager:
    """🔐 LEGENDARY OAuth2 Authentication Manager"""

    def __init__(self):
        # Discord OAuth2 Configuration
        self.discord_client_id = os.getenv("DISCORD_APPLICATION_ID")
        self.discord_client_secret = os.getenv(
            "DISCORD_CLIENT_SECRET", "3gp9hupUeCAp8TGVXVfRLj45tNWUPfhK"
        )
        self.discord_redirect_uri = "http://localhost:8080/auth/discord/callback"

        # TikTok OAuth2 Configuration
        self.tiktok_client_id = os.getenv("TIKTOK_CLIENT_KEY")
        self.tiktok_client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
        self.tiktok_redirect_uri = os.getenv("TIKTOK_REDIRECT_URI")

        # OAuth2 sessions storage
        self.active_sessions = {}

    def generate_pkce_challenge(self) -> Dict[str, str]:
        """🔒 Generate PKCE challenge for OAuth2 security"""
        # Generate code verifier (43-128 characters)
        code_verifier = (
            base64.urlsafe_b64encode(secrets.token_bytes(32))
            .decode("utf-8")
            .rstrip("=")
        )

        # Generate code challenge
        code_challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode("utf-8")).digest()
            )
            .decode("utf-8")
            .rstrip("=")
        )

        return {
            "code_verifier": code_verifier,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

    def generate_discord_auth_url(self, user_id: str = None) -> Dict[str, str]:
        """🤖 Generate Discord OAuth2 authorization URL"""
        state = secrets.token_urlsafe(32)
        pkce = self.generate_pkce_challenge()

        # Store session data
        session_id = secrets.token_urlsafe(16)
        self.active_sessions[session_id] = {
            "state": state,
            "pkce": pkce,
            "user_id": user_id,
            "platform": "discord",
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(minutes=10),
        }

        # Discord OAuth2 scopes
        scopes = [
            "identify",
            "email",
            "guilds",
            "guilds.join",
            "bot",
            "applications.commands",
        ]

        params = {
            "response_type": "code",
            "client_id": self.discord_client_id,
            "redirect_uri": self.discord_redirect_uri,
            "scope": " ".join(scopes),
            "state": state,
            "code_challenge": pkce["code_challenge"],
            "code_challenge_method": pkce["code_challenge_method"],
            "permissions": "8",  # Administrator permissions for bot
        }

        auth_url = (
            f"https://discord.com/api/oauth2/authorize?{urllib.parse.urlencode(params)}"
        )

        return {
            "auth_url": auth_url,
            "session_id": session_id,
            "state": state,
            "expires_in": 600,  # 10 minutes
        }

    def generate_tiktok_auth_url(self, user_id: str = None) -> Dict[str, str]:
        """📱 Generate TikTok OAuth2 authorization URL"""
        state = secrets.token_urlsafe(32)

        session_id = secrets.token_urlsafe(16)
        self.active_sessions[session_id] = {
            "state": state,
            "user_id": user_id,
            "platform": "tiktok",
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(minutes=10),
        }

        # TikTok OAuth2 scopes
        scopes = ["user.info.basic", "video.list", "video.upload"]

        params = {
            "response_type": "code",
            "client_key": self.tiktok_client_id,
            "redirect_uri": self.tiktok_redirect_uri,
            "scope": ",".join(scopes),
            "state": state,
        }

        auth_url = (
            f"https://www.tiktok.com/auth/authorize/?{urllib.parse.urlencode(params)}"
        )

        return {
            "auth_url": auth_url,
            "session_id": session_id,
            "state": state,
            "expires_in": 600,
        }

    def handle_discord_callback(self, code: str, state: str) -> Dict[str, any]:
        """🎯 Handle Discord OAuth2 callback"""
        # Find session by state
        session = None
        session_id = None

        for sid, sess in self.active_sessions.items():
            if sess["state"] == state and sess["platform"] == "discord":
                session = sess
                session_id = sid
                break

        if not session:
            return {"error": "Invalid state or expired session"}

        if datetime.now() > session["expires_at"]:
            del self.active_sessions[session_id]
            return {"error": "Session expired"}

        # Exchange code for token
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.discord_redirect_uri,
            "client_id": self.discord_client_id,
            "client_secret": self.discord_client_secret,
            "code_verifier": session["pkce"]["code_verifier"],
        }

        try:
            response = requests.post(
                "https://discord.com/api/oauth2/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 200:
                token_info = response.json()

                # Get user info
                user_response = requests.get(
                    "https://discord.com/api/users/@me",
                    headers={"Authorization": f"Bearer {token_info['access_token']}"},
                )

                user_info = (
                    user_response.json() if user_response.status_code == 200 else {}
                )

                # Clean up session
                del self.active_sessions[session_id]

                return {
                    "success": True,
                    "access_token": token_info["access_token"],
                    "refresh_token": token_info.get("refresh_token"),
                    "expires_in": token_info["expires_in"],
                    "user_info": user_info,
                    "platform": "discord",
                }
            else:
                return {"error": f"Token exchange failed: {response.status_code}"}

        except Exception as e:
            return {"error": f"Authentication failed: {str(e)}"}

    def get_bot_invite_url(self) -> str:
        """🤖 Generate proper Discord bot invite URL"""
        params = {
            "client_id": self.discord_client_id,
            "permissions": "8",  # Administrator
            "scope": "bot applications.commands",
        }

        return (
            f"https://discord.com/api/oauth2/authorize?{urllib.parse.urlencode(params)}"
        )

    def cleanup_expired_sessions(self):
        """🧹 Clean up expired OAuth2 sessions"""
        now = datetime.now()
        expired_sessions = [
            sid
            for sid, session in self.active_sessions.items()
            if now > session["expires_at"]
        ]

        for sid in expired_sessions:
            del self.active_sessions[sid]

        return len(expired_sessions)


def main():
    """🚀 Test the OAuth2 system"""
    print("🚀💥 BROSKI OAUTH2 SYSTEM TEST 💥🚀")
    print("=" * 50)

    oauth_manager = BROskiOAuth2Manager()

    # Test Discord OAuth2 URL generation
    discord_auth = oauth_manager.generate_discord_auth_url("test_user_123")
    print("✅ Discord OAuth2 URL generated!")
    print(f"🔗 Auth URL: {discord_auth['auth_url']}")
    print(f"🆔 Session ID: {discord_auth['session_id']}")
    print()

    # Test TikTok OAuth2 URL generation
    if oauth_manager.tiktok_client_id:
        tiktok_auth = oauth_manager.generate_tiktok_auth_url("test_user_123")
        print("✅ TikTok OAuth2 URL generated!")
        print(f"🔗 Auth URL: {tiktok_auth['auth_url']}")
        print()

    # Test bot invite URL
    bot_invite = oauth_manager.get_bot_invite_url()
    print("✅ Discord Bot Invite URL:")
    print(f"🤖 {bot_invite}")
    print()

    print("🔥 OAUTH2 SYSTEM READY FOR LEGENDARY INTEGRATIONS! 🔥")


if __name__ == "__main__":
    main()
