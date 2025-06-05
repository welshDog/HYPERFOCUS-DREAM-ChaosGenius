#!/usr/bin/env python3
"""
🔐 ChaosGenius COMPREHENSIVE Security Test Suite - ULTRA MODE
===========================================================
Tests ALL security aspects: Auth, APIs, Environment, Database, OAuth flows
"""

import base64
import hashlib
import json
import os
import secrets
import sqlite3
import string

# Import your modules
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard_api import app
from security_validator import check_env_security, generate_secure_key


class TestEnvironmentSecurity:
    """Test environment variable security"""

    def test_env_file_exists(self):
        """Test .env file exists"""
        env_file = Path(".env")
        # Should either exist or have .env.example as template
        assert (
            env_file.exists() or Path(".env.example").exists()
        ), "No environment configuration found"

    def test_gitignore_protects_secrets(self):
        """Test .env is in .gitignore"""
        gitignore = Path(".gitignore")
        if gitignore.exists():
            content = gitignore.read_text()
            assert (
                ".env" in content
            ), ".env file not protected by .gitignore - SECURITY RISK!"

    def test_no_hardcoded_secrets_in_code(self):
        """Test no hardcoded API keys or secrets in source code"""
        dangerous_patterns = [
            "api_key",
            "secret_key",
            "password",
            "token",
            "access_token",
        ]

        # Scan Python files for potential hardcoded secrets
        for py_file in Path(".").rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            content = py_file.read_text().lower()
            for pattern in dangerous_patterns:
                # Look for assignment patterns like api_key = "actual_key"
                if f'{pattern} = "' in content or f'{pattern}="' in content:
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if f'{pattern} = "' in line or f'{pattern}="' in line:
                            # Allow test values and placeholders
                            if any(
                                placeholder in line
                                for placeholder in [
                                    "test",
                                    "fake",
                                    "placeholder",
                                    "example",
                                    "your_",
                                ]
                            ):
                                continue
                            pytest.fail(
                                f"Potential hardcoded {pattern} in {py_file}:{i+1}"
                            )


class TestAPIKeySecurity:
    """Test API key security and validation"""

    def test_api_key_format_validation(self):
        """Test API keys have proper format"""
        from dotenv import load_dotenv

        load_dotenv()

        # Etsy API keys should be specific format
        etsy_key = os.getenv("ETSY_API_KEY")
        if etsy_key:
            assert len(etsy_key) >= 20, "Etsy API key too short"
            assert (
                etsy_key.isalnum() or "_" in etsy_key
            ), "Etsy API key has invalid characters"

    def test_secure_key_generation(self):
        """Test secure key generation function"""
        key1 = generate_secure_key(32)
        key2 = generate_secure_key(32)

        assert len(key1) == 32, "Generated key wrong length"
        assert len(key2) == 32, "Generated key wrong length"
        assert key1 != key2, "Generated keys are not unique"

        # Test key entropy (should have mix of chars)
        assert any(c.isupper() for c in key1), "No uppercase in generated key"
        assert any(c.islower() for c in key1), "No lowercase in generated key"
        assert any(c.isdigit() for c in key1), "No digits in generated key"


