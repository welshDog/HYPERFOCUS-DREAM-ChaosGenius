#!/usr/bin/env python3
"""
🌐📊 CHAOSGENIUS IMMORTAL STATUS API 📊🌐
Real-time system status monitoring endpoint
"""

import json
import os
import subprocess
from datetime import datetime

import psutil
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)


def get_system_status():
    """Get comprehensive system status"""

    # System resources
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    # Check running services
    services_status = {}
    critical_services = [
        "dashboard_api.py",
        "immortal_guardian.py",
        "chaosgenius_discord_bot.py",
        "hboard_api.py",
    ]

    for service in critical_services:
        services_status[service] = "stopped"
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if service in " ".join(proc.info["cmdline"] or []):
                    services_status[service] = "running"
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    # Check database files
    db_files = [
        "chaosgenius.db",
        "broski_ultra_brain.db",
        "broski_learning_optimized.db",
    ]
    db_status = {}
    for db in db_files:
        db_status[db] = {
            "exists": os.path.exists(db),
            "size_mb": (
                round(os.path.getsize(db) / 1024 / 1024, 2) if os.path.exists(db) else 0
            ),
        }

    # Overall health score
    running_services = sum(
        1 for status in services_status.values() if status == "running"
    )
    total_services = len(services_status)
    health_score = (
        round((running_services / total_services) * 100, 1) if total_services > 0 else 0
    )

    return {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": round(memory.available / 1024**3, 2),
            "disk_percent": round((disk.used / disk.total) * 100, 1),
            "disk_free_gb": round(disk.free / 1024**3, 2),
        },
        "services": services_status,
        "databases": db_status,
        "health": {
            "score": health_score,
            "status": (
                "excellent"
                if health_score >= 80
                else "good" if health_score >= 60 else "needs_attention"
            ),
            "running_services": running_services,
            "total_services": total_services,
        },
        "immortal_features": {
            "auto_restart": (
                "active"
                if services_status.get("immortal_guardian.py") == "running"
                else "inactive"
            ),
            "health_monitoring": "active",
            "auto_recovery": (
                "active"
                if services_status.get("immortal_guardian.py") == "running"
                else "inactive"
            ),
        },
    }


@app.route("/api/immortal/status")
def api_status():
    """API endpoint for system status"""
    return jsonify(get_system_status())


@app.route("/immortal/dashboard")
def dashboard():
    """Web dashboard for system status"""
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🛡️ ChaosGenius Immortal Status</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                color: white;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header {
                text-align: center;
                margin-bottom: 30px;
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            .status-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .status-card {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .status-good { border-left: 5px solid #00ff88; }
            .status-warning { border-left: 5px solid #ffaa00; }
            .status-critical { border-left: 5px solid #ff4757; }
            .metric {
                display: flex;
                justify-content: space-between;
                margin: 10px 0;
                padding: 8px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .service-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .status-badge {
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
            }
            .running { background: #00ff88; color: #000; }
            .stopped { background: #ff4757; color: #fff; }
            .refresh-btn {
                background: linear-gradient(45deg, #00ff88, #00d4ff);
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                color: black;
                font-weight: bold;
                cursor: pointer;
                margin: 10px;
            }
            .immortal-badge {
                background: linear-gradient(45deg, #ff6b6b, #feca57);
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                color: black;
                display: inline-block;
                margin: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️🚀 ChaosGenius Immortal Status 🚀🛡️</h1>
                <p>Real-time system monitoring & auto-recovery status</p>
                <div class="immortal-badge">IMMORTAL MODE ACTIVE</div>
                <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Status</button>
            </div>

            <div id="status-content">
                <div class="status-card">
                    <h3>📊 Loading system status...</h3>
                    <p>Please wait while we fetch the latest data...</p>
                </div>
            </div>
        </div>

        <script>
            async function loadStatus() {
                try {
                    const response = await fetch('/api/immortal/status');
                    const data = await response.json();
                    updateDashboard(data);
                } catch (error) {
                    document.getElementById('status-content').innerHTML =
                        '<div class="status-card status-critical"><h3>❌ Error loading status</h3><p>' + error + '</p></div>';
                }
            }

            function updateDashboard(data) {
                const healthClass = data.health.score >= 80 ? 'status-good' :
                                  data.health.score >= 60 ? 'status-warning' : 'status-critical';

                let servicesHtml = '';
                for (const [service, status] of Object.entries(data.services)) {
                    const badgeClass = status === 'running' ? 'running' : 'stopped';
                    const emoji = status === 'running' ? '✅' : '🔴';
                    servicesHtml += `
                        <div class="service-item">
                            <span>${emoji} ${service}</span>
                            <span class="status-badge ${badgeClass}">${status.toUpperCase()}</span>
                        </div>
                    `;
                }

                document.getElementById('status-content').innerHTML = `
                    <div class="status-grid">
                        <div class="status-card ${healthClass}">
                            <h3>🎯 Overall Health</h3>
                            <div class="metric">
                                <span>Health Score:</span>
                                <span>${data.health.score}%</span>
                            </div>
                            <div class="metric">
                                <span>Status:</span>
                                <span>${data.health.status.toUpperCase()}</span>
                            </div>
                            <div class="metric">
                                <span>Services:</span>
                                <span>${data.health.running_services}/${data.health.total_services}</span>
                            </div>
                        </div>

                        <div class="status-card">
                            <h3>📊 System Resources</h3>
                            <div class="metric">
                                <span>CPU Usage:</span>
                                <span>${data.system.cpu_percent}%</span>
                            </div>
                            <div class="metric">
                                <span>Memory Usage:</span>
                                <span>${data.system.memory_percent}%</span>
                            </div>
                            <div class="metric">
                                <span>Disk Usage:</span>
                                <span>${data.system.disk_percent}%</span>
                            </div>
                            <div class="metric">
                                <span>Free Space:</span>
                                <span>${data.system.disk_free_gb}GB</span>
                            </div>
                        </div>

                        <div class="status-card">
                            <h3>🚀 Services Status</h3>
                            ${servicesHtml}
                        </div>

                        <div class="status-card">
                            <h3>🛡️ Immortal Features</h3>
                            <div class="metric">
                                <span>🔄 Auto-Restart:</span>
                                <span>${data.immortal_features.auto_restart.toUpperCase()}</span>
                            </div>
                            <div class="metric">
                                <span>📊 Health Monitor:</span>
                                <span>${data.immortal_features.health_monitoring.toUpperCase()}</span>
                            </div>
                            <div class="metric">
                                <span>🔧 Auto-Recovery:</span>
                                <span>${data.immortal_features.auto_recovery.toUpperCase()}</span>
                            </div>
                            <div class="metric">
                                <span>⏰ Last Update:</span>
                                <span>${new Date().toLocaleTimeString()}</span>
                            </div>
                        </div>
                    </div>
                `;
            }

            // Load status on page load
            loadStatus();

            // Auto-refresh every 10 seconds
            setInterval(loadStatus, 10000);
        </script>
    </body>
    </html>
    """
    return dashboard_html


if __name__ == "__main__":
    print("🌐 Starting Immortal Status API on http://localhost:6000")
    print("🎛️ Dashboard: http://localhost:6000/immortal/dashboard")
    print("📊 API: http://localhost:6000/api/immortal/status")
    app.run(host="0.0.0.0", port=6000, debug=False)
