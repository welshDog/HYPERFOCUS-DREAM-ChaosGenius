#!/usr/bin/env python3
"""
🚨🔄 EMERGENCY RESTART CONTROLLER 🔄🚨
Prevents infinite restart loops and manages system stability
"""

import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmergencyRestartController:
    """🚨 Emergency restart loop prevention system"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.restart_tracking_dir = "/tmp/chaosgenius_restarts"
        self.max_restarts_per_hour = 5
        self.max_restarts_per_day = 20
        self.circuit_breaker_duration = 300  # 5 minutes

        # Create tracking directory
        Path(self.restart_tracking_dir).mkdir(exist_ok=True)

        logger.info("🚨 Emergency Restart Controller initialized")

    def get_restart_count(self, process_name: str) -> Dict:
        """Get restart count for a process"""
        tracking_file = f"{self.restart_tracking_dir}/{process_name}.json"

        if not Path(tracking_file).exists():
            return {"hourly": 0, "daily": 0, "last_restart": None}

        try:
            with open(tracking_file, 'r') as f:
                data = json.load(f)

            # Clean old entries
            now = datetime.now()
            if data.get("last_restart"):
                last_restart = datetime.fromisoformat(data["last_restart"])

                # Reset hourly count if more than 1 hour ago
                if now - last_restart > timedelta(hours=1):
                    data["hourly"] = 0

                # Reset daily count if more than 1 day ago
                if now - last_restart > timedelta(days=1):
                    data["daily"] = 0

            return data

        except Exception as e:
            logger.error(f"Error reading restart data for {process_name}: {e}")
            return {"hourly": 0, "daily": 0, "last_restart": None}

    def record_restart(self, process_name: str):
        """Record a restart attempt"""
        tracking_file = f"{self.restart_tracking_dir}/{process_name}.json"

        data = self.get_restart_count(process_name)
        data["hourly"] += 1
        data["daily"] += 1
        data["last_restart"] = datetime.now().isoformat()

        try:
            with open(tracking_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Error recording restart for {process_name}: {e}")

    def should_allow_restart(self, process_name: str) -> tuple[bool, str]:
        """Check if restart should be allowed"""
        data = self.get_restart_count(process_name)

        # Check circuit breaker
        circuit_breaker_file = f"{self.restart_tracking_dir}/{process_name}_circuit_breaker"
        if Path(circuit_breaker_file).exists():
            try:
                with open(circuit_breaker_file, 'r') as f:
                    breaker_time = datetime.fromisoformat(f.read().strip())

                if datetime.now() - breaker_time < timedelta(seconds=self.circuit_breaker_duration):
                    remaining = self.circuit_breaker_duration - (datetime.now() - breaker_time).seconds
                    return False, f"Circuit breaker active for {remaining}s"
                else:
                    # Remove expired circuit breaker
                    Path(circuit_breaker_file).unlink()
            except:
                Path(circuit_breaker_file).unlink()

        # Check restart limits
        if data["hourly"] >= self.max_restarts_per_hour:
            self._activate_circuit_breaker(process_name)
            return False, f"Hourly restart limit exceeded ({data['hourly']}/{self.max_restarts_per_hour})"

        if data["daily"] >= self.max_restarts_per_day:
            self._activate_circuit_breaker(process_name)
            return False, f"Daily restart limit exceeded ({data['daily']}/{self.max_restarts_per_day})"

        return True, "Restart allowed"

    def _activate_circuit_breaker(self, process_name: str):
        """Activate circuit breaker for a process"""
        circuit_breaker_file = f"{self.restart_tracking_dir}/{process_name}_circuit_breaker"
        with open(circuit_breaker_file, 'w') as f:
            f.write(datetime.now().isoformat())

        logger.warning(f"🚨 Circuit breaker activated for {process_name}")

    def kill_runaway_processes(self):
        """Kill processes that are restarting too frequently"""
        problem_processes = []

        for tracking_file in Path(self.restart_tracking_dir).glob("*.json"):
            process_name = tracking_file.stem
            data = self.get_restart_count(process_name)

            if data["hourly"] >= self.max_restarts_per_hour:
                problem_processes.append(process_name)

        for process_name in problem_processes:
            logger.warning(f"🔥 Killing runaway process: {process_name}")
            self._kill_process(process_name)

    def _kill_process(self, process_name: str):
        """Kill a specific process"""
        try:
            # Kill by process name
            subprocess.run(f"pkill -f {process_name}", shell=True, check=False)

            # Also kill by exact script name
            subprocess.run(f"pkill -f 'python.*{process_name}'", shell=True, check=False)

            logger.info(f"🔥 Killed process: {process_name}")

        except Exception as e:
            logger.error(f"Error killing process {process_name}: {e}")

    def get_system_status(self) -> Dict:
        """Get overall system restart status"""
        status = {
            "active_circuit_breakers": [],
            "high_restart_processes": [],
            "total_processes_tracked": 0,
            "timestamp": datetime.now().isoformat()
        }

        for tracking_file in Path(self.restart_tracking_dir).glob("*.json"):
            process_name = tracking_file.stem
            data = self.get_restart_count(process_name)
            status["total_processes_tracked"] += 1

            # Check for circuit breakers
            circuit_breaker_file = f"{self.restart_tracking_dir}/{process_name}_circuit_breaker"
            if Path(circuit_breaker_file).exists():
                status["active_circuit_breakers"].append(process_name)

            # Check for high restart count
            if data["hourly"] >= 3:  # Warning threshold
                status["high_restart_processes"].append({
                    "process": process_name,
                    "hourly_restarts": data["hourly"],
                    "daily_restarts": data["daily"]
                })

        return status

    def emergency_stop_all_restarts(self):
        """Emergency stop for all restart loops"""
        logger.warning("🚨 EMERGENCY STOP: Stopping all restart loops")

        # Activate circuit breakers for all tracked processes
        for tracking_file in Path(self.restart_tracking_dir).glob("*.json"):
            process_name = tracking_file.stem
            self._activate_circuit_breaker(process_name)

        # Kill common problematic processes
        problematic_processes = [
            "agent_army_mission_2_security_fortress.py",
            "broski_advanced_analytics.py",
            "dashboard_api.py",
            "broski_agent_evolution_engine.py"
        ]

        for process in problematic_processes:
            self._kill_process(process)

        logger.info("🛑 Emergency stop completed")

    def reset_all_counters(self):
        """Reset all restart counters"""
        logger.info("🔄 Resetting all restart counters")

        # Remove all tracking files
        for file in Path(self.restart_tracking_dir).glob("*"):
            file.unlink()

        logger.info("✅ All restart counters reset")

def main():
    """🚀 Main emergency controller"""
    controller = EmergencyRestartController()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "status":
            status = controller.get_system_status()
            print(json.dumps(status, indent=2))

        elif command == "emergency-stop":
            controller.emergency_stop_all_restarts()

        elif command == "reset":
            controller.reset_all_counters()

        elif command == "kill-runaway":
            controller.kill_runaway_processes()

        else:
            print("Usage: emergency_restart_controller.py [status|emergency-stop|reset|kill-runaway]")

    else:
        # Interactive mode
        print("🚨 Emergency Restart Controller")
        print("1. Check system status")
        print("2. Emergency stop all restarts")
        print("3. Reset all counters")
        print("4. Kill runaway processes")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            status = controller.get_system_status()
            print(json.dumps(status, indent=2))
        elif choice == "2":
            controller.emergency_stop_all_restarts()
        elif choice == "3":
            controller.reset_all_counters()
        elif choice == "4":
            controller.kill_runaway_processes()

if __name__ == "__main__":
    main()