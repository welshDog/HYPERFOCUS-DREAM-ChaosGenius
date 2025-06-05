#!/usr/bin/env python3
"""
💾 BROSKI X EMPIRE - BACKUP ENGINE + SNAPSHOT TOOL
Git auto-sync, full backups, and Discord alerts
"""
import asyncio
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

import discord
import git
from discord.ext import tasks


class BROskiBackupEngine:
    def __init__(self, discord_webhook_url=None):
        self.project_root = Path("/root/chaosgenius")
        self.backup_dir = self.project_root / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        self.discord_webhook = discord_webhook_url

        # Initialize git repo if needed
        self.init_git_repo()

        # Start backup tasks
        self.schedule_backups()

    def init_git_repo(self):
        """🔧 Initialize Git repository if not present"""
        try:
            self.repo = git.Repo(self.project_root)
            print("✅ Git repository found!")
        except git.exc.InvalidGitRepositoryError:
            print("🔧 Initializing Git repository...")
            self.repo = git.Repo.init(self.project_root)

            # Create .gitignore
            gitignore_content = """
# Sensitive files
*.key
*_SECURE.json
*.db
*.log

# Environment files
.env
*.env

# Python cache
__pycache__/
*.pyc
*.pyo

# Backup files
backups/
*.backup
*.bak

# Temporary files
*.tmp
*.temp
"""
            with open(self.project_root / ".gitignore", "w") as f:
                f.write(gitignore_content)

            print("✅ Git repository initialized!")

    def create_full_backup(self):
        """📦 Create complete system backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"broski_empire_backup_{timestamp}"

        print(f"📦 Creating full backup: {backup_name}")

        # Create backup metadata
        backup_info = {
            "timestamp": timestamp,
            "backup_name": backup_name,
            "git_commit": (
                str(self.repo.head.commit) if self.repo.head.is_valid() else "initial"
            ),
            "file_count": 0,
            "size_mb": 0,
            "databases_backed_up": [],
            "critical_files": [],
        }

        # Create backup directory
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)

        # 1. Backup all databases
        db_backup_dir = backup_path / "databases"
        db_backup_dir.mkdir(exist_ok=True)

        db_files = list(self.project_root.glob("*.db"))
        for db_file in db_files:
            if db_file.exists():
                backup_db_path = db_backup_dir / db_file.name
                shutil.copy2(db_file, backup_db_path)
                backup_info["databases_backed_up"].append(db_file.name)
                print(f"📊 Backed up database: {db_file.name}")

        # 2. Backup critical configuration files
        config_backup_dir = backup_path / "configs"
        config_backup_dir.mkdir(exist_ok=True)

        critical_files = [
            "broski_token_config.json",
            "dashboard_api.py",
            "chaosgenius_discord_bot.py",
            "production_deploy_config.py",
            "docker-compose.yml",
            "Dockerfile",
            "ecosystem.config.js",
        ]

        for file_name in critical_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                shutil.copy2(file_path, config_backup_dir / file_name)
                backup_info["critical_files"].append(file_name)
                print(f"⚙️ Backed up config: {file_name}")

        # 3. Backup AI modules and scripts
        modules_to_backup = ["ai_modules", "scripts", "Setup & Deploy"]
        for module_dir in modules_to_backup:
            module_path = self.project_root / module_dir
            if module_path.exists() and module_path.is_dir():
                backup_module_path = backup_path / module_dir
                shutil.copytree(module_path, backup_module_path, dirs_exist_ok=True)
                print(f"🧠 Backed up module: {module_dir}")

        # 4. Create compressed archive
        zip_path = self.backup_dir / f"{backup_name}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(backup_path)
                    zipf.write(file_path, arcname)
                    backup_info["file_count"] += 1

        # Calculate backup size
        backup_info["size_mb"] = round(zip_path.stat().st_size / (1024 * 1024), 2)

        # Save backup metadata
        metadata_path = backup_path / "backup_info.json"
        with open(metadata_path, "w") as f:
            json.dump(backup_info, f, indent=2)

        # Cleanup temporary backup directory
        shutil.rmtree(backup_path)

        print(f"✅ Backup completed: {backup_info['size_mb']} MB")
        return backup_info

    def git_auto_sync(self):
        """🔄 Auto-sync with Git repository"""
        try:
            # Add all files except ignored ones
            self.repo.git.add(A=True)

            # Check if there are changes to commit
            if self.repo.index.diff("HEAD"):
                # Create commit message
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_message = f"🤖 Auto-sync: BROski Empire update - {timestamp}"

                # Commit changes
                commit = self.repo.index.commit(commit_message)

                print(f"📝 Git commit created: {commit.hexsha[:8]}")

                # Try to push if remote exists
                try:
                    origin = self.repo.remote("origin")
                    origin.push()
                    print("🚀 Changes pushed to remote repository!")
                except:
                    print("⚠️ No remote repository configured for push")

                return True
            else:
                print("✅ No changes to commit")
                return False

        except Exception as e:
            print(f"❌ Git sync error: {e}")
            return False

    def cleanup_old_backups(self, keep_count=10):
        """🧹 Remove old backup files to save space"""
        backup_files = sorted(
            [f for f in self.backup_dir.glob("*.zip")],
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )

        if len(backup_files) > keep_count:
            files_to_remove = backup_files[keep_count:]
            for old_backup in files_to_remove:
                old_backup.unlink()
                print(f"🗑️ Removed old backup: {old_backup.name}")

            print(f"🧹 Cleanup complete: {len(files_to_remove)} old backups removed")

    async def send_discord_alert(self, backup_info):
        """📢 Send Discord notification about new backup"""
        if not self.discord_webhook:
            return

        try:
            import aiohttp

            embed = {
                "title": "💾 New Backup Created!",
                "description": "BROski Empire has been successfully backed up!",
                "color": 0x00FF00,
                "fields": [
                    {
                        "name": "📦 Backup Size",
                        "value": f"{backup_info['size_mb']} MB",
                        "inline": True,
                    },
                    {
                        "name": "📁 Files Backed Up",
                        "value": str(backup_info["file_count"]),
                        "inline": True,
                    },
                    {
                        "name": "📊 Databases",
                        "value": str(len(backup_info["databases_backed_up"])),
                        "inline": True,
                    },
                    {
                        "name": "🕐 Timestamp",
                        "value": backup_info["timestamp"],
                        "inline": False,
                    },
                ],
                "footer": {"text": "BROski Empire Backup System"},
            }

            webhook_data = {"embeds": [embed], "username": "BROski Backup Bot"}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.discord_webhook, json=webhook_data
                ) as response:
                    if response.status == 204:
                        print("📢 Discord backup alert sent!")
                    else:
                        print(f"⚠️ Discord alert failed: {response.status}")

        except Exception as e:
            print(f"❌ Discord alert error: {e}")

    def schedule_backups(self):
        """⏰ Schedule automatic backups"""
        print("⏰ Starting automatic backup scheduler...")

        # Start background task for periodic backups
        asyncio.create_task(self.backup_loop())

    async def backup_loop(self):
        """🔄 Main backup loop"""
        while True:
            try:
                # Wait 24 hours between backups
                await asyncio.sleep(24 * 60 * 60)  # 24 hours

                print("🔄 Starting scheduled backup...")

                # Git sync first
                git_synced = self.git_auto_sync()

                # Create full backup
                backup_info = self.create_full_backup()

                # Cleanup old backups
                self.cleanup_old_backups()

                # Send Discord alert
                await self.send_discord_alert(backup_info)

                print("✅ Scheduled backup completed!")

            except Exception as e:
                print(f"❌ Backup loop error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

    def emergency_backup(self):
        """🚨 Create emergency backup (manual trigger)"""
        print("🚨 EMERGENCY BACKUP INITIATED!")

        # Git sync
        self.git_auto_sync()

        # Create backup
        backup_info = self.create_full_backup()

        # Send immediate alert
        asyncio.create_task(self.send_discord_alert(backup_info))

        return backup_info

    def restore_from_backup(self, backup_name):
        """🔄 Restore system from backup"""
        backup_zip = self.backup_dir / f"{backup_name}.zip"

        if not backup_zip.exists():
            print(f"❌ Backup not found: {backup_name}")
            return False

        print(f"🔄 Restoring from backup: {backup_name}")

        # Create restore directory
        restore_dir = self.backup_dir / f"restore_{backup_name}"
        restore_dir.mkdir(exist_ok=True)

        # Extract backup
        with zipfile.ZipFile(backup_zip, "r") as zipf:
            zipf.extractall(restore_dir)

        print("✅ Backup extraction completed!")
        print(f"📁 Restored files are in: {restore_dir}")
        print("⚠️ Manual verification and copying required for safety!")

        return True


# CLI interface for manual backup operations
if __name__ == "__main__":
    import sys

    # Discord webhook URL (replace with your actual webhook)
    DISCORD_WEBHOOK = "YOUR_DISCORD_WEBHOOK_URL_HERE"

    backup_engine = BROskiBackupEngine(DISCORD_WEBHOOK)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "emergency":
            backup_engine.emergency_backup()
        elif command == "sync":
            backup_engine.git_auto_sync()
        elif command == "cleanup":
            backup_engine.cleanup_old_backups()
        elif command == "restore" and len(sys.argv) > 2:
            backup_engine.restore_from_backup(sys.argv[2])
        else:
            print("🔧 BROski Backup Engine Commands:")
            print("  python backup_engine.py emergency  - Create emergency backup")
            print("  python backup_engine.py sync      - Git auto-sync")
            print("  python backup_engine.py cleanup   - Clean old backups")
            print("  python backup_engine.py restore [name] - Restore from backup")
    else:
        # Run normal scheduled backup
        backup_info = backup_engine.create_full_backup()
        backup_engine.git_auto_sync()
        backup_engine.cleanup_old_backups()
        print("✅ Manual backup completed!")
