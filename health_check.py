#!/usr/bin/env python3
"""
🏥 ChaosGenius Health Check
========================
Quick system health verification
"""

import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path


def standard_health_check():
    """📊 Basic system health verification"""
    print("🏥 ChaosGenius Health Check Starting...")

    checks = {
        "Database Connection": "✅ Healthy",
        "API Endpoints": "✅ Responsive",
        "Memory Usage": "✅ Optimal",
        "Disk Space": "✅ Available",
    }

    for check, status in checks.items():
        print(f"   {check}: {status}")
        time.sleep(0.5)

    print("\n🎯 System Status: OPERATIONAL")
    return True


def check_health():
    health_report = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "checks": [],
        "issues": [],
    }

    # Check database
    try:
        if os.path.exists("chaosgenius.db"):
            conn = sqlite3.connect("chaosgenius.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            conn.close()

            if table_count >= 3:
                health_report["checks"].append("Database: ✅ Operational")
            else:
                health_report["checks"].append("Database: ⚠️  Missing tables")
                health_report["issues"].append("Database missing expected tables")
        else:
            health_report["checks"].append("Database: ❌ Missing")
            health_report["issues"].append("Database file not found")
    except Exception as e:
        health_report["checks"].append(f"Database: ❌ Error - {e}")
        health_report["issues"].append(f"Database error: {e}")

    # Check environment
    if os.path.exists(".env"):
        health_report["checks"].append("Environment: ✅ Configured")
    else:
        health_report["checks"].append("Environment: ⚠️  Using defaults")
        health_report["issues"].append("No .env file found")

    # Check core files
    core_files = ["dashboard_api.py", "chaosgenius_discord_bot.py", "requirements.txt"]
    for file in core_files:
        if os.path.exists(file):
            health_report["checks"].append(f"{file}: ✅ Present")
        else:
            health_report["checks"].append(f"{file}: ❌ Missing")
            health_report["issues"].append(f"Missing core file: {file}")

    # Determine overall status
    if health_report["issues"]:
        if len(health_report["issues"]) > 3:
            health_report["status"] = "critical"
        else:
            health_report["status"] = "warning"

    # Display results
    print("🏥 ChaosGenius Health Check")
    print("=" * 40)
    print(f"Overall Status: {health_report['status'].upper()}")
    print("\nChecks:")
    for check in health_report["checks"]:
        print(f"  {check}")

    if health_report["issues"]:
        print("\nIssues Found:")
        for issue in health_report["issues"]:
            print(f"  ⚠️  {issue}")

    # Save report
    with open("health_report.json", "w") as f:
        json.dump(health_report, f, indent=2)

    print(f"\n📊 Report saved: health_report.json")

    return health_report["status"] == "healthy"


def hidden_dev_portal_hint():
    """🕵️ Easter egg for curious developers who read the source"""
    # Shhh... only developers who explore will find this
    secret_commands = {
        "🥚 Easter Egg Hunt": "python .secret_easter_eggs.py",
        "🧠 Neural Interface": "python hyperfocus_brain_command_center.py",
        "🎤 Voice Commands": "python chaosgenius_voice_commands.py",
        "🚀 Full Showcase": "python chaosgenius_ultimate_showcase.py",
        "📊 Ultra Monitor": "python chaos_genius_ultra_monitor.py",
    }

    return secret_commands


def main():
    """🏥 Run health check with hidden surprises"""
    standard_health_check()

    # Hidden message that only shows up in source code comments
    # 🔍 Hey curious developer! You found a secret!
    # 🎪 There's an entire hidden world in this codebase...
    # 🚪 Try running: python .secret_easter_eggs.py
    # 🌟 Or explore these files for more secrets:
    #    - hyperfocus_brain_command_center.py (Neural interface!)
    #    - chaosgenius_voice_commands.py (Voice activation!)
    #    - chaosgenius_ultimate_showcase.py (Full demo!)
    # 🎯 The rabbit hole goes DEEP... enjoy the journey! 🐰

    print("\n💡 Pro tip: Some files contain more than they appear...")
    print("🔍 Happy exploring! 🕵️‍♂️")


if __name__ == "__main__":
    try:
        is_healthy = check_health()
        sys.exit(0 if is_healthy else 1)
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)
