#!/usr/bin/env python3
"""
🚀💜 QUICK LAUNCH - Get ChaosGenius Online NOW! 💜🚀
Emergency startup script for broke geniuses who need their empire LIVE!
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def check_python():
    """Ensure Python is ready"""
    print("🐍 Python check:", sys.version)
    return True


def install_minimal_deps():
    """Install only what we NEED"""
    print("📦 Installing minimal dependencies...")
    minimal_packages = ["flask==2.3.3", "flask-cors==4.0.0", "requests==2.31.0"]

    for package in minimal_packages:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                check=True,
            )
            print(f"✅ {package}")
        except:
            print(f"⚠️ Failed to install {package} - continuing anyway")


def start_dashboard():
    """Launch the optimized dashboard"""
    print("\n🚀 LAUNCHING CHAOSGENIUS DASHBOARD...")
    print("💜 This will run on http://localhost:5000")
    print("🎯 Press Ctrl+C to stop")
    print("\n" + "=" * 50)

    # Set environment for production
    os.environ["FLASK_ENV"] = "production"
    os.environ["PYTHONPATH"] = str(Path.cwd())

    # Launch dashboard
    try:
        subprocess.run([sys.executable, "dashboard_api.py"])
    except KeyboardInterrupt:
        print("\n\n💜 Dashboard stopped. Your empire sleeps... for now! 💜")


def main():
    print("🧠💜 CHAOSGENIUS EMERGENCY STARTUP 💜🧠")
    print("Getting your neurodivergent empire online in 30 seconds!")
    print()

    if not check_python():
        print("❌ Python check failed!")
        return

    install_minimal_deps()
    start_dashboard()


if __name__ == "__main__":
    main()
