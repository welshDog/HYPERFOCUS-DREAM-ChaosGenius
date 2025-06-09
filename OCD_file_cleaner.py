import os
import shutil
from datetime import datetime
from pathlib import Path

# Enhanced BROski Folder Structure
FOLDER_STRUCTURE = {
    "src": [".py", ".js", ".ts", ".java", ".cpp"],
    "assets": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".mp3", ".ttf", ".otf"],
    "docs": [".md", ".txt", ".pdf", ".docx"],
    "env": [".env", ".json", ".yaml", ".yml", ".ini", ".cfg"],
    "build": [".exe", ".dll", ".so", ".bin"],
    "crystals": [".broski"],  # 💎 BROski Memory Crystals!
    "databases": [".db"],  # 📊 Database files
    "archives": [".tar.gz", ".zip", ".rar"],  # 📦 Compressed files
    "scripts": [".sh", ".bat", ".ps1"],  # 🔧 Script files
}

JUNK_FILES = [".DS_Store", "Thumbs.db", ".log", ".tmp", "__pycache__"]

# 💜 CHAOSGENIUS SPECIAL FILES - Never touch these!
PROTECTED_FILES = [
    "broski_core.py",
    "app.py",
    "dashboard_api.py",
    "broski_ultra_launcher.py",
    "OCD_file_cleaner.py",  # Don't move ourselves!
]


def organize_project(project_path):
    log = []
    project = Path(project_path)
    if not project.is_dir():
        return f"Skipping non-folder: {project}"

    log.append(f"# 🧹 BROski Ultra Clean Report: {project.name}")
    log.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append(f"**ChaosGenius OCD Cleaner v2.0** 🧠💜\n")

    files_moved = 0
    files_protected = 0
    crystals_found = 0

    for file in project.rglob("*"):
        if file.is_file():
            # 🛡️ Protect important ChaosGenius files
            if file.name in PROTECTED_FILES:
                log.append(f"🛡️ Protected: {file.name} (core system file)")
                files_protected += 1
                continue

            # 🗑️ Delete junk files
            if any(junk in file.name for junk in JUNK_FILES):
                try:
                    file.unlink()
                    log.append(f"🗑️ Deleted junk file: {file}")
                except Exception as e:
                    log.append(f"⚠️ Couldn't delete {file}: {e}")
                continue

            moved = False
            for folder, extensions in FOLDER_STRUCTURE.items():
                if file.suffix.lower() in extensions:
                    # 💎 Special handling for BROski crystals
                    if file.suffix == ".broski":
                        crystals_found += 1
                        log.append(f"💎 Found Memory Crystal: {file.name}")

                    target_folder = project / folder
                    target_folder.mkdir(exist_ok=True)
                    new_path = target_folder / file.name

                    # Avoid overwriting existing files
                    counter = 1
                    while new_path.exists():
                        stem = file.stem
                        suffix = file.suffix
                        new_path = target_folder / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(file), str(new_path))
                        log.append(f"📁 Moved {file.name} to {folder}/")
                        files_moved += 1
                    except Exception as e:
                        log.append(f"⚠️ Failed to move {file.name}: {e}")
                    moved = True
                    break
            if not moved:
                log.append(f"❓ Left file in place: {file.name}")

    # 🧠 Enhanced grading system
    if crystals_found > 0:
        grade = (
            "🧠💎 BROSKI LEGEND"
            if files_moved >= 10
            else "💜 CRYSTAL MASTER" if files_moved > 0 else "💎 ORGANIZED GENIUS"
        )
    else:
        grade = (
            "💯 LEGEND"
            if files_moved >= 10
            else "😐 Needs Work" if files_moved > 0 else "💩 Messy"
        )

    log.append(f"\n## 🧠 Project Grade: {grade}")
    log.append(f"**Stats:**")
    log.append(f"- Files moved: {files_moved}")
    log.append(f"- Protected files: {files_protected}")
    log.append(f"- Memory crystals: {crystals_found}")
    log.append(
        f"- Cleanup efficiency: {((files_moved + files_protected) / max(1, files_moved + files_protected + crystals_found)) * 100:.1f}%"
    )

    with open(project / "README_BROski_Report.md", "w", encoding="utf-8") as report:
        report.write("\n".join(log))

    return f"{project.name}: {grade} ({files_moved} files moved, {crystals_found} crystals)"


def scan_all_projects(root_folder):
    print(f"\n🔍 BROski Ultra Cleaner scanning: {root_folder}\n")
    results = []
    total_crystals = 0

    for item in Path(root_folder).iterdir():
        if item.is_dir():
            result = organize_project(item)
            results.append(result)
            # Count crystals from result string
            if "crystals)" in result:
                crystal_count = int(result.split("crystals)")[0].split()[-1])
                total_crystals += crystal_count

    print("\n🎉 BROSKI ULTRA CLEAN-UP COMPLETE:\n")
    for r in results:
        print("✅", r)

    print(f"\n💎 Total Memory Crystals Found: {total_crystals}")
    print(
        f"🧠 ChaosGenius Organization Level: {'LEGENDARY' if total_crystals > 10 else 'EPIC' if total_crystals > 0 else 'GETTING STARTED'}"
    )


if __name__ == "__main__":
    root = input(
        "Enter the path to your Projects Root Folder (e.g., C:\\Users\\YourName\\Documents\\Code):\n"
    ).strip()
    if Path(root).exists():
        scan_all_projects(root)
    else:
        print("❌ Invalid path! Please check and try again.")
