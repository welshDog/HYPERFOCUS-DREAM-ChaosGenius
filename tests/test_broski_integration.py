#!/usr/bin/env python3
"""
🧪 BROski ClanVerse Ultra - System Integration Test Suite
Complete end-to-end testing of the BROski AI ecosystem
"""

import json
import sys
import time

import requests
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)


def print_status(message, status="INFO"):
    colors = {
        "SUCCESS": Fore.GREEN,
        "ERROR": Fore.RED,
        "WARNING": Fore.YELLOW,
        "INFO": Fore.CYAN,
    }
    print(f"{colors.get(status, Fore.WHITE)}[{status}] {message}{Style.RESET_ALL}")


def test_broski_api_endpoints():
    """Test all BROski API endpoints"""
    print_status("🧠 Testing BROski ClanVerse Ultra API Integration", "INFO")

    base_url = "http://localhost:5000"
    tests_passed = 0
    total_tests = 0

    # Test 1: BROski Status
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/broski/status")
        if response.status_code == 200:
            data = response.json()
            # Handle both direct and nested response formats
            if "broski_data" in data:
                status = data["broski_data"]["status"]
                intelligence = data["broski_data"]["system_intelligence"]
            else:
                status = data["status"]
                intelligence = data["system_intelligence"]
            print_status(
                f"✅ BROski Status: {status} (Intelligence: {intelligence}%)", "SUCCESS"
            )
            tests_passed += 1
        else:
            print_status(
                f"❌ BROski Status endpoint failed: {response.status_code}", "ERROR"
            )
    except Exception as e:
        print_status(f"❌ BROski Status test failed: {e}", "ERROR")

    # Test 2: BROski Chat
    total_tests += 1
    try:
        chat_data = {
            "user_id": "test_integration_user",
            "message": "I'm feeling overwhelmed with my coding project. Can you help?",
            "context": {"platform": "integration_test", "test_mode": True},
        }
        response = requests.post(f"{base_url}/api/broski/chat", json=chat_data)
        if response.status_code == 200:
            data = response.json()
            print_status(
                f"✅ BROski Chat: {data['style']} response generated", "SUCCESS"
            )
            print_status(
                f"   Mood Detected: {data['mood_detected']} (Confidence: {data['confidence']})",
                "INFO",
            )
            print_status(f"   Energy Level: {data['energy_level']}/100", "INFO")
            tests_passed += 1
        else:
            print_status(
                f"❌ BROski Chat endpoint failed: {response.status_code}", "ERROR"
            )
    except Exception as e:
        print_status(f"❌ BROski Chat test failed: {e}", "ERROR")

    # Test 3: Hyperfocus Session
    total_tests += 1
    try:
        hyperfocus_data = {
            "user_id": "test_integration_user",
            "session_data": {
                "duration_minutes": 25,
                "task_type": "Complete API integration testing",
                "user_id": "test_integration_user",
            },
        }
        response = requests.post(
            f"{base_url}/api/broski/hyperfocus", json=hyperfocus_data
        )
        if response.status_code == 200:
            data = response.json()
            # Handle both success_data and support_data response formats
            if "support_data" in data:
                print_status(f"✅ Hyperfocus Session: Complete", "SUCCESS")
            elif "success" in data:
                print_status(f"✅ Hyperfocus Session: {data['success']}", "SUCCESS")
            else:
                print_status(f"✅ Hyperfocus Session: Response received", "SUCCESS")
            tests_passed += 1
        else:
            print_status(
                f"❌ Hyperfocus endpoint failed: {response.status_code}", "ERROR"
            )
    except Exception as e:
        print_status(f"❌ Hyperfocus test failed: {e}", "ERROR")

    # Test 4: User Feedback
    total_tests += 1
    try:
        feedback_data = {
            "user_id": "test_integration_user",
            "interaction_id": "test_interaction_001",
            "feedback": "helpful",
            "rating": 5,
            "context": {"test_mode": True},
        }
        response = requests.post(f"{base_url}/api/broski/feedback", json=feedback_data)
        if response.status_code == 200:
            data = response.json()
            # Handle various response formats
            if "success" in data:
                print_status(f"✅ User Feedback: {data['success']}", "SUCCESS")
            elif "status" in data:
                print_status(f"✅ User Feedback: {data['status']}", "SUCCESS")
            else:
                print_status(f"✅ User Feedback: Response received", "SUCCESS")
            tests_passed += 1
        else:
            print_status(
                f"❌ Feedback endpoint failed: {response.status_code}", "ERROR"
            )
    except Exception as e:
        print_status(f"❌ Feedback test failed: {e}", "ERROR")

    # Summary
    success_rate = (tests_passed / total_tests) * 100
    print_status(
        f"\n📊 Test Results: {tests_passed}/{total_tests} passed ({success_rate:.1f}%)",
        "SUCCESS" if success_rate >= 75 else "WARNING",
    )

    # Use assert instead of return for pytest compatibility
    assert (
        success_rate >= 75
    ), f"Test suite failed with {success_rate:.1f}% success rate"


