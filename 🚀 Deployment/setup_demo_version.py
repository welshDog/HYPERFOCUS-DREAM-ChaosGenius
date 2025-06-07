#!/usr/bin/env python3
"""
🔒 HYPERFOCUS DREAM - Demo Version Setup
====================================
Prepares the repo for public release while keeping the good stuff private.
"""

import os
import shutil
import json
from datetime import datetime


class DemoSetup:
    def __init__(self):
        self.demo_files = [
            "README.md",
            "requirements.txt",
            "dashboard_api.py",
            "health_check.py",
            "chaos_test_suite.py",
            "DISCUSSION.md",
            ".gitignore",
            "dashboard.html",
            "static/",
            "api/etsy_connector.py",  # Sample API
            "Welcome & Onboarding/",
            "generated_docs/",
        ]

        self.private_files = [
            "ai_modules/broski/",
            "ultra_ai/",
            "chaos_modules/",
            "Business Data/",
            "logs/",
            "chaosgenius.db",
            ".env",
            "config/api_keys.py",
            "discord_token.txt",
            "etsy_credentials.json"
        ]

    def check_gitignore_coverage(self):
        """Verify .gitignore covers all sensitive files"""
        print("🔍 Checking .gitignore coverage...")

        try:
            with open('.gitignore', 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
        except UnicodeDecodeError:
            with open('.gitignore', 'r', encoding='latin-1') as f:
                gitignore_content = f.read()

        covered = []
        missing = []

        for private_file in self.private_files:
            if any(pattern in gitignore_content for pattern in [
                private_file,
                private_file.replace('/', ''),
                private_file.split('/')[0]
            ]):
                covered.append(private_file)
            else:
                missing.append(private_file)

        print(f"✅ Protected: {len(covered)} files/folders")
        if missing:
            print(f"⚠️  Missing protection: {missing}")
        else:
            print("🔒 All sensitive files are protected!")

        return len(missing) == 0

    def create_demo_manifest(self):
        """Create a manifest of what's included in demo"""
        demo_manifest = {
            "demo_version": "1.0",
            "created": datetime.now().isoformat(),
            "included_features": [
                "Dashboard preview",
                "Sample API endpoints",
                "Health monitoring",
                "Basic documentation",
                "Test suite (limited)"
            ],
            "hidden_features": [
                "AI Squad automation",
                "BROski assistant core",
                "Advanced TikTok/Etsy sync",
                "Real business data",
                "Discord bot full features"
            ],
            "public_files": self.demo_files,
            "collaboration_info": {
                "discussions_enabled": True,
                "contribution_welcome": True,
                "contact_method": "GitHub Discussions"
            }
        }

        with open('DEMO_MANIFEST.json', 'w') as f:
            json.dump(demo_manifest, f, indent=2)

        print("📋 Demo manifest created!")

    def verify_demo_ready(self):
        """Run final checks before going public"""
        print("\n🚀 DEMO VERSION READINESS CHECK")
        print("=" * 40)

        checks = {
            "README.md exists": os.path.exists("README.md"),
            ".gitignore configured": os.path.exists(".gitignore"),
            "Discussion starter ready": os.path.exists("DISCUSSION.md"),
            "No .env in root": not os.path.exists(".env"),
            "No database exposed": not any(f.endswith('.db') for f in os.listdir('.') if os.path.isfile(f)),
            "Gitignore coverage": self.check_gitignore_coverage()
        }

        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check}")

        all_passed = all(checks.values())

        if all_passed:
            print("\n🎉 DEMO VERSION IS READY FOR PUBLIC RELEASE!")
            print("Next steps:")
            print("1. Push to GitHub")
            print("2. Enable Discussions in repo settings")
            print("3. Pin welcome message from DISCUSSION.md")
            print("4. Share with the community!")
        else:
            print("\n⚠️  Fix the failed checks before going public")

        return all_passed

    def run_full_setup(self):
        """Execute complete demo setup process"""
        print("🔒 Setting up Hyperfocus Dream demo version...")

        # Create manifest
        self.create_demo_manifest()

        # Run verification
        ready = self.verify_demo_ready()

        if ready:
            print("\n✨ Demo setup complete! Ready to reel in the legends! 🧠💜")

        return ready


if __name__ == "__main__":
    setup = DemoSetup()
    setup.run_full_setup()
