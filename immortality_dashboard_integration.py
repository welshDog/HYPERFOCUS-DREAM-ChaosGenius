#!/usr/bin/env python3
"""
🛡️ IMMORTALITY PROTOCOL DASHBOARD INTEGRATION 🛡️
================================================
Real-time immortality monitoring for the ChaosGenius Dashboard
"""

import asyncio
import json
import threading
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template, request

from immortality_protocol_core import ImmortalityProtocol

# Create blueprint for immortality dashboard
immortality_bp = Blueprint("immortality", __name__, url_prefix="/immortality")

# Global immortality instance
immortality_protocol = None
immortality_thread = None


def start_immortality_background():
    """Start immortality protocol in background thread"""
    global immortality_protocol
    immortality_protocol = ImmortalityProtocol()
    immortality_protocol.quantum_redundancy_active = True

    # Start immortality loop in separate thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(immortality_protocol.immortality_main_loop())


@immortality_bp.route("/")
def immortality_dashboard():
    """🛡️ Main immortality dashboard"""
    return render_template("immortality_dashboard.html")


@immortality_bp.route("/api/status")
def get_immortality_status():
    """Get real-time immortality status"""
    global immortality_protocol

    if not immortality_protocol:
        return jsonify(
            {"error": "Immortality Protocol not active", "status": "OFFLINE"}
        )

    status = immortality_protocol.get_immortality_status()
    return jsonify(status)


@immortality_bp.route("/api/services")
def get_service_status():
    """Get detailed service status"""
    global immortality_protocol

    if not immortality_protocol:
        return jsonify({"services": {}})

    services = {}
    for service_name in immortality_protocol.critical_services:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        status = loop.run_until_complete(
            immortality_protocol.quantum_health_check(service_name)
        )
        services[service_name] = {
            "name": status.name,
            "status": status.status,
            "uptime_percentage": status.uptime_percentage,
            "cpu_usage": status.cpu_usage,
            "memory_usage": status.memory_usage,
            "error_count": status.error_count,
            "restart_count": status.restart_count,
            "last_check": status.last_check.isoformat(),
        }

    return jsonify({"services": services})


@immortality_bp.route("/api/metrics/history")
def get_metrics_history():
    """Get historical system metrics"""
    global immortality_protocol

    if not immortality_protocol:
        return jsonify({"metrics": []})

    try:
        import sqlite3

        conn = sqlite3.connect(immortality_protocol.db_path)
        cursor = conn.cursor()

        # Get last 24 hours of metrics
        cursor.execute(
            """
            SELECT timestamp, total_cpu_usage, total_memory_usage, disk_usage
            FROM system_metrics
            WHERE timestamp > datetime('now', '-24 hours')
            ORDER BY timestamp DESC
            LIMIT 100
        """
        )

        metrics = []
        for row in cursor.fetchall():
            metrics.append(
                {
                    "timestamp": row[0],
                    "cpu_usage": row[1],
                    "memory_usage": row[2],
                    "disk_usage": row[3],
                }
            )

        conn.close()
        return jsonify({"metrics": metrics})

    except Exception as e:
        return jsonify({"error": str(e)})


@immortality_bp.route("/api/incidents")
def get_recent_incidents():
    """Get recent incidents"""
    global immortality_protocol

    if not immortality_protocol:
        return jsonify({"incidents": []})

    try:
        import sqlite3

        conn = sqlite3.connect(immortality_protocol.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, service_name, incident_type, severity, description
            FROM incidents
            WHERE timestamp > datetime('now', '-24 hours')
            ORDER BY timestamp DESC
            LIMIT 50
        """
        )

        incidents = []
        for row in cursor.fetchall():
            incidents.append(
                {
                    "timestamp": row[0],
                    "service_name": row[1],
                    "incident_type": row[2],
                    "severity": row[3],
                    "description": row[4],
                }
            )

        conn.close()
        return jsonify({"incidents": incidents})

    except Exception as e:
        return jsonify({"error": str(e)})


@immortality_bp.route("/api/healing_actions")
def get_healing_actions():
    """Get recent self-healing actions"""
    global immortality_protocol

    if not immortality_protocol:
        return jsonify({"actions": []})

    try:
        import sqlite3

        conn = sqlite3.connect(immortality_protocol.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, service_name, action_type, success, details
            FROM self_healing_actions
            WHERE timestamp > datetime('now', '-24 hours')
            ORDER BY timestamp DESC
            LIMIT 50
        """
        )

        actions = []
        for row in cursor.fetchall():
            actions.append(
                {
                    "timestamp": row[0],
                    "service_name": row[1],
                    "action_type": row[2],
                    "success": bool(row[3]),
                    "details": row[4],
                }
            )

        conn.close()
        return jsonify({"actions": actions})

    except Exception as e:
        return jsonify({"error": str(e)})


@immortality_bp.route("/api/control/restart_service", methods=["POST"])
def restart_service():
    """Manually restart a service"""
    global immortality_protocol

    if not immortality_protocol:
        return jsonify({"error": "Immortality Protocol not active"})

    data = request.get_json()
    service_name = data.get("service_name")

    if not service_name:
        return jsonify({"error": "Service name required"})

    try:
        # Trigger resurrection protocol
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            immortality_protocol.resurrection_protocol(service_name)
        )

        return jsonify(
            {"success": True, "message": f"Restart initiated for {service_name}"}
        )

    except Exception as e:
        return jsonify({"error": str(e)})


@immortality_bp.route("/api/control/emergency_stop", methods=["POST"])
def emergency_stop():
    """Emergency stop immortality protocol"""
    global immortality_protocol

    if immortality_protocol:
        immortality_protocol.stop_immortality_protocol()
        return jsonify({"success": True, "message": "Immortality Protocol stopped"})

    return jsonify({"error": "Protocol not running"})


def init_immortality_integration(app):
    """Initialize immortality protocol integration with Flask app"""
    global immortality_thread

    # Register blueprint
    app.register_blueprint(immortality_bp)

    # Start immortality protocol in background
    immortality_thread = threading.Thread(
        target=start_immortality_background, daemon=True
    )
    immortality_thread.start()

    print("🛡️ IMMORTALITY PROTOCOL INTEGRATION ACTIVATED!")
    return immortality_bp
