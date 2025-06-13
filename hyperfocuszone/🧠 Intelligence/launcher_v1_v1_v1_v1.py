#!/usr/bin/env python3
"""
🚀💥 HYPERFOCUSzone Auto Monitor & Launcher 💥🚀
Keep your ADHD empire running at LEGENDARY performance!
"""

import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests


class HyperfocusZoneLauncher:
    def __init__(self):
        self.flask_process = None
        self.project_dir = Path(__file__).parent
        self.log_file = self.project_dir / "launcher.log"
        self.running = True
        self.venv_python = self.project_dir / "venv" / "bin" / "python3"

    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        # Write to log file
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    def check_server_health(self):
        """Check if the Flask server is responding"""
        try:
            response = requests.get("http://localhost:5000/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def start_flask_server(self):
        """Start the Flask application"""
        try:
            self.log("🚀 Starting HYPERFOCUSzone Flask server...")

            # Change to project directory
            os.chdir(self.project_dir)

            # Use virtual environment Python if available
            python_cmd = (
                str(self.venv_python) if self.venv_python.exists() else sys.executable
            )

            # Start Flask server
            self.flask_process = subprocess.Popen(
                [python_cmd, "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Wait a moment for startup
            time.sleep(3)

            if self.check_server_health():
                self.log("✅ Flask server started successfully!")
                self.log("🌐 Portal available at: http://localhost:5000")
                self.log(
                    "🎯 Command Center: http://localhost:5000/ultimate-command-center"
                )
                return True
            else:
                self.log("❌ Flask server failed to start properly")
                return False

        except Exception as e:
            self.log(f"❌ Failed to start Flask server: {e}")
            return False

    def restart_server(self):
        """Restart the Flask server"""
        self.log("🔄 Restarting HYPERFOCUSzone server...")

        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process.wait()
            self.flask_process = None
            time.sleep(2)

        return self.start_flask_server()

    def monitor_loop(self):
        """Main monitoring loop"""
        self.log("🧠⚡ HYPERFOCUSzone Auto Monitor Started! ⚡🧠")
        self.log("💜 Keeping your ADHD empire running smoothly...")

        # Start initial server
        if not self.start_flask_server():
            self.log("💥 Initial startup failed! Check your setup.")
            return

        health_check_interval = 30  # Check every 30 seconds
        last_check = time.time()
        consecutive_failures = 0

        try:
            while self.running:
                current_time = time.time()

                # Health check
                if current_time - last_check >= health_check_interval:
                    if self.check_server_health():
                        if consecutive_failures > 0:
                            self.log("✅ Server health restored!")
                            consecutive_failures = 0
                        # Periodic healthy status
                        if int(current_time) % 300 == 0:  # Every 5 minutes
                            self.log(
                                "💚 HYPERFOCUSzone running smoothly - LEGENDARY STATUS!"
                            )
                    else:
                        consecutive_failures += 1
                        self.log(
                            f"⚠️ Health check failed (attempt {consecutive_failures})"
                        )

                        if consecutive_failures >= 3:
                            self.log(
                                "🚨 Multiple health check failures - restarting server!"
                            )
                            if self.restart_server():
                                consecutive_failures = 0
                            else:
                                self.log(
                                    "💥 Restart failed! Manual intervention needed."
                                )
                                break

                    last_check = current_time

                time.sleep(1)  # Sleep 1 second between checks

        except KeyboardInterrupt:
            self.log("🛑 Monitor stopped by user")
        except Exception as e:
            self.log(f"💥 Monitor error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean shutdown"""
        self.log("🧹 Cleaning up...")
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process.wait()
        self.log("👋 HYPERFOCUSzone Monitor shutdown complete!")

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.log(f"📡 Received signal {signum}")
        self.running = False


if __name__ == "__main__":
    launcher = HyperfocusZoneLauncher()

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, launcher.signal_handler)
    signal.signal(signal.SIGTERM, launcher.signal_handler)

    try:
        launcher.monitor_loop()
    except Exception as e:
        launcher.log(f"💥 Fatal error: {e}")
        sys.exit(1)
