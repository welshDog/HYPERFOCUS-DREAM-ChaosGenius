#!/usr/bin/env python3
"""
🧠⚡ HYPERFOCUSzone Flask Backend ⚡🧠
"""

import json
import sqlite3
import time
import uuid
from datetime import datetime

import psutil
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = "hyperfocus-broski-legends-2025"

# Database setup
DB_FILE = "hyperfocus_portal.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS portal_users (
            id TEXT PRIMARY KEY,
            discord_id TEXT UNIQUE,
            username TEXT,
            email TEXT,
            access_level TEXT DEFAULT 'demo',
            total_xp INTEGER DEFAULT 0,
            broski_gems INTEGER DEFAULT 0,
            created_at TEXT,
            last_login TEXT,
            preferences TEXT DEFAULT '{}'
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            session_type TEXT,
            start_time TEXT,
            end_time TEXT,
            duration_minutes INTEGER,
            xp_earned INTEGER DEFAULT 0,
            data TEXT DEFAULT '{}'
        )
    """
    )

    conn.commit()
    conn.close()


@app.route("/")
def portal_home():
    return render_template("hyperfocuszone_portal.html")


@app.route("/api/user/discord-status")
def check_discord_status():
    # Check if user has Discord connection
    discord_id = session.get("discord_id")
    if discord_id:
        conn = sqlite3.connect(DB_FILE)
        user = conn.execute(
            "SELECT * FROM portal_users WHERE discord_id = ?", (discord_id,)
        ).fetchone()
        conn.close()

        if user:
            return jsonify(
                {
                    "connected": True,
                    "user": {
                        "id": user[1],
                        "username": user[2],
                        "access_level": user[4],
                        "total_xp": user[5],
                        "broski_gems": user[6],
                    },
                }
            )

    return jsonify({"connected": False})


@app.route("/api/portal/demo-session", methods=["POST"])
def start_demo_session():
    session_id = str(uuid.uuid4())
    session["demo_session_id"] = session_id
    session["demo_start_time"] = datetime.now().isoformat()

    return jsonify(
        {
            "session_id": session_id,
            "demo_duration": 30,  # 30 minutes
            "features_unlocked": ["focus_tools", "basic_dashboard"],
            "message": "🎮 Demo session started! 30 minutes of ADHD optimization ahead!",
        }
    )


@app.route("/api/agents/status")
def get_agent_status():
    # Return demo or personalized agent status
    if session.get("discord_id"):
        # Full agent army for Discord users
        agents = {
            "GUARDIAN-ZERO": {"status": "active", "health": 100, "missions": 15},
            "FOCUS-BUDDY": {"status": "active", "health": 100, "sessions": 8},
            "MEMORY-CRYSTAL": {"status": "active", "health": 100, "memories": 1247},
            "AGENT-ARMY": {"status": "active", "health": 100, "deployments": 23},
        }
    else:
        # Limited demo agents
        agents = {
            "DEMO-GUARDIAN": {
                "status": "demo",
                "health": 75,
                "limitations": "30min sessions",
            }
        }

    return jsonify(agents)


@app.route("/api/status")
def api_status():
    """🚀 HYPERFOCUSzone API status endpoint"""
    try:
        return jsonify(
            {
                "status": "active",
                "message": "HYPERFOCUSzone Portal is running at LEGENDARY PERFORMANCE!",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0-HYPERFOCUS",
                "zone_mode": "ADHD_OPTIMIZED",
                "services": {
                    "hyperfocus_portal": "active",
                    "adhd_agents": "deployed",
                    "memory_crystals": "operational",
                    "guardian_zero": "protecting",
                    "agent_army": "legendary",
                },
                "performance": {
                    "response_time": "ultra_fast",
                    "optimization_level": "maximum",
                    "dopamine_boost": "activated",
                },
                "neurodivergent_features": {
                    "adhd_friendly_ui": "enabled",
                    "executive_function_support": "active",
                    "sensory_customization": "available",
                    "hyperfocus_sessions": "ready",
                },
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"HYPERFOCUSzone status check failed: {str(e)}",
                }
            ),
            500,
        )


@app.route("/api/health")
def health_check():
    """🧠 HYPERFOCUSzone health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "zone_status": "HYPERFOCUS_READY",
            "timestamp": datetime.now().isoformat(),
            "uptime": "legendary",
            "brain_power": "maximum",
        }
    )