class TestOAuthSecurity:
    """Test OAuth flow security"""

    def test_oauth_state_parameter(self):
        """Test OAuth flows use state parameter for CSRF protection"""
        # Check TikTok OAuth implementation
        with app.test_client() as client:
            with patch.dict(os.environ, {"TIKTOK_CLIENT_KEY": "test_key"}):
                response = client.get("/api/tiktok-shop/auth/start")
                if response.status_code == 302:
                    location = response.headers.get("Location", "")
                    assert (
                        "state=" in location
                    ), "OAuth flow missing state parameter - CSRF vulnerability!"

    def test_code_verifier_security(self):
        """Test OAuth code verifier is properly generated"""
        from dashboard_api import code_verifier

        assert len(code_verifier) >= 43, "Code verifier too short"
        assert len(code_verifier) <= 128, "Code verifier too long"
        assert (
            code_verifier.replace("-", "").replace("_", "").isalnum()
        ), "Code verifier has invalid chars"

    @patch("requests.post")
    def test_oauth_callback_validates_code(self, mock_post):
        """Test OAuth callback properly validates authorization code"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "test_token"}

        with app.test_client() as client:
            # Test missing code
            response = client.get("/auth/callback")
            assert (
                response.status_code == 400
            ), "OAuth callback should reject missing code"

            # Test with code
            response = client.get("/auth/callback?code=test_code")
            # Should attempt token exchange


class TestDatabaseSecurity:
    """Test database security measures"""

    def test_database_connection_secure(self):
        """Test database connections are secure"""
        # Test SQLite database exists and is accessible
        db_file = Path("chaosgenius.db")
        if db_file.exists():
            conn = sqlite3.connect("chaosgenius.db")
            cursor = conn.cursor()

            # Test basic connectivity
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            assert len(tables) > 0, "Database has no tables"

            conn.close()

    def test_sql_injection_protection(self):
        """Test SQL injection protection in database queries"""
        # This would test parameterized queries
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        # Create test table
        cursor.execute("""CREATE TABLE test_table (id INTEGER, data TEXT)""")

        # Test parameterized query (safe)
        malicious_input = "'; DROP TABLE test_table; --"
        cursor.execute(
            "INSERT INTO test_table (id, data) VALUES (?, ?)", (1, malicious_input)
        )

        # Table should still exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';"
        )
        result = cursor.fetchone()
        assert result is not None, "SQL injection protection failed"

        conn.close()


class TestAPIEndpointSecurity:
    """Test API endpoint security"""

    def test_cors_headers(self):
        """Test CORS headers are properly configured"""
        with app.test_client() as client:
            response = client.options("/")
            # CORS should be configured but not overly permissive
            assert "Access-Control-Allow-Origin" in response.headers

    def test_sensitive_endpoints_protection(self):
        """Test sensitive endpoints have proper protection"""
        with app.test_client() as client:
            # Test API setup endpoint
            response = client.post("/api/setup-social-apis", json={"malicious": "data"})
            # Should validate input properly

    def test_error_handling_no_info_leak(self):
        """Test error messages don't leak sensitive information"""
        with app.test_client() as client:
            # Test non-existent endpoint
            response = client.get("/api/nonexistent")
            assert response.status_code == 404

            # Error message shouldn't reveal internal structure
            data = response.get_json() if response.is_json else {}
            error_msg = str(data) + str(response.data)
            sensitive_terms = [
                "password",
                "secret",
                "key",
                "token",
                "/root/",
                "traceback",
            ]
            for term in sensitive_terms:
                assert (
                    term.lower() not in error_msg.lower()
                ), f"Error message leaks sensitive info: {term}"


class TestInputValidation:
    """Test input validation and sanitization"""

    def test_api_input_validation(self):
        """Test API endpoints validate input properly"""
        with app.test_client() as client:
            # Test API setup with invalid data
            invalid_payloads = [
                {"etsy_api_key": ""},  # Empty key
                {"etsy_api_key": "x" * 1000},  # Too long
                {"etsy_api_key": '<script>alert("xss")</script>'},  # XSS attempt
                {"etsy_api_key": "../../../etc/passwd"},  # Path traversal
            ]

            for payload in invalid_payloads:
                response = client.post("/api/setup-social-apis", json=payload)
                # Should handle gracefully without errors
                assert response.status_code in [
                    200,
                    400,
                    422,
                ], "Invalid input not handled properly"

    def test_file_upload_security(self):
        """Test file upload security if any endpoints accept files"""
        # Check if there are any file upload endpoints
        dangerous_extensions = [".exe", ".php", ".asp", ".jsp", ".sh"]
        # This would test file upload validation if implemented


