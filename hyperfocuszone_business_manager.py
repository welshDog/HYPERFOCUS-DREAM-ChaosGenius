#!/usr/bin/env python3
"""
🤖💰 HYPERFOCUSZONE BUSINESS INTEGRATION MANAGER
Connects all systems and provides EPIC management dashboard!
"""

import asyncio
import json
import sqlite3
import subprocess
import sys
import time
import requests
from datetime import datetime
from pathlib import Path

class HyperFocusZoneBusinessManager:
    """🎯 The Ultimate Business Empire Manager"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.services = {
            "website": {"port": 8080, "status": "OFFLINE", "process": None},
            "capture_api": {"port": 5000, "status": "OFFLINE", "process": None},
            "admin_portal": {"port": 5001, "status": "OFFLINE", "process": None}
        }

        print("🎯💼 HYPERFOCUSZONE BUSINESS MANAGER ACTIVATED!")

    def check_service_health(self, service_name, port):
        """🔍 Check if a service is responding"""
        try:
            response = requests.get(f"http://localhost:{port}", timeout=3)
            return "ONLINE" if response.status_code in [200, 404] else "ERROR"
        except:
            return "OFFLINE"

    def get_system_status(self):
        """📊 Get comprehensive system status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "empire_status": "OPERATIONAL",
            "services": {},
            "stats": {},
            "revenue_metrics": {}
        }

        # Check all services
        for service, config in self.services.items():
            status["services"][service] = {
                "port": config["port"],
                "status": self.check_service_health(service, config["port"]),
                "uptime": "Active"
            }

        # Get lead stats if database exists
        try:
            db_path = f"{self.base_path}/hyperfocus_leads.db"
            if Path(db_path).exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Today's stats
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute("SELECT COUNT(*) FROM leads WHERE DATE(timestamp) = ?", (today,))
                today_leads = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM leads")
                total_leads = cursor.fetchone()[0]

                cursor.execute("SELECT SUM(estimated_value) FROM leads")
                total_pipeline = cursor.fetchone()[0] or 0

                status["stats"] = {
                    "leads_today": today_leads,
                    "total_leads": total_leads,
                    "pipeline_value": total_pipeline
                }

                conn.close()
        except Exception as e:
            status["stats"] = {"error": str(e)}

        return status

    def display_epic_dashboard(self):
        """🎯 Display the EPIC management dashboard"""
        status = self.get_system_status()

        print("\n" + "🔥" * 60)
        print("💎💰 HYPERFOCUSZONE BUSINESS EMPIRE DASHBOARD 💰💎")
        print("🔥" * 60)

        print(f"\n⏰ Status Time: {status['timestamp']}")
        print(f"🏰 Empire Status: {status['empire_status']}")

        print("\n🌐 SERVICE STATUS:")
        print("-" * 40)
        for service, config in status["services"].items():
            status_emoji = "✅" if config["status"] == "ONLINE" else "🔴"
            print(f"{status_emoji} {service.upper()}: {config['status']} (Port {config['port']})")

        if status["stats"]:
            print("\n💰 REVENUE INTELLIGENCE:")
            print("-" * 40)
            print(f"🎯 Leads Today: {status['stats'].get('leads_today', 0)}")
            print(f"📊 Total Leads: {status['stats'].get('total_leads', 0)}")
            print(f"💎 Pipeline Value: ${status['stats'].get('pipeline_value', 0):,.0f}")

        print("\n🔗 ACCESS POINTS:")
        print("-" * 40)
        print("🌐 Public Website: http://localhost:8080/hyperfocuszone_public_website.html")
        print("🤖 Lead Capture API: http://localhost:5000/api/capture-lead")
        print("👑 Admin Dashboard: http://localhost:5000/admin/dashboard")
        print("📊 Live Stats: http://localhost:5000/api/stats")

        print("\n🔥" * 60)

    def deploy_business_empire(self):
        """🚀 Deploy the complete business empire"""
        print("🚀💰 DEPLOYING HYPERFOCUSZONE BUSINESS EMPIRE...")

        # Run the launcher script
        try:
            result = subprocess.run(
                ["bash", f"{self.base_path}/launch_hyperfocuszone_empire.sh"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                print("✅ Business empire deployment initiated!")
                time.sleep(5)  # Give services time to start
                self.display_epic_dashboard()
            else:
                print("⚠️ Deployment had issues, but systems may still be running...")
                print("Checking status manually...")
                time.sleep(3)
                self.display_epic_dashboard()

        except subprocess.TimeoutExpired:
            print("⚡ Deployment running in background...")
            time.sleep(3)
            self.display_epic_dashboard()
        except Exception as e:
            print(f"🔧 Manual deployment needed: {e}")
            self.manual_deployment_guide()

    def manual_deployment_guide(self):
        """📋 Show manual deployment guide"""
        print("\n🔧 MANUAL DEPLOYMENT GUIDE:")
        print("=" * 50)
        print("1. Start Customer Capture API:")
        print("   python3 hyperfocuszone_customer_capture_agent.py &")
        print()
        print("2. Start Website Server:")
        print("   python3 -m http.server 8080 &")
        print()
        print("3. Check status:")
        print("   python3 hyperfocuszone_business_manager.py --status")

    def monitor_empire(self):
        """👁️ Monitor the business empire continuously"""
        print("👁️ EMPIRE MONITORING ACTIVATED!")
        print("Press Ctrl+C to stop monitoring...")

        try:
            while True:
                self.display_epic_dashboard()
                time.sleep(30)  # Update every 30 seconds
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped.")

    def quick_test_empire(self):
        """⚡ Quick test of all empire systems"""
        print("⚡ RUNNING EMPIRE SYSTEMS TEST...")

        status = self.get_system_status()

        # Test website
        website_test = self.check_service_health("website", 8080)
        print(f"🌐 Website Test: {'✅ PASS' if website_test == 'ONLINE' else '❌ FAIL'}")

        # Test API
        api_test = self.check_service_health("api", 5000)
        print(f"🤖 API Test: {'✅ PASS' if api_test == 'ONLINE' else '❌ FAIL'}")

        # Test database
        db_path = f"{self.base_path}/hyperfocus_leads.db"
        db_test = "✅ PASS" if Path(db_path).exists() else "❌ FAIL"
        print(f"🗄️ Database Test: {db_test}")

        # Overall health
        all_tests = [website_test, api_test, "ONLINE" if Path(db_path).exists() else "OFFLINE"]
        overall = "🟢 HEALTHY" if all([t == "ONLINE" for t in all_tests]) else "🟡 PARTIAL"
        print(f"\n🏰 Empire Health: {overall}")

def main():
    """🚀 Main business manager interface"""
    manager = HyperFocusZoneBusinessManager()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--deploy":
            manager.deploy_business_empire()
        elif command == "--status":
            manager.display_epic_dashboard()
        elif command == "--monitor":
            manager.monitor_empire()
        elif command == "--test":
            manager.quick_test_empire()
        else:
            print("Unknown command. Use: --deploy, --status, --monitor, or --test")
    else:
        # Interactive mode
        print("🎯 HYPERFOCUSZONE BUSINESS MANAGER")
        print("=" * 40)
        print("1. Deploy Empire")
        print("2. Check Status")
        print("3. Monitor Empire")
        print("4. Test Systems")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ")

        if choice == "1":
            manager.deploy_business_empire()
        elif choice == "2":
            manager.display_epic_dashboard()
        elif choice == "3":
            manager.monitor_empire()
        elif choice == "4":
            manager.quick_test_empire()
        elif choice == "5":
            print("👋 Business empire management ended!")
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()