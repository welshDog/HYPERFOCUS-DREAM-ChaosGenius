#!/usr/bin/env python3
"""
🧠💎 BROSKI MEMORY MONITOR & OPTIMIZER 💎🧠
Real-time Memory Monitoring & Automatic Optimization
Built for the ChaosGenius Empire
"""

import psutil
import time
import json
import logging
import threading
from datetime import datetime
import subprocess
import gc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BroskiMemoryMonitor:
    """🧠 Ultimate Memory Monitoring & Optimization System"""

    def __init__(self):
        self.monitoring_active = False
        self.alert_threshold = 80.0  # Alert at 80% memory usage
        self.critical_threshold = 90.0  # Critical at 90% memory usage
        self.optimization_threshold = 75.0  # Start optimization at 75%
        self.base_path = "/root/chaosgenius"
        self.log_file = f"{self.base_path}/memory_monitor.log"
        self.metrics_file = f"{self.base_path}/memory_metrics.json"

        print("🧠💜 BROSKI MEMORY MONITOR INITIALIZING! 💜🧠")

    def start_monitoring(self):
        """🔄 Start memory monitoring loop"""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        logger.info("🔄 Memory monitoring started")

    def _monitoring_loop(self):
        """🔄 Main memory monitoring loop"""
        while self.monitoring_active:
            try:
                mem_info = self.get_memory_status()
                usage_percent = mem_info['usage_percent']

                # Log current status
                self._log_memory_status(mem_info)

                # Check thresholds and take action
                if usage_percent >= self.critical_threshold:
                    self._handle_critical_memory()
                elif usage_percent >= self.alert_threshold:
                    self._handle_high_memory()
                elif usage_percent >= self.optimization_threshold:
                    self._optimize_memory()

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"❌ Memory monitoring error: {e}")
                time.sleep(60)

    def get_memory_status(self):
        """📊 Get detailed memory status"""
        mem = psutil.virtual_memory()

        return {
            'timestamp': datetime.now().isoformat(),
            'usage_percent': mem.percent,
            'available_gb': mem.available / (1024**3),
            'used_gb': mem.used / (1024**3),
            'total_gb': mem.total / (1024**3),
            'free_gb': mem.free / (1024**3),
            'buffers_gb': mem.buffers / (1024**3),
            'cached_gb': mem.cached / (1024**3)
        }

    def _optimize_memory(self):
        """⚡ Optimize memory usage"""
        logger.info("⚡ Starting memory optimization...")

        # Force garbage collection
        gc.collect()

        # Clear system caches (if possible)
        try:
            subprocess.run(['sync'], check=True)
            logger.info("✅ System sync completed")
        except:
            pass

        logger.info("✅ Memory optimization completed")

    def _handle_high_memory(self):
        """⚠️ Handle high memory usage"""
        logger.warning("⚠️ High memory usage detected!")

        # Get top memory processes
        top_processes = self._get_top_memory_processes()

        # Log the issue
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': 'HIGH',
            'memory_percent': psutil.virtual_memory().percent,
            'top_processes': top_processes
        }

        with open(f"{self.base_path}/memory_alerts.json", 'a') as f:
            f.write(json.dumps(alert) + '\n')

        # Optimize memory
        self._optimize_memory()

    def _handle_critical_memory(self):
        """🚨 Handle critical memory usage"""
        logger.error("🚨 CRITICAL memory usage detected!")

        # More aggressive optimization
        self._optimize_memory()

        # Log critical alert
        critical_alert = {
            'timestamp': datetime.now().isoformat(),
            'level': 'CRITICAL',
            'memory_percent': psutil.virtual_memory().percent,
            'action': 'emergency_optimization'
        }

        with open(f"{self.base_path}/memory_critical.json", 'a') as f:
            f.write(json.dumps(critical_alert) + '\n')

    def _get_top_memory_processes(self):
        """📊 Get top memory consuming processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by memory usage and return top 5
        return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]

    def _log_memory_status(self, mem_info):
        """📝 Log memory status to file"""
        with open(self.metrics_file, 'w') as f:
            json.dump(mem_info, f, indent=2)

    def get_memory_report(self):
        """📊 Generate memory report"""
        mem_info = self.get_memory_status()
        top_processes = self._get_top_memory_processes()

        print("\n🧠💎 MEMORY STATUS REPORT 💎🧠")
        print(f"📊 Usage: {mem_info['usage_percent']:.1f}%")
        print(f"💾 Used: {mem_info['used_gb']:.2f}GB")
        print(f"🆓 Available: {mem_info['available_gb']:.2f}GB")
        print(f"📦 Total: {mem_info['total_gb']:.2f}GB")

        print("\n🔝 TOP MEMORY PROCESSES:")
        for i, proc in enumerate(top_processes, 1):
            print(f"{i}. {proc['name']}: {proc['memory_percent']:.1f}%")

        return mem_info

    def stop_monitoring(self):
        """⏹️ Stop memory monitoring"""
        self.monitoring_active = False
        logger.info("⏹️ Memory monitoring stopped")

def main():
    """🎯 Main execution"""
    monitor = BroskiMemoryMonitor()
    monitor.start_monitoring()

    try:
        # Generate initial report
        monitor.get_memory_report()

        # Keep running
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        print("\n🔴 Shutting down memory monitor...")
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()