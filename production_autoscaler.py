#!/usr/bin/env python3
"""
ChaosGenius Auto-Scaling Controller
Automatically scales instances based on performance metrics
"""

import psutil
import subprocess
import time
import logging
from datetime import datetime

class AutoScaler:
    def __init__(self):
        self.min_instances = 1
        self.max_instances = 5
        self.current_instances = 1
        self.scale_up_threshold = 80  # CPU %
        self.scale_down_threshold = 30  # CPU %
        self.monitoring_interval = 30  # seconds

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('AutoScaler')

    def get_system_metrics(self):
        """Get current system performance metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'load_avg': psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
        }

    def scale_up(self):
        """Add new instance"""
        if self.current_instances < self.max_instances:
            port = 3000 + self.current_instances
            try:
                # Start new instance on different port
                subprocess.Popen([
                    'python', 'dashboard_api.py', '--port', str(port)
                ], cwd='/workspaces/HYPERFOCUS-DREAM-ChaosGenius')

                self.current_instances += 1
                self.logger.info(f"Scaled up: Started instance on port {port}")
                return True
            except Exception as e:
                self.logger.error(f"Scale up failed: {e}")
                return False
        return False

    def scale_down(self):
        """Remove instance"""
        if self.current_instances > self.min_instances:
            port = 3000 + self.current_instances - 1
            try:
                # Gracefully stop instance
                subprocess.run(['pkill', '-f', f'port.*{port}'])
                self.current_instances -= 1
                self.logger.info(f"Scaled down: Stopped instance on port {port}")
                return True
            except Exception as e:
                self.logger.error(f"Scale down failed: {e}")
                return False
        return False

    def monitor_and_scale(self):
        """Main monitoring and scaling loop"""
        self.logger.info("Auto-scaling system started")

        while True:
            try:
                metrics = self.get_system_metrics()
                cpu_usage = metrics['cpu_percent']

                self.logger.info(f"CPU: {cpu_usage}%, Instances: {self.current_instances}")

                if cpu_usage > self.scale_up_threshold:
                    self.logger.warning(f"High CPU usage detected: {cpu_usage}%")
                    if self.scale_up():
                        self.logger.info("Successfully scaled up")
                        time.sleep(60)  # Cool-down period

                elif cpu_usage < self.scale_down_threshold:
                    self.logger.info(f"Low CPU usage detected: {cpu_usage}%")
                    if self.scale_down():
                        self.logger.info("Successfully scaled down")
                        time.sleep(60)  # Cool-down period

                time.sleep(self.monitoring_interval)

            except KeyboardInterrupt:
                self.logger.info("Auto-scaling system stopped")
                break
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(self.monitoring_interval)

if __name__ == "__main__":
    scaler = AutoScaler()
    scaler.monitor_and_scale()
