#!/usr/bin/env python3
"""
🧹 HYPERFOCUS DREAM Project Cleanup & Organization Script
Automatically fixes issues identified by the Ultra Folder Analyzer
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import re

# 📁 Project configuration
PROJECT_ROOT = Path("C:/Users/Lyndz/OneDrive/Desktop/HYPERFOCUS DREAM build idea")
BACKUP_DIR = PROJECT_ROOT / "cleanup_backups"
LOG_FILE = PROJECT_ROOT / f"cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

class ProjectOrganizer:
    def __init__(self):
        self.cleanup_log = {
            "start_time": datetime.now().isoformat(),
            "actions": [],
            "issues_fixed": 0,
            "files_moved": 0,
            "files_renamed": 0,
            "space_freed_mb": 0
        }

        # Ensure backup directory exists
        BACKUP_DIR.mkdir(exist_ok=True)

    def log_action(self, action_type, description, details=None):
        """Log cleanup actions for transparency"""
        action = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "description": description,
            "details": details or {}
        }
        self.cleanup_log["actions"].append(action)
        print(f"✅ {action_type}: {description}")

    def fix_file_naming_issues(self):
        """Fix files with spaces and problematic characters"""
        print("\n🔧 FIXING FILE NAMING ISSUES...")
        scripts_dir = PROJECT_ROOT / "Scripts & Prompts"

        if not scripts_dir.exists():
            return

        for item in scripts_dir.iterdir():
            if item.is_file() and " " in item.name:
                # Create safe filename
                new_name = re.sub(r'[^\w\-_.]', '_', item.name)
                new_name = re.sub(r'_+', '_', new_name)  # Remove multiple underscores
                new_path = scripts_dir / new_name

                try:
                    # Backup original
                    backup_path = BACKUP_DIR / f"original_{item.name}"
                    shutil.copy2(item, backup_path)

                    # Rename file
                    item.rename(new_path)
                    self.log_action("RENAME", f"Fixed filename: {item.name} → {new_name}")
                    self.cleanup_log["files_renamed"] += 1

                except Exception as e:
                    self.log_action("ERROR", f"Failed to rename {item.name}: {e}")

    def consolidate_duplicate_files(self):
        """Handle duplicate .gitignore, README.md, etc."""
        print("\n📋 CONSOLIDATING DUPLICATE FILES...")

        # Find all .gitignore files
        gitignore_files = list(PROJECT_ROOT.rglob(".gitignore"))
        if len(gitignore_files) > 1:
            # Keep the root one, backup others
            root_gitignore = PROJECT_ROOT / ".gitignore"
            for gitignore in gitignore_files:
                if gitignore != root_gitignore:
                    backup_name = f"gitignore_backup_{gitignore.parent.name}_{datetime.now().strftime('%Y%m%d')}"
                    backup_path = BACKUP_DIR / backup_name
                    shutil.move(str(gitignore), str(backup_path))
                    self.log_action("CONSOLIDATE", f"Moved duplicate .gitignore to backup: {backup_name}")

        # Find and handle duplicate README files
        readme_files = list(PROJECT_ROOT.rglob("README.md"))
        if len(readme_files) > 1:
            # Keep the main project README
            main_readme = PROJECT_ROOT / "README.md"
            for readme in readme_files:
                if readme != main_readme and readme.parent != PROJECT_ROOT / "generated_docs":
                    backup_name = f"readme_backup_{readme.parent.name}_{datetime.now().strftime('%Y%m%d')}.md"
                    backup_path = BACKUP_DIR / backup_name
                    shutil.move(str(readme), str(backup_path))
                    self.log_action("CONSOLIDATE", f"Moved duplicate README to backup: {backup_name}")

    def cleanup_large_report_files(self):
        """Archive old analysis reports to free up space"""
        print("\n📊 CLEANING UP LARGE REPORT FILES...")

        # Create reports archive directory
        reports_archive = PROJECT_ROOT / "archived_reports"
        reports_archive.mkdir(exist_ok=True)

        # Find large analysis reports
        report_patterns = [
            "hyperfocus_project_analysis_*.json",
            "project_analysis_report_*.json",
            "file_organization_log_*.json"
        ]

        for pattern in report_patterns:
            for report_file in PROJECT_ROOT.glob(pattern):
                file_size_mb = report_file.stat().st_size / (1024 * 1024)
                if file_size_mb > 5:  # Archive reports larger than 5MB
                    new_path = reports_archive / report_file.name
                    shutil.move(str(report_file), str(new_path))
                    self.cleanup_log["space_freed_mb"] += file_size_mb
                    self.log_action("ARCHIVE", f"Moved large report ({file_size_mb:.1f}MB): {report_file.name}")

    def cleanup_log_files(self):
        """Archive old log files"""
        print("\n📋 CLEANING UP LOG FILES...")

        logs_dir = PROJECT_ROOT / "logs"
        if logs_dir.exists():
            logs_archive = PROJECT_ROOT / "archived_logs"
            logs_archive.mkdir(exist_ok=True)

            for log_file in logs_dir.glob("*.log"):
                # Check if log is older than 7 days
                file_age_days = (datetime.now() - datetime.fromtimestamp(log_file.stat().st_mtime)).days
                if file_age_days > 7:
                    new_path = logs_archive / log_file.name
                    shutil.move(str(log_file), str(new_path))
                    self.log_action("ARCHIVE", f"Archived old log file: {log_file.name}")

    def create_gitignore_improvements(self):
        """Improve .gitignore to prevent future clutter"""
        print("\n📝 IMPROVING .GITIGNORE...")

        gitignore_path = PROJECT_ROOT / ".gitignore"

        additional_ignores = [
            "\n# === HYPERFOCUS PROJECT CLEANUP ADDITIONS ===",
            "# Analysis reports",
            "hyperfocus_project_analysis_*.json",
            "project_analysis_report_*.json",
            "health_report_*.json",
            "test_report_*.json",
            "",
            "# Archived files",
            "archived_reports/",
            "archived_logs/",
            "cleanup_backups/",
            "",
            "# Large virtual environment",
            "venv/",
            "venvve/",
            "",
            "# IDE and system files",
            ".vscode/settings.json",
            "__pycache__/",
            "*.pyc",
            ".DS_Store",
            "Thumbs.db",
            "",
            "# Log files",
            "*.log",
            "logs/*.log",
            "",
            "# Database files",
            "*.db",
            "*.sqlite3"
        ]

        try:
            with open(gitignore_path, "a", encoding="utf-8") as f:
                f.write("\n".join(additional_ignores))
            self.log_action("IMPROVE", "Enhanced .gitignore with cleanup patterns")
        except Exception as e:
            self.log_action("ERROR", f"Failed to improve .gitignore: {e}")

    def generate_organization_report(self):
        """Create final organization report"""
        print("\n📈 GENERATING ORGANIZATION REPORT...")

        self.cleanup_log["end_time"] = datetime.now().isoformat()
        self.cleanup_log["duration_minutes"] = (
            datetime.fromisoformat(self.cleanup_log["end_time"]) -
            datetime.fromisoformat(self.cleanup_log["start_time"])
        ).total_seconds() / 60

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cleanup_log, f, indent=2, ensure_ascii=False)

        self.log_action("COMPLETE", f"Cleanup log saved to: {LOG_FILE}")

    def run_cleanup(self):
        """Execute the complete cleanup process"""
        print("🚀 STARTING HYPERFOCUS DREAM PROJECT CLEANUP...")
        print(f"📁 Project Root: {PROJECT_ROOT}")
        print(f"💾 Backups will be saved to: {BACKUP_DIR}")

        try:
            self.fix_file_naming_issues()
            self.consolidate_duplicate_files()
            self.cleanup_large_report_files()
            self.cleanup_log_files()
            self.create_gitignore_improvements()
            self.generate_organization_report()

            print(f"\n🎉 CLEANUP COMPLETE!")
            print(f"📊 Summary:")
            print(f"   • Files renamed: {self.cleanup_log['files_renamed']}")
            print(f"   • Space freed: {self.cleanup_log['space_freed_mb']:.1f} MB")
            print(f"   • Actions taken: {len(self.cleanup_log['actions'])}")
            print(f"   • Backup location: {BACKUP_DIR}")
            print(f"   • Full log: {LOG_FILE}")

        except Exception as e:
            self.log_action("ERROR", f"Cleanup failed: {e}")
            print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    organizer = ProjectOrganizer()
    organizer.run_cleanup()