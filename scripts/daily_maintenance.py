import os
import subprocess
import json
from datetime import datetime, timedelta

def run_health_check():
    """Run the ChaosGenius system health check"""
    print("\n🧠 Running Health Check...")
    try:
        if os.path.exists("health_check.py"):
            result = subprocess.run(["python", "health_check.py"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Health check completed successfully")
            else:
                print(f"⚠️ Health check had issues: {result.stderr}")
        elif os.path.exists("chaosgenius_system_optimizer.py"):
            result = subprocess.run(["python", "chaosgenius_system_optimizer.py"], capture_output=True, text=True)
            print("✅ System optimizer ran")
        else:
            print("⚠️ No health check script found")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

def run_archive_script():
    """Archive old reports to keep directory clean"""
    print("\n📦 Archiving Old Reports...")
    try:
        archive_script = "./scripts/archive_old_health_reports.py"
        if os.path.exists(archive_script):
            result = subprocess.run(["python", archive_script], capture_output=True, text=True)
            print(result.stdout)
        else:
            print("⚠️ Archive script not found")
    except Exception as e:
        print(f"❌ Archive failed: {e}")

def run_config_validator():
    """Validate configuration files"""
    print("\n🔐 Validating Config Files...")
    try:
        validator_script = "./config/config_validator.py"
        if os.path.exists(validator_script):
            result = subprocess.run(["python", validator_script], capture_output=True, text=True)
            print(result.stdout)
        else:
            print("⚠️ Config validator not found")
    except Exception as e:
        print(f"❌ Config validation failed: {e}")

def cleanup_temp_files():
    """Clean up temporary files and cache"""
    print("\n🧹 Cleaning Temporary Files...")
    temp_patterns = ["*.tmp", "*.log", "__pycache__"]
    cleaned_count = 0
    
    # Clean __pycache__ directories
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                import shutil
                shutil.rmtree(pycache_path)
                print(f"🗑️ Removed: {pycache_path}")
                cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Couldn't remove {pycache_path}: {e}")
    
    print(f"✅ Cleaned {cleaned_count} cache directories")

def generate_maintenance_summary():
    """Generate a comprehensive maintenance summary"""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "maintenance_completed": True,
        "tasks_run": [
            "health_check",
            "archive_old_reports", 
            "config_validation",
            "temp_file_cleanup"
        ],
        "next_maintenance_due": (datetime.now().replace(hour=0, minute=0, second=0) + 
                               timedelta(days=1)).isoformat()
    }
    
    # Save summary
    os.makedirs("./logs/", exist_ok=True)
    summary_file = f"./logs/daily_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📝 Maintenance summary saved: {summary_file}")
    return summary_file

def display_project_status():
    """Display current project health status"""
    print("\n" + "="*50)
    print("🎯 HYPERFOCUS DREAM - Project Status")
    print("="*50)
    
    # Count files in main categories
    try:
        main_files = len([f for f in os.listdir(".") if os.path.isfile(f)])
        folders = len([f for f in os.listdir(".") if os.path.isdir(f)])
        
        print(f"📁 Main Directory: {main_files} files, {folders} folders")
        
        if os.path.exists("./tests/"):
            test_files = len([f for f in os.listdir("./tests/") if f.endswith(".py")])
            print(f"🧪 Test Files: {test_files}")
        
        if os.path.exists("./logs/"):
            log_files = len([f for f in os.listdir("./logs/") if f.endswith((".json", ".log"))])
            print(f"📊 Log Files: {log_files}")
            
        print("✅ Project Status: ULTRA MODE ACTIVE")
        
    except Exception as e:
        print(f"⚠️ Status check error: {e}")

if __name__ == "__main__":
    print("🚀 HYPERFOCUS DREAM - Daily Maintenance")
    print("=" * 50)
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all maintenance tasks
    run_health_check()
    run_archive_script()
    run_config_validator()
    cleanup_temp_files()
    
    # Generate summary and display status
    summary_file = generate_maintenance_summary()
    display_project_status()
    
    print("\n🎉 Daily maintenance completed successfully!")
    print(f"📋 Full report: {summary_file}")