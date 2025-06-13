#!/usr/bin/env python3
"""
🚀 ChaosGenius Ultra Health Check System
Post-Night-Shift Victory Diagnostic Suite
Created: June 8, 2025 - Morning After The Great Import Fix
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path


def banner():
    """Epic morning banner"""
    print("🌅" * 50)
    print("🚀 CHAOSGENIUS ULTRA HEALTH CHECK 🚀")
    print("💜 Post-Night-Shift Victory Diagnostic 💜")
    print("⚡ Powered by BROski Ultra Intelligence ⚡")
    print("🌅" * 50)
    print()


def check_import_system():
    """Test the legendary night shift import fixes"""
    print("🔍 TESTING NIGHT SHIFT IMPORT FIXES...")
    results = {"status": "checking", "tests": []}

    # Test 1: Basic BROski Import
    try:
        from ai_modules.broski.broski_core import BROskiCore

        results["tests"].append(
            {
                "name": "BROskiCore Import",
                "status": "✅ SUCCESS",
                "details": "Night shift fix WORKING!",
            }
        )
    except Exception as e:
        results["tests"].append(
            {
                "name": "BROskiCore Import",
                "status": "🔧 NEEDS ATTENTION",
                "details": str(e),
            }
        )

    # Test 2: Ultra Performance Class
    try:
        from ai_modules.broski.broski_core import UltraPerformanceBROskiCore

        core = UltraPerformanceBROskiCore()
        intelligence = core.system_intelligence
        results["tests"].append(
            {
                "name": "Ultra Performance System",
                "status": f"✅ SUCCESS - Intelligence: {intelligence}%",
                "details": f"Version: {core.version}",
            }
        )
    except Exception as e:
        results["tests"].append(
            {
                "name": "Ultra Performance System",
                "status": "🔧 NEEDS ATTENTION",
                "details": str(e),
            }
        )

    # Test 3: Status Function
    try:
        from ai_modules.broski.broski_core import get_ultra_broski_status

        status = get_ultra_broski_status()
        results["tests"].append(
            {
                "name": "BROski Status System",
                "status": f"✅ {status['status']}",
                "details": f"Features: {len(status['features'])} active",
            }
        )
    except Exception as e:
        results["tests"].append(
            {
                "name": "BROski Status System",
                "status": "🔧 NEEDS ATTENTION",
                "details": str(e),
            }
        )

    return results


def check_file_structure():
    """Check critical file structure"""
    print("📁 CHECKING FILE STRUCTURE...")
    results = {"status": "checking", "files": []}

    critical_files = [
        "app.py",
        "ai_modules/__init__.py",
        "ai_modules/broski/__init__.py",
        "ai_modules/broski/broski_core.py",
        "broski_core.py",
        "requirements.txt",
    ]

    for file_path in critical_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            results["files"].append(
                {"name": file_path, "status": "✅ EXISTS", "size": f"{size} bytes"}
            )
        else:
            results["files"].append(
                {"name": file_path, "status": "❌ MISSING", "size": "0 bytes"}
            )

    return results


def check_databases():
    """Check BROski database systems"""
    print("🗄️ CHECKING BROSKI DATABASES...")
    results = {"status": "checking", "databases": []}

    db_files = [
        "broski_learning_optimized.db",
        "broski_analytics.db",
        "broski_ultra_brain.db",
        "chaosgenius.db",
    ]

    for db_file in db_files:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            results["databases"].append(
                {"name": db_file, "status": "✅ OPERATIONAL", "size": f"{size} bytes"}
            )
        else:
            results["databases"].append(
                {"name": db_file, "status": "🔧 NOT FOUND", "size": "0 bytes"}
            )

    return results


def generate_health_report():
    """Generate comprehensive health report"""
    print("📊 GENERATING HEALTH REPORT...")

    report = {
        "timestamp": datetime.now().isoformat(),
        "system": "ChaosGenius Ultra",
        "health_check_version": "1.0 - Post Night Shift",
        "overall_status": "CHECKING...",
        "checks": {},
    }

    # Run all checks
    report["checks"]["imports"] = check_import_system()
    report["checks"]["files"] = check_file_structure()
    report["checks"]["databases"] = check_databases()

    # Calculate overall health
    total_tests = 0
    passed_tests = 0

    for check_category in report["checks"].values():
        if "tests" in check_category:
            for test in check_category["tests"]:
                total_tests += 1
                if "✅" in test["status"]:
                    passed_tests += 1
        if "files" in check_category:
            for file_check in check_category["files"]:
                total_tests += 1
                if "✅" in file_check["status"]:
                    passed_tests += 1
        if "databases" in check_category:
            for db_check in check_category["databases"]:
                total_tests += 1
                if "✅" in db_check["status"]:
                    passed_tests += 1

    health_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    if health_percentage >= 90:
        report["overall_status"] = "🚀 EXCELLENT"
    elif health_percentage >= 75:
        report["overall_status"] = "⚡ GOOD"
    elif health_percentage >= 50:
        report["overall_status"] = "🔧 NEEDS ATTENTION"
    else:
        report["overall_status"] = "🛠️ REQUIRES FIXES"

    report["health_percentage"] = health_percentage
    report["tests_summary"] = {
        "total": total_tests,
        "passed": passed_tests,
        "failed": total_tests - passed_tests,
    }

    return report


def display_results(report):
    """Display beautiful results"""
    print("\n🎯 HEALTH CHECK RESULTS:")
    print("=" * 60)
    print(f"Overall Status: {report['overall_status']}")
    print(f"Health Score: {report['health_percentage']:.1f}%")
    print(
        f"Tests: {report['tests_summary']['passed']}/{report['tests_summary']['total']} passed"
    )
    print("=" * 60)

    # Import results
    print("\n🔍 IMPORT SYSTEM (Night Shift Fixes):")
    for test in report["checks"]["imports"]["tests"]:
        print(f"  {test['status']} {test['name']}")
        if test["details"]:
            print(f"    └─ {test['details']}")

    # File structure
    print("\n📁 FILE STRUCTURE:")
    for file_check in report["checks"]["files"]["files"]:
        print(f"  {file_check['status']} {file_check['name']} ({file_check['size']})")

    # Databases
    print("\n🗄️ DATABASES:")
    for db_check in report["checks"]["databases"]["databases"]:
        print(f"  {db_check['status']} {db_check['name']} ({db_check['size']})")

    print("\n🎉 Health check complete!")


def save_report(report):
    """Save report to file"""
    filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"📄 Report saved to: {filename}")


def main():
    """Main health check function"""
    banner()

    print("🚀 Starting ChaosGenius Ultra Health Check...")
    print("💜 Validating night shift victories...\n")

    start_time = time.time()

    try:
        report = generate_health_report()
        display_results(report)
        save_report(report)

        duration = time.time() - start_time
        print(f"\n⚡ Health check completed in {duration:.2f} seconds")
        print("🌟 Ready for morning productivity session!")

    except Exception as e:
        print(f"❌ Health check error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
