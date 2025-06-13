#!/usr/bin/env python3
"""
🚀💥 BROSKI .ENV CLEANUP & MANAGEMENT SCRIPT 💥🚀
Clean up scattered .env files and consolidate everything!
By Command of Chief Lyndz - BROski∞ Configuration Master
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class BROskiEnvManager:
    """🔧 LEGENDARY .env file management system"""

    def __init__(self):
        self.root_path = Path("/root/chaosgenius")
        self.master_env = self.root_path / ".env"
        self.backup_dir = self.root_path / "🔐 Secure Backups"

    def find_all_env_files(self):
        """🔍 Find all .env files in the workspace"""
        env_files = []

        # Search patterns for .env files
        patterns = ["**/.env*", "**/config/.env*", "**/.env.*"]

        for pattern in patterns:
            for file_path in self.root_path.glob(pattern):
                if file_path != self.master_env and file_path.is_file():
                    env_files.append(file_path)

        return env_files

    def backup_env_files(self, env_files):
        """💾 Backup existing .env files before cleanup"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_report = {
            "timestamp": timestamp,
            "backed_up_files": [],
            "master_env_location": str(self.master_env),
        }

        for env_file in env_files:
            try:
                # Create relative path for backup name
                rel_path = env_file.relative_to(self.root_path)
                backup_name = f"{rel_path.as_posix().replace('/', '_')}_{timestamp}"
                backup_path = self.backup_dir / backup_name

                # Copy the file
                shutil.copy2(env_file, backup_path)
                backup_report["backed_up_files"].append(
                    {
                        "original": str(env_file),
                        "backup": str(backup_path),
                        "size": env_file.stat().st_size,
                    }
                )

                print(f"✅ Backed up: {rel_path} → {backup_name}")

            except Exception as e:
                print(f"❌ Failed to backup {env_file}: {e}")

        # Save backup report
        report_file = self.backup_dir / f"env_cleanup_report_{timestamp}.json"
        with open(report_file, "w") as f:
            json.dump(backup_report, f, indent=2)

        return backup_report

    def remove_duplicate_env_files(self, env_files, backup_first=True):
        """🧹 Remove duplicate .env files after backing them up"""
        if backup_first:
            backup_report = self.backup_env_files(env_files)
            print(f"\n💾 Backup completed! Report saved.")

        removed_files = []

        for env_file in env_files:
            try:
                rel_path = env_file.relative_to(self.root_path)
                env_file.unlink()
                removed_files.append(str(rel_path))
                print(f"🗑️ Removed: {rel_path}")

            except Exception as e:
                print(f"❌ Failed to remove {env_file}: {e}")

        return removed_files

    def create_env_symlinks(self):
        """🔗 Create symbolic links to master .env in key directories"""
        link_directories = ["broski_auth_system", "config", "⚙️ Configuration"]

        created_links = []

        for dir_name in link_directories:
            dir_path = self.root_path / dir_name
            if dir_path.exists():
                link_path = dir_path / ".env"

                try:
                    # Remove existing file/link
                    if link_path.exists() or link_path.is_symlink():
                        link_path.unlink()

                    # Create relative symlink
                    relative_master = os.path.relpath(self.master_env, dir_path)
                    link_path.symlink_to(relative_master)
                    created_links.append(str(link_path))
                    print(f"🔗 Created symlink: {dir_name}/.env → {relative_master}")

                except Exception as e:
                    print(f"❌ Failed to create symlink in {dir_name}: {e}")

        return created_links

    def validate_master_env(self):
        """✅ Validate the master .env file"""
        if not self.master_env.exists():
            print("❌ Master .env file not found!")
            return False

        try:
            with open(self.master_env, "r") as f:
                content = f.read()

            # Check for key sections
            required_sections = [
                "DISCORD_BOT_TOKEN",
                "FLASK_SECRET_KEY",
                "DATABASE_URL",
                "BROSKI_ADMIN_PASSWORD",
            ]

            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)

            if missing_sections:
                print(f"⚠️ Missing sections in master .env: {missing_sections}")
                return False

            print("✅ Master .env file validated successfully!")
            return True

        except Exception as e:
            print(f"❌ Error validating master .env: {e}")
            return False

    def generate_env_summary(self):
        """📊 Generate summary of .env configuration"""
        try:
            with open(self.master_env, "r") as f:
                lines = f.readlines()

            total_lines = len(lines)
            config_lines = len(
                [
                    line
                    for line in lines
                    if "=" in line and not line.strip().startswith("#")
                ]
            )
            comment_lines = len(
                [line for line in lines if line.strip().startswith("#")]
            )

            summary = {
                "total_lines": total_lines,
                "config_entries": config_lines,
                "comment_lines": comment_lines,
                "file_size_kb": round(self.master_env.stat().st_size / 1024, 2),
                "last_modified": datetime.fromtimestamp(
                    self.master_env.stat().st_mtime
                ).isoformat(),
            }

            return summary

        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return None


def main():
    """🚀 Main cleanup and consolidation process"""
    print("🚀💥 BROSKI .ENV CLEANUP & CONSOLIDATION 💥🚀")
    print("=" * 60)

    manager = BROskiEnvManager()

    # Find all scattered .env files
    print("🔍 Scanning for scattered .env files...")
    env_files = manager.find_all_env_files()

    print(f"\n📊 FOUND {len(env_files)} SCATTERED .ENV FILES:")
    for env_file in env_files:
        rel_path = env_file.relative_to(manager.root_path)
        size_kb = round(env_file.stat().st_size / 1024, 2)
        print(f"   📄 {rel_path} ({size_kb} KB)")

    if not env_files:
        print("✅ No scattered .env files found - system is already clean!")
    else:
        # Backup and remove duplicates
        print(f"\n💾 Backing up and removing {len(env_files)} duplicate .env files...")
        removed_files = manager.remove_duplicate_env_files(env_files)
        print(f"✅ Removed {len(removed_files)} duplicate .env files")

    # Create symlinks for convenience
    print(f"\n🔗 Creating convenient symlinks...")
    created_links = manager.create_env_symlinks()
    print(f"✅ Created {len(created_links)} symlinks")

    # Validate master .env
    print(f"\n✅ Validating master .env file...")
    is_valid = manager.validate_master_env()

    # Generate summary
    summary = manager.generate_env_summary()
    if summary:
        print(f"\n📊 MASTER .ENV SUMMARY:")
        print(f"   📄 Total lines: {summary['total_lines']}")
        print(f"   ⚙️ Config entries: {summary['config_entries']}")
        print(f"   💬 Comment lines: {summary['comment_lines']}")
        print(f"   📦 File size: {summary['file_size_kb']} KB")

    print(f"\n🎉 LEGENDARY .ENV CONSOLIDATION COMPLETE! 🎉")
    print("=" * 60)
    print("🔥 BENEFITS OF ONE MASTER .ENV:")
    print("   ✅ No more scattered configuration files")
    print("   ✅ Single source of truth for all settings")
    print("   ✅ Easy to backup and version control")
    print("   ✅ Consistent configuration across all services")
    print("   ✅ Convenient symlinks for legacy compatibility")
    print("\n💡 LOCATION: /root/chaosgenius/.env")
    print("🔗 SYMLINKS: Available in key directories")
    print("💾 BACKUPS: Stored in 🔐 Secure Backups/")


if __name__ == "__main__":
    main()
