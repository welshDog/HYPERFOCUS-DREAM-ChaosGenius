#!/usr/bin/env python3
"""
🧹 ChaosGenius Workspace Cleanup Script
======================================
Remove unnecessary files and organize the workspace properly
"""

import os
import shutil
import sqlite3
from pathlib import Path
import json
import subprocess

class WorkspaceCleanup:
    def __init__(self):
        self.project_root = Path("/root/chaosgenius")
        self.backup_dir = self.project_root / "cleanup_backup"
        self.files_to_remove = []
        self.dirs_to_remove = []
        self.files_moved = 0
        self.files_removed = 0

    def create_backup(self):
        """Create backup of important files before cleanup"""
        print("📦 Creating backup...")
        self.backup_dir.mkdir(exist_ok=True)

        # Backup core files
        core_files = [
            "app.py",
            "dashboard_api.py",
            "requirements.txt",
            "chaosgenius_discord_bot.py",
            ".env"
        ]

        for file in core_files:
            file_path = self.project_root / file
            if file_path.exists():
                shutil.copy2(file_path, self.backup_dir / file)
                print(f"✅ Backed up: {file}")

    def identify_files_to_remove(self):
        """Identify files that should be removed"""

        # Files with dramatic/duplicate names
        dramatic_patterns = [
            "ULTRA_", "HYPER", "LEGENDARY", "SUPREME", "IMMORTAL", "INFINITE",
            "OMEGA", "GALAXY", "TRANSCENDENT", "EMPIRE", "GODMODE", "STEALTH",
            "ULTRA MODE", "PHASE", "💥", "🧠", "🚀", "🌌", "⚡", "🔥"
        ]

        # Database files that are likely temporary
        temp_db_patterns = [
            "_test.db", "_temp.db", "_backup.db", "_copy.db",
            "learning_optimized.db-shm", "learning_optimized.db-wal"
        ]

        # Log and temp files
        temp_file_patterns = [
            ".log", ".tmp", ".cache", ".pyc", "__pycache__",
            "output.log", "night_shift_status.txt"
        ]

        # Duplicate/versioned files
        duplicate_patterns = [
            "_v1", "_v2", "_v3", "_ultra", "_supreme", "_god", "_master",
            "_copy", "_backup", "_old", "_archive", "_test"
        ]

        print("🔍 Scanning for files to remove...")

        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                file_name = file_path.name
                file_str = str(file_path)

                # Check dramatic patterns
                if any(pattern in file_str for pattern in dramatic_patterns):
                    self.files_to_remove.append(file_path)
                    continue

                # Check temp patterns
                if any(pattern in file_name for pattern in temp_file_patterns):
                    self.files_to_remove.append(file_path)
                    continue

                # Check duplicate patterns
                if any(pattern in file_name for pattern in duplicate_patterns):
                    self.files_to_remove.append(file_path)
                    continue

                # Check temp databases
                if any(pattern in file_name for pattern in temp_db_patterns):
                    self.files_to_remove.append(file_path)
                    continue

    def identify_dirs_to_remove(self):
        """Identify directories that should be removed"""

        dramatic_dir_patterns = [
            "🧠", "🚀", "💥", "🌌", "⚡", "🔥", "💡", "💼", "💷", "🤑",
            "ULTRA", "HYPER", "LEGENDARY", "SUPREME", "IMMORTAL", "INFINITE",
            "GALAXY", "EMPIRE", "TRANSCENDENT", "PHASE", "STEALTH"
        ]

        temp_dirs = [
            "__pycache__", ".pytest_cache", "temp", "cache",
            "archived_logs", "archived_reports", "cleanup_backups",
            "emergency_backups", "optimization_backups"
        ]

        print("🔍 Scanning for directories to remove...")

        for dir_path in self.project_root.iterdir():
            if dir_path.is_dir():
                dir_name = dir_path.name

                # Check dramatic patterns
                if any(pattern in dir_name for pattern in dramatic_dir_patterns):
                    self.dirs_to_remove.append(dir_path)
                    continue

                # Check temp dirs
                if dir_name in temp_dirs:
                    self.dirs_to_remove.append(dir_path)
                    continue

    def remove_duplicate_databases(self):
        """Remove duplicate database files"""
        print("🗄️ Cleaning up duplicate databases...")

        db_files = list(self.project_root.glob("*.db"))

        # Keep only core databases
        core_dbs = [
            "chaosgenius.db",
            "broski_analytics.db",
            "hyperfocus_portal.db"
        ]

        for db_file in db_files:
            if db_file.name not in core_dbs:
                self.files_to_remove.append(db_file)

    def create_organized_structure(self):
        """Create organized directory structure"""
        print("📁 Creating organized structure...")

        # Create main directories
        main_dirs = [
            "src",
            "src/api",
            "src/core",
            "src/bots",
            "src/utils",
            "config",
            "tests",
            "docs",
            "scripts",
            "logs",
            "data"
        ]

        for dir_name in main_dirs:
            (self.project_root / dir_name).mkdir(parents=True, exist_ok=True)

    def move_core_files(self):
        """Move core files to organized structure"""
        print("📦 Organizing core files...")

        # Define file movements
        file_movements = {
            # Core application files
            "app.py": "src/app.py",
            "dashboard_api.py": "src/api/dashboard.py",

            # Bot files
            "chaosgenius_discord_bot.py": "src/bots/discord_bot.py",
            "fresh_broski_discord_bot.py": "src/bots/broski_bot.py",

            # Core modules
            "broski_core.py": "src/core/broski_core.py",

            # Configuration
            ".env": "config/.env",
            "requirements.txt": "requirements.txt",  # Keep at root

            # Documentation
            "README.md": "docs/README.md",
            "API_DOCUMENTATION.md": "docs/API_DOCUMENTATION.md",
        }

        for source, target in file_movements.items():
            source_path = self.project_root / source
            target_path = self.project_root / target

            if source_path.exists():
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source_path), str(target_path))
                print(f"✅ Moved: {source} → {target}")
                self.files_moved += 1

    def create_new_requirements(self):
        """Create clean requirements.txt"""
        print("📋 Creating clean requirements.txt...")

        clean_requirements = """# Core Flask application
Flask==2.3.3
Flask-CORS==4.0.0
Werkzeug==2.3.7

# API Documentation
flasgger==0.9.7.1

# Environment Management
python-dotenv==1.0.0

# HTTP Requests
requests==2.31.0

# Discord Bot
discord.py==2.3.2

# Database
sqlite3

# Development Tools (optional)
# black==23.7.0
# pytest==7.4.2
"""

        with open(self.project_root / "requirements.txt", 'w') as f:
            f.write(clean_requirements)

        print("✅ Created clean requirements.txt")

    def create_new_app_py(self):
        """Create clean app.py"""
        print("🚀 Creating clean app.py...")

        clean_app = """#!/usr/bin/env python3
\"\"\"
ChaosGenius Main Application
===========================
Clean Flask application entry point
\"\"\"

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

if __name__ == "__main__":
    print("🧠 Starting ChaosGenius Dashboard...")

    try:
        from api.dashboard import app

        print("💜 Dashboard URL: http://localhost:3000")
        print("📚 API Docs: http://localhost:3000/apidocs/")
        print("\\n✨ Press Ctrl+C to stop\\n")

        app.run(debug=True, host="0.0.0.0", port=3000)

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)
"""

        with open(self.project_root / "app.py", 'w') as f:
            f.write(clean_app)

        print("✅ Created clean app.py")

    def remove_files(self):
        """Remove identified files"""
        print(f"🗑️ Removing {len(self.files_to_remove)} files...")

        for file_path in self.files_to_remove:
            try:
                if file_path.exists():
                    file_path.unlink()
                    self.files_removed += 1
            except Exception as e:
                print(f"⚠️ Could not remove {file_path}: {e}")

    def remove_directories(self):
        """Remove identified directories"""
        print(f"🗑️ Removing {len(self.dirs_to_remove)} directories...")

        for dir_path in self.dirs_to_remove:
            try:
                if dir_path.exists():
                    shutil.rmtree(dir_path)
                    print(f"✅ Removed directory: {dir_path.name}")
            except Exception as e:
                print(f"⚠️ Could not remove {dir_path}: {e}")

    def create_gitignore(self):
        """Create proper .gitignore"""
        print("📝 Creating .gitignore...")

        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite3

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
temp/
tmp/
cache/
*.tmp
*.cache

