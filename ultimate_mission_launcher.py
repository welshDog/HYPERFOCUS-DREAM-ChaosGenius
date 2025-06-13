#!/usr/bin/env python3
"""
🎯🔥 ULTIMATE CHAOS GENIUS MISSION LAUNCHER 🔥🎯
Master controller for all 4 NEXT MISSION OPTIONS!
Power of 10,000 keyboard warriors at your command!
"""

import os
import subprocess
import sys
import time
from datetime import datetime


class UltimateMissionLauncher:
    def __init__(self):
        self.missions = {
            "1": {
                "name": "AGENT WARFARE SIMULATION 💣",
                "script": "agent_warfare_simulation.py",
                "description": "Unleash the full Agent Army in synchronized task force blitz!",
            },
            "2": {
                "name": "ULTRA DISCORD DEPLOYMENT WAVE 🎙️",
                "script": "ultra_discord_deployment_wave.py",
                "description": "BROski Bot with welcome magic, role assignment, and weekly dopamine boosters!",
            },
            "3": {
                "name": "CLOAKED CAVE LAUNCHPAD 🚀",
                "script": "cloaked_cave_launchpad.py",
                "description": "Auto-open VSCode, launch Flask, ping Discord, run task previews!",
            },
            "4": {
                "name": "DIGITAL UNIVERSE EXPANSION 🌌",
                "script": "digital_universe_expansion.py",
                "description": "Neuro Stars Map + Agent Army XP + BROski$ Token Economy!",
            },
            "ALL": {
                "name": "FULL DEPLOYMENT SEQUENCE 🌀",
                "script": "ALL",
                "description": "Launch ALL systems in perfect harmony!",
            },
        }

    def display_mission_menu(self):
        """Display the epic mission selection menu"""
        print("\n" + "=" * 70)
        print("🎯🔥 CHAOS GENIUS ULTIMATE MISSION LAUNCHER 🔥🎯")
        print("⚡ Power of 10,000 keyboard warriors awaits your command! ⚡")
        print("=" * 70)

        for key, mission in self.missions.items():
            print(f"\n[{key}] {mission['name']}")
            print(f"    📝 {mission['description']}")

        print("\n" + "=" * 70)
        print("💡 Choose your mission number (1-4) or 'ALL' for full deployment!")
        print("🚀 Type 'exit' to return to the cave...")

    def launch_mission(self, choice):
        """Launch the selected mission"""
        if choice.upper() == "EXIT":
            print("🕋 Returning to the cave... See you space cowboy! 🌌")
            return False

        if choice.upper() == "ALL":
            return self.launch_all_missions()

        if choice in self.missions and choice != "ALL":
            mission = self.missions[choice]
            print(f"\n🚀 LAUNCHING: {mission['name']}")
            print(f"📝 {mission['description']}")
            print("⚡ Initializing systems...")

            try:
                # Make script executable
                script_path = f"/root/chaosgenius/{mission['script']}"
                subprocess.run(["chmod", "+x", script_path], check=True)

                # Launch the mission
                result = subprocess.run(
                    [sys.executable, script_path],
                    cwd="/root/chaosgenius",
                    capture_output=False,
                )

                if result.returncode == 0:
                    print(f"✅ {mission['name']} completed successfully!")
                else:
                    print(
                        f"⚠️ {mission['name']} encountered some turbulence but may have completed."
                    )

            except Exception as e:
                print(f"❌ Error launching {mission['name']}: {e}")

        else:
            print("🔧 Invalid mission code! Please choose 1-4 or 'ALL'")

        return True

    def launch_all_missions(self):
        """🌀 FULL DEPLOYMENT SEQUENCE - Launch all systems!"""
        print("\n🌀💥 INITIATING FULL DEPLOYMENT SEQUENCE 💥🌀")
        print("🚀 Deploying all 4 mission systems in perfect harmony!")

        sequence = ["4", "1", "3", "2"]  # Strategic deployment order

        for i, mission_id in enumerate(sequence, 1):
            mission = self.missions[mission_id]
            print(f"\n⚡ STEP {i}/4: Deploying {mission['name']}")
            time.sleep(2)  # Tactical delay

            try:
                script_path = f"/root/chaosgenius/{mission['script']}"
                subprocess.run(["chmod", "+x", script_path], check=True)

                # Launch in background for most, foreground for cave launchpad
                if mission_id == "3":  # Cave launchpad - interactive
                    subprocess.run(
                        [sys.executable, script_path], cwd="/root/chaosgenius"
                    )
                else:
                    subprocess.Popen(
                        [sys.executable, script_path], cwd="/root/chaosgenius"
                    )

                print(f"✅ {mission['name']} deployed!")

            except Exception as e:
                print(f"⚠️ {mission['name']} deployment encountered turbulence: {e}")

        print("\n🏆💥 FULL DEPLOYMENT SEQUENCE COMPLETE! 💥🏆")
        print("🌌 The ChaosGenius Universe is now fully operational!")
        print("⚡ All systems online and ready for maximum productivity!")

        return True


def main():
    """Main launcher loop"""
    launcher = UltimateMissionLauncher()

    print("🌀🕋 ULTIMATE CHAOS GENIUS SYSTEM ONLINE 🕋🌀")

    while True:
        launcher.display_mission_menu()
        choice = input("\n🎯 Enter your mission choice: ").strip()

        if not launcher.launch_mission(choice):
            break

        print("\n⚡ Ready for next mission deployment!")
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
