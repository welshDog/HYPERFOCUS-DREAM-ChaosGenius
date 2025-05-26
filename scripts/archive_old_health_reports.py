import os
import shutil
from datetime import datetime, timedelta
import json

def archive_old_health_reports():
    """Archive old health reports and project analysis files to keep main directory clean"""
    
    # Configuration
    SOURCE_DIR = "./"
    ARCHIVE_DIR = "./archives/2025_q1/"
    CUTOFF_DATE = datetime.now() - timedelta(days=7)  # Archive files older than 7 days
    
    # Ensure archive directory exists
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    archived_files = []
    total_size_saved = 0
    
    # Patterns to archive
    archive_patterns = [
        "health_report_",
        "project_analysis_report_",
        "project_optimization_log_",
        "test_report_",
        "file_organization_log_"
    ]
    
    print("🗂️ Scanning for files to archive...")
    
    try:
        for filename in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
                
            # Check if file matches archive patterns
            should_archive = any(filename.startswith(pattern) for pattern in archive_patterns)
            
            if should_archive and os.path.isfile(file_path):
                # Check file age
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_mod_time < CUTOFF_DATE:
                    # Calculate file size
                    file_size = os.path.getsize(file_path)
                    total_size_saved += file_size
                    
                    # Move file to archive
                    dest_path = os.path.join(ARCHIVE_DIR, filename)
                    shutil.move(file_path, dest_path)
                    archived_files.append(filename)
                    print(f"📦 Archived: {filename} ({file_size} bytes)")
        
        # Generate archive summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "files_archived": len(archived_files),
            "total_size_saved": total_size_saved,
            "archive_location": ARCHIVE_DIR,
            "archived_files": archived_files
        }
        
        # Save archive log
        log_file = os.path.join(ARCHIVE_DIR, f"archive_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        if archived_files:
            print(f"\n✅ Archive Complete!")
            print(f"📁 Files archived: {len(archived_files)}")
            print(f"💾 Space saved: {total_size_saved:,} bytes")
            print(f"📍 Archive location: {ARCHIVE_DIR}")
        else:
            print("\n✅ No files needed archiving - system is already clean!")
            
    except Exception as e:
        print(f"❌ Archive error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 HYPERFOCUS DREAM - Archive System")
    print("=" * 50)
    archive_old_health_reports()
    print("=" * 50)
    print("📋 Archive process completed!")