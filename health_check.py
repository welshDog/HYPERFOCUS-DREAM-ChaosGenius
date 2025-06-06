#!/usr/bin/env python3
"""
🏥 ChaosGenius Health Check
========================
Quick system health verification
"""

import sys
import os
from pathlib import Path
import sqlite3
import json
from datetime import datetime

def check_health():
    health_report = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "checks": [],
        "issues": []
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

if __name__ == "__main__":
    try:
        is_healthy = check_health()
        sys.exit(0 if is_healthy else 1)
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)
