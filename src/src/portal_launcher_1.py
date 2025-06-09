#!/usr/bin/env python3
"""
🚀💜 CHAOSGENIUS PORTAL LAUNCHER - NO CONFLICTS MODE! 💜🚀
Launches all your BROski services in perfect harmony with optimized ports

🌍 PORTAL NETWORK:
- Port 5000: ChaosGenius Dashboard (Main Control Center)
- Port 5001: BROski Health Matrix (System Vitals)
- Port 5002: Memory Crystal Portal (AI Memory & Metrics)
- Port 5003: Performance Control Center (Optimization Hub)
- Port 5004: BROski Ad Slot System (Business Operations)
- Port 5005: BROski Ultra Server Armor (Protection & Monitoring)
- Port 5006: BROski Wallet API (Token & Finance Management)
- Port 5007: Security Fortress (Advanced Security)
- Port 5008: Brain Command Center (Neural Interface)
- Port 5009: Defender Simulator (Cybersecurity RPG)
- Port 5173: BROski HyperPortal (React UI)
- Port 7777: Immortal Dream Server (Chief Lyndz Memorial)
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import psutil
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - 🚀 Portal Launcher - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/root/chaosgenius/logs/portal_launcher.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ChaosGeniusPortalLauncher:
    """🚀💜 The Ultimate Portal Management System"""

    def __init__(self):
        self.base_path = Path("/root/chaosgenius")
        self.processes = {}
        self.portal_config = {
            "5000": {
                "name": "ChaosGenius Dashboard",
                "script": "dashboard_api.py",
                "icon": "🎛️",
                "priority": 1,
                "startup_delay": 2,
                "health_endpoint": "/api/health",
            },
            "5001": {
                "name": "BROski Health Matrix",
                "script": "broski_health_matrix.py",
                "icon": "💚",
                "priority": 2,
                "startup_delay": 3,
                "health_endpoint": "/api/broski/health",
            },
            "5002": {
                "name": "Memory Crystal Portal",
                "script": "memory_crystal_generator.py",
                "icon": "💎",
                "priority": 3,
                "startup_delay": 2,
                "health_endpoint": "/api/health",
            },
            "5003": {
                "name": "Performance Control Center",
                "script": "performance_control_center.py",
                "icon": "⚡",
                "priority": 4,
                "startup_delay": 2,
                "health_endpoint": "/api/status",
            },
            "5004": {
                "name": "BROski Ad Slot System",
                "script": "broski_adslot_system.py",
                "icon": "💰",
                "priority": 5,
                "startup_delay": 4,
                "health_endpoint": "/api/adslots",
            },
            "5005": {
                "name": "BROski Ultra Server Armor",
                "script": "broski_ultra_server_armor.py",
                "icon": "🛡️",
                "priority": 6,
                "startup_delay": 3,
                "health_endpoint": "/monitor",
            },
            "5006": {
                "name": "BROski Wallet API",
                "script": "broski_wallet_api.py",
                "icon": "🪙",
                "priority": 7,
                "startup_delay": 2,
                "health_endpoint": "/api/health",
            },
            "5007": {
                "name": "Security Fortress",
                "script": "broski_ultra_security_fortress.py",
                "icon": "🔐",
                "priority": 8,
                "startup_delay": 3,
                "health_endpoint": "/api/security/status",
            },
            "5008": {
                "name": "Brain Command Center",
                "script": "hyperfocus_brain_command_center.py",
                "icon": "🧠",
                "priority": 9,
                "startup_delay": 4,
                "health_endpoint": "/api/brain-state",
            },
            "5009": {
                "name": "Defender Simulator",
                "script": "broski_defender_simulator.py",
                "icon": "🎮",
                "priority": 10,
                "startup_delay": 3,
                "health_endpoint": "/api/security/status",
            },
        }

    def print_banner(self):
        """🎨 Display the legendary startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════╗
