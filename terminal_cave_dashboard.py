#!/usr/bin/env python3
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def cave_dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🕋 Terminal Ultra Cave Dashboard</title>
        <style>
            body {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #00ff00;
                font-family: 'Courier New', monospace;
                margin: 0;
                padding: 20px;
            }
            .container { max-width: 1000px; margin: 0 auto; }
            .cave-header { text-align: center; margin-bottom: 30px; }
            .system-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .system-card {
                background: rgba(0,255,0,0.1);
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
            }
            .status-online { color: #00ff00; }
            .status-warning { color: #ffff00; }
            .ascii-art { font-size: 10px; line-height: 1; }
        </style>
        <script>
            setInterval(() => {
                document.getElementById('timestamp').textContent = new Date().toLocaleString();
            }, 1000);
        </script>
    </head>
    <body>
        <div class="container">
            <div class="cave-header">
                <h1>🌀🕋 TERMINAL ULTRA CAVE DASHBOARD 🕋🌀</h1>
                <p>CHAOSGENIUS ULTRA PHASE II: GALAXY MODE</p>
                <p>⏰ <span id="timestamp">{{ timestamp }}</span></p>
            </div>

            <div class="system-grid">
                <div class="system-card">
                    <h3>🧬 Health Matrix</h3>
                    <p class="status-online">✅ IMMORTAL STATUS</p>
                    <p>Port: 5001</p>
                </div>

                <div class="system-card">
                    <h3>⚡ Immortal Guardian</h3>
                    <p class="status-online">✅ PROTECTING</p>
                    <p>Auto-Resurrection: Active</p>
                </div>

                <div class="system-card">
                    <h3>🤖 Agent Army</h3>
                    <p class="status-online">✅ READY FOR DEPLOY</p>
                    <p>Agents: 5 Active</p>
                </div>

                <div class="system-card">
                    <h3>🛡️ Security Fortress</h3>
                    <p class="status-online">✅ FORTRESS MODE</p>
                    <p>Protection: Maximum</p>
                </div>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <h3>🎯 CURRENT MISSION</h3>
                <p style="color: #ff69b4; font-size: 18px;">{{ mission }}</p>
            </div>
        </div>
    </body>
    </html>
    """, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        mission="🚀 Terminal Ultra Cave is BLAZING with power!")

if __name__ == '__main__':
    print("🌐 Starting Terminal Ultra Cave Dashboard...")
    app.run(host='127.0.0.1', port=5003, debug=False)
