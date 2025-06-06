#!/usr/bin/env python3
"""
🧪 Simple Unit Tests - ChaosGenius Core Functions
Basic unit tests that don't require external services
"""

import os
import sys

import pytest

# Add project root to path
sys.path.append("/root/chaosgenius")


def test_basic_imports():
    """Test that core modules can be imported successfully"""
    try:
        # Test basic Python imports
        import datetime
        import json
        import sqlite3

        assert True
    except ImportError as e:
        pytest.fail(f"Basic import failed: {e}")


def test_project_structure():
    """Test that required project files exist"""
    project_root = "/root/chaosgenius"

    # Check for key files
    required_files = [
        "dashboard_api.py",
        "chaosgenius_discord_bot.py",
        "health_check.py",
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(project_root, file)):
            missing_files.append(file)

    assert not missing_files, f"Missing required files: {missing_files}"


def test_ai_modules_structure():
    """Test that AI modules directory structure exists"""
    ai_modules_path = "/root/chaosgenius/ai_modules"
    broski_path = os.path.join(ai_modules_path, "broski")

    assert os.path.exists(ai_modules_path), "ai_modules directory missing"
    assert os.path.exists(broski_path), "broski module directory missing"

    # Check for key broski files
    broski_files = ["broski_core.py", "token_engine.py", "token_commands.py"]

    for file in broski_files:
        file_path = os.path.join(broski_path, file)
        assert os.path.exists(file_path), f"Missing broski file: {file}"


def test_database_creation():
    """Test that we can create and interact with databases"""
    import sqlite3
    import tempfile

    # Create a temporary database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    try:
        # Test database operations
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create a test table
        cursor.execute(
            """
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Insert test data
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test_entry",))
        conn.commit()

        # Query test data
        cursor.execute("SELECT name FROM test_table WHERE id = 1")
        result = cursor.fetchone()

        assert result is not None, "Database query returned no results"
        assert result[0] == "test_entry", f"Expected 'test_entry', got '{result[0]}'"

        conn.close()

    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_json_operations():
    """Test JSON operations for configuration handling"""
    import json
    import tempfile

    test_data = {
        "system_status": "active",
        "intelligence_level": 95,
        "features": ["chat", "tokens", "hyperfocus"],
        "config": {"debug": False, "version": "3.0"},
    }

    # Test JSON serialization
    json_string = json.dumps(test_data)
    assert isinstance(json_string, str), "JSON serialization failed"

    # Test JSON deserialization
    parsed_data = json.loads(json_string)
    assert parsed_data == test_data, "JSON round-trip failed"

    # Test file operations
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump(test_data, tmp)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "r") as f:
            loaded_data = json.load(f)

        assert loaded_data == test_data, "JSON file operations failed"

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_environment_setup():
    """Test that the Python environment is properly configured"""
    import sys

    # Check Python version
    assert sys.version_info >= (3, 8), f"Python 3.8+ required, got {sys.version_info}"

    # Check for required packages
    required_packages = ["flask", "sqlite3", "json", "datetime"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    assert not missing_packages, f"Missing required packages: {missing_packages}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
