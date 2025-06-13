#!/usr/bin/env python3
"""
🛡️👾 GUARDIAN X ACTIVATION & TESTING SCRIPT 👾🛡️
Real-time protection system testing and demonstration
"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List

import requests


class GuardianXTester:
    """🚀 Guardian X System Tester - Prove the bouncer works!"""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_user_id = "guardian_test_user"
        self.protection_scenarios = self._init_protection_scenarios()

    def _init_protection_scenarios(self) -> List[Dict]:
        """Initialize test scenarios for each protection type"""
        return [
            {
                "name": "Energy Crash Protection",
                "context": {
                    "user_id": self.test_user_id,
                    "energy_level": 25,  # Below 30% threshold
                    "mood": "tired",
                    "mood_confidence": 0.8,
                    "continuous_work_minutes": 45,
                },
                "expected_protection": "redirect",
                "emoji": "🛡️",
            },
            {
                "name": "Overwhelm Gate",
                "context": {
                    "user_id": self.test_user_id,
                    "energy_level": 60,
                    "mood": "overwhelmed",
                    "mood_confidence": 0.85,
                    "message": "I have so many tasks and deadlines I don't know where to start",
                },
                "expected_protection": "suggest",
                "emoji": "🌊",
            },
            {
                "name": "Hyperfocus Burnout Shield",
                "context": {
                    "user_id": self.test_user_id,
                    "energy_level": 70,
                    "mood": "focused",
                    "continuous_work_minutes": 200,  # Over 3 hours
                    "context": "hyperfocus_session",
                },
                "expected_protection": "warn",
                "emoji": "⚡",
            },
            {
                "name": "Sleep Guardian",
                "context": {
                    "user_id": self.test_user_id,
                    "energy_level": 50,
                    "mood": "neutral",
                    "hour": 23.5,  # Late night
                    "continuous_work_minutes": 120,
                },
                "expected_protection": "suggest",
                "emoji": "🌙",
            },
            {
                "name": "Focus Fortress",
                "context": {
                    "user_id": self.test_user_id,
                    "energy_level": 85,
                    "mood": "focused",
                    "context": "hyperfocus_session",
                    "interruption_risk": 0.8,
                },
                "expected_protection": "block",
                "emoji": "🎯",
            },
            {
                "name": "Dopamine Reserve Monitor",
                "context": {
                    "user_id": self.test_user_id,
                    "energy_level": 40,
                    "mood": "tired",
                    "mood_confidence": 0.9,
                    "recent_completions": 0,
                },
                "expected_protection": "suggest",
                "emoji": "🔋",
            },
        ]

    def print_banner(self):
        """🚀 Epic Guardian X activation banner"""
        print("\n" + "=" * 70)
        print("🛡️👾 GUARDIAN X ACTIVATION SEQUENCE INITIATED 👾🛡️")
        print("    Mental Nightclub Bouncer - Protection System Test")
        print("=" * 70 + "\n")

    async def test_guardian_status(self) -> bool:
        """Test if Guardian system is operational"""
        try:
            print("🔍 Testing Guardian System Status...")
            response = requests.get(f"{self.base_url}/api/broski/guardian/status")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Guardian Status: {data.get('status', 'Unknown')}")
                print(f"🛡️ Guardian Active: {data.get('guardian_active', False)}")
                print(
                    f"🔐 Active Rules: {data.get('protection_stats', {}).get('active_rules', 0)}"
                )
                return data.get("guardian_active", False)
            else:
                print(f"❌ Guardian status check failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Guardian status error: {e}")
            return False

    async def test_protection_scenario(self, scenario: Dict) -> Dict:
        """Test a specific protection scenario"""
        print(f"\n{scenario['emoji']} Testing: {scenario['name']}")
        print("-" * 50)

        try:
            # Test protection check
            response = requests.post(
                f"{self.base_url}/api/broski/guardian/protection-check",
                json={"user_id": self.test_user_id, "context": scenario["context"]},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                protections = data.get("protection_actions", [])

                print(f"📊 Protections Triggered: {len(protections)}")

                if protections:
                    main_protection = protections[0]
                    print(
                        f"🛡️ Protection Type: {main_protection.get('action', 'unknown')}"
                    )
                    print(f"💬 Message: {main_protection.get('message', 'No message')}")

                    if main_protection.get("suggestions"):
                        print("💡 Suggestions:")
                        for suggestion in main_protection["suggestions"][:3]:
                            print(f"   • {suggestion}")

                    if main_protection.get("redirect_suggestions"):
                        print("🔄 Redirections:")
                        for redirect in main_protection["redirect_suggestions"][:3]:
                            print(f"   • {redirect}")

                    # Check if expected protection was triggered
                    expected = scenario.get("expected_protection")
                    actual = main_protection.get("action")

                    if expected == actual:
                        print(
                            f"✅ PROTECTION WORKING! Expected: {expected}, Got: {actual}"
                        )
                        return {"success": True, "protection": main_protection}
                    else:
                        print(
                            f"⚠️ Unexpected protection: Expected {expected}, Got {actual}"
                        )
                        return {
                            "success": False,
                            "expected": expected,
                            "actual": actual,
                        }
                else:
                    print("🟡 No protections triggered for this scenario")
                    return {"success": False, "reason": "no_protections"}
            else:
                print(f"❌ Protection test failed: {response.status_code}")
                return {"success": False, "error": response.status_code}

        except Exception as e:
            print(f"❌ Protection test error: {e}")
            return {"success": False, "error": str(e)}

    async def test_safe_mode(self):
        """Test Safe Mode activation"""
        print(f"\n🛡️💜 Testing Safe Mode Activation")
        print("-" * 50)

        try:
            response = requests.post(
                f"{self.base_url}/api/broski/guardian/safe-mode",
                json={"user_id": self.test_user_id, "duration_hours": 1},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                print("✅ Safe Mode activated successfully!")
                print(f"💜 Status: {data.get('status', 'unknown')}")
                print(
                    f"⏰ Duration: {data.get('result', {}).get('duration', 'unknown')}"
                )

                modifications = data.get("result", {}).get("modifications", {})
                if modifications:
                    print("🔧 Active Modifications:")
                    for mod, enabled in modifications.items():
                        if enabled:
                            print(f"   • {mod.replace('_', ' ').title()}")

                return True
            else:
                print(f"❌ Safe Mode activation failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Safe Mode test error: {e}")
            return False

    async def test_work_session_tracking(self):
        """Test work session tracking features"""
        print(f"\n⏰ Testing Work Session Tracking")
        print("-" * 50)

        try:
            # Start work session
            response = requests.post(
                f"{self.base_url}/api/broski/guardian/session/start",
                json={"user_id": self.test_user_id, "session_type": "hyperfocus"},
                timeout=10,
            )

            if response.status_code == 200:
                print("✅ Work session started successfully!")

                # Wait a moment
                await asyncio.sleep(2)

                # Take a break
                break_response = requests.post(
                    f"{self.base_url}/api/broski/guardian/session/break",
                    json={"user_id": self.test_user_id, "break_type": "micro"},
                    timeout=10,
                )

                if break_response.status_code == 200:
                    print("✅ Break recorded successfully!")
                    return True
                else:
                    print(f"⚠️ Break recording failed: {break_response.status_code}")
                    return False
            else:
                print(f"❌ Work session start failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Session tracking test error: {e}")
            return False

    async def test_custom_boundaries(self):
        """Test custom boundary setting"""
        print(f"\n🔐 Testing Custom Boundary Setting")
        print("-" * 50)

        try:
            # Set work hours boundary
            boundary_data = {
                "user_id": self.test_user_id,
                "boundary_type": "work_hours",
                "boundary_data": {"start_hour": 9, "end_hour": 17, "timezone": "UTC"},
            }

            response = requests.post(
                f"{self.base_url}/api/broski/guardian/boundary",
                json=boundary_data,
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                print("✅ Custom boundary set successfully!")
                print(f"🔐 Boundary Type: {data.get('boundary_type', 'unknown')}")
                return True
            else:
                print(f"❌ Boundary setting failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Boundary test error: {e}")
            return False

    async def run_full_test_suite(self):
        """🚀 Run the complete Guardian X test suite"""
        self.print_banner()

        # Test results tracking
        results = {"total_tests": 0, "passed": 0, "failed": 0, "details": []}

        # 1. Test Guardian Status
        print("🔍 PHASE 1: Guardian System Status Check")
        guardian_active = await self.test_guardian_status()
        results["total_tests"] += 1
        if guardian_active:
            results["passed"] += 1
            results["details"].append("✅ Guardian System Status: OPERATIONAL")
        else:
            results["failed"] += 1
            results["details"].append("❌ Guardian System Status: OFFLINE")
            print("\n🚨 Guardian system is not active. Some tests may fail.")

        # 2. Test Protection Scenarios
        print(f"\n🛡️ PHASE 2: Protection Scenarios Testing")
        for scenario in self.protection_scenarios:
            result = await self.test_protection_scenario(scenario)
            results["total_tests"] += 1

            if result.get("success"):
                results["passed"] += 1
                results["details"].append(f"✅ {scenario['name']}: WORKING")
            else:
                results["failed"] += 1
                results["details"].append(f"❌ {scenario['name']}: FAILED")

            await asyncio.sleep(1)  # Brief pause between tests

        # 3. Test Safe Mode
        print(f"\n🛡️ PHASE 3: Safe Mode Testing")
        safe_mode_result = await self.test_safe_mode()
        results["total_tests"] += 1
        if safe_mode_result:
            results["passed"] += 1
            results["details"].append("✅ Safe Mode: WORKING")
        else:
            results["failed"] += 1
            results["details"].append("❌ Safe Mode: FAILED")

        # 4. Test Session Tracking
        print(f"\n⏰ PHASE 4: Session Tracking Testing")
        session_result = await self.test_work_session_tracking()
        results["total_tests"] += 1
        if session_result:
            results["passed"] += 1
            results["details"].append("✅ Session Tracking: WORKING")
        else:
            results["failed"] += 1
            results["details"].append("❌ Session Tracking: FAILED")

        # 5. Test Custom Boundaries
        print(f"\n🔐 PHASE 5: Custom Boundaries Testing")
        boundary_result = await self.test_custom_boundaries()
        results["total_tests"] += 1
        if boundary_result:
            results["passed"] += 1
            results["details"].append("✅ Custom Boundaries: WORKING")
        else:
            results["failed"] += 1
            results["details"].append("❌ Custom Boundaries: FAILED")

        # Final Results
        self.print_final_results(results)

        return results

    def print_final_results(self, results: Dict):
        """Print epic final test results"""
        print("\n" + "=" * 70)
        print("🏆 GUARDIAN X TEST SUITE RESULTS 🏆")
        print("=" * 70)

        success_rate = (
            (results["passed"] / results["total_tests"]) * 100
            if results["total_tests"] > 0
            else 0
        )

        print(f"📊 Total Tests: {results['total_tests']}")
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"🎯 Success Rate: {success_rate:.1f}%")

        print(f"\n📋 Detailed Results:")
        for detail in results["details"]:
            print(f"   {detail}")

        if success_rate >= 80:
            print(f"\n🚀💥 GUARDIAN X IS FULLY OPERATIONAL! 💥🚀")
            print("Your mental nightclub bouncer is ready to protect your energy!")
        elif success_rate >= 60:
            print(f"\n⚠️ Guardian X is mostly working but needs some attention.")
        else:
            print(f"\n🚨 Guardian X needs troubleshooting before full deployment.")

        print("=" * 70 + "\n")


async def main():
    """🚀 Main Guardian X test execution"""
    print("🛡️👾 Initializing Guardian X Test Suite...")

    # Check if dashboard is running
    tester = GuardianXTester()

    try:
        # Quick connectivity test
        response = requests.get(f"{tester.base_url}/api/broski/status", timeout=5)
        if response.status_code != 200:
            print("⚠️ Dashboard connectivity issue, but proceeding with tests...")
    except Exception as e:
        print(f"🚨 Cannot connect to dashboard at {tester.base_url}")
        print("Please ensure the ChaosGenius Dashboard is running:")
        print("   python dashboard_api.py")
        return

    # Run the full test suite
    results = await tester.run_full_test_suite()

    # Generate test report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"guardian_x_test_report_{timestamp}.json"

    with open(report_filename, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "test_results": results,
                "guardian_version": "1.0.0",
                "test_suite_version": "1.0.0",
            },
            f,
            indent=2,
        )

    print(f"📄 Test report saved: {report_filename}")


if __name__ == "__main__":
    asyncio.run(main())
