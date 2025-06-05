#!/usr/bin/env python3
"""
🧹 ChaosGenius Folder Optimizer - ULTRA MODE
===========================================
Intelligently organizes the main project directory while preserving functionality
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChaosGeniusFolderOptimizer:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.optimization_log = []
        self.backup_created = False

    def log_action(self, action, details):
        """Log optimization actions"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        self.optimization_log.append(entry)
        logger.info(f"{action}: {details}")

    def create_safety_backup(self):
        """Create a safety backup before optimization"""
        try:
            backup_dir = self.project_root / "optimization_backups" / f"pre_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Backup critical files that will be moved
            critical_files = [
                "health_report_*.json",
                "project_analysis_report_*.json",
                "project_optimization_log_*.json",
                "test_report_*.json",
                "file_organization_log_*.json"
            ]

            for pattern in critical_files:
                for file_path in self.project_root.glob(pattern):
                    if file_path.is_file():
                        shutil.copy2(file_path, backup_dir / file_path.name)

            self.backup_created = True
            self.log_action("Safety Backup Created", f"Backup location: {backup_dir}")
            return True

        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False

    def organize_reports_and_logs(self):
        """Move scattered reports and logs to appropriate folders"""

        # Health Reports → archived_reports
        health_reports = list(self.project_root.glob("health_report_*.json"))
        if health_reports:
            archived_reports_dir = self.project_root / "archived_reports"
            archived_reports_dir.mkdir(exist_ok=True)

            for report in health_reports:
                destination = archived_reports_dir / report.name
                shutil.move(str(report), str(destination))
                self.log_action("Moved Health Report", f"{report.name} → archived_reports/")

        # Project Analysis Reports → archived_reports/analysis
        analysis_reports = list(self.project_root.glob("project_analysis_report_*.json"))
        if analysis_reports:
            analysis_dir = self.project_root / "archived_reports" / "analysis"
            analysis_dir.mkdir(parents=True, exist_ok=True)

            for report in analysis_reports:
                destination = analysis_dir / report.name
                shutil.move(str(report), str(destination))
                self.log_action("Moved Analysis Report", f"{report.name} → archived_reports/analysis/")

        # Project Optimization Logs → archived_logs/optimization
        opt_logs = list(self.project_root.glob("project_optimization_log_*.json"))
        if opt_logs:
            opt_logs_dir = self.project_root / "archived_logs" / "optimization"
            opt_logs_dir.mkdir(parents=True, exist_ok=True)

            for log in opt_logs:
                destination = opt_logs_dir / log.name
                shutil.move(str(log), str(destination))
                self.log_action("Moved Optimization Log", f"{log.name} → archived_logs/optimization/")

        # Test Reports → archived_reports/tests
        test_reports = list(self.project_root.glob("test_report_*.json"))
        if test_reports:
            test_reports_dir = self.project_root / "archived_reports" / "tests"
            test_reports_dir.mkdir(parents=True, exist_ok=True)

            for report in test_reports:
                destination = test_reports_dir / report.name
                shutil.move(str(report), str(destination))
                self.log_action("Moved Test Report", f"{report.name} → archived_reports/tests/")

        # File Organization Logs → archived_logs
        file_org_logs = list(self.project_root.glob("file_organization_log_*.json"))
        if file_org_logs:
            archived_logs_dir = self.project_root / "archived_logs"
            archived_logs_dir.mkdir(exist_ok=True)

            for log in file_org_logs:
                destination = archived_logs_dir / log.name
                shutil.move(str(log), str(destination))
                self.log_action("Moved File Organization Log", f"{log.name} → archived_logs/")

    def organize_html_dashboards(self):
        """Organize HTML dashboard files"""

        # Create dashboard directory structure
        dashboard_dir = self.project_root / "frontend" / "dashboards"
        dashboard_dir.mkdir(parents=True, exist_ok=True)

        # HTML files to organize
        html_files = {
            "dashboard_ultra_mode.html": "ultra_mode.html",
            "Master AI Control Brain.html": "master_control.html",
            "Master_AI_Control_Brain.html": "master_control_alt.html",
            "Hyperfocus Bio Zone.html": "bio_zone.html"
        }

        for original_name, new_name in html_files.items():
            original_path = self.project_root / original_name
            if original_path.exists():
                destination = dashboard_dir / new_name
                shutil.move(str(original_path), str(destination))
                self.log_action("Organized Dashboard HTML", f"{original_name} → frontend/dashboards/{new_name}")

        # Move CSS files too
        css_files = ["MasterControlBrain.css"]
        css_dir = dashboard_dir / "css"
        css_dir.mkdir(exist_ok=True)

        for css_file in css_files:
            css_path = self.project_root / css_file
            if css_path.exists():
                destination = css_dir / css_file
                shutil.move(str(css_path), str(destination))
                self.log_action("Organized CSS File", f"{css_file} → frontend/dashboards/css/")

    def organize_test_files(self):
        """Move test files to tests directory"""

        test_files = ["test_chaosgenius_dashboard.py"]
        tests_dir = self.project_root / "tests"
        tests_dir.mkdir(exist_ok=True)

        for test_file in test_files:
            test_path = self.project_root / test_file
            if test_path.exists():
                destination = tests_dir / test_file
                shutil.move(str(test_path), str(destination))
                self.log_action("Moved Test File", f"{test_file} → tests/")

    def organize_special_folders(self):
        """Organize special folders with spaces in names"""

        # Handle special folders/files with spaces
        special_items = [
            "Hyperfocus Zone Command Central (FULL ULTRA MODE)",
            "SYSTEM OPTIMIZE PHASE ULTRA ACTIVATED"
        ]

        special_dir = self.project_root / "The Zone" / "special_modes"
        special_dir.mkdir(parents=True, exist_ok=True)

        for item in special_items:
            item_path = self.project_root / item
            if item_path.exists():
                # Create a clean filename
                clean_name = item.replace(" ", "_").replace("(", "").replace(")", "").lower()
                destination = special_dir / clean_name

                if item_path.is_dir():
                    shutil.move(str(item_path), str(destination))
                    self.log_action("Moved Special Directory", f"{item} → The Zone/special_modes/{clean_name}")
                else:
                    shutil.move(str(item_path), str(destination))
                    self.log_action("Moved Special File", f"{item} → The Zone/special_modes/{clean_name}")

    def clean_temporary_files(self):
        """Clean up temporary and cache files"""

        # Files to potentially clean (with user confirmation)
        temp_patterns = [
            "__pycache__",
            ".pytest_cache",
            "htmlcov",
            ".coverage"
        ]

        for pattern in temp_patterns:
            for item in self.project_root.glob(pattern):
                if item.is_dir():
                    # Keep these but note them
                    self.log_action("Temporary Directory Found", f"{item.name} (keeping for development)")
                elif item.is_file() and item.name == ".coverage":
                    self.log_action("Coverage File Found", f"{item.name} (keeping for testing)")

    def create_organization_summary(self):
        """Create a summary of the optimization"""

        summary = {
            "optimization_date": datetime.now().isoformat(),
            "backup_created": self.backup_created,
            "actions_performed": self.optimization_log,
            "total_actions": len(self.optimization_log),
            "organized_categories": [
                "Health Reports",
                "Analysis Reports",
                "Optimization Logs",
                "Test Reports",
                "Dashboard HTML Files",
                "Test Files",
                "Special Folders"
            ]
        }

        # Save summary
        summary_file = self.project_root / "archived_logs" / f"folder_optimization_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        self.log_action("Optimization Summary Created", f"Summary saved to {summary_file}")
        return summary

    def run_optimization(self):
        """Execute the complete folder optimization"""

        print("🧹 ChaosGenius Folder Optimizer - ULTRA MODE")
        print("=" * 50)
        print("Starting intelligent folder organization...")

        # Step 1: Safety backup
        print("\n📋 Step 1: Creating safety backup...")
        if not self.create_safety_backup():
            print("❌ Backup failed. Aborting optimization for safety.")
            return False

        # Step 2: Organize reports and logs
        print("\n📊 Step 2: Organizing reports and logs...")
        self.organize_reports_and_logs()

        # Step 3: Organize HTML dashboards
        print("\n🌐 Step 3: Organizing dashboard files...")
        self.organize_html_dashboards()

        # Step 4: Organize test files
        print("\n🧪 Step 4: Organizing test files...")
        self.organize_test_files()

        # Step 5: Organize special folders
        print("\n✨ Step 5: Organizing special folders...")
        self.organize_special_folders()

        # Step 6: Clean temporary files
        print("\n🧹 Step 6: Analyzing temporary files...")
        self.clean_temporary_files()

        # Step 7: Create summary
        print("\n📝 Step 7: Creating optimization summary...")
        summary = self.create_organization_summary()

        # Final report
        print(f"\n🎉 OPTIMIZATION COMPLETE!")
        print(f"✅ {summary['total_actions']} actions performed")
        print(f"🔒 Safety backup created: {self.backup_created}")
        print(f"📁 Organized categories: {len(summary['organized_categories'])}")

        print("\n📂 Main folder is now optimized!")
        print("🎯 All reports moved to archived_reports/")
        print("📊 All logs moved to archived_logs/")
        print("🌐 Dashboard files organized in frontend/dashboards/")
        print("🧪 Test files moved to tests/")
        print("✨ Special folders organized in The Zone/")

        return True

def main():
    """Main optimization function"""
    optimizer = ChaosGeniusFolderOptimizer()

    print("🧠 Welcome to ChaosGenius Folder Optimizer!")
    print("This will organize your main project directory safely.")
    print("\nThe optimizer will:")
    print("  • Move health reports to archived_reports/")
    print("  • Move logs to archived_logs/")
    print("  • Organize dashboard HTML files")
    print("  • Move test files to tests/")
    print("  • Create safety backups")

    response = input("\n🚀 Proceed with optimization? (y/N): ").strip().lower()

    if response in ['y', 'yes']:
        print("\n🎯 Starting optimization...")
        success = optimizer.run_optimization()

        if success:
            print("\n🎉 Your ChaosGenius main folder is now ULTRA ORGANIZED!")
        else:
            print("\n❌ Optimization encountered issues. Check the logs.")
    else:
        print("\n💜 Optimization cancelled. Your files remain unchanged.")

if __name__ == "__main__":
    main()