║  🚀💜 CHAOSGENIUS PORTAL LAUNCHER - ULTRA HARMONY MODE! 💜🚀      ║
║                                                                  ║
║  🌍 ALL PORTALS OPTIMIZED FOR MAXIMUM NEURODIVERGENT POWER!     ║
║  ⚡ ZERO CONFLICTS • PERFECT TIMING • LEGENDARY PERFORMANCE     ║
║                                                                  ║
║  Ready to launch your entire BROski empire with NO CONFLICTS!   ║
╚══════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def check_port_availability(self, port):
        """🔍 Check if a port is available"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == int(port) and conn.status == "LISTEN":
                    return False
            return True
        except:
            return True

    def kill_existing_processes(self):
        """🧹 Clean up any existing processes on our ports"""
        logger.info("🧹 Cleaning up any existing processes...")

        for port in self.portal_config.keys():
            if not self.check_port_availability(port):
                logger.info(f"🔧 Cleaning up process on port {port}")
                try:
                    # Find and kill process using the port
                    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                        try:
                            for conn in proc.connections():
                                if conn.laddr.port == int(port):
                                    logger.info(
                                        f"🛑 Terminating process {proc.pid} on port {port}"
                                    )
                                    proc.terminate()
                                    time.sleep(1)
                                    if proc.is_running():
                                        proc.kill()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                except Exception as e:
                    logger.warning(f"⚠️ Could not clean port {port}: {e}")

    def start_portal(self, port, config):
        """🚀 Start a single portal service"""
        script_path = self.base_path / config["script"]

        if not script_path.exists():
            logger.warning(f"⚠️ Script not found: {script_path}")
            return False

        try:
            logger.info(f"🚀 Starting {config['icon']} {config['name']} on port {port}")

            # Start the process
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.processes[port] = {
                "process": process,
                "config": config,
                "start_time": datetime.now(),
                "status": "starting",
            }

            # Wait for startup delay
            time.sleep(config["startup_delay"])

            # Check if process is still running
            if process.poll() is None:
                logger.info(
                    f"✅ {config['icon']} {config['name']} started successfully on port {port}"
                )
                return True
            else:
                stdout, stderr = process.communicate()
                logger.error(f"❌ {config['name']} failed to start: {stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to start {config['name']}: {e}")
            return False

    def check_portal_health(self, port, config):
        """💚 Check if a portal is healthy"""
        try:
            url = f"http://localhost:{port}{config['health_endpoint']}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                self.processes[port]["status"] = "healthy"
                return True
            else:
                self.processes[port]["status"] = "unhealthy"
                return False

        except Exception as e:
            self.processes[port]["status"] = "unreachable"
            return False

    def launch_all_portals(self):
        """🚀 Launch all portals in optimized order"""
        logger.info("🚀 Starting portal launch sequence...")

        # Sort portals by priority
        sorted_portals = sorted(
            self.portal_config.items(), key=lambda x: x[1]["priority"]
        )

        successful_launches = 0

        for port, config in sorted_portals:
            if self.start_portal(port, config):
                successful_launches += 1

            # Small delay between launches to prevent resource conflicts
            time.sleep(1)

        logger.info(
            f"🎯 Launch complete! {successful_launches}/{len(self.portal_config)} portals started"
        )
        return successful_launches

    def run_health_check(self):
        """💚 Run health checks on all portals"""
        logger.info("💚 Running health checks...")

        healthy_count = 0

        for port, process_info in self.processes.items():
            config = process_info["config"]

            # Wait a moment for the service to fully start
            time.sleep(2)

            if self.check_portal_health(port, config):
                logger.info(f"✅ {config['icon']} {config['name']} is healthy")
                healthy_count += 1
            else:
                logger.warning(
                    f"⚠️ {config['icon']} {config['name']} health check failed"
                )

        return healthy_count

    def print_portal_status(self):
        """📊 Display current portal status"""
        print("\n" + "=" * 80)
        print("🌍 CHAOSGENIUS PORTAL NETWORK STATUS")
        print("=" * 80)

        for port, process_info in self.processes.items():
            config = process_info["config"]
            status = process_info.get("status", "unknown")

            status_icon = {
                "healthy": "✅",
                "starting": "🔄",
                "unhealthy": "⚠️",
                "unreachable": "❌",
            }.get(status, "❓")

            print(
                f"{config['icon']} Port {port}: {config['name']} {status_icon} {status.upper()}"
            )
            print(f"   🌐 URL: http://localhost:{port}")
            print(f"   ⏰ Started: {process_info['start_time'].strftime('%H:%M:%S')}")
            print()

    def monitor_portals(self):
        """👁️ Monitor all portals continuously"""
        logger.info("👁️ Starting portal monitoring...")

        try:
            while True:
                print(
                    f"\n⏰ Portal Status Check - {datetime.now().strftime('%H:%M:%S')}"
                )

                for port, process_info in self.processes.items():
                    process = process_info["process"]
                    config = process_info["config"]

                    # Check if process is still running
                    if process.poll() is not None:
                        logger.warning(f"🔄 {config['name']} stopped, restarting...")
                        self.start_portal(port, config)
                    else:
                        # Check health
                        self.check_portal_health(port, config)

                self.print_portal_status()
                time.sleep(30)  # Check every 30 seconds

        except KeyboardInterrupt:
            logger.info("🛑 Monitoring stopped by user")
            self.shutdown_all_portals()

    def shutdown_all_portals(self):
        """🛑 Gracefully shutdown all portals"""
        logger.info("🛑 Shutting down all portals...")

        for port, process_info in self.processes.items():
            process = process_info["process"]
            config = process_info["config"]

            try:
                logger.info(f"🛑 Stopping {config['name']}")
                process.terminate()

                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

            except Exception as e:
                logger.error(f"❌ Error stopping {config['name']}: {e}")

        logger.info("✅ All portals shut down")

    def create_quick_launcher(self):
        """🚀 Create a quick launcher script"""
        launcher_script = """#!/bin/bash
# 🚀💜 Quick Portal Launcher
echo "🚀 Starting ChaosGenius Portal Network..."
python3 /root/chaosgenius/portal_launcher.py
"""

        launcher_path = self.base_path / "quick_launch.sh"
        with open(launcher_path, "w") as f:
            f.write(launcher_script)

        os.chmod(launcher_path, 0o755)
        logger.info(f"✅ Quick launcher created: {launcher_path}")

    def run(self):
        """🚀 Main execution method"""
        # Create logs directory
        os.makedirs(self.base_path / "logs", exist_ok=True)

        self.print_banner()

        # Clean up any existing processes
        self.kill_existing_processes()

        # Launch all portals
        successful = self.launch_all_portals()

        if successful > 0:
            # Run health checks
            healthy = self.run_health_check()

            # Display status
            self.print_portal_status()

            print(f"\n🎉 PORTAL LAUNCH COMPLETE!")
            print(f"✅ {successful} portals started")
            print(f"💚 {healthy} portals healthy")
            print(f"\n🌐 Main Dashboard: http://localhost:5000")
            print(
                f"💜 BROski Empire is ONLINE and ready for neurodivergent excellence!"
            )

            # Create quick launcher
            self.create_quick_launcher()

            # Start monitoring
            input("\nPress Enter to start portal monitoring (Ctrl+C to exit)...")
            self.monitor_portals()
        else:
            print("❌ No portals could be started. Check logs for details.")


if __name__ == "__main__":
    launcher = ChaosGeniusPortalLauncher()
    launcher.run()
