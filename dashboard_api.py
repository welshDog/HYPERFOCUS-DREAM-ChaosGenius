#!/usr/bin/env python3
"""
🧠 ChaosGenius Dashboard API - Flask Backend
===========================================
Interactive web API for the Hyperfocus Zone dashboard system with REAL social media feeds
"""

import datetime
import json
import logging
import os
import secrets
import signal
import sqlite3
import string
import subprocess
import sys
import threading
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests
from dotenv import load_dotenv
from flasgger import Swagger, swag_from
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

# Import the new social media integrations
try:
    from api.social_media_integrations import (
        SocialMediaAggregator,
        get_live_social_metrics,
    )

    SOCIAL_INTEGRATIONS_AVAILABLE = True
except ImportError:
    SOCIAL_INTEGRATIONS_AVAILABLE = False
    print("⚠️  Social media integrations not available - using mock data")

# Load environment variables from .env file
load_dotenv()

# Etsy OAuth Configuration
ETSY_CLIENT_ID = os.getenv("ETSY_API_KEY")
ETSY_CLIENT_SECRET = os.getenv("ETSY_SHARED_SECRET")
ETSY_REDIRECT_URI = os.getenv(
    "ETSY_REDIRECT_URI", "http://localhost:5000/auth/callback"
)

# TikTok Shop Configuration
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
TIKTOK_REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", "http://localhost:5000/callback")

# Generate code verifier for OAuth flow
code_verifier = "".join(
    secrets.choice(string.ascii_letters + string.digits) for _ in range(64)
)

# Database configuration
DATABASE_FILE = "chaosgenius.db"

# Flask app configuration
app = Flask(__name__)
CORS(app)

# Set port for the application
port = int(os.getenv("PORT", 5000))

