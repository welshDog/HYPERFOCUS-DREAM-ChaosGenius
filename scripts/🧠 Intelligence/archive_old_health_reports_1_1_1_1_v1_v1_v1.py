#!/usr/bin/env python3
"""
Archive Old Health Reports Script
Automatically archives old health check reports and logs to keep the workspace clean.
"""

import glob
import json
import os
import shutil
import sqlite3
from datetime import datetime, timedelta


def create_archive_directory():
    """Create archive directory if it doesn't exist"""
    archive_dir = "archives"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    return archive_dir


def archive_old_logs():
    """Archive old log files"""
    archive_dir = create_archive_directory()
    log_files = glob.glob("*.log") + glob.glob("*log*.txt") + glob.glob("*log*.json")

    archived_count = 0
    for log_file in log_files:
        if os.path.exists(log_file):
            # Check if file is older than 7 days
            file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
            if datetime.now() - file_time > timedelta(days=7):
                dest_path = os.path.join(archive_dir, f"archived_{log_file}")
                shutil.move(log_file, dest_path)
                archived_count += 1
                print(f"Archived: {log_file} -> {dest_path}")

    return archived_count


def archive_old_reports():
    """Archive old health reports and cleanup files"""
    archive_dir = create_archive_directory()
    report_files = (
        glob.glob("*report*.txt")
        + glob.glob("*report*.json")
        + glob.glob("cleanup_log_*.json")
    )

    archived_count = 0
    for report_file in report_files:
        if os.path.exists(report_file):
            # Archive reports older than 30 days
            file_time = datetime.fromtimestamp(os.path.getmtime(report_file))
            if datetime.now() - file_time > timedelta(days=30):
                dest_path = os.path.join(archive_dir, f"archived_{report_file}")
                shutil.move(report_file, dest_path)
                archived_count += 1
                print(f"Archived: {report_file} -> {dest_path}")

    return archived_count


def cleanup_temp_files():
    """Clean up temporary files and cache"""
    temp_patterns = ["*.tmp", "*.temp", "__pycache__", "*.pyc", ".pytest_cache"]
    cleaned_count = 0

    for pattern in temp_patterns:
        files = glob.glob(pattern, recursive=True)
        for file in files:
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    cleaned_count += 1
                elif os.path.isdir(file):
                    shutil.rmtree(file)
                    cleaned_count += 1
                print(f"Cleaned: {file}")
            except Exception as e:
                print(f"Warning: Could not clean {file}: {e}")

    return cleaned_count


def main():
    """Main archive and cleanup function"""
    print("🧹 Starting Archive & Cleanup Process...")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # Archive old logs
        log_count = archive_old_logs()
        print(f"📋 Archived {log_count} old log files")

        # Archive old reports
        report_count = archive_old_reports()
        print(f"📊 Archived {report_count} old report files")

        # Clean up temporary files
        temp_count = cleanup_temp_files()
        print(f"🗑️ Cleaned {temp_count} temporary files")

        # Create cleanup summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "archived_logs": log_count,
            "archived_reports": report_count,
            "cleaned_temp_files": temp_count,
            "status": "success",
        }

        with open(
            f"cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w"
        ) as f:
            json.dump(summary, f, indent=2)

        print("✅ Archive & Cleanup completed successfully!")
        print(f"📈 Total files processed: {log_count + report_count + temp_count}")

    except Exception as e:
        print(f"❌ Error during archive & cleanup: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