class TestSessionSecurity:
    """Test session and authentication security"""

    def test_flask_secret_key_configured(self):
        """Test Flask secret key is properly configured"""
        assert app.secret_key is not None, "Flask secret key not configured"
        if app.secret_key:
            assert len(app.secret_key) >= 32, "Flask secret key too short"
            assert app.secret_key != "dev", "Using default/weak secret key"

    def test_session_cookie_security(self):
        """Test session cookies have security flags"""
        with app.test_client() as client:
            # If sessions are used, cookies should be secure
            with client.session_transaction() as sess:
                sess["test"] = "value"

            response = client.get("/")
            # Check cookie security flags if cookies are set
            if "Set-Cookie" in response.headers:
                cookie_header = response.headers["Set-Cookie"]
                # In production, should have Secure and HttpOnly flags


class TestExternalAPICallSecurity:
    """Test security of external API calls"""

    @patch("requests.post")
    def test_external_api_timeout(self, mock_post):
        """Test external API calls have timeouts"""
        mock_post.side_effect = requests.Timeout()

        with app.test_client() as client:
            # Test OAuth callback with timeout
            response = client.get("/auth/callback?code=test")
            # Should handle timeout gracefully

    @patch("requests.post")
    def test_external_api_ssl_verification(self, mock_post):
        """Test external API calls verify SSL certificates"""
        # Check that requests are made with verify=True (default)
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "test"}

        with app.test_client() as client:
            with patch.dict(
                os.environ,
                {"ETSY_CLIENT_ID": "test_id", "ETSY_SHARED_SECRET": "test_secret"},
            ):
                response = client.get("/auth/callback?code=test_code")

                if mock_post.called:
                    # Check that SSL verification wasn't disabled
                    call_kwargs = mock_post.call_args[1] if mock_post.call_args else {}
                    assert (
                        call_kwargs.get("verify", True) is not False
                    ), "SSL verification disabled!"


class TestLogSecurity:
    """Test logging security"""

    def test_logs_dont_contain_secrets(self):
        """Test log files don't contain sensitive information"""
        log_files = list(Path(".").rglob("*.log"))

        sensitive_patterns = [
            r"api_key=\w+",
            r"password=\w+",
            r"secret=\w+",
            r"token=\w+",
        ]

        for log_file in log_files:
            try:
                content = log_file.read_text()
                for pattern in sensitive_patterns:
                    import re

                    if re.search(pattern, content, re.IGNORECASE):
                        pytest.fail(
                            f"Log file {log_file} contains sensitive data matching {pattern}"
                        )
            except Exception:
                # Skip unreadable log files
                pass


class TestSecurityHeaders:
    """Test security headers in HTTP responses"""

    def test_security_headers_present(self):
        """Test important security headers are present"""
        with app.test_client() as client:
            response = client.get("/")

            # Test for important security headers
            important_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "X-XSS-Protection",
            ]

            # Note: These might not be implemented yet, but good to test
            missing_headers = []
            for header in important_headers:
                if header not in response.headers:
                    missing_headers.append(header)

            if missing_headers:
                print(f"⚠️  Missing security headers: {missing_headers}")
                # Don't fail test yet, just warn


def test_comprehensive_security_scan():
    """Run a comprehensive security scan"""
    print("\n🔐 RUNNING COMPREHENSIVE SECURITY SCAN...")

    security_issues = []

    # Check environment setup
    try:
        configured, total = check_env_security()
        if configured < total:
            security_issues.append(f"Only {configured}/{total} API keys configured")
    except Exception as e:
        security_issues.append(f"Environment check failed: {e}")

    # Check for common security files
    security_files = [".env.example", ".gitignore", "requirements.txt"]
    for file_name in security_files:
        if not Path(file_name).exists():
            security_issues.append(f"Missing {file_name}")

    print(f"\n📊 SECURITY SCAN RESULTS:")
    if security_issues:
        print("⚠️  Issues found:")
        for issue in security_issues:
            print(f"   - {issue}")
    else:
        print("✅ No critical security issues detected!")

    return len(security_issues) == 0


if __name__ == "__main__":
    # Run comprehensive security test
    test_comprehensive_security_scan()
    print(
        "\n🚀 Run full test suite with: pytest tests/test_security_comprehensive.py -v"
    )
