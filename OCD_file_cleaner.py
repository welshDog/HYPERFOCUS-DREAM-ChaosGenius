#!/usr/bin/env python3

import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# 🌌 ULTRA STRUCTURE MAP INTEGRATION
ULTRA_FOLDER_STRUCTURE = {
    # 🧠 AI & Intelligence Systems
    "🧠 Intelligence": [".py", ".ipynb", ".pkl", ".model"],
    "ai_agents": [".py"],
    "ai_modules": [".py"],
    # 💰 Revenue & Business Systems
    "💰 Revenue Systems": [".py", ".json"],
    "business_data": [".csv", ".xlsx", ".json"],
    # 🚀 Deployment & Infrastructure
    "🚀 Deployment": [".sh", ".yml", ".yaml", ".dockerfile", ".json"],
    "scripts": [".sh", ".bat", ".ps1"],
    # 🔐 Security & Authentication
    "🔐 Secure Backups": [".key", ".pem", ".cert", ".env"],
    "backups": [".tar.gz", ".zip", ".backup"],
    # 🎨 Frontend & UI
    "🎨 Frontend & UI": [".html", ".css", ".js", ".ts", ".vue", ".react"],
    "assets": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".mp3", ".ttf", ".otf"],
    # 🗄️ Databases & Data
    "🗄️ Databases": [".db", ".sqlite", ".sql"],
    "data": [".csv", ".json", ".xml", ".parquet"],
    # 📝 Documentation
    "📝 Documentation": [".md", ".txt", ".pdf", ".docx"],
    "generated_docs": [".html", ".pdf"],
    # 🧪 Testing & Health
    "🧪 Testing & Health": [".py", ".json"],
    "logs": [".log", ".txt"],
    # ⚙️ Configuration
    "⚙️ Configuration": [".env", ".json", ".yaml", ".yml", ".ini", ".cfg", ".toml"],
    # 📦 Archives & Build
    "📦 Archives & Backups": [".tar.gz", ".zip", ".rar", ".7z"],
    "build": [".exe", ".dll", ".so", ".bin"],
    # 💎 Special BROski Files
    "crystals": [".broski"],  # 💎 BROski Memory Crystals!
    "🌌 Ultra Systems": [".ultra", ".galaxy"],  # 🌌 Galaxy-tier files
}

JUNK_FILES = [".DS_Store", "Thumbs.db", ".log", ".tmp", "__pycache__", "*.pyc"]

# 💜 CHAOSGENIUS ULTRA PROTECTED FILES - Never touch these legendary files!
ULTRA_PROTECTED_FILES = [
    "app.py",
    "broski_core.py",
    "dashboard_api.py",
    "chaosgenius_discord_bot.py",
    "business_agent_god.py",
    "ULTRA_STRUCTURE_MAP.md",
    "update_structure_map.sh",
    "OCD_file_cleaner.py",
    "quick_launch.sh",
    "launch_empire.sh",
    "immortal_guardian_ultra.py",
    "hyperfocus_zone_ultra_launcher.py",
]


def update_structure_map():
    """🔄 Auto-update the ULTRA Structure Map after cleaning"""
    try:
        result = subprocess.run(
            ["./update_structure_map.sh"],
            capture_output=True,
            text=True,
            cwd="/root/chaosgenius",
        )
        if result.returncode == 0:
            return "✅ ULTRA Structure Map updated successfully!"
        else:
            return f"⚠️ Structure map update had issues: {result.stderr}"
    except Exception as e:
        return f"⚠️ Couldn't update structure map: {e}"


