"""
🔐 BROski Guardian Code System - Mental Nightclub Bouncer
Your AI protects your time, focus, and energy like a BOUNCER at your mental nightclub
"""

import asyncio
import json
import logging
import sqlite3
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger("BROski.Guardian")


@dataclass
class GuardianRule:
    """A protection rule for the Guardian System"""

    name: str
    trigger_type: str  # 'time', 'energy', 'mood', 'boundary'
    condition: Dict[str, Any]
    action: str  # 'block', 'warn', 'suggest', 'redirect'
    message: str
    priority: int = 1
    active: bool = True


@dataclass
class ProtectionEvent:
    """An event where Guardian protection was triggered"""

    timestamp: datetime
    rule_name: str
    trigger_data: Dict[str, Any]
    action_taken: str
    user_response: Optional[str] = None
    effectiveness_score: Optional[float] = None


class BROskiGuardianSystem:
    """🛡️ Your personal AI bouncer - protects peace, energy, and focus"""

    def __init__(self, db_path: str = "chaosgenius.db"):
        self.db_path = db_path
        self.active_protections = {}
        self.protection_history = deque(maxlen=1000)
        self.user_boundaries = defaultdict(dict)
        self.energy_threshold_alerts = defaultdict(list)
        self.safe_mode_active = False

        # Initialize default protection rules
        self._init_default_rules()
        self._setup_database()

    def _init_default_rules(self):
        """Initialize default protection rules"""
        self.protection_rules = {
            "energy_crash_protection": GuardianRule(
                name="Energy Crash Shield",
                trigger_type="energy",
                condition={"energy_level": "<", "threshold": 30},
                action="redirect",
                message="🛡️ Guardian detected low energy! Time for a gentle break, champion. Your brain needs recharge time.",
                priority=1,
            ),
            "overwhelm_gate": GuardianRule(
                name="Overwhelm Gate",
                trigger_type="mood",
                condition={"mood": "overwhelmed", "confidence": ">", "threshold": 0.7},
                action="suggest",
                message="🌊 Guardian sees the overwhelm wave coming. Let's break this down into smaller, manageable pieces.",
                priority=2,
            ),
            "hyperfocus_burnout_prevention": GuardianRule(
                name="Hyperfocus Burnout Shield",
                trigger_type="time",
                condition={"continuous_work": ">", "threshold": 180},  # 3 hours
                action="warn",
                message="⚡ You've been in hyperfocus for 3+ hours! Guardian recommends a 15-minute break to maintain your superpower.",
                priority=1,
            ),
            "late_night_protection": GuardianRule(
                name="Sleep Guardian",
                trigger_type="time",
                condition={"hour": ">", "threshold": 23},
                action="suggest",
                message="🌙 Guardian notices it's getting late. Your creative brain does its best work when rested!",
                priority=2,
            ),
            "distraction_blocker": GuardianRule(
                name="Focus Fortress",
                trigger_type="boundary",
                condition={
                    "context": "hyperfocus_session",
                    "interruption_risk": ">",
                    "threshold": 0.6,
                },
                action="block",
                message="🎯 Guardian is protecting your hyperfocus zone! This can wait until your session is complete.",
                priority=3,
            ),
            "dopamine_depletion_alert": GuardianRule(
                name="Dopamine Reserve Monitor",
                trigger_type="mood",
                condition={"mood": "tired", "recent_completions": "<", "threshold": 1},
                action="suggest",
                message="🔋 Guardian detects low dopamine reserves. Let's do one tiny, easy win to spark your engine!",
                priority=2,
            ),
        }

    def _setup_database(self):
        """Setup Guardian system database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS guardian_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT,
                rule_name TEXT NOT NULL,
                trigger_data TEXT,
                action_taken TEXT,
                user_response TEXT,
                effectiveness_score REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_boundaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                boundary_type TEXT NOT NULL,
                boundary_data TEXT,
                active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    async def evaluate_protection_needed(
        self, user_id: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """🛡️ Main Guardian evaluation - checks if protection is needed"""
        protection_actions = []

        for rule_name, rule in self.protection_rules.items():
            if not rule.active:
                continue

            if await self._rule_triggered(rule, context):
                action = await self._execute_protection_action(user_id, rule, context)
                protection_actions.append(action)

                # Log the protection event
                event = ProtectionEvent(
                    timestamp=datetime.now(),
                    rule_name=rule_name,
                    trigger_data=context,
                    action_taken=action["action"],
                )
                self.protection_history.append(event)

        return protection_actions

    async def _rule_triggered(
        self, rule: GuardianRule, context: Dict[str, Any]
    ) -> bool:
        """Check if a protection rule is triggered"""
        try:
            if rule.trigger_type == "energy":
                user_energy = context.get("energy_level", 50)
                threshold = rule.condition["threshold"]
                operator = rule.condition.get("energy_level", ">")

                if operator == "<":
                    return user_energy < threshold
                elif operator == ">":
                    return user_energy > threshold

            elif rule.trigger_type == "mood":
                user_mood = context.get("mood", "neutral")
                required_mood = rule.condition.get("mood")
                confidence = context.get("mood_confidence", 0.5)

                if required_mood and user_mood == required_mood:
                    min_confidence = rule.condition.get("threshold", 0.5)
                    return confidence > min_confidence

            elif rule.trigger_type == "time":
                current_hour = datetime.now().hour
                if "hour" in rule.condition:
                    threshold = rule.condition["threshold"]
                    operator = rule.condition.get("hour", ">")

                    if operator == ">":
                        return current_hour > threshold

                if "continuous_work" in rule.condition:
                    work_minutes = context.get("continuous_work_minutes", 0)
                    return work_minutes > rule.condition["threshold"]

            elif rule.trigger_type == "boundary":
                # Check user-specific boundaries
                return await self._check_user_boundaries(context)

        except Exception as e:
            logger.error(f"Error evaluating rule {rule.name}: {e}")

        return False

    async def _execute_protection_action(
        self, user_id: str, rule: GuardianRule, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the protection action"""
        action_result = {
            "rule_name": rule.name,
            "action": rule.action,
            "message": rule.message,
            "priority": rule.priority,
            "timestamp": datetime.now().isoformat(),
        }

        if rule.action == "block":
            action_result["blocking"] = True
            action_result["suggested_action"] = "Take a break and return later"

        elif rule.action == "redirect":
            action_result["redirect_suggestions"] = (
                await self._get_redirect_suggestions(context)
            )

        elif rule.action == "suggest":
            action_result["suggestions"] = await self._get_contextual_suggestions(
                rule, context
            )

        elif rule.action == "warn":
            action_result["warning_level"] = "medium"
            action_result["continue_allowed"] = True

        # Store in database
        await self._log_protection_event(user_id, action_result, context)

        return action_result

    async def _get_redirect_suggestions(self, context: Dict[str, Any]) -> List[str]:
        """Get suggestions for healthier activities"""
        energy_level = context.get("energy_level", 50)

        if energy_level < 30:
            return [
                "🛌 Take a 10-minute power nap",
                "🚶‍♀️ Go for a gentle 5-minute walk",
                "💧 Drink some water and do breathing exercises",
                "🎵 Listen to calming music for a few minutes",
                "🌱 Do some light stretching",
            ]
        elif energy_level < 60:
            return [
                "☕ Get a healthy snack or drink",
                "🪟 Look out the window for 2 minutes",
                "📝 Do a quick brain dump of thoughts",
                "🧘‍♀️ Try a 5-minute meditation",
                "🎨 Doodle or do something creative",
            ]
        else:
            return [
                "🎯 Switch to a different type of task",
                "💪 Do some energizing movement",
                "🧠 Try a different approach to the problem",
                "📞 Connect with someone supportive",
                "🎮 Take a quick fun break",
            ]

    async def _get_contextual_suggestions(
        self, rule: GuardianRule, context: Dict[str, Any]
    ) -> List[str]:
        """Get contextual suggestions based on the rule and situation"""
        if rule.name == "Overwhelm Gate":
            return [
                "📋 Write down everything in your head",
                "🎯 Pick just ONE thing to focus on",
                "⏰ Set a timer for 15 minutes and work on that one thing",
                "🔢 Number your tasks by importance",
                "💜 Remember: You don't have to do everything right now",
            ]
        elif rule.name == "Dopamine Reserve Monitor":
            return [
                "✅ Complete one tiny, easy task",
                "🎵 Play your favorite motivational song",
                "📱 Text someone who makes you smile",
                "🏆 Celebrate something you did today",
                "🌟 Look at your past achievements",
            ]
        else:
            return [
                "🌟 Trust your Guardian - this protection is for your wellbeing",
                "💜 Your future self will thank you for this boundary",
                "🧠 Sustainable progress beats burnout every time",
            ]

    async def activate_safe_mode(
        self, user_id: str, duration_hours: int = 24
    ) -> Dict[str, Any]:
        """🛡️ Activate Safe Mode for sensitive mental health days"""
        self.safe_mode_active = True
        safe_mode_config = {
            "user_id": user_id,
            "activated_at": datetime.now().isoformat(),
            "duration_hours": duration_hours,
            "modifications": {
                "gentle_language": True,
                "reduced_notifications": True,
                "lower_energy_requirements": True,
                "extra_encouragement": True,
                "simplified_interface": True,
            },
        }

        # Store safe mode activation
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO guardian_events
            (timestamp, user_id, rule_name, trigger_data, action_taken)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                user_id,
                "safe_mode_activation",
                json.dumps(safe_mode_config),
                "safe_mode_enabled",
            ),
        )
        conn.commit()
        conn.close()

        return {
            "status": "safe_mode_activated",
            "message": "🛡️💜 Safe Mode activated. Guardian is providing extra gentle protection today.",
            "duration": f"{duration_hours} hours",
            "modifications": safe_mode_config["modifications"],
        }

    async def set_user_boundary(
        self, user_id: str, boundary_type: str, boundary_data: Dict[str, Any]
    ) -> bool:
        """Set a custom user boundary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO user_boundaries (user_id, boundary_type, boundary_data)
            VALUES (?, ?, ?)
        """,
            (user_id, boundary_type, json.dumps(boundary_data)),
        )

        conn.commit()
        conn.close()

        # Update in-memory boundaries
        self.user_boundaries[user_id][boundary_type] = boundary_data

        return True

    async def _check_user_boundaries(self, context: Dict[str, Any]) -> bool:
        """Check if user-specific boundaries are violated"""
        user_id = context.get("user_id")
        if not user_id or user_id not in self.user_boundaries:
            return False

        # Check various boundary types
        for boundary_type, boundary_data in self.user_boundaries[user_id].items():
            if boundary_type == "work_hours":
                current_hour = datetime.now().hour
                start = boundary_data.get("start_hour", 9)
                end = boundary_data.get("end_hour", 17)
                if not (start <= current_hour <= end):
                    return True

            elif boundary_type == "energy_limits":
                energy = context.get("energy_level", 50)
                min_energy = boundary_data.get("minimum_energy", 20)
                if energy < min_energy:
                    return True

        return False

    async def _log_protection_event(
        self, user_id: str, action_result: Dict[str, Any], context: Dict[str, Any]
    ):
        """Log protection event to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO guardian_events
            (timestamp, user_id, rule_name, trigger_data, action_taken)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                action_result["timestamp"],
                user_id,
                action_result["rule_name"],
                json.dumps(context),
                action_result["action"],
            ),
        )

        conn.commit()
        conn.close()

    def get_protection_stats(self, user_id: str = None) -> Dict[str, Any]:
        """Get Guardian protection statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if user_id:
            cursor.execute(
                """
                SELECT rule_name, COUNT(*) as count
                FROM guardian_events
                WHERE user_id = ? AND timestamp >= datetime('now', '-7 days')
                GROUP BY rule_name
            """,
                (user_id,),
            )
        else:
            cursor.execute(
                """
                SELECT rule_name, COUNT(*) as count
                FROM guardian_events
                WHERE timestamp >= datetime('now', '-7 days')
                GROUP BY rule_name
            """
            )

        protection_counts = dict(cursor.fetchall())

        cursor.execute(
            """
            SELECT COUNT(*) FROM guardian_events
            WHERE timestamp >= datetime('now', '-24 hours')
        """
        )

        recent_protections = cursor.fetchone()[0]
        conn.close()

        return {
            "protections_last_7_days": protection_counts,
            "protections_last_24_hours": recent_protections,
            "safe_mode_active": self.safe_mode_active,
            "total_active_rules": len(
                [r for r in self.protection_rules.values() if r.active]
            ),
        }


# Export Guardian system
guardian_system = BROskiGuardianSystem()
