#!/usr/bin/env python3
"""
🔧 HYPERFOCUS DREAM Advanced Project Optimizer
Fixes remaining issues from the comprehensive analysis and optimizes project structure
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# 📁 Project configuration
PROJECT_ROOT = Path("/root/chaosgenius")
BACKUP_DIR = PROJECT_ROOT / "optimization_backups"
LOG_FILE = (
    PROJECT_ROOT
    / f"project_optimization_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
)


class AdvancedProjectOptimizer:
    def __init__(self):
        self.optimization_log = {
            "start_time": datetime.now().isoformat(),
            "actions": [],
            "files_processed": 0,
            "space_freed_mb": 0,
            "issues_fixed": 0,
            "optimizations_applied": [],
        }

        # Ensure backup directory exists
        BACKUP_DIR.mkdir(exist_ok=True)

    def log_action(self, action_type, description, details=None):
        """Log optimization actions"""
        action = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "description": description,
            "details": details or {},
        }
        self.optimization_log["actions"].append(action)
        print(f"✅ {action_type}: {description}")

    def fix_remaining_file_naming_issues(self):
        """Fix remaining files with spaces in names"""
        print("\n🔧 FIXING REMAINING FILE NAMING ISSUES...")

        problematic_files = [
            PROJECT_ROOT / "Auto File Organizer Script",
            PROJECT_ROOT / "cleanup_backups" / "original_administrator powers",
            PROJECT_ROOT / "cleanup_backups" / "original_ai builder",
            PROJECT_ROOT / "cleanup_backups" / "original_AI Squad",
            PROJECT_ROOT / "cleanup_backups" / "original_ANALYZE + SETUP BOOSTER",
        ]

        for file_path in problematic_files:
            if file_path.exists():
                # Create safe filename
                new_name = re.sub(r"[^\w\-_.]", "_", file_path.name)
                new_name = re.sub(r"_+", "_", new_name)
                new_path = file_path.parent / new_name

                try:
                    file_path.rename(new_path)
                    self.log_action(
                        "RENAME", f"Fixed naming: {file_path.name} → {new_name}"
                    )
                    self.optimization_log["files_processed"] += 1
                except Exception as e:
                    self.log_action("ERROR", f"Failed to rename {file_path.name}: {e}")

    def consolidate_duplicate_scripts(self):
        """Consolidate duplicate Auto File Organizer Scripts"""
        print("\n📋 CONSOLIDATING DUPLICATE SCRIPTS...")

        # Find all Auto File Organizer Scripts
        auto_organizer_files = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            for file in files:
                if (
                    "Auto File Organizer Script" in file
                    or "Auto_File_Organizer_Script" in file
                ):
                    auto_organizer_files.append(Path(root) / file)

        if len(auto_organizer_files) > 1:
            # Keep the one in Tools & Utilities, archive others
            tools_dir = PROJECT_ROOT / "Tools & Utilities"
            main_script = None

            for script in auto_organizer_files:
                if "Tools & Utilities" in str(script):
                    main_script = script
                    break

            for script in auto_organizer_files:
                if script != main_script:
                    backup_name = f"auto_organizer_backup_{script.parent.name}_{datetime.now().strftime('%Y%m%d')}"
                    backup_path = BACKUP_DIR / backup_name
                    shutil.move(str(script), str(backup_path))
                    self.log_action(
                        "CONSOLIDATE",
                        f"Moved duplicate script to backup: {backup_name}",
                    )

    def optimize_virtual_environment(self):
        """Optimize virtual environment and add proper .gitignore"""
        print("\n🔧 OPTIMIZING VIRTUAL ENVIRONMENT...")

        venv_dirs = [PROJECT_ROOT / "venv", PROJECT_ROOT / "venvve"]

        for venv_dir in venv_dirs:
            if venv_dir.exists():
                # Calculate size before optimization
                total_size = sum(
                    f.stat().st_size for f in venv_dir.rglob("*") if f.is_file()
                )
                size_mb = total_size / (1024 * 1024)

                # Create venv-specific .gitignore
                gitignore_path = venv_dir / ".gitignore"
                gitignore_content = [
                    "# Virtual Environment - Ignore Everything",
                    "*",
                    "!.gitignore",
                    "",
                    "# This virtual environment should be recreated with:",
                    "# python -m venv venv",
                    "# pip install -r requirements.txt",
                ]

                try:
                    with open(gitignore_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(gitignore_content))
                    self.log_action(
                        "OPTIMIZE",
                        f"Added .gitignore to {venv_dir.name} ({size_mb:.1f}MB)",
                    )
                except Exception as e:
                    self.log_action("ERROR", f"Failed to optimize {venv_dir.name}: {e}")

    def archive_old_analysis_reports(self):
        """Archive all old analysis reports efficiently"""
        print("\n📊 ARCHIVING OLD ANALYSIS REPORTS...")

        # Create comprehensive reports archive
        reports_archive = PROJECT_ROOT / "archived_reports"
        reports_archive.mkdir(exist_ok=True)

        # Find all analysis/report files
        report_patterns = [
            "hyperfocus_project_analysis_*.json",
            "project_analysis_report_*.json",
            "file_organization_log_*.json",
            "health_report_*.json",
            "test_report_*.json",
            "cleanup_log_*.json",
        ]

        total_freed = 0
        for pattern in report_patterns:
            for report_file in PROJECT_ROOT.glob(pattern):
                if (
                    report_file.parent != reports_archive
                ):  # Don't move files already in archive
                    file_size_mb = report_file.stat().st_size / (1024 * 1024)
                    if file_size_mb > 1:  # Archive reports larger than 1MB
                        new_path = reports_archive / report_file.name
                        shutil.move(str(report_file), str(new_path))
                        total_freed += file_size_mb
                        self.log_action(
                            "ARCHIVE",
                            f"Archived report ({file_size_mb:.1f}MB): {report_file.name}",
                        )

        self.optimization_log["space_freed_mb"] += total_freed

    def optimize_project_structure(self):
        """Create optimal project structure with clear organization"""
        print("\n🏗️ OPTIMIZING PROJECT STRUCTURE...")

        # Create standardized folder structure
        standard_folders = {
            "src": "Source code and main application files",
            "docs": "Documentation and guides",
            "scripts": "Utility scripts and automation tools",
            "config": "Configuration files and settings",
            "assets": "Static assets (images, audio, video)",
            "data": "Data files and databases",
            "tests": "Test files and test data",
            "build": "Build artifacts and compiled files",
            "deploy": "Deployment scripts and configurations",
        }

        for folder, description in standard_folders.items():
            folder_path = PROJECT_ROOT / folder
            if not folder_path.exists():
                folder_path.mkdir(exist_ok=True)
                # Create README in each folder
                readme_path = folder_path / "README.md"
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(f"# {folder.title()}\n\n{description}\n")
                self.log_action("CREATE", f"Created standard folder: {folder}")

    def update_master_gitignore(self):
        """Create comprehensive .gitignore for the entire project"""
        print("\n📝 UPDATING MASTER .GITIGNORE...")

        gitignore_path = PROJECT_ROOT / ".gitignore"

        comprehensive_gitignore = [
            "# === HYPERFOCUS DREAM PROJECT .GITIGNORE ===",
            "",
            "# Virtual Environments",
            "venv/",
            "venvve/",
            "env/",
            ".env",
            "",
            "# Python",
            "__pycache__/",
            "*.py[cod]",
            "*$py.class",
            "*.so",
            ".Python",
            "build/",
            "develop-eggs/",
            "dist/",
            "downloads/",
            "eggs/",
            ".eggs/",
            "lib/",
            "lib64/",
            "parts/",
            "sdist/",
            "var/",
            "wheels/",
            "*.egg-info/",
            ".installed.cfg",
            "*.egg",
            "",
            "# Analysis Reports & Logs",
            "hyperfocus_project_analysis_*.json",
            "project_analysis_report_*.json",
            "file_organization_log_*.json",
            "health_report_*.json",
            "test_report_*.json",
            "cleanup_log_*.json",
            "optimization_log_*.json",
            "*.log",
            "logs/",
            "",
            "# Backup Directories",
            "cleanup_backups/",
            "optimization_backups/",
            "archived_reports/",
            "archived_logs/",
            "",
            "# IDE & Editor Files",
            ".vscode/settings.json",
            ".idea/",
            "*.swp",
            "*.swo",
            "*~",
            "",
            "# OS Files",
            ".DS_Store",
            ".DS_Store?",
            "._*",
            ".Spotlight-V100",
            ".Trashes",
            "ehthumbs.db",
            "Thumbs.db",
            "",
            "# Database Files",
            "*.db",
            "*.sqlite3",
            "*.db-journal",
            "",
            "# Large Media Files (>50MB)",
            "*.mp4",
            "*.mov",
            "*.avi",
            "*.mkv",
            "*.wav",
            "*.flac",
            "",
            "# Temporary Files",
            "*.tmp",
            "*.temp",
            "*.bak",
            "*.backup",
            "",
            "# Node modules (if any JS)",
            "node_modules/",
            "npm-debug.log*",
            "",
            "# Docker",
            ".dockerignore",
            "",
            "# Coverage Reports",
            "htmlcov/",
            ".coverage",
            ".coverage.*",
            "coverage.xml",
            "*.cover",
            "",
            "# Production secrets",
            "*.env.production",
            "*.env.local",
            "secrets/",
            "credentials.json",
        ]

        try:
            # Read existing .gitignore if it exists
            existing_content = []
            if gitignore_path.exists():
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    existing_content = f.read().strip().split("\n")

            # Combine with new comprehensive rules (avoid duplicates)
            final_content = []
            seen_rules = set()

            # Add existing unique rules first
            for line in existing_content:
                if line.strip() and not line.startswith("#") and line not in seen_rules:
                    final_content.append(line)
                    seen_rules.add(line)

            # Add comprehensive rules
            final_content.extend(comprehensive_gitignore)

            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write("\n".join(final_content))

            self.log_action(
                "OPTIMIZE", "Updated master .gitignore with comprehensive rules"
            )

        except Exception as e:
            self.log_action("ERROR", f"Failed to update .gitignore: {e}")

    def create_project_health_monitor(self):
        """Create a script to monitor project health"""
        print("\n🔍 CREATING PROJECT HEALTH MONITOR...")

        monitor_script = PROJECT_ROOT / "project_health_monitor.py"

        monitor_code = '''#!/usr/bin/env python3
"""
🏥 HYPERFOCUS DREAM Project Health Monitor
Automatically monitors project health and suggests optimizations
"""

import os
import json
from pathlib import Path
from datetime import datetime

class ProjectHealthMonitor:
    def __init__(self, project_root):
        self.project_root = Path(project_root)

    def check_project_health(self):
        """Perform comprehensive health check"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "UNKNOWN",
            "metrics": {},
            "issues": [],
            "recommendations": []
        }

        # Check file count
        total_files = sum(1 for _ in self.project_root.rglob('*') if _.is_file())
        health_report["metrics"]["total_files"] = total_files

        # Check for large files
        large_files = []
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                try:
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    if size_mb > 50:
                        large_files.append({"path": str(file_path), "size_mb": size_mb})
                except:
                    pass

        health_report["metrics"]["large_files_count"] = len(large_files)
        health_report["metrics"]["large_files"] = large_files[:5]  # Top 5

        # Check .gitignore existence
        gitignore_exists = (self.project_root / ".gitignore").exists()
        health_report["metrics"]["gitignore_exists"] = gitignore_exists

        # Determine overall health
        issues_count = 0
        if total_files > 25000:
            health_report["issues"].append("Project has excessive file count")
            issues_count += 1
        if len(large_files) > 10:
            health_report["issues"].append("Too many large files detected")
            issues_count += 1
        if not gitignore_exists:
            health_report["issues"].append("Missing .gitignore file")
            issues_count += 1

        # Set health status
        if issues_count == 0:
            health_report["overall_health"] = "EXCELLENT"
        elif issues_count <= 2:
            health_report["overall_health"] = "GOOD"
        elif issues_count <= 4:
            health_report["overall_health"] = "FAIR"
        else:
            health_report["overall_health"] = "POOR"

        return health_report

    def save_health_report(self, report):
        """Save health report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.project_root / f"health_report_{timestamp}.json"

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        return report_path

if __name__ == "__main__":
    project_root = Path(__file__).parent
    monitor = ProjectHealthMonitor(project_root)

    print("🔍 Running HYPERFOCUS DREAM Project Health Check...")
    health_report = monitor.check_project_health()

    print(f"\\n🏥 HEALTH STATUS: {health_report['overall_health']}")
    print(f"📊 Total Files: {health_report['metrics']['total_files']:,}")
    print(f"💾 Large Files: {health_report['metrics']['large_files_count']}")

    if health_report['issues']:
        print("\\n⚠️  Issues Found:")
        for issue in health_report['issues']:
            print(f"   • {issue}")

    report_path = monitor.save_health_report(health_report)
    print(f"\\n📋 Health report saved: {report_path}")
'''

        try:
            with open(monitor_script, "w", encoding="utf-8") as f:
                f.write(monitor_code)
            self.log_action("CREATE", "Created project health monitor script")
        except Exception as e:
            self.log_action("ERROR", f"Failed to create health monitor: {e}")

    def generate_optimization_summary(self):
        """Generate final optimization summary"""
        print("\n📈 GENERATING OPTIMIZATION SUMMARY...")

        self.optimization_log["end_time"] = datetime.now().isoformat()
        self.optimization_log["duration_minutes"] = (
            datetime.fromisoformat(self.optimization_log["end_time"])
            - datetime.fromisoformat(self.optimization_log["start_time"])
        ).total_seconds() / 60

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.optimization_log, f, indent=2, ensure_ascii=False)

        self.log_action("COMPLETE", f"Optimization log saved to: {LOG_FILE}")

    def run_optimization(self):
        """Execute the complete optimization process"""
        print("🚀 STARTING HYPERFOCUS DREAM PROJECT OPTIMIZATION...")
        print(f"📁 Project Root: {PROJECT_ROOT}")
        print(f"💾 Backups will be saved to: {BACKUP_DIR}")

        try:
            self.fix_remaining_file_naming_issues()
            self.consolidate_duplicate_scripts()
            self.optimize_virtual_environment()
            self.archive_old_analysis_reports()
            self.optimize_project_structure()
            self.update_master_gitignore()
            self.create_project_health_monitor()
            self.generate_optimization_summary()

            print(f"\n🎉 OPTIMIZATION COMPLETE!")
            print(f"📊 Summary:")
            print(f"   • Files processed: {self.optimization_log['files_processed']}")
            print(f"   • Space freed: {self.optimization_log['space_freed_mb']:.1f} MB")
            print(f"   • Actions taken: {len(self.optimization_log['actions'])}")
            print(f"   • Backup location: {BACKUP_DIR}")
            print(f"   • Optimization log: {LOG_FILE}")
            print(f"\n💡 Next steps:")
            print(f"   1. Run: python project_health_monitor.py")
            print(f"   2. Review archived reports in: archived_reports/")
            print(f"   3. Consider committing optimizations to git")

        except Exception as e:
            self.log_action("ERROR", f"Optimization failed: {e}")
            print(f"❌ Optimization failed: {e}")


if __name__ == "__main__":
    optimizer = AdvancedProjectOptimizer()
    optimizer.run_optimization()
