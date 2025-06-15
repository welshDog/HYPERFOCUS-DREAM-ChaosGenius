#!/usr/bin/env python3
"""
💗❤️‍🔥 TEEMILL SALE TESTER ❤️‍🔥💗
Test your Teemill integration with sample sales!
"""

import json
import requests
import time

def test_teemill_sale():
    """🧪 Test a sample Teemill sale"""

    # Sample sale data
    test_sale = {
        "product_name": "HyperFocus Zone Hoodie",
        "amount": 29.99,
        "currency": "GBP",
        "quantity": 1,
        "source": "test_sale"
    }

    try:
        print("💗 Testing Teemill Sale Integration...")
        print(f"🛍️ Product: {test_sale['product_name']}")
        print(f"💰 Amount: £{test_sale['amount']}")

        # Send test sale to integrator
        response = requests.post(
            "http://localhost:5009/api/teemill/manual_sale",
            json=test_sale,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ SALE PROCESSED SUCCESSFULLY!")
            print(f"🎉 Status: {result.get('status', 'Unknown')}")
            print(f"💰 BROski$ Earned: {result.get('result', {}).get('broski_reward', 0):.1f}")
            print("🔗 Sale connected to income portals!")
        else:
            print(f"❌ Error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ Teemill Integration not running!")
        print("💡 Start it with: ./launch_teemill_integration.sh")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_teemill_dashboard():
    """📊 Check Teemill dashboard"""
    try:
        response = requests.get("http://localhost:5009/api/teemill/dashboard", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("📊 TEEMILL DASHBOARD STATUS:")
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print("❌ Dashboard not accessible")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

if __name__ == "__main__":
    print("💗❤️‍🔥 TEEMILL INTEGRATION TESTER ❤️‍🔥💗")
    print("🫱🏼‍🫲🏻💪🦾 TESTING PASSIVE MERCH SALES 🦾💪🫱🏼‍🫲🏻")
    print("")

    # Test sale
    test_teemill_sale()

    print("")

    # Check dashboard
    check_teemill_dashboard()

    print("")
    print("💗❤️‍🔥 Test complete! Check your money portals for the sale! ❤️‍🔥💗")