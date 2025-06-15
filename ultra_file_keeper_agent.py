#!/usr/bin/env python3
"""
🗂️💪 ULTRA FILE KEEPER AGENT - THE DIGITAL LIBRARIAN 💪🗂️
🚀 The most LEGENDARY file organization and management agent! 🚀

This agent brings ORDER to digital chaos with:
- 🔍 HYPER file scanning and analysis
- 🗂️ Smart categorization and organization
- 📁 Automated folder structure creation
- 🧹 Duplicate detection and cleanup
- 📊 Real-time file monitoring
- 🎯 Intelligent file recommendations
- 💾 Storage optimization
- 🔒 Security scanning
"""

import os
import sys
import json
import asyncio
import sqlite3
import hashlib
import shutil
import time
import mimetypes
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Set up epic logging
logging.basicConfig(
    level=logging.INFO,
    format='🗂️ %(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('ultra_file_keeper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    """Data class for file information"""
    path: str
    name: str
    size: int
    extension: str
    mime_type: str
    created_time: float
    modified_time: float
    hash_md5: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class OrganizationRule:
    """Rule for file organization"""
    name: str
    pattern: str
    destination: str
    action: str  # move, copy, link
    enabled: bool = True
    priority: int = 0

class UltraFileKeeperAgent:
    """🚀 THE ULTRA FILE KEEPER AGENT 🚀"""

    def __init__(self, workspace_path: str = "/root/chaosgenius"):
        self.workspace_path = Path(workspace_path)
        self.db_path = self.workspace_path / "ultra_file_keeper.db"
        self.config_path = self.workspace_path / "ultra_file_keeper_config.json"

        # File categories mapping
        self.file_categories = {
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf', '.odt'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'code': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.c', '.go', '.rs'],
            'data': ['.json', '.xml', '.csv', '.sql', '.db', '.sqlite', '.xlsx', '.xls'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'executables': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app', '.appimage'],
            'configs': ['.conf', '.cfg', '.ini', '.yaml', '.yml', '.toml', '.env'],
            'logs': ['.log', '.out', '.err', '.trace']
        }

        # Initialize database and config
        asyncio.create_task(self.initialize())

    async def initialize(self):
        """Initialize the Ultra File Keeper Agent"""
        logger.info("🚀 Initializing Ultra File Keeper Agent...")

        # Create workspace if not exists
        self.workspace_path.mkdir(exist_ok=True)

        # Initialize database
        await self.init_database()

        # Load configuration
        await self.load_config()

        logger.info("✅ Ultra File Keeper Agent initialized successfully!")

    async def init_database(self):
        """Initialize the SQLite database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Files table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        path TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        size INTEGER NOT NULL,
                        extension TEXT,
                        mime_type TEXT,
                        category TEXT,
                        hash_md5 TEXT,
                        created_time REAL,
                        modified_time REAL,
                        last_scanned REAL,
                        tags TEXT,
                        metadata TEXT
                    )
                ''')

                # Organization rules table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS organization_rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        pattern TEXT NOT NULL,
                        destination TEXT NOT NULL,
                        action TEXT NOT NULL,
                        priority INTEGER DEFAULT 0,
                        enabled BOOLEAN DEFAULT 1,
                        created_time REAL,
                        last_used REAL
                    )
                ''')

                # File operations log
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS file_operations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        operation TEXT NOT NULL,
                        source_path TEXT,
                        destination_path TEXT,
                        timestamp REAL,
                        success BOOLEAN,
                        error_message TEXT
                    )
                ''')

                # System stats table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL,
                        total_files INTEGER,
                        total_size INTEGER,
                        categories_data TEXT,
                        largest_files TEXT,
                        duplicates_count INTEGER
                    )
                ''')

                conn.commit()
                logger.info("✅ Database initialized successfully")

        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")

    async def load_config(self):
        """Load configuration from file"""
        default_config = {
            "auto_organize": True,
            "duplicate_handling": "prompt",
            "max_file_size_mb": 1000,
            "excluded_paths": [".git", "__pycache__", "node_modules"],
            "organization_enabled": True,
            "scan_interval_hours": 24,
            "backup_before_move": True,
            "custom_categories": {},
            "notification_enabled": True
        }

        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                await self.save_config()

            logger.info("✅ Configuration loaded successfully")

        except Exception as e:
            logger.error(f"❌ Configuration loading failed: {e}")
            self.config = default_config

    async def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("✅ Configuration saved successfully")
        except Exception as e:
            logger.error(f"❌ Configuration saving failed: {e}")

    def get_file_category(self, file_path: Path) -> str:
        """Determine file category based on extension"""
        extension = file_path.suffix.lower()

        # Check custom categories first
        for category, extensions in self.config.get("custom_categories", {}).items():
            if extension in extensions:
                return category

        # Check default categories
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category

        return 'other'

    def calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """Calculate MD5 hash of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.warning(f"⚠️ Could not calculate hash for {file_path}: {e}")
            return None

    async def scan_file(self, file_path: Path) -> Optional[FileInfo]:
        """Scan a single file and extract information"""
        try:
            if not file_path.is_file():
                return None

            stat = file_path.stat()
            mime_type, _ = mimetypes.guess_type(str(file_path))

            file_info = FileInfo(
                path=str(file_path),
                name=file_path.name,
                size=stat.st_size,
                extension=file_path.suffix.lower(),
                mime_type=mime_type or 'unknown',
                created_time=stat.st_ctime,
                modified_time=stat.st_mtime,
                category=self.get_file_category(file_path)
            )

            # Calculate hash for files smaller than max size
            max_size = self.config.get("max_file_size_mb", 1000) * 1024 * 1024
            if stat.st_size <= max_size:
                file_info.hash_md5 = self.calculate_file_hash(file_path)

            return file_info

        except Exception as e:
            logger.warning(f"⚠️ Could not scan file {file_path}: {e}")
            return None

    async def hyper_file_scan(self, target_path: Optional[str] = None) -> Dict[str, Any]:
        """🔍 HYPER FILE SCAN - The most comprehensive file analysis! 🔍"""
        scan_path = Path(target_path) if target_path else self.workspace_path

        logger.info(f"🔍 Starting HYPER scan of: {scan_path}")

        results = {
            "scan_time": datetime.now().isoformat(),
            "target_path": str(scan_path),
            "total_files": 0,
            "total_size": 0,
            "categories": {},
            "large_files": [],
            "duplicates": [],
            "organization_opportunities": [],
            "errors": []
        }

        file_hashes = {}

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for file_path in scan_path.rglob("*"):
                    # Skip excluded paths
                    if any(excluded in str(file_path) for excluded in self.config.get("excluded_paths", [])):
                        continue

                    if file_path.is_file():
                        file_info = await self.scan_file(file_path)
                        if not file_info:
                            continue

                        results["total_files"] += 1
                        results["total_size"] += file_info.size

                        # Category statistics
                        category = file_info.category
                        if category not in results["categories"]:
                            results["categories"][category] = {"count": 0, "size": 0}
                        results["categories"][category]["count"] += 1
                        results["categories"][category]["size"] += file_info.size

                        # Track large files (>10MB)
                        if file_info.size > 10 * 1024 * 1024:
                            results["large_files"].append({
                                "path": file_info.path,
                                "size": file_info.size,
                                "size_mb": round(file_info.size / (1024 * 1024), 2)
                            })

                        # Track duplicates
                        if file_info.hash_md5:
                            if file_info.hash_md5 in file_hashes:
                                file_hashes[file_info.hash_md5].append(file_info.path)
                            else:
                                file_hashes[file_info.hash_md5] = [file_info.path]

                        # Store in database
                        cursor.execute('''
                            INSERT OR REPLACE INTO files
                            (path, name, size, extension, mime_type, category, hash_md5,
                             created_time, modified_time, last_scanned, tags, metadata)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            file_info.path, file_info.name, file_info.size,
                            file_info.extension, file_info.mime_type, file_info.category,
                            file_info.hash_md5, file_info.created_time, file_info.modified_time,
                            time.time(), json.dumps(file_info.tags), "{}"
                        ))

                conn.commit()

            # Find duplicates
            for hash_val, paths in file_hashes.items():
                if len(paths) > 1:
                    results["duplicates"].append({
                        "hash": hash_val,
                        "files": paths,
                        "count": len(paths)
                    })

            # Generate organization opportunities
            results["organization_opportunities"] = await self.analyze_organization_opportunities()

            # Save scan results
            await self.save_scan_results(results)

            logger.info(f"✅ HYPER scan completed! Found {results['total_files']} files")

        except Exception as e:
            logger.error(f"❌ HYPER scan failed: {e}")
            results["errors"].append(str(e))

        return results

    async def analyze_organization_opportunities(self) -> List[Dict[str, Any]]:
        """Analyze files and suggest organization opportunities"""
        opportunities = []

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Find files in root that should be organized
                cursor.execute('''
                    SELECT category, COUNT(*) as count, GROUP_CONCAT(name, '; ') as files
                    FROM files
                    WHERE path LIKE ? AND path NOT LIKE '%/%'
                    GROUP BY category
                    HAVING count > 2
                ''', (f"{self.workspace_path}%",))

                for category, count, files in cursor.fetchall():
                    if category != 'other':
                        opportunities.append({
                            "type": "category_organization",
                            "category": category,
                            "file_count": count,
                            "suggestion": f"Create '{category}' folder and move {count} files",
                            "files": files.split('; ')[:5]  # Show first 5 files
                        })

                # Find files with same extension scattered
                cursor.execute('''
                    SELECT extension, COUNT(*) as count
                    FROM files
                    WHERE extension != ''
                    GROUP BY extension
                    HAVING count > 3
                ''')

                for extension, count in cursor.fetchall():
                    opportunities.append({
                        "type": "extension_organization",
                        "extension": extension,
                        "file_count": count,
                        "suggestion": f"Consider organizing {count} {extension} files together"
                    })

        except Exception as e:
            logger.error(f"❌ Organization analysis failed: {e}")

        return opportunities

    async def save_scan_results(self, results: Dict[str, Any]):
        """Save scan results to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO system_stats
                    (timestamp, total_files, total_size, categories_data,
                     largest_files, duplicates_count)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    time.time(),
                    results["total_files"],
                    results["total_size"],
                    json.dumps(results["categories"]),
                    json.dumps(results["large_files"][:10]),
                    len(results["duplicates"])
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"❌ Could not save scan results: {e}")

    async def auto_organize_files(self, dry_run: bool = False) -> Dict[str, Any]:
        """🗂️ AUTO ORGANIZE - Smart file organization! 🗂️"""
        if not self.config.get("organization_enabled", True):
            return {"status": "disabled", "message": "Auto organization is disabled"}

        logger.info("🗂️ Starting auto file organization...")

        results = {
            "organized_files": 0,
            "created_folders": [],
            "operations": [],
            "errors": []
        }

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get files in workspace root that need organizing
                cursor.execute('''
                    SELECT path, category FROM files
                    WHERE path LIKE ? AND path NOT LIKE '%/%'
                    AND category != 'other'
                ''', (f"{self.workspace_path}/%",))

                files_to_organize = cursor.fetchall()

                for file_path, category in files_to_organize:
                    try:
                        source_path = Path(file_path)
                        if not source_path.exists():
                            continue

                        # Create category folder
                        category_folder = self.workspace_path / f"organized_{category}"

                        if not dry_run:
                            category_folder.mkdir(exist_ok=True)
                            if str(category_folder) not in results["created_folders"]:
                                results["created_folders"].append(str(category_folder))

                        # Move file
                        destination_path = category_folder / source_path.name

                        if not dry_run:
                            # Backup if enabled
                            if self.config.get("backup_before_move", True):
                                await self.create_backup(source_path)

                            shutil.move(str(source_path), str(destination_path))

                            # Update database
                            cursor.execute('''
                                UPDATE files SET path = ? WHERE path = ?
                            ''', (str(destination_path), str(source_path)))

                            # Log operation
                            cursor.execute('''
                                INSERT INTO file_operations
                                (operation, source_path, destination_path, timestamp, success)
                                VALUES (?, ?, ?, ?, ?)
                            ''', ("move", str(source_path), str(destination_path), time.time(), True))

                        results["operations"].append({
                            "action": "move",
                            "source": str(source_path),
                            "destination": str(destination_path),
                            "category": category
                        })

                        results["organized_files"] += 1

                    except Exception as e:
                        error_msg = f"Failed to organize {file_path}: {e}"
                        logger.error(f"❌ {error_msg}")
                        results["errors"].append(error_msg)

                if not dry_run:
                    conn.commit()

        except Exception as e:
            logger.error(f"❌ Auto organization failed: {e}")
            results["errors"].append(str(e))

        status = "completed" if not results["errors"] else "completed_with_errors"
        results["status"] = status

        logger.info(f"✅ Auto organization {status}! Organized {results['organized_files']} files")

        return results

    async def create_backup(self, file_path: Path):
        """Create backup of file before operations"""
        try:
            backup_dir = self.workspace_path / "backups" / datetime.now().strftime("%Y%m%d")
            backup_dir.mkdir(parents=True, exist_ok=True)

            backup_path = backup_dir / file_path.name
            shutil.copy2(str(file_path), str(backup_path))

            logger.info(f"📋 Backup created: {backup_path}")

        except Exception as e:
            logger.warning(f"⚠️ Backup creation failed: {e}")

    async def find_and_handle_duplicates(self, action: str = "prompt") -> Dict[str, Any]:
        """🔄 Find and handle duplicate files"""
        logger.info("🔄 Searching for duplicate files...")

        results = {
            "duplicate_groups": 0,
            "total_duplicates": 0,
            "space_saved": 0,
            "actions_taken": [],
            "errors": []
        }

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Find files with same hash
                cursor.execute('''
                    SELECT hash_md5, COUNT(*) as count, GROUP_CONCAT(path, '|') as paths,
                           AVG(size) as avg_size
                    FROM files
                    WHERE hash_md5 IS NOT NULL
                    GROUP BY hash_md5
                    HAVING count > 1
                ''')

                duplicate_groups = cursor.fetchall()

                for hash_val, count, paths_str, avg_size in duplicate_groups:
                    paths = paths_str.split('|')
                    results["duplicate_groups"] += 1
                    results["total_duplicates"] += count - 1  # Keep one copy

                    if action == "remove":
                        # Keep the first file, remove others
                        for path_to_remove in paths[1:]:
                            try:
                                Path(path_to_remove).unlink()
                                results["space_saved"] += avg_size
                                results["actions_taken"].append(f"Removed: {path_to_remove}")

                                # Remove from database
                                cursor.execute('DELETE FROM files WHERE path = ?', (path_to_remove,))

                            except Exception as e:
                                results["errors"].append(f"Failed to remove {path_to_remove}: {e}")

                    elif action == "move_to_duplicates":
                        # Move duplicates to a special folder
                        duplicates_folder = self.workspace_path / "duplicates"
                        duplicates_folder.mkdir(exist_ok=True)

                        for i, duplicate_path in enumerate(paths[1:], 1):
                            try:
                                source = Path(duplicate_path)
                                dest_name = f"{source.stem}_duplicate_{i}{source.suffix}"
                                dest_path = duplicates_folder / dest_name

                                shutil.move(str(source), str(dest_path))
                                results["actions_taken"].append(f"Moved to duplicates: {duplicate_path}")

                                # Update database
                                cursor.execute('UPDATE files SET path = ? WHERE path = ?',
                                             (str(dest_path), duplicate_path))

                            except Exception as e:
                                results["errors"].append(f"Failed to move {duplicate_path}: {e}")

                conn.commit()

        except Exception as e:
            logger.error(f"❌ Duplicate handling failed: {e}")
            results["errors"].append(str(e))

        logger.info(f"✅ Duplicate handling completed! Found {results['duplicate_groups']} groups")

        return results

    async def get_system_stats(self) -> Dict[str, Any]:
        """📊 Get comprehensive system statistics"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "workspace": str(self.workspace_path),
            "database_size": 0,
            "total_files": 0,
            "total_size": 0,
            "total_size_gb": 0,
            "categories": {},
            "largest_files": [],
            "recent_operations": [],
            "health_score": 0
        }

        try:
            # Database size
            if self.db_path.exists():
                stats["database_size"] = self.db_path.stat().st_size

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Basic stats
                cursor.execute('SELECT COUNT(*), SUM(size) FROM files')
                count, total_size = cursor.fetchone()
                stats["total_files"] = count or 0
                stats["total_size"] = total_size or 0
                stats["total_size_gb"] = round((total_size or 0) / (1024**3), 2)

                # Category breakdown
                cursor.execute('''
                    SELECT category, COUNT(*) as count, SUM(size) as size
                    FROM files GROUP BY category ORDER BY count DESC
                ''')

                for category, count, size in cursor.fetchall():
                    stats["categories"][category] = {
                        "count": count,
                        "size": size,
                        "size_mb": round(size / (1024**2), 2)
                    }

                # Largest files
                cursor.execute('''
                    SELECT name, size, category FROM files
                    ORDER BY size DESC LIMIT 10
                ''')

                stats["largest_files"] = [
                    {
                        "name": name,
                        "size": size,
                        "size_mb": round(size / (1024**2), 2),
                        "category": category
                    }
                    for name, size, category in cursor.fetchall()
                ]

                # Recent operations
                cursor.execute('''
                    SELECT operation, source_path, destination_path, timestamp, success
                    FROM file_operations ORDER BY timestamp DESC LIMIT 5
                ''')

                stats["recent_operations"] = [
                    {
                        "operation": op,
                        "source": src,
                        "destination": dst,
                        "time": datetime.fromtimestamp(ts).isoformat(),
                        "success": bool(success)
                    }
                    for op, src, dst, ts, success in cursor.fetchall()
                ]

            # Calculate health score (0-100)
            health_factors = []

            # Organization factor (fewer files in root = better)
            root_files = len([f for f in self.workspace_path.iterdir() if f.is_file()])
            org_score = max(0, 100 - (root_files * 2))  # Penalty for root files
            health_factors.append(org_score)

            # Size distribution factor
            if stats["categories"]:
                category_counts = [cat["count"] for cat in stats["categories"].values()]
                size_balance = 100 - (max(category_counts) / sum(category_counts) * 100)
                health_factors.append(size_balance)

            stats["health_score"] = round(sum(health_factors) / len(health_factors)) if health_factors else 50

        except Exception as e:
            logger.error(f"❌ Stats generation failed: {e}")

        return stats

# File Monitor for real-time watching
class UltraFileMonitor(FileSystemEventHandler):
    """Real-time file system monitor"""

    def __init__(self, agent: UltraFileKeeperAgent):
        self.agent = agent

    def on_created(self, event):
        if not event.is_directory:
            asyncio.create_task(self.agent.scan_file(Path(event.src_path)))

    def on_modified(self, event):
        if not event.is_directory:
            asyncio.create_task(self.agent.scan_file(Path(event.src_path)))

    def on_moved(self, event):
        if not event.is_directory:
            # Update database with new path
            asyncio.create_task(self.handle_file_move(event.src_path, event.dest_path))

    async def handle_file_move(self, old_path: str, new_path: str):
        """Handle file move in database"""
        try:
            with sqlite3.connect(self.agent.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE files SET path = ? WHERE path = ?', (new_path, old_path))
                conn.commit()
        except Exception as e:
            logger.error(f"❌ Failed to update moved file: {e}")

async def main():
    """Main function to run the Ultra File Keeper Agent"""
    print("🗂️💪 ULTRA FILE KEEPER AGENT STARTING UP! 💪🗂️")

    # Initialize agent
    agent = UltraFileKeeperAgent()
    await agent.initialize()

    # Set up file monitor
    event_handler = UltraFileMonitor(agent)
    observer = Observer()
    observer.schedule(event_handler, str(agent.workspace_path), recursive=True)
    observer.start()

    try:
        print("🚀 Agent is now ACTIVE and monitoring your files!")
        print("📊 Starting initial HYPER scan...")

        # Initial scan
        scan_results = await agent.hyper_file_scan()
        print(f"✅ Initial scan completed! Found {scan_results['total_files']} files")

        # Auto-organize if enabled
        if agent.config.get("auto_organize", True):
            print("🗂️ Running auto organization...")
            org_results = await agent.auto_organize_files()
            print(f"✅ Organized {org_results['organized_files']} files")

        # Keep running
        while True:
            await asyncio.sleep(3600)  # Check every hour

            # Periodic scan
            print("🔄 Running periodic scan...")
            await agent.hyper_file_scan()

    except KeyboardInterrupt:
        print("\n🛑 Shutting down Ultra File Keeper Agent...")
    finally:
        observer.stop()
        observer.join()
        print("👋 Ultra File Keeper Agent stopped. Stay organized! 💪")

if __name__ == "__main__":
    asyncio.run(main())