#!/usr/bin/env python3
"""
🦙 Pinta IPFS Setup Helper for ChaosGenius
==========================================
Helper script to test Pinta IPFS integration and verify API connectivity
"""

import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


class PintaIPFSSetupHelper:
    def __init__(self):
        # Use the correct variable names from your .env file
        self.api_key = os.getenv("PINTA_IPSF_API_KEY")  # Fixed variable name
        self.api_secret = os.getenv("PINTA_IPSF_API_SECRET")  # Fixed variable name
        self.jwt_token = os.getenv("PINTA_IPSF_JWT")
        self.base_url = "https://api.pinata.cloud"

    def verify_credentials(self):
        """Verify Pinta API credentials"""
        print("🔍 Verifying Pinta IPFS API credentials...")

        if not self.api_key or not self.api_secret:
            print("❌ API credentials not found in .env file")
            return False

        print(f"   API Key: {self.api_key[:10]}...{self.api_key[-5:]}")
        print(f"   API Secret: {self.api_secret[:10]}...{self.api_secret[-10:]}")

        try:
            headers = {
                "pinata_api_key": self.api_key,
                "pinata_secret_api_key": self.api_secret,
            }

            response = requests.get(
                f"{self.base_url}/data/testAuthentication", headers=headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                print("✅ Pinta API credentials are valid!")
                print(f"   Message: {data.get('message', 'Authentication successful')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Error testing authentication: {e}")
            return False

    def test_pin_list(self):
        """Test fetching pinned content"""
        print("\n📋 Testing pinned content retrieval...")

        try:
            headers = {
                "pinata_api_key": self.api_key,
                "pinata_secret_api_key": self.api_secret,
            }

            response = requests.get(
                f"{self.base_url}/data/pinList?status=pinned",
                headers=headers,
                timeout=15,
            )

            if response.status_code == 200:
                data = response.json()
                pin_count = data.get("count", 0)
                pins = data.get("rows", [])

                print(f"✅ Found {pin_count} pinned items")
                if pins:
                    print("   Recent pins:")
                    for pin in pins[:3]:  # Show first 3
                        name = pin.get("metadata", {}).get("name", "Unnamed")
                        hash_val = pin.get("ipfs_pin_hash", "")[:20] + "..."
                        date = pin.get("date_pinned", "Unknown date")
                        print(f"   • {name} ({hash_val}) - {date}")
                else:
                    print("   No pins found in account")

                return data
            else:
                print(f"❌ Failed to fetch pin list: {response.status_code}")
                print(f"   Response: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Error fetching pin list: {e}")
            return None

    def test_json_upload(self):
        """Test uploading JSON content to IPFS"""
        print("\n📤 Testing JSON upload to IPFS...")

        try:
            headers = {
                "pinata_api_key": self.api_key,
                "pinata_secret_api_key": self.api_secret,
                "Content-Type": "application/json",
            }

            test_data = {
                "project": "ChaosGenius",
                "test_timestamp": datetime.now().isoformat(),
                "message": "Pinta IPFS integration test",
                "status": "testing",
            }

            upload_payload = {
                "pinataContent": test_data,
                "pinataMetadata": {
                    "name": f"chaosgenius_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "description": "ChaosGenius Pinta IPFS integration test",
                },
            }

            response = requests.post(
                f"{self.base_url}/pinning/pinJSONToIPFS",
                headers=headers,
                json=upload_payload,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                ipfs_hash = result.get("IpfsHash")
                print("✅ JSON upload successful!")
                print(f"   IPFS Hash: {ipfs_hash}")
                print(f"   Gateway URL: https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
                print(f"   Size: {result.get('PinSize', 'Unknown')} bytes")
                return result
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Error during upload: {e}")
            return None

    def get_account_info(self):
        """Get account usage information"""
        print("\n📊 Checking account information...")

        try:
            headers = {
                "pinata_api_key": self.api_key,
                "pinata_secret_api_key": self.api_secret,
            }

            response = requests.get(
                f"{self.base_url}/data/userPinnedDataTotal", headers=headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                pin_count = data.get("pin_count", 0)
                pin_size_total = data.get("pin_size_total", 0)

                print("✅ Account information:")
                print(f"   Total pins: {pin_count:,}")
                print(
                    f"   Total size: {pin_size_total:,} bytes ({pin_size_total/1024/1024:.2f} MB)"
                )
                return data
            else:
                print(f"❌ Failed to get account info: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error getting account info: {e}")
            return None

    def generate_setup_report(self):
        """Generate comprehensive Pinta IPFS setup report"""
        print("=" * 60)
        print("🦙 PINTA IPFS SETUP REPORT")
        print("=" * 60)

        # Credential verification
        credentials_valid = self.verify_credentials()

        # Account info
        account_info = self.get_account_info() if credentials_valid else None

        # Pin list test
        pin_data = self.test_pin_list() if credentials_valid else None

        # Upload test
        upload_result = self.test_json_upload() if credentials_valid else None

        # Summary
        print("\n" + "=" * 60)
        print("📋 PINTA IPFS SUMMARY")
        print("=" * 60)
        print(f"✅ API Credentials: {'Valid' if credentials_valid else 'Invalid'}")
        print(f"📊 Account Access: {'Working' if account_info else 'Failed'}")
        print(f"📋 Pin Listing: {'Working' if pin_data else 'Failed'}")
        print(f"📤 Upload Test: {'Successful' if upload_result else 'Failed'}")

        if credentials_valid:
            if account_info:
                print(f"📦 Total Pins: {account_info.get('pin_count', 0):,}")
                print(
                    f"💾 Storage Used: {account_info.get('pin_size_total', 0)/1024/1024:.2f} MB"
                )

        # Save report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "credentials_valid": credentials_valid,
            "account_info": account_info,
            "pin_data_sample": pin_data.get("rows", [])[:5] if pin_data else [],
            "upload_test": upload_result,
            "status": "configured" if credentials_valid else "setup_needed",
        }

        with open("pinta_ipfs_setup_report.json", "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"\n💾 Report saved to: pinta_ipfs_setup_report.json")

        if not credentials_valid:
            print("\n🚀 NEXT STEPS:")
            print("1. Visit https://app.pinata.cloud/developers/api-keys")
            print("2. Create a new API key with required permissions")
            print("3. Update your .env file with the new credentials")
            print("4. Re-run this script to verify setup")
        else:
            print("\n🎉 Pinta IPFS integration is working perfectly!")
            print(
                "   Your ChaosGenius project can now use IPFS for decentralized storage"
            )


def main():
    """Main entry point"""
    helper = PintaIPFSSetupHelper()
    helper.generate_setup_report()


if __name__ == "__main__":
    main()
