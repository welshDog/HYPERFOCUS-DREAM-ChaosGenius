#!/usr/bin/env python3
"""
🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
    HYPERGATE WEB CONTROL PANEL v1.0
🌌 VISUAL COMMAND CENTER FOR CHIEF LYNDZ 🌌
👑 HYPERFOCUS EMPIRE REMOTE DASHBOARD 👑
"""

import json
import os
import sqlite3
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for

from hypergate_manager import HyperGateManager

app = Flask(__name__)
app.secret_key = "hypergate_ultra_secret_key_2025"

# Initialize HyperGate manager
hypergate = HyperGateManager()


@app.route("/")
def dashboard():
    """Main dashboard"""
    return render_template("dashboard.html")


@app.route("/api/status")
def api_status():
    """Get current connection status"""
    status = hypergate.get_status()
    stats = hypergate.get_connection_stats()

    return jsonify(
        {"status": status, "stats": stats, "timestamp": datetime.now().isoformat()}
    )


@app.route("/api/connect", methods=["POST"])
def api_connect():
    """Connect to HyperGate"""
    try:
        success = hypergate.connect()
        return jsonify(
            {
                "success": success,
                "message": "HyperGate connected!" if success else "Connection failed",
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route("/api/disconnect", methods=["POST"])
def api_disconnect():
    """Disconnect from HyperGate"""
    try:
        hypergate.disconnect()
        return jsonify({"success": True, "message": "HyperGate disconnected"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route("/api/test", methods=["POST"])
def api_test():
    """Test connection"""
    try:
        success, latency = hypergate.test_connection()
        return jsonify(
            {
                "success": success,
                "latency": latency,
                "message": f'Test {"passed" if success else "failed"}',
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route("/api/execute", methods=["POST"])
def api_execute():
    """Execute remote command"""
    try:
        command = request.json.get("command", "")
        if not command:
            return jsonify({"success": False, "message": "No command provided"}), 400

        success, output = hypergate.execute_remote_command(command)
        return jsonify({"success": success, "output": output, "command": command})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route("/api/logs")
def api_logs():
    """Get recent connection logs"""
    try:
        log_file = Path.home() / ".hypergate" / "connections.log"
        if not log_file.exists():
            return jsonify({"logs": []})

        # Read last 50 lines
        with open(log_file, "r") as f:
            lines = f.readlines()
            recent_logs = lines[-50:] if len(lines) > 50 else lines

        return jsonify({"logs": [line.strip() for line in recent_logs]})
    except Exception as e:
        return jsonify({"logs": [], "error": str(e)})


@app.route("/api/config")
def api_config():
    """Get configuration"""
    return jsonify(hypergate.config)


@app.route("/api/config", methods=["POST"])
def api_update_config():
    """Update configuration"""
    try:
        new_config = request.json
        hypergate.config.update(new_config)
        hypergate.save_config()

        return jsonify({"success": True, "message": "Configuration updated"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route("/api/history")
def api_history():
    """Get connection history"""
    try:
        conn = sqlite3.connect(hypergate.db_file)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, server_ip, username, duration, status, latency
            FROM connections
            ORDER BY timestamp DESC
            LIMIT 100
        """
        )

        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append(
                {
                    "timestamp": row[0],
                    "server_ip": row[1],
                    "username": row[2],
                    "duration": row[3],
                    "status": row[4],
                    "latency": row[5],
                }
            )

        return jsonify({"history": history})
    except Exception as e:
        return jsonify({"history": [], "error": str(e)})


if __name__ == "__main__":
    print("🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐")
    print("    HYPERGATE WEB CONTROL PANEL")
    print("🌌 Starting visual command center... 🌌")
    print("🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐")
    print()
    print("🌐 Access dashboard at: http://localhost:5000")
    print("🎮 Chief Lyndz, your HyperGate awaits!")

    app.run(host="0.0.0.0", port=5000, debug=True)
