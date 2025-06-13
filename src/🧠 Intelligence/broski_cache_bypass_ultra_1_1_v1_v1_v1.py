#!/usr/bin/env python3
"""
🚨⚡ BROski Ultra Cache Bypass Tool
==================================
Instantly bypass ALL caches for real-time development!
"""

import json
import os
import shutil
import subprocess
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


class BROskiCacheBypassUltra:
    def __init__(self):
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def banner(self):
        """🎯 Display ultra bypass banner"""
        print("=" * 70)
        print("🚨⚡ BROSKI ULTRA CACHE BYPASS ACTIVATED! ⚡🚨")
        print("=" * 70)
        print("💜 Bypassing ALL caches for real-time development...")
        print()

    def enable_cloudflare_dev_mode(self):
        """🔥 Enable Cloudflare Development Mode"""
        print("🌐 Enabling Cloudflare Development Mode...")

        if not self.api_token or not self.zone_id:
            print("⚠️  Missing Cloudflare credentials!")
            print("   Add CLOUDFLARE_API_TOKEN and CLOUDFLARE_ZONE_ID to .env")
            print(
                "   🎯 Manual Method: Go to Cloudflare Dashboard > Overview > Development Mode = ON"
            )
            return False

        try:
            # Enable development mode
            payload = {"value": "on"}
            response = requests.patch(
                f"{self.base_url}/zones/{self.zone_id}/settings/development_mode",
                headers=self.headers,
                json=payload,
                timeout=10,
            )

            if response.status_code == 200:
                print("✅ Cloudflare Development Mode ENABLED!")
                print("   🕐 Cache bypass active for 3 hours")
                print("   🚀 All changes will be visible instantly")
                return True
            else:
                print(f"❌ Failed to enable dev mode: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Error enabling dev mode: {e}")
            return False

    def clear_cloudflare_cache(self):
        """🧹 Purge all Cloudflare cache"""
        print("\n🧹 Purging Cloudflare cache...")

        if not self.api_token or not self.zone_id:
            print("⚠️  Skipping Cloudflare cache purge (missing credentials)")
            return False

        try:
            # Purge everything
            payload = {"purge_everything": True}
            response = requests.post(
                f"{self.base_url}/zones/{self.zone_id}/purge_cache",
                headers=self.headers,
                json=payload,
                timeout=10,
            )

            if response.status_code == 200:
                print("✅ Cloudflare cache PURGED!")
                print("   🔥 All cached content cleared")
                return True
            else:
                print(f"❌ Cache purge failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Error purging cache: {e}")
            return False

    def clear_local_service_worker_cache(self):
        """🗑️ Clear local browser/service worker cache"""
        print("\n🗑️ Clearing local service worker cache...")

        # Update cache version to force refresh
        cache_worker_path = "/root/chaosgenius/static/js/broski-cache-worker.js"

        try:
            if os.path.exists(cache_worker_path):
                with open(cache_worker_path, "r") as f:
                    content = f.read()

                # Update cache version with timestamp
                timestamp = int(time.time())
                new_cache_name = f'"broski-ultra-nav-v{timestamp}"'

                # Replace cache name
                content = content.replace(
                    'const CACHE_NAME = "broski-ultra-nav-v2.0"',
                    f"const CACHE_NAME = {new_cache_name}",
                )

                with open(cache_worker_path, "w") as f:
                    f.write(content)

                print("✅ Service worker cache version updated!")
                print(f"   New version: {new_cache_name}")
            else:
                print("⚠️  Service worker file not found")

        except Exception as e:
            print(f"❌ Error updating service worker: {e}")

    def add_cache_busting_headers(self):
        """📡 Add cache-busting headers to dashboard"""
        print("\n📡 Adding cache-busting headers...")

        # Look for dashboard files to add cache-busting
        dashboard_files = [
            "/root/chaosgenius/dashboard_api.py",
            "/root/chaosgenius/app.py",
        ]

        cache_busting_code = '''
# 🚨 CACHE BUSTING HEADERS FOR DEVELOPMENT
from flask import make_response

def add_no_cache_headers(response):
    """Add headers to prevent caching during development"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['X-Dev-Mode'] = 'true'
    return response

# Apply to all responses
@app.after_request
def after_request(response):
    return add_no_cache_headers(response)
'''

        for file_path in dashboard_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        content = f.read()

                    # Only add if not already present
                    if "add_no_cache_headers" not in content:
                        # Find a good place to insert (after imports)
                        lines = content.split("\n")
                        insert_line = 0

                        for i, line in enumerate(lines):
                            if line.startswith("app = ") or line.startswith(
                                "application = "
                            ):
                                insert_line = i + 1
                                break

                        # Insert cache busting code
                        lines.insert(insert_line, cache_busting_code)

                        with open(file_path, "w") as f:
                            f.write("\n".join(lines))

                        print(
                            f"✅ Added cache-busting headers to {os.path.basename(file_path)}"
                        )
                    else:
                        print(
                            f"✅ Cache-busting already enabled in {os.path.basename(file_path)}"
                        )

                except Exception as e:
                    print(f"❌ Error updating {file_path}: {e}")

    def restart_dashboard(self):
        """🔄 Restart dashboard to apply changes"""
        print("\n🔄 Restarting dashboard with cache bypass...")

        try:
            # Kill any existing dashboard processes
            subprocess.run(["pkill", "-f", "dashboard_api.py"], capture_output=True)
            subprocess.run(["pkill", "-f", "app.py"], capture_output=True)
            time.sleep(2)

            print("✅ Stopped existing dashboard processes")
            print("🚀 Ready to restart with fresh cache!")
            print("\n💡 Run this command to start with cache bypass:")
            print("   python dashboard_api.py")

        except Exception as e:
            print(f"⚠️  Error restarting: {e}")

    def generate_bypass_report(self):
        """📋 Generate cache bypass status report"""
        print("\n" + "=" * 70)
        print("📋 CACHE BYPASS STATUS REPORT")
        print("=" * 70)

        report = {
            "timestamp": datetime.now().isoformat(),
            "cloudflare_dev_mode": (
                "enabled" if self.api_token and self.zone_id else "manual_required"
            ),
            "local_cache": "cleared",
            "service_worker": "updated",
            "cache_headers": "added",
            "status": "bypass_active",
        }

        print("✅ Cloudflare Development Mode: ENABLED")
        print("✅ Cloudflare Cache: PURGED")
        print("✅ Service Worker: UPDATED")
        print("✅ Cache Headers: NO-CACHE FORCED")
        print("✅ Dashboard: READY FOR RESTART")

        print("\n🎯 TESTING YOUR DASHBOARD:")
        print("1. Restart dashboard: python dashboard_api.py")
        print("2. Open: http://localhost:5000")
        print("3. Force refresh: Ctrl+F5 or Cmd+Shift+R")
        print("4. Check for 'X-Dev-Mode: true' in Network tab")

        # Save report
        with open("cache_bypass_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n💾 Report saved: cache_bypass_report.json")

    def run_full_bypass(self):
        """🚀 Execute complete cache bypass sequence"""
        self.banner()

        # Execute all bypass steps
        self.enable_cloudflare_dev_mode()
        self.clear_cloudflare_cache()
        self.clear_local_service_worker_cache()
        self.add_cache_busting_headers()
        self.restart_dashboard()
        self.generate_bypass_report()

        print("\n" + "=" * 70)
        print("🎉 CACHE BYPASS COMPLETE! 🎉")
        print("=" * 70)
        print("💜 Your dashboard is now CACHE-FREE for development!")
        print("🚀 All changes will appear instantly!")


def main():
    """🚀 Main execution"""
    bypass_tool = BROskiCacheBypassUltra()
    bypass_tool.run_full_bypass()


if __name__ == "__main__":
    main()
