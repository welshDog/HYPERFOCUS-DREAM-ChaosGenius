#!/usr/bin/env python3
"""
🔧🛡️ BROSKI SECURITY TUNER - OPTIMIZATION MASTER 🛡️🔧
🌟 Reduces False Positives & Fine-Tunes Your Security Fortress 🌟
👑 By Command of Chief Lyndz - Perfect Balance Protection! 👑
"""

import argparse
import json
import logging
import os
import sqlite3
import sys
from datetime import datetime
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BroskiSecurityTuner:
    """🔧 Ultimate Security Optimization Engine"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.security_db = f"{self.base_path}/broski_security_fortress.db"
        self.config_file = f"{self.base_path}/broski_security_config.json"

        # Default security thresholds
        self.default_config = {
            "whitelist_ips": ["127.0.0.1", "::1", "localhost", "0.0.0.0"],
            "whitelist_processes": [
                "python3",
                "python",
                "node",
                "npm",
                "git",
                "ssh",
                "curl",
                "wget",
            ],
            "thresholds": {
                "port_scan_threshold": 20,  # Reduced from default
                "max_failed_logins": 10,  # Increased from 5
                "suspicious_connection_threshold": 15,
                "file_change_cooldown": 300,  # 5 minutes
            },
            "noise_reduction": {
                "ignore_local_connections": True,
                "ignore_common_ports": [22, 80, 443, 8080, 3000, 5000],
                "ignore_development_activity": True,
                "rate_limit_alerts": True,
            },
            "stealth_mode": {
                "enabled": False,
                "log_only": False,
                "minimal_alerts": False,
            },
        }

        print("🔧💜 BROSKI SECURITY TUNER INITIALIZED! 💜🔧")

    def load_current_config(self) -> Dict:
        """📥 Load current security configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                logger.info("📥 Loaded existing security configuration")
                return config
            else:
                logger.info("📝 Creating new security configuration")
                return self.default_config.copy()
        except Exception as e:
            logger.error(f"❌ Config loading error: {e}")
            return self.default_config.copy()

    def save_config(self, config: Dict):
        """💾 Save security configuration"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
            logger.info("💾 Security configuration saved!")
        except Exception as e:
            logger.error(f"❌ Config save error: {e}")

    def whitelist_local_ips(self):
        """🏠 Add local development IPs to whitelist"""
        config = self.load_current_config()

        # Common development IPs
        dev_ips = [
            "127.0.0.1",
            "::1",
            "localhost",
            "0.0.0.0",
            "192.168.*",  # Local network
            "10.*",  # Private network
            "172.16.*",  # Private network
        ]

        for ip in dev_ips:
            if ip not in config["whitelist_ips"]:
                config["whitelist_ips"].append(ip)

        self.save_config(config)
        print(f"🏠 Whitelisted {len(dev_ips)} local/development IPs")

    def reduce_noise(self):
        """🔇 Reduce false positive noise"""
        config = self.load_current_config()

        # Optimize thresholds
        config["thresholds"]["port_scan_threshold"] = 25
        config["thresholds"]["max_failed_logins"] = 15
        config["thresholds"]["suspicious_connection_threshold"] = 20

        # Enable noise reduction
        config["noise_reduction"]["ignore_local_connections"] = True
        config["noise_reduction"]["ignore_development_activity"] = True
        config["noise_reduction"]["rate_limit_alerts"] = True

        # Add common development processes
        dev_processes = [
            "python3",
            "python",
            "node",
            "npm",
            "yarn",
            "git",
            "curl",
            "wget",
            "ssh",
            "scp",
            "rsync",
            "docker",
            "code",
            "vim",
            "nano",
            "tail",
            "grep",
            "find",
        ]

        for process in dev_processes:
            if process not in config["whitelist_processes"]:
                config["whitelist_processes"].append(process)

        self.save_config(config)
        print("🔇 Noise reduction optimizations applied!")

    def enable_stealth_mode(self):
        """👻 Enable stealth mode for covert operations"""
        config = self.load_current_config()

        config["stealth_mode"]["enabled"] = True
        config["stealth_mode"]["minimal_alerts"] = True
        config["noise_reduction"]["rate_limit_alerts"] = True

        # Increase thresholds for stealth
        config["thresholds"]["port_scan_threshold"] = 50
        config["thresholds"]["max_failed_logins"] = 25

        self.save_config(config)
        print("👻 Stealth mode enabled! Silent protection activated.")

    def performance_mode(self):
        """⚡ Optimize for performance over sensitivity"""
        config = self.load_current_config()

        # High-performance thresholds
        config["thresholds"]["port_scan_threshold"] = 35
        config["thresholds"]["max_failed_logins"] = 20
        config["thresholds"]["suspicious_connection_threshold"] = 30

        # Enable all noise reduction
        for key in config["noise_reduction"]:
            config["noise_reduction"][key] = True

        self.save_config(config)
        print("⚡ Performance mode activated! Optimized for speed.")

    def paranoid_mode(self):
        """🔥 Maximum security sensitivity"""
        config = self.load_current_config()

        # Ultra-sensitive thresholds
        config["thresholds"]["port_scan_threshold"] = 5
        config["thresholds"]["max_failed_logins"] = 3
        config["thresholds"]["suspicious_connection_threshold"] = 8

        # Disable noise reduction
        for key in config["noise_reduction"]:
            config["noise_reduction"][key] = False

        config["stealth_mode"]["enabled"] = False

        self.save_config(config)
        print("🔥 PARANOID MODE ACTIVATED! Maximum threat detection!")

    def analyze_current_threats(self):
        """📊 Analyze current threat patterns"""
        try:
            with sqlite3.connect(self.security_db) as conn:
                cursor = conn.cursor()

                # Get threat statistics
                stats = cursor.execute(
                    """
                    SELECT event_type, COUNT(*) as count, AVG(CAST(description AS INTEGER)) as avg_attempts
                    FROM security_events
                    WHERE timestamp > datetime('now', '-1 hour')
                    GROUP BY event_type
                    ORDER BY count DESC
                """
                ).fetchall()

                print("\n📊 THREAT ANALYSIS (Last Hour):")
                print("=" * 50)

                for event_type, count, avg_attempts in stats:
                    print(
                        f"🚨 {event_type}: {count} events (avg: {avg_attempts:.0f} attempts)"
                    )

                # Recommendations
                if stats:
                    most_common = stats[0]
                    if most_common[1] > 10:  # More than 10 events
                        print(f"\n💡 RECOMMENDATION:")
                        print(f"   High frequency of {most_common[0]} detected.")
                        print(
                            f"   Consider increasing thresholds or whitelisting if legitimate."
                        )

        except Exception as e:
            logger.error(f"❌ Analysis error: {e}")
            print("📊 No threat data available for analysis")

    def show_current_config(self):
        """📋 Display current security configuration"""
        config = self.load_current_config()

        print("\n📋 CURRENT SECURITY CONFIGURATION:")
        print("=" * 50)
        print(f"🏠 Whitelisted IPs: {len(config['whitelist_ips'])}")
        print(f"⚙️ Whitelisted Processes: {len(config['whitelist_processes'])}")
        print(f"🎯 Port Scan Threshold: {config['thresholds']['port_scan_threshold']}")
        print(f"🔐 Max Failed Logins: {config['thresholds']['max_failed_logins']}")
        print(
            f"👻 Stealth Mode: {'ENABLED' if config['stealth_mode']['enabled'] else 'DISABLED'}"
        )
        print(
            f"🔇 Noise Reduction: {'ENABLED' if config['noise_reduction']['ignore_local_connections'] else 'DISABLED'}"
        )

    def reset_to_defaults(self):
        """🔄 Reset configuration to defaults"""
        self.save_config(self.default_config.copy())
        print("🔄 Security configuration reset to defaults!")


def main():
    parser = argparse.ArgumentParser(description="🔧 BROski Security Tuner")
    parser.add_argument(
        "--whitelist-local",
        action="store_true",
        help="🏠 Whitelist local/development IPs",
    )
    parser.add_argument(
        "--reduce-noise", action="store_true", help="🔇 Reduce false positive noise"
    )
    parser.add_argument(
        "--stealth-mode", action="store_true", help="👻 Enable stealth mode"
    )
    parser.add_argument(
        "--performance-mode", action="store_true", help="⚡ Optimize for performance"
    )
    parser.add_argument(
        "--paranoid-mode", action="store_true", help="🔥 Maximum security sensitivity"
    )
    parser.add_argument(
        "--analyze", action="store_true", help="📊 Analyze current threats"
    )
    parser.add_argument(
        "--show-config", action="store_true", help="📋 Show current configuration"
    )
    parser.add_argument("--reset", action="store_true", help="🔄 Reset to defaults")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    tuner = BroskiSecurityTuner()

    if args.whitelist_local:
        tuner.whitelist_local_ips()

    if args.reduce_noise:
        tuner.reduce_noise()

    if args.stealth_mode:
        tuner.enable_stealth_mode()

    if args.performance_mode:
        tuner.performance_mode()

    if args.paranoid_mode:
        tuner.paranoid_mode()

    if args.analyze:
        tuner.analyze_current_threats()

    if args.show_config:
        tuner.show_current_config()

    if args.reset:
        tuner.reset_to_defaults()

    print("\n🎯 BROski Security Tuner complete! 🛡️")


if __name__ == "__main__":
    main()
