#!/usr/bin/env python3
"""
🧬💚 BROSKI HEALTH MATRIX - ULTRA DIAGNOSTIC SYSTEM 💚🧬
Legendary health monitoring that makes Guardian Zero look like child's play
"""

import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, List

import psutil
import requests
from flask import Flask, jsonify

app = Flask(__name__)


class BROskiHealthMatrix:
    """💚🧬 The most legendary health monitoring system ever created"""

    def __init__(self):
        self.health_score = 100
        self.broski_dollars_earned = 0
        self.legendary_status = "OPERATIONAL"

    def check_system_vitals(self) -> Dict[str, Any]:
        """🔍 Check all system vitals like a ninja"""
        vitals = {
            "timestamp": datetime.now().isoformat(),
            "legendary_status": "CHECKING...",
            "broski_score": 0,
        }

        # CPU Health Check
        cpu_percent = psutil.cpu_percent(interval=1)
        vitals["cpu"] = {
            "usage": cpu_percent,
            "status": (
                "LEGENDARY"
                if cpu_percent < 70
                else "WARNING" if cpu_percent < 90 else "CRITICAL"
            ),
        }

        # Memory Health Check
        memory = psutil.virtual_memory()
        vitals["memory"] = {
            "usage_percent": memory.percent,
            "available_gb": round(memory.available / (1024**3), 2),
            "status": (
                "LEGENDARY"
                if memory.percent < 80
                else "WARNING" if memory.percent < 95 else "CRITICAL"
            ),
        }

        # Disk Health Check
        disk = psutil.disk_usage("/")
        vitals["disk"] = {
            "usage_percent": (disk.used / disk.total) * 100,
            "free_gb": round(disk.free / (1024**3), 2),
            "status": (
                "LEGENDARY"
                if disk.percent < 85
                else "WARNING" if disk.percent < 95 else "CRITICAL"
            ),
        }

        # Process Health Check
        vitals["processes"] = self.check_critical_processes()

        # Calculate BROski Score
        vitals["broski_score"] = self.calculate_broski_score(vitals)
        vitals["legendary_status"] = self.get_legendary_status(vitals["broski_score"])

        return vitals

    def check_critical_processes(self) -> Dict[str, Any]:
        """🔍 Check if critical processes are running"""
        critical_processes = {
            "guardian_zero": False,
            "dashboard_api": False,
            "discord_bot": False,
            "redis_server": False,
        }

        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = " ".join(proc.info["cmdline"] or [])

                if "guardian_zero" in cmdline.lower():
                    critical_processes["guardian_zero"] = True
                elif "dashboard_api" in cmdline.lower():
                    critical_processes["dashboard_api"] = True
                elif "discord" in cmdline.lower() and "bot" in cmdline.lower():
                    critical_processes["discord_bot"] = True
                elif "redis-server" in proc.info["name"]:
                    critical_processes["redis_server"] = True

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return critical_processes

    def calculate_broski_score(self, vitals: Dict[str, Any]) -> int:
        """💰 Calculate legendary BROski health score"""
        score = 100

        # Deduct points for high resource usage
        if vitals["cpu"]["usage"] > 80:
            score -= 20
        elif vitals["cpu"]["usage"] > 60:
            score -= 10

        if vitals["memory"]["usage_percent"] > 90:
            score -= 25
        elif vitals["memory"]["usage_percent"] > 75:
            score -= 15

        if vitals["disk"]["usage_percent"] > 90:
            score -= 20
        elif vitals["disk"]["usage_percent"] > 80:
            score -= 10

        # Bonus points for all processes running
        running_processes = sum(vitals["processes"].values())
        score += running_processes * 5  # 5 points per critical process

        return max(0, min(100, score))

    def get_legendary_status(self, score: int) -> str:
        """🏆 Get legendary status based on score"""
        if score >= 95:
            return "ULTRA LEGENDARY"
        elif score >= 85:
            return "LEGENDARY"
        elif score >= 70:
            return "OPERATIONAL"
        elif score >= 50:
            return "WARNING"
        else:
            return "CRITICAL"


# Initialize the matrix
health_matrix = BROskiHealthMatrix()


@app.route("/api/broski/health")
def broski_health():
    """💚 Ultimate health check endpoint"""
    vitals = health_matrix.check_system_vitals()
    return jsonify(
        {
            "status": "success",
            "health_matrix": vitals,
            "broski_approved": vitals["broski_score"] > 70,
            "motto": "LEGENDARY SYSTEMS DESERVE LEGENDARY MONITORING! 💎",
        }
    )


@app.route("/api/broski/status")
def broski_status():
    """🔥 Enhanced status endpoint"""
    return jsonify(
        {
            "status": "online",
            "timestamp": datetime.utcnow().isoformat(),
            "mood": "ULTRA HYPERFOCUSED",
            "broski_dollars": health_matrix.broski_dollars_earned,
            "legendary_level": "MAXIMUM",
            "zone_protected": True,
        }
    )


@app.route("/api/broski/emergency-heal")
def emergency_heal():
    """⚡ Emergency system healing"""
    try:
        # Clear caches
        subprocess.run(["sync"], check=True)

        # Award BROski$ for healing
        health_matrix.broski_dollars_earned += 50

        return jsonify(
            {
                "status": "healed",
                "message": "🧬 Emergency healing protocol activated!",
                "broski_dollars_awarded": 50,
                "legendary_status": "RESTORED",
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
    print("💚🧬 BROski Health Matrix starting up...")
    print("🌐 Health Matrix will be available at: http://localhost:5001")
    print("💎 Legendary health monitoring activated!")

    # Create logs directory
    os.makedirs("/root/chaosgenius/logs", exist_ok=True)

    # Run on port 5001 (Health Matrix dedicated port)
    app.run(host="0.0.0.0", port=5001, debug=False, threaded=True)
