#!/usr/bin/env python3
"""
🕶️💥 HYPER STEALTH MONITOR: GHOST MODE ACTIVATED 💥🕶️
Ultra-Ninja Discord Bot Monitor with Secret Paths & Command Injection
By the CHAOS WARRIORS - BROski∞ Stealth Edition
"""

import base64
import io
import os
import random
import string
import subprocess
import time
from datetime import datetime

import psutil
import qrcode
from flask import Flask, jsonify, redirect, render_template_string, request

app = Flask(__name__)

# 🔥 STEALTH CONFIGURATION
BOT_PID_FILE = "/root/chaosgenius/discord_bot.pid"
LOG_FILE = "/root/chaosgenius/discord_bot.log"
LAUNCHER_SCRIPT = "/root/chaosgenius/hyperbuild_discord_launcher.sh"
START_TIME = time.time()

# 🧬 SECRET PATHS - RANDOMLY GENERATED
SECRET_PATHS = {
    "main": f"/🧠{''.join(random.choices(string.ascii_lowercase, k=6))}🔒",
    "command": f"/ninja{''.join(random.choices(string.ascii_lowercase, k=4))}",
    "mobile": f"/qr{''.join(random.choices(string.ascii_lowercase, k=5))}",
    "api": f"/api{''.join(random.choices(string.ascii_lowercase, k=4))}",
}


