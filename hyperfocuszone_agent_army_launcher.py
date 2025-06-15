#!/usr/bin/env python3
"""
🚀💯 HYPERFOCUSZONE AGENT ARMY LAUNCHER 💯🚀
🔥 ONE COMMAND TO RULE THEM ALL! 🔥
👑 Launch ALL Agent Systems in Perfect Harmony! 👑
"""

import asyncio
import subprocess
import sys
import time
import signal
import os
from typing import List, Dict

class HyperFocusZoneAgentLauncher:
    """🚀 Launch ALL agent systems in coordination"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.active_processes = []
        self.shutdown_requested = False

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Shutdown signal received: {signum}")
        self.shutdown_requested = True

    async def launch_all_systems(self):
        """🚀 Launch ALL agent army systems in coordination"""
        print("🔥💪" * 25)
        print("🚀 LAUNCHING HYPERFOCUSZONE AGENT ARMY!")
        print("🎯 ALL SYSTEMS WILL WORK TOGETHER!")
        print("🥳 PARTY MODE WHEN WORK IS DONE!")
        print("🔥💪" * 25)

        # Launch sequence
        launch_sequence = [
            {
                'name': '🤖 Agent Army Command Portal',
                'script': 'broski_agent_army_command_portal.py',
                'priority': 1,
                'delay': 2
            },
            {
                'name': '🪖 Army Coordination Command',
                'script': 'broski_army_coordination_command.py',
                'priority': 1,
                'delay': 3
            },
            {
                'name': '🛡️ Security Fortress Portal',
                'script': 'broski_security_fortress_portal.py',
                'priority': 2,
                'delay': 2
            },
            {
                'name': '💰 Money Maker Portal',
                'script': 'broski_money_maker_portal.py',
                'priority': 2,
                'delay': 2
            },
            {
                'name': '🧠 Brain Data Engine',
                'script': 'broski_brain_data_engine.py',
                'priority': 2,
                'delay': 2
            },
            {
                'name': '🎯 Ultra Agent Commander',
                'script': 'ultra_agent_army_command_nexus.py',
                'priority': 1,
                'delay': 3
            },
            {
                'name': '🎼 Symphony Conductor',
                'script': 'hyperagent_symphony_conductor.py',
                'priority': 2,
                'delay': 2
            },
            {
                'name': '🔥 HyperFocusZone Coordinator',
                'script': 'hyperfocuszone_ultimate_agent_coordinator.py',
                'priority': 0,  # Launch this LAST to coordinate everyone
                'delay': 5
            }
        ]

        # Sort by priority (lower number = higher priority)
        launch_sequence.sort(key=lambda x: x['priority'])

        # Launch each system
        for system in launch_sequence:
            if self.shutdown_requested:
                break

            await self.launch_system(system)

            if system['delay'] > 0:
                print(f"⏳ Waiting {system['delay']} seconds for {system['name']} to stabilize...")
                await asyncio.sleep(system['delay'])

        if not self.shutdown_requested:
            print("\n🎉" * 30)
            print("✅ ALL AGENT SYSTEMS LAUNCHED SUCCESSFULLY!")
            print("🔥 HYPERFOCUSZONE MODE ACTIVATED!")
            print("🎯 NO AGENT WILL SIT IDLE!")
            print("🥳 PARTY MODE WHEN WORK IS DONE!")
            print("🎉" * 30)

            # Keep launcher running to monitor systems
            await self.monitor_systems()

    async def launch_system(self, system: Dict):
        """🚀 Launch individual system"""
        script_path = f"{self.base_path}/{system['script']}"

        if not os.path.exists(script_path):
            print(f"⚠️ {system['name']}: Script not found - {script_path}")
            return

        try:
            print(f"🚀 Launching {system['name']}...")

            # Launch process
            process = subprocess.Popen([
                sys.executable, script_path
            ],
            cwd=self.base_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )

            self.active_processes.append({
                'name': system['name'],
                'script': system['script'],
                'process': process,
                'start_time': time.time()
            })

            print(f"✅ {system['name']} launched! PID: {process.pid}")

        except Exception as e:
            print(f"❌ Failed to launch {system['name']}: {e}")

    async def monitor_systems(self):
        """📊 Monitor all launched systems"""
        print("📊 System monitoring activated...")

        while not self.shutdown_requested:
            try:
                # Check system health
                active_count = 0
                failed_systems = []

                for system_info in self.active_processes:
                    process = system_info['process']

                    if process.poll() is None:
                        # Process is still running
                        active_count += 1
                    else:
                        # Process has terminated
                        failed_systems.append(system_info)

                # Report status
                if len(self.active_processes) > 0:
                    print(f"\n📊 SYSTEM STATUS: {active_count}/{len(self.active_processes)} systems active")

                    if failed_systems:
                        print("⚠️ Failed systems detected:")
                        for failed in failed_systems:
                            print(f"   ❌ {failed['name']} (PID: {failed['process'].pid})")
                            # Attempt restart
                            await self.restart_system(failed)

                # Wait before next check
                await asyncio.sleep(30)

            except Exception as e:
                print(f"📊 Monitoring error: {e}")
                await asyncio.sleep(30)

    async def restart_system(self, failed_system: Dict):
        """🔄 Restart failed system"""
        try:
            print(f"🔄 Attempting to restart {failed_system['name']}...")

            script_path = f"{self.base_path}/{failed_system['script']}"

            # Launch new process
            new_process = subprocess.Popen([
                sys.executable, script_path
            ],
            cwd=self.base_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )

            # Update process info
            failed_system['process'] = new_process
            failed_system['start_time'] = time.time()

            print(f"✅ {failed_system['name']} restarted! New PID: {new_process.pid}")

        except Exception as e:
            print(f"❌ Failed to restart {failed_system['name']}: {e}")

    async def shutdown_all_systems(self):
        """🛑 Gracefully shutdown all systems"""
        print("\n🛑 Shutting down all agent systems...")

        for system_info in self.active_processes:
            try:
                process = system_info['process']

                if process.poll() is None:
                    print(f"🛑 Stopping {system_info['name']}...")

                    # Try graceful shutdown first
                    process.terminate()

                    # Wait a bit for graceful shutdown
                    await asyncio.sleep(3)

                    # Force kill if still running
                    if process.poll() is None:
                        print(f"💀 Force killing {system_info['name']}...")
                        process.kill()

            except Exception as e:
                print(f"❌ Error stopping {system_info['name']}: {e}")

        print("🛑 All systems shutdown complete!")

    async def run(self):
        """🚀 Main launcher execution"""
        try:
            await self.launch_all_systems()
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received...")
        finally:
            await self.shutdown_all_systems()


async def main():
    """🚀 Main launcher entry point"""
    print("🔥💪 HYPERFOCUSZONE AGENT ARMY LAUNCHER STARTING! 💪🔥")

    launcher = HyperFocusZoneAgentLauncher()
    await launcher.run()


if __name__ == "__main__":
    asyncio.run(main())