def test_ai_intelligence():
    """Test BROski AI intelligence and learning capabilities"""
    print_status("🎓 Testing BROski AI Intelligence & Learning", "INFO")

    try:
        # Import BROski core directly
        sys.path.append(".")
        import asyncio

        from ai_modules.broski.broski_core import BROskiCore

        # Initialize BROski
        broski = BROskiCore()

        async def test_ai_responses():
            # Test AI Processing
            test_messages = [
                "I can't focus today, everything feels chaotic",
                "I'm excited to start this new project!",
                "I'm stuck on this coding problem and feeling frustrated",
            ]

            for i, message in enumerate(test_messages, 1):
                print_status(f"Testing AI Response {i}/3...", "INFO")
                response = await broski.process_user_interaction(
                    f"test_user_{i}", message, {"platform": "integration_test"}
                )

                # Validate response structure
                required_fields = [
                    "message",
                    "mood_detected",
                    "energy_level",
                    "recommendations",
                ]
                missing_fields = [
                    field for field in required_fields if not hasattr(response, field)
                ]

                if not missing_fields:
                    print_status(f"✅ AI Response {i}: Complete and valid", "SUCCESS")
                else:
                    print_status(
                        f"❌ AI Response {i}: Missing fields: {missing_fields}", "ERROR"
                    )
                    assert (
                        False
                    ), f"AI Response {i} missing required fields: {missing_fields}"

            return True

        # Run async test
        result = asyncio.run(test_ai_responses())

        print_status(
            f"🧠 System Intelligence: {broski.system_intelligence}%", "SUCCESS"
        )
        assert result, "AI Intelligence test failed"

    except Exception as e:
        print_status(f"❌ AI Intelligence test failed: {e}", "ERROR")
        assert False, f"AI Intelligence test failed: {e}"


def test_system_performance():
    """Test system performance and response times"""
    print_status("⚡ Testing System Performance", "INFO")

    try:
        # Test API response times
        start_time = time.time()
        response = requests.get("http://localhost:5000/api/broski/status")
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200 and response_time < 500:
            print_status(
                f"✅ API Response Time: {response_time:.1f}ms (Excellent)", "SUCCESS"
            )
        elif response_time < 1000:
            print_status(
                f"⚠️ API Response Time: {response_time:.1f}ms (Acceptable)", "WARNING"
            )
        else:
            print_status(
                f"❌ API Response Time: {response_time:.1f}ms (Too Slow)", "ERROR"
            )
            assert False, f"API response time too slow: {response_time:.1f}ms"

        assert (
            response.status_code == 200
        ), f"API returned status code {response.status_code}"
        assert (
            response_time < 1000
        ), f"API response time too slow: {response_time:.1f}ms"

    except Exception as e:
        print_status(f"❌ Performance test failed: {e}", "ERROR")
        assert False, f"Performance test failed: {e}"
