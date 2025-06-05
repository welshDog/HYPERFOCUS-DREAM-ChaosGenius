#!/usr/bin/env python3
"""
🧠🚀💜 CHAOSGENIUS HYPERFOCUS BOARD API - ULTRA EDITION 💜🚀🧠
================================================================
Advanced hyperfocus monitoring and productivity tracking API
WOOP WOOP - NEURODIVERGENT PRODUCTIVITY REVOLUTION!
"""

import json
import logging
import os
import sqlite3
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

import psutil
import requests
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HyperfocusEngine:
    """Advanced hyperfocus and productivity tracking engine"""

    def __init__(self):
        self.session_start = datetime.now()
        self.focus_sessions = []
        self.productivity_score = 0
        self.energy_level = "high"

    def get_system_health(self):
        """Get comprehensive system health metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Check ChaosGenius processes
            processes = self.check_chaosgenius_processes()

            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available_gb": f"{memory.available / (1024**3):.1f}",
                "disk_usage": disk.percent,
                "disk_free_gb": f"{disk.free / (1024**3):.1f}",
                "chaosgenius_processes": len(processes),
                "load_average": os.getloadavg()[0] if hasattr(os, "getloadavg") else 0,
                "uptime": self.get_system_uptime(),
                "health_status": (
                    "excellent"
                    if cpu_percent < 50 and memory.percent < 80
                    else "good" if cpu_percent < 80 else "needs_attention"
                ),
            }
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {"error": f"Could not get system health: {e}"}

    def check_chaosgenius_processes(self):
        """Check all ChaosGenius related processes"""
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            processes = []

            for line in result.stdout.split("\n"):
                if any(
                    keyword in line.lower()
                    for keyword in [
                        "dashboard_api",
                        "chaosgenius",
                        "gunicorn",
                        "hyperfocus",
                    ]
                ):
                    if "python" in line:
                        parts = line.split()
                        if len(parts) > 1:
                            processes.append(
                                {
                                    "pid": parts[1],
                                    "cpu": parts[2],
                                    "memory": parts[3],
                                    "command": " ".join(parts[10:])[:50] + "...",
                                }
                            )
            return processes
        except Exception as e:
            logger.error(f"Error checking processes: {e}")
            return []

    def get_system_uptime(self):
        """Get system uptime in human readable format"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            uptime_timedelta = timedelta(seconds=uptime_seconds)
            days = uptime_timedelta.days
            hours, remainder = divmod(uptime_timedelta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{days}d {hours}h {minutes}m"
        except:
            return "Unknown"

    def test_main_dashboard(self):
        """Test connection to main ChaosGenius dashboard"""
        try:
            response = requests.get("http://localhost:5000/api/status", timeout=5)
            return {
                "status": "connected" if response.status_code == 200 else "error",
                "response_time": response.elapsed.total_seconds(),
                "main_dashboard_data": (
                    response.json() if response.status_code == 200 else None
                ),
            }
        except Exception as e:
            return {
                "status": "disconnected",
                "error": str(e),
                "main_dashboard_data": None,
            }

    def calculate_productivity_score(self):
        """Calculate current productivity score based on various metrics"""
        system_health = self.get_system_health()
        main_dashboard = self.test_main_dashboard()

        score = 100

        # Deduct points for poor system performance
        if system_health.get("cpu_usage", 0) > 80:
            score -= 20
        if system_health.get("memory_usage", 0) > 90:
            score -= 30
        if main_dashboard["status"] != "connected":
            score -= 25

        # Add points for good performance
        if system_health.get("chaosgenius_processes", 0) > 5:
            score += 10
        if system_health.get("cpu_usage", 0) < 30:
            score += 5

        return max(0, min(100, score))


# Initialize the hyperfocus engine
hyperfocus_engine = HyperfocusEngine()


def init_enhanced_database():
    """Initialize enhanced SQLite database for hyperfocus tracking with proper migration"""
    conn = sqlite3.connect("chaosgenius.db")
    cursor = conn.cursor()

    # Check if we need to migrate existing tables
    cursor.execute("PRAGMA table_info(activity_log)")
    existing_columns = [column[1] for column in cursor.fetchall()]

    # Enhanced projects table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT,
            energy_level TEXT,
            focus_score INTEGER DEFAULT 0,
            productivity_rating INTEGER DEFAULT 0,
            last_focus_session TIMESTAMP,
            total_focus_time INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Add missing columns to projects table if needed
    cursor.execute("PRAGMA table_info(projects)")
    project_columns = [column[1] for column in cursor.fetchall()]

    missing_project_columns = [
        ("focus_score", "INTEGER DEFAULT 0"),
        ("productivity_rating", "INTEGER DEFAULT 0"),
        ("last_focus_session", "TIMESTAMP"),
        ("total_focus_time", "INTEGER DEFAULT 0"),
    ]

    for col_name, col_def in missing_project_columns:
        if col_name not in project_columns:
            try:
                cursor.execute(f"ALTER TABLE projects ADD COLUMN {col_name} {col_def}")
            except sqlite3.OperationalError:
                pass  # Column might already exist

    # Focus sessions table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY,
            project_id INTEGER,
            session_type TEXT,
            duration_minutes INTEGER,
            productivity_score INTEGER,
            energy_before TEXT,
            energy_after TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """
    )

    # Enhanced activity log table - handle migration
    if "productivity_impact" not in existing_columns:
        # Add missing columns to existing activity_log table
        missing_activity_columns = [
            ("productivity_impact", "INTEGER DEFAULT 0"),
            ("energy_level", "TEXT DEFAULT 'medium'"),
            ("focus_state", "TEXT DEFAULT 'normal'"),
        ]

        for col_name, col_def in missing_activity_columns:
            try:
                cursor.execute(
                    f"ALTER TABLE activity_log ADD COLUMN {col_name} {col_def}"
                )
            except sqlite3.OperationalError:
                pass  # Column might already exist

    # Create activity_log table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY,
            action TEXT NOT NULL,
            type TEXT,
            details TEXT,
            productivity_impact INTEGER DEFAULT 0,
            energy_level TEXT DEFAULT 'medium',
            focus_state TEXT DEFAULT 'normal',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # System health log table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS system_health_log (
            id INTEGER PRIMARY KEY,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            process_count INTEGER,
            health_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Insert enhanced default data if projects table is empty
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """
            INSERT INTO projects (name, status, energy_level, focus_score, productivity_rating)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Hyperfocus Zone Ultra Studio", "Active Development", "high", 85, 92),
        )

    # Check if we need to add enhanced initial activities
    cursor.execute(
        "SELECT COUNT(*) FROM activity_log WHERE action LIKE '%HBoard API Ultra%'"
    )
    if cursor.fetchone()[0] == 0:
        # Add enhanced initial activities
        activities = [
            (
                "HBoard API Ultra initialized",
                "system",
                "Advanced hyperfocus tracking activated",
                15,
                "high",
                "focused",
            ),
            (
                "Productivity engine started",
                "hyperfocus",
                "Real-time monitoring engaged",
                20,
                "high",
                "deep_focus",
            ),
            (
                "System health monitoring active",
                "system",
                "Full resource tracking online",
                10,
                "high",
                "focused",
            ),
            (
                "Neurodivergent optimization activated",
                "ai",
                "ADHD-friendly workflows enabled",
                25,
                "high",
                "hyperfocus",
            ),
        ]

        for action, type_, details, impact, energy, focus in activities:
            cursor.execute(
                """
                INSERT INTO activity_log (action, type, details, productivity_impact, energy_level, focus_state)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (action, type_, details, impact, energy, focus),
            )

    conn.commit()
    conn.close()
    print("✅ Database migration completed successfully!")


@app.route("/api/status")
def api_status():
    """Enhanced API status with full system integration"""
    main_dashboard = hyperfocus_engine.test_main_dashboard()
    system_health = hyperfocus_engine.get_system_health()
    productivity_score = hyperfocus_engine.calculate_productivity_score()

    return jsonify(
        {
            "status": "active",
            "message": "ChaosGenius HBoard API Ultra - Hyperfocus Engine Running",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0-ultra",
            "services": {
                "hyperfocus_engine": "active",
                "productivity_tracker": "monitoring",
                "main_dashboard": main_dashboard["status"],
                "system_health": system_health.get("health_status", "unknown"),
            },
            "productivity_score": productivity_score,
            "session_duration": str(datetime.now() - hyperfocus_engine.session_start),
            "integration": {
                "main_api_connected": main_dashboard["status"] == "connected",
                "response_time": main_dashboard.get("response_time", 0),
                "processes_running": system_health.get("chaosgenius_processes", 0),
            },
        }
    )


@app.route("/api/health")
def health_check():
    """Comprehensive health check with system metrics"""
    system_health = hyperfocus_engine.get_system_health()
    main_dashboard = hyperfocus_engine.test_main_dashboard()

    return jsonify(
        {
            "status": "healthy",
            "service": "HBoard API Ultra",
            "timestamp": datetime.now().isoformat(),
            "system_health": system_health,
            "main_dashboard_connection": main_dashboard,
            "uptime": hyperfocus_engine.get_system_uptime(),
            "processes": hyperfocus_engine.check_chaosgenius_processes(),
        }
    )


@app.route("/api/hyperfocus")
def hyperfocus_metrics():
    """Get current hyperfocus and productivity metrics"""
    productivity_score = hyperfocus_engine.calculate_productivity_score()
    system_health = hyperfocus_engine.get_system_health()

    return jsonify(
        {
            "productivity_score": productivity_score,
            "energy_level": hyperfocus_engine.energy_level,
            "session_duration": str(datetime.now() - hyperfocus_engine.session_start),
            "focus_state": (
                "hyperfocus"
                if productivity_score > 80
                else "focused" if productivity_score > 60 else "distracted"
            ),
            "system_performance": {
                "cpu_optimal": system_health.get("cpu_usage", 0) < 50,
                "memory_optimal": system_health.get("memory_usage", 0) < 80,
                "processes_healthy": system_health.get("chaosgenius_processes", 0) > 3,
            },
            "recommendations": [
                (
                    "🧠 System running optimally for hyperfocus!"
                    if productivity_score > 80
                    else "⚡ Consider closing unused applications"
                ),
                (
                    "💜 Neurodivergent optimization active"
                    if system_health.get("chaosgenius_processes", 0) > 5
                    else "🔧 Start more ChaosGenius processes"
                ),
                (
                    "🚀 Perfect environment for deep work!"
                    if system_health.get("health_status") == "excellent"
                    else "📊 Monitor system resources"
                ),
            ],
        }
    )


@app.route("/api/projects")
def get_projects():
    """Get all projects with hyperfocus metrics"""
    conn = sqlite3.connect("chaosgenius.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, status, energy_level, focus_score, productivity_rating,
               total_focus_time, created_at, updated_at
        FROM projects
        ORDER BY updated_at DESC
    """
    )

    projects = []
    for row in cursor.fetchall():
        projects.append(
            {
                "id": row[0],
                "name": row[1],
                "status": row[2],
                "energy_level": row[3],
                "focus_score": row[4],
                "productivity_rating": row[5],
                "total_focus_time": row[6],
                "created_at": row[7],
                "updated_at": row[8],
            }
        )

    conn.close()
    return jsonify({"projects": projects})


