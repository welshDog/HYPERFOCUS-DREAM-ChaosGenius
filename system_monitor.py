#!/usr/bin/env python3
"""
🧠 ChaosGenius System Monitor
============================
Quick system health check and restart if needed
"""

import requests
import subprocess
import time
import os
from pathlib import Path

def check_dashboard_health():
    """Check if dashboard is responding"""
    try:
        response = requests.get("http://localhost:3000/api/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def restart_dashboard():
    """Restart the dashboard if needed"""
    print("🔄 Restarting dashboard...")

    # Kill existing processes
    subprocess.run(["pkill", "-f", "app.py"], capture_output=True)
    time.sleep(2)

    # Start new process
    os.chdir(Path(__file__).parent)
    subprocess.Popen(["python", "app.py"])
    print("✅ Dashboard restarted!")

def main():
    """Main monitoring function"""
    print("🧠 ChaosGenius System Monitor")
    print("=" * 30)

    if check_dashboard_health():
        print("✅ Dashboard is healthy and responding")

        # Test key endpoints
        endpoints = [
            "/api/hyperfocus-analytics",
            "/ultra-analytics",
            "/api/status"
        ]

        for endpoint in endpoints:
            try:
                response = requests.get(f"http://localhost:3000{endpoint}", timeout=3)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"{status} {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint}: Error - {e}")

        print("\n🎯 System Status: OPERATIONAL")
        print("💜 Dashboard URL: http://localhost:3000")
        print("🎛️ Ultra Analytics: http://localhost:3000/ultra-analytics")

    else:
        print("❌ Dashboard not responding - restarting...")
        restart_dashboard()
        time.sleep(5)

        if check_dashboard_health():
            print("✅ Dashboard restart successful!")
        else:
            print("❌ Dashboard restart failed - manual intervention needed")

if __name__ == "__main__":
    main()
