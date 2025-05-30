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
