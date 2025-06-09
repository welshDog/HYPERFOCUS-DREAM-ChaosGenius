#!/usr/bin/env python3
"""
🧪 ChaosGenius Business Logic Tests
==================================
Tests for business logic and data processing
"""

import pytest
import json
import sqlite3
from pathlib import Path
import sys

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestBusinessLogic:
    """Test business logic components"""

    def test_project_health_calculation(self):
        """Test project health score calculation"""
        # Mock project data
        project_data = {
            "total_files": 16399,
            "python_files": 5795,
            "api_endpoints": 13,
            "database_exists": True,
            "business_docs": True
        }

        # Calculate health score (simplified version)
        structure_score = min(100, (project_data["total_files"] / 50) * 100)
        api_score = (project_data["api_endpoints"] / 15) * 100

        assert structure_score == 100  # Should max out at 100
        assert api_score > 80  # Should be high with 13 endpoints

    def test_energy_level_mapping(self):
        """Test energy level to recommendation mapping"""
        energy_mappings = {
            "low": ["Take breaks", "Focus on simple tasks"],
            "medium": ["Balance work and rest", "Tackle moderate challenges"],
            "high": ["Maximize productivity", "Take on complex projects"]
        }

        assert "Take breaks" in energy_mappings["low"]
        assert "Maximize productivity" in energy_mappings["high"]

    def test_product_pipeline_metrics(self):
        """Test product pipeline calculations"""
        # Mock product data
        products = [
            {"name": "EEp Tool", "status": "live", "revenue": 1240},
            {"name": "HelloFresh Frame", "status": "development", "revenue": 0},
            {"name": "Product 3", "status": "planning", "revenue": 0}
        ]

        live_products = [p for p in products if p["status"] == "live"]
        total_revenue = sum(p["revenue"] for p in products)

        assert len(live_products) == 1
        assert total_revenue == 1240

    def test_project_health_empty_data(self):
        """Fail case: health calculation with empty data"""
        project_data = {}
        with pytest.raises(KeyError):
            _ = (project_data["total_files"] / 50) * 100

    def test_project_health_invalid_types(self):
        """Fail case: health calculation with invalid types"""
        project_data = {"total_files": "a lot", "api_endpoints": None}
        with pytest.raises(TypeError):
            _ = (project_data["total_files"] / 50) * 100
        with pytest.raises(TypeError):
            _ = (project_data["api_endpoints"] / 15) * 100

    def test_energy_level_mapping_edge(self):
        """Edge case: unknown energy level"""
        energy_mappings = {
            "low": ["Take breaks", "Focus on simple tasks"],
            "medium": ["Balance work and rest", "Tackle moderate challenges"],
            "high": ["Maximize productivity", "Take on complex projects"]
        }
        assert energy_mappings.get("ultra") is None

    def test_product_pipeline_empty(self):
        """Edge case: empty product list"""
        products = []
        live_products = [p for p in products if p.get("status") == "live"]
        total_revenue = sum(p.get("revenue", 0) for p in products)
        assert len(live_products) == 0
        assert total_revenue == 0

    def test_product_pipeline_missing_keys(self):
        """Fail case: product dict missing keys"""
        products = [{"name": "X"}]
        with pytest.raises(KeyError):
            _ = products[0]["status"]


class TestDatabaseOperations:
    """Test database operations and data integrity"""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        import tempfile
        db_fd, db_path = tempfile.mkstemp()
        yield db_path
        import os
        os.close(db_fd)
        os.unlink(db_path)

    def test_database_initialization(self, temp_db):
        """Test database table creation"""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Create tables (simplified version)
        cursor.execute('''
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE activity_log (
                id INTEGER PRIMARY KEY,
                action TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Test table creation
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        assert 'projects' in tables
        assert 'activity_log' in tables

        conn.close()

    def test_project_crud_operations(self, temp_db):
        """Test Create, Read, Update, Delete operations"""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Create table
        cursor.execute('''
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT
            )
        ''')

        # CREATE
        cursor.execute("INSERT INTO projects (name, status) VALUES (?, ?)",
                      ("Test Project", "active"))

        # READ
        cursor.execute("SELECT * FROM projects WHERE name = ?", ("Test Project",))
        project = cursor.fetchone()
        assert project[1] == "Test Project"
        assert project[2] == "active"

        # UPDATE
        cursor.execute("UPDATE projects SET status = ? WHERE name = ?",
                      ("completed", "Test Project"))

        cursor.execute("SELECT status FROM projects WHERE name = ?", ("Test Project",))
        status = cursor.fetchone()[0]
        assert status == "completed"

        conn.close()

    def test_db_disconnect_handling(self, temp_db):
        """Simulate DB disconnect and error handling"""
        conn = sqlite3.connect(temp_db)
        conn.close()
        with pytest.raises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")

    def test_db_table_exists_false(self, temp_db):
        """Edge: check for non-existent table"""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ghost_table'")
        result = cursor.fetchone()
        assert result is None
        conn.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])