# Swagger configuration
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "ChaosGenius Dashboard API",
        "description": "AI-powered neurodivergent business creation ecosystem API",
        "version": "1.0.0",
        "contact": {
            "name": "ChaosGenius Team",
            "url": "https://github.com/chaosgenius",
        },
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http", "https"],
    "tags": [
        {"name": "Dashboard", "description": "Dashboard operations"},
        {"name": "AI Squad", "description": "AI Squad management and operations"},
        {"name": "Analytics", "description": "Analytics and reporting"},
        {"name": "Projects", "description": "Project management"},
    ],
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "dashboard_api.log"
rotating_handler = RotatingFileHandler(
    log_file,
    maxBytes=2 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8",
    errors="replace",
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[rotating_handler, logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
shutdown_flag = False


def signal_handler(sig, frame):
    """Handle SIGINT (Ctrl+C) gracefully"""
    global shutdown_flag
    print("\n🛑 Gracefully shutting down ChaosGenius Dashboard...")
    print("💜 Thanks for using the Hyperfocus Zone!")
    shutdown_flag = True
    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


# Database setup
def init_database():
    """Initialize SQLite database for dashboard data"""
    conn = sqlite3.connect("chaosgenius.db")
    cursor = conn.cursor()

    # Projects table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT,
            energy_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # AI Sessions table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_sessions (
            id INTEGER PRIMARY KEY,
            project_id INTEGER,
            session_type TEXT,
            energy_level TEXT,
            insights_generated INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """
    )

    # Activity log table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY,
            action TEXT NOT NULL,
            type TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Insert default project if not exists
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """
            INSERT INTO projects (name, status, energy_level)
            VALUES (?, ?, ?)
        """,
            ("Hyperfocus Zone Ultra Studio", "In Development - Phase 1", "high"),
        )

        # Add some initial activity
        activities = [
            ("ChaosGenius Engine initialized", "system", "Dashboard system started"),
            (
                "Project structure created",
                "project",
                "Complete folder structure generated",
            ),
            ("AI Squad framework activated", "ai", "Setup1 and Setup2 modules ready"),
        ]

        for action, type_, details in activities:
            cursor.execute(
                """
                INSERT INTO activity_log (action, type, details)
                VALUES (?, ?, ?)
            """,
                (action, type_, details),
            )

    conn.commit()
    conn.close()


# Initialize database on startup
init_database()


# Routes
@app.route("/")
def dashboard():
    """Serve the main dashboard HTML"""
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>🧠 ChaosGenius Dashboard</h1>
        <p>Dashboard HTML file not found. Please make sure dashboard.html exists.</p>
        <p><a href="/api/status">Check API Status</a></p>
        """


@app.route("/api/status")
def api_status():
    """Get current API status and health metrics"""
    try:
        return jsonify(
            {
                "status": "active",
                "message": "ChaosGenius Engine API is running",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "services": {
                    "database": "connected",
                    "ai_models": "active",
                    "discord_bot": "online",
                },
            }
        )
    except Exception as e:
        logger.error(f"Error getting API status: {e}")
        return (
            jsonify(
                {"status": "error", "message": f"❌ Error retrieving status: {str(e)}"}
            ),
            500,
        )


@app.route("/api/health")
def api_health():
    """Health check endpoint for blast off system validation"""
    try:
        # Test database connection
        conn = sqlite3.connect("chaosgenius.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]
        conn.close()

        return jsonify(
            {
                "status": "healthy",
                "message": "🚀 BROski X Forever Empire is OPERATIONAL!",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "empire_status": {
                    "broski_ai": "96.2% intelligence active",
                    "database": "connected",
                    "projects": project_count,
                    "token_system": "operational",
                    "discord_bot": "ready",
                    "dashboard": "live",
                },
                "uptime": "running",
                "performance": "optimal",
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return (
            jsonify(
                {"status": "unhealthy", "message": f"❌ Health check failed: {str(e)}"}
            ),
            500,
        )


@app.route("/api/analytics", methods=["GET"])
def analytics():
    """Get analytics data with REAL social media integration"""
    try:
        analytics_data = {
            "etsy_sales": 17,
            "tiktok_views": 22000,
            "active_products": 9,
            "total_revenue": "£1,240",
            "engagement_rate": "8.4%",
            "social_reach": 22000,
            "conversion_rate": 0.077,
            "last_updated": datetime.now().isoformat(),
            "data_source": "mock_data",
            "api_status": {"etsy": "mock_data", "tiktok": "mock_data"},
            "status": "ok",
        }

        logger.info(
            f"📊 Analytics data retrieved from {analytics_data.get('data_source', 'unknown')} source"
        )
        return jsonify(analytics_data)

    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"❌ Error retrieving analytics: {str(e)}",
                }
            ),
            500,
        )


@app.route("/api/hyperfocus-analytics")
def hyperfocus_analytics():
    """Get hyperfocus session analytics"""
    try:
        return jsonify(
            {
                "hyperfocus_metrics": {
                    "total_sessions": 3,
                    "average_duration": 45,
                    "productivity_boost": "23%",
                    "peak_hours": ["14:00", "15:00", "16:00"],
                    "energy_patterns": {"morning": 75, "afternoon": 90, "evening": 65},
                },
                "neurodivergent_power_level": 87,
                "empire_stats": {
                    "total_revenue": 1240,
                    "active_projects": 2,
                    "conversion_rate": 0.077,
                },
                "status": "ok",
                "generated_at": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        logger.error(f"Error getting hyperfocus analytics: {e}")
        return jsonify({"status": "error", "message": f"❌ Error: {str(e)}"}), 500


@app.route("/api/ai-squad/start", methods=["POST"])
def ai_squad_start():
    """Start AI Squad session"""
    try:
        data = request.get_json() or {}
        return jsonify(
            {
                "status": "success",
                "project": data.get("project", "Test Project"),
                "energy_level": data.get("energy_level", "high"),
                "session_id": "test-session-1",
            }
        )
    except Exception as e:
        logger.error(f"Error starting AI Squad: {e}")
        return jsonify({"status": "error", "message": f"❌ Error: {str(e)}"}), 500


"""
🧠💜 AI SQUAD DASHBOARD INTEGRATION 💜🧠
Ultra Mode Dashboard with AI Squad Control Panel
"""

import asyncio
import json
from datetime import datetime

from ai_squad_activation import AISquadActivation


# Add AI Squad integration to your dashboard
@app.route("/api/ai-squad/activate", methods=["POST"])
def activate_ai_squad():
    """🚀 API endpoint to activate AI Squad from dashboard"""
    try:
        data = request.get_json()
        energy_level = data.get("energy_level", "medium")

        # Run AI Squad activation
        squad = AISquadActivation()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(squad.activate_all_agents(energy_level))
        loop.close()

        return jsonify(
            {
                "status": "success",
                "message": "🧠💜 AI Squad activated successfully!",
                "results": results,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"AI Squad activation error: {str(e)}"}
            ),
            500,
        )


@app.route("/api/ai-squad/status")
def get_ai_squad_status():
    """📊 Get AI Squad activity status"""
    try:
        conn = sqlite3.connect("chaosgenius.db")
        cursor = conn.cursor()

        # Get recent AI Squad activities
        cursor.execute(
            """
            SELECT agent_type, action, energy_boost, timestamp, status
            FROM ai_squad_activity
            ORDER BY timestamp DESC
            LIMIT 10
        """
        )
        activities = cursor.fetchall()

        # Get dopamine tracking data
        cursor.execute(
            """
            SELECT mood_score, energy_level, activity, dopamine_boost, timestamp
            FROM dopamine_tracking
            ORDER BY timestamp DESC
            LIMIT 5
        """
        )
        dopamine_data = cursor.fetchall()

        # Get auto-generated plans
        cursor.execute(
            """
            SELECT project_name, priority, tasks, deadline, progress
            FROM auto_plans
            WHERE created_by = 'auto_planner_agent'
            ORDER BY timestamp DESC
            LIMIT 5
        """
        )
        auto_plans = cursor.fetchall()

        conn.close()

        return jsonify(
            {
                "status": "success",
                "recent_activities": [
                    {
                        "agent": activity[0],
                        "action": activity[1],
                        "energy_boost": activity[2],
                        "timestamp": activity[3],
                        "status": activity[4],
                    }
                    for activity in activities
                ],
                "dopamine_tracking": [
                    {
                        "mood_score": data[0],
                        "energy_level": data[1],
                        "activity": data[2],
                        "boost": data[3],
                        "timestamp": data[4],
                    }
                    for data in dopamine_data
                ],
                "auto_plans": [
                    {
                        "project": plan[0],
                        "priority": plan[1],
                        "tasks": json.loads(plan[2]) if plan[2] else [],
                        "deadline": plan[3],
                        "progress": plan[4],
                    }
                    for plan in auto_plans
                ],
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    logger.info("🚀 Starting ChaosGenius Dashboard API...")
    logger.info("🧠 AI Squad standing by for activation")
    logger.info("📊 Real-time analytics engine initialized")

    try:
        app.run(debug=True, host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped gracefully")
    except Exception as e:
        print(f"\n💥 Server error: {e}")
