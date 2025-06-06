#!/usr/bin/env python3
"""
🛡️ BROski Ultra Security Validator
==================================
Scans your HYPERFOCUSzone for security vulnerabilities
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


class BroskiSecurityValidator:
    def __init__(self):
        self.vulnerabilities = []
        self.secure_score = 0
        self.total_checks = 0

    def check_env_security(self):
        """Check .env files for exposed secrets"""
        print("🔐 SCANNING ENVIRONMENT FILES...")

        env_files = [".env", ".env.prod", ".env.dev", ".env.local"]

        for env_file in env_files:
            if Path(env_file).exists():
                with open(env_file, "r") as f:
                    content = f.read()

                # Check for real Discord tokens (they start with specific patterns)
                if re.search(r"DISCORD_BOT_TOKEN=[A-Za-z0-9_-]{20,}\.", content):
                    self.vulnerabilities.append(
                        f"🚨 REAL Discord token found in {env_file}"
                    )

                # Check for real API keys (not placeholders)
                real_keys = re.findall(
                    r"(\w+_API_KEY)=([^YOUR_][A-Za-z0-9_-]{10,})", content
                )
                for key_name, key_value in real_keys:
                    if not key_value.startswith(("YOUR_", "GENERATE_", "sk-YOUR_")):
                        self.vulnerabilities.append(
                            f"🚨 REAL API key exposed: {key_name} in {env_file}"
                        )

        self.total_checks += 1
        if not self.vulnerabilities:
            self.secure_score += 1
            print("✅ Environment files secure")
        else:
            print("❌ Environment security issues found")

    def check_gitignore(self):
        """Verify .gitignore protects sensitive files"""
        print("📁 CHECKING .GITIGNORE PROTECTION...")

        if not Path(".gitignore").exists():
            self.vulnerabilities.append("🚨 No .gitignore file found")
            self.total_checks += 1
            return

        with open(".gitignore", "r") as f:
            gitignore_content = f.read()

        required_entries = [".env", "*.key", "*.pem", "__pycache__", "node_modules"]
        missing_entries = []

        for entry in required_entries:
            if entry not in gitignore_content:
                missing_entries.append(entry)

        if missing_entries:
            self.vulnerabilities.append(
                f"🚨 Missing .gitignore entries: {', '.join(missing_entries)}"
            )

        self.total_checks += 1
        if not missing_entries:
            self.secure_score += 1
            print("✅ .gitignore properly configured")
        else:
            print("❌ .gitignore needs updates")

    def check_file_permissions(self):
        """Check for files with sensitive data"""
        print("🔍 SCANNING FOR SENSITIVE FILES...")

        sensitive_patterns = [
            r".*\.key$",
            r".*private.*\.pem$",
            r".*secret.*\.json$",
            r".*token.*\.txt$",
        ]

        sensitive_files = []
        for pattern in sensitive_patterns:
            sensitive_files.extend(Path(".").glob(pattern))

        for file_path in sensitive_files:
            if file_path.is_file():
                self.vulnerabilities.append(f"🚨 Sensitive file found: {file_path}")

        self.total_checks += 1
        if not sensitive_files:
            self.secure_score += 1
            print("✅ No exposed sensitive files")
        else:
            print("❌ Sensitive files need protection")

    def check_database_security(self):
        """Check database configuration"""
        print("💾 CHECKING DATABASE SECURITY...")

        # Check if database files are in gitignore
        db_files = list(Path(".").glob("*.db*"))

        if Path(".gitignore").exists():
            with open(".gitignore", "r") as f:
                gitignore = f.read()

            protected_dbs = []
            for db_file in db_files:
                if str(db_file) in gitignore or "*.db" in gitignore:
                    protected_dbs.append(db_file)

            if len(protected_dbs) < len(db_files):
                self.vulnerabilities.append("🚨 Some database files not in .gitignore")

        self.total_checks += 1
        if len(db_files) == 0 or all("*.db" in open(".gitignore").read() for _ in [1]):
            self.secure_score += 1
            print("✅ Database security adequate")
        else:
            print("❌ Database security needs attention")

    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("\n🛡️ RUNNING BROSKI SECURITY SCAN...")
        print("=" * 50)

        self.check_env_security()
        self.check_gitignore()
        self.check_file_permissions()
        self.check_database_security()

        # Calculate security score
        security_percentage = (
            (self.secure_score / self.total_checks) * 100
            if self.total_checks > 0
            else 0
        )

        print(
            f"\n🏆 SECURITY SCORE: {self.secure_score}/{self.total_checks} ({security_percentage:.1f}%)"
        )

        if self.vulnerabilities:
            print("\n🚨 VULNERABILITIES FOUND:")
            for vuln in self.vulnerabilities:
                print(f"  {vuln}")

            print("\n🔧 RECOMMENDED ACTIONS:")
            print("  1. Run: cp .env.secure_template .env.local")
            print("  2. Add real API keys to .env.local (not version controlled)")
            print("  3. Update .gitignore with missing entries")
            print("  4. Rotate any exposed API keys")
            print("  5. Use environment-specific configurations")
        else:
            print("✅ NO CRITICAL VULNERABILITIES FOUND!")

        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "security_score": f"{self.secure_score}/{self.total_checks}",
            "security_percentage": security_percentage,
            "vulnerabilities": self.vulnerabilities,
            "status": "SECURE" if security_percentage >= 80 else "NEEDS_ATTENTION",
        }

        with open("security_audit_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Report saved to: security_audit_report.json")

        if security_percentage >= 90:
            print("🏆 BROSKI CREW SECURITY RATING: ULTRA SECURE! 💪")
        elif security_percentage >= 70:
            print("🎯 BROSKI CREW SECURITY RATING: GOOD - Minor fixes needed")
        else:
            print("🚨 BROSKI CREW SECURITY RATING: NEEDS IMMEDIATE ATTENTION!")


if __name__ == "__main__":
    print("🛡️ BROSKI ULTRA SECURITY VALIDATOR")
    print("==================================")
    print("Scanning your HYPERFOCUSzone for vulnerabilities...\n")

    validator = BroskiSecurityValidator()
    validator.generate_security_report()

    print("\n💪 BROski Security Scan Complete!")
    print("Follow the recommended actions to secure your HYPERFOCUSzone!")
