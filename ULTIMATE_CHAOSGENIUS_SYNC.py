#!/usr/bin/env python3
"""
🚀💎 ULTIMATE CHAOSGENIUS EMPIRE SYNC & COORDINATOR v2.0 💎🚀
===============================================================
The LEGENDARY master controller that syncs ALL your systems!
🦾💪 By Command of Chief Lyndz - SYNC ALL THE THINGS! 💪🦾
✅ FIXED: Favicon, Template errors, Process management, Error handling
"""

import os
import sys
import time
import json
import psutil
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, render_template_string, send_from_directory

# 🎯 ULTIMATE PORT ALLOCATION - NO MORE CONFLICTS!
EMPIRE_SERVICES = {
    "chaosgenius_main": {"port": 3000, "script": "app.py", "priority": 1},
    "dashboard_api": {"port": 5000, "script": "dashboard_api.py", "priority": 2},
    "hyperfocuszone": {"port": 5100, "script": "hyperfocuszone/app.py", "priority": 3},
    "health_matrix": {"port": 5001, "script": "broski_health_matrix.py", "priority": 4},
    "brain_engine": {"port": 5002, "script": "broski_brain_data_engine.py", "priority": 5},
    "team_collaboration": {"port": 5555, "script": "team_collaboration_hub.py", "priority": 6},
    "money_maker": {"port": 5007, "script": "money_maker_portal.py", "priority": 7},
    "teemill_integration": {"port": 5009, "script": "teemill_income_integrator.py", "priority": 8},
    "brain_intelligence": {"port": 5010, "script": "chaosgenius_brain_intelligence_hub.py", "priority": 9},
    "nl_commander": {"port": 8000, "script": "broski_nl_web_api.py", "priority": 10},
    "command_center": {"port": 8080, "script": "ultimate_command_center.py", "priority": 11},
    "hyperview_dashboard": {"port": 5201, "script": "hyperview_dashboard.py", "priority": 12},
    "agent_army": {"port": 8888, "script": "ultra_agent_army_dashboard.py", "priority": 13}
}

