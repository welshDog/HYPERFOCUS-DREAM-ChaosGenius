#!/usr/bin/env python3
"""
🚀 ChaosGenius Engine - Quick Start Script
==========================================
One-click setup and launch for the complete ChaosGenius ecosystem
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Display startup banner"""
    print("\n" + "="*60)
    print("🧠 CHAOSGENIUS ENGINE - QUICK START")
    print("="*60)
    print("🚀 Launching your neurodivergent business empire...")
    print("💜 Built for minds that think differently")
    print("\n" + "-"*60)

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("⚠️ requirements.txt not found - continuing anyway")
        return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    directories = [
        "production_assets/product_ideas",
        "production_assets/automation_scripts",
        "generated_docs",
        "logs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure created")

def launch_dashboard():
    """Launch the ChaosGenius Dashboard"""
    print("\n🎛️ Launching ChaosGenius Dashboard...")
    print("📍 Dashboard will be available at: http://localhost:5000")
    print("\n🎯 Dashboard Features:")
    print("   • 🧠 AI Squad Launch")
    print("   • 🛠️ Product Creation")
    print("   • 📊 Analytics & Insights")
    print("   • 💼 Empire Status Tracking")
    print("\n⏳ Starting server... (this may take a moment)")
    
    try:
        # Start the dashboard
        subprocess.run([sys.executable, "dashboard_api.py"])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Dashboard error: {e}")
        print("💡 Try running manually: python dashboard_api.py")

def main():
    """Main startup sequence"""
    print_banner()
    
    # Check system requirements
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️ Continuing despite dependency issues...")
    
    # Setup directories
    create_directories()
    
    # Launch dashboard
    print("\n🎉 Setup complete! Launching dashboard...")
    time.sleep(1)
    launch_dashboard()

if __name__ == "__main__":
    main()