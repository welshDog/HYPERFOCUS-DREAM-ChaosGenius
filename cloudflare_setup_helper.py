#!/usr/bin/env python3
"""
🌐 Cloudflare Setup Helper for ChaosGenius
==========================================
Helper script to set up Cloudflare integration and test API connectivity
"""

import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


class CloudflareSetupHelper:
    def __init__(self):
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def verify_token(self):
        """Verify API token is valid"""
        print("🔍 Verifying Cloudflare API token...")

        try:
            response = requests.get(
                f"{self.base_url}/user/tokens/verify", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                print("✅ Token is valid and active!")
                print(f"   Token ID: {data['result']['id']}")
                print(f"   Status: {data['result']['status']}")
                return True
            else:
                print(f"❌ Token verification failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error verifying token: {e}")
            return False

    def list_zones(self):
        """List all zones in the account"""
        print("\n📋 Checking available zones...")

        try:
            response = requests.get(
                f"{self.base_url}/zones", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                zones = data.get("result", [])

                if zones:
                    print(f"✅ Found {len(zones)} zone(s):")
                    for zone in zones:
                        print(f"   • {zone['name']} (ID: {zone['id']})")
                        print(f"     Status: {zone['status']}")
                        print(f"     Plan: {zone['plan']['name']}")
                else:
                    print("📭 No zones found in your Cloudflare account")
                    print("\n💡 To add hyperfocuszone.com:")
                    print("   1. Visit https://dash.cloudflare.com")
                    print("   2. Click 'Add a Site'")
                    print("   3. Enter 'hyperfocuszone.com'")
                    print("   4. Follow the nameserver setup instructions")

                return zones
            else:
                print(f"❌ Failed to fetch zones: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Error fetching zones: {e}")
            return []

    def test_analytics(self, zone_id=None):
        """Test analytics API with real or mock data"""
        print("\n📊 Testing analytics API...")

        if zone_id:
            try:
                response = requests.get(
                    f"{self.base_url}/zones/{zone_id}/analytics/dashboard",
                    headers=self.headers,
                    timeout=10,
                )

                if response.status_code == 200:
                    data = response.json().get("result", {})
                    totals = data.get("totals", {})

                    print("✅ Real analytics data:")
                    print(f"   Requests: {totals.get('requests', {}).get('all', 0):,}")
                    print(
                        f"   Bandwidth: {totals.get('bandwidth', {}).get('all', 0):,} bytes"
                    )
                    print(f"   Threats: {totals.get('threats', {}).get('all', 0):,}")
                    return data
                else:
                    print(f"❌ Analytics request failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Analytics error: {e}")

        # Fallback to enhanced mock data
        print("📊 Using enhanced mock data for demo:")
        mock_data = {
            "requests": 45230,
            "bandwidth": 1024000000,  # 1GB
            "threats_blocked": 127,
            "status": "mock_data",
            "period": "last_24h",
        }

        for key, value in mock_data.items():
            if key == "bandwidth":
                print(f"   {key}: {value:,} bytes ({value/1024/1024:.1f} MB)")
            elif isinstance(value, int) and value > 1000:
                print(f"   {key}: {value:,}")
            else:
                print(f"   {key}: {value}")

        return mock_data

    def generate_setup_report(self):
        """Generate a comprehensive setup report"""
        print("=" * 60)
        print("🌐 CLOUDFLARE SETUP REPORT")
        print("=" * 60)

        # Token verification
        token_valid = self.verify_token()

        # Zone listing
        zones = self.list_zones()

        # Analytics test
        zone_id = zones[0]["id"] if zones else None
        analytics = self.test_analytics(zone_id)

        # Summary
        print("\n" + "=" * 60)
        print("📋 SETUP SUMMARY")
        print("=" * 60)
        print(f"✅ API Token: {'Valid' if token_valid else 'Invalid'}")
        print(f"🌐 Zones Found: {len(zones)}")
        print(f"📊 Analytics: {'Real Data' if zone_id else 'Mock Data'}")

        if not zones:
            print("\n🚀 NEXT STEPS:")
            print("1. Add hyperfocuszone.com to your Cloudflare account")
            print("2. Update nameservers as instructed by Cloudflare")
            print("3. Wait for DNS propagation (24-48 hours)")
            print("4. Re-run this script to verify setup")
        else:
            print("\n🎉 Your Cloudflare integration is ready!")
            print("   Your ChaosGenius dashboard can now use real analytics data")

        # Save report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "token_valid": token_valid,
            "zones_count": len(zones),
            "zones": zones,
            "analytics_sample": analytics,
            "status": "configured" if zones else "setup_needed",
        }

        with open("cloudflare_setup_report.json", "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"\n💾 Report saved to: cloudflare_setup_report.json")


def main():
    """Main entry point"""
    helper = CloudflareSetupHelper()
    helper.generate_setup_report()


if __name__ == "__main__":
    main()
