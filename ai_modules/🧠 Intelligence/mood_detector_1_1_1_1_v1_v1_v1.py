"""
🧠 BROski ClanVerse Ultra - Advanced Mood Detection Engine
AI-Powered Emotional Intelligence for Neurodivergent Excellence
"""

import re
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
from textblob import TextBlob

logger = logging.getLogger('BROski.MoodDetector')

class MoodDetector:
    """🎯 Ultra-Advanced AI Mood Detection & Emotional Intelligence System"""

    def __init__(self, db_path: str = "chaosgenius.db"):
        self.db_path = db_path
        self.mood_patterns = {
            'hyperfocus': {
                'keywords': ['focused', 'in the zone', 'flowing', 'crushing', 'on fire', 'locked in'],
                'indicators': ['multiple tasks completed', 'high productivity', 'time flying'],
                'score_threshold': 0.7
            },
            'overwhelmed': {
                'keywords': ['stressed', 'too much', 'scattered', 'chaos', 'drowning', 'overloaded'],
                'indicators': ['multiple incomplete tasks', 'switching between activities'],
                'score_threshold': -0.3
            },
            'excited': {
                'keywords': ['pumped', 'excited', 'ready', 'motivated', 'energized', 'let\'s go'],
                'indicators': ['new project started', 'high energy messages'],
                'score_threshold': 0.5
            },
            'frustrated': {
                'keywords': ['stuck', 'annoying', 'difficult', 'problem', 'issue', 'bug'],
                'indicators': ['repeated attempts', 'error messages', 'debugging'],
                'score_threshold': -0.4
            },
            'accomplished': {
                'keywords': ['done', 'finished', 'completed', 'success', 'achieved', 'nailed'],
                'indicators': ['task completion', 'celebration emojis', 'sharing wins'],
                'score_threshold': 0.6
            },
            'tired': {
                'keywords': ['tired', 'exhausted', 'drained', 'burnt out', 'sleepy', 'worn out'],
                'indicators': ['late hours', 'low activity', 'simple responses'],
                'score_threshold': -0.2
            }
        }

        # ADHD-specific mood indicators
        self.adhd_indicators = {
            'dopamine_seeking': ['new project', 'different task', 'switch', 'something else'],
            'hyperfocus_crash': ['suddenly tired', 'brain fog', 'done for today'],
            'rejection_sensitivity': ['criticism', 'feedback', 'wrong', 'mistake'],
            'time_blindness': ['where did time go', 'already late', 'lost track']
        }

    def analyze_mood(self, text: str, user_id: str, context: Dict = None) -> Dict[str, Any]:
        """🎯 Comprehensive mood analysis with ADHD awareness"""
        try:
            # Clean and prepare text
            clean_text = self._preprocess_text(text)

            # Multiple analysis layers
            sentiment_score = self._get_sentiment_score(clean_text)
            keyword_matches = self._detect_mood_keywords(clean_text)
            adhd_patterns = self._detect_adhd_patterns(clean_text)
            context_clues = self._analyze_context(context) if context else {}

            # Get historical mood pattern
            mood_history = self._get_mood_history(user_id)

            # Combine all analysis for final mood determination
            final_mood = self._determine_final_mood(
                sentiment_score, keyword_matches, adhd_patterns,
                context_clues, mood_history
            )

            # Store mood data
            self._store_mood_data(user_id, final_mood, text)

            return {
                'primary_mood': final_mood['primary'],
                'secondary_mood': final_mood.get('secondary'),
                'confidence': final_mood['confidence'],
                'sentiment_score': sentiment_score,
                'adhd_indicators': adhd_patterns,
                'context_awareness': context_clues,
                'recommendations': self._get_mood_recommendations(final_mood),
                'energy_level': self._estimate_energy_level(final_mood, adhd_patterns),
                'support_message': self._generate_support_message(final_mood)
            }

        except Exception as e:
            logger.error(f"Error analyzing mood: {e}")
            return self._get_default_mood_analysis()

    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        # Remove extra whitespace, convert to lowercase
        clean_text = re.sub(r'\s+', ' ', text.lower().strip())
        # Handle emojis and special characters
        clean_text = re.sub(r'[^\w\s\!\?\.\,\-]', ' ', clean_text)
        return clean_text

    def _get_sentiment_score(self, text: str) -> float:
        """Get sentiment polarity using TextBlob"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity  # Returns -1 to 1
        except:
            return 0.0

    def _detect_mood_keywords(self, text: str) -> Dict[str, int]:
        """Detect mood-specific keywords"""
        matches = {}
        for mood, patterns in self.mood_patterns.items():
            count = 0
            for keyword in patterns['keywords']:
                if keyword in text:
                    count += 1
            matches[mood] = count
        return matches

    def _detect_adhd_patterns(self, text: str) -> List[str]:
        """Detect ADHD-specific behavioral patterns"""
        detected_patterns = []
        for pattern, keywords in self.adhd_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    detected_patterns.append(pattern)
                    break
        return detected_patterns

    def _analyze_context(self, context: Dict) -> Dict[str, Any]:
        """Analyze contextual information"""
        clues = {}

        if 'time_of_day' in context:
            hour = context['time_of_day']
            if hour < 6 or hour > 22:
                clues['late_hours'] = True
            elif 6 <= hour <= 10:
                clues['morning_energy'] = True

        if 'tasks_completed' in context:
            if context['tasks_completed'] > 5:
                clues['high_productivity'] = True
            elif context['tasks_completed'] == 0:
                clues['low_productivity'] = True

        if 'focus_time' in context:
            if context['focus_time'] > 180:  # 3+ hours
                clues['potential_hyperfocus'] = True

        return clues

    def _get_mood_history(self, user_id: str) -> List[Dict]:
        """Get recent mood history for pattern recognition"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT mood, confidence, timestamp
                FROM mood_data
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 10
            """, (user_id,))

            history = cursor.fetchall()
            conn.close()

            return [{'mood': row[0], 'confidence': row[1], 'timestamp': row[2]}
                   for row in history]
        except:
            return []

    def _determine_final_mood(self, sentiment: float, keywords: Dict,
                            adhd_patterns: List, context: Dict, history: List) -> Dict:
        """Combine all analysis for final mood determination"""

        # Score each possible mood
        mood_scores = {}

        for mood, patterns in self.mood_patterns.items():
            score = 0

            # Keyword matching score
            if keywords.get(mood, 0) > 0:
                score += keywords[mood] * 0.3

            # Sentiment alignment
            if sentiment >= patterns['score_threshold']:
                score += 0.4

            # Context clues
            if mood == 'hyperfocus' and context.get('potential_hyperfocus'):
                score += 0.3
            elif mood == 'tired' and context.get('late_hours'):
                score += 0.3
            elif mood == 'accomplished' and context.get('high_productivity'):
                score += 0.3

            mood_scores[mood] = score

        # Find highest scoring mood
        primary_mood = max(mood_scores, key=mood_scores.get)
        confidence = min(mood_scores[primary_mood], 1.0)

        # Secondary mood (if close score)
        sorted_moods = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)
        secondary_mood = None
        if len(sorted_moods) > 1 and sorted_moods[1][1] > 0.3:
            secondary_mood = sorted_moods[1][0]

        return {
            'primary': primary_mood,
            'secondary': secondary_mood,
            'confidence': confidence,
            'all_scores': mood_scores
        }

    def _get_mood_recommendations(self, mood: Dict) -> List[str]:
        """Get personalized recommendations based on mood"""
        primary = mood['primary']

        recommendations = {
            'hyperfocus': [
                "🔥 Ride this wave! Set a timer to maintain awareness",
                "💧 Hydration reminder - keep that brain fueled!",
                "📝 Document your breakthroughs while you're in the zone"
            ],
            'overwhelmed': [
                "🧘‍♂️ Time for a brain dump - get it all out on paper",
                "🎯 Pick ONE thing to focus on right now",
                "💪 Break it down into tiny, manageable steps"
            ],
            'excited': [
                "⚡ Channel that energy! Start with your biggest priority",
                "🎵 Add your power playlist to amplify the momentum",
                "📊 Set up tracking to see your progress"
            ],
            'frustrated': [
                "🔄 Step away for 5 minutes - fresh perspective incoming",
                "🧩 Break the problem into smaller pieces",
                "💬 Rubber duck debugging or ask for help!"
            ],
            'accomplished': [
                "🎉 Celebrate this win! You earned it!",
                "📈 Reflect on what worked - capture the strategy",
                "🎯 Ride this momentum into your next challenge"
            ],
            'tired': [
                "😴 Your brain needs rest - that's not weakness, it's wisdom",
                "☕ Gentle energy boost: water, snack, or short walk",
                "🎮 Maybe switch to a lighter, more enjoyable task"
            ]
        }

        return recommendations.get(primary, ["🌟 Take it one step at a time - you've got this!"])

    def _estimate_energy_level(self, mood: Dict, adhd_patterns: List) -> int:
        """Estimate energy level 1-100"""
        base_energy = {
            'hyperfocus': 90,
            'excited': 85,
            'accomplished': 75,
            'frustrated': 60,
            'overwhelmed': 45,
            'tired': 25
        }

        energy = base_energy.get(mood['primary'], 50)

        # Adjust for ADHD patterns
        if 'dopamine_seeking' in adhd_patterns:
            energy += 10
        if 'hyperfocus_crash' in adhd_patterns:
            energy -= 20

        return max(10, min(100, energy))

    def _generate_support_message(self, mood: Dict) -> str:
        """Generate supportive message based on mood"""
        primary = mood['primary']

        messages = {
            'hyperfocus': "🔥 You're in THE ZONE! BROski is here to keep you fueled and focused!",
            'overwhelmed': "💪 Feeling the chaos? BROski's got your back - let's break it down together!",
            'excited': "⚡ THAT ENERGY IS PURE GOLD! Let's channel it into something amazing!",
            'frustrated': "🧘‍♂️ Hitting a wall? Every genius faces them - let's find another way through!",
            'accomplished': "🏆 VICTORY LAP TIME! You absolutely crushed it - BROski is proud!",
            'tired': "😌 Your brain worked hard today. Rest is productive too, champion!"
        }

        return messages.get(primary, "🌟 BROski is here for you, whatever you're feeling!")

    def _store_mood_data(self, user_id: str, mood: Dict, original_text: str):
        """Store mood analysis for learning and patterns"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR IGNORE INTO mood_data
                (user_id, mood, confidence, original_text, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, mood['primary'], mood['confidence'],
                  original_text[:500], datetime.now().isoformat()))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error storing mood data: {e}")

    def _get_default_mood_analysis(self) -> Dict[str, Any]:
        """Fallback mood analysis"""
        return {
            'primary_mood': 'neutral',
            'confidence': 0.5,
            'sentiment_score': 0.0,
            'recommendations': ["🌟 Take it one step at a time!"],
            'energy_level': 50,
            'support_message': "🤗 BROski is here for you!"
        }

        return result
