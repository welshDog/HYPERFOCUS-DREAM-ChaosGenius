#!/usr/bin/env python3
"""
🚀💜 CHAOSGENIUS PERFORMANCE OPTIMIZATION CONTROL CENTER 💜🚀
Real-time performance monitoring and optimization dashboard
"""

import gc
import json
import os
import sqlite3
import sys
import time
from datetime import datetime

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)


class PerformanceOptimizer:
    def __init__(self):
        self.optimization_history = []

    def run_quick_optimization(self):
        """Run a quick performance optimization cycle"""
        start_time = time.time()
        optimizations = []

        # Memory optimization
        initial_objects = len(gc.get_objects())
        collected = gc.collect()
        final_objects = len(gc.get_objects())

        optimizations.append(
            {
                "type": "memory",
                "objects_collected": collected,
                "objects_before": initial_objects,
                "objects_after": final_objects,
            }
        )

        # Database optimization
        db_files = [f for f in os.listdir(".") if f.endswith(".db")]
        db_optimized = 0

        for db_file in db_files[:3]:  # Quick optimization of first 3 DBs
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("PRAGMA optimize")
                conn.close()
                db_optimized += 1
            except:
                pass

        optimizations.append(
            {
                "type": "database",
                "databases_optimized": db_optimized,
                "total_databases": len(db_files),
            }
        )

        duration = time.time() - start_time

        result = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(duration, 2),
            "optimizations": optimizations,
            "status": "success",
        }

        self.optimization_history.append(result)
        return result

    def get_system_status(self):
        """Get current system performance status"""
        try:
            import psutil

            return {
                "memory_percent": psutil.virtual_memory().percent,
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "disk_percent": psutil.disk_usage("/").percent,
                "process_count": len(psutil.pids()),
            }
        except:
            return {
                "memory_percent": "N/A",
                "cpu_percent": "N/A",
                "disk_percent": "N/A",
                "process_count": "N/A",
            }


