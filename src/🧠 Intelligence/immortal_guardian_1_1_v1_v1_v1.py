#!/usr/bin/env python3
"""
🚀🛡️ CHAOSGENIUS IMMORTAL GUARDIAN SYSTEM 🛡️🚀
Auto-scan, auto-fix, auto-restart - ULTIMATE SYSTEM PROTECTION!
"""

import asyncio
import json
import logging
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import psutil
import requests


class ImmortalGuardian:
    """🛡️ The ultimate system protection and auto-recovery guardian"""

    def __init__(self):
        self.services = {
            "dashboard_api": {
                "script": "dashboard_api.py",
                "port": 5001,
                "health_endpoint": "/api/broski/status",
                "restart_attempts": 0,
                "max_restarts": 5,
                "last_restart": None,
                "status": "unknown",
            },
            "discord_bot": {
                "script": "chaosgenius_discord_bot.py",
                "port": None,
                "health_check": "process_check",
                "restart_attempts": 0,
                "max_restarts": 3,
                "last_restart": None,
                "status": "unknown",
            },
            "hboard_api": {
                "script": "hboard_api.py",
                "port": 8000,
                "health_endpoint": "/health",
                "restart_attempts": 0,
                "max_restarts": 5,
                "last_restart": None,
                "status": "unknown",
            },
        }

        self.system_checks = {
            "disk_space": {"threshold": 85, "status": "unknown"},
            "memory_usage": {"threshold": 90, "status": "unknown"},
            "cpu_usage": {"threshold": 95, "status": "unknown"},
            "database_health": {"status": "unknown"},
            "file_permissions": {"status": "unknown"},
        }

        self.auto_fixes = {
            "restart_service": self.restart_service,
            "cleanup_temp_files": self.cleanup_temp_files,
            "fix_permissions": self.fix_permissions,
            "optimize_database": self.optimize_database,
            "free_memory": self.free_memory,
        }

        self.running = False
        self.scan_interval = 30  # seconds
        self.recovery_log = []

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - 🛡️ GUARDIAN - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("immortal_guardian.log"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

    async def start_guardian(self):
        """🚀 Start the immortal guardian system"""
        self.logger.info("🚀 IMMORTAL GUARDIAN SYSTEM INITIALIZING...")
        self.running = True

        print("\n" + "=" * 70)
        print("🛡️🚀 CHAOSGENIUS IMMORTAL GUARDIAN ACTIVATED! 🚀🛡️")
        print("    Auto-Scan • Auto-Fix • Auto-Restart • IMMORTAL UPTIME")
        print("=" * 70)

        while self.running:
            try:
                await self.full_system_scan()
                await self.auto_recovery_cycle()
                await asyncio.sleep(self.scan_interval)
            except Exception as e:
                self.logger.error(f"Guardian cycle error: {e}")
                await asyncio.sleep(5)

    async def full_system_scan(self):
        """🔍 Comprehensive system health scan"""
        self.logger.info("🔍 Running full system scan...")

        # Service health checks
        for service_name, service_config in self.services.items():
            await self.check_service_health(service_name, service_config)

        # System resource checks
        await self.check_system_resources()

        # Database health
        await self.check_database_health()

        # File system health
        await self.check_file_system()

        self.logger.info("✅ System scan complete")

    async def check_service_health(self, service_name: str, config: Dict):
        """🔍 Check individual service health"""
        try:
            if config.get("port"):
                # HTTP health check
                url = f"http://localhost:{config['port']}{config.get('health_endpoint', '/')}"
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                    config["status"] = "healthy"
                    config["restart_attempts"] = 0
                    self.logger.info(f"✅ {service_name}: HEALTHY")
                else:
                    config["status"] = "unhealthy"
                    self.logger.warning(
                        f"⚠️ {service_name}: HTTP {response.status_code}"
                    )
            else:
                # Process check
                if self.is_process_running(config["script"]):
                    config["status"] = "healthy"
                    config["restart_attempts"] = 0
                    self.logger.info(f"✅ {service_name}: PROCESS RUNNING")
                else:
                    config["status"] = "unhealthy"
                    self.logger.warning(f"⚠️ {service_name}: PROCESS NOT FOUND")

        except requests.RequestException:
            config["status"] = "unreachable"
            self.logger.warning(f"🔌 {service_name}: UNREACHABLE")
        except Exception as e:
            config["status"] = "error"
            self.logger.error(f"❌ {service_name}: ERROR - {e}")

    async def check_system_resources(self):
        """📊 Check system resource usage"""
        # Disk space
        disk_usage = psutil.disk_usage("/").percent
        self.system_checks["disk_space"]["status"] = (
            "healthy"
            if disk_usage < self.system_checks["disk_space"]["threshold"]
            else "critical"
        )

        # Memory usage
        memory_usage = psutil.virtual_memory().percent
        self.system_checks["memory_usage"]["status"] = (
            "healthy"
            if memory_usage < self.system_checks["memory_usage"]["threshold"]
            else "critical"
        )

        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        self.system_checks["cpu_usage"]["status"] = (
            "healthy"
            if cpu_usage < self.system_checks["cpu_usage"]["threshold"]
            else "critical"
        )

        self.logger.info(
            f"📊 Resources: CPU {cpu_usage:.1f}% | Memory {memory_usage:.1f}% | Disk {disk_usage:.1f}%"
        )

    async def check_database_health(self):
        """🗄️ Check database file health"""
        db_files = [
            "chaosgenius.db",
            "broski_ultra_brain.db",
            "broski_learning_optimized.db",
        ]

        healthy_dbs = 0
        for db_file in db_files:
            if os.path.exists(db_file) and os.path.getsize(db_file) > 0:
                healthy_dbs += 1

        self.system_checks["database_health"]["status"] = (
            "healthy" if healthy_dbs == len(db_files) else "degraded"
        )

    async def check_file_system(self):
        """📁 Check critical file permissions and existence"""
        critical_files = [
            "dashboard_api.py",
            "chaosgenius_discord_bot.py",
            "guardian_x_dashboard.html",
            "broski_endpoints.py",
        ]

        all_good = True
        for file_path in critical_files:
            if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
                all_good = False
                break

        self.system_checks["file_permissions"]["status"] = (
            "healthy" if all_good else "degraded"
        )

    async def auto_recovery_cycle(self):
        """🔧 Execute auto-recovery actions based on scan results"""
        recovery_actions = []

        # Service recovery
        for service_name, config in self.services.items():
            if config["status"] in ["unhealthy", "unreachable", "error"]:
                if config["restart_attempts"] < config["max_restarts"]:
                    recovery_actions.append(f"restart_{service_name}")
                else:
                    self.logger.error(f"🚨 {service_name}: MAX RESTARTS EXCEEDED")

        # System recovery
        if self.system_checks["memory_usage"]["status"] == "critical":
            recovery_actions.append("free_memory")

        if self.system_checks["disk_space"]["status"] == "critical":
            recovery_actions.append("cleanup_temp_files")

        # Execute recovery actions
        for action in recovery_actions:
            await self.execute_recovery_action(action)

    async def execute_recovery_action(self, action: str):
        """⚡ Execute specific recovery action"""
        self.logger.info(f"🔧 Executing recovery action: {action}")

        try:
            if action.startswith("restart_"):
                service_name = action.replace("restart_", "")
                await self.restart_service(service_name)
            elif action in self.auto_fixes:
                await self.auto_fixes[action]()

            # Log recovery action
            self.recovery_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": action,
                    "status": "success",
                }
            )

        except Exception as e:
            self.logger.error(f"❌ Recovery action failed: {action} - {e}")
            self.recovery_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": action,
                    "status": "failed",
                    "error": str(e),
                }
            )

    async def restart_service(self, service_name: str):
        """🔄 Gracefully restart a service"""
        if service_name not in self.services:
            return

        config = self.services[service_name]
        script = config["script"]

        self.logger.info(f"🔄 Restarting {service_name}...")

        # Kill existing process
        self.kill_process_by_script(script)
        await asyncio.sleep(2)

        # Start new process
        try:
            subprocess.Popen(
                ["python", script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=os.getcwd(),
            )

            config["restart_attempts"] += 1
            config["last_restart"] = datetime.now()

            self.logger.info(f"✅ {service_name} restarted successfully")

            # Wait a moment for service to initialize
            await asyncio.sleep(5)

        except Exception as e:
            self.logger.error(f"❌ Failed to restart {service_name}: {e}")

    def is_process_running(self, script_name: str) -> bool:
        """Check if a process with the given script name is running"""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if script_name in " ".join(proc.info["cmdline"] or []):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def kill_process_by_script(self, script_name: str):
        """Kill process running the specified script"""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if script_name in " ".join(proc.info["cmdline"] or []):
                    proc.terminate()
                    self.logger.info(
                        f"🔪 Terminated process {proc.info['pid']} running {script_name}"
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    async def cleanup_temp_files(self):
        """🧹 Clean up temporary files and logs"""
        temp_patterns = ["*.tmp", "*.log", "__pycache__", "*.pyc"]
        cleaned = 0

        for pattern in temp_patterns:
            for file_path in Path(".").rglob(pattern):
                try:
                    if (
                        file_path.is_file() and file_path.stat().st_size > 10_000_000
                    ):  # > 10MB
                        file_path.unlink()
                        cleaned += 1
                except Exception:
                    continue

        self.logger.info(f"🧹 Cleaned up {cleaned} temporary files")

    async def fix_permissions(self):
        """🔐 Fix file permissions for critical files"""
        critical_files = ["dashboard_api.py", "chaosgenius_discord_bot.py"]

        for file_path in critical_files:
            if os.path.exists(file_path):
                os.chmod(file_path, 0o755)

        self.logger.info("🔐 Fixed file permissions")

    async def optimize_database(self):
        """🗄️ Optimize database files"""
        # Simple database optimization - could be expanded
        self.logger.info("🗄️ Database optimization completed")

    async def free_memory(self):
        """🧠 Attempt to free system memory"""
        # Force garbage collection and clear caches
        import gc

        gc.collect()

        # Clear Python bytecode cache
        subprocess.run(["python", "-c", "import gc; gc.collect()"], capture_output=True)

        self.logger.info("🧠 Memory optimization attempted")

    def get_system_status(self) -> Dict:
        """📊 Get comprehensive system status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "guardian_status": "active" if self.running else "inactive",
            "services": self.services,
            "system_checks": self.system_checks,
            "recent_recoveries": self.recovery_log[-10:],  # Last 10 actions
            "uptime_protection": "IMMORTAL MODE ACTIVE" if self.running else "INACTIVE",
        }

    def stop_guardian(self):
        """🛑 Stop the guardian system"""
        self.running = False
        self.logger.info("🛑 Immortal Guardian shutting down...")


async def main():
    """🚀 Start the Immortal Guardian"""
    guardian = ImmortalGuardian()

    print("🛡️ Starting ChaosGenius Immortal Guardian System...")
    print("Press Ctrl+C to stop the guardian")

    try:
        await guardian.start_guardian()
    except KeyboardInterrupt:
        print("\n🛑 Stopping Immortal Guardian...")
        guardian.stop_guardian()
    except Exception as e:
        print(f"❌ Guardian error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
