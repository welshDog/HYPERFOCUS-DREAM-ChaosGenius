#!/usr/bin/env python3
"""
🌌💜 BROSKI MASTER PORTAL DIRECTORY 💜🌌
🌐 Complete Portal Network Management System 🌐
👑 By Command of Chief Lyndz - Ultimate Portal Command Center! 👑
"""

import json
import logging
import os
import sqlite3
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BroskiMasterPortalDirectory:
    """🌌 Ultimate Portal Network Management System"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.portal_db = f"{self.base_path}/broski_master_portals.db"
        self.monitoring_active = False
        self.portal_registry = {}
        self.portal_status = {}
        self._monitor_thread = None

        print("🌌💜 BROSKI MASTER PORTAL DIRECTORY ONLINE! 💜🌌")
        self._initialize_portal_database()
        self._discover_all_portals()
        self._initialize_portal_health_monitoring()

    def _initialize_portal_database(self):
        """🗄️ Initialize master portal database"""
        try:
            with sqlite3.connect(self.portal_db) as conn:
                cursor = conn.cursor()

                # Portal Registry Table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS portal_registry (
                        portal_id TEXT PRIMARY KEY,
                        portal_name TEXT,
                        portal_type TEXT,
                        portal_url TEXT,
                        file_path TEXT,
                        port INTEGER,
                        status TEXT DEFAULT 'UNKNOWN',
                        last_health_check REAL,
                        response_time REAL,
                        uptime_percentage REAL DEFAULT 0.0,
                        launch_command TEXT
                    )
                """
                )

                # Portal Health Log Table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS portal_health_log (
                        check_id TEXT PRIMARY KEY,
                        portal_id TEXT,
                        timestamp REAL,
                        status TEXT,
                        response_time REAL,
                        error_message TEXT,
                        cpu_usage REAL,
                        memory_usage REAL
                    )
                """
                )

                # Portal Network Map Table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS portal_network_map (
                        connection_id TEXT PRIMARY KEY,
                        source_portal TEXT,
                        target_portal TEXT,
                        connection_type TEXT,
                        data_flow TEXT,
                        last_sync REAL,
                        sync_status TEXT
                    )
                """
                )

                conn.commit()
                logger.info("🌌 Portal database initialized!")

        except sqlite3.Error as e:
            logger.error(f"Portal database error: {e}")

    def _discover_all_portals(self):
        """🔍 Discover all available portals in the system"""
        self.portal_registry = {
            # Web Portals
            "hyperportal": {
                "name": "🧠 BROski HyperPortal",
                "type": "WEB_INTERFACE",
                "url": "http://localhost:5173",
                "file_path": f"{self.base_path}/broski_hyperportal",
                "port": 5173,
                "description": "ADHD-optimized productivity portal",
                "launch_command": "cd broski_hyperportal && npm run dev",
                "status": "UNKNOWN",
            },
            "dashboard": {
                "name": "🎛️ ChaosGenius Dashboard",
                "type": "WEB_DASHBOARD",
                "url": "http://localhost:5000",
                "file_path": f"{self.base_path}/app.py",
                "port": 5000,
                "description": "Main control center dashboard",
                "launch_command": "python3 app.py",
                "status": "UNKNOWN",
            },
            # Security Portals
            "security_fortress": {
                "name": "🛡️ Security Fortress Portal",
                "type": "SECURITY_MONITORING",
                "url": "terminal://security_fortress",
                "file_path": f"{self.base_path}/broski_security_fortress_portal.py",
                "port": None,
                "description": "Advanced threat detection and monitoring",
                "launch_command": "python3 broski_security_fortress_portal.py",
                "status": "UNKNOWN",
            },
            # Financial Portals
            "money_maker": {
                "name": "💰 Money Maker Portal",
                "type": "FINANCIAL_TRACKER",
                "url": "terminal://money_maker",
                "file_path": f"{self.base_path}/broski_money_maker_portal.py",
                "port": None,
                "description": "Income generation and financial tracking",
                "launch_command": "python3 broski_money_maker_portal.py",
                "status": "UNKNOWN",
            },
            # Agent Management Portals
            "agent_command": {
                "name": "🤖 Agent Army Command",
                "type": "AGENT_MANAGEMENT",
                "url": "terminal://agent_command",
                "file_path": f"{self.base_path}/broski_agent_army_command_portal.py",
                "port": None,
                "description": "Direct agent command and control",
                "launch_command": "python3 broski_agent_army_command_portal.py",
                "status": "UNKNOWN",
            },
            # Neural Network Portals
            "neural_hyperlink": {
                "name": "🧠 Neural Hyperlink System",
                "type": "NEURAL_NETWORK",
                "url": "terminal://neural_hyperlink",
                "file_path": f"{self.base_path}/ULTRA_MODE_NEURAL_HYPERLINK_SYSTEM.py",
                "port": None,
                "description": "AI consciousness and neural processing",
                "launch_command": "python3 ULTRA_MODE_NEURAL_HYPERLINK_SYSTEM.py",
                "status": "UNKNOWN",
            },
            # Integration Portals
            "ultra_integration": {
                "name": "🚀 Ultra Integration Portal",
                "type": "SYSTEM_INTEGRATION",
                "url": "terminal://ultra_integration",
                "file_path": f"{self.base_path}/agent_army_ultra_integration.py",
                "port": None,
                "description": "Complete system integration hub",
                "launch_command": "python3 agent_army_ultra_integration.py",
                "status": "UNKNOWN",
            },
            # Discord Portals
            "discord_bot": {
                "name": "🎮 Discord Bot Portal",
                "type": "DISCORD_INTEGRATION",
                "url": "discord://bot_connection",
                "file_path": f"{self.base_path}/chaosgenius_discord_bot.py",
                "port": None,
                "description": "Discord community integration",
                "launch_command": "python3 chaosgenius_discord_bot.py",
                "status": "UNKNOWN",
            },
            # API Portals
            "api_gateway": {
                "name": "🌐 API Gateway",
                "type": "API_INTERFACE",
                "url": "http://localhost:8000",
                "file_path": f"{self.base_path}/broski_api_gateway.py",
                "port": 8000,
                "description": "External service connections",
                "launch_command": "python3 broski_api_gateway.py",
                "status": "UNKNOWN",
            },
        }

        # Register all portals in database
        for portal_id, portal_data in self.portal_registry.items():
            self._register_portal(portal_id, portal_data)

    def _register_portal(self, portal_id: str, portal_data: Dict):
        """📝 Register portal in database"""
        try:
            with sqlite3.connect(self.portal_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO portal_registry
                    (portal_id, portal_name, portal_type, portal_url, file_path,
                     port, launch_command, last_health_check)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        portal_id,
                        portal_data["name"],
                        portal_data["type"],
                        portal_data["url"],
                        portal_data["file_path"],
                        portal_data.get("port"),
                        portal_data["launch_command"],
                        time.time(),
                    ),
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Portal registration error: {e}")

    def _initialize_portal_health_monitoring(self):
        """💓 Initialize portal health monitoring"""
        print("💓 Initializing portal health monitoring...")
        for portal_id in self.portal_registry.keys():
            self.portal_status[portal_id] = {
                "status": "UNKNOWN",
                "last_check": 0,
                "response_time": 0,
                "uptime": 0,
                "error_count": 0,
            }

    def start_portal_monitoring(self):
        """🔄 Start portal health monitoring"""
        if self.monitoring_active:
            print("⚠️ Portal monitoring already active!")
            return

        self.monitoring_active = True
        self._monitor_thread = threading.Thread(
            target=self._portal_monitor, daemon=True
        )
        self._monitor_thread.start()
        print("🔄🌌 Portal monitoring started!")

    def _portal_monitor(self):
        """🔄 Continuous portal monitoring loop"""
        while self.monitoring_active:
            try:
                for portal_id, portal_data in self.portal_registry.items():
                    self._check_portal_health(portal_id, portal_data)

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"Portal monitoring error: {e}")
                time.sleep(60)

    def _check_portal_health(self, portal_id: str, portal_data: Dict):
        """💓 Check individual portal health"""
        start_time = time.time()
        status = "OFFLINE"
        response_time = 0
        error_message = ""

        try:
            if (
                portal_data["type"] == "WEB_INTERFACE"
                or portal_data["type"] == "WEB_DASHBOARD"
            ):
                # Check web portals
                import requests

                try:
                    response = requests.get(portal_data["url"], timeout=5)
                    if response.status_code == 200:
                        status = "ONLINE"
                    else:
                        status = "ERROR"
                        error_message = f"HTTP {response.status_code}"
                except requests.exceptions.RequestException as e:
                    status = "OFFLINE"
                    error_message = str(e)

            elif portal_data["type"] == "API_INTERFACE":
                # Check API endpoints
                import requests

                try:
                    response = requests.get(f"{portal_data['url']}/health", timeout=5)
                    status = "ONLINE" if response.status_code == 200 else "ERROR"
                except:
                    status = "OFFLINE"

            else:
                # Check file existence for terminal/python portals
                if os.path.exists(portal_data["file_path"]):
                    status = "READY"
                else:
                    status = "MISSING"
                    error_message = "File not found"

            response_time = time.time() - start_time

        except Exception as e:
            status = "ERROR"
            error_message = str(e)
            response_time = time.time() - start_time

        # Update portal status
        self.portal_status[portal_id] = {
            "status": status,
            "last_check": time.time(),
            "response_time": response_time,
            "error_message": error_message,
        }

        # Log health check
        self._log_portal_health(portal_id, status, response_time, error_message)

    def _log_portal_health(
        self, portal_id: str, status: str, response_time: float, error_message: str
    ):
        """📊 Log portal health check"""
        check_id = f"{portal_id}_{int(time.time())}"

        try:
            with sqlite3.connect(self.portal_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO portal_health_log
                    (check_id, portal_id, timestamp, status, response_time, error_message)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        check_id,
                        portal_id,
                        time.time(),
                        status,
                        response_time,
                        error_message,
                    ),
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Health logging error: {e}")

    def launch_portal(self, portal_id: str):
        """🚀 Launch specific portal"""
        if portal_id not in self.portal_registry:
            print(f"❌ Portal {portal_id} not found!")
            return False

        portal = self.portal_registry[portal_id]
        launch_command = portal["launch_command"]

        print(f"🚀 Launching {portal['name']}...")

        try:
            # Change to base directory
            os.chdir(self.base_path)

            # Execute launch command
            if portal["type"] in ["WEB_INTERFACE", "WEB_DASHBOARD"]:
                # Launch web portals in background
                subprocess.Popen(launch_command, shell=True)
                print(f"✅ {portal['name']} launched at {portal['url']}")

                # Open in browser after a delay
                time.sleep(3)
                webbrowser.open(portal["url"])

            else:
                # Launch terminal portals
                print(f"📡 Executing: {launch_command}")
                subprocess.run(launch_command, shell=True)

            return True

        except Exception as e:
            print(f"❌ Failed to launch {portal['name']}: {e}")
            return False

    def launch_all_portals(self):
        """🌌 Launch all available portals"""
        print("🌌 Launching complete portal network...")

        # Launch web portals first
        web_portals = [
            pid
            for pid, p in self.portal_registry.items()
            if p["type"] in ["WEB_INTERFACE", "WEB_DASHBOARD"]
        ]

        for portal_id in web_portals:
            self.launch_portal(portal_id)
            time.sleep(2)  # Stagger launches

        print("🎉 Web portals launched! Terminal portals ready for manual launch.")

    def open_portal_in_browser(self, portal_id: str):
        """🌐 Open portal URL in browser"""
        if portal_id not in self.portal_registry:
            print(f"❌ Portal {portal_id} not found!")
            return

        portal = self.portal_registry[portal_id]
        if portal["url"].startswith("http"):
            webbrowser.open(portal["url"])
            print(f"🌐 Opened {portal['name']} in browser")
        else:
            print(
                f"💡 {portal['name']} is a terminal portal - use launch_portal() instead"
            )

    def get_portal_status(self, portal_id: str) -> Dict:
        """📊 Get detailed portal status"""
        if portal_id not in self.portal_registry:
            return {"error": f"Portal {portal_id} not found"}

        portal = self.portal_registry[portal_id]
        status = self.portal_status.get(portal_id, {})

        return {
            "🌌 Portal Name": portal["name"],
            "🎯 Type": portal["type"],
            "🔋 Status": status.get("status", "UNKNOWN"),
            "🌐 URL": portal["url"],
            "⚡ Response Time": f"{status.get('response_time', 0):.3f}s",
            "💓 Last Check": status.get("last_check", 0),
            "📁 File Path": portal["file_path"],
            "🚀 Launch Command": portal["launch_command"],
        }

    def get_network_overview(self) -> Dict:
        """🌌 Get complete portal network overview"""
        total_portals = len(self.portal_registry)
        online_portals = len(
            [s for s in self.portal_status.values() if s.get("status") == "ONLINE"]
        )
        ready_portals = len(
            [s for s in self.portal_status.values() if s.get("status") == "READY"]
        )
        offline_portals = len(
            [s for s in self.portal_status.values() if s.get("status") == "OFFLINE"]
        )

        # Count by type
        portal_types = {}
        for portal in self.portal_registry.values():
            portal_type = portal["type"]
            portal_types[portal_type] = portal_types.get(portal_type, 0) + 1

        return {
            "🌌 Total Portals": total_portals,
            "🟢 Online Portals": online_portals,
            "🟡 Ready Portals": ready_portals,
            "🔴 Offline Portals": offline_portals,
            "🔄 Monitoring": "ACTIVE" if self.monitoring_active else "INACTIVE",
            "📊 Portal Types": portal_types,
            "⚡ Network Health": f"{((online_portals + ready_portals) / total_portals * 100):.1f}%",
        }

    def generate_portal_directory_html(self):
        """🌐 Generate HTML portal directory page"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 BROski Master Portal Directory</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d1b69 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}

        .portal-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .portal-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }}

        .portal-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(153, 102, 255, 0.3);
        }}

        .status-online {{ color: #00ff88; }}
        .status-ready {{ color: #ffaa00; }}
        .status-offline {{ color: #ff4444; }}
        .status-unknown {{ color: #888888; }}

        .portal-link {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: linear-gradient(45deg, #9966ff, #00ff88);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
        }}

        .portal-link:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(153, 102, 255, 0.4);
        }}

        .network-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌌💜 BROski Master Portal Directory 💜🌌</h1>
        <p>Complete Portal Network Management System</p>
        <p>👑 By Command of Chief Lyndz - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 👑</p>
    </div>

    <div class="network-stats">"""

        # Add network stats
        overview = self.get_network_overview()
        for stat_name, stat_value in overview.items():
            if not isinstance(stat_value, dict):
                html_content += f"""
        <div class="stat-card">
            <h3>{stat_name}</h3>
            <p>{stat_value}</p>
        </div>"""

        html_content += """
    </div>

    <div class="portal-grid">"""

        # Add portal cards
        for portal_id, portal_data in self.portal_registry.items():
            status = self.portal_status.get(portal_id, {}).get("status", "UNKNOWN")
            status_class = f"status-{status.lower()}"

            html_content += f"""
        <div class="portal-card">
            <h3>{portal_data['name']}</h3>
            <p>{portal_data['description']}</p>
            <p><strong>Type:</strong> {portal_data['type']}</p>
            <p class="{status_class}"><strong>Status:</strong> {status}</p>
            <p><strong>Launch:</strong> <code>{portal_data['launch_command']}</code></p>"""

            if portal_data["url"].startswith("http"):
                html_content += f"""
            <a href="{portal_data['url']}" class="portal-link" target="_blank">🚀 Open Portal</a>"""
            else:
                html_content += f"""
            <div class="portal-link" style="background: #666;">📡 Terminal Portal</div>"""

            html_content += """
        </div>"""

        html_content += """
    </div>

    <div style="text-align: center; margin-top: 40px; padding: 20px;">
        <p>🌌 BY COMMAND OF CHIEF LYNDZ - PORTAL EMPIRE REIGNS SUPREME! 🌌</p>
    </div>
</body>
</html>"""

        # Save HTML file
        html_path = f"{self.base_path}/master_portal_directory.html"
        with open(html_path, "w") as f:
            f.write(html_content)

        print(f"🌐 Portal directory generated: {html_path}")
        return html_path

    def stop_portal_monitoring(self):
        """⏹️ Stop portal monitoring"""
        self.monitoring_active = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)
        print("⏹️ Portal monitoring stopped!")

    def interactive_portal_manager(self):
        """🎮 Interactive portal management interface"""
        while True:
            print("\n🌌💜 BROSKI MASTER PORTAL DIRECTORY 💜🌌")
            print("=" * 60)
            print("1. 📊 View Portal Network Overview")
            print("2. 🔍 Check Individual Portal Status")
            print("3. 🚀 Launch Specific Portal")
            print("4. 🌌 Launch All Web Portals")
            print("5. 🌐 Generate HTML Directory")
            print("6. 🔄 Start/Stop Monitoring")
            print("7. 📋 List All Portals")
            print("0. 👋 Exit")

            choice = input("\n💜 Enter your choice (0-7): ").strip()

            if choice == "0":
                print("👋 See you later, Portal Commander!")
                break
            elif choice == "1":
                overview = self.get_network_overview()
                print("\n📊 PORTAL NETWORK OVERVIEW:")
                for key, value in overview.items():
                    print(f"  {key}: {value}")
            elif choice == "2":
                portal_id = input("🔍 Enter portal ID: ").strip()
                status = self.get_portal_status(portal_id)
                print(f"\n📊 Portal Status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
            elif choice == "3":
                portal_id = input("🚀 Enter portal ID to launch: ").strip()
                self.launch_portal(portal_id)
            elif choice == "4":
                self.launch_all_portals()
            elif choice == "5":
                html_path = self.generate_portal_directory_html()
                webbrowser.open(f"file://{html_path}")
            elif choice == "6":
                if self.monitoring_active:
                    self.stop_portal_monitoring()
                else:
                    self.start_portal_monitoring()
            elif choice == "7":
                print("\n📋 ALL AVAILABLE PORTALS:")
                for portal_id, portal_data in self.portal_registry.items():
                    status = self.portal_status.get(portal_id, {}).get(
                        "status", "UNKNOWN"
                    )
                    print(f"  {portal_id}: {portal_data['name']} ({status})")
            else:
                print("❌ Invalid choice. Please try again.")


def main():
    """🚀 Launch Master Portal Directory"""
    print("🌌💜 LAUNCHING BROSKI MASTER PORTAL DIRECTORY! 💜🌌")

    directory = BroskiMasterPortalDirectory()

    # Start monitoring
    directory.start_portal_monitoring()

    # Generate initial HTML directory
    directory.generate_portal_directory_html()

    # Start interactive manager
    try:
        directory.interactive_portal_manager()
    except KeyboardInterrupt:
        print("\n🌌 Shutting down Master Portal Directory...")
        directory.stop_portal_monitoring()


if __name__ == "__main__":
    main()