optimizer = PerformanceOptimizer()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🚀 ChaosGenius Performance Control Center</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; margin: 0; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .card {
            background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
            border-radius: 15px; padding: 20px; margin: 15px 0;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric { text-align: center; padding: 15px; }
        .metric-value { font-size: 2em; font-weight: bold; color: #00ff88; }
        .button {
            background: linear-gradient(45deg, #ff6b9d, #c44569);
            border: none; color: white; padding: 15px 30px;
            border-radius: 25px; font-size: 16px; cursor: pointer;
            margin: 10px; transition: all 0.3s;
        }
        .button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
        .log {
            background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;
            font-family: 'Courier New', monospace; font-size: 14px;
            max-height: 300px; overflow-y: auto;
        }
        .status-good { color: #00ff88; }
        .status-warning { color: #ffaa00; }
        .status-critical { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀💜 CHAOSGENIUS PERFORMANCE CONTROL CENTER 💜🚀</h1>
            <p>Real-time optimization and monitoring for neurodivergent excellence</p>
        </div>

        <div class="card">
            <h2>📊 System Performance Metrics</h2>
            <div class="metrics" id="metrics">
                <div class="metric">
                    <div>💾 Memory Usage</div>
                    <div class="metric-value" id="memory">Loading...</div>
                </div>
                <div class="metric">
                    <div>⚡ CPU Usage</div>
                    <div class="metric-value" id="cpu">Loading...</div>
                </div>
                <div class="metric">
                    <div>🗄️ Disk Usage</div>
                    <div class="metric-value" id="disk">Loading...</div>
                </div>
                <div class="metric">
                    <div>🔥 Processes</div>
                    <div class="metric-value" id="processes">Loading...</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🚀 Optimization Controls</h2>
            <div style="text-align: center;">
                <button class="button" onclick="runOptimization()">⚡ Quick Optimization</button>
                <button class="button" onclick="getStatus()">📊 Refresh Status</button>
                <button class="button" onclick="viewHistory()">📈 View History</button>
            </div>
        </div>

        <div class="card">
            <h2>📝 Optimization Log</h2>
            <div class="log" id="log">
                <div>🚀 ChaosGenius Performance Control Center Online!</div>
                <div>💜 Ready for neurodivergent optimization excellence!</div>
                <div>⚡ Click 'Quick Optimization' to boost performance!</div>
            </div>
        </div>

        <div class="card">
            <h2>🤖 Automated Scheduler Status</h2>
            <div id="scheduler-status">
                <p>✅ BROski Optimization Scheduler: <span class="status-good">ACTIVE</span></p>
                <p>⏰ Next optimization: Every 3 hours (ADHD-friendly timing)</p>
                <p>🧠 Smart optimization: Won't interrupt hyperfocus sessions</p>
                <p>📊 Background monitoring: Continuous performance tracking</p>
            </div>
        </div>
    </div>

    <script>
        function log(message, color = '#00ff88') {
            const logDiv = document.getElementById('log');
            const timestamp = new Date().toLocaleTimeString();
            logDiv.innerHTML += `<div style="color: ${color}">[${timestamp}] ${message}</div>`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        async function runOptimization() {
            log('🚀 Starting quick optimization...', '#ffaa00');
            try {
                const response = await fetch('/api/optimize', { method: 'POST' });
                const data = await response.json();

                if (data.status === 'success') {
                    log(`✅ Optimization complete in ${data.duration_seconds}s`, '#00ff88');
                    data.optimizations.forEach(opt => {
                        if (opt.type === 'memory') {
                            log(`🧠 Memory: ${opt.objects_collected} objects collected`, '#00ff88');
                        } else if (opt.type === 'database') {
                            log(`🗄️ Databases: ${opt.databases_optimized}/${opt.total_databases} optimized`, '#00ff88');
                        }
                    });
                    getStatus(); // Refresh metrics
                } else {
                    log('❌ Optimization failed', '#ff4444');
                }
            } catch (error) {
                log('❌ Connection error', '#ff4444');
            }
        }

        async function getStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();

                document.getElementById('memory').textContent = data.memory_percent + '%';
                document.getElementById('cpu').textContent = data.cpu_percent + '%';
                document.getElementById('disk').textContent = data.disk_percent + '%';
                document.getElementById('processes').textContent = data.process_count;

                // Color coding for metrics
                const memoryEl = document.getElementById('memory');
                if (parseFloat(data.memory_percent) > 80) {
                    memoryEl.className = 'metric-value status-critical';
                } else if (parseFloat(data.memory_percent) > 60) {
                    memoryEl.className = 'metric-value status-warning';
                } else {
                    memoryEl.className = 'metric-value status-good';
                }

                log('📊 Status refreshed', '#00ff88');
            } catch (error) {
                log('❌ Status update failed', '#ff4444');
            }
        }

        async function viewHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();

                log(`📈 Last ${data.length} optimizations:`, '#ffaa00');
                data.slice(-5).forEach(opt => {
                    const time = new Date(opt.timestamp).toLocaleTimeString();
                    log(`  [${time}] Duration: ${opt.duration_seconds}s`, '#dddddd');
                });
            } catch (error) {
                log('❌ History fetch failed', '#ff4444');
            }
        }

        // Auto-refresh status every 30 seconds
        setInterval(getStatus, 30000);

        // Initial status load
        getStatus();

        log('🎯 Performance Control Center ready!', '#ff6b9d');
    </script>
</body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/optimize", methods=["POST"])
def optimize():
    return jsonify(optimizer.run_quick_optimization())


@app.route("/api/status")
def status():
    return jsonify(optimizer.get_system_status())


@app.route("/api/history")
def history():
    return jsonify(optimizer.optimization_history)


if __name__ == "__main__":
    print("🚀💜 ChaosGenius Performance Control Center Starting...")
    print("🌐 Dashboard will be available at: http://localhost:5003")
    print("⚡ Real-time optimization controls activated!")
    app.run(host="0.0.0.0", port=5003, debug=False)