@app.route("/api/activity")
def get_activity():
    """Get recent activity with productivity metrics"""
    conn = sqlite3.connect("chaosgenius.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT action, type, details, productivity_impact, energy_level, focus_state, created_at
        FROM activity_log
        ORDER BY created_at DESC
        LIMIT 20
    """
    )

    activities = []
    for row in cursor.fetchall():
        activities.append(
            {
                "action": row[0],
                "type": row[1],
                "details": row[2],
                "productivity_impact": row[3],
                "energy_level": row[4],
                "focus_state": row[5],
                "created_at": row[6],
            }
        )

    conn.close()
    return jsonify({"activities": activities})


@app.route("/api/dashboard")
def dashboard_overview():
    """Get complete dashboard overview for hyperfocus monitoring"""
    productivity_score = hyperfocus_engine.calculate_productivity_score()
    system_health = hyperfocus_engine.get_system_health()
    main_dashboard = hyperfocus_engine.test_main_dashboard()

    # Get recent activity
    conn = sqlite3.connect("chaosgenius.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM activity_log WHERE created_at > datetime('now', '-1 hour')"
    )
    recent_activity_count = cursor.fetchone()[0]
    conn.close()

    return jsonify(
        {
            "overview": {
                "productivity_score": productivity_score,
                "energy_level": hyperfocus_engine.energy_level,
                "focus_state": (
                    "hyperfocus"
                    if productivity_score > 80
                    else "focused" if productivity_score > 60 else "needs_boost"
                ),
                "session_duration": str(
                    datetime.now() - hyperfocus_engine.session_start
                ),
                "recent_activity_count": recent_activity_count,
            },
            "system": system_health,
            "integration": {
                "main_dashboard": main_dashboard["status"],
                "api_response_time": main_dashboard.get("response_time", 0),
                "full_system_operational": main_dashboard["status"] == "connected"
                and system_health.get("chaosgenius_processes", 0) > 3,
            },
            "timestamp": datetime.now().isoformat(),
        }
    )


if __name__ == "__main__":
    print("🧠🚀💜 CHAOSGENIUS HYPERFOCUS BOARD API ULTRA STARTING! 💜🚀🧠")
    print("WOOP WOOP - NEURODIVERGENT PRODUCTIVITY REVOLUTION!")
    print()

    # Initialize enhanced database
    init_enhanced_database()

    # Log system startup
    system_health = hyperfocus_engine.get_system_health()
    conn = sqlite3.connect("chaosgenius.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO activity_log (action, type, details, productivity_impact, energy_level, focus_state)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            "HBoard API Ultra started",
            "system",
            f"Advanced hyperfocus tracking online with {system_health.get('chaosgenius_processes', 0)} processes",
            20,
            "high",
            "focused",
        ),
    )
    conn.commit()
    conn.close()

    print("✅ Enhanced database initialized")
    print("✅ Hyperfocus engine activated")
    print("✅ System health monitoring online")
    print(
        f"✅ Found {system_health.get('chaosgenius_processes', 0)} ChaosGenius processes"
    )
    print()
    print("🎯 HBoard API Ultra running on http://localhost:5001")
    print("🔗 Integrated with main dashboard on http://localhost:5000")
    print("💜 Ready for neurodivergent productivity optimization!")

    app.run(debug=True, host="0.0.0.0", port=5001)