# Backups
*backup*
*_backup/
cleanup_backup/
"""

        with open(self.project_root / ".gitignore", 'w') as f:
            f.write(gitignore_content)

        print("✅ Created .gitignore")

    def run_cleanup(self):
        """Run the complete cleanup process"""
        print("🧹 Starting ChaosGenius Workspace Cleanup")
        print("=" * 50)

        # Step 1: Backup
        self.create_backup()

        # Step 2: Identify files to remove
        self.identify_files_to_remove()
        self.identify_dirs_to_remove()
        self.remove_duplicate_databases()

        # Step 3: Show what will be removed
        print(f"\n📊 Cleanup Summary:")
        print(f"Files to remove: {len(self.files_to_remove)}")
        print(f"Directories to remove: {len(self.dirs_to_remove)}")

        # Ask for confirmation
        response = input("\n🤔 Proceed with cleanup? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cleanup cancelled")
            return

        # Step 4: Create organized structure
        self.create_organized_structure()

        # Step 5: Move core files
        self.move_core_files()

        # Step 6: Remove files and directories
        self.remove_files()
        self.remove_directories()

        # Step 7: Create new clean files
        self.create_new_requirements()
        self.create_new_app_py()
        self.create_gitignore()

        print("\n✅ Cleanup Complete!")
        print(f"📁 Files moved: {self.files_moved}")
        print(f"🗑️ Files removed: {self.files_removed}")
        print(f"💾 Backup created at: {self.backup_dir}")
        print("\n🚀 You can now run: python app.py")

if __name__ == "__main__":
    cleanup = WorkspaceCleanup()
    cleanup.run_cleanup()