def organize_ultra_project(project_path):
    """🌌 ULTRA Organization with Structure Map Integration"""
    log = []
    project = Path(project_path)
    if not project.is_dir():
        return f"Skipping non-folder: {project}"

    log.append(f"# 🌌 ULTRA BROSKI ORGANIZATION REPORT: {project.name}")
    log.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append("**ChaosGenius ULTRA OCD Cleaner v3.0** 🧠💜🌌\n")

    files_moved = 0
    files_protected = 0
    crystals_found = 0
    ultra_files_found = 0
    galaxy_tier_moves = 0

    for file in project.rglob("*"):
        if file.is_file():
            # 🛡️ ULTRA Protection for legendary system files
            if file.name in ULTRA_PROTECTED_FILES:
                log.append(f"🛡️⭐ ULTRA PROTECTED: {file.name} (legendary system file)")
                files_protected += 1
                continue

            # 🗑️ Eliminate junk with extreme prejudice
            if any(junk in file.name for junk in JUNK_FILES):
                try:
                    file.unlink()
                    log.append(f"🗑️💥 OBLITERATED junk file: {file}")
                except (OSError, PermissionError) as e:
                    log.append(f"⚠️ Couldn't obliterate {file}: {e}")
                continue

            moved = False
            for folder, extensions in ULTRA_FOLDER_STRUCTURE.items():
                if file.suffix.lower() in extensions:
                    # 💎 Special handling for BROski crystals
                    if file.suffix == ".broski":
                        crystals_found += 1
                        log.append(f"💎✨ MEMORY CRYSTAL DISCOVERED: {file.name}")

                    # 🌌 Special handling for Ultra/Galaxy files
                    if file.suffix in [".ultra", ".galaxy"]:
                        ultra_files_found += 1
                        galaxy_tier_moves += 1
                        log.append(f"🌌⚡ GALAXY-TIER FILE DETECTED: {file.name}")

                    target_folder = project / folder
                    target_folder.mkdir(exist_ok=True)
                    new_path = target_folder / file.name

                    # Avoid overwriting existing files with ULTRA precision
                    counter = 1
                    while new_path.exists():
                        stem = file.stem
                        suffix = file.suffix
                        new_path = target_folder / f"{stem}_v{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(file), str(new_path))
                        folder_icon = "🌌" if "Ultra" in folder else "📁"
                        log.append(f"{folder_icon} RELOCATED: {file.name} → {folder}/")
                        files_moved += 1
                    except (OSError, PermissionError) as e:
                        log.append(f"⚠️ RELOCATION FAILED for {file.name}: {e}")
                    moved = True
                    break

            if not moved:
                log.append(f"❓ LEFT IN PLACE: {file.name}")

    # 🧠 ULTRA Enhanced grading system
    total_special = crystals_found + ultra_files_found
    if total_special > 0 and galaxy_tier_moves > 0:
        if files_moved >= 20:
            grade = "🌌💎 GALAXY EMPEROR"
        elif files_moved >= 10:
            grade = "🧠⚡ ULTRA LEGEND"
        else:
            grade = "💜🌀 CRYSTAL GUARDIAN"
    elif crystals_found > 0:
        if files_moved >= 10:
            grade = "🧠💎 BROSKI LEGEND"
        elif files_moved > 0:
            grade = "💜 CRYSTAL MASTER"
        else:
            grade = "💎 ORGANIZED GENIUS"
    else:
        if files_moved >= 15:
            grade = "💯⚡ ULTRA LEGEND"
        elif files_moved >= 5:
            grade = "🔥 SOLID WORK"
        else:
            grade = "😐 Needs ULTRA Boost"

    log.append(f"\n## 🌌 ULTRA PROJECT GRADE: {grade}")
    log.append("**🧠 ULTRA STATS:**")
    log.append(f"- Files relocated: {files_moved}")
    log.append(f"- Protected legendary files: {files_protected}")
    log.append(f"- Memory crystals discovered: {crystals_found}")
    log.append(f"- Galaxy-tier files: {ultra_files_found}")
    log.append(f"- Galaxy relocations: {galaxy_tier_moves}")

    total_files = files_moved + files_protected + crystals_found + ultra_files_found
    efficiency = ((files_moved + files_protected) / max(1, total_files)) * 100
    log.append(f"- ULTRA cleanup efficiency: {efficiency:.1f}%")

    # 🔄 Update the ULTRA Structure Map
    log.append(f"\n## 🔄 STRUCTURE MAP INTEGRATION")
    map_update_result = update_structure_map()
    log.append(f"- {map_update_result}")

    report_path = project / "🌌_ULTRA_BROski_Report.md"
    with open(report_path, "w", encoding="utf-8") as report:
        report.write("\n".join(log))

    return (
        f"{project.name}: {grade} ({files_moved} files moved, "
        f"{crystals_found} crystals, {ultra_files_found} galaxy-tier)"
    )


def scan_all_projects(root_folder):
    print(f"\n🔍 BROski Ultra Cleaner scanning: {root_folder}\n")
    results = []
    total_crystals = 0

    for item in Path(root_folder).iterdir():
        if item.is_dir():
            result = organize_ultra_project(item)
            results.append(result)
            # Count crystals from result string
            if "crystals)" in result:
                crystal_count = int(result.split("crystals)")[0].split()[-1])
                total_crystals += crystal_count

    print("\n🎉 BROSKI ULTRA CLEAN-UP COMPLETE:\n")
    for r in results:
        print("✅", r)

    print(f"\n💎 Total Memory Crystals Found: {total_crystals}")
    if total_crystals > 10:
        org_level = "LEGENDARY"
    elif total_crystals > 0:
        org_level = "EPIC"
    else:
        org_level = "GETTING STARTED"
    print(f"🧠 ChaosGenius Organization Level: {org_level}")


if __name__ == "__main__":
    # 🌌 ULTRA Auto-mode for ChaosGenius workspace
    import sys

    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "/root/chaosgenius"  # Default to current workspace

    print(f"🌌 ULTRA BROSKI CLEANER v3.0 - Galaxy Mode Activated!")
    print(f"🎯 Target: {root}")

    if Path(root).exists():
        scan_all_projects(root)
        print(f"\n🔄 Updating ULTRA Structure Map...")
        map_result = update_structure_map()
        print(f"✅ {map_result}")
    else:
        print("❌ Invalid path! Please check and try again.")
        prompt_text = (
            "Enter the path to your Projects Root Folder "
            "(e.g., /home/user/projects):\n"
        )
        root = input(prompt_text).strip()
        if Path(root).exists():
            scan_all_projects(root)
        else:
            print("❌ Invalid path! Please check and try again.")
