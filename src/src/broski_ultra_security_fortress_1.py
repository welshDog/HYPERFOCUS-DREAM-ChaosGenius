#!/usr/bin/env python3
"""
🔒🛡️ BROSKI ULTRA SECURITY FORTRESS - LEGENDARY THREAT DETECTION 🛡️🔒
The most legendary security monitoring and auto-response system ever created!
Auto-detects threats, blocks attackers, and protects your legendary empire!
"""

import asyncio
import hashlib
import ipaddress
import json
import logging
import os
import socket
import sqlite3
import subprocess
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import psutil

# Import Guardian Zero for epic integration
try:
    from guardian_zero_command import guardian_zero

    GUARDIAN_ZERO_AVAILABLE = True
except ImportError:
    GUARDIAN_ZERO_AVAILABLE = False
    print("⚠️ Guardian Zero not available, running in standalone fortress mode")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BROskiSecurityFortress:
    """🔒🛡️ The most legendary security fortress that protects your digital empire"""

    def __init__(self):
        self.motto = "NO THREAT SHALL PASS. THE FORTRESS IS IMPENETRABLE."
        self.broski_dollars_earned = 0
        self.threats_detected = 0
        self.threats_blocked = 0
        self.legendary_status = "FORTRESS MODE"

        # Threat tracking
        self.active_threats = {}
        self.blocked_ips = set()
        self.suspicious_activities = deque(maxlen=1000)
        self.failed_login_attempts = defaultdict(int)
        self.port_scan_attempts = defaultdict(list)
        self.file_integrity_hashes = {}

        # Security settings
        self.max_failed_logins = 5
        self.port_scan_threshold = 10  # connections per minute
        self.auto_block_duration = 3600  # 1 hour
        self.critical_files = [
            "guardian_zero_command.py",
            "dashboard_api.py",
            "broski_token_config.json",
            "chaosgenius.db",
            "guardian_zero.db",
            "broski_ultra_security_fortress.py",
        ]

        # Monitoring flags
        self.monitoring_active = False
        self.fortress_initialized = False

        # Initialize security database
        self.init_security_database()

        # Calculate initial file hashes
        self.update_file_integrity_baseline()

    def init_security_database(self):
        """🗄️ Initialize security monitoring database"""
        try:
            self.db_path = "broski_security_fortress.db"
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Threats table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS threats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    threat_type TEXT,
                    source_ip TEXT,
                    severity TEXT,
                    description TEXT,
                    action_taken TEXT,
                    broski_dollars_awarded INTEGER
                )
            """
            )

            # Blocked IPs table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS blocked_ips (
                    ip TEXT PRIMARY KEY,
                    blocked_at TEXT,
                    reason TEXT,
                    block_duration INTEGER,
                    auto_unblock_at TEXT
                )
            """
            )

            # Security events table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_type TEXT,
                    details TEXT,
                    severity TEXT
                )
            """
            )

            conn.commit()
            conn.close()
            logger.info("🗄️ Security fortress database initialized")

        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")

    def update_file_integrity_baseline(self):
        """🔍 Update file integrity baseline hashes"""
        try:
            for file_path in self.critical_files:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                        self.file_integrity_hashes[file_path] = file_hash

            logger.info(
                f"🔍 File integrity baseline updated for {len(self.file_integrity_hashes)} critical files"
            )

        except Exception as e:
            logger.error(f"❌ File integrity baseline update failed: {e}")

    async def start_fortress_monitoring(self):
        """🛡️ Start the legendary security fortress monitoring"""
        logger.info("🛡️ BROSKI SECURITY FORTRESS ACTIVATING...")
        logger.info(f"Motto: {self.motto}")

        self.monitoring_active = True
        self.fortress_initialized = True

        # Start all monitoring tasks
        monitoring_tasks = [
            self.monitor_network_connections(),
            self.monitor_file_integrity(),
            self.monitor_system_processes(),
            self.monitor_failed_logins(),
            self.auto_unblock_expired_ips(),
            self.generate_security_reports(),
        ]

        logger.info("🚀 All security monitoring systems activated!")

        try:
            await asyncio.gather(*monitoring_tasks)
        except KeyboardInterrupt:
            logger.info("🛑 Fortress shutdown initiated by user")
            await self.fortress_shutdown()

    async def monitor_network_connections(self):
        """🌐 Monitor network connections for suspicious activity"""
        logger.info("🌐 Network connection monitoring activated")

        while self.monitoring_active:
            try:
                connections = psutil.net_connections(kind="inet")
                current_time = datetime.now()

                # Track connections per IP
                ip_connections = defaultdict(int)

                for conn in connections:
                    if conn.raddr:  # Remote address exists
                        remote_ip = conn.raddr.ip

                        # Skip localhost and private IPs for port scan detection
                        if not self.is_local_ip(remote_ip):
                            ip_connections[remote_ip] += 1

                            # Track for port scan detection
                            if remote_ip not in self.port_scan_attempts:
                                self.port_scan_attempts[remote_ip] = []

                            self.port_scan_attempts[remote_ip].append(current_time)

                            # Remove old entries (older than 1 minute)
                            self.port_scan_attempts[remote_ip] = [
                                t
                                for t in self.port_scan_attempts[remote_ip]
                                if current_time - t < timedelta(minutes=1)
                            ]

                # Check for port scanning
                for ip, timestamps in self.port_scan_attempts.items():
                    if (
                        len(timestamps) > self.port_scan_threshold
                        and ip not in self.blocked_ips
                    ):
                        await self.handle_threat(
                            "port_scan",
                            ip,
                            f"Port scan detected: {len(timestamps)} connections in 1 minute",
                        )

                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                logger.error(f"❌ Network monitoring error: {e}")
                await asyncio.sleep(30)

    async def monitor_file_integrity(self):
        """📁 Monitor critical files for unauthorized changes"""
        logger.info("📁 File integrity monitoring activated")

        while self.monitoring_active:
            try:
                for file_path, original_hash in self.file_integrity_hashes.items():
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            current_hash = hashlib.sha256(f.read()).hexdigest()

                        if current_hash != original_hash:
                            await self.handle_threat(
                                "file_modification",
                                "localhost",
                                f"Critical file modified: {file_path}",
                            )
                            # Update hash after detection
                            self.file_integrity_hashes[file_path] = current_hash

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"❌ File integrity monitoring error: {e}")
                await asyncio.sleep(60)

    async def monitor_system_processes(self):
        """⚙️ Monitor system processes for suspicious activity"""
        logger.info("⚙️ Process monitoring activated")

        known_processes = set()

        while self.monitoring_active:
            try:
                current_processes = set()

                for proc in psutil.process_iter(["pid", "name", "cmdline", "username"]):
                    try:
                        proc_info = proc.info
                        proc_signature = f"{proc_info['name']}:{' '.join(proc_info['cmdline'] or [])}"
                        current_processes.add(proc_signature)

                        # Check for suspicious process names
                        suspicious_names = ["nc", "ncat", "telnet", "wget", "curl"]
                        if any(
                            suspicious in proc_info["name"].lower()
                            for suspicious in suspicious_names
                        ):
                            if proc_signature not in known_processes:
                                await self.handle_threat(
                                    "suspicious_process",
                                    "localhost",
                                    f"Suspicious process detected: {proc_info['name']} (PID: {proc_info['pid']})",
                                )

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                # Update known processes
                known_processes.update(current_processes)

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"❌ Process monitoring error: {e}")
                await asyncio.sleep(60)

    async def monitor_failed_logins(self):
        """🔐 Monitor for failed login attempts"""
        logger.info("🔐 Login attempt monitoring activated")

        while self.monitoring_active:
            try:
                # Check for SSH brute force attempts
                ssh_connections = [
                    conn
                    for conn in psutil.net_connections()
                    if conn.laddr
                    and conn.laddr.port == 22
                    and conn.status == "ESTABLISHED"
                ]

                for conn in ssh_connections:
                    if conn.raddr:
                        remote_ip = conn.raddr.ip
                        if not self.is_local_ip(remote_ip):
                            self.failed_login_attempts[remote_ip] += 1

                            if (
                                self.failed_login_attempts[remote_ip]
                                > self.max_failed_logins
                            ):
                                await self.handle_threat(
                                    "brute_force",
                                    remote_ip,
                                    f"Brute force attack detected: {self.failed_login_attempts[remote_ip]} attempts",
                                )

                await asyncio.sleep(20)  # Check every 20 seconds

            except Exception as e:
                logger.error(f"❌ Login monitoring error: {e}")
                await asyncio.sleep(60)

    async def handle_threat(self, threat_type: str, source_ip: str, description: str):
        """🚨 Handle detected threats with appropriate response"""
        try:
            severity = self.determine_threat_severity(threat_type)
            timestamp = datetime.now()

            logger.warning(
                f"🚨 THREAT DETECTED: {threat_type} from {source_ip} - {description}"
            )

            # Record threat
            self.threats_detected += 1
            threat_id = f"{threat_type}_{source_ip}_{int(timestamp.timestamp())}"

            self.active_threats[threat_id] = {
                "type": threat_type,
                "source": source_ip,
                "description": description,
                "severity": severity,
                "detected_at": timestamp,
                "action_taken": None,
            }

            # Determine and execute response
            action_taken = await self.execute_threat_response(
                threat_type, source_ip, severity
            )

            self.active_threats[threat_id]["action_taken"] = action_taken

            # Award BROski$ based on threat severity
            broski_reward = self.calculate_broski_reward(severity)
            self.broski_dollars_earned += broski_reward

            # Log to database
            self.log_threat_to_database(
                threat_type,
                source_ip,
                severity,
                description,
                action_taken,
                broski_reward,
            )

            # Send alert to Guardian Zero
            if GUARDIAN_ZERO_AVAILABLE:
                guardian_zero.send_alert(
                    "SECURITY-FORTRESS",
                    f"threat_{severity.lower()}",
                    f"🚨 {threat_type.upper()}: {description} - Action: {action_taken}",
                    severity.lower(),
                )
                guardian_zero.award_xp(
                    broski_reward, f"Security threat detection: {threat_type}"
                )

            logger.info(f"💰 Security action rewarded: +{broski_reward} BROski$")

        except Exception as e:
            logger.error(f"❌ Threat handling error: {e}")

    async def execute_threat_response(
        self, threat_type: str, source_ip: str, severity: str
    ) -> str:
        """⚔️ Execute appropriate response to threat"""
        try:
            if severity in ["HIGH", "CRITICAL"] and source_ip != "localhost":
                # Auto-block IP for severe threats
                await self.block_ip(source_ip, threat_type)
                self.threats_blocked += 1
                return f"IP_BLOCKED"

            elif threat_type == "file_modification":
                # Alert only for file modifications (don't block localhost)
                return "ALERT_SENT"

            elif threat_type == "suspicious_process":
                # Alert for suspicious processes
                return "PROCESS_MONITORED"

            else:
                # Default: Monitor and alert
                return "MONITORING_INCREASED"

        except Exception as e:
            logger.error(f"❌ Threat response error: {e}")
            return "RESPONSE_FAILED"

    async def block_ip(self, ip: str, reason: str):
        """🚫 Block an IP address"""
        try:
            if ip in self.blocked_ips:
                return  # Already blocked

            # Add to blocked set
            self.blocked_ips.add(ip)

            # Log the block (iptables may not be available in all environments)
            logger.info(f"🚫 IP {ip} blocked for: {reason}")

            # Log to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            unblock_time = datetime.now() + timedelta(seconds=self.auto_block_duration)

            cursor.execute(
                """
                INSERT OR REPLACE INTO blocked_ips
                (ip, blocked_at, reason, block_duration, auto_unblock_at)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    ip,
                    datetime.now().isoformat(),
                    reason,
                    self.auto_block_duration,
                    unblock_time.isoformat(),
                ),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"❌ IP blocking error: {e}")

    async def auto_unblock_expired_ips(self):
        """🔓 Automatically unblock IPs after expiration"""
        logger.info("🔓 Auto-unblock monitoring activated")

        while self.monitoring_active:
            try:
                current_time = datetime.now()

                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Find expired blocks
                cursor.execute(
                    """
                    SELECT ip, auto_unblock_at FROM blocked_ips
                    WHERE auto_unblock_at <= ?
                """,
                    (current_time.isoformat(),),
                )

                expired_blocks = cursor.fetchall()

                for ip, unblock_time in expired_blocks:
                    await self.unblock_ip(ip)

                    # Remove from database
                    cursor.execute("DELETE FROM blocked_ips WHERE ip = ?", (ip,))

                conn.commit()
                conn.close()

                await asyncio.sleep(300)  # Check every 5 minutes

            except Exception as e:
                logger.error(f"❌ Auto-unblock error: {e}")
                await asyncio.sleep(300)

    async def unblock_ip(self, ip: str):
        """🔓 Unblock an IP address"""
        try:
            if ip not in self.blocked_ips:
                return

            # Remove from blocked set
            self.blocked_ips.discard(ip)
            logger.info(f"🔓 IP {ip} unblocked (expired)")

        except Exception as e:
            logger.error(f"❌ IP unblocking error: {e}")

    def determine_threat_severity(self, threat_type: str) -> str:
        """📊 Determine threat severity level"""
        severity_map = {
            "brute_force": "HIGH",
            "port_scan": "MEDIUM",
            "file_modification": "CRITICAL",
            "suspicious_process": "MEDIUM",
            "malware_detection": "CRITICAL",
            "privilege_escalation": "CRITICAL",
        }

        return severity_map.get(threat_type, "LOW")

    def calculate_broski_reward(self, severity: str) -> int:
        """💰 Calculate BROski$ reward based on threat severity"""
        reward_map = {"LOW": 5, "MEDIUM": 15, "HIGH": 25, "CRITICAL": 50}

        return reward_map.get(severity, 5)

    def is_local_ip(self, ip: str) -> bool:
        """🔍 Check if IP is local/private"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_loopback or ip_obj.is_private
        except:
            return False

    def log_threat_to_database(
        self,
        threat_type: str,
        source_ip: str,
        severity: str,
        description: str,
        action_taken: str,
        broski_reward: int,
    ):
        """🗄️ Log threat to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO threats
                (timestamp, threat_type, source_ip, severity, description, action_taken, broski_dollars_awarded)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    threat_type,
                    source_ip,
                    severity,
                    description,
                    action_taken,
                    broski_reward,
                ),
            )

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"❌ Database logging error: {e}")

    async def generate_security_reports(self):
        """📊 Generate periodic security reports"""
        logger.info("📊 Security reporting activated")

        while self.monitoring_active:
            try:
                await asyncio.sleep(3600)  # Generate report every hour

                report = self.generate_hourly_security_report()

                # Save report
                report_file = (
                    f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                with open(report_file, "w") as f:
                    json.dump(report, f, indent=2, default=str)

                logger.info(f"📊 Security report generated: {report_file}")

                # Award BROski$ for report generation
                self.broski_dollars_earned += 10

                if GUARDIAN_ZERO_AVAILABLE:
                    guardian_zero.send_alert(
                        "SECURITY-FORTRESS",
                        "security_report",
                        f"📊 Hourly security report generated: {report['summary']['total_threats']} threats detected",
                        "info",
                    )

            except Exception as e:
                logger.error(f"❌ Report generation error: {e}")
                await asyncio.sleep(3600)

    def generate_hourly_security_report(self) -> Dict[str, Any]:
        """📊 Generate comprehensive security report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get threats from last hour
            one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()

            cursor.execute(
                """
                SELECT threat_type, severity, COUNT(*) as count
                FROM threats
                WHERE timestamp >= ?
                GROUP BY threat_type, severity
            """,
                (one_hour_ago,),
            )

            threat_stats = cursor.fetchall()

            # Get currently blocked IPs
            cursor.execute("SELECT COUNT(*) FROM blocked_ips")
            blocked_count = cursor.fetchone()[0]

            conn.close()

            return {
                "timestamp": datetime.now().isoformat(),
                "period": "1_hour",
                "summary": {
                    "total_threats": self.threats_detected,
                    "threats_blocked": self.threats_blocked,
                    "broski_dollars_earned": self.broski_dollars_earned,
                    "currently_blocked_ips": blocked_count,
                    "fortress_status": self.legendary_status,
                },
                "threat_breakdown": [
                    {"type": t[0], "severity": t[1], "count": t[2]}
                    for t in threat_stats
                ],
                "fortress_motto": self.motto,
            }

        except Exception as e:
            logger.error(f"❌ Report generation error: {e}")
            return {"error": str(e)}

    def get_fortress_status(self) -> Dict[str, Any]:
        """🛡️ Get complete fortress status"""
        return {
            "fortress_online": self.fortress_initialized,
            "monitoring_active": self.monitoring_active,
            "motto": self.motto,
            "legendary_status": self.legendary_status,
            "broski_dollars_earned": self.broski_dollars_earned,
            "security_stats": {
                "threats_detected": self.threats_detected,
                "threats_blocked": self.threats_blocked,
                "active_threats": len(self.active_threats),
                "blocked_ips": len(self.blocked_ips),
                "critical_files_monitored": len(self.file_integrity_hashes),
            },
            "active_threats": [
                {
                    "id": threat_id,
                    "type": threat["type"],
                    "source": threat["source"],
                    "severity": threat["severity"],
                    "detected_at": threat["detected_at"].isoformat(),
                    "action_taken": threat["action_taken"],
                }
                for threat_id, threat in self.active_threats.items()
            ],
            "blocked_ips": list(self.blocked_ips),
            "legendary_rating": (
                "ULTRA LEGENDARY" if self.threats_blocked > 10 else "LEGENDARY"
            ),
        }

    async def emergency_lockdown(self):
        """🚨 Emergency lockdown protocol"""
        logger.warning("🚨 EMERGENCY LOCKDOWN PROTOCOL ACTIVATED!")

        try:
            self.legendary_status = "LOCKDOWN MODE"

            # Award massive BROski$ for emergency response
            self.broski_dollars_earned += 200

            if GUARDIAN_ZERO_AVAILABLE:
                guardian_zero.send_alert(
                    "SECURITY-FORTRESS",
                    "emergency_lockdown",
                    "🚨 EMERGENCY LOCKDOWN ACTIVATED - All external access monitored!",
                    "critical",
                )
                guardian_zero.award_xp(200, "Emergency lockdown protocol activation")

            return {"status": "lockdown_activated", "broski_dollars_awarded": 200}

        except Exception as e:
            logger.error(f"❌ Emergency lockdown error: {e}")
            return {"status": "lockdown_failed", "error": str(e)}

    async def fortress_shutdown(self):
        """🛑 Gracefully shutdown the fortress"""
        logger.info("🛑 Security fortress shutting down gracefully...")
        self.monitoring_active = False

        # Generate final report
        final_report = self.get_fortress_status()
        with open(
            f"fortress_final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "w",
        ) as f:
            json.dump(final_report, f, indent=2, default=str)

        logger.info("🛡️ Security fortress shutdown complete")


# Global security fortress instance
security_fortress = BROskiSecurityFortress()


async def main():
    """🛡️ Main security fortress monitoring loop"""
    logger.info("🔒🛡️ BROSKI ULTRA SECURITY FORTRESS STARTING UP 🛡️🔒")
    logger.info(f"Motto: {security_fortress.motto}")

    await security_fortress.start_fortress_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
