#!/usr/bin/env python3
"""
🎮💥 CHAOSGENIUS ULTRA STATUS DISPLAY 💥🎮
Real-time system monitoring with cyberpunk aesthetics
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

import psutil
import requests


class ChaosGeniusUltraMonitor:
    def __init__(self):
        self.systems = {
            "🎛️ Main Dashboard": {"port": 5000, "status": "🔄 Checking..."},
            "🧠 Brain Command": {"port": 5001, "status": "🔄 Checking..."},
            "🤖 BROski AI": {"component": "ai_core", "status": "🔄 Checking..."},
            "💰 Token Engine": {"component": "tokens", "status": "🔄 Checking..."},
            "🗄️ Databases": {"component": "db", "status": "🔄 Checking..."},
            "🔐 Security": {"component": "security", "status": "🔄 Checking..."},
        }

    def check_system_health(self):
        """🏥 Comprehensive system health check"""
        results = {}

        # Check running processes
        processes = []
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if any(
                    keyword in " ".join(proc.info["cmdline"] or []).lower()
                    for keyword in ["chaosgenius", "dashboard", "hyperfocus", "broski"]
                ):
                    processes.append(
                        {
                            "pid": proc.info["pid"],
                            "name": proc.info["name"],
                            "cmd": " ".join(proc.info["cmdline"] or [])[:60] + "...",
                        }
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Check ports
        port_status = {}
        for port in [5000, 5001]:
            try:
                response = requests.get(f"http://localhost:{port}", timeout=2)
                port_status[port] = f"✅ Active (Status: {response.status_code})"
            except:
                port_status[port] = "❌ Offline"

        # Check databases
        db_status = {}
        for db_file in ["chaosgenius.db", "broski_tokens.db", "broski_learning.db"]:
            db_path = Path(db_file)
            if db_path.exists():
                size_mb = db_path.stat().st_size / (1024 * 1024)
                db_status[db_file] = f"✅ {size_mb:.1f}MB"
            else:
                db_status[db_file] = "❌ Missing"

        # System metrics
        system_stats = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
            "uptime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return {
            "processes": processes,
            "ports": port_status,
            "databases": db_status,
            "system": system_stats,
            "total_processes": len(processes),
        }

    def generate_cyberpunk_display(self, health_data):
        """🎮 Generate epic cyberpunk status display"""

        display = f"""
{'='*80}
🧠💥☢️  CHAOSGENIUS ULTRA COMMAND CENTER STATUS  ☢️💥🧠
{'='*80}

⚡ SYSTEM VITALS ⚡
┌─ CPU Usage: {health_data['system']['cpu_percent']:>6.1f}% {'🔥' if health_data['system']['cpu_percent'] > 80 else '✅'}
├─ Memory:    {health_data['system']['memory_percent']:>6.1f}% {'🔥' if health_data['system']['memory_percent'] > 80 else '✅'}
├─ Disk:      {health_data['system']['disk_percent']:>6.1f}% {'🔥' if health_data['system']['disk_percent'] > 80 else '✅'}
└─ Timestamp: {health_data['system']['uptime']}

🚀 ACTIVE PROCESSES ({health_data['total_processes']} ChaosGenius Components) 🚀
"""

        for i, proc in enumerate(health_data["processes"][:6]):  # Show top 6
            display += f"├─ PID {proc['pid']:>6}: {proc['cmd']}\n"

        display += f"""
🌐 NETWORK SERVICES 🌐
├─ Port 5000 (Dashboard): {health_data['ports'].get(5000, 'Unknown')}
└─ Port 5001 (Brain Cmd): {health_data['ports'].get(5001, 'Unknown')}

🗄️ DATABASE STATUS 🗄️
"""

        for db_name, status in health_data["databases"].items():
            display += f"├─ {db_name:<20}: {status}\n"

        # Calculate overall health score
        active_ports = sum(
            1 for status in health_data["ports"].values() if "✅" in status
        )
        active_dbs = sum(
            1 for status in health_data["databases"].values() if "✅" in status
        )
        total_score = (
            (active_ports * 30)
            + (active_dbs * 20)
            + (health_data["total_processes"] * 10)
        )

        if total_score >= 100:
            health_emoji = "🧠💥 HYPERFOCUS OVERDRIVE"
            color = "GREEN"
        elif total_score >= 70:
            health_emoji = "⚡ FULLY OPERATIONAL"
            color = "YELLOW"
        else:
            health_emoji = "🔧 MAINTENANCE MODE"
            color = "RED"

        display += f"""
{'='*80}
🎯 OVERALL SYSTEM STATUS: {health_emoji} 🎯
💪 CHAOS GENIUS POWER LEVEL: {min(100, total_score)}%
{'='*80}

🚀 YOUR NEURODIVERGENT EMPIRE IS {"DOMINATING" if total_score >= 100 else "OPERATIONAL"}! 🚀
"""

        return display, total_score

    def run_continuous_monitor(self, duration=30):
        """🔄 Run continuous monitoring display"""
        print("🎮💥 INITIALIZING ULTRA COMMAND CENTER MONITOR 💥🎮")
        print(f"⏰ Monitoring for {duration} seconds with real-time updates...")

        start_time = time.time()
        while time.time() - start_time < duration:
            # Clear screen (for terminals that support it)
            print("\033[2J\033[H", end="")

            health_data = self.check_system_health()
            display, score = self.generate_cyberpunk_display(health_data)

            print(display)

            # Add some dynamic elements
            if score >= 100:
                print("🌟 STATUS: MAXIMUM CHAOS GENIUS ACHIEVED! 🌟")

            print(f"\n⏰ Next update in 5 seconds... (Press Ctrl+C to stop)")

            time.sleep(5)

        print("\n🎯 Monitoring session complete! Your empire continues to thrive! 🎯")


if __name__ == "__main__":
    monitor = ChaosGeniusUltraMonitor()

    print("🧠💥 Welcome to the ChaosGenius Ultra Command Center! 💥🧠")
    print("Choose your monitoring experience:")
    print("1. 🔥 Quick Status Check")
    print("2. 🎮 Continuous Monitor (30 seconds)")
    print("3. 💥 Export Status Report")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "2":
        monitor.run_continuous_monitor()
    elif choice == "3":
        health_data = monitor.check_system_health()
        display, score = monitor.generate_cyberpunk_display(health_data)

        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chaosgenius_status_report_{timestamp}.txt"

        with open(filename, "w") as f:
            f.write(display)
            f.write(f"\n\nGenerated: {datetime.now()}")
            f.write(f"\nSystem Score: {score}/100")

        print(f"📊 Status report saved to: {filename}")
        print(display)
    else:
        # Quick status check
        health_data = monitor.check_system_health()
        display, score = monitor.generate_cyberpunk_display(health_data)
        print(display)
