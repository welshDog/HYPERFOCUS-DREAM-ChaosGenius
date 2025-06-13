#!/usr/bin/env python3
"""
🧠💜 BROski Portal Links Manager
Centralized management of all ChaosGenius portal URLs and endpoints
"""

import json
import os
import webbrowser
from datetime import datetime
from typing import Any, Dict, Optional

import requests


class PortalLinksManager:
    def __init__(self, config_path: str = "portal_links_config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load portal configuration from JSON file"""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Config file not found: {self.config_path}")
            return {}

    def save_config(self):
        """Save current configuration to JSON file"""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        print(f"✅ Configuration saved to {self.config_path}")

    def get_portal_url(self, portal_name: str) -> Optional[str]:
        """Get URL for a specific portal"""
        return self.config.get("main_portals", {}).get(portal_name, {}).get("url")

    def get_api_endpoint(self, endpoint_name: str) -> Optional[str]:
        """Get URL for a specific API endpoint"""
        return self.config.get("api_endpoints", {}).get(endpoint_name, {}).get("url")

    def check_portal_status(self, portal_name: str) -> bool:
        """Check if a portal is accessible"""
        url = self.get_portal_url(portal_name)
        if not url:
            print(f"❌ Portal '{portal_name}' not found in config")
            return False

        try:
            response = requests.get(url, timeout=5)
            is_active = response.status_code == 200
            status = "🟢 ONLINE" if is_active else "🔴 OFFLINE"
            print(f"{status} {portal_name}: {url}")
            return is_active
        except requests.exceptions.RequestException:
            print(f"🔴 OFFLINE {portal_name}: {url} (Connection failed)")
            return False

    def check_all_portals(self) -> Dict[str, bool]:
        """Check status of all configured portals"""
        print("🚀 Checking all portal statuses...\n")
        statuses = {}

        for portal_name in self.config.get("main_portals", {}):
            statuses[portal_name] = self.check_portal_status(portal_name)

        print(f"\n📊 Portal Status Summary:")
        online_count = sum(statuses.values())
        total_count = len(statuses)
        print(f"   Online: {online_count}/{total_count}")

        return statuses

    def open_portal(self, portal_name: str):
        """Open a portal in the default browser"""
        url = self.get_portal_url(portal_name)
        if url:
            print(f"🌐 Opening {portal_name}: {url}")
            webbrowser.open(url)
        else:
            print(f"❌ Portal '{portal_name}' not found")

    def list_all_portals(self):
        """Display all configured portals with their info"""
        print("🌟 ChaosGenius Portal Directory:\n")

        portals = self.config.get("main_portals", {})
        for name, info in portals.items():
            status_emoji = "🟢" if info.get("status") == "active" else "🟡"
            print(f"{status_emoji} {info.get('name', name)}")
            print(f"   URL: {info.get('url')}")
            print(f"   Type: {info.get('type', 'unknown')}")
            print(f"   Status: {info.get('status', 'unknown')}")
            print(f"   Description: {info.get('description', 'No description')}")
            print()

    def get_quick_links(self) -> Dict[str, str]:
        """Get commonly used portal links for quick access"""
        quick_links = {}

        # Main portals
        portals = self.config.get("main_portals", {})
        for name, info in portals.items():
            if info.get("status") == "active":
                quick_links[name] = info.get("url")

        # External links
        external = self.config.get("external_links", {})
        quick_links.update(external)

        return quick_links

    def generate_html_portal_page(self, output_path: str = "portal_directory.html"):
        """Generate an HTML page with all portal links"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 ChaosGenius Portal Directory</title>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .portal-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .portal-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .portal-card:hover {
            transform: translateY(-5px);
        }
        .portal-link {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 25px;
            margin-top: 10px;
            transition: background 0.3s ease;
        }
        .portal-link:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        .status-active { color: #4ade80; }
        .status-planned { color: #fbbf24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠💜 ChaosGenius Portal Directory</h1>
            <p>Your centralized hub for all ADHD-optimized productivity portals</p>
        </div>

        <div class="portal-grid">
"""

        # Add portal cards
        portals = self.config.get("main_portals", {})
        for name, info in portals.items():
            status_class = f"status-{info.get('status', 'unknown')}"
            html_content += f"""
            <div class="portal-card">
                <h3>{info.get('name', name)}</h3>
                <p>{info.get('description', 'No description available')}</p>
                <p class="{status_class}">Status: {info.get('status', 'Unknown').upper()}</p>
                <a href="{info.get('url')}" class="portal-link" target="_blank">🚀 Launch Portal</a>
            </div>
"""

        html_content += """
        </div>
    </div>

    <script>
        // Auto-refresh status every 30 seconds
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

        with open(output_path, "w") as f:
            f.write(html_content)
        print(f"✅ Portal directory page generated: {output_path}")

    def update_portal_status(self, portal_name: str, status: str):
        """Update the status of a specific portal"""
        if portal_name in self.config.get("main_portals", {}):
            self.config["main_portals"][portal_name]["status"] = status
            self.config["portal_config"]["last_updated"] = datetime.now().strftime(
                "%Y-%m-%d"
            )
            self.save_config()
            print(f"✅ Updated {portal_name} status to: {status}")
        else:
            print(f"❌ Portal '{portal_name}' not found")


def main():
    """Main CLI interface for portal management"""
    manager = PortalLinksManager()

    print("🧠💜 ChaosGenius Portal Links Manager")
    print("=" * 50)

    while True:
        print("\n🚀 Available Commands:")
        print("1. List all portals")
        print("2. Check portal statuses")
        print("3. Open portal in browser")
        print("4. Generate HTML portal page")
        print("5. Update portal status")
        print("6. Show quick links")
        print("0. Exit")

        choice = input("\n💜 Enter your choice (0-6): ").strip()

        if choice == "0":
            print("👋 See you later, ADHD warrior!")
            break
        elif choice == "1":
            manager.list_all_portals()
        elif choice == "2":
            manager.check_all_portals()
        elif choice == "3":
            portal_name = input("🌐 Enter portal name: ").strip()
            manager.open_portal(portal_name)
        elif choice == "4":
            manager.generate_html_portal_page()
        elif choice == "5":
            portal_name = input("📝 Enter portal name: ").strip()
            status = input("📊 Enter new status (active/planned/disabled): ").strip()
            manager.update_portal_status(portal_name, status)
        elif choice == "6":
            quick_links = manager.get_quick_links()
            print("\n⚡ Quick Links:")
            for name, url in quick_links.items():
                print(f"   {name}: {url}")
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
