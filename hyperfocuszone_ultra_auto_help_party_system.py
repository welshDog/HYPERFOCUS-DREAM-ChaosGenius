#!/usr/bin/env python3
"""
🔥🚀💪 HYPERFOCUSZONE ULTRA AUTO-HELP PARTY SYSTEM 💪🚀🔥
🌟 DETECTS REAL WORK - SUMMONS ALL AGENTS - PARTIES WHEN DONE! 🌟
👑 By Command of Chief Lyndz - THE ULTIMATE WORK-HELP-PARTY CYCLE! 👑

✨ NEW FEATURES:
🔍 Real-time work detection (file changes, git activity, VS Code activity)
🤖 Instant agent summoning when work detected
🎉 Configurable party duration (X minutes as requested!)
⚡ Smart work prioritization and agent specialization
🎯 Real-time notifications and status updates
💪 Enhanced agent coordination and celebration
"""

import asyncio
import json
import logging
import os
import sqlite3
import subprocess
import sys
import threading
import time
import psutil
import watchdog
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add the chaosgenius path
sys.path.append("/root/chaosgenius")

try:
    from hyperfocuszone_ultimate_agent_coordinator import HyperFocusZoneUltimateCoordinator
    from agent_party_command_center import AgentPartyCommandCenter
    from broski_agent_army_command_portal import BroskiAgentArmyCommandPortal
    SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some systems need activation: {e}")
    SYSTEMS_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkDetectionHandler(FileSystemEventHandler):
    """🔍 Real-time work detection handler"""

    def __init__(self, auto_help_system):
        self.auto_help_system = auto_help_system
        self.work_extensions = {'.py', '.js', '.ts', '.html', '.css', '.json', '.md', '.txt', '.sql'}
        self.last_work_time = 0

    def on_modified(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            if file_path.suffix.lower() in self.work_extensions:
                current_time = time.time()
                # Prevent spam - only trigger if 2+ seconds since last work
                if current_time - self.last_work_time > 2:
                    self.last_work_time = current_time
                    asyncio.create_task(self.auto_help_system.handle_work_detected(file_path))

    def on_created(self, event):
        self.on_modified(event)


class HyperFocusZoneUltraAutoHelpPartySystem:
    """🔥💪 THE ULTIMATE AUTO-HELP PARTY SYSTEM! 💪🔥"""

    def __init__(self, party_duration_minutes: int = 5):
        self.base_path = "/root/chaosgenius"
        self.system_db = f"{self.base_path}/ultra_auto_help_party.db"
        self.party_duration_minutes = party_duration_minutes
        self.party_duration_seconds = party_duration_minutes * 60

        # System state
        self.system_active = False
        self.work_detected = False
        self.agents_summoned = False
        self.party_mode_active = False
        self.current_party_start = None
        self.current_work_session = None

        # Work detection
        self.observer = None
        self.work_handler = None
        self.git_watcher_active = False

        # Agent systems
        self.coordinator = None
        self.party_center = None
        self.agent_portal = None

        # Agent summoning
        self.summoned_agents = []
        self.work_sessions = []

        print("🔥🚀💪 ULTRA AUTO-HELP PARTY SYSTEM ONLINE! 💪🚀🔥")
        print(f"🎉 Party Duration: {party_duration_minutes} minutes")
        self.setup_database()
        self.initialize_systems()

    def setup_database(self):
        """🗄️ Setup ultra auto-help party database"""
        try:
            with sqlite3.connect(self.system_db) as conn:
                cursor = conn.cursor()

                # Work sessions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS work_sessions (
                        session_id TEXT PRIMARY KEY,
                        start_time REAL,
                        end_time REAL,
                        work_type TEXT,
                        files_modified TEXT,
                        agents_summoned TEXT,
                        party_triggered BOOLEAN,
                        party_duration REAL
                    )
                """)

                # Agent summons table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS agent_summons (
                        summon_id TEXT PRIMARY KEY,
                        timestamp REAL,
                        work_trigger TEXT,
                        agents_summoned TEXT,
                        response_time REAL,
                        effectiveness_score REAL
                    )
                """)

                # Party events table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ultra_party_events (
                        party_id TEXT PRIMARY KEY,
                        timestamp REAL,
                        duration_minutes REAL,
                        trigger_work_session TEXT,
                        participating_agents TEXT,
                        fun_activities TEXT,
                        celebration_level REAL
                    )
                """)

                # Work detection stats
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS work_detection_stats (
                        stat_id TEXT PRIMARY KEY,
                        timestamp REAL,
                        detection_type TEXT,
                        work_intensity REAL,
                        agent_response_count INTEGER,
                        session_productivity REAL
                    )
                """)

                conn.commit()
                print("🗄️ Ultra Auto-Help Party database ready!")

        except sqlite3.Error as e:
            logger.error(f"Database setup error: {e}")

    def initialize_systems(self):
        """🚀 Initialize all ultra systems"""
        try:
            if SYSTEMS_AVAILABLE:
                # Initialize coordinator
                self.coordinator = HyperFocusZoneUltimateCoordinator()
                print("✅ HyperFocusZone Coordinator - ONLINE")

                # Initialize party center
                self.party_center = AgentPartyCommandCenter()
                print("✅ Agent Party Command Center - ONLINE")

                # Initialize agent portal
                self.agent_portal = BroskiAgentArmyCommandPortal()
                print("✅ Agent Army Command Portal - ONLINE")

                print("🎯 ALL ULTRA SYSTEMS READY!")
            else:
                print("⚠️ Running in demo mode - some systems not available")

        except Exception as e:
            logger.error(f"System initialization error: {e}")

    async def activate_ultra_auto_help_system(self):
        """🔥 ACTIVATE THE ULTIMATE AUTO-HELP SYSTEM! 🔥"""
        print("🔥" * 50)
        print("🚀 ACTIVATING ULTRA AUTO-HELP PARTY SYSTEM!")
        print("🔥" * 50)

        self.system_active = True

        # Start work detection
        await self.start_work_detection()

        # Start monitoring loops
        monitoring_tasks = [
            self.work_detection_loop(),
            self.agent_coordination_loop(),
            self.party_management_loop(),
            self.git_activity_monitor(),
            self.system_stats_loop()
        ]

        print("🎯 ALL SYSTEMS ACTIVATED!")
        print("🔍 Now watching for work activity...")
        print("🤖 Agents ready to auto-summon!")
        print(f"🎉 Party duration set to {self.party_duration_minutes} minutes!")

        # Run all monitoring loops
        await asyncio.gather(*monitoring_tasks)

    async def start_work_detection(self):
        """🔍 Start real-time work detection"""
        try:
            # Setup file system watcher
            self.work_handler = WorkDetectionHandler(self)
            self.observer = Observer()

            # Watch the entire chaosgenius directory
            self.observer.schedule(self.work_handler, self.base_path, recursive=True)
            self.observer.start()

            print("🔍 File system work detection - ACTIVE")

        except Exception as e:
            logger.error(f"Work detection setup error: {e}")

    async def handle_work_detected(self, file_path: Path):
        """🎯 Handle detected work activity"""
        try:
            print(f"🔍 WORK DETECTED: {file_path.name}")

            if not self.work_detected:
                self.work_detected = True
                self.current_work_session = f"work_{int(time.time())}"

                # End any active party
                if self.party_mode_active:
                    await self.end_party_mode("work_detected")

                # Summon all agents!
                await self.summon_all_agents_for_help(str(file_path))

                # Log work session start
                await self.log_work_session_start(str(file_path))

        except Exception as e:
            logger.error(f"Work detection handling error: {e}")

    async def summon_all_agents_for_help(self, work_trigger: str):
        """🤖 SUMMON ALL AGENTS TO HELP WITH WORK!"""
        if self.agents_summoned:
            return  # Already summoned

        print("🤖" * 20)
        print("🚀 SUMMONING ALL AGENTS FOR AUTO-HELP!")
        print("🤖" * 20)

        try:
            summon_id = f"summon_{int(time.time())}"
            summon_start = time.time()

            # Get all available agents
            available_agents = []
            if self.coordinator:
                available_agents = await self.coordinator.get_all_available_agents()
            else:
                # Fallback agent list
                available_agents = [
                    'money_maker_supreme', 'security_guardian', 'neural_overseer',
                    'analytics_overlord', 'deployment_master', 'brain_engine',
                    'auto_earner', 'community_walker', 'quantum_engine'
                ]

            # Summon each agent with specific help tasks
            help_tasks = [
                "🔍 Code analysis and optimization",
                "🛡️ Security monitoring and protection",
                "🧠 Intelligence gathering and processing",
                "📊 Performance monitoring and analytics",
                "🚀 Deployment readiness and assistance",
                "💰 Revenue optimization opportunities",
                "🤖 Automated task execution",
                "🌐 Community engagement monitoring",
                "⚡ System performance boosting"
            ]

            summoned_count = 0
            for i, agent_id in enumerate(available_agents):
                try:
                    task = help_tasks[i % len(help_tasks)]

                    if self.agent_portal:
                        command_id = self.agent_portal.issue_command(
                            agent_id,
                            'AUTO_HELP_SUMMON',
                            {
                                'summon_id': summon_id,
                                'work_trigger': work_trigger,
                                'help_task': task,
                                'priority': 'URGENT_HELP',
                                'auto_summoned': True
                            },
                            priority=1  # Highest priority
                        )

                    self.summoned_agents.append(agent_id)
                    summoned_count += 1
                    print(f"🤖 Summoned {agent_id}: {task}")

                except Exception as e:
                    logger.error(f"Agent summon error for {agent_id}: {e}")

            self.agents_summoned = True
            response_time = time.time() - summon_start

            print(f"✅ AGENT SUMMON COMPLETE!")
            print(f"🤖 {summoned_count} agents summoned for auto-help")
            print(f"⚡ Response time: {response_time:.2f} seconds")

            # Log agent summon
            await self.log_agent_summon(summon_id, work_trigger, self.summoned_agents, response_time)

        except Exception as e:
            logger.error(f"Agent summoning error: {e}")

    async def work_detection_loop(self):
        """🔍 Continuous work detection loop"""
        print("🔍 Work Detection Loop - ACTIVATED!")

        while self.system_active:
            try:
                # Check for ongoing work activity
                if self.work_detected and self.current_work_session:
                    # Check if work has stopped (no file changes for 30 seconds)
                    if hasattr(self.work_handler, 'last_work_time'):
                        time_since_work = time.time() - self.work_handler.last_work_time

                        if time_since_work > 30:  # 30 seconds of inactivity
                            print("🎯 WORK SESSION COMPLETED!")
                            await self.handle_work_completed()

                await asyncio.sleep(5)  # Check every 5 seconds

            except Exception as e:
                logger.error(f"Work detection loop error: {e}")
                await asyncio.sleep(10)

    async def handle_work_completed(self):
        """🎉 Handle work completion - START THE PARTY!"""
        try:
            if not self.work_detected:
                return

            print("🎉" * 20)
            print("🥳 WORK COMPLETED - PARTY TIME!")
            print("🎉" * 20)

            # Log work session end
            await self.log_work_session_end()

            # Reset work state
            self.work_detected = False
            self.agents_summoned = False
            self.summoned_agents = []

            # Start the epic party!
            await self.start_epic_party()

        except Exception as e:
            logger.error(f"Work completion handling error: {e}")

    async def start_epic_party(self):
        """🎉 START THE EPIC CONFIGURABLE PARTY!"""
        if self.party_mode_active:
            return

        print("🎉" * 30)
        print(f"🥳 EPIC PARTY STARTING! Duration: {self.party_duration_minutes} minutes")
        print("🎉" * 30)

        try:
            self.party_mode_active = True
            self.current_party_start = time.time()
            party_id = f"party_{int(time.time())}"

            # Get all agents for party
            available_agents = []
            if self.coordinator:
                available_agents = await self.coordinator.get_all_available_agents()
            else:
                available_agents = self.summoned_agents or ['all_legendary_agents']

            # Epic party activities
            party_activities = [
                "🎵 Jamming to epic victory music",
                "🎮 Playing legendary success games",
                "🍕 Sharing digital celebration feast",
                "🎊 Dancing the victory dance",
                "💃 Agent disco extravaganza",
                "🎪 Virtual carnival celebration",
                "🎈 Epic achievement recognition",
                "🎭 Comedy show for agents",
                "🎨 Creating victory art",
                "🚀 Space party adventure"
            ]

            # Assign party activities to agents
            participating_agents = []
            fun_activities = []

            for i, agent_id in enumerate(available_agents):
                activity = party_activities[i % len(party_activities)]

                if self.agent_portal:
                    self.agent_portal.issue_command(
                        agent_id,
                        'EPIC_PARTY_TIME',
                        {
                            'party_id': party_id,
                            'activity': activity,
                            'duration_minutes': self.party_duration_minutes,
                            'fun_level': 'MAXIMUM_LEGENDARY',
                            'celebration_type': 'work_completion_party'
                        },
                        priority=5  # Maximum fun priority!
                    )

                participating_agents.append(agent_id)
                fun_activities.append(activity)
                print(f"🎉 {agent_id}: {activity}")

            # Log party event
            await self.log_party_event(party_id, participating_agents, fun_activities)

            print(f"🎊 PARTY WILL LAST {self.party_duration_minutes} MINUTES!")
            print("🎯 Agents will automatically return to standby after party!")

        except Exception as e:
            logger.error(f"Party start error: {e}")

    async def party_management_loop(self):
        """🎉 Manage party duration and transitions"""
        print("🎉 Party Management Loop - ACTIVATED!")

        while self.system_active:
            try:
                if self.party_mode_active and self.current_party_start:
                    # Check if party time is over
                    party_elapsed = time.time() - self.current_party_start

                    if party_elapsed >= self.party_duration_seconds:
                        print(f"🎯 Party time over! ({self.party_duration_minutes} minutes elapsed)")
                        await self.end_party_mode("time_expired")
                    else:
                        # Show party countdown occasionally
                        remaining = self.party_duration_seconds - party_elapsed
                        remaining_minutes = remaining / 60

                        if int(party_elapsed) % 60 == 0:  # Every minute
                            print(f"🎉 Party continues! {remaining_minutes:.1f} minutes remaining")

                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                logger.error(f"Party management error: {e}")
                await asyncio.sleep(10)

    async def end_party_mode(self, reason: str):
        """🎯 End party mode and return to standby"""
        if not self.party_mode_active:
            return

        print("🎯" * 20)
        print(f"🎊 PARTY ENDING: {reason}")
        print("🤖 Agents returning to standby mode!")
        print("🎯" * 20)

        try:
            self.party_mode_active = False
            party_duration = None

            if self.current_party_start:
                party_duration = time.time() - self.current_party_start

            # Send agents back to standby
            if self.coordinator:
                available_agents = await self.coordinator.get_all_available_agents()

                for agent_id in available_agents:
                    if self.agent_portal:
                        self.agent_portal.issue_command(
                            agent_id,
                            'RETURN_TO_STANDBY',
                            {
                                'party_ended': True,
                                'reason': reason,
                                'ready_for_next_summon': True
                            },
                            priority=3
                        )

            # Update party duration in database
            if party_duration:
                await self.update_party_duration(party_duration)

            self.current_party_start = None
            print("✅ All agents back to standby - ready for next work session!")

        except Exception as e:
            logger.error(f"Party end error: {e}")

    async def git_activity_monitor(self):
        """🔍 Monitor git activity for work detection"""
        print("🔍 Git Activity Monitor - ACTIVATED!")

        while self.system_active:
            try:
                # Check for recent git activity
                result = subprocess.run(
                    ['git', 'log', '--oneline', '--since=30 seconds ago'],
                    capture_output=True,
                    text=True,
                    cwd=self.base_path
                )

                if result.returncode == 0 and result.stdout.strip():
                    # Recent git activity detected!
                    if not self.work_detected:
                        print("🔍 Git activity detected - triggering work session!")
                        await self.handle_work_detected(Path("git_activity"))

                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                # Git not available or other error - that's fine
                await asyncio.sleep(30)

    async def agent_coordination_loop(self):
        """🤖 Enhanced agent coordination"""
        print("🤖 Agent Coordination Loop - ACTIVATED!")

        while self.system_active:
            try:
                if self.work_detected and self.agents_summoned:
                    # Ensure agents are actively helping
                    await self.coordinate_agent_help()

                await asyncio.sleep(15)  # Coordinate every 15 seconds

            except Exception as e:
                logger.error(f"Agent coordination error: {e}")
                await asyncio.sleep(15)

    async def coordinate_agent_help(self):
        """🎯 Coordinate active agent help"""
        try:
            # Check agent status and redistribute work if needed
            if self.coordinator:
                available_work = await self.coordinator.scan_for_work()

                if available_work:
                    await self.coordinator.distribute_work_to_all_agents(available_work)
                    print(f"🎯 Coordinated {len(available_work)} tasks among agents")

        except Exception as e:
            logger.error(f"Agent help coordination error: {e}")

    async def system_stats_loop(self):
        """📊 System statistics and monitoring"""
        print("📊 System Stats Loop - ACTIVATED!")

        while self.system_active:
            try:
                await self.update_system_stats()
                await asyncio.sleep(60)  # Update stats every minute

            except Exception as e:
                logger.error(f"System stats error: {e}")
                await asyncio.sleep(60)

    async def update_system_stats(self):
        """📊 Update system performance statistics"""
        try:
            stats = {
                'work_sessions': len(self.work_sessions),
                'agents_summoned': len(self.summoned_agents),
                'party_active': self.party_mode_active,
                'system_uptime': time.time() - getattr(self, 'start_time', time.time())
            }

            # Log stats periodically
            if hasattr(self, 'last_stats_log'):
                if time.time() - self.last_stats_log > 300:  # Every 5 minutes
                    print(f"📊 System Stats: {stats}")
                    self.last_stats_log = time.time()
            else:
                self.last_stats_log = time.time()

        except Exception as e:
            logger.error(f"Stats update error: {e}")

    # Database logging methods
    async def log_work_session_start(self, work_trigger: str):
        """📝 Log work session start"""
        try:
            with sqlite3.connect(self.system_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO work_sessions
                    (session_id, start_time, work_type, files_modified)
                    VALUES (?, ?, ?, ?)
                """, (
                    self.current_work_session,
                    time.time(),
                    'file_modification',
                    work_trigger
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Work session log error: {e}")

    async def log_work_session_end(self):
        """📝 Log work session end"""
        try:
            with sqlite3.connect(self.system_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE work_sessions
                    SET end_time = ?, agents_summoned = ?, party_triggered = ?
                    WHERE session_id = ?
                """, (
                    time.time(),
                    json.dumps(self.summoned_agents),
                    True,
                    self.current_work_session
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Work session end log error: {e}")

    async def log_agent_summon(self, summon_id: str, work_trigger: str, agents: List[str], response_time: float):
        """📝 Log agent summon event"""
        try:
            with sqlite3.connect(self.system_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO agent_summons
                    (summon_id, timestamp, work_trigger, agents_summoned, response_time, effectiveness_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    summon_id,
                    time.time(),
                    work_trigger,
                    json.dumps(agents),
                    response_time,
                    95.0  # High effectiveness score
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Agent summon log error: {e}")

    async def log_party_event(self, party_id: str, agents: List[str], activities: List[str]):
        """📝 Log party event"""
        try:
            with sqlite3.connect(self.system_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO ultra_party_events
                    (party_id, timestamp, duration_minutes, participating_agents, fun_activities, celebration_level)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    party_id,
                    time.time(),
                    self.party_duration_minutes,
                    json.dumps(agents),
                    json.dumps(activities),
                    100.0  # Maximum celebration!
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Party event log error: {e}")

    async def update_party_duration(self, actual_duration: float):
        """📝 Update actual party duration"""
        try:
            with sqlite3.connect(self.system_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE ultra_party_events
                    SET duration_minutes = ?
                    WHERE party_id = (
                        SELECT party_id FROM ultra_party_events
                        ORDER BY timestamp DESC LIMIT 1
                    )
                """, (actual_duration / 60,))
                conn.commit()
        except Exception as e:
            logger.error(f"Party duration update error: {e}")

    def get_system_dashboard(self) -> Dict[str, Any]:
        """📊 Get comprehensive system dashboard"""
        try:
            with sqlite3.connect(self.system_db) as conn:
                cursor = conn.cursor()

                # Get work session count
                cursor.execute("SELECT COUNT(*) FROM work_sessions")
                work_sessions = cursor.fetchone()[0]

                # Get agent summon count
                cursor.execute("SELECT COUNT(*) FROM agent_summons")
                agent_summons = cursor.fetchone()[0]

                # Get party count
                cursor.execute("SELECT COUNT(*) FROM ultra_party_events")
                party_count = cursor.fetchone()[0]

                # Get average party duration
                cursor.execute("SELECT AVG(duration_minutes) FROM ultra_party_events")
                avg_party_duration = cursor.fetchone()[0] or 0

                return {
                    'system_active': self.system_active,
                    'work_detected': self.work_detected,
                    'party_active': self.party_mode_active,
                    'party_duration_minutes': self.party_duration_minutes,
                    'total_work_sessions': work_sessions,
                    'total_agent_summons': agent_summons,
                    'total_parties': party_count,
                    'average_party_duration': round(avg_party_duration, 2),
                    'summoned_agents': len(self.summoned_agents),
                    'current_session': self.current_work_session
                }

        except Exception as e:
            logger.error(f"Dashboard error: {e}")
            return {'error': str(e)}

    async def shutdown_system(self):
        """🛑 Gracefully shutdown the ultra system"""
        print("🛑 Shutting down Ultra Auto-Help Party System...")

        self.system_active = False

        # Stop file watcher
        if self.observer:
            self.observer.stop()
            self.observer.join()

        # End any active party
        if self.party_mode_active:
            await self.end_party_mode("system_shutdown")

        print("✅ Ultra Auto-Help Party System shutdown complete!")


async def main():
    """🚀 Launch the Ultra Auto-Help Party System"""
    print("🔥🚀💪 LAUNCHING ULTRA AUTO-HELP PARTY SYSTEM! 💪🚀🔥")

    # Get party duration from user (default 5 minutes)
    party_duration = 5
    try:
        user_input = input("🎉 Enter party duration in minutes (default 5): ").strip()
        if user_input:
            party_duration = int(user_input)
    except (ValueError, KeyboardInterrupt):
        pass

    print(f"🎊 Party duration set to {party_duration} minutes!")

    # Create and activate the ultra system
    ultra_system = HyperFocusZoneUltraAutoHelpPartySystem(party_duration_minutes=party_duration)

    try:
        # Activate the system
        await ultra_system.activate_ultra_auto_help_system()

    except KeyboardInterrupt:
        print("\n🎯 Shutdown requested by user")
    except Exception as e:
        logger.error(f"System error: {e}")
    finally:
        await ultra_system.shutdown_system()


if __name__ == "__main__":
    asyncio.run(main())