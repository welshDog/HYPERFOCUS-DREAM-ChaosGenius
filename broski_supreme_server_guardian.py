#!/usr/bin/env python3
"""
🛡️💻 BROSKI SUPREME SERVER GUARDIAN 💻🛡️
🌌 Ultimate Server Monitoring & Resource Management 🌌
👑 By Command of Chief Lyndz - Always Running SUPREME! 👑
"""

import asyncio
import json
import logging
import os
import psutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BroskiSupremeServerGuardian:
    """🛡️ Ultimate Server Guardian & Resource Manager"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.guardian_db = f"{self.base_path}/broski_server_guardian.db"
        self.config_file = f"{self.base_path}/server_guardian_config.json"

        # Server limits and thresholds
        self.resource_limits = {
            "cpu_warning": 75.0,      # CPU usage warning threshold
            "cpu_critical": 90.0,     # CPU usage critical threshold
            "memory_warning": 80.0,   # Memory usage warning threshold
            "memory_critical": 95.0,  # Memory usage critical threshold
            "disk_warning": 85.0,     # Disk usage warning threshold
            "disk_critical": 95.0,    # Disk usage critical threshold
            "load_warning": 4.0,      # System load warning
            "load_critical": 8.0      # System load critical
        }

        # Process monitoring
        self.monitored_processes = [
            "python3",
            "node",
            "nginx",
            "postgresql",
            "redis-server"
        ]

        # Auto-optimization settings
        self.auto_optimize = True
        self.monitoring_active = False

        print("🛡️💜 BROSKI SUPREME SERVER GUARDIAN ONLINE! 💜🛡️")
        self._initialize_guardian_database()
        self._load_config()

    def _initialize_guardian_database(self):
        """🗄️ Initialize server monitoring database"""
        try:
            with sqlite3.connect(self.guardian_db) as conn:
                cursor = conn.cursor()

                # Server metrics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS server_metrics (
                        timestamp REAL,
                        cpu_usage REAL,
                        memory_usage REAL,
                        disk_usage REAL,
                        system_load REAL,
                        processes_count INTEGER,
                        network_io TEXT,
                        disk_io TEXT
                    )
                """)

                # Resource alerts table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS resource_alerts (
                        timestamp REAL,
                        alert_type TEXT,
                        resource_type TEXT,
                        current_value REAL,
                        threshold REAL,
                        action_taken TEXT,
                        resolved BOOLEAN DEFAULT FALSE
                    )
                """)

                # Process monitoring table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS process_monitoring (
                        timestamp REAL,
                        process_name TEXT,
                        pid INTEGER,
                        cpu_percent REAL,
                        memory_percent REAL,
                        status TEXT
                    )
                """)

                conn.commit()
                logger.info("🛡️ Server Guardian database initialized!")

        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    def _load_config(self):
        """⚙️ Load configuration settings"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                self.resource_limits.update(config.get('resource_limits', {}))
                self.auto_optimize = config.get('auto_optimize', True)
        except Exception as e:
            logger.warning(f"Config load warning: {e}")
            self._save_default_config()

    def _save_default_config(self):
        """💾 Save default configuration"""
        config = {
            "resource_limits": self.resource_limits,
            "auto_optimize": self.auto_optimize,
            "monitoring_interval": 10,
            "optimization_cooldown": 300,
            "version": "1.0.0"
        }

        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Config save error: {e}")

    def get_system_stats(self) -> Dict:
        """📊 Get comprehensive system statistics"""
        try:
            # CPU stats
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()

            # Memory stats
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            # Disk stats
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()

            # Network stats
            network = psutil.net_io_counters()

            # System load
            load_avg = os.getloadavg()

            # Process count
            processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))

            stats = {
                "timestamp": time.time(),
                "cpu": {
                    "usage_percent": cpu_usage,
                    "count": cpu_count,
                    "frequency": cpu_freq.current if cpu_freq else None,
                    "load_avg": load_avg
                },
                "memory": {
                    "total": memory.total,
                    "used": memory.used,
                    "available": memory.available,
                    "percent": memory.percent,
                    "swap_total": swap.total,
                    "swap_used": swap.used,
                    "swap_percent": swap.percent
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": disk.percent,
                    "read_bytes": disk_io.read_bytes if disk_io else 0,
                    "write_bytes": disk_io.write_bytes if disk_io else 0
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                },
                "processes": {
                    "count": len(processes),
                    "details": processes[:10]  # Top 10 processes
                }
            }

            return stats

        except Exception as e:
            logger.error(f"Stats collection error: {e}")
            return {}

    def check_resource_alerts(self, stats: Dict) -> List[Dict]:
        """🚨 Check for resource alerts and thresholds"""
        alerts = []

        try:
            # CPU alerts
            cpu_usage = stats["cpu"]["usage_percent"]
            if cpu_usage >= self.resource_limits["cpu_critical"]:
                alerts.append({
                    "type": "CRITICAL",
                    "resource": "CPU",
                    "current": cpu_usage,
                    "threshold": self.resource_limits["cpu_critical"],
                    "message": f"🔥 CRITICAL CPU USAGE: {cpu_usage:.1f}%"
                })
            elif cpu_usage >= self.resource_limits["cpu_warning"]:
                alerts.append({
                    "type": "WARNING",
                    "resource": "CPU",
                    "current": cpu_usage,
                    "threshold": self.resource_limits["cpu_warning"],
                    "message": f"⚠️ High CPU usage: {cpu_usage:.1f}%"
                })

            # Memory alerts
            memory_usage = stats["memory"]["percent"]
            if memory_usage >= self.resource_limits["memory_critical"]:
                alerts.append({
                    "type": "CRITICAL",
                    "resource": "MEMORY",
                    "current": memory_usage,
                    "threshold": self.resource_limits["memory_critical"],
                    "message": f"🔥 CRITICAL MEMORY USAGE: {memory_usage:.1f}%"
                })
            elif memory_usage >= self.resource_limits["memory_warning"]:
                alerts.append({
                    "type": "WARNING",
                    "resource": "MEMORY",
                    "current": memory_usage,
                    "threshold": self.resource_limits["memory_warning"],
                    "message": f"⚠️ High memory usage: {memory_usage:.1f}%"
                })

            # Disk alerts
            disk_usage = stats["disk"]["percent"]
            if disk_usage >= self.resource_limits["disk_critical"]:
                alerts.append({
                    "type": "CRITICAL",
                    "resource": "DISK",
                    "current": disk_usage,
                    "threshold": self.resource_limits["disk_critical"],
                    "message": f"🔥 CRITICAL DISK USAGE: {disk_usage:.1f}%"
                })
            elif disk_usage >= self.resource_limits["disk_warning"]:
                alerts.append({
                    "type": "WARNING",
                    "resource": "DISK",
                    "current": disk_usage,
                    "threshold": self.resource_limits["disk_warning"],
                    "message": f"⚠️ High disk usage: {disk_usage:.1f}%"
                })

            # System load alerts
            load_avg = stats["cpu"]["load_avg"][0]  # 1-minute load average
            if load_avg >= self.resource_limits["load_critical"]:
                alerts.append({
                    "type": "CRITICAL",
                    "resource": "LOAD",
                    "current": load_avg,
                    "threshold": self.resource_limits["load_critical"],
                    "message": f"🔥 CRITICAL SYSTEM LOAD: {load_avg:.2f}"
                })
            elif load_avg >= self.resource_limits["load_warning"]:
                alerts.append({
                    "type": "WARNING",
                    "resource": "LOAD",
                    "current": load_avg,
                    "threshold": self.resource_limits["load_warning"],
                    "message": f"⚠️ High system load: {load_avg:.2f}"
                })

            return alerts

        except Exception as e:
            logger.error(f"Alert check error: {e}")
            return []

    def auto_optimize_system(self, alerts: List[Dict]):
        """⚡ Auto-optimize system based on alerts"""
        if not self.auto_optimize:
            return

        try:
            for alert in alerts:
                if alert["type"] == "CRITICAL":
                    self._handle_critical_alert(alert)
                elif alert["type"] == "WARNING":
                    self._handle_warning_alert(alert)

        except Exception as e:
            logger.error(f"Auto-optimization error: {e}")

    def _handle_critical_alert(self, alert: Dict):
        """🚨 Handle critical resource alerts"""
        resource = alert["resource"]

        if resource == "CPU":
            self._optimize_cpu_usage()
        elif resource == "MEMORY":
            self._optimize_memory_usage()
        elif resource == "DISK":
            self._optimize_disk_usage()
        elif resource == "LOAD":
            self._optimize_system_load()

    def _handle_warning_alert(self, alert: Dict):
        """⚠️ Handle warning alerts"""
        logger.warning(f"⚠️ {alert['message']}")
        # Log warning but don't take aggressive action yet

    def _optimize_cpu_usage(self):
        """⚡ Optimize CPU usage"""
        logger.info("⚡ Optimizing CPU usage...")

        try:
            # Find high CPU processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 50:  # High CPU usage
                        processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Log high CPU processes
            for proc in processes[:5]:  # Top 5
                logger.info(f"🔥 High CPU process: {proc['name']} (PID: {proc['pid']}) - {proc['cpu_percent']:.1f}%")

            # Could implement process throttling here

        except Exception as e:
            logger.error(f"CPU optimization error: {e}")

    def _optimize_memory_usage(self):
        """🧠 Optimize memory usage"""
        logger.info("🧠 Optimizing memory usage...")

        try:
            # Clear system caches
            subprocess.run(['sync'], check=False)
            subprocess.run(['echo', '1', '>', '/proc/sys/vm/drop_caches'],
                          shell=True, check=False)

            # Find high memory processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    if proc.info['memory_percent'] > 10:  # High memory usage
                        processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Log high memory processes
            for proc in processes[:5]:  # Top 5
                logger.info(f"🧠 High memory process: {proc['name']} (PID: {proc['pid']}) - {proc['memory_percent']:.1f}%")

        except Exception as e:
            logger.error(f"Memory optimization error: {e}")

    def _optimize_disk_usage(self):
        """💾 Optimize disk usage"""
        logger.info("💾 Optimizing disk usage...")

        try:
            # Clean temporary files
            temp_dirs = ['/tmp', '/var/tmp', f'{self.base_path}/logs']

            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    # Clean files older than 1 day
                    subprocess.run([
                        'find', temp_dir, '-type', 'f', '-mtime', '+1', '-delete'
                    ], check=False)

            # Clean old log files
            log_files = [
                f'{self.base_path}/*.log',
                f'{self.base_path}/logs/*.log'
            ]

            for log_pattern in log_files:
                subprocess.run([
                    'find', os.path.dirname(log_pattern), '-name',
                    os.path.basename(log_pattern), '-size', '+100M', '-delete'
                ], check=False)

        except Exception as e:
            logger.error(f"Disk optimization error: {e}")

    def _optimize_system_load(self):
        """🎯 Optimize system load"""
        logger.info("🎯 Optimizing system load...")

        try:
            # Nice down heavy processes
            for proc in psutil.process_iter(['pid', 'name', 'nice']):
                try:
                    if proc.info['name'] in ['python3', 'node'] and proc.info['nice'] < 10:
                        # Increase niceness (lower priority)
                        subprocess.run(['renice', '10', str(proc.info['pid'])],
                                      check=False)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        except Exception as e:
            logger.error(f"Load optimization error: {e}")

    def log_metrics(self, stats: Dict):
        """📊 Log metrics to database"""
        try:
            with sqlite3.connect(self.guardian_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO server_metrics
                    (timestamp, cpu_usage, memory_usage, disk_usage, system_load,
                     processes_count, network_io, disk_io)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    stats["timestamp"],
                    stats["cpu"]["usage_percent"],
                    stats["memory"]["percent"],
                    stats["disk"]["percent"],
                    stats["cpu"]["load_avg"][0],
                    stats["processes"]["count"],
                    json.dumps({
                        "bytes_sent": stats["network"]["bytes_sent"],
                        "bytes_recv": stats["network"]["bytes_recv"]
                    }),
                    json.dumps({
                        "read_bytes": stats["disk"]["read_bytes"],
                        "write_bytes": stats["disk"]["write_bytes"]
                    })
                ))
                conn.commit()

        except Exception as e:
            logger.error(f"Metrics logging error: {e}")

    def log_alerts(self, alerts: List[Dict]):
        """🚨 Log alerts to database"""
        try:
            with sqlite3.connect(self.guardian_db) as conn:
                cursor = conn.cursor()
                for alert in alerts:
                    cursor.execute("""
                        INSERT INTO resource_alerts
                        (timestamp, alert_type, resource_type, current_value,
                         threshold, action_taken)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        time.time(),
                        alert["type"],
                        alert["resource"],
                        alert["current"],
                        alert["threshold"],
                        "AUTO_OPTIMIZE" if self.auto_optimize else "LOGGED_ONLY"
                    ))
                conn.commit()

        except Exception as e:
            logger.error(f"Alert logging error: {e}")

    def get_guardian_dashboard(self) -> Dict:
        """📊 Get guardian dashboard data"""
        stats = self.get_system_stats()
        alerts = self.check_resource_alerts(stats)

        return {
            "server_status": "SUPREME" if not alerts else "MONITORING",
            "current_stats": stats,
            "active_alerts": alerts,
            "resource_limits": self.resource_limits,
            "auto_optimize": self.auto_optimize,
            "monitoring_active": self.monitoring_active,
            "guardian_uptime": time.time() - getattr(self, 'start_time', time.time())
        }

    async def start_monitoring(self):
        """🛡️ Start continuous server monitoring"""
        self.monitoring_active = True
        self.start_time = time.time()

        logger.info("🛡️ SUPREME SERVER GUARDIAN MONITORING STARTED!")

        while self.monitoring_active:
            try:
                # Get system stats
                stats = self.get_system_stats()

                # Check for alerts
                alerts = self.check_resource_alerts(stats)

                # Display current status
                self._display_status(stats, alerts)

                # Auto-optimize if needed
                if alerts:
                    self.auto_optimize_system(alerts)
                    self.log_alerts(alerts)

                # Log metrics
                self.log_metrics(stats)

                # Wait before next check
                await asyncio.sleep(10)  # Check every 10 seconds

            except KeyboardInterrupt:
                logger.info("🛡️ Server Guardian shutting down...")
                break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(30)

    def _display_status(self, stats: Dict, alerts: List[Dict]):
        """📺 Display current system status"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n🛡️ SUPREME SERVER GUARDIAN STATUS - {timestamp}")
        print("=" * 60)

        # Resource status
        cpu = stats["cpu"]["usage_percent"]
        memory = stats["memory"]["percent"]
        disk = stats["disk"]["percent"]
        load = stats["cpu"]["load_avg"][0]

        cpu_status = "🔥" if cpu > 90 else "⚠️" if cpu > 75 else "✅"
        memory_status = "🔥" if memory > 95 else "⚠️" if memory > 80 else "✅"
        disk_status = "🔥" if disk > 95 else "⚠️" if disk > 85 else "✅"
        load_status = "🔥" if load > 8 else "⚠️" if load > 4 else "✅"

        print(f"{cpu_status} CPU Usage: {cpu:.1f}%")
        print(f"{memory_status} Memory Usage: {memory:.1f}%")
        print(f"{disk_status} Disk Usage: {disk:.1f}%")
        print(f"{load_status} System Load: {load:.2f}")
        print(f"📊 Processes: {stats['processes']['count']}")

        # Alerts
        if alerts:
            print(f"\n🚨 ACTIVE ALERTS ({len(alerts)}):")
            for alert in alerts:
                print(f"   {alert['message']}")
        else:
            print(f"\n✅ ALL SYSTEMS OPTIMAL!")

        print("=" * 60)

    def stop_monitoring(self):
        """⏹️ Stop server monitoring"""
        self.monitoring_active = False
        logger.info("⏹️ Server Guardian monitoring stopped!")


async def main():
    """🚀 Launch Supreme Server Guardian"""
    print("🛡️💜 LAUNCHING BROSKI SUPREME SERVER GUARDIAN! 💜🛡️")

    guardian = BroskiSupremeServerGuardian()

    try:
        await guardian.start_monitoring()
    except KeyboardInterrupt:
        guardian.stop_monitoring()
        print("🛡️ Guardian shutdown complete!")


if __name__ == "__main__":
    asyncio.run(main())