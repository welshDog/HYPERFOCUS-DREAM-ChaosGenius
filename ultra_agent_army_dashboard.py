#!/usr/bin/env python3
"""
🖥️💪♾️ ULTRA AGENT ARMY DASHBOARD - SUPREME COMMAND CENTER ♾️💪🖥️
Real-time monitoring and control interface for your agent army!
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
import json
from datetime import datetime, timedelta
import time
import threading
import asyncio
from ultra_agent_army_command_nexus import UltraAgentArmyCommander

app = Flask(__name__)
app.secret_key = "ULTRA_AGENT_ARMY_SUPREME_KEY_2025"

# Global army commander instance
army_commander = None

@app.route('/')
def dashboard():
    """🏠 Main Dashboard"""
    return render_template('ultra_agent_army_dashboard.html')

@app.route('/api/army-status')
def get_army_status():
    """📊 Get Real-time Army Status"""
    if not army_commander:
        return jsonify({"error": "Army not deployed"}), 503

    status = army_commander.get_army_status()

    # Add system metrics
    status.update({
        "system_time": datetime.now().isoformat(),
        "uptime": time.time() - (army_commander.deploy_time if hasattr(army_commander, 'deploy_time') else time.time()),
        "cpu_usage": get_system_cpu(),
        "memory_usage": get_system_memory()
    })

    return jsonify(status)

@app.route('/api/agents')
def get_agents():
    """🤖 Get All Agents"""
    if not army_commander:
        return jsonify([])

    agents = []
    for agent_id, agent in army_commander.active_agents.items():
        agent_data = {
            **agent,
            "performance": army_commander.performance_metrics.get(agent_id, {}),
            "health_status": "HEALTHY" if agent["status"] == "ACTIVE" else agent["status"]
        }
        agents.append(agent_data)

    return jsonify(agents)

@app.route('/api/missions')
def get_missions():
    """📋 Get Mission History"""
    conn = sqlite3.connect('/root/chaosgenius/ultra_agent_army.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM mission_control
        ORDER BY start_time DESC
        LIMIT 100
    """)

    missions = []
    for row in cursor.fetchall():
        missions.append({
            "mission_id": row[0],
            "mission_type": row[1],
            "priority": row[2],
            "assigned_agent": row[3],
            "status": row[4],
            "start_time": row[5],
            "completion_time": row[6],
            "success": bool(row[7]),
            "revenue_impact": row[8],
            "performance_score": row[9]
        })

    conn.close()
    return jsonify(missions)

@app.route('/api/metrics')
def get_metrics():
    """📈 Get Performance Metrics"""
    conn = sqlite3.connect('/root/chaosgenius/ultra_agent_army.db')
    cursor = conn.cursor()

    # Get recent metrics
    cursor.execute("""
        SELECT metric_name, metric_value, timestamp
        FROM army_metrics
        WHERE timestamp > datetime('now', '-24 hours')
        ORDER BY timestamp DESC
    """)

    metrics = {}
    for row in cursor.fetchall():
        metric_name = row[0]
        if metric_name not in metrics:
            metrics[metric_name] = []

        metrics[metric_name].append({
            "value": row[1],
            "timestamp": row[2]
        })

    conn.close()
    return jsonify(metrics)

@app.route('/api/deploy-agent', methods=['POST'])
def deploy_new_agent():
    """🚀 Deploy New Agent"""
    if not army_commander:
        return jsonify({"error": "Army commander not initialized"}), 503

    data = request.json
    agent_config = {
        "name": data.get("name", "Custom Agent"),
        "type": data.get("type", "general"),
        "specialization": data.get("specialization", "multi_purpose"),
        "power_level": int(data.get("power_level", 100))
    }

    # Deploy agent asynchronously
    async def deploy():
        await army_commander.deploy_agent(agent_config)

    # Run in thread to avoid blocking
    threading.Thread(target=lambda: asyncio.run(deploy())).start()

    return jsonify({"success": True, "message": f"Deploying {agent_config['name']}"})

@app.route('/api/emergency-shutdown', methods=['POST'])
def emergency_shutdown():
    """🛑 Emergency Army Shutdown"""
    if army_commander:
        army_commander.army_status = "SHUTDOWN"
        return jsonify({"success": True, "message": "Emergency shutdown initiated"})

    return jsonify({"error": "No army to shutdown"}), 404

@app.route('/api/chaos-mode', methods=['POST'])
def toggle_chaos_mode():
    """😈 Toggle Chaos Mode"""
    from ultra_agent_army_command_nexus import AGENT_ARMY_CONFIG

    AGENT_ARMY_CONFIG["chaos_mode"] = not AGENT_ARMY_CONFIG["chaos_mode"]

    return jsonify({
        "success": True,
        "chaos_mode": AGENT_ARMY_CONFIG["chaos_mode"],
        "message": "CHAOS MODE ACTIVATED! 😈" if AGENT_ARMY_CONFIG["chaos_mode"] else "Chaos mode deactivated"
    })

def get_system_cpu():
    """💻 Get System CPU Usage"""
    try:
        import psutil
        return psutil.cpu_percent(interval=1)
    except:
        return 0

def get_system_memory():
    """🧠 Get System Memory Usage"""
    try:
        import psutil
        return psutil.virtual_memory().percent
    except:
        return 0

def run_army_in_background():
    """🔄 Run Army Commander in Background"""
    global army_commander

    async def start_army():
        global army_commander
        army_commander = UltraAgentArmyCommander()
        army_commander.deploy_time = time.time()
        await army_commander.deploy_agent_army()

    asyncio.run(start_army())

if __name__ == '__main__':
    print("🚀 Starting Ultra Agent Army Dashboard...")

    # Start army in background thread
    army_thread = threading.Thread(target=run_army_in_background, daemon=True)
    army_thread.start()

    # Give army time to initialize
    time.sleep(2)

    print("🖥️ Dashboard running at http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)