#!/usr/bin/env python3
"""
🚀 ChaosGenius Startup Manager
================================
One-click startup for the entire ChaosGenius ecosystem
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class ChaosGeniusLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def check_requirements(self):
        """Check if all required files exist"""
        required_files = [
            "dashboard_api.py",
            "chaosgenius_discord_bot.py",
            "requirements.txt"
        ]
        
        missing_files = [f for f in required_files if not Path(f).exists()]
        
        if missing_files:
            print(f"❌ Missing required files: {missing_files}")
            return False
        return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    def create_directories(self):
        """Create necessary directories"""
        dirs = ["logs", "production_assets/product_ideas", "generated_docs"]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        print("✅ Directories created")
    
    def start_dashboard(self):
        """Start the dashboard API"""
        print("🎛️ Starting ChaosGenius Dashboard...")
        process = subprocess.Popen([sys.executable, "dashboard_api.py"])
        self.processes.append(("Dashboard", process))
        time.sleep(3)  # Give dashboard time to start
        return process
    
    def start_discord_bot(self):
        """Start the Discord bot if token is available"""
        if os.getenv('DISCORD_BOT_TOKEN'):
            print("🤖 Starting Discord Bot...")
            process = subprocess.Popen([sys.executable, "chaosgenius_discord_bot.py"])
            self.processes.append(("Discord Bot", process))
            return process
        else:
            print("⚠️ Discord bot token not found - skipping bot startup")
            return None
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down ChaosGenius...")
        self.running = False
        self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown all processes"""
        for name, process in self.processes:
            print(f"🔌 Stopping {name}...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("💜 ChaosGenius shutdown complete")
        sys.exit(0)
    
    def monitor_processes(self):
        """Monitor running processes and restart if needed"""
        while self.running:
            for i, (name, process) in enumerate(self.processes):
                if process.poll() is not None:  # Process has terminated
                    print(f"⚠️ {name} process terminated unexpectedly")
                    # Could implement restart logic here
            time.sleep(5)
    
    def launch(self):
        """Main launch sequence"""
        print("🧠 ChaosGenius Startup Manager")
        print("=" * 40)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Pre-flight checks
        if not self.check_requirements():
            return False
        
        self.create_directories()
        
        # Install dependencies
        if not self.install_dependencies():
            return False
        
        # Start services
        dashboard_process = self.start_dashboard()
        discord_process = self.start_discord_bot()
        
        print("\n🚀 ChaosGenius Systems Online!")
        print("=" * 40)
        print("🎛️ Dashboard: http://localhost:5000")
        print("📚 API Docs: http://localhost:5000/apidocs/")
        if discord_process:
            print("🤖 Discord Bot: Active")
        print("\n✨ Press Ctrl+C to stop all services")
        print("💜 Building neurodivergent empires...")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        monitor_thread.start()
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
        
        return True

if __name__ == "__main__":
    launcher = ChaosGeniusLauncher()
    success = launcher.launch()
    if not success:
        sys.exit(1)