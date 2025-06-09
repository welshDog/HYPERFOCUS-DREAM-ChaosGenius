#!/usr/bin/env python3
"""
🧬⚡ IMMORTAL GUARDIAN ULTRA - AUTO-RESURRECTION SYSTEM ⚡🧬
The most legendary process monitoring and auto-restart system ever created
"""

import asyncio
import json
import logging
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil

# Import Guardian Zero for integration
try:
    from guardian_zero_command import guardian_zero

    GUARDIAN_ZERO_AVAILABLE = True
except ImportError:
    GUARDIAN_ZERO_AVAILABLE = False
    print("⚠️ Guardian Zero not available, running in standalone mode")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImmortalGuardian:
    """🧬⚡ The legendary immortal guardian that never lets anything die"""

    def __init__(self):
        self.motto = "NOTHING DIES ON MY WATCH. RESURRECTION IS GUARANTEED."
        self.broski_dollars_earned = 0
        self.resurrections_performed = 0
        self.immortal_processes = {
            "dashboard_api": {
                "script": "dashboard_api.py",
                "port": 5000,
                "health_endpoint": "http://localhost:5000/api/portal-status",
                "max_restarts": 5,
                "restart_count": 0,
                "last_restart": None,
                "process": None,
                "status": "MONITORING",
            },
            "health_matrix": {
                "script": "broski_health_matrix.py",
                "port": 5001,
                "health_endpoint": "http://localhost:5001/api/broski/health",
                "max_restarts": 5,
                "restart_count": 0,
                "last_restart": None,
                "process": None,
                "status": "MONITORING",
            },
            "discord_bot": {
                "script": "chaosgenius_discord_bot.py",
                "port": None,
                "health_endpoint": None,  # Discord presence check
                "max_restarts": 3,
                "restart_count": 0,
                "last_restart": None,
                "process": None,
                "status": "MONITORING",
            },
            "guardian_zero": {
                "script": "guardian_zero_command.py",
                "port": None,
                "health_endpoint": None,
                "max_restarts": 10,  # Guardian Zero gets more chances
                "restart_count": 0,
                "last_restart": None,
                "process": None,
                "status": "MONITORING",
            },
        }

        # Stats tracking
        self.monitoring_since = datetime.now()
        self.total_health_checks = 0
        self.successful_resurrections = 0
        self.failed_resurrections = 0

    async def monitor_immortal_processes(self):
        """🔍 Monitor all immortal processes and resurrect if needed"""
        logger.info("🧬 Immortal Guardian starting patrol...")

        while True:
            try:
                for process_name, config in self.immortal_processes.items():
                    await self.check_and_resurrect(process_name, config)
                    await asyncio.sleep(2)  # Brief pause between checks

                self.total_health_checks += 1

                # Award BROski$ for successful monitoring rounds
                if self.total_health_checks % 10 == 0:
                    self.broski_dollars_earned += 1
                    if GUARDIAN_ZERO_AVAILABLE:
                        guardian_zero.award_xp(5, "Immortal Guardian monitoring round")

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"❌ Immortal Guardian patrol error: {e}")
                await asyncio.sleep(60)  # Longer wait on errors

    async def check_and_resurrect(self, process_name: str, config: Dict[str, Any]):
        """⚡ Check if process is alive and resurrect if needed"""
        is_alive = await self.is_process_alive(process_name, config)

        if not is_alive:
            logger.warning(f"💀 {process_name} is DEAD! Initiating resurrection...")

            # Check if we haven't exceeded max restarts
            if config["restart_count"] < config["max_restarts"]:
                success = await self.resurrect_process(process_name, config)

                if success:
                    self.successful_resurrections += 1
                    self.broski_dollars_earned += 10

                    if GUARDIAN_ZERO_AVAILABLE:
                        guardian_zero.send_alert(
                            "IMMORTAL-GUARDIAN",
                            "resurrection",
                            f"⚡ Successfully resurrected {process_name}!",
                            "success",
                        )
                        guardian_zero.award_xp(25, f"Resurrected {process_name}")
                else:
                    self.failed_resurrections += 1
                    if GUARDIAN_ZERO_AVAILABLE:
                        guardian_zero.send_alert(
                            "IMMORTAL-GUARDIAN",
                            "resurrection_failed",
                            f"💀 Failed to resurrect {process_name}",
                            "error",
                        )
            else:
                logger.error(f"🚨 {process_name} exceeded max restart attempts!")
                config["status"] = "ABANDONED"

                if GUARDIAN_ZERO_AVAILABLE:
                    guardian_zero.send_alert(
                        "IMMORTAL-GUARDIAN",
                        "max_restarts_exceeded",
                        f"🚨 {process_name} abandoned - too many failures!",
                        "critical",
                    )

    async def is_process_alive(self, process_name: str, config: Dict[str, Any]) -> bool:
        """🔍 Check if process is actually alive and healthy"""

        # Method 1: Check if process object is running
        if config.get("process"):
            try:
                if config["process"].poll() is None:  # Process still running
                    # Method 2: Health endpoint check (if available)
                    if config.get("health_endpoint"):
                        return await self.check_health_endpoint(
                            config["health_endpoint"]
                        )
                    return True
            except:
                pass

        # Method 3: Search for process by script name
        script_name = config["script"]
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = " ".join(proc.info["cmdline"] or [])
                if script_name in cmdline:
                    # Method 4: Port check (if applicable)
                    if config.get("port"):
                        return await self.check_port_alive(config["port"])
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return False

    async def check_health_endpoint(self, endpoint: str) -> bool:
        """🩺 Check if health endpoint responds"""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, timeout=5) as response:
                    return response.status == 200
        except:
            return False

    async def check_port_alive(self, port: int) -> bool:
        """🔍 Check if port is responding"""
        try:
            import socket

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(("localhost", port))
            sock.close()
            return result == 0
        except:
            return False

    async def resurrect_process(
        self, process_name: str, config: Dict[str, Any]
    ) -> bool:
        """⚡ Resurrect a dead process like a legendary necromancer"""
        try:
            script_path = config["script"]

            # Kill any zombie processes first
            await self.kill_zombie_processes(script_path)

            # Start the process
            logger.info(f"⚡ Resurrecting {process_name} from {script_path}...")

            process = subprocess.Popen(
                ["python", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd(),
            )

            config["process"] = process
            config["restart_count"] += 1
            config["last_restart"] = datetime.now()
            config["status"] = "RESURRECTED"

            # Wait a moment to see if it starts successfully
            await asyncio.sleep(3)

            if process.poll() is None:  # Still running
                logger.info(
                    f"✅ {process_name} successfully resurrected! PID: {process.pid}"
                )
                self.resurrections_performed += 1
                return True
            else:
                logger.error(f"❌ {process_name} died immediately after resurrection")
                return False

        except Exception as e:
            logger.error(f"❌ Resurrection failed for {process_name}: {e}")
            return False

    async def kill_zombie_processes(self, script_name: str):
        """💀 Kill any zombie processes before resurrection"""
        try:
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = " ".join(proc.info["cmdline"] or [])
                    if script_name in cmdline:
                        logger.info(
                            f"💀 Killing zombie process: PID {proc.info['pid']}"
                        )
                        proc.terminate()
                        await asyncio.sleep(1)
                        if proc.is_running():
                            proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"❌ Error killing zombies: {e}")

    def get_immortal_status(self) -> Dict[str, Any]:
        """📊 Get complete immortal guardian status"""
        uptime = datetime.now() - self.monitoring_since

        return {
            "immortal_guardian_online": True,
            "motto": self.motto,
            "monitoring_since": self.monitoring_since.isoformat(),
            "uptime_hours": round(uptime.total_seconds() / 3600, 2),
            "broski_dollars_earned": self.broski_dollars_earned,
            "stats": {
                "total_health_checks": self.total_health_checks,
                "successful_resurrections": self.successful_resurrections,
                "failed_resurrections": self.failed_resurrections,
                "resurrections_performed": self.resurrections_performed,
            },
            "processes": {
                name: {
                    "status": config["status"],
                    "restart_count": config["restart_count"],
                    "max_restarts": config["max_restarts"],
                    "last_restart": (
                        config["last_restart"].isoformat()
                        if config["last_restart"]
                        else None
                    ),
                    "process_running": config["process"]
                    and config["process"].poll() is None,
                }
                for name, config in self.immortal_processes.items()
            },
            "legendary_rating": (
                "ULTRA LEGENDARY" if self.successful_resurrections > 10 else "LEGENDARY"
            ),
        }

    async def emergency_resurrect_all(self):
        """🚨 Emergency: Resurrect all dead processes immediately"""
        logger.warning("🚨 EMERGENCY RESURRECTION PROTOCOL ACTIVATED!")

        tasks = []
        for process_name, config in self.immortal_processes.items():
            if config["status"] != "ABANDONED":
                config["restart_count"] = 0  # Reset restart count for emergency
                tasks.append(self.resurrect_process(process_name, config))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful = sum(1 for r in results if r is True)

        logger.info(
            f"🧬 Emergency resurrection complete: {successful}/{len(tasks)} processes restored"
        )

        if GUARDIAN_ZERO_AVAILABLE:
            guardian_zero.send_alert(
                "IMMORTAL-GUARDIAN",
                "emergency_resurrection",
                f"🚨 Emergency protocol: {successful}/{len(tasks)} processes restored",
                "warning",
            )
            guardian_zero.award_xp(100, "Emergency resurrection protocol")

        return {"resurrected": successful, "total": len(tasks)}


# Global immortal guardian instance
immortal_guardian = ImmortalGuardian()


async def main():
    """🧬 Main immortal guardian loop"""
    logger.info("🧬⚡ IMMORTAL GUARDIAN ULTRA STARTING UP ⚡🧬")
    logger.info(f"Motto: {immortal_guardian.motto}")

    await immortal_guardian.monitor_immortal_processes()


if __name__ == "__main__":
    asyncio.run(main())
