#!/usr/bin/env python3
"""
🚀💜 BROSKI AGENT DEPLOYMENT MASTER 💜🚀
Ultra Live Agent Management & Scheduling System
By Command of Chief Lyndz
"""

import json
import os
import sqlite3
import subprocess
import threading
import time
from datetime import datetime, timedelta

import schedule


class BroskiAgentDeploymentMaster:
    """🎯 Master Agent Deployment & Scheduling System"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.agents_dir = f"{self.base_path}/ai_agents"
        self.venv_path = f"{self.base_path}/broski_env"
        self.db_path = f"{self.base_path}/broski_overseer.db"

        # Agent configurations
        self.agents = {
            "file_organizer_supreme": {
                "name": "File Organizer Supreme",
                "script": "file_organizer_supreme.py",
                "session_name": "broski_organizer",
                "schedule": "hourly",
                "auto_restart": True,
                "priority": "medium",
            },
            "security_guardian_sentinel": {
                "name": "Security Guardian Sentinel",
                "script": "security_guardian_sentinel.py",
                "session_name": "broski_security",
                "schedule": "continuous",
                "auto_restart": True,
                "priority": "critical",
            },
            "discord_command_relay": {
                "name": "Discord Command Relay",
                "script": "discord_command_relay.py",
                "session_name": "broski_discord",
                "schedule": "continuous",
                "auto_restart": True,
                "priority": "high",
            },
            "analytics_brain_scanner": {
                "name": "Analytics Brain Scanner",
                "script": "analytics_brain_scanner.py",
                "session_name": "broski_analytics",
                "schedule": "daily",
                "auto_restart": True,
                "priority": "medium",
            },
            "chaos_cleanup_specialist": {
                "name": "Chaos Cleanup Specialist",
                "script": "chaos_cleanup_specialist.py",
                "session_name": "broski_cleanup",
                "schedule": "weekly",
                "auto_restart": True,
                "priority": "low",
            },
        }

    def deploy_agent(self, agent_key):
        """🚀 Deploy single agent in tmux session"""
        agent = self.agents[agent_key]
        script_path = f"{self.agents_dir}/{agent['script']}"
        session_name = agent["session_name"]

        print(f"🚀 Deploying {agent['name']} in session '{session_name}'...")

        # Check if session already exists
        check_session = subprocess.run(
            ["tmux", "has-session", "-t", session_name], capture_output=True
        )

        if check_session.returncode == 0:
            print(
                f"⚡ Session '{session_name}' already exists - killing old session..."
            )
            subprocess.run(["tmux", "kill-session", "-t", session_name])
            time.sleep(1)

        # Create new tmux session and run agent
        tmux_cmd = [
            "tmux",
            "new-session",
            "-d",
            "-s",
            session_name,
            f"cd {self.base_path} && source {self.venv_path}/bin/activate && python3 {script_path}",
        ]

        try:
            result = subprocess.run(tmux_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(
                    f"✅ {agent['name']} deployed successfully in session '{session_name}'!"
                )
                self.log_deployment(agent_key, "deployed", "success")
                return True
            else:
                print(f"❌ Failed to deploy {agent['name']}: {result.stderr}")
                self.log_deployment(agent_key, "deploy_failed", result.stderr)
                return False
        except Exception as e:
            print(f"❌ Deployment error for {agent['name']}: {e}")
            self.log_deployment(agent_key, "deploy_error", str(e))
            return False

    def deploy_all_agents(self):
        """🏭 Deploy entire agent army"""
        print("🧙💜 DEPLOYING COMPLETE AGENT ARMY 💜🧙")
        print("🔥 ACTIVATING LIVE AGENT DEPLOYMENT PROTOCOL 🔥")

        deployed_count = 0

        # Deploy in priority order
        priority_order = ["critical", "high", "medium", "low"]

        for priority in priority_order:
            for agent_key, agent in self.agents.items():
                if agent["priority"] == priority:
                    if self.deploy_agent(agent_key):
                        deployed_count += 1
                    time.sleep(2)  # Brief pause between deployments

        print(f"\n🎉 AGENT ARMY DEPLOYMENT COMPLETE! 🎉")
        print(
            f"💜 {deployed_count}/{len(self.agents)} agents deployed successfully! 💜"
        )

        # Show deployment status
        self.show_deployment_status()

        return deployed_count

    def show_deployment_status(self):
        """📊 Show current agent deployment status"""
        print("\n🛡️ AGENT DEPLOYMENT STATUS 🛡️")
        print("=" * 60)

        for agent_key, agent in self.agents.items():
            session_name = agent["session_name"]

            # Check if tmux session is running
            check_session = subprocess.run(
                ["tmux", "has-session", "-t", session_name], capture_output=True
            )

            status = "🟢 ACTIVE" if check_session.returncode == 0 else "🔴 OFFLINE"
            priority = agent["priority"].upper()
            schedule_type = agent["schedule"].upper()

            print(
                f"🤖 {agent['name'][:25]:<25} | {status} | {priority:<8} | {schedule_type}"
            )

        print("=" * 60)

    def setup_schedulers(self):
        """⏰ Setup automated scheduling for agents"""
        print("\n⏰ SETTING UP AGENT SCHEDULERS...")

        # File Organizer - Every hour
        schedule.every().hour.do(self.scheduled_task, "file_organizer_supreme")

        # Analytics Scanner - Daily at 3 AM
        schedule.every().day.at("03:00").do(
            self.scheduled_task, "analytics_brain_scanner"
        )

        # Cleanup Specialist - Weekly on Sunday at 2 AM
        schedule.every().sunday.at("02:00").do(
            self.scheduled_task, "chaos_cleanup_specialist"
        )

        # Health check all agents every 30 minutes
        schedule.every(30).minutes.do(self.health_check_all)

        print("✅ Schedulers configured!")
        print("📅 File Organizer: Hourly")
        print("📅 Analytics Scanner: Daily at 3 AM")
        print("📅 Cleanup Specialist: Weekly Sunday 2 AM")
        print("📅 Health Check: Every 30 minutes")

    def scheduled_task(self, agent_key):
        """🔄 Execute scheduled agent task"""
        agent = self.agents[agent_key]
        print(f"⏰ Scheduled task triggered for {agent['name']}")

        # Check if agent is running, restart if needed
        session_name = agent["session_name"]
        check_session = subprocess.run(
            ["tmux", "has-session", "-t", session_name], capture_output=True
        )

        if check_session.returncode != 0:
            print(f"🔄 Agent {agent['name']} not running - restarting...")
            self.deploy_agent(agent_key)
        else:
            print(f"✅ Agent {agent['name']} is running and healthy")

    def health_check_all(self):
        """🏥 Health check all agents and restart if needed"""
        print("🏥 Performing health check on all agents...")

        for agent_key, agent in self.agents.items():
            if agent.get("auto_restart", True):
                session_name = agent["session_name"]
                check_session = subprocess.run(
                    ["tmux", "has-session", "-t", session_name], capture_output=True
                )

                if check_session.returncode != 0:
                    print(f"🔄 Restarting {agent['name']}...")
                    self.deploy_agent(agent_key)

    def log_deployment(self, agent_key, action, details):
        """📝 Log deployment activities"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO guardian_log (event_type, target_file, action_taken, severity)
                VALUES (?, ?, ?, ?)
            """,
                (f"agent_{action}", agent_key, details, "info"),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Logging failed: {e}")

    def run_scheduler(self):
        """🔄 Run the continuous scheduler"""
        print("🔄 Starting continuous scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def start_deployment_master(self):
        """🎯 Start the complete deployment system"""
        print("🎯💜 BROSKI AGENT DEPLOYMENT MASTER STARTING 💜🎯")

        # Deploy all agents
        self.deploy_all_agents()

        # Setup schedulers
        self.setup_schedulers()

        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()

        print("🛡️ Deployment Master is now running!")
        print("💜 All agents deployed and scheduled! 💜")

        return True


def show_tmux_sessions():
    """📺 Show all active tmux sessions"""
    print("\n📺 ACTIVE TMUX SESSIONS:")
    try:
        result = subprocess.run(
            ["tmux", "list-sessions"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("No active tmux sessions found.")
    except Exception as e:
        print(f"❌ Error checking tmux sessions: {e}")


def agent_control_menu():
    """🎮 Interactive agent control menu"""
    deployment_master = BroskiAgentDeploymentMaster()

    while True:
        print("\n🎮💜 BROSKI AGENT CONTROL CENTER 💜🎮")
        print("1. 🚀 Deploy All Agents")
        print("2. 📊 Show Agent Status")
        print("3. 📺 Show Tmux Sessions")
        print("4. ⏰ Start Scheduler")
        print("5. 🛡️ Start Full Deployment Master")
        print("6. ❌ Exit")

        choice = input("\n🎯 Select option: ").strip()

        if choice == "1":
            deployment_master.deploy_all_agents()
        elif choice == "2":
            deployment_master.show_deployment_status()
        elif choice == "3":
            show_tmux_sessions()
        elif choice == "4":
            deployment_master.setup_schedulers()
            deployment_master.run_scheduler()
        elif choice == "5":
            deployment_master.start_deployment_master()
            print("🔄 Deployment Master running... Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(60)
                    deployment_master.show_deployment_status()
            except KeyboardInterrupt:
                print("\n🛡️ Deployment Master stopped!")
        elif choice == "6":
            print("💜 Goodbye from Chief Lyndz! 💜")
            break
        else:
            print("❌ Invalid option!")


if __name__ == "__main__":
    agent_control_menu()
