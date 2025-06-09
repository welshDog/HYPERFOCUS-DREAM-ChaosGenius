#!/usr/bin/env python3
"""
🚀🔥💜 HYPERFOCUS ZONE LIVE MONITORING DASHBOARD 💜🔥🚀
Real-time launch monitoring and visitor tracking for hyperfocuszone.com
WOOP WOOP - TRACKING THE REVOLUTION!
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

import psutil
import requests


class HyperfocusZoneLiveMonitor:
    def __init__(self):
        self.domain = "hyperfocuszone.com"
        self.local_server = "localhost:5000"  # Fixed: Use actual dashboard port
        self.local_api_endpoint = "http://localhost:5000/api/status"  # ChaosGenius API
        self.start_time = datetime.now()
        self.stats = {
            "dns_checks": 0,
            "successful_connections": 0,
            "failed_connections": 0,
            "first_live_time": None,
            "uptime_percentage": 0,
            "response_times": [],
            "server_status": "Starting...",
            "dashboard_responses": 0,
            "api_responses": 0,
        }

    def check_dns_resolution(self):
        """Check if DNS has propagated"""
        try:
            result = subprocess.run(
                ["nslookup", self.domain], capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            print(f"DNS check error: {e}")
            return False

    def test_domain_connection(self):
        """Test if domain is responding"""
        try:
            start_time = time.time()
            response = requests.get(
                f"http://{self.domain}", timeout=10, allow_redirects=True
            )
            response_time = time.time() - start_time
            self.stats["response_times"].append(response_time)
            return response.status_code in [200, 301, 302, 404]
        except Exception as e:
            return False

    def test_production_server(self):
        """Test local ChaosGenius dashboard"""
        try:
            # Test main dashboard
            dashboard_response = requests.get(f"http://{self.local_server}", timeout=5)
            dashboard_ok = dashboard_response.status_code in [200, 301, 302]

            if dashboard_ok:
                self.stats["dashboard_responses"] += 1

            # Test API endpoint
            api_response = requests.get(self.local_api_endpoint, timeout=5)
            api_ok = api_response.status_code in [200, 301, 302]

            if api_ok:
                self.stats["api_responses"] += 1

            return dashboard_ok and api_ok
        except Exception as e:
            return False

    def get_server_stats(self):
        """Get server resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": f"{memory.available / (1024**3):.1f}GB",
                "disk_usage": disk.percent,
                "disk_free": f"{disk.free / (1024**3):.1f}GB",
                "load_average": os.getloadavg()[0] if hasattr(os, "getloadavg") else 0,
            }
        except Exception as e:
            return {"error": f"Could not get system stats: {e}"}

    def check_chaosgenius_processes(self):
        """Check ChaosGenius processes"""
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            processes = []

            for line in result.stdout.split("\n"):
                if any(
                    keyword in line.lower()
                    for keyword in ["dashboard_api", "chaosgenius", "gunicorn"]
                ):
                    if "python" in line:
                        processes.append(line.split()[1])  # Get PID

            return len(processes), processes
        except Exception as e:
            return 0, []

    def display_status(self, iteration):
        """Display current monitoring status"""
        current_time = datetime.now().strftime("%H:%M:%S")

        # Clear screen for live updates
        os.system("clear" if os.name == "posix" else "cls")

        print("🚀🔥💜" + "=" * 60 + "💜🔥🚀")
        print("     HYPERFOCUS ZONE LIVE LAUNCH MONITORING")
        print("     WOOP WOOP - NEURODIVERGENT REVOLUTION TRACKER!")
        print("🚀🔥💜" + "=" * 60 + "💜🔥🚀")
        print()

        # Test all services
        dns_resolved = self.check_dns_resolution()
        domain_live = self.test_domain_connection()
        server_running = self.test_production_server()
        process_count, process_pids = self.check_chaosgenius_processes()

        print(f"⏰ Current Time: {current_time}")
        print(
            f"🔄 Check #{iteration} | Running for: {datetime.now() - self.start_time}"
        )
        print()

        # DNS Status
        dns_status = "🟢 RESOLVED" if dns_resolved else "🟡 PROPAGATING"
        print(f"🌐 DNS Status: {dns_status}")

        # Domain Status
        if domain_live:
            if not self.stats["first_live_time"]:
                self.stats["first_live_time"] = datetime.now()
                print("🎉🎉🎉 DOMAIN WENT LIVE! EMPIRE IS BORN! 🎉🎉🎉")
            domain_status = "🚀 LIVE AND SERVING!"
            self.stats["successful_connections"] += 1
        else:
            domain_status = "⏳ Waiting for activation..."
            self.stats["failed_connections"] += 1

        print(f"🌍 Domain Status: {domain_status}")

        # ChaosGenius Dashboard Status
        if server_running:
            server_status = "🟢 CHAOSGENIUS OPERATIONAL"
        else:
            server_status = "🔴 CHAOSGENIUS DOWN"
        print(f"⚡ Local Dashboard: {server_status}")

        # Process monitoring
        if process_count > 0:
            print(
                f"🔧 ChaosGenius Processes: {process_count} running (PIDs: {', '.join(process_pids)})"
            )
        else:
            print(f"🔧 ChaosGenius Processes: 🔴 NO PROCESSES FOUND!")

        print()
        print("📊 LIVE STATISTICS:")
        print(f"   DNS Checks: {self.stats['dns_checks']}")
        print(f"   Domain Connections: {self.stats['successful_connections']}")
        print(f"   Dashboard Responses: {self.stats['dashboard_responses']}")
        print(f"   API Responses: {self.stats['api_responses']}")
        print(f"   Failed Checks: {self.stats['failed_connections']}")

        if self.stats["first_live_time"]:
            live_duration = datetime.now() - self.stats["first_live_time"]
            print(f"   🎯 DOMAIN LIVE FOR: {live_duration}")

        # Response time stats
        if self.stats["response_times"]:
            avg_response = sum(self.stats["response_times"]) / len(
                self.stats["response_times"]
            )
            print(f"   ⚡ Avg Response Time: {avg_response:.2f}s")

        # Server resources
        server_stats = self.get_server_stats()
        if "error" not in server_stats:
            print()
            print("🖥️  SERVER RESOURCES:")
            print(f"   CPU: {server_stats['cpu_usage']:.1f}%")
            print(
                f"   Memory: {server_stats['memory_usage']:.1f}% ({server_stats['memory_available']} free)"
            )
            print(
                f"   Disk: {server_stats['disk_usage']:.1f}% ({server_stats['disk_free']} free)"
            )
            if "load_average" in server_stats:
                print(f"   Load Average: {server_stats['load_average']:.2f}")

        print()

        # Status-specific messages
        if not server_running:
            print("🚨 CHAOSGENIUS DASHBOARD NOT RESPONDING:")
            print("   🔧 Check if dashboard_api.py is running")
            print("   🔧 Try: python dashboard_api.py")
            print("   🔧 Or use VS Code task: 🎛️ Launch ChaosGenius Dashboard")
        elif domain_live:
            print("🎯 NEXT STEPS:")
            print("   ✅ Visit https://hyperfocuszone.com")
            print("   ✅ Test your real API integrations")
            print("   ✅ Share launch announcements")
            print("   ✅ Activate Discord bot with real token")
            print("   ✅ CONQUER THE WORLD! 🌍👑")
        else:
            print("⏳ WAITING FOR:")
            print("   🌐 DNS propagation to complete")
            print("   🚀 Domain to start responding")
            print("   💜 NEURODIVERGENT EMPIRE ACTIVATION!")

        print()
        print("💜 Your ChaosGenius empire is ready to change the world! 💜")
        print(
            "🧠 Built for neurodivergent entrepreneurs, by neurodivergent passion! 🧠"
        )

        # Update stats
        self.stats["dns_checks"] += 1
        total_checks = (
            self.stats["successful_connections"] + self.stats["failed_connections"]
        )
        if total_checks > 0:
            self.stats["uptime_percentage"] = (
                self.stats["successful_connections"] / total_checks
            ) * 100

    def save_monitoring_log(self):
        """Save monitoring data to file"""
        try:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "domain": self.domain,
                "monitoring_duration": str(datetime.now() - self.start_time),
                "stats": self.stats,
                "server_resources": self.get_server_stats(),
            }

            log_file = Path("logs/hyperfocus_zone_launch_monitor.json")
            log_file.parent.mkdir(exist_ok=True)

            with open(log_file, "w") as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            print(f"Failed to save monitoring log: {e}")

    def run_monitoring(self, max_duration_minutes=30):
        """Run the live monitoring dashboard"""
        print("🚀 Starting Hyperfocus Zone Launch Monitor...")
        print("🧠 Monitoring for domain activation and server health...")
        print()

        iteration = 0
        max_iterations = max_duration_minutes * 2  # Check every 30 seconds

        try:
            while iteration < max_iterations:
                iteration += 1
                self.display_status(iteration)

                # Save progress every 10 checks
                if iteration % 10 == 0:
                    self.save_monitoring_log()

                # If domain is live, continue monitoring but less frequently
                if self.stats["first_live_time"]:
                    time.sleep(60)  # Check every minute when live
                else:
                    time.sleep(30)  # Check every 30 seconds when waiting

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n🚨 Monitoring error: {e}")
        finally:
            print("\n💾 Saving final monitoring report...")
            self.save_monitoring_log()
            print("✅ Monitoring complete!")


if __name__ == "__main__":
    print("🚀🔥💜 HYPERFOCUS ZONE LAUNCH MONITOR ACTIVATED! 💜🔥🚀")
    print("WOOP WOOP - TRACKING THE NEURODIVERGENT REVOLUTION!")
    print()

    monitor = HyperfocusZoneLiveMonitor()
    monitor.run_monitoring(max_duration_minutes=30)  # Monitor for 30 minutes max
