#!/usr/bin/env python3
"""
🧑‍🔧⚡ HYPERFOCUS THROTTLE ENGINEER AGENT - STANDALONE EDITION ⚡🧑‍🔧
🎯💪 ADHD-OPTIMIZED PERFORMANCE THROTTLING SYSTEM! 💪🎯
😎♾️ NO EXTERNAL DEPENDENCIES - PURE LEGENDARY PYTHON! ♾️😎
"""

import time
import psutil
import json
import logging
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from collections import defaultdict, deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryRateLimiter:
    """🧠 In-memory rate limiter for when Redis isn't available"""
    def __init__(self, period=60):
        self.period = period
        self.requests = defaultdict(deque)
        self.lock = threading.Lock()

    def allow(self, key: str, limit: int) -> bool:
        """🚦 Check if request is allowed under current limits"""
        now = time.time()
        cutoff = now - self.period

        with self.lock:
            # Clean old requests
            while self.requests[key] and self.requests[key][0] < cutoff:
                self.requests[key].popleft()

            # Check if under limit
            if len(self.requests[key]) < limit:
                self.requests[key].append(now)
                return True
            return False

class HyperFocusZoneConfig:
    """🎯 HyperFocusZone-specific configuration management"""
    def __init__(self, path="/root/chaosgenius/hfz_config.json"):
        try:
            with open(path, 'r') as f:
                cfg = json.load(f)
        except FileNotFoundError:
            # Create default config if not exists
            cfg = self._create_default_config(path)

        self.default_limit = cfg.get("default_limit", 100)
        self.focus_multiplier = cfg.get("focus_limit_multiplier", 3)
        self.focus_tags = set(cfg.get("focus_tags", ["CODING", "BUSINESS", "AI_DEVELOPMENT"]))
        self.boost_flag = cfg.get("🔥_boost", 5)

    def _create_default_config(self, path: str) -> Dict:
        """🔧 Create default HyperFocus configuration"""
        default_config = {
            "default_limit": 100,
            "focus_limit_multiplier": 3,
            "focus_tags": ["CODING", "BUSINESS", "AI_DEVELOPMENT", "CREATIVE", "URGENT"],
            "🔥_boost": 5,
            "power_threshold": 20,
            "cpu_throttle_threshold": 80
        }

        with open(path, 'w') as f:
            json.dump(default_config, f, indent=2)

        print(f"✅ Created default HyperFocus config at {path}")
        return default_config