def get_bot_status():
    """🛡️ Get comprehensive bot status"""
    status_data = {
        "status": "OFFLINE",
        "pid": None,
        "memory": 0,
        "cpu": 0,
        "uptime": 0,
        "log_count": 0,
        "restart_count": 0,
    }

    if os.path.isfile(BOT_PID_FILE):
        try:
            with open(BOT_PID_FILE) as f:
                pid = int(f.read().strip())

            if psutil.pid_exists(pid):
                status_data["status"] = "ONLINE"
                status_data["pid"] = pid

                p = psutil.Process(pid)
                status_data["memory"] = round(p.memory_info().rss / (1024 * 1024), 2)
                status_data["cpu"] = round(p.cpu_percent(interval=0.1), 2)

                # Calculate uptime
                create_time = p.create_time()
                status_data["uptime"] = int(time.time() - create_time)

        except (ValueError, psutil.NoSuchProcess):
            pass

    # Get log stats
    if os.path.isfile(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()
                status_data["log_count"] = len(lines)
                status_data["restart_count"] = sum(
                    1 for line in lines if "restart" in line.lower()
                )
        except:
            pass

    return status_data


def get_recent_logs(count=8):
    """📝 Get recent log entries"""
    logs = []
    if os.path.isfile(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()[-count:]
                for line in lines:
                    # Add timestamp and format
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    logs.append(f"[{timestamp}] {line.strip()}")
        except:
            logs = ["[ERROR] Could not read logs"]
    else:
        logs = ["[SYSTEM] No logs available"]
    return logs


def generate_qr_code(url):
    """📱 Generate QR code for mobile access"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="lime", back_color="black")

    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"


@app.route("/")
def redirect_to_secret():
    """🚪 Redirect main page to secret stealth monitor"""
    return redirect(SECRET_PATHS["main"])


@app.route(SECRET_PATHS["main"])
def stealth_monitor():
    """🕶️ Main stealth monitoring dashboard"""
    status = get_bot_status()
    logs = get_recent_logs()

    # Generate mobile QR code
    mobile_url = f"http://{request.host}{SECRET_PATHS['mobile']}"
    qr_code = generate_qr_code(mobile_url)

    return render_template_string(
        """
<!DOCTYPE html>
<html>
<head>
    <title>[:: STEALTH MONITOR ACTIVE ::]</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: #000;
            color: #0f0;
            font-family: 'Courier New', monospace;
            padding: 20px;
            margin: 0;
            line-height: 1.4;
        }
        .header {
            color: #0ff;
            text-align: center;
            border-bottom: 2px solid #0ff;
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-shadow: 0 0 10px #0ff;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .status-card {
            background: #111;
            border: 1px solid #0f0;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(0,255,0,0.3);
        }
        .status-online { border-color: #0f0; color: #0f0; }
        .status-offline { border-color: #f00; color: #f00; }
        .log-container {
            background: #111;
            border: 2px solid #0f0;
            padding: 15px;
            border-radius: 5px;
            max-height: 300px;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(0,255,0,0.4);
        }
        .log-entry {
            margin: 5px 0;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 5px #0f0; }
            to { text-shadow: 0 0 15px #0f0, 0 0 25px #0f0; }
        }
        .command-section {
            margin-top: 20px;
            padding: 15px;
            background: #222;
            border: 1px solid #ff0;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(255,255,0,0.3);
        }
        .ninja-button {
            background: linear-gradient(45deg, #0f0, #0ff);
            color: #000;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .ninja-button:hover {
            background: linear-gradient(45deg, #ff0, #f0f);
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255,255,0,0.8);
        }
        .qr-section {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            background: #333;
            border-radius: 5px;
        }
        .secret-info {
            color: #ff0;
            font-size: 12px;
            text-align: center;
            margin-top: 20px;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        .uptime-bar {
            width: 100%;
            height: 10px;
            background: #333;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 5px;
        }
        .uptime-fill {
            height: 100%;
            background: linear-gradient(90deg, #0f0, #0ff);
            animation: flow 2s linear infinite;
        }
        @keyframes flow {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
    </style>
    <script>
        function executeCommand(action) {
            fetch('{{command_path}}', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: action})
            })
            .then(response => response.json())
            .then(data => {
                alert('🔥 ' + data.message);
                setTimeout(() => location.reload(), 2000);
            })
            .catch(error => alert('❌ Error: ' + error));
        }

        // Auto-refresh every 10 seconds
        setInterval(() => location.reload(), 10000);

        // Matrix-style background effect
        function createMatrixEffect() {
            const chars = '01';
            const container = document.body;
            for(let i = 0; i < 50; i++) {
                const span = document.createElement('span');
                span.textContent = chars[Math.floor(Math.random() * chars.length)];
                span.style.position = 'fixed';
                span.style.top = Math.random() * 100 + '%';
                span.style.left = Math.random() * 100 + '%';
                span.style.color = 'rgba(0,255,0,0.1)';
                span.style.fontSize = '10px';
                span.style.zIndex = '-1';
                span.style.animation = `float ${3 + Math.random() * 3}s linear infinite`;
                container.appendChild(span);
            }
        }

        window.onload = createMatrixEffect;
    </script>
</head>
<body>
    <div class="header">
        <h1>[:: 🕶️ BROski∞ STEALTH MONITOR 🕶️ ::]</h1>
        <p>💥 GHOST MODE ACTIVATED 💥</p>
    </div>

    <div class="status-grid">
        <div class="status-card status-{{status_class}}">
            <h3>🤖 BOT STATUS</h3>
            <p><strong>{{status.status}}</strong></p>
            <p>PID: {{status.pid}}</p>
            <div class="uptime-bar">
                <div class="uptime-fill" style="width: {{uptime_percent}}%"></div>
            </div>
        </div>

        <div class="status-card">
            <h3>💾 RESOURCES</h3>
            <p>Memory: <strong>{{status.memory}}MB</strong></p>
            <p>CPU: <strong>{{status.cpu}}%</strong></p>
            <p>Uptime: <strong>{{uptime_display}}</strong></p>
        </div>

        <div class="status-card">
            <h3>📊 STATS</h3>
            <p>Log Entries: <strong>{{status.log_count}}</strong></p>
            <p>Restarts: <strong>{{status.restart_count}}</strong></p>
            <p>Ghost Level: <strong>💀 MAXIMUM</strong></p>
        </div>
    </div>

    <div class="log-container">
        <h3>📝 LIVE NEURAL FEED:</h3>
        {% for log in logs %}
        <div class="log-entry">{{log}}</div>
        {% endfor %}
    </div>

    <div class="command-section">
        <h3>🥷 NINJA COMMAND CENTER:</h3>
        <button class="ninja-button" onclick="executeCommand('status')">🛡️ STATUS CHECK</button>
        <button class="ninja-button" onclick="executeCommand('restart')">🔄 RESTART BOT</button>
        <button class="ninja-button" onclick="executeCommand('logs')">📝 CLEAR LOGS</button>
        <button class="ninja-button" onclick="executeCommand('immortal')">💀 IMMORTAL MODE</button>
    </div>

    <div class="qr-section">
        <h3>📱 MOBILE GHOST ACCESS:</h3>
        <img src="{{qr_code}}" alt="QR Code" style="max-width: 200px;">
        <p>Scan for stealth mobile monitoring</p>
    </div>

    <div class="secret-info">
        🔒 SECRET PATHS ACTIVE | 🧬 GHOST PROTOCOLS ENGAGED | 💥 ULTRA MODE ENABLED
        <br>
        Command Injection: {{command_path}} | Mobile Access: {{mobile_path}}
    </div>
</body>
</html>
    """,
        status=status,
        status_class="online" if status["status"] == "ONLINE" else "offline",
        uptime_percent=min(100, (status["uptime"] / 3600) * 10),  # Scale for visual
        uptime_display=f"{status['uptime']//3600}h {(status['uptime']%3600)//60}m",
        logs=logs,
        qr_code=qr_code,
        command_path=SECRET_PATHS["command"],
        mobile_path=SECRET_PATHS["mobile"],
    )


@app.route(SECRET_PATHS["command"], methods=["POST"])
def ninja_command():
    """🥷 Execute ninja commands remotely"""
    try:
        data = request.get_json()
        action = data.get("action", "")

        if action == "restart":
            subprocess.Popen([LAUNCHER_SCRIPT, "restart"])
            return jsonify(
                {"status": "success", "message": "Bot restart initiated! 🔄"}
            )

        elif action == "status":
            status = get_bot_status()
            return jsonify(
                {"status": "success", "message": f'Bot is {status["status"]} 🛡️'}
            )

        elif action == "logs":
            # Clear logs
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w") as f:
                    f.write(f"[{datetime.now()}] Logs cleared via stealth monitor\n")
            return jsonify({"status": "success", "message": "Logs cleared! 📝"})

        elif action == "immortal":
            subprocess.Popen([LAUNCHER_SCRIPT, "immortal"])
            return jsonify(
                {"status": "success", "message": "Immortal mode activated! 💀"}
            )

        else:
            return jsonify({"status": "error", "message": "Unknown command"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Command failed: {str(e)}"})


@app.route(SECRET_PATHS["mobile"])
def mobile_monitor():
    """📱 Mobile-optimized stealth monitor"""
    status = get_bot_status()
    logs = get_recent_logs(5)

    return render_template_string(
        """
<!DOCTYPE html>
<html>
<head>
    <title>🕶️ Mobile Ghost Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: #000;
            color: #0f0;
            font-family: monospace;
            padding: 10px;
            margin: 0;
            font-size: 14px;
        }
        .header { color: #0ff; text-align: center; margin-bottom: 15px; }
        .status {
            background: #111;
            border: 1px solid #0f0;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .logs {
            background: #111;
            border: 1px solid #0f0;
            padding: 10px;
            max-height: 200px;
            overflow-y: auto;
            font-size: 12px;
        }
        .status-{{status_class}} { border-color: {{'#0f0' if status.status == 'ONLINE' else '#f00'}}; }
    </style>
    <script>
        setInterval(() => location.reload(), 15000);
    </script>
</head>
<body>
    <div class="header">
        <h2>🕶️ GHOST MONITOR</h2>
        <p>💥 Mobile Stealth Mode</p>
    </div>

    <div class="status status-{{status_class}}">
        <strong>🤖 {{status.status}}</strong><br>
        💾 {{status.memory}}MB | 🔁 {{status.cpu}}%<br>
        ⏱️ {{uptime_display}} | 📝 {{status.log_count}} logs
    </div>

    <div class="logs">
        <strong>📡 NEURAL FEED:</strong><br>
        {% for log in logs %}
        {{log}}<br>
        {% endfor %}
    </div>

    <div style="text-align: center; margin-top: 15px; color: #ff0; font-size: 10px;">
        🔒 STEALTH ACTIVE | Auto-refresh: 15s
    </div>
</body>
</html>
    """,
        status=status,
        status_class="online" if status["status"] == "ONLINE" else "offline",
        uptime_display=f"{status['uptime']//3600}h {(status['uptime']%3600)//60}m",
        logs=logs,
    )


@app.route(SECRET_PATHS["api"])
def api_status():
    """🔌 API endpoint for external monitoring"""
    status = get_bot_status()
    return jsonify(
        {
            "ghost_mode": True,
            "timestamp": datetime.now().isoformat(),
            "bot_status": status,
            "secret_paths": list(SECRET_PATHS.keys()),
            "stealth_level": "MAXIMUM",
        }
    )


if __name__ == "__main__":
    print("🕶️💥 STEALTH MONITOR: GHOST MODE ACTIVATED 💥🕶️")
    print(f"🔒 Secret Main Path: {SECRET_PATHS['main']}")
    print(f"🥷 Command Injection: {SECRET_PATHS['command']}")
    print(f"📱 Mobile Access: {SECRET_PATHS['mobile']}")
    print(f"🔌 API Endpoint: {SECRET_PATHS['api']}")
    print("💀 WARRIORS READY - ULTRA STEALTH ENGAGED!")

    app.run(host="0.0.0.0", port=5001, debug=False)
