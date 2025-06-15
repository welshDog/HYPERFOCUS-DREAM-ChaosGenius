#!/usr/bin/env python3
"""
🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
    HYPERGATE CONNECTION MANAGER v1.0
🌌 QUANTUM SSH BRIDGE FOR CHIEF LYNDZ 🌌
👑 HYPERFOCUS EMPIRE REMOTE CONTROL 👑
"""

import json
import os
import socket
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path


class HyperGateManager:
    def __init__(self):
        self.config_file = Path.home() / ".hypergate" / "config.json"
        self.log_file = Path.home() / ".hypergate" / "connections.log"
        self.db_file = Path.home() / ".hypergate" / "hypergate.db"
        self.status_file = Path.home() / ".hypergate" / "status.json"

        # Create directories
        self.config_file.parent.mkdir(exist_ok=True)

        # Initialize database
        self.init_database()

        # Load configuration
        self.config = self.load_config()

        # Connection state
        self.is_connected = False
        self.connection_start_time = None
        self.monitor_thread = None
        self.stop_monitor = False

    def init_database(self):
        """Initialize SQLite database for connection tracking"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                server_ip TEXT,
                username TEXT,
                duration INTEGER,
                status TEXT,
                latency REAL
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_throughput REAL
            )
        """
        )

        conn.commit()
        conn.close()

    def load_config(self):
        """Load HyperGate configuration"""
        default_config = {
            "server_ip": "212.227.127.144",
            "username": "lyndz",
            "ssh_port": 22,
            "key_file": str(Path.home() / ".ssh" / "hypergate_ed25519"),
            "auto_reconnect": True,
            "keep_alive_interval": 30,
            "connection_timeout": 10,
            "max_reconnect_attempts": 5,
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    # Merge with defaults
                    default_config.update(config)
            except Exception as e:
                self.log(f"⚠️ Error loading config: {e}")

        return default_config

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log(f"⚠️ Error saving config: {e}")

    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        print(log_entry)

        # Write to log file
        try:
            with open(self.log_file, "a") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"⚠️ Error writing to log: {e}")

    def update_status(self, status_data):
        """Update status file for web interface"""
        try:
            with open(self.status_file, "w") as f:
                json.dump(status_data, f, indent=2)
        except Exception as e:
            self.log(f"⚠️ Error updating status: {e}")

    def test_connection(self):
        """Test SSH connection without connecting"""
        self.log("🧪 Testing HyperGate connection...")

        cmd = [
            "ssh",
            "-i",
            self.config["key_file"],
            "-p",
            str(self.config["ssh_port"]),
            "-o",
            "ConnectTimeout=5",
            "-o",
            "BatchMode=yes",
            "-o",
            "StrictHostKeyChecking=no",
            f"{self.config['username']}@{self.config['server_ip']}",
            'echo "HyperGate test successful"',
        ]

        try:
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            latency = round((time.time() - start_time) * 1000, 2)

            if result.returncode == 0:
                self.log(f"✅ Connection test PASSED (latency: {latency}ms)")
                return True, latency
            else:
                self.log(f"❌ Connection test FAILED: {result.stderr.strip()}")
                return False, None
        except subprocess.TimeoutExpired:
            self.log("❌ Connection test TIMEOUT")
            return False, None
        except Exception as e:
            self.log(f"❌ Connection test ERROR: {e}")
            return False, None

    def connect(self):
        """Establish HyperGate connection"""
        if self.is_connected:
            self.log("⚠️ HyperGate already connected!")
            return True

        self.log("🚀 Initiating HyperGate connection...")

        # Test connection first
        test_result, latency = self.test_connection()
        if not test_result:
            self.log("❌ Connection test failed. Aborting connection.")
            return False

        # Create SSH connection
        cmd = [
            "autossh",
            "-M",
            "0",
            "-i",
            self.config["key_file"],
            "-p",
            str(self.config["ssh_port"]),
            "-o",
            f"ServerAliveInterval={self.config['keep_alive_interval']}",
            "-o",
            "ServerAliveCountMax=3",
            "-o",
            f"ConnectTimeout={self.config['connection_timeout']}",
            "-o",
            "ExitOnForwardFailure=yes",
            "-o",
            "StrictHostKeyChecking=no",
            f"{self.config['username']}@{self.config['server_ip']}",
        ]

        try:
            # Start SSH connection in background
            self.ssh_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            # Give it a moment to establish
            time.sleep(3)

            # Check if connection is alive
            if self.ssh_process.poll() is None:
                self.is_connected = True
                self.connection_start_time = datetime.now()

                # Log to database
                self.log_connection(latency, "CONNECTED")

                # Start monitoring
                self.start_monitoring()

                self.log("✅ HyperGate connection established!")
                self.log("🌌 Welcome to the HyperFocus Empire, Chief Lyndz!")

                return True
            else:
                error_output = self.ssh_process.stderr.read().decode()
                self.log(f"❌ SSH connection failed: {error_output}")
                return False

        except Exception as e:
            self.log(f"❌ Connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect HyperGate"""
        if not self.is_connected:
            self.log("⚠️ HyperGate not connected!")
            return

        self.log("🔌 Disconnecting HyperGate...")

        # Stop monitoring
        self.stop_monitor = True
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

        # Terminate SSH process
        if hasattr(self, "ssh_process") and self.ssh_process:
            self.ssh_process.terminate()
            try:
                self.ssh_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ssh_process.kill()

        # Calculate session duration
        if self.connection_start_time:
            duration = (datetime.now() - self.connection_start_time).total_seconds()
            self.log_connection(None, "DISCONNECTED", duration)

        self.is_connected = False
        self.connection_start_time = None

        self.log("👋 HyperGate disconnected. Until next time, Chief!")

    def log_connection(self, latency, status, duration=None):
        """Log connection event to database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO connections (server_ip, username, duration, status, latency)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    self.config["server_ip"],
                    self.config["username"],
                    duration,
                    status,
                    latency,
                ),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            self.log(f"⚠️ Error logging to database: {e}")

    def start_monitoring(self):
        """Start connection monitoring thread"""
        self.stop_monitor = False
        self.monitor_thread = threading.Thread(
            target=self._monitor_connection, daemon=True
        )
        self.monitor_thread.start()

    def _monitor_connection(self):
        """Monitor connection health"""
        check_interval = 30  # seconds

        while not self.stop_monitor and self.is_connected:
            try:
                # Test connection
                test_result, latency = self.test_connection()

                if not test_result:
                    self.log("🔴 Connection lost! Attempting reconnection...")
                    if self.config["auto_reconnect"]:
                        self.reconnect()
                    else:
                        self.disconnect()
                        break
                else:
                    # Update status
                    uptime = (
                        datetime.now() - self.connection_start_time
                    ).total_seconds()
                    status_data = {
                        "connected": True,
                        "latency": latency,
                        "uptime": uptime,
                        "server": f"{self.config['username']}@{self.config['server_ip']}",
                        "last_check": datetime.now().isoformat(),
                    }
                    self.update_status(status_data)

                time.sleep(check_interval)

            except Exception as e:
                self.log(f"⚠️ Monitor error: {e}")
                time.sleep(check_interval)

    def reconnect(self):
        """Attempt to reconnect"""
        max_attempts = self.config["max_reconnect_attempts"]

        for attempt in range(1, max_attempts + 1):
            self.log(f"🔄 Reconnection attempt {attempt}/{max_attempts}")

            # Disconnect first
            if self.is_connected:
                self.disconnect()

            time.sleep(5)  # Wait before retry

            if self.connect():
                self.log("✅ Reconnection successful!")
                return True

            if attempt < max_attempts:
                wait_time = attempt * 10  # Exponential backoff
                self.log(f"⏳ Waiting {wait_time} seconds before next attempt...")
                time.sleep(wait_time)

        self.log("❌ All reconnection attempts failed!")
        return False

    def get_status(self):
        """Get current connection status"""
        if not self.is_connected:
            return {
                "connected": False,
                "status": "OFFLINE",
                "uptime": 0,
                "server": f"{self.config['username']}@{self.config['server_ip']}",
            }

        uptime = (datetime.now() - self.connection_start_time).total_seconds()
        return {
            "connected": True,
            "status": "ONLINE",
            "uptime": uptime,
            "server": f"{self.config['username']}@{self.config['server_ip']}",
            "start_time": self.connection_start_time.isoformat(),
        }

    def execute_remote_command(self, command):
        """Execute command on remote server"""
        if not self.is_connected:
            self.log("❌ Not connected to execute command!")
            return False, "Not connected"

        cmd = [
            "ssh",
            "-i",
            self.config["key_file"],
            "-p",
            str(self.config["ssh_port"]),
            f"{self.config['username']}@{self.config['server_ip']}",
            command,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)

    def get_connection_stats(self):
        """Get connection statistics from database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Get total connections
            cursor.execute(
                "SELECT COUNT(*) FROM connections WHERE status = 'CONNECTED'"
            )
            total_connections = cursor.fetchone()[0]

            # Get average latency
            cursor.execute(
                "SELECT AVG(latency) FROM connections WHERE latency IS NOT NULL"
            )
            avg_latency = cursor.fetchone()[0] or 0

            # Get total uptime
            cursor.execute(
                "SELECT SUM(duration) FROM connections WHERE duration IS NOT NULL"
            )
            total_uptime = cursor.fetchone()[0] or 0

            conn.close()

            return {
                "total_connections": total_connections,
                "average_latency": round(avg_latency, 2),
                "total_uptime": round(total_uptime / 3600, 2),  # hours
            }
        except Exception as e:
            self.log(f"⚠️ Error getting stats: {e}")
            return {"total_connections": 0, "average_latency": 0, "total_uptime": 0}


def main():
    """Main HyperGate CLI interface"""
    print("🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐")
    print("    HYPERGATE CONNECTION MANAGER")
    print("🌌 Quantum SSH Bridge for Chief Lyndz 🌌")
    print("🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐")
    print()

    hypergate = HyperGateManager()

    if len(sys.argv) < 2:
        print("Usage: python hypergate_manager.py [command]")
        print()
        print("Commands:")
        print("  connect    - Connect to HyperFocus server")
        print("  disconnect - Disconnect from server")
        print("  status     - Show connection status")
        print("  test       - Test connection")
        print("  stats      - Show connection statistics")
        print("  monitor    - Start monitoring mode")
        print("  config     - Show configuration")
        return

    command = sys.argv[1].lower()

    if command == "connect":
        success = hypergate.connect()
        if success:
            print("🎉 HyperGate connected successfully!")
            # Keep alive until interrupted
            try:
                while hypergate.is_connected:
                    time.sleep(1)
            except KeyboardInterrupt:
                hypergate.disconnect()
        else:
            print("❌ Failed to connect HyperGate")
            sys.exit(1)

    elif command == "disconnect":
        hypergate.disconnect()

    elif command == "status":
        status = hypergate.get_status()
        print(f"🔗 Connection: {status['status']}")
        print(f"📡 Server: {status['server']}")
        if status["connected"]:
            uptime_hours = status["uptime"] / 3600
            print(f"⏱️ Uptime: {uptime_hours:.2f} hours")

    elif command == "test":
        success, latency = hypergate.test_connection()
        if success:
            print(f"✅ Connection test PASSED (latency: {latency}ms)")
        else:
            print("❌ Connection test FAILED")

    elif command == "stats":
        stats = hypergate.get_connection_stats()
        print(f"📊 Total connections: {stats['total_connections']}")
        print(f"⚡ Average latency: {stats['average_latency']}ms")
        print(f"⏱️ Total uptime: {stats['total_uptime']} hours")

    elif command == "monitor":
        if hypergate.connect():
            print("🔍 Monitoring mode started. Press Ctrl+C to stop.")
            try:
                while True:
                    status = hypergate.get_status()
                    if status["connected"]:
                        print(f"🟢 ONLINE - Uptime: {status['uptime']:.0f}s")
                    else:
                        print("🔴 OFFLINE")
                    time.sleep(10)
            except KeyboardInterrupt:
                hypergate.disconnect()

    elif command == "config":
        print("🔧 HyperGate Configuration:")
        for key, value in hypergate.config.items():
            print(f"  {key}: {value}")

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
