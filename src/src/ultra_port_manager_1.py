#!/usr/bin/env python3
"""
🚀💜 ULTRA PORT MANAGER - NEURODIVERGENT EXCELLENCE 💜🚀
Multi-Dashboard Port Management System for ChaosGenius
Run ALL dashboards simultaneously on different ports!
"""

import os
import subprocess
import sys
import threading
import time
from pathlib import Path


class UltraPortManager:
    """🎯 Manage multiple dashboard services on different ports"""

    def __init__(self):
        self.services = {
            "main_dashboard": {
                "port": 5000,
                "file": "dashboard_api.py",
                "name": "🎛️ Main ChaosGenius Dashboard",
                "process": None,
            },
            "memory_crystals": {
                "port": 5001,
                "file": "dashboard_api.py",
                "name": "💎 Memory Crystal Command Center",
                "process": None,
                "env_vars": {"MEMORY_CRYSTAL_MODE": "true"},
            },
            "etsy_dashboard": {
                "port": 5002,
                "file": "🎨 Frontend & UI/etsy_dashboard_api.py",
                "name": "🛍️ Etsy Shop Dashboard",
                "process": None,
            },
            "tiktok_dashboard": {
                "port": 5003,
                "file": "🎨 Frontend & UI/tiktok_dashboard_api.py",
                "name": "🎵 TikTok Shop Dashboard",
                "process": None,
            },
            "broski_ai": {
                "port": 5004,
                "file": "broski_ultra_server_armor.py",
                "name": "🧠 BROski AI Chat Hub",
                "process": None,
            },
            "hyperfocus_brain": {
                "port": 5005,
                "file": "hyperfocus_brain_command_center.py",
                "name": "⚡ HyperFocus Brain Command",
                "process": None,
            },
            "guardian_defense": {
                "port": 5006,
                "file": "broski_ultra_security_fortress.py",
                "name": "🛡️ Guardian Defense System",
                "process": None,
            },
            "analytics_hub": {
                "port": 5007,
                "file": "performance_control_center.py",
                "name": "📊 Ultra Analytics Hub",
                "process": None,
            },
        }

        self.running_services = {}

    def create_service_files(self):
        """Create individual service files for each port"""
        print("🔧 Creating individual service files...")

        # Create Etsy Dashboard API
        etsy_api = '''#!/usr/bin/env python3
"""🛍️ Etsy Dashboard API - Port 5002"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from dashboard_api import app

if __name__ == "__main__":
    print("🛍️ Starting Etsy Dashboard on port 5002...")
    app.run(debug=True, host="0.0.0.0", port=5002)
'''
        os.makedirs("🎨 Frontend & UI", exist_ok=True)
        with open("🎨 Frontend & UI/etsy_dashboard_api.py", "w") as f:
            f.write(etsy_api)

        # Create TikTok Dashboard API
        tiktok_api = '''#!/usr/bin/env python3
"""🎵 TikTok Dashboard API - Port 5003"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from dashboard_api import app

if __name__ == "__main__":
    print("🎵 Starting TikTok Dashboard on port 5003...")
    app.run(debug=True, host="0.0.0.0", port=5003)
'''
        with open("🎨 Frontend & UI/tiktok_dashboard_api.py", "w") as f:
            f.write(tiktok_api)

        print("✅ Service files created!")

    def start_service(self, service_name):
        """Start a specific service"""
        service = self.services.get(service_name)
        if not service:
            print(f"❌ Service {service_name} not found!")
            return False

        file_path = service["file"]
        port = service["port"]
        name = service["name"]

        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            return False

        print(f"🚀 Starting {name} on port {port}...")

        # Set up environment
        env = os.environ.copy()
        env["PORT"] = str(port)
        if "env_vars" in service:
            env.update(service["env_vars"])

        # Start the process
        try:
            if file_path.endswith(".py"):
                process = subprocess.Popen(
                    [sys.executable, file_path],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            else:
                print(f"⚠️ Unsupported file type: {file_path}")
                return False

            service["process"] = process
            self.running_services[service_name] = service

            print(f"✅ {name} started on port {port}")
            return True

        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return False

    def stop_service(self, service_name):
        """Stop a specific service"""
        if service_name not in self.running_services:
            print(f"⚠️ Service {service_name} not running")
            return

        service = self.running_services[service_name]
        process = service["process"]

        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
                print(f"🛑 Stopped {service['name']}")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"🔥 Force killed {service['name']}")

        del self.running_services[service_name]

    def start_all_services(self):
        """Start all dashboard services"""
        print("🚀💜 STARTING ULTRA MULTI-PORT DASHBOARD SYSTEM! 💜🚀")
        print("=" * 60)

        self.create_service_files()

        # Start services with delays to avoid conflicts
        service_order = [
            "main_dashboard",
            "memory_crystals",
            "broski_ai",
            "hyperfocus_brain",
            "guardian_defense",
            "analytics_hub",
            "etsy_dashboard",
            "tiktok_dashboard",
        ]

        for service_name in service_order:
            if service_name in self.services:
                self.start_service(service_name)
                time.sleep(2)  # Wait between starts

        time.sleep(5)  # Let everything initialize
        self.show_status()

    def stop_all_services(self):
        """Stop all running services"""
        print("🛑 Stopping all services...")

        for service_name in list(self.running_services.keys()):
            self.stop_service(service_name)

        print("✅ All services stopped!")

    def show_status(self):
        """Show status of all services"""
        print("\n🎯 ULTRA DASHBOARD NETWORK STATUS:")
        print("=" * 50)

        for name, service in self.services.items():
            port = service["port"]
            title = service["name"]

            if name in self.running_services:
                process = self.running_services[name]["process"]
                if process and process.poll() is None:
                    status = "🟢 RUNNING"
                    url = f"http://localhost:{port}"
                else:
                    status = "🔴 STOPPED"
                    url = "N/A"
            else:
                status = "⚪ NOT STARTED"
                url = "N/A"

            print(f"{status} {title}")
            if url != "N/A":
                print(f"    🌐 URL: {url}")
            print()

        print("🧠💜 NEURODIVERGENT EMPIRE: FULLY OPERATIONAL! 💜🧠")

    def restart_all(self):
        """Restart all services"""
        print("🔄 Restarting entire dashboard network...")
        self.stop_all_services()
        time.sleep(3)
        self.start_all_services()


if __name__ == "__main__":
    manager = UltraPortManager()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "start":
            manager.start_all_services()
        elif command == "stop":
            manager.stop_all_services()
        elif command == "restart":
            manager.restart_all()
        elif command == "status":
            manager.show_status()
        else:
            print("Usage: python ultra_port_manager.py [start|stop|restart|status]")
    else:
        # Interactive mode
        while True:
            print("\n🚀 ULTRA PORT MANAGER MENU:")
            print("1. 🚀 Start All Services")
            print("2. 🛑 Stop All Services")
            print("3. 🔄 Restart All Services")
            print("4. 📊 Show Status")
            print("5. 🚪 Exit")

            choice = input("\nSelect option (1-5): ").strip()

            if choice == "1":
                manager.start_all_services()
            elif choice == "2":
                manager.stop_all_services()
            elif choice == "3":
                manager.restart_all()
            elif choice == "4":
                manager.show_status()
            elif choice == "5":
                print("👋 Thanks for using Ultra Port Manager!")
                manager.stop_all_services()
                break
            else:
                print("❌ Invalid choice! Please select 1-5.")