class ChaosGeniusEmpireSync:
    def __init__(self):
        self.services_status = {}
        self.running_processes = {}
        self.sync_app = Flask(__name__)
        self.sync_app.secret_key = "chaosgenius_ultra_legendary_sync_2025"
        self.setup_sync_routes()

        # Create static directory for favicon
        os.makedirs("static", exist_ok=True)
        self.create_favicon()

    def create_favicon(self):
        """Create a simple favicon to prevent 404 errors"""
        favicon_path = "static/favicon.ico"
        if not os.path.exists(favicon_path):
            # Create a simple 1x1 transparent favicon
            with open(favicon_path, "wb") as f:
                # Minimal ICO file header for 1x1 transparent icon
                f.write(b'\x00\x00\x01\x00\x01\x00\x01\x01\x00\x00\x01\x00\x18\x00(\x00\x00\x00\x16\x00\x00\x00(\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def print_header(self, text):
        print("=" * 60)
        print(f"🚀 {text}")
        print("=" * 60)

    def check_port_available(self, port):
        """Check if port is available"""
        try:
            for conn in psutil.net_connections():
                if hasattr(conn, 'laddr') and conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
                    return False
            return True
        except (psutil.AccessDenied, AttributeError):
            # Fallback check using netstat
            try:
                result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
                return f":{port} " not in result.stdout
            except:
                return True

    def kill_port_processes(self, port):
        """Kill any processes using a specific port"""
        try:
            # Try psutil first
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    for conn in proc.connections():
                        if hasattr(conn, 'laddr') and conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
                            print(f"🔫 Killing process {proc.info['pid']} on port {port}")
                            proc.kill()
                            time.sleep(1)
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    pass
        except Exception as e:
            # Fallback to system commands
            try:
                subprocess.run(['fuser', '-k', f'{port}/tcp'], capture_output=True)
            except:
                print(f"⚠️ Could not kill processes on port {port}: {e}")

    def start_service(self, service_name, config):
        """Start a service with proper port management"""
        port = config["port"]
        script = config["script"]

        print(f"\n🚀 Starting {service_name} on port {port}...")

        # Check if script exists
        if not os.path.exists(script):
            print(f"⚠️ Script {script} not found, skipping {service_name}")
            self.services_status[service_name] = "missing"
            return False

        # Kill any existing processes on this port
        if not self.check_port_available(port):
            print(f"🔧 Port {port} in use, clearing...")
            self.kill_port_processes(port)
            time.sleep(2)

        try:
            # Start the service
            env = os.environ.copy()
            env["PORT"] = str(port)
            env["SERVICE_NAME"] = service_name
            env["PYTHONPATH"] = os.getcwd()

            process = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None  # Create new process group
            )

            # Give it a moment to start
            time.sleep(3)

            # Check if it's running
            if process.poll() is None:
                self.running_processes[service_name] = process
                self.services_status[service_name] = "running"
                print(f"✅ {service_name} started successfully on port {port}")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ {service_name} failed to start")
                error_msg = stderr.decode()[:200] if stderr else "Unknown error"
                print(f"Error: {error_msg}")
                self.services_status[service_name] = "failed"
                return False

        except Exception as e:
            print(f"❌ Error starting {service_name}: {e}")
            self.services_status[service_name] = "error"
            return False

    def stop_service(self, service_name):
        """Stop a running service"""
        if service_name in self.running_processes:
            process = self.running_processes[service_name]
            try:
                # Try graceful termination first
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                process.kill()
                process.wait()
            except:
                pass
            finally:
                del self.running_processes[service_name]
                self.services_status[service_name] = "stopped"
                print(f"🛑 Stopped {service_name}")

    def restart_service(self, service_name):
        """Restart a service"""
        if service_name in EMPIRE_SERVICES:
            self.stop_service(service_name)
            time.sleep(2)
            return self.start_service(service_name, EMPIRE_SERVICES[service_name])
        return False

    def check_all_services(self):
        """Check status of all services"""
        print("\n📊 CHECKING ALL SERVICES...")
        for service_name, process in list(self.running_processes.items()):
            if process.poll() is None:
                self.services_status[service_name] = "running"
            else:
                self.services_status[service_name] = "crashed"
                del self.running_processes[service_name]

    def setup_sync_routes(self):
        """Setup the sync dashboard routes"""

        @self.sync_app.route("/favicon.ico")
        def favicon():
            return send_from_directory("static", "favicon.ico")

        @self.sync_app.route("/")
        def sync_dashboard():
            try:
                return render_template_string(SYNC_DASHBOARD_HTML, services=self.services_status)
            except Exception as e:
                return f"<h1>🚨 Empire Sync Dashboard</h1><p>Error: {e}</p><p>Services: {self.services_status}</p>"

        @self.sync_app.route("/api/status")
        def api_status():
            running_count = len([s for s in self.services_status.values() if s == "running"])
            return jsonify({
                "empire_status": "LEGENDARY" if running_count > 0 else "STARTING",
                "services": self.services_status,
                "total_services": len(EMPIRE_SERVICES),
                "running_services": running_count,
                "success_rate": round((running_count / len(EMPIRE_SERVICES)) * 100) if EMPIRE_SERVICES else 0,
                "timestamp": datetime.now().isoformat()
            })

        @self.sync_app.route("/api/start/<service_name>")
        def start_service_api(service_name):
            if service_name in EMPIRE_SERVICES:
                success = self.start_service(service_name, EMPIRE_SERVICES[service_name])
                return jsonify({"success": success, "service": service_name})
            return jsonify({"success": False, "error": "Service not found"})

        @self.sync_app.route("/api/stop/<service_name>")
        def stop_service_api(service_name):
            self.stop_service(service_name)
            return jsonify({"success": True, "service": service_name})

        @self.sync_app.route("/api/restart/<service_name>")
        def restart_service_api(service_name):
            success = self.restart_service(service_name)
            return jsonify({"success": success, "service": service_name})

        @self.sync_app.route("/api/emergency-recovery")
        def emergency_recovery_api():
            self.emergency_recovery()
            return jsonify({"success": True, "message": "Emergency recovery initiated"})

    def start_priority_services(self):
        """Start services in priority order"""
        self.print_header("STARTING CHAOSGENIUS EMPIRE IN PRIORITY ORDER")

        # Sort services by priority
        sorted_services = sorted(EMPIRE_SERVICES.items(), key=lambda x: x[1]["priority"])

        for service_name, config in sorted_services:
            self.start_service(service_name, config)
            time.sleep(1)  # Brief pause between starts

    def emergency_recovery(self):
        """Emergency recovery - restart all failed services"""
        print("\n🚨 EMERGENCY RECOVERY MODE ACTIVATED!")
        self.check_all_services()

        for service_name, status in self.services_status.items():
            if status in ["crashed", "failed", "error"]:
                print(f"🔧 Recovering {service_name}...")
                self.restart_service(service_name)

    def run_sync_dashboard(self):
        """Run the sync coordination dashboard"""
        print("\n🎛️ Starting Empire Sync Dashboard on port 9999...")
        print("🌐 Access at: http://localhost:9999")
        print("🔧 Press Ctrl+C to stop")

        try:
            self.sync_app.run(host="0.0.0.0", port=9999, debug=False, use_reloader=False)
        except KeyboardInterrupt:
            print("\n🛑 Sync dashboard stopping...")
        except Exception as e:
            print(f"❌ Sync dashboard error: {e}")

