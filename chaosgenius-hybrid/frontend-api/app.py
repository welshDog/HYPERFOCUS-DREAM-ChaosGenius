#!/usr/bin/env python3
"""
🧠💜 ChaosGenius Hybrid Frontend API - Public Dashboard
=====================================================
Lightweight Flask API for public hosting (Railway/Render)
Communicates with private agent army via secure endpoints
"""

import json
import logging
import os
from datetime import datetime

import requests
from flask import Flask, Response, jsonify, render_template_string, request
from flask_cors import CORS

# Configure minimal logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Create optimized Flask app
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# CORS for API access
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
AGENT_ARMY_URL = os.getenv("AGENT_ARMY_URL", "http://localhost:8080")
API_SECRET = os.getenv("API_SECRET", "broski-hybrid-secret-2025")


class HybridDashboard:
    """Hybrid dashboard controller"""

    def __init__(self):
        self.status = {
            "frontend": "active",
            "agents": "checking...",
            "last_check": datetime.now().isoformat(),
        }

    def check_agent_army(self):
        """Check if agent army is responding"""
        try:
            response = requests.get(
                f"{AGENT_ARMY_URL}/api/status",
                headers={"Authorization": f"Bearer {API_SECRET}"},
                timeout=5,
            )
            if response.status_code == 200:
                self.status["agents"] = "active"
                return response.json()
        except:
            self.status["agents"] = "offline"

        self.status["last_check"] = datetime.now().isoformat()
        return None


# Initialize dashboard
dashboard = HybridDashboard()

# Dashboard HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🧠💜 ChaosGenius Hybrid Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: white;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .status-indicator {
            display: inline-block; width: 10px; height: 10px;
            border-radius: 50%; margin-right: 10px;
        }
        .active { background: #4CAF50; }
        .offline { background: #f44336; }
        .checking { background: #ff9800; animation: pulse 1s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 30px; }
        .btn {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            border: none; padding: 10px 20px; border-radius: 25px;
            color: white; font-weight: bold; cursor: pointer;
            text-decoration: none; display: inline-block;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠💜 ChaosGenius Hybrid Empire</h1>

        <div class="card">
            <h2>🚀 System Status</h2>
            <div class="status-grid">
                <div>
                    <span class="status-indicator active"></span>
                    <strong>Frontend API:</strong> Active ({{ frontend_status }})
                </div>
                <div>
                    <span class="status-indicator {{ agent_class }}"></span>
                    <strong>Agent Army:</strong> {{ agent_status }}
                </div>
                <div>
                    <strong>Last Check:</strong> {{ last_check }}
                </div>
                <div>
                    <strong>Architecture:</strong> Hybrid Split Deployment
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🎯 Quick Actions</h2>
            <a href="/api/status" class="btn">📊 API Status</a>
            <a href="/api/agent-health" class="btn">🤖 Agent Health</a>
            <a href="/api/logs" class="btn">📝 System Logs</a>
        </div>

        <div class="card">
            <h2>🧠 Neurodivergent Empire Components</h2>
            <p><strong>🌐 Frontend (This):</strong> Public dashboard, API endpoints, status monitoring</p>
            <p><strong>🤖 Agent Army:</strong> Background services, file processing, security monitoring</p>
            <p><strong>💜 Communication:</strong> Secure API bridge between components</p>
        </div>
    </div>

    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
"""


# Routes
@app.route("/")
def index():
    """Main dashboard"""
    agent_data = dashboard.check_agent_army()
    agent_class = "active" if dashboard.status["agents"] == "active" else "offline"

    return render_template_string(
        DASHBOARD_HTML,
        frontend_status=dashboard.status["frontend"],
        agent_status=dashboard.status["agents"],
        agent_class=agent_class,
        last_check=dashboard.status["last_check"],
    )


@app.route("/api/status")
def api_status():
    """Frontend API status"""
    return jsonify(
        {
            "status": "success",
            "component": "frontend-api",
            "version": "hybrid-v1.0",
            "timestamp": datetime.now().isoformat(),
            "system": dashboard.status,
        }
    )


@app.route("/api/agent-health")
def agent_health():
    """Check agent army health"""
    agent_data = dashboard.check_agent_army()

    if agent_data:
        return jsonify(
            {"status": "success", "agent_army": agent_data, "communication": "active"}
        )
    else:
        return (
            jsonify(
                {
                    "status": "warning",
                    "message": "Agent army offline or unreachable",
                    "agent_url": AGENT_ARMY_URL,
                }
            ),
            503,
        )


@app.route("/api/logs")
def api_logs():
    """Simple log endpoint"""
    return jsonify(
        {
            "status": "success",
            "logs": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "level": "INFO",
                    "message": "Frontend API operational",
                },
                {
                    "timestamp": dashboard.status["last_check"],
                    "level": "INFO",
                    "message": f"Agent army status: {dashboard.status['agents']}",
                },
            ],
        }
    )


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == "__main__":
    print("🚀💜 ChaosGenius Hybrid Frontend API Starting...")
    print("🌐 This is the PUBLIC component - deploy to Railway/Render")
    print("🤖 Agent army should run separately on PythonAnywhere/VPS")
    print(f"💜 Dashboard: http://localhost:{os.getenv('PORT', 5000)}")

    app.run(
        debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)), threaded=True
    )
