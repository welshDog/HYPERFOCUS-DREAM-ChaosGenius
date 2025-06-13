"""
🔥 BROski ClanVerse Ultra - Motivation Engine
Advanced AI-Powered Motivation & Hyperfocus Enhancement System
"""

import random
import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger('BROski.MotivationEngine')

class MotivationEngine:
    """🚀 Ultra-Advanced BROski Motivation Engine for Neurodivergent Excellence"""

    def __init__(self, db_path: str = "chaosgenius.db"):
        self.db_path = db_path
        self.personality_traits = {
            'energy_level': 95,
            'enthusiasm': 100,
            'supportiveness': 100,
            'humor_level': 85,
            'intensity': 90
        }
        self.hyperfocus_phrases = [
            "🔥 HYPERFOCUS MODE ACTIVATED, BRO! Let's CRUSH this!",
            "⚡ Your brain is PURE LIGHTNING right now! RIDE THE WAVE!",
            "🧠 NEURAL PATHWAYS ARE LIT! This is YOUR moment!",
            "🎯 LOCKED AND LOADED! Your focus is UNSTOPPABLE!",
            "🌟 GENIUS MODE ENGAGED! You're in THE ZONE!"
        ]
        self.break_reminders = [
            "💪 BRO! Time for a power break! Your brain needs fuel!",
            "🏃‍♂️ Movement time! Quick walk = MASSIVE brain boost!",
            "💧 HYDRATION CHECK! Water = brain power, my dude!",
            "🧘‍♂️ Breathe deep, stretch out! Reset for MAXIMUM power!",
            "🍎 Snack attack! Feed that beautiful brain!"
        ]

    def get_personalized_motivation(self, user_id: str, current_mood: str = "neutral") -> Dict[str, Any]:
        """Generate ultra-personalized motivation based on user patterns"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get user's recent productivity patterns
            cursor.execute("""
                SELECT focus_score, mood, task_type, timestamp
                FROM productivity_data
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 10
            """, (user_id,))

            recent_data = cursor.fetchall()
            conn.close()

            # Analyze patterns for ultra-personalized response
            if recent_data:
                avg_focus = sum(row[0] for row in recent_data) / len(recent_data)
                recent_moods = [row[1] for row in recent_data]

                if avg_focus > 80:
                    motivation_type = "high_performer"
                elif avg_focus > 60:
                    motivation_type = "steady_climber"
                else:
                    motivation_type = "comeback_warrior"
            else:
                motivation_type = "fresh_start"

            return self._generate_motivation_response(motivation_type, current_mood)

        except Exception as e:
            logger.error(f"Error generating motivation: {e}")
            return self._get_default_motivation()

    def _generate_motivation_response(self, motivation_type: str, mood: str) -> Dict[str, Any]:
        """Generate specific motivation based on type and mood"""

        responses = {
            "high_performer": {
                "message": "🏆 ABSOLUTE LEGEND! You're on FIRE! Keep that momentum BLAZING!",
                "energy_boost": "⚡ Channel that excellence into your next challenge!",
                "tips": ["🎯 Set an even bigger goal!", "📈 Track your streak!", "🔥 Share your wins!"]
            },
            "steady_climber": {
                "message": "📈 CLIMBING THE MOUNTAIN, BRO! Every step counts!",
                "energy_boost": "💪 You're building UNSTOPPABLE momentum!",
                "tips": ["🎮 Gamify your next task!", "⏰ Try a focus sprint!", "🎵 Add your power playlist!"]
            },
            "comeback_warrior": {
                "message": "⚔️ COMEBACK STORY IN PROGRESS! Warriors rise from setbacks!",
                "energy_boost": "🔥 Your resilience is YOUR SUPERPOWER!",
                "tips": ["🧩 Break it into micro-tasks!", "🎯 One win at a time!", "💝 Celebrate small victories!"]
            },
            "fresh_start": {
                "message": "🌟 NEW JOURNEY BEGINS! Fresh energy, UNLIMITED potential!",
                "energy_boost": "🚀 Your brain is ready for GREATNESS!",
                "tips": ["📝 Start with brain dump!", "🎯 Pick ONE priority!", "⏰ Set a 25-min timer!"]
            }
        }

        base_response = responses.get(motivation_type, responses["fresh_start"])

        # Add mood-specific enhancement
        if mood == "excited":
            base_response["bonus"] = "🎊 THAT EXCITEMENT IS PURE ROCKET FUEL! USE IT!"
        elif mood == "tired":
            base_response["bonus"] = "😴 Tired brain = CREATIVE brain! Gentle progress counts!"
        elif mood == "anxious":
            base_response["bonus"] = "🧘‍♂️ Anxiety = care in disguise! Channel it into focus!"

        return base_response

    def get_hyperfocus_activation(self) -> str:
        """Get powerful hyperfocus activation phrase"""
        return random.choice(self.hyperfocus_phrases)

    def get_break_reminder(self, hours_focused: int) -> str:
        """Get contextual break reminder"""
        if hours_focused > 3:
            return "🚨 BRAIN BREAK EMERGENCY! You've been CRUSHING it for 3+ hours! MANDATORY rest time!"
        elif hours_focused > 2:
            return "⏰ Power break time! 2+ hours of genius-level work deserves a victory lap!"
        else:
            return random.choice(self.break_reminders)

    def _get_default_motivation(self) -> Dict[str, Any]:
        """Fallback motivation when data unavailable"""
        return {
            "message": "🌟 BROski here! Ready to IGNITE your productivity?",
            "energy_boost": "🔥 Today is YOUR day to shine!",
            "tips": ["🎯 Start with ONE task!", "⏰ Set a timer!", "💪 You've got this!"],
            "hyperfocus_phrase": self.get_hyperfocus_activation()
        }