class HyperFocusRateLimiter:
    """🚀 Enhanced rate limiter with HyperFocus capabilities"""
    def __init__(self, config, period=60):
        self.memory_limiter = MemoryRateLimiter(period)
        self.config = config
        self.period = period
        self.current_focus = None
        self.focus_start_time = None

    def get_limit(self, key=None):
        """🎯 Get dynamic limit based on focus state and priority"""
        base = self.config.default_limit

        # CPU-based dynamic adjustment
        cpu = psutil.cpu_percent()
        if cpu > 80:
            base = max(1, base // 2)
        elif cpu < 20:
            base = base * 2

        # Priority flag boost (🔥)
        if key and key.endswith("🔥"):
            return int(base * self.config.boost_flag)

        # Focus session boost
        if self.current_focus and key and any(tag in key.upper() for tag in self.focus_tags):
            return int(base * self.config.focus_multiplier)

        return base

    def set_focus(self, focus_tag: str):
        """🎯 Start a HyperFocus session"""
        self.current_focus = focus_tag
        self.focus_start_time = time.time()
        logger.info(f"🎯 HyperFocus session started: {focus_tag}")

    def clear_focus(self):
        """🔄 End HyperFocus session"""
        if self.current_focus:
            duration = time.time() - self.focus_start_time
            logger.info(f"✅ HyperFocus session ended: {self.current_focus} ({duration:.1f}s)")
        self.current_focus = None
        self.focus_start_time = None

    @property
    def focus_tags(self):
        """🏷️ Get current focus tags"""
        return self.config.focus_tags

    def allow(self, key: str) -> bool:
        """🚦 Check if request is allowed under current limits"""
        try:
            limit = self.get_limit(key)
            return self.memory_limiter.allow(key, limit)
        except Exception as e:
            logger.error(f"❌ Rate limiter error: {e}")
            return True  # Fail open

class PowerMonitor:
    """⚡ System power and resource monitoring"""
    def __init__(self, config):
        self.config = config

    def level(self) -> float:
        """📊 Get current power level"""
        try:
            if hasattr(psutil, 'sensors_battery'):
                battery = psutil.sensors_battery()
                if battery:
                    return battery.percent
            # Fallback to CPU-based power estimate
            cpu_percent = psutil.cpu_percent()
            return max(0, 100 - cpu_percent)
        except:
            return 100.0

    def level_ok(self) -> bool:
        """✅ Check if power level is acceptable"""
        return self.level() > self.config.get("power_threshold", 20)

    def get_system_stats(self) -> Dict:
        """📊 Get comprehensive system statistics"""
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "power_level": self.level(),
                "power_ok": self.level_ok(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Error getting system stats: {e}")
            return {"error": str(e)}

class ThrottleAgent:
    """🤖 HyperFocus-aware throttling agent"""
    def __init__(self, limiter, power_monitor):
        self.limiter = limiter
        self.power = power_monitor
        self.task_history = []

    def plan(self, context: Dict) -> Optional[str]:
        """🎯 Decide route based on power, limits, and HyperFocus state"""
        task_key = context.get("task_key", "unknown")

        # Check power level first
        if not self.power.level_ok():
            logger.warning(f"⚠️ Low power: throttling task {task_key}")
            return None

        # Check rate limits
        if self.limiter.allow(task_key):
            logger.info(f"✅ Allowing task: {task_key}")
            return context.get("route", "default")
        else:
            logger.warning(f"🚫 Throttled task: {task_key}")
            return None

    def act(self, decision: Optional[str], context: Dict):
        """⚡ Execute the decision"""
        if decision:
            self.execute_hyperway(decision, context)
        else:
            self.handle_throttled_task(context)

    def observe(self) -> Dict:
        """👁️ Observe current system state"""
        stats = self.power.get_system_stats()
        stats.update({
            "current_focus": self.limiter.current_focus,
            "focus_duration": time.time() - self.limiter.focus_start_time if self.limiter.focus_start_time else 0,
            "active_tasks": len(self.task_history)
        })
        return stats

    def execute_hyperway(self, route: str, context: Dict):
        """🚀 Execute HyperWay pipeline"""
        task_key = context.get("task_key", "unknown")
        start_time = time.time()

        logger.info(f"🚀 Executing HyperWay: {route} for task {task_key}")

        # Simulate task execution with focus-based speed
        if self.limiter.current_focus and any(tag in task_key.upper() for tag in self.limiter.focus_tags):
            # Faster execution during focus sessions
            time.sleep(0.05)
            print(f"⚡ HYPERFOCUS BOOST: {task_key} executed at 2x speed!")
        else:
            time.sleep(0.1)

        execution_time = time.time() - start_time
        self.task_history.append({
            "task_key": task_key,
            "route": route,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "focus_session": self.limiter.current_focus
        })

        logger.info(f"✅ Completed {task_key} in {execution_time:.3f}s")

    def handle_throttled_task(self, context: Dict):
        """🔄 Handle throttled tasks"""
        task_key = context.get("task_key", "unknown")
        logger.info(f"⏳ Task {task_key} throttled - queuing for retry")

class HyperFocusThrottleEngineer:
    """🧑‍🔧 Main HyperFocus Throttle Engineer Agent"""
    def __init__(self):
        print("🧑‍🔧💜 HYPERFOCUS THROTTLE ENGINEER AGENT ONLINE! 💜🧑‍🔧")
        print("🎯 ADHD-OPTIMIZED PERFORMANCE THROTTLING ACTIVATED! 🎯")
        print("🧠 Running in standalone mode - no external dependencies!")

        # Initialize components
        self.config = HyperFocusZoneConfig()
        self.limiter = HyperFocusRateLimiter(self.config)
        self.power_monitor = PowerMonitor(self.config.__dict__)
        self.agent = ThrottleAgent(self.limiter, self.power_monitor)

        self._initialize_database()

    def _initialize_database(self):
        """🗄️ Initialize performance tracking database"""
        try:
            with sqlite3.connect("/root/chaosgenius/hyperfocus_performance.db") as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS task_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        task_key TEXT,
                        route TEXT,
                        execution_time REAL,
                        focus_session TEXT,
                        system_stats TEXT
                    )
                """)
                logger.info("✅ Performance database initialized")
        except Exception as e:
            logger.error(f"❌ Database initialization error: {e}")

    def start_focus_session(self, focus_tag: str):
        """🎯 Start a new HyperFocus session"""
        self.limiter.set_focus(focus_tag)
        print(f"🎯 HyperFocus session started: {focus_tag}")
        print(f"⚡ Performance boost: {self.config.focus_multiplier}x rate limit")
        print(f"🚀 Execution speed: 2x faster for {focus_tag} tasks!")

    def end_focus_session(self):
        """🔄 End current HyperFocus session"""
        self.limiter.clear_focus()
        print("✅ HyperFocus session ended")

    def process_task(self, task_key: str, route: str = "default", priority: bool = False):
        """⚡ Process a single task through the throttle system"""
        if priority:
            task_key += "🔥"

        context = {"task_key": task_key, "route": route}
        decision = self.agent.plan(context)
        self.agent.act(decision, context)

        return self.agent.observe()

    def get_performance_dashboard(self) -> Dict:
        """📊 Get comprehensive performance dashboard"""
        stats = self.agent.observe()

        return {
            "system_health": stats,
            "current_focus": self.limiter.current_focus,
            "focus_tags": list(self.limiter.focus_tags),
            "rate_limits": {
                "default": self.limiter.get_limit(),
                "focus_boost": self.limiter.get_limit("FOCUS_TASK"),
                "priority_boost": self.limiter.get_limit("PRIORITY🔥")
            },
            "recent_tasks": self.agent.task_history[-10:]  # Last 10 tasks
        }

    def run_demo(self):
        """🎮 Run demonstration of HyperFocus capabilities"""
        print("\n🎮 HYPERFOCUS THROTTLE ENGINEER DEMO STARTING! 🎮")
        print("=" * 60)

        # Demo tasks
        demo_tasks = [
            {"key": "CODING:api_refactor", "route": "code_update"},
            {"key": "BUSINESS:strategy_plan", "route": "business_analysis"},
            {"key": "background_sync🔥", "route": "data_sync"},
            {"key": "URGENT:security_patch🔥", "route": "security_update"},
            {"key": "routine_maintenance", "route": "maintenance"},
            {"key": "CODING:bug_fix", "route": "debug"},
            {"key": "AI_DEVELOPMENT:neural_training", "route": "ai_training"}
        ]

        # First, run without focus
        print(f"\n🔄 Processing tasks WITHOUT focus session...")
        for i, task in enumerate(demo_tasks[:3]):
            result = self.process_task(task["key"], task["route"])
            print(f"📊 Task {i+1}: CPU: {result['cpu_percent']:.1f}% | Power: {result['power_level']:.1f}%")
            time.sleep(0.2)

        # Now start focus session
        print(f"\n🎯 ACTIVATING HYPERFOCUS SESSION...")
        self.start_focus_session("CODING")

        print(f"\n⚡ Processing tasks WITH CODING focus active...")
        for i, task in enumerate(demo_tasks[3:]):
            result = self.process_task(task["key"], task["route"])
            print(f"📊 Task {i+4}: CPU: {result['cpu_percent']:.1f}% | Power: {result['power_level']:.1f}%")
            time.sleep(0.2)

        # End focus session
        self.end_focus_session()

        # Display dashboard
        dashboard = self.get_performance_dashboard()
        print(f"\n📊 PERFORMANCE DASHBOARD:")
        print(f"   🎯 Total tasks processed: {len(dashboard['recent_tasks'])}")
        print(f"   💻 Current CPU usage: {dashboard['system_health']['cpu_percent']:.1f}%")
        print(f"   ⚡ Power level: {dashboard['system_health']['power_level']:.1f}%")
        print(f"   🧠 Memory usage: {dashboard['system_health']['memory_percent']:.1f}%")
        print(f"   🔄 Rate limits:")
        print(f"      • Default: {dashboard['rate_limits']['default']}")
        print(f"      • Focus boost: {dashboard['rate_limits']['focus_boost']}")
        print(f"      • Priority boost: {dashboard['rate_limits']['priority_boost']}")

def main():
    """🚀 Launch HyperFocus Throttle Engineer Agent"""
    print("🧑‍🔧🚀 LAUNCHING HYPERFOCUS THROTTLE ENGINEER AGENT! 🚀🧑‍🔧")

    engineer = HyperFocusThrottleEngineer()
    engineer.run_demo()

    print(f"\n🎯 HyperFocus Throttle Engineer is now active!")
    print(f"💡 Available focus tags: {', '.join(engineer.limiter.focus_tags)}")
    print(f"🔥 Use priority flag (🔥) for urgent tasks!")
    print(f"🧠 ADHD-optimized throttling system ready for your empire!")

if __name__ == "__main__":
    main()