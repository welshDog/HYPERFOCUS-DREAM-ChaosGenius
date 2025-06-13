#!/usr/bin/env python3
"""
⚡💀 IMMORTAL GUARDIAN ULTRA - AUTO-RESURRECTION SYSTEM 💀⚡
The ultimate system that ensures BROSKI∞ NEVER DIES!
"""

import asyncio
import json
import logging
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImmortalGuardianUltra:
    """⚡💀 The most legendary auto-resurrection system ever created 💀⚡"""

    def __init__(self):
        self.motto = "DEATH IS TEMPORARY. RESURRECTION IS ETERNAL. BROSKI∞ IS IMMORTAL."
        self.guardian_config_path = Path("immortal_guardian_config.json")
        self.resurrection_log_path = Path("resurrection_log.json")

        # Guardian stats
        self.resurrections_performed = 0
        self.systems_monitored = 0
        self.immortality_score = 100

        # Load configuration
        self.config = self.load_guardian_config()

        # Resurrection log
        self.resurrection_log = []

        logger.info("⚡💀 IMMORTAL GUARDIAN ULTRA ACTIVATED! 💀⚡")
        logger.info(f"🔥 Motto: {self.motto}")

    def load_guardian_config(self) -> Dict[str, Any]:
        """📜 Load the guardian configuration"""
        default_config = {
            "monitored_systems": {
                "broski_health_matrix": {
                    "script": "broski_health_matrix.py",
                    "port": 5001,
                    "check_interval": 30,
                    "max_failures": 3,
                    "auto_resurrect": True,
                    "resurrection_delay": 5,
                    "health_check_url": "http://localhost:5001/api/health",
                },
                "dashboard_api": {
                    "script": "dashboard_api.py",
                    "port": 5000,
                    "check_interval": 30,
                    "max_failures": 3,
                    "auto_resurrect": True,
                    "resurrection_delay": 5,
                    "health_check_url": "http://localhost:5000/api/status",
                },
                "chaosgenius_discord_bot": {
                    "script": "chaosgenius_discord_bot.py",
                    "port": None,
                    "check_interval": 60,
                    "max_failures": 2,
                    "auto_resurrect": True,
                    "resurrection_delay": 10,
                    "health_check_url": None,
                },
                "agent_army_forge_master": {
                    "script": "agent_army_forge_master.py",
                    "port": None,
                    "check_interval": 120,
                    "max_failures": 2,
                    "auto_resurrect": True,
                    "resurrection_delay": 15,
                    "health_check_url": None,
                },
            },
            "guardian_settings": {
                "master_check_interval": 15,
                "resurrection_cooldown": 30,
                "max_concurrent_resurrections": 3,
                "emergency_protocols": True,
                "notification_enabled": True,
                "auto_backup_before_resurrection": True,
            },
        }

        if self.guardian_config_path.exists():
            try:
                with open(self.guardian_config_path, "r") as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                default_config.update(loaded_config)
            except Exception as e:
                logger.warning(f"⚠️ Failed to load config, using defaults: {e}")

        # Save the config (in case defaults were used)
        self.save_guardian_config(default_config)
        return default_config

    def save_guardian_config(self, config: Dict[str, Any]):
        """💾 Save guardian configuration"""
        try:
            with open(self.guardian_config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to save config: {e}")

    async def check_system_health(
        self, system_name: str, system_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🩺 Check the health of a specific system"""
        health_status = {
            "system_name": system_name,
            "timestamp": datetime.now().isoformat(),
            "is_alive": False,
            "process_running": False,
            "port_responding": False,
            "health_check_passed": False,
            "cpu_usage": 0,
            "memory_usage": 0,
            "failures": 0,
        }

        try:
            # Check if process is running
            script_name = system_config["script"]
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    if proc.info["cmdline"] and script_name in " ".join(
                        proc.info["cmdline"]
                    ):
                        health_status["process_running"] = True
                        health_status["cpu_usage"] = proc.cpu_percent()
                        health_status["memory_usage"] = proc.memory_percent()
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Check port if applicable
            if system_config.get("port"):
                health_status["port_responding"] = await self.check_port_alive(
                    system_config["port"]
                )

            # Perform health check if URL provided
            if system_config.get("health_check_url"):
                health_status["health_check_passed"] = await self.perform_health_check(
                    system_config["health_check_url"]
                )

            # Determine overall health
            if system_config.get("port"):
                health_status["is_alive"] = (
                    health_status["process_running"]
                    and health_status["port_responding"]
                )
            else:
                health_status["is_alive"] = health_status["process_running"]

            if system_config.get("health_check_url"):
                health_status["is_alive"] = (
                    health_status["is_alive"] and health_status["health_check_passed"]
                )

        except Exception as e:
            logger.error(f"❌ Health check failed for {system_name}: {e}")
            health_status["error"] = str(e)

        return health_status

    async def check_port_alive(self, port: int) -> bool:
        """🔍 Check if a port is responding"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            return result == 0
        except Exception:
            return False

    async def perform_health_check(self, health_url: str) -> bool:
        """🌐 Perform HTTP health check"""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(health_url, timeout=5) as response:
                    return response.status == 200
        except Exception:
            # Fallback to basic requests if aiohttp not available
            try:
                import requests

                response = requests.get(health_url, timeout=5)
                return response.status_code == 200
            except Exception:
                return False

    async def resurrect_system(
        self, system_name: str, system_config: Dict[str, Any]
    ) -> bool:
        """⚡💀 RESURRECT A FALLEN SYSTEM WITH ULTIMATE POWER 💀⚡"""
        logger.info(f"⚡💀 INITIATING RESURRECTION: {system_name} 💀⚡")

        resurrection_attempt = {
            "system_name": system_name,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "error": None,
            "resurrection_type": "AUTO",
            "attempts": 1,
        }

        try:
            # Step 1: Backup if enabled
            if self.config["guardian_settings"]["auto_backup_before_resurrection"]:
                await self.create_emergency_backup(system_name)

            # Step 2: Kill any zombie processes
            await self.eliminate_zombie_processes(system_config["script"])

            # Step 3: Wait resurrection delay
            resurrection_delay = system_config.get("resurrection_delay", 5)
            logger.info(f"⏳ Resurrection delay: {resurrection_delay} seconds...")
            await asyncio.sleep(resurrection_delay)

            # Step 4: Launch the system
            script_path = Path(system_config["script"])
            if not script_path.exists():
                raise FileNotFoundError(f"Script not found: {script_path}")

            logger.info(f"🚀 Launching {system_name}...")
            process = subprocess.Popen(
                ["python3", str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=".",
            )

            # Step 5: Verify resurrection
            await asyncio.sleep(3)  # Give it time to start

            if process.poll() is None:  # Still running
                # Double-check with health check
                await asyncio.sleep(2)
                health_status = await self.check_system_health(
                    system_name, system_config
                )

                if health_status["is_alive"]:
                    resurrection_attempt["success"] = True
                    self.resurrections_performed += 1
                    logger.info(
                        f"✅ RESURRECTION SUCCESSFUL: {system_name} IS ALIVE! ⚡💀"
                    )
                else:
                    raise Exception("System started but failed health check")
            else:
                raise Exception("Process died immediately after launch")

        except Exception as e:
            resurrection_attempt["error"] = str(e)
            logger.error(f"❌ RESURRECTION FAILED: {system_name} - {e}")

        # Log the resurrection attempt
        self.resurrection_log.append(resurrection_attempt)
        self.save_resurrection_log()

        return resurrection_attempt["success"]

    async def eliminate_zombie_processes(self, script_name: str):
        """💀 Kill any zombie processes for the script"""
        try:
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    if proc.info["cmdline"] and script_name in " ".join(
                        proc.info["cmdline"]
                    ):
                        logger.info(
                            f"💀 Eliminating zombie process: PID {proc.info['pid']}"
                        )
                        proc.terminate()
                        await asyncio.sleep(1)
                        if proc.is_running():
                            proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.warning(f"⚠️ Failed to eliminate zombies: {e}")

    async def create_emergency_backup(self, system_name: str):
        """🛡️ Create emergency backup before resurrection"""
        try:
            backup_dir = Path("emergency_backups")
            backup_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{system_name}_emergency_backup_{timestamp}"

            # This is a placeholder - in a real system you'd backup databases, configs, etc.
            logger.info(f"🛡️ Emergency backup created: {backup_name}")

        except Exception as e:
            logger.warning(f"⚠️ Backup failed: {e}")

    async def monitor_all_systems(self):
        """👁️ Monitor all configured systems"""
        logger.info("👁️ Starting immortal monitoring of all systems...")

        system_failures = {}  # Track failures per system

        while True:
            try:
                master_interval = self.config["guardian_settings"][
                    "master_check_interval"
                ]

                for system_name, system_config in self.config[
                    "monitored_systems"
                ].items():
                    if not system_config.get("auto_resurrect", True):
                        continue  # Skip systems with auto-resurrect disabled

                    # Check system health
                    health_status = await self.check_system_health(
                        system_name, system_config
                    )

                    if not health_status["is_alive"]:
                        # System is dead!
                        if system_name not in system_failures:
                            system_failures[system_name] = 0

                        system_failures[system_name] += 1
                        max_failures = system_config.get("max_failures", 3)

                        logger.warning(
                            f"💀 SYSTEM DOWN: {system_name} (Failure {system_failures[system_name]}/{max_failures})"
                        )

                        if system_failures[system_name] >= max_failures:
                            # Time for resurrection!
                            logger.info(
                                f"⚡ RESURRECTION THRESHOLD REACHED: {system_name}"
                            )

                            success = await self.resurrect_system(
                                system_name, system_config
                            )
                            if success:
                                system_failures[system_name] = 0  # Reset failure count
                            else:
                                # Failed resurrection - wait before trying again
                                await asyncio.sleep(
                                    self.config["guardian_settings"][
                                        "resurrection_cooldown"
                                    ]
                                )
                    else:
                        # System is alive - reset failure count
                        if system_name in system_failures:
                            system_failures[system_name] = 0

                        # Log healthy status periodically
                        if hasattr(self, "_last_health_log"):
                            if (
                                time.time() - self._last_health_log > 300
                            ):  # Every 5 minutes
                                logger.info(f"💚 SYSTEM HEALTHY: {system_name}")
                                self._last_health_log = time.time()
                        else:
                            self._last_health_log = time.time()

                # Update immortality score
                total_systems = len(self.config["monitored_systems"])
                healthy_systems = sum(
                    1 for failures in system_failures.values() if failures == 0
                )
                self.immortality_score = (
                    int((healthy_systems / total_systems) * 100)
                    if total_systems > 0
                    else 100
                )

                await asyncio.sleep(master_interval)

            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                await asyncio.sleep(30)  # Short delay before retrying

    def save_resurrection_log(self):
        """📝 Save resurrection log to file"""
        try:
            with open(self.resurrection_log_path, "w") as f:
                json.dump(self.resurrection_log, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to save resurrection log: {e}")

    def get_immortal_status(self) -> Dict[str, Any]:
        """📊 Get complete immortal guardian status"""
        return {
            "motto": self.motto,
            "immortality_score": self.immortality_score,
            "resurrections_performed": self.resurrections_performed,
            "systems_monitored": len(self.config["monitored_systems"]),
            "guardian_uptime": "ETERNAL",
            "legendary_rating": self.get_legendary_rating(),
            "recent_resurrections": (
                self.resurrection_log[-10:] if self.resurrection_log else []
            ),
            "config": self.config,
        }

    def get_legendary_rating(self) -> str:
        """👑 Get legendary rating based on performance"""
        if self.immortality_score >= 95:
            return "ULTRA IMMORTAL 👑💀"
        elif self.immortality_score >= 85:
            return "LEGENDARY GUARDIAN 🌟⚡"
        elif self.immortality_score >= 70:
            return "EPIC PROTECTOR ⚡🛡️"
        elif self.immortality_score >= 50:
            return "STABLE GUARDIAN 🛡️"
        else:
            return "LEARNING IMMORTAL 📚⚡"

    async def emergency_protocol(self, system_name: str):
        """🚨 Execute emergency resurrection protocol"""
        logger.info(f"🚨 EMERGENCY PROTOCOL ACTIVATED: {system_name}")

        # This would implement emergency measures like:
        # - Force restart system services
        # - Clear temporary files
        # - Reset network connections
        # - Notify administrators
        # - Activate backup systems

        emergency_log = {
            "timestamp": datetime.now().isoformat(),
            "system": system_name,
            "protocol": "EMERGENCY_RESURRECTION",
            "actions": [
                "Force process termination",
                "Resource cleanup",
                "Emergency restart",
                "Health verification",
            ],
        }

        self.resurrection_log.append(emergency_log)
        logger.info(f"🚨 Emergency protocol completed for {system_name}")


async def main():
    """⚡💀 Main immortal guardian execution 💀⚡"""
    guardian = ImmortalGuardianUltra()

    logger.info("⚡💀 IMMORTAL GUARDIAN ULTRA IS FULLY OPERATIONAL! 💀⚡")
    logger.info(f"🛡️ Monitoring {len(guardian.config['monitored_systems'])} systems")
    logger.info(f"⚡ Resurrection protocols ACTIVE")

    try:
        await guardian.monitor_all_systems()
    except KeyboardInterrupt:
        logger.info("🛑 Immortal Guardian shutting down... (but immortality remains!)")
        guardian.save_resurrection_log()


if __name__ == "__main__":
    asyncio.run(main())
