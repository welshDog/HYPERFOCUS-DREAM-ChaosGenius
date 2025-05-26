#!/usr/bin/env python3
"""
🧠💥 CHAOSGENIUS SYSTEM OPTIMIZER - PHASE ULTRA 💥🧠
Transforms your scattered digital chaos into organized quantum order.
Built for neurodivergent minds that think in beautiful chaos patterns.
"""

import os
import shutil
import time
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system_optimization.log'),
        logging.StreamHandler()
    ]
)

class ChaosGeniusOptimizer:
    """🚀 The ultimate ADHD-friendly project optimizer"""
    
    def __init__(self, root_folder):
        self.root_folder = Path(root_folder)
        self.results = {
            'renamed_files': [],
            'archived_files': [],
            'duplicates_found': {},
            'organized_files': [],
            'errors': []
        }
        
    def print_header(self, title):
        """Cyberpunk-style section headers"""
        print(f"\n{'='*60}")
        print(f"🧠 {title}")
        print(f"{'='*60}")
        
    def rename_files_with_spaces(self, dry_run=True):
        """🔥 FILE RENAMER BOT - Fixes filenames with spaces"""
        self.print_header("FILE RENAMER BOT ACTIVATED")
        
        count = 0
        for path in self.root_folder.rglob("*"):
            if " " in path.name and not path.name.startswith('.'):
                try:
                    # Create safe filename
                    new_name = (path.name
                               .replace(" ", "_")
                               .replace("(", "")
                               .replace(")", "")
                               .replace("[", "")
                               .replace("]", "")
                               .replace("&", "and"))
                    
                    new_path = path.with_name(new_name)
                    
                    if dry_run:
                        print(f"📝 WOULD RENAME: {path.name} ➜ {new_name}")
                    else:
                        if not new_path.exists():
                            path.rename(new_path)
                            print(f"✅ RENAMED: {path.name} ➜ {new_name}")
                            self.results['renamed_files'].append({
                                'old': str(path),
                                'new': str(new_path)
                            })
                            count += 1
                        else:
                            print(f"⚠️ SKIP: {new_name} already exists")
                            
                except Exception as e:
                    error_msg = f"❌ ERROR renaming {path}: {e}"
                    print(error_msg)
                    self.results['errors'].append(error_msg)
                    
        print(f"\n🎯 Files processed: {count}")
        return count
    
    def archive_large_files(self, size_limit_mb=10, dry_run=True):
        """📦 PROJECT COMPACTOR - Moves huge files to archive"""
        self.print_header("PROJECT COMPACTOR ACTIVATED")
        
        archive_dir = self.root_folder / "__archive" / time.strftime("%Y-%m-%d")
        count = 0
        total_size = 0
        
        for path in self.root_folder.rglob("*.*"):
            if path.is_file():
                try:
                    file_size = path.stat().st_size
                    size_mb = file_size / (1024 * 1024)
                    
                    if size_mb > size_limit_mb:
                        if dry_run:
                            print(f"📦 WOULD ARCHIVE: {path.name} ({size_mb:.1f}MB)")
                        else:
                            archive_dir.mkdir(parents=True, exist_ok=True)
                            dest_path = archive_dir / path.name
                            
                            # Handle name conflicts
                            counter = 1
                            while dest_path.exists():
                                stem = path.stem
                                suffix = path.suffix
                                dest_path = archive_dir / f"{stem}_{counter}{suffix}"
                                counter += 1
                            
                            shutil.move(str(path), str(dest_path))
                            print(f"📦 ARCHIVED: {path.name} ({size_mb:.1f}MB)")
                            
                            self.results['archived_files'].append({
                                'file': path.name,
                                'size_mb': size_mb,
                                'archived_to': str(dest_path)
                            })
                            count += 1
                            total_size += size_mb
                            
                except Exception as e:
                    error_msg = f"❌ ERROR archiving {path}: {e}"
                    print(error_msg)
                    self.results['errors'].append(error_msg)
                    
        print(f"\n🎯 Files archived: {count} ({total_size:.1f}MB total)")
        return count
    
    def find_duplicate_filenames(self):
        """🧼 DUPLICATE SWEEPER - Finds repeated filenames"""
        self.print_header("DUPLICATE SWEEPER ACTIVATED")
        
        seen = defaultdict(list)
        for path in self.root_folder.rglob("*.*"):
            if path.is_file():
                seen[path.name].append(str(path))
        
        duplicates = {name: paths for name, paths in seen.items() if len(paths) > 1}
        
        for filename, paths in duplicates.items():
            print(f"⚠️ DUPLICATE: {filename} ({len(paths)} copies)")
            for p in paths:
                print(f"   └── {p}")
            print()
            
        self.results['duplicates_found'] = duplicates
        print(f"\n🎯 Duplicate groups found: {len(duplicates)}")
        return duplicates
    
    def organize_by_filetype(self, dry_run=True):
        """📂 ULTRA FOLDER ORGANIZER - Sorts files by type"""
        self.print_header("ULTRA FOLDER ORGANIZER ACTIVATED")
        
        # Enhanced file type mapping
        types = {
            # Code files
            ".py": "code/python", ".pyc": "code/python", ".pyi": "code/python",
            ".js": "code/javascript", ".ts": "code/typescript",
            ".html": "frontend/html", ".css": "frontend/css",
            
            # Data files
            ".json": "data/json", ".csv": "data/csv", ".xlsx": "data/excel",
            ".db": "data/databases", ".sqlite": "data/databases",
            
            # Documentation
            ".md": "docs/markdown", ".txt": "docs/text", ".pdf": "docs/pdf",
            
            # Media
            ".png": "media/images", ".jpg": "media/images", ".jpeg": "media/images",
            ".mp4": "media/video", ".mp3": "media/audio",
            
            # Archives
            ".zip": "archives", ".rar": "archives", ".7z": "archives",
        }
        
        count = 0
        for path in self.root_folder.rglob("*.*"):
            if path.is_file():
                ext = path.suffix.lower()
                if ext in types:
                    try:
                        dest_dir = self.root_folder / "_organized" / types[ext]
                        dest_path = dest_dir / path.name
                        
                        if dry_run:
                            print(f"📁 WOULD MOVE: {path.name} ➜ {types[ext]}/")
                        else:
                            dest_dir.mkdir(parents=True, exist_ok=True)
                            
                            # Handle name conflicts
                            counter = 1
                            while dest_path.exists():
                                stem = path.stem
                                suffix = path.suffix
                                dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                                counter += 1
                            
                            shutil.move(str(path), str(dest_path))
                            print(f"📁 MOVED: {path.name} ➜ {types[ext]}/")
                            
                            self.results['organized_files'].append({
                                'file': path.name,
                                'from': str(path.parent),
                                'to': str(dest_dir)
                            })
                            count += 1
                            
                    except Exception as e:
                        error_msg = f"❌ ERROR organizing {path}: {e}"
                        print(error_msg)
                        self.results['errors'].append(error_msg)
                        
        print(f"\n🎯 Files organized: {count}")
        return count
    
    def generate_readme_index(self):
        """📋 MASTER INDEX BUILDER - Creates comprehensive project index"""
        self.print_header("MASTER INDEX BUILDER ACTIVATED")
        
        readme_path = self.root_folder / "README_MASTER_INDEX.md"
        
        # Collect files by category
        categories = {
            'dashboards': [],
            'scripts': [],
            'documentation': [],
            'configuration': [],
            'data': [],
            'other': []
        }
        
        for path in self.root_folder.rglob("*.*"):
            if path.is_file():
                rel_path = path.relative_to(self.root_folder)
                ext = path.suffix.lower()
                name = path.name.lower()
                
                if 'dashboard' in name or ext == '.html':
                    categories['dashboards'].append(rel_path)
                elif ext == '.py' or 'script' in name:
                    categories['scripts'].append(rel_path)
                elif ext in ['.md', '.txt', '.pdf']:
                    categories['documentation'].append(rel_path)
                elif ext in ['.json', '.yaml', '.yml', '.toml', '.cfg']:
                    if 'config' in name or 'setup' in name:
                        categories['configuration'].append(rel_path)
                    else:
                        categories['data'].append(rel_path)
                else:
                    categories['other'].append(rel_path)
        
        # Generate the master index
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# 🧠 ChaosGenius Project Master Index\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write("## 🎯 Quick Navigation\n\n")
            
            for category, files in categories.items():
                if files:
                    f.write(f"### 🔗 {category.title()} ({len(files)} files)\n\n")
                    for file_path in sorted(files):
                        f.write(f"- [{file_path}](./{file_path})\n")
                    f.write("\n")
            
            # Add project statistics
            f.write("## 📊 Project Statistics\n\n")
            f.write(f"- **Total Files Indexed:** {sum(len(files) for files in categories.values())}\n")
            f.write(f"- **Python Scripts:** {len(categories['scripts'])}\n")
            f.write(f"- **Dashboards:** {len(categories['dashboards'])}\n")
            f.write(f"- **Documentation:** {len(categories['documentation'])}\n")
            f.write(f"- **Configuration Files:** {len(categories['configuration'])}\n")
            f.write(f"- **Data Files:** {len(categories['data'])}\n\n")
            
            f.write("---\n")
            f.write("*💜 Built by ChaosGenius - Where chaos becomes quantum order*\n")
        
        print(f"📋 Created: {readme_path}")
        return str(readme_path)
    
    def save_results(self):
        """💾 Save optimization results to JSON"""
        results_file = self.root_folder / f"optimization_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {results_file}")
        return str(results_file)
    
    def run_full_optimization(self, dry_run=True):
        """🚀 Run the complete optimization suite"""
        print("🧠💥 CHAOSGENIUS SYSTEM OPTIMIZER - PHASE ULTRA ACTIVATED! 💥🧠")
        print("Transforming chaos into quantum digital order...\n")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No files will be modified")
            print("Run with dry_run=False to execute changes\n")
        
        try:
            # 1. Rename files with spaces
            self.rename_files_with_spaces(dry_run)
            
            # 2. Archive large files
            self.archive_large_files(dry_run=dry_run)
            
            # 3. Find duplicates (always safe to run)
            self.find_duplicate_filenames()
            
            # 4. Organize by file type
            self.organize_by_filetype(dry_run)
            
            # 5. Generate master index (always safe to run)
            self.generate_readme_index()
            
            # 6. Save results
            if not dry_run:
                self.save_results()
            
            print("\n🎉 OPTIMIZATION COMPLETE!")
            print("Your hyperfocus zone is now quantum-organized! 🧠⚡")
            
        except Exception as e:
            error_msg = f"💥 CRITICAL ERROR: {e}"
            print(error_msg)
            self.results['errors'].append(error_msg)
            logging.error(error_msg)


def main():
    """🎯 Main execution function"""
    project_root = r"C:\Users\Lyndz\OneDrive\Desktop\HYPERFOCUS DREAM build idea"
    
    print("🧠 ChaosGenius System Optimizer")
    print("Choose your optimization level:")
    print("1. 🔍 DRY RUN (Preview changes only)")
    print("2. 🚀 FULL OPTIMIZATION (Execute all changes)")
    print("3. 📋 INDEX ONLY (Just create master index)")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        optimizer = ChaosGeniusOptimizer(project_root)
        
        if choice == "1":
            optimizer.run_full_optimization(dry_run=True)
        elif choice == "2":
            confirm = input("⚠️ This will modify your files. Are you sure? (yes/no): ")
            if confirm.lower() in ['yes', 'y']:
                optimizer.run_full_optimization(dry_run=False)
            else:
                print("❌ Operation cancelled")
        elif choice == "3":
            optimizer.generate_readme_index()
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"💥 Error: {e}")


if __name__ == "__main__":
    main()