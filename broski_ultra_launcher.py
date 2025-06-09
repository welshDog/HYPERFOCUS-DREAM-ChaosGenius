#!/usr/bin/env python3
"""
🎯🚀 BROSKI ULTRA TASK AUTOMATION - LEGENDARY LAUNCHER 🚀🎯
Auto-launches, monitors, and manages all your legendary systems
"""

import asyncio
import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BROskiTaskLauncher:
    """🎯 The most legendary task automation system ever created"""

    def __init__(self):
        self.motto = "LEGENDARY SYSTEMS LAUNCH THEMSELVES. AUTOMATION IS KING."
        self.broski_dollars_earned = 0
        self.tasks_completed = 0

        # Define all legendary tasks
        self.legendary_tasks = {
            "health_matrix": {
                "name": "🧬 BROski Health Matrix",
                "script": "broski_health_matrix.py",
                "auto_launch": True,
                "port": 5001,
                "description": "Ultimate health monitoring system",
                "dependencies": [],
                "status": "READY",
            },
            "dashboard_api": {
                "name": "🎛️ ChaosGenius Dashboard",
                "script": "dashboard_api.py",
                "auto_launch": True,
                "port": 5000,
                "description": "Main command center dashboard",
                "dependencies": [],
                "status": "READY",
            },
            "immortal_guardian": {
                "name": "⚡ Immortal Guardian",
                "script": "immortal_guardian_ultra.py",
                "auto_launch": True,
                "port": None,
                "description": "Auto-resurrection monitoring system",
                "dependencies": [],
                "status": "READY",
            },
            "guardian_zero": {
                "name": "🛡️ Guardian Zero",
                "script": "guardian_zero_command.py",
                "auto_launch": False,  # Manual activation
                "port": None,
                "description": "Elite Defense Units command",
                "dependencies": [],
                "status": "STANDBY",
            },
            "discord_bot": {
                "name": "🤖 ChaosGenius Discord Bot",
                "script": "chaosgenius_discord_bot.py",
                "auto_launch": False,  # Requires token
                "port": None,
                "description": "Discord community management",
                "dependencies": ["discord_token"],
                "status": "READY",
            },
        }

        self.active_processes = {}
        self.launch_sequence_started = False

    async def epic_launch_sequence(self):
        """🚀 Execute the legendary launch sequence"""
        logger.info("🚀 INITIATING EPIC LAUNCH SEQUENCE...")
        logger.info(f"Motto: {self.motto}")

        self.launch_sequence_started = True

        # Phase 1: Core Systems
        logger.info("📡 PHASE 1: Launching core systems...")
        core_systems = ["health_matrix", "dashboard_api"]

        for task_name in core_systems:
            if self.legendary_tasks[task_name]["auto_launch"]:
                await self.launch_task(task_name)
                await asyncio.sleep(3)  # Brief pause between launches

        # Phase 2: Monitoring Systems
        logger.info("🛡️ PHASE 2: Activating monitoring systems...")
        monitoring_systems = ["immortal_guardian"]

        for task_name in monitoring_systems:
            if self.legendary_tasks[task_name]["auto_launch"]:
                await self.launch_task(task_name)
                await asyncio.sleep(2)

        # Phase 3: Verification
        logger.info("✅ PHASE 3: System verification...")
        await self.verify_all_systems()

        # Phase 4: Award BROski$ for successful launch
        self.broski_dollars_earned += 100
        logger.info(f"💰 Launch sequence complete! Earned 100 BROski$!")

        return await self.get_launch_status()

    async def launch_task(self, task_name: str) -> bool:
        """🚀 Launch a specific legendary task"""
        if task_name not in self.legendary_tasks:
            logger.error(f"❌ Unknown task: {task_name}")
            return False

        task_config = self.legendary_tasks[task_name]

        # Check dependencies
        if not await self.check_dependencies(task_config):
            logger.warning(f"⚠️ Dependencies not met for {task_name}")
            return False

        try:
            logger.info(f"🚀 Launching {task_config['name']}...")

            # Kill any existing process first
            await self.kill_existing_process(task_name)

            # Launch the process
            process = subprocess.Popen(
                ["python", task_config["script"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=".",
            )

            # Store process info
            self.active_processes[task_name] = {
                "process": process,
                "launched_at": datetime.now(),
                "pid": process.pid,
            }

            task_config["status"] = "LAUNCHING"

            # Wait a moment and verify it started
            await asyncio.sleep(2)

            if process.poll() is None:  # Still running
                task_config["status"] = "ACTIVE"
                logger.info(
                    f"✅ {task_config['name']} launched successfully! PID: {process.pid}"
                )
                self.tasks_completed += 1
                self.broski_dollars_earned += 10
                return True
            else:
                task_config["status"] = "FAILED"
                logger.error(f"❌ {task_config['name']} failed to start")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to launch {task_name}: {e}")
            task_config["status"] = "ERROR"
            return False

    async def check_dependencies(self, task_config: Dict[str, Any]) -> bool:
        """🔍 Check if task dependencies are met"""
        dependencies = task_config.get("dependencies", [])

        for dep in dependencies:
            if dep == "discord_token":
                # Check if Discord token exists
                token_file = Path("broski_token_config.json")
                if not token_file.exists():
                    logger.warning("⚠️ Discord token config not found")
                    return False

                try:
                    with open(token_file) as f:
                        config = json.load(f)
                        if not config.get("discord", {}).get("token"):
                            logger.warning("⚠️ Discord token not configured")
                            return False
                except:
                    logger.warning("⚠️ Could not read Discord token config")
                    return False

        return True

    async def kill_existing_process(self, task_name: str):
        """💀 Kill any existing process for this task"""
        if task_name in self.active_processes:
            try:
                process = self.active_processes[task_name]["process"]
                if process.poll() is None:  # Still running
                    process.terminate()
                    await asyncio.sleep(1)
                    if process.poll() is None:
                        process.kill()
                del self.active_processes[task_name]
            except:
                pass

    async def verify_all_systems(self) -> Dict[str, bool]:
        """✅ Verify all launched systems are healthy"""
        verification_results = {}

        for task_name, task_config in self.legendary_tasks.items():
            if task_config["status"] == "ACTIVE":
                is_healthy = await self.verify_task_health(task_name, task_config)
                verification_results[task_name] = is_healthy

                if is_healthy:
                    logger.info(f"✅ {task_config['name']} is healthy")
                else:
                    logger.warning(f"⚠️ {task_config['name']} may have issues")

        return verification_results

    async def verify_task_health(
        self, task_name: str, task_config: Dict[str, Any]
    ) -> bool:
        """🩺 Verify individual task health"""
        # Check if process is still running
        if task_name in self.active_processes:
            process = self.active_processes[task_name]["process"]
            if process.poll() is not None:  # Process died
                return False

        # Check port if applicable
        if task_config.get("port"):
            return await self.check_port_health(task_config["port"])

        return True

    async def check_port_health(self, port: int) -> bool:
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

    async def shutdown_all_tasks(self):
        """🛑 Gracefully shutdown all tasks"""
        logger.info("🛑 Initiating graceful shutdown of all tasks...")

        for task_name in list(self.active_processes.keys()):
            await self.shutdown_task(task_name)

        logger.info("🛑 All tasks shutdown complete")

    async def shutdown_task(self, task_name: str):
        """🛑 Shutdown a specific task"""
        if task_name in self.active_processes:
            try:
                process = self.active_processes[task_name]["process"]
                task_config = self.legendary_tasks[task_name]

                logger.info(f"🛑 Shutting down {task_config['name']}...")

                process.terminate()
                await asyncio.sleep(2)

                if process.poll() is None:  # Still running
                    logger.warning(f"⚠️ Force killing {task_config['name']}...")
                    process.kill()

                del self.active_processes[task_name]
                task_config["status"] = "STOPPED"

                logger.info(f"✅ {task_config['name']} shutdown complete")

            except Exception as e:
                logger.error(f"❌ Error shutting down {task_name}: {e}")

    async def restart_task(self, task_name: str) -> bool:
        """🔄 Restart a specific task"""
        logger.info(f"🔄 Restarting {task_name}...")

        await self.shutdown_task(task_name)
        await asyncio.sleep(1)

        return await self.launch_task(task_name)

    def get_launch_status(self) -> Dict[str, Any]:
        """📊 Get complete launch status"""
        active_count = len(
            [t for t in self.legendary_tasks.values() if t["status"] == "ACTIVE"]
        )
        total_tasks = len(self.legendary_tasks)

        return {
            "launch_sequence_started": self.launch_sequence_started,
            "motto": self.motto,
            "broski_dollars_earned": self.broski_dollars_earned,
            "tasks_completed": self.tasks_completed,
            "active_tasks": active_count,
            "total_tasks": total_tasks,
            "legendary_rating": "ULTRA LEGENDARY" if active_count >= 3 else "LEGENDARY",
            "tasks": {
                name: {
                    "name": config["name"],
                    "status": config["status"],
                    "description": config["description"],
                    "auto_launch": config["auto_launch"],
                    "port": config.get("port"),
                    "pid": self.active_processes.get(name, {}).get("pid"),
                    "launched_at": (
                        self.active_processes.get(name, {})
                        .get("launched_at", "")
                        .isoformat()
                        if self.active_processes.get(name, {}).get("launched_at")
                        else None
                    ),
                }
                for name, config in self.legendary_tasks.items()
            },
        }


# Global task launcher instance
task_launcher = BROskiTaskLauncher()


async def main():
    """🚀 Main launcher interface"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "launch":
            await task_launcher.epic_launch_sequence()
        elif command == "status":
            status = task_launcher.get_launch_status()
            print(json.dumps(status, indent=2, default=str))
        elif command == "shutdown":
            await task_launcher.shutdown_all_tasks()
        elif command.startswith("restart-"):
            task_name = command.replace("restart-", "")
            await task_launcher.restart_task(task_name)
        else:
            print(f"Unknown command: {command}")
    else:
        # Default: Epic launch sequence
        await task_launcher.epic_launch_sequence()

        # Keep running to monitor
        try:
            while True:
                await asyncio.sleep(60)
                await task_launcher.verify_all_systems()
        except KeyboardInterrupt:
            await task_launcher.shutdown_all_tasks()


if __name__ == "__main__":
    asyncio.run(main())