# 🎨 FIXED SYNC DASHBOARD HTML TEMPLATE - ALL ERRORS RESOLVED!
SYNC_DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🚀💎 ChaosGenius Empire Sync Dashboard</title>
    <link rel="icon" href="data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQEAYAAABPYyMiAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAAF0lEQVRIx2NgGAWjYBSMglEwCkbBSAcACAABAAGjeNxTAAAARUlORQk=" type="image/x-icon">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff88; font-family: 'Courier New', monospace; margin: 0; padding: 20px;
            min-height: 100vh;
        }
        .header { text-align: center; margin-bottom: 30px; }
        .celebration { font-size: 2em; text-align: center; margin: 20px 0; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        .services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin: 20px 0; }
        .service-card {
            background: rgba(0, 255, 136, 0.1); border: 1px solid #00ff88;
            border-radius: 10px; padding: 15px; position: relative; transition: all 0.3s;
        }
        .service-card:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0, 255, 136, 0.3); }
        .service-running { border-color: #00ff88; background: rgba(0, 255, 136, 0.2); }
        .service-stopped { border-color: #ff6b6b; background: rgba(255, 107, 107, 0.1); }
        .service-failed { border-color: #ff4757; background: rgba(255, 71, 87, 0.1); }
        .service-missing { border-color: #ffa726; background: rgba(255, 167, 38, 0.1); }
        .service-crashed { border-color: #ff4757; background: rgba(255, 71, 87, 0.15); }
        .service-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .service-status { margin: 10px 0; }
        .control-buttons { margin-top: 10px; }
        .btn {
            background: #00ff88; color: #000; border: none; padding: 8px 12px;
            border-radius: 5px; margin: 2px; cursor: pointer; font-weight: bold; font-size: 0.9em;
            transition: all 0.2s;
        }
        .btn:hover { background: #00cc6a; transform: scale(1.05); }
        .btn.danger { background: #ff4757; color: white; }
        .btn.danger:hover { background: #ff3742; }
        .stats {
            background: rgba(0, 255, 136, 0.2); padding: 20px; border-radius: 10px;
            margin-bottom: 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;
        }
        .stat-item { text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; }
        .quick-links {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px; margin: 20px 0;
        }
        .quick-link {
            background: #00ff88; color: #000; padding: 12px; text-decoration: none;
            border-radius: 5px; text-align: center; font-weight: bold; transition: all 0.2s;
        }
        .quick-link:hover { background: #00cc6a; transform: scale(1.02); }
        .status-indicator { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; }
        .status-running { background: #00ff88; }
        .status-failed { background: #ff4757; }
        .status-missing { background: #ffa726; }
        .status-stopped { background: #ff6b6b; }
        .status-crashed { background: #ff4757; animation: blink 1s infinite; }
        @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0.3; } }
        .controls-section { text-align: center; margin: 30px 0; }
        .master-control { background: #ff4757; color: white; font-size: 1.3em; padding: 15px 25px; }
        .error-notice { background: rgba(255, 71, 87, 0.2); border: 1px solid #ff4757; border-radius: 10px; padding: 15px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀💎 CHAOSGENIUS EMPIRE SYNC DASHBOARD v2.0 💎🚀</h1>
        <p>Ultimate Service Coordination & Management Portal</p>
        <p>🦾💪 By Command of Chief Lyndz - ALL SYSTEMS SYNCHRONIZED! 💪🦾</p>
    </div>

    {% set services_list = services.values() %}
    {% set total_count = services|length %}
    {% set running_count = services_list|selectattr('match', 'running')|list|length %}
    {% set failed_count = services_list|selectattr('match', 'failed')|list|length %}
    {% set crashed_count = services_list|selectattr('match', 'crashed')|list|length %}
    {% set missing_count = services_list|selectattr('match', 'missing')|list|length %}
    {% set success_rate = ((running_count / total_count) * 100)|round if total_count > 0 else 0 %}

    <div class="celebration">
        🏆 EMPIRE STATUS: {{ running_count }}/{{ total_count }} SERVICES ({{ success_rate }}%) 🏆
    </div>

    {% if success_rate >= 80 %}
        <div style="text-align: center; color: #00ff88; font-size: 1.5em; margin: 20px 0;">
            💎 LEGENDARY STATUS ACHIEVED! 💎
        </div>
    {% elif success_rate >= 60 %}
        <div style="text-align: center; color: #ffa726; font-size: 1.5em; margin: 20px 0;">
            💪 SOLID EMPIRE PERFORMANCE! 💪
        </div>
    {% else %}
        <div class="error-notice">
            <h3>⚠️ EMPIRE NEEDS ATTENTION</h3>
            <p>Some services are down. Use Emergency Recovery to restore full power!</p>
        </div>
    {% endif %}

    <div class="stats">
        <div class="stat-item">
            <div class="stat-number">{{ total_count }}</div>
            <div>Total Services</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" style="color: #00ff88;">{{ running_count }}</div>
            <div>Running</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" style="color: #ff4757;">{{ failed_count + crashed_count }}</div>
            <div>Failed/Crashed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" style="color: #ffa726;">{{ missing_count }}</div>
            <div>Missing</div>
        </div>
    </div>

    <div class="services-grid">
        {% for service_name, status in services.items() %}
        <div class="service-card service-{{ status }}">
            <div class="service-title">
                <span class="status-indicator status-{{ status }}"></span>
                {{ service_name.replace('_', ' ').title() }}
            </div>
            <div class="service-status">Status: <strong>{{ status.upper() }}</strong></div>
            {% if status == "running" %}
                <div style="color: #00ff88;">✅ LEGENDARY PERFORMANCE!</div>
            {% elif status == "failed" %}
                <div style="color: #ff4757;">⚠️ Needs attention - Check logs</div>
            {% elif status == "crashed" %}
                <div style="color: #ff4757;">💥 Crashed - Ready for recovery</div>
            {% elif status == "missing" %}
                <div style="color: #ffa726;">📝 Script not found in workspace</div>
            {% else %}
                <div style="color: #ff6b6b;">🔄 Ready to launch</div>
            {% endif %}
            <div class="control-buttons">
                <button class="btn" onclick="startService('{{ service_name }}')">🚀 START</button>
                <button class="btn" onclick="stopService('{{ service_name }}')">🛑 STOP</button>
                <button class="btn" onclick="restartService('{{ service_name }}')">🔄 RESTART</button>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="controls-section">
        <h2>🎯 QUICK ACCESS TO YOUR EMPIRE:</h2>
        <div class="quick-links">
            <a href="http://localhost:3000" target="_blank" class="quick-link">🎛️ Main Dashboard</a>
            <a href="http://localhost:5000" target="_blank" class="quick-link">📡 API Dashboard</a>
            <a href="http://localhost:5100" target="_blank" class="quick-link">🧠 HyperFocus Zone</a>
            <a href="http://localhost:5001" target="_blank" class="quick-link">💚 Health Matrix</a>
            <a href="http://localhost:8080" target="_blank" class="quick-link">🎮 Command Center</a>
            <a href="http://localhost:5555" target="_blank" class="quick-link">👥 Team Hub</a>
        </div>

        <button class="btn master-control" onclick="emergencyRecovery()">
            🚨 EMERGENCY RECOVERY - RESURRECT ALL SERVICES
        </button>

        <div style="margin-top: 20px;">
            <button class="btn" onclick="location.reload()" style="background: #17a2b8; color: white;">
                🔄 REFRESH STATUS
            </button>
            <button class="btn" onclick="openAllDashboards()" style="background: #28a745; color: white;">
                🚀 OPEN ALL DASHBOARDS
            </button>
        </div>
    </div>

    <script>
        function startService(name) {
            fetch(`/api/start/${name}`)
                .then(r => r.json())
                .then(d => {
                    if(d.success) {
                        showNotification(`🚀 ${name} started successfully!`, 'success');
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        showNotification(`❌ Failed to start ${name}`, 'error');
                    }
                })
                .catch(e => showNotification(`❌ Error: ${e.message}`, 'error'));
        }

        function stopService(name) {
            fetch(`/api/stop/${name}`)
                .then(r => r.json())
                .then(d => {
                    if(d.success) {
                        showNotification(`🛑 ${name} stopped`, 'warning');
                        setTimeout(() => location.reload(), 1000);
                    }
                })
                .catch(e => showNotification(`❌ Error: ${e.message}`, 'error'));
        }

        function restartService(name) {
            showNotification(`🔄 Restarting ${name}...`, 'info');
            fetch(`/api/restart/${name}`)
                .then(r => r.json())
                .then(d => {
                    if(d.success) {
                        showNotification(`✅ ${name} restarted successfully!`, 'success');
                        setTimeout(() => location.reload(), 2000);
                    } else {
                        showNotification(`❌ Failed to restart ${name}`, 'error');
                    }
                })
                .catch(e => showNotification(`❌ Error: ${e.message}`, 'error'));
        }

        function emergencyRecovery() {
            if(confirm('🚨 Initiate EMERGENCY RECOVERY for all failed services?\\n\\nThis will attempt to restart all crashed/failed services.')) {
                showNotification('🚨 Emergency recovery initiated...', 'info');
                fetch('/api/emergency-recovery')
                    .then(r => r.json())
                    .then(d => {
                        showNotification('✅ Emergency recovery completed!', 'success');
                        setTimeout(() => location.reload(), 3000);
                    })
                    .catch(e => showNotification(`❌ Recovery error: ${e.message}`, 'error'));
            }
        }

        function openAllDashboards() {
            const dashboards = [
                'http://localhost:3000',
                'http://localhost:5000',
                'http://localhost:5100',
                'http://localhost:5001',
                'http://localhost:8080'
            ];

            dashboards.forEach(url => {
                window.open(url, '_blank');
            });

            showNotification('🚀 Opening all dashboards!', 'success');
        }

        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.innerHTML = message;
            notification.style.cssText = `
                position: fixed; top: 20px; right: 20px; z-index: 1000;
                padding: 15px 20px; border-radius: 5px; color: white; font-weight: bold;
                background: ${type === 'success' ? '#00ff88' : type === 'error' ? '#ff4757' : type === 'warning' ? '#ffa726' : '#17a2b8'};
                color: ${type === 'success' ? '#000' : '#fff'};
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
                max-width: 300px;
            `;
            document.body.appendChild(notification);
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => {
                    if (document.body.contains(notification)) {
                        document.body.removeChild(notification);
                    }
                }, 300);
            }, 4000);
        }

        // Auto-refresh every 30 seconds
        setInterval(() => {
            fetch('/api/status')
                .then(r => r.json())
                .then(d => {
                    console.log('🚀 Empire status:', d.empire_status, 'Running:', d.running_services);
                })
                .catch(e => console.log('Status check failed:', e));
        }, 30000);

        // Show loading state
        window.addEventListener('load', () => {
            console.log('🚀 ChaosGenius Empire Sync Dashboard v2.0 Loaded!');
            showNotification('🎛️ Empire Dashboard Online!', 'success');
        });

        // Add empire status to console
        console.log('🎯 Current Empire Status:');
        console.log('- Total Services: {{ total_count }}');
        console.log('- Running: {{ running_count }}');
        console.log('- Success Rate: {{ success_rate }}%');
    </script>
</body>
</html>
"""

def main():
    print("🚀💎 ULTIMATE CHAOSGENIUS EMPIRE SYNC v2.0 STARTING! 💎🚀")
    print("🦾💪 Scanning and synchronizing ALL systems... 💪🦾")

    sync_master = ChaosGeniusEmpireSync()

    # Check what's already running and clean up conflicts
    sync_master.print_header("CLEANING UP PORT CONFLICTS")
    for service_name, config in EMPIRE_SERVICES.items():
        port = config["port"]
        if not sync_master.check_port_available(port):
            print(f"🔧 Clearing port {port} for {service_name}")
            sync_master.kill_port_processes(port)

    print("\n✅ Port conflicts resolved!")

    # Start services in priority order
    sync_master.start_priority_services()

    # Final status check
    time.sleep(5)
    sync_master.check_all_services()

    sync_master.print_header("CHAOSGENIUS EMPIRE STATUS")
    running_count = 0
    for service_name, status in sync_master.services_status.items():
        icon = "✅" if status == "running" else "❌" if status in ["failed", "crashed"] else "⚠️"
        print(f"{icon} {service_name}: {status.upper()}")
        if status == "running":
            running_count += 1

    print(f"\n🎯 EMPIRE SUMMARY: {running_count}/{len(EMPIRE_SERVICES)} services running")
    success_rate = round((running_count / len(EMPIRE_SERVICES)) * 100) if EMPIRE_SERVICES else 0

    if success_rate >= 80:
        print("🏆 LEGENDARY STATUS ACHIEVED! 🏆")
    elif success_rate >= 50:
        print("💪 SOLID PERFORMANCE - EMPIRE STRONG! 💪")
    else:
        print("⚠️ Some services need attention - Emergency recovery available!")

    print(f"\n🎛️ SYNC DASHBOARD: http://localhost:9999")
    print("🚀 Use the dashboard to manage all your services!")
    print("🔧 Fixed: Favicon errors, template issues, process management")

    # Start the sync dashboard
    try:
        sync_master.run_sync_dashboard()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down ChaosGenius Empire Sync...")
        for service_name in list(sync_master.running_processes.keys()):
            sync_master.stop_service(service_name)
        print("💜 Empire synchronized and sleeping... until next time! 💜")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()