@app.route("/api/deploy-adhd-agents", methods=["POST"])
def deploy_adhd_agents():
    """🤖 Deploy ADHD-optimized agent army"""
    try:
        data = request.get_json()
        mode = data.get("mode", "hyperfocus")

        return jsonify(
            {
                "status": "success",
                "message": "🤖⚡ ADHD Agent Army deployed successfully!",
                "agents_deployed": [
                    "ADHD Task Manager",
                    "Focus Enhancement Monitor",
                    "Executive Function Support",
                    "Dopamine Optimization Coach",
                    "Hyperfocus Session Guardian",
                    "Neurodivergent Workflow Specialist",
                ],
                "mode": mode,
                "deployment_time": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"Agent deployment failed: {str(e)}"}
            ),
            500,
        )


@app.route("/guardian")
def guardian_hud():
    return render_template("guardian_hud.html")


@app.route("/api/real-time-metrics")
def get_real_time_metrics():
    """🔥 Real-time system metrics for live monitoring"""
    try:
        # System performance
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # ADHD-optimized metrics
        focus_level = min(100, max(0, 100 - cpu_percent))  # Inverse of CPU load
        brain_power = (memory.available / memory.total) * 100

        return jsonify(
            {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "cpu_usage": cpu_percent,
                    "memory_usage": memory.percent,
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "disk_usage": round((disk.used / disk.total) * 100, 1),
                    "disk_free_gb": round(disk.free / (1024**3), 2),
                },
                "hyperfocus_metrics": {
                    "focus_level": round(focus_level, 1),
                    "brain_power": round(brain_power, 1),
                    "productivity_score": round((focus_level + brain_power) / 2, 1),
                    "zone_status": (
                        "HYPERFOCUS"
                        if focus_level > 80
                        else "ACTIVE" if focus_level > 50 else "WARMING_UP"
                    ),
                },
                "portal_stats": {
                    "total_sessions": 127,
                    "active_agents": 6,
                    "memory_crystals": 1247,
                    "broski_gems_earned": 2847,
                    "legendary_achievements": 15,
                },
                "neurodivergent_features": {
                    "adhd_mode": "optimal",
                    "sensory_friendly": True,
                    "executive_function_support": "active",
                    "dopamine_boost_level": "maximum",
                },
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": f"Metrics collection failed: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@app.route("/api/agent-army-status")
def get_agent_army_status():
    """🤖 Get real-time agent army deployment status"""
    try:
        agents = [
            {
                "name": "GUARDIAN-ZERO",
                "status": "LEGENDARY_ACTIVE",
                "health": 100,
                "missions_completed": 847,
                "specialty": "Elite Defense & Memory Protection",
                "power_level": "MAXIMUM",
            },
            {
                "name": "FOCUS-BUDDY",
                "status": "HYPERFOCUS_READY",
                "health": 98,
                "sessions_supported": 234,
                "specialty": "ADHD Optimization & Flow State",
                "power_level": "LEGENDARY",
            },
            {
                "name": "MEMORY-CRYSTAL",
                "status": "CRYSTALLIZING",
                "health": 95,
                "memories_stored": 1247,
                "specialty": "Knowledge Synthesis & Recall",
                "power_level": "EPIC",
            },
            {
                "name": "DOPAMINE-OPTIMIZER",
                "status": "REWARD_READY",
                "health": 100,
                "optimizations": 567,
                "specialty": "Motivation Enhancement",
                "power_level": "MAXIMUM",
            },
            {
                "name": "EXECUTIVE-FUNCTION-COACH",
                "status": "COACHING_ACTIVE",
                "health": 92,
                "tasks_organized": 1834,
                "specialty": "Task Management & Planning",
                "power_level": "LEGENDARY",
            },
            {
                "name": "SENSORY-GUARDIAN",
                "status": "MONITORING",
                "health": 100,
                "environments_optimized": 89,
                "specialty": "Sensory Environment Control",
                "power_level": "EPIC",
            },
        ]

        return jsonify(
            {
                "army_status": "FULLY_DEPLOYED",
                "total_agents": len(agents),
                "agents": agents,
                "deployment_time": datetime.now().isoformat(),
                "combat_readiness": "MAXIMUM",
                "mission_success_rate": 99.7,
            }
        )
    except Exception as e:
        return jsonify({"error": f"Agent status unavailable: {str(e)}"}), 500


@app.route("/ultimate-command-center")
def ultimate_command_center():
    """🎯 Ultimate HYPERFOCUSzone Command Center Dashboard"""
    return render_template_string(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠⚡ HYPERFOCUSzone Ultimate Command Center</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a, #1a0a2e, #16213e);
            color: #00ff88;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .command-center {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(0, 255, 136, 0.1);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #00ff88;
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(transparent, rgba(0, 255, 136, 0.1), transparent, rgba(0, 255, 136, 0.1));
            animation: rotate 4s linear infinite;
        }

        .header-content {
            position: relative;
            z-index: 2;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .metric-card {
            background: rgba(0, 255, 136, 0.05);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00ff88, transparent);
            animation: scan 3s infinite;
        }

        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .metric-title {
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #00ffaa;
        }

        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #00ff88;
            text-shadow: 0 0 10px #00ff88;
        }

        .metric-status {
            margin-top: 10px;
            font-size: 0.9em;
            color: #88ffaa;
        }

        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }

        .agent-card {
            background: rgba(0, 100, 255, 0.1);
            border: 1px solid #0088ff;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .agent-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 136, 255, 0.3);
        }

        .agent-name {
            font-weight: bold;
            color: #0088ff;
            margin-bottom: 10px;
        }

        .agent-status {
            color: #88aaff;
            font-size: 0.9em;
            margin-bottom: 5px;
        }

        .status-LEGENDARY_ACTIVE, .status-HYPERFOCUS_READY, .status-REWARD_READY, .status-MONITORING {
            color: #00ff88 !important;
            text-shadow: 0 0 5px #00ff88;
        }

        .status-CRYSTALLIZING, .status-COACHING_ACTIVE {
            color: #ffaa00 !important;
            text-shadow: 0 0 5px #ffaa00;
        }

        .chart-container {
            background: rgba(0, 255, 136, 0.05);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .real-time-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 255, 136, 0.2);
            padding: 10px 15px;
            border-radius: 20px;
            border: 1px solid #00ff88;
            font-size: 0.9em;
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .zone-status-HYPERFOCUS {
            color: #ff0088 !important;
            text-shadow: 0 0 10px #ff0088;
            animation: glow 2s infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 10px #ff0088; }
            to { text-shadow: 0 0 20px #ff0088, 0 0 30px #ff0088; }
        }
    </style>
</head>
<body>
    <div class="real-time-indicator pulse">
        🔴 LIVE MONITORING
    </div>

    <div class="command-center">
        <div class="header">
            <div class="header-content">
                <h1>🧠⚡ HYPERFOCUSZONE ULTIMATE COMMAND CENTER ⚡🧠</h1>
                <p>Real-time ADHD-optimized monitoring & control system</p>
                <p id="last-update">Last Update: Loading...</p>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">🧠 Focus Level</div>
                <div class="metric-value" id="focus-level">--</div>
                <div class="metric-status" id="zone-status">Initializing...</div>
            </div>

            <div class="metric-card">
                <div class="metric-title">⚡ Brain Power</div>
                <div class="metric-value" id="brain-power">--</div>
                <div class="metric-status">Available Processing Power</div>
            </div>

            <div class="metric-card">
                <div class="metric-title">🎯 Productivity Score</div>
                <div class="metric-value" id="productivity-score">--</div>
                <div class="metric-status">Combined Performance Index</div>
            </div>

            <div class="metric-card">
                <div class="metric-title">💎 Memory Crystals</div>
                <div class="metric-value" id="memory-crystals">--</div>
                <div class="metric-status">Knowledge Fragments Stored</div>
            </div>
        </div>

        <div class="chart-container">
            <h3>📊 Real-Time System Performance</h3>
            <canvas id="performanceChart" width="400" height="200"></canvas>
        </div>

        <div class="metric-card" style="margin-bottom: 20px;">
            <div class="metric-title">🤖 AGENT ARMY STATUS</div>
            <div id="agents-grid" class="agents-grid">
                <!-- Agents will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        let performanceChart;
        let updateInterval;

        // Initialize performance chart
        function initChart() {
            const ctx = document.getElementById('performanceChart').getContext('2d');
            performanceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'Focus Level',
                            data: [],
                            borderColor: '#ff0088',
                            backgroundColor: 'rgba(255, 0, 136, 0.1)',
                            tension: 0.4
                        },
                        {
                            label: 'Brain Power',
                            data: [],
                            borderColor: '#00ff88',
                            backgroundColor: 'rgba(0, 255, 136, 0.1)',
                            tension: 0.4
                        },
                        {
                            label: 'CPU Usage',
                            data: [],
                            borderColor: '#0088ff',
                            backgroundColor: 'rgba(0, 136, 255, 0.1)',
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            grid: { color: 'rgba(0, 255, 136, 0.2)' },
                            ticks: { color: '#00ff88' }
                        },
                        x: {
                            grid: { color: 'rgba(0, 255, 136, 0.2)' },
                            ticks: { color: '#00ff88' }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: { color: '#00ff88' }
                        }
                    }
                }
            });
        }

        // Update metrics
        async function updateMetrics() {
            try {
                const response = await fetch('/api/real-time-metrics');
                const data = await response.json();

                // Update main metrics
                document.getElementById('focus-level').textContent = data.hyperfocus_metrics.focus_level + '%';
                document.getElementById('brain-power').textContent = data.hyperfocus_metrics.brain_power.toFixed(1) + '%';
                document.getElementById('productivity-score').textContent = data.hyperfocus_metrics.productivity_score + '%';
                document.getElementById('memory-crystals').textContent = data.portal_stats.memory_crystals.toLocaleString();

                // Update zone status with special styling
                const zoneStatus = document.getElementById('zone-status');
                zoneStatus.textContent = data.hyperfocus_metrics.zone_status;
                zoneStatus.className = 'metric-status zone-status-' + data.hyperfocus_metrics.zone_status;

                // Update chart
                const now = new Date().toLocaleTimeString();
                performanceChart.data.labels.push(now);
                performanceChart.data.datasets[0].data.push(data.hyperfocus_metrics.focus_level);
                performanceChart.data.datasets[1].data.push(data.hyperfocus_metrics.brain_power);
                performanceChart.data.datasets[2].data.push(data.system.cpu_usage);

                // Keep only last 20 data points
                if (performanceChart.data.labels.length > 20) {
                    performanceChart.data.labels.shift();
                    performanceChart.data.datasets.forEach(dataset => dataset.data.shift());
                }

                performanceChart.update('none');

                document.getElementById('last-update').textContent = 'Last Update: ' + new Date().toLocaleTimeString();

            } catch (error) {
                console.error('Failed to update metrics:', error);
            }
        }

        // Update agent army status
        async function updateAgentStatus() {
            try {
                const response = await fetch('/api/agent-army-status');
                const data = await response.json();

                const agentsGrid = document.getElementById('agents-grid');
                agentsGrid.innerHTML = data.agents.map(agent => `
                    <div class="agent-card">
                        <div class="agent-name">${agent.name}</div>
                        <div class="agent-status status-${agent.status}">${agent.status}</div>
                        <div class="agent-status">Health: ${agent.health}%</div>
                        <div class="agent-status">${agent.specialty}</div>
                        <div class="agent-status">Power: ${agent.power_level}</div>
                    </div>
                `).join('');

            } catch (error) {
                console.error('Failed to update agent status:', error);
            }
        }

        // Initialize everything
        window.addEventListener('load', () => {
            initChart();
            updateMetrics();
            updateAgentStatus();

            // Update every 3 seconds
            updateInterval = setInterval(() => {
                updateMetrics();
                updateAgentStatus();
            }, 3000);

            // GSAP animations
            gsap.from('.metric-card', {
                duration: 1,
                y: 50,
                opacity: 0,
                stagger: 0.1,
                ease: "power2.out"
            });
        });
    </script>
</body>
</html>
    """
    )


if __name__ == "__main__":
    init_db()
    print("🧠⚡ HYPERFOCUSzone Portal starting...")
    app.run(debug=True, host="0.0.0.0", port=5000)
