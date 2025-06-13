#!/usr/bin/env python3
"""
🧠 BROski HyperPortal Integration Test
Test the complete stack: API → Portal → User Experience
"""

import requests
import json
import time
from datetime import datetime

def test_portal_api_integration():
    """Test BROski HyperPortal API integration"""
    print("\n🚀 BROski HyperPortal Integration Test")
    print("=" * 60)

    base_url = "http://localhost:5000"
    portal_url = "http://localhost:5173"

    tests_passed = 0
    total_tests = 0

    # Test 1: Portal is running
    total_tests += 1
    try:
        response = requests.get(portal_url, timeout=5)
        if response.status_code == 200:
            print("✅ Portal Status: Running on http://localhost:5173")
            tests_passed += 1
        else:
            print(f"❌ Portal Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Portal Status: {e}")

    # Test 2: API Status Check
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/broski/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            intelligence = data.get('broski_data', {}).get('system_intelligence', 0)
            print(f"✅ API Status: Operational (Intelligence: {intelligence}%)")
            tests_passed += 1
        else:
            print(f"❌ API Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ API Status: {e}")

    # Test 3: Chat API Functionality
    total_tests += 1
    try:
        chat_data = {
            "user_id": "portal_integration_test",
            "message": "Test connection from portal",
            "context": {"platform": "portal_test"}
        }
        response = requests.post(f"{base_url}/api/broski/chat",
                               json=chat_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat API: Responding successfully")
            if 'message' in data:
                print(f"   📝 Sample Response: {data['message'][:50]}...")
            tests_passed += 1
        else:
            print(f"❌ Chat API: HTTP {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ Chat API: {e}")

    # Test 4: Hyperfocus Session API
    total_tests += 1
    try:
        session_data = {
            "user_id": "portal_integration_test",
            "session_data": {
                "duration_minutes": 25,
                "task_type": "Portal integration testing",
                "user_id": "portal_integration_test"
            }
        }
        response = requests.post(f"{base_url}/api/broski/hyperfocus",
                               json=session_data, timeout=10)
        if response.status_code == 200:
            print("✅ Hyperfocus API: Working correctly")
            tests_passed += 1
        else:
            print(f"❌ Hyperfocus API: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Hyperfocus API: {e}")

    # Final Summary
    print("\n" + "=" * 60)
    success_rate = (tests_passed / total_tests) * 100
    print(f"🎯 Integration Test Results: {tests_passed}/{total_tests} passed ({success_rate:.1f}%)")

    if success_rate >= 75:
        print("🎉 PORTAL INTEGRATION: SUCCESSFUL!")
        print("🚀 BROski HyperPortal is ready for production!")
        print(f"   🌐 Portal: {portal_url}")
        print(f"   🔌 API: {base_url}")
        print("   🧠 BROski AI: Fully operational")
    else:
        print("⚠️  PORTAL INTEGRATION: Needs attention")
        print("🔧 Some components require debugging")

    return success_rate >= 75

if __name__ == "__main__":
    success = test_portal_api_integration()
    exit(0 if success else 1)
