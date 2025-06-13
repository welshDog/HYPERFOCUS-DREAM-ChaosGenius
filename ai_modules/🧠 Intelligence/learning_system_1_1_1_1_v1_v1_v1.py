"""
🎓 BROski ClanVerse Ultra - Advanced Learning & Adaptation System
Self-Improving AI that learns from every interaction
"""

import json
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import pickle
import logging
from collections import defaultdict, Counter
import re

logger = logging.getLogger('BROski.LearningSystem')

class LearningSystem:
    """🧠 Ultra-Advanced Self-Learning AI System for BROski"""

    def __init__(self, db_path: str = "chaosgenius.db"):
        self.db_path = db_path
        self.learning_data = {
            'user_preferences': {},
            'response_effectiveness': {},
            'pattern_recognition': {},
            'optimization_insights': {}
        }
        self.adaptation_weights = {
            'response_success': 0.4,
            'user_feedback': 0.3,
            'pattern_consistency': 0.2,
            'outcome_quality': 0.1
        }
        self._initialize_learning_database()

    def _initialize_learning_database(self):
        """Initialize learning database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # User interaction learning table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    interaction_type TEXT,
                    input_data TEXT,
                    response_data TEXT,
                    effectiveness_score REAL,
                    user_feedback TEXT,
                    outcome_metrics TEXT,
                    timestamp TEXT
                )
            """)

            # Pattern recognition table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT,
                    pattern_data TEXT,
                    success_rate REAL,
                    confidence_level REAL,
                    usage_count INTEGER,
                    last_updated TEXT
                )
            """)

            # User preference learning
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences_learned (
                    user_id TEXT,
                    preference_type TEXT,
                    preference_value TEXT,
                    confidence REAL,
                    learn_date TEXT,
                    PRIMARY KEY (user_id, preference_type)
                )
            """)

            conn.commit()
            conn.close()
            logger.info("🎓 Learning database initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing learning database: {e}")

    def learn_from_interaction(self, user_id: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """🎯 Learn from every user interaction to improve responses"""
        try:
            # Extract learning signals
            interaction_type = interaction_data.get('type', 'general')
            user_input = interaction_data.get('input', '')
            bot_response = interaction_data.get('response', '')
            user_feedback = interaction_data.get('feedback')
            outcome_metrics = interaction_data.get('metrics', {})

            # Calculate effectiveness score
            effectiveness_score = self._calculate_effectiveness_score(
                interaction_data, user_feedback, outcome_metrics
            )

            # Store interaction for learning
            self._store_interaction_data(
                user_id, interaction_type, user_input, bot_response,
                effectiveness_score, user_feedback, outcome_metrics
            )

            # Update user preferences
            preferences_learned = self._extract_user_preferences(user_id, interaction_data)

            # Update pattern recognition
            patterns_identified = self._identify_new_patterns(interaction_data)

            # Generate adaptation insights
            adaptation_recommendations = self._generate_adaptation_insights(
                user_id, effectiveness_score, patterns_identified
            )

            return {
                'learning_success': True,
                'effectiveness_score': effectiveness_score,
                'preferences_learned': preferences_learned,
                'patterns_identified': patterns_identified,
                'adaptations': adaptation_recommendations,
                'confidence_improvement': self._calculate_confidence_improvement(user_id)
            }

        except Exception as e:
            logger.error(f"Error learning from interaction: {e}")
            return {'learning_success': False, 'error': str(e)}

    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get overall learning system statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Interaction statistics
            cursor.execute("SELECT COUNT(*) FROM learning_interactions")
            total_interactions = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(effectiveness_score) FROM learning_interactions")
            avg_effectiveness = cursor.fetchone()[0] or 0.0

            # Pattern statistics
            cursor.execute("SELECT COUNT(*) FROM learned_patterns WHERE success_rate > 0.7")
            high_success_patterns = cursor.fetchone()[0]

            # User preference statistics
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM user_preferences_learned")
            users_with_preferences = cursor.fetchone()[0]

            conn.close()

            return {
                'total_interactions_learned': total_interactions,
                'average_effectiveness': round(avg_effectiveness, 3),
                'high_success_patterns': high_success_patterns,
                'users_with_learned_preferences': users_with_preferences,
                'learning_confidence': min(100, (total_interactions / 100) * 100),
                'system_maturity': 'Advanced' if total_interactions > 500 else
                                 'Developing' if total_interactions > 100 else 'Learning'
            }

        except Exception as e:
            logger.error(f"Error getting learning statistics: {e}")
            return {'error': 'Unable to retrieve statistics'}

    def _calculate_effectiveness_score(self, interaction_data: Dict, user_feedback: Any,
                                      outcome_metrics: Dict) -> float:
        """Calculate effectiveness score for interaction"""
        try:
            score = 0.5  # Base score

            # Feedback-based scoring
            if user_feedback:
                if isinstance(user_feedback, (int, float)):
                    score = max(0, min(1, user_feedback / 5.0))  # Normalize 1-5 scale
                elif isinstance(user_feedback, str):
                    positive_words = ['good', 'great', 'helpful', 'amazing', 'perfect', 'yes']
                    negative_words = ['bad', 'wrong', 'unhelpful', 'terrible', 'no']

                    feedback_lower = user_feedback.lower()
                    if any(word in feedback_lower for word in positive_words):
                        score += 0.3
                    elif any(word in feedback_lower for word in negative_words):
                        score -= 0.3

            # Outcome metrics scoring
            if outcome_metrics:
                if outcome_metrics.get('task_completed'):
                    score += 0.2
                if outcome_metrics.get('user_engaged'):
                    score += 0.1
                if outcome_metrics.get('follow_up_questions') and outcome_metrics['follow_up_questions'] > 0:
                    score += 0.1

            return max(0.0, min(1.0, score))

        except Exception as e:
            logger.error(f"Error calculating effectiveness score: {e}")
            return 0.5

    def _store_interaction_data(self, user_id: str, interaction_type: str, user_input: str,
                               bot_response: str, effectiveness_score: float,
                               user_feedback: Any, outcome_metrics: Dict):
        """Store interaction data for learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO learning_interactions
                (user_id, interaction_type, input_data, response_data, effectiveness_score,
                 user_feedback, outcome_metrics, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, interaction_type, user_input[:1000], bot_response[:1000],
                  effectiveness_score, json.dumps(user_feedback) if user_feedback else None,
                  json.dumps(outcome_metrics), datetime.now().isoformat()))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Error storing interaction data: {e}")

    def _extract_user_preferences(self, user_id: str, interaction_data: Dict) -> Dict:
        """Extract and update user preferences from interaction"""
        try:
            preferences = {}

            # Extract communication style preferences
            user_input = interaction_data.get('input', '').lower()

            if any(word in user_input for word in ['motivate', 'pump up', 'energy']):
                preferences['communication_style'] = 'high_energy'
            elif any(word in user_input for word in ['calm', 'gentle', 'quiet']):
                preferences['communication_style'] = 'gentle_supportive'

            # Extract timing preferences
            context = interaction_data.get('context', {})
            if 'hour' in context:
                hour = context['hour']
                if 6 <= hour <= 12:
                    preferences['preferred_time'] = 'morning'
                elif 12 <= hour <= 18:
                    preferences['preferred_time'] = 'afternoon'
                else:
                    preferences['preferred_time'] = 'evening'

            # Store preferences
            if preferences:
                self._update_user_preferences(user_id, preferences)

            return preferences

        except Exception as e:
            logger.error(f"Error extracting user preferences: {e}")
            return {}

    def _update_user_preferences(self, user_id: str, preferences: Dict):
        """Update user preferences in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for pref_type, pref_value in preferences.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO user_preferences_learned
                    (user_id, preference_type, preference_value, confidence, learn_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, pref_type, str(pref_value), 0.8, datetime.now().isoformat()))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")

    def _identify_new_patterns(self, interaction_data: Dict) -> List[str]:
        """Identify new patterns from interaction"""
        try:
            patterns = []

            user_input = interaction_data.get('input', '').lower()
            context = interaction_data.get('context', {})

            # Pattern detection
            if 'hyperfocus' in user_input or 'in the zone' in user_input:
                patterns.append('hyperfocus_detection')

            if any(word in user_input for word in ['stuck', 'blocked', 'problem']):
                patterns.append('problem_solving_needed')

            if any(word in user_input for word in ['tired', 'exhausted', 'drained']):
                patterns.append('energy_management_needed')

            # Time-based patterns
            if context.get('hour'):
                hour = context['hour']
                if hour < 9 and 'morning' in user_input:
                    patterns.append('morning_person')
                elif hour > 20 and 'night' in user_input:
                    patterns.append('night_person')

            return patterns

        except Exception as e:
            logger.error(f"Error identifying patterns: {e}")
            return []

    def _generate_adaptation_insights(self, user_id: str, effectiveness_score: float,
                                    patterns: List[str]) -> List[str]:
        """Generate insights for adapting to user"""
        try:
            adaptations = []

            if effectiveness_score < 0.4:
                adaptations.append("Consider adjusting communication style")
                adaptations.append("User may need different type of support")

            if 'hyperfocus_detection' in patterns:
                adaptations.append("User shows hyperfocus patterns - provide focus support")

            if 'problem_solving_needed' in patterns:
                adaptations.append("User benefits from problem-solving approaches")

            if 'energy_management_needed' in patterns:
                adaptations.append("Focus on energy and wellness recommendations")

            if 'morning_person' in patterns:
                adaptations.append("User is most active in mornings")
            elif 'night_person' in patterns:
                adaptations.append("User is most active in evenings")

            return adaptations

        except Exception as e:
            logger.error(f"Error generating adaptation insights: {e}")
            return []

    def _calculate_confidence_improvement(self, user_id: str) -> float:
        """Calculate confidence improvement from learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get recent effectiveness scores
            cursor.execute("""
                SELECT effectiveness_score FROM learning_interactions
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 10
            """, (user_id,))

            scores = [row[0] for row in cursor.fetchall()]
            conn.close()

            if len(scores) < 2:
                return 0.0

            # Calculate trend
            recent_avg = sum(scores[:5]) / min(5, len(scores))
            overall_avg = sum(scores) / len(scores)

            return max(0.0, recent_avg - overall_avg)

        except Exception as e:
            logger.error(f"Error calculating confidence improvement: {e}")
            return 0.0

    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get learned user preferences"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT preference_type, preference_value, confidence
                FROM user_preferences_learned
                WHERE user_id = ?
            """, (user_id,))

            preferences = {}
            for row in cursor.fetchall():
                preferences[row[0]] = {
                    'value': row[1],
                    'confidence': row[2]
                }

            conn.close()
            return preferences

        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {}
