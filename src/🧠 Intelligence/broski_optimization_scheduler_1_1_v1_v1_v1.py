#!/usr/bin/env python3
"""
🛡️💜 BROSKI ULTRA OPTIMIZATION SCHEDULER - NEURODIVERGENT EXCELLENCE
Automated continuous optimization system that runs in the background

🚀 FEATURES:
- Continuous performance monitoring
- Automatic optimization triggers
- ADHD-friendly notifications
- Smart resource management
- Predictive optimization scheduling
"""

import asyncio
import json
import logging
import os
import sys
import threading
import time
from datetime import datetime, timedelta

import schedule

# Add our modules
sys.path.append("/root/chaosgenius")
from chaosgenius_ultra_optimizer_v3 import ChaosGeniusUltraOptimizer


class BROskiOptimizationScheduler:
    """🤖 Intelligent optimization scheduler with ADHD-friendly features"""

    def __init__(self):
        self.optimizer = ChaosGeniusUltraOptimizer()
        self.last_optimization = None
        self.optimization_history = []
        self.is_running = False

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - 🤖 SCHEDULER - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(
                    "/root/chaosgenius/logs/optimization_scheduler.log"
                ),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def should_optimize(self) -> bool:
        """🧠 Intelligent decision on whether to optimize now"""
        # Check system load
        import psutil

        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        # Don't optimize during high load (user might be in hyperfocus)
        if cpu_percent > 80 or memory_percent > 85:
            self.logger.info(
                "🧠 Skipping optimization - system under high load (protecting hyperfocus)"
            )
            return False

        # Check time since last optimization
        if self.last_optimization:
            time_since = datetime.now() - self.last_optimization
            if time_since < timedelta(hours=2):
                return False

        return True

    async def run_smart_optimization(self):
        """🚀 Run optimization with ADHD-friendly notifications"""
        if not self.should_optimize():
            return

        self.logger.info("🚀 Starting scheduled optimization...")

        try:
            # Run optimization
            results = await self.optimizer.run_full_optimization()

            # Update tracking
            self.last_optimization = datetime.now()
            self.optimization_history.append(
                {
                    "timestamp": self.last_optimization.isoformat(),
                    "success": True,
                    "improvements": results,
                }
            )

            self.logger.info("✅ Scheduled optimization completed successfully!")

        except Exception as e:
            self.logger.error(f"❌ Optimization failed: {str(e)}")
            self.optimization_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "error": str(e),
                }
            )

    def start_scheduler(self):
        """🎯 Start the optimization scheduler"""
        self.logger.info("🎯 Starting BROski Optimization Scheduler...")

        # Schedule optimizations at ADHD-friendly times
        schedule.every(3).hours.do(lambda: asyncio.run(self.run_smart_optimization()))
        schedule.every().day.at("03:00").do(
            lambda: asyncio.run(self.run_smart_optimization())
        )  # Night optimization
        schedule.every().sunday.at("06:00").do(
            lambda: asyncio.run(self.run_smart_optimization())
        )  # Weekly deep clean

        self.is_running = True

        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def stop_scheduler(self):
        """🛑 Stop the scheduler"""
        self.is_running = False
        self.logger.info("🛑 Optimization scheduler stopped")


# 🚀 Auto-start if run directly
if __name__ == "__main__":
    scheduler = BROskiOptimizationScheduler()

    try:
        print("🤖💜 BROski Optimization Scheduler STARTING...")
        print("🧠 Will automatically optimize your system when it's safe!")
        print("⚡ Running in background - won't interrupt your hyperfocus!")

        scheduler.start_scheduler()

    except KeyboardInterrupt:
        print("🛑 Stopping scheduler...")
        scheduler.stop_scheduler()
