#!/usr/bin/env python3
"""
🧠 BROski X ULTRA BRAIN ENGINE 🧠
Hybrid Redis/SQLite Memory System for LEGENDARY Intelligence Enhancement

Created by: The BROski X Brain Construction Crew
Status: ULTRA OPERATIONAL
"""

import hashlib
import json
import logging
import pickle
import queue
import sqlite3
import threading
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import redis

# Configure logging for brain activity
logging.basicConfig(
    level=logging.INFO,
    format="🧠 %(asctime)s - BROski Brain: %(message)s",
    handlers=[
        logging.FileHandler("/root/chaosgenius/logs/brain_activity.log"),
        logging.StreamHandler(),
    ],
)


@dataclass
class BrainMemory:
    """Individual memory unit in the BROski Brain"""

    id: str
    content: str
    timestamp: datetime
    memory_type: str  # conversation, pattern, energy, goal
    context: Dict[str, Any]
    importance: float
    associations: List[str]
    energy_level: int
    tags: List[str]


@dataclass
class BrainPattern:
    """Detected patterns in brain activity"""

    pattern_id: str
    pattern_type: str
    frequency: int
    confidence: float
    triggers: List[str]
    outcomes: List[str]
    energy_correlation: float


class BROskiBrainEngine:
    """
    🧠 ULTRA HYBRID MEMORY ENGINE 🧠

    Features:
    - SQLite for persistent storage
    - Redis for ultra-fast retrieval
    - Pattern recognition AI
    - Energy state tracking
    - Memory crystal generation
    - Association mapping
    """

    def __init__(self, db_path: str = "/root/chaosgenius/🗄️ Databases/broski_brain.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)

        # Initialize Redis connection
        try:
            self.redis_client = redis.Redis(
                host="localhost", port=6379, db=0, decode_responses=True
            )
            self.redis_client.ping()
            self.logger.info(
                "🔥 Redis connection established! ULTRA FAST MODE ACTIVATED!"
            )
        except redis.ConnectionError:
            self.logger.warning("⚠️ Redis not available, using SQLite only mode")
            self.redis_client = None

        # Initialize SQLite database
        self._init_database()

        # Brain state tracking
        self.current_energy = 8
        self.intelligence_level = 95.0
        self.pattern_cache = {}
        self.memory_associations = defaultdict(list)

        # Background processing
        self.processing_queue = queue.Queue()
        self.background_thread = threading.Thread(
            target=self._background_processor, daemon=True
        )
        self.background_thread.start()

        self.logger.info("🧠 BROski X ULTRA BRAIN ENGINE: FULLY OPERATIONAL! 🚀")

    def _init_database(self):
        """Initialize SQLite database with optimized tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main memories table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                memory_type TEXT NOT NULL,
                context TEXT,
                importance REAL DEFAULT 0.5,
                associations TEXT,
                energy_level INTEGER DEFAULT 5,
                tags TEXT,
                embedding BLOB
            )
        """
        )

        # Patterns table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                confidence REAL DEFAULT 0.5,
                triggers TEXT,
                outcomes TEXT,
                energy_correlation REAL DEFAULT 0.0,
                last_seen REAL NOT NULL
            )
        """
        )

        # Energy states table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS energy_states (
                timestamp REAL PRIMARY KEY,
                energy_level INTEGER NOT NULL,
                mood TEXT,
                activity TEXT,
                productivity REAL,
                context TEXT
            )
        """
        )

        # Memory crystals table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_crystals (
                crystal_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                creation_time REAL NOT NULL,
                memories_count INTEGER,
                patterns_count INTEGER,
                energy_snapshot TEXT,
                crystal_data BLOB
            )
        """
        )

        # Create indexes for performance
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories(timestamp)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_patterns_type ON patterns(pattern_type)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_energy_timestamp ON energy_states(timestamp)"
        )

        conn.commit()
        conn.close()

        self.logger.info("🗄️ Brain database initialized with ULTRA structure!")

    def store_memory(
        self,
        content: str,
        memory_type: str = "conversation",
        context: Dict[str, Any] = None,
        energy_level: int = None,
    ) -> str:
        """Store a new memory in the brain"""

        # Generate unique memory ID
        memory_id = hashlib.sha256(f"{content}{time.time()}".encode()).hexdigest()[:16]

        # Use current energy if not specified
        if energy_level is None:
            energy_level = self.current_energy

        # Create memory object
        memory = BrainMemory(
            id=memory_id,
            content=content,
            timestamp=datetime.now(),
            memory_type=memory_type,
            context=context or {},
            importance=self._calculate_importance(content, memory_type),
            associations=[],
            energy_level=energy_level,
            tags=self._extract_tags(content),
        )

        # Store in SQLite
        self._store_memory_sqlite(memory)

        # Store in Redis for fast access
        if self.redis_client:
            self._store_memory_redis(memory)

        # Queue for background processing
        self.processing_queue.put(("process_memory", memory))

        self.logger.info(
            f"💾 Memory stored: {memory_id} ({memory_type}) - Energy: {energy_level}"
        )
        return memory_id

    def _store_memory_sqlite(self, memory: BrainMemory):
        """Store memory in SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO memories
            (id, content, timestamp, memory_type, context, importance,
             associations, energy_level, tags, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                memory.id,
                memory.content,
                memory.timestamp.timestamp(),
                memory.memory_type,
                json.dumps(memory.context),
                memory.importance,
                json.dumps(memory.associations),
                memory.energy_level,
                json.dumps(memory.tags),
                pickle.dumps(self._generate_embedding(memory.content)),
            ),
        )

        conn.commit()
        conn.close()

    def _store_memory_redis(self, memory: BrainMemory):
        """Store memory in Redis for ultra-fast access"""
        try:
            memory_key = f"memory:{memory.id}"
            memory_data = {
                "content": memory.content,
                "timestamp": memory.timestamp.isoformat(),
                "type": memory.memory_type,
                "context": json.dumps(memory.context),
                "importance": memory.importance,
                "energy": memory.energy_level,
                "tags": json.dumps(memory.tags),
            }

            self.redis_client.hmset(memory_key, memory_data)
            self.redis_client.expire(memory_key, 86400)  # 24 hour TTL

            # Add to type-based sets for quick filtering
            self.redis_client.sadd(f"memories:{memory.memory_type}", memory.id)

            # Add to recent memories list
            self.redis_client.lpush("recent_memories", memory.id)
            self.redis_client.ltrim("recent_memories", 0, 99)  # Keep last 100

        except Exception as e:
            self.logger.warning(f"Redis storage failed: {e}")

    def retrieve_memories(
        self, memory_type: str = None, limit: int = 50, min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Retrieve memories with optional filtering"""

        # Try Redis first for speed
        if self.redis_client and memory_type:
            try:
                return self._retrieve_memories_redis(memory_type, limit)
            except Exception as e:
                self.logger.warning(f"Redis retrieval failed: {e}")

        # Fallback to SQLite
        return self._retrieve_memories_sqlite(memory_type, limit, min_importance)

    def _retrieve_memories_redis(
        self, memory_type: str, limit: int
    ) -> List[Dict[str, Any]]:
        """Ultra-fast memory retrieval from Redis"""
        memory_ids = self.redis_client.smembers(f"memories:{memory_type}")
        memories = []

        for memory_id in list(memory_ids)[:limit]:
            memory_data = self.redis_client.hgetall(f"memory:{memory_id}")
            if memory_data:
                memory_data["id"] = memory_id
                memory_data["context"] = json.loads(memory_data.get("context", "{}"))
                memory_data["tags"] = json.loads(memory_data.get("tags", "[]"))
                memories.append(memory_data)

        return sorted(memories, key=lambda x: x["timestamp"], reverse=True)

    def _retrieve_memories_sqlite(
        self, memory_type: str = None, limit: int = 50, min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Retrieve memories from SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT id, content, timestamp, memory_type, context, importance,
                   associations, energy_level, tags
            FROM memories
            WHERE importance >= ?
        """
        params = [min_importance]

        if memory_type:
            query += " AND memory_type = ?"
            params.append(memory_type)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        memories = []
        for row in rows:
            memory = {
                "id": row[0],
                "content": row[1],
                "timestamp": datetime.fromtimestamp(row[2]).isoformat(),
                "type": row[3],
                "context": json.loads(row[4] or "{}"),
                "importance": row[5],
                "associations": json.loads(row[6] or "[]"),
                "energy": row[7],
                "tags": json.loads(row[8] or "[]"),
            }
            memories.append(memory)

        return memories

    def find_similar_memories(
        self, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find memories similar to the query using embedding similarity"""
        query_embedding = self._generate_embedding(query)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, content, timestamp, memory_type, context, importance,
                   energy_level, tags, embedding
            FROM memories
            ORDER BY timestamp DESC
            LIMIT 1000
        """
        )

        results = []
        for row in cursor.fetchall():
            if row[8]:  # Has embedding
                memory_embedding = pickle.loads(row[8])
                similarity = self._cosine_similarity(query_embedding, memory_embedding)

                if similarity > 0.3:  # Similarity threshold
                    memory = {
                        "id": row[0],
                        "content": row[1],
                        "timestamp": datetime.fromtimestamp(row[2]).isoformat(),
                        "type": row[3],
                        "context": json.loads(row[4] or "{}"),
                        "importance": row[5],
                        "energy": row[6],
                        "tags": json.loads(row[7] or "[]"),
                        "similarity": similarity,
                    }
                    results.append(memory)

        conn.close()

        # Sort by similarity and return top results
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:limit]

    def detect_patterns(self) -> List[Dict[str, Any]]:
        """Advanced pattern detection in brain activity"""
        patterns = []

        # Analyze energy patterns
        energy_patterns = self._analyze_energy_patterns()
        patterns.extend(energy_patterns)

        # Analyze conversation patterns
        conversation_patterns = self._analyze_conversation_patterns()
        patterns.extend(conversation_patterns)

        # Analyze time-based patterns
        time_patterns = self._analyze_time_patterns()
        patterns.extend(time_patterns)

        # Store patterns in database
        for pattern in patterns:
            self._store_pattern(pattern)

        self.logger.info(f"🧩 Detected {len(patterns)} patterns in brain activity")
        return patterns

    def update_energy_state(
        self,
        energy_level: int,
        mood: str = None,
        activity: str = None,
        productivity: float = None,
    ):
        """Update current energy state and log for pattern analysis"""
        self.current_energy = max(1, min(10, energy_level))

        # Store energy state
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO energy_states
            (timestamp, energy_level, mood, activity, productivity, context)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                time.time(),
                self.current_energy,
                mood,
                activity,
                productivity,
                json.dumps(
                    {
                        "previous_energy": getattr(self, "_prev_energy", 5),
                        "change_rate": self.current_energy
                        - getattr(self, "_prev_energy", 5),
                    }
                ),
            ),
        )

        conn.commit()
        conn.close()

        # Update Redis if available
        if self.redis_client:
            self.redis_client.set("current_energy", self.current_energy)
            self.redis_client.lpush(
                "energy_history",
                json.dumps(
                    {
                        "timestamp": time.time(),
                        "energy": self.current_energy,
                        "mood": mood,
                    }
                ),
            )
            self.redis_client.ltrim("energy_history", 0, 199)  # Keep last 200

        self._prev_energy = self.current_energy
        self.logger.info(f"⚡ Energy updated: {self.current_energy}/10 - Mood: {mood}")

    def get_brain_stats(self) -> Dict[str, Any]:
        """Get comprehensive brain statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Memory counts by type
        cursor.execute(
            "SELECT memory_type, COUNT(*) FROM memories GROUP BY memory_type"
        )
        memory_counts = dict(cursor.fetchall())

        # Pattern counts
        cursor.execute("SELECT COUNT(*) FROM patterns")
        pattern_count = cursor.fetchone()[0]

        # Crystal counts
        cursor.execute("SELECT COUNT(*) FROM memory_crystals")
        crystal_count = cursor.fetchone()[0]

        # Total memories
        cursor.execute("SELECT COUNT(*) FROM memories")
        total_memories = cursor.fetchone()[0]

        # Average importance
        cursor.execute("SELECT AVG(importance) FROM memories")
        avg_importance = cursor.fetchone()[0] or 0.5

        # Recent energy average
        cursor.execute(
            """
            SELECT AVG(energy_level) FROM energy_states
            WHERE timestamp > ?
        """,
            (time.time() - 86400,),
        )  # Last 24 hours
        recent_energy = cursor.fetchone()[0] or self.current_energy

        conn.close()

        stats = {
            "total_memories": total_memories,
            "memory_types": memory_counts,
            "patterns_detected": pattern_count,
            "memory_crystals": crystal_count,
            "current_energy": self.current_energy,
            "average_energy_24h": round(recent_energy, 1),
            "intelligence_level": self.intelligence_level,
            "average_importance": round(avg_importance, 2),
            "redis_connected": self.redis_client is not None,
            "background_queue_size": self.processing_queue.qsize(),
        }

        return stats

    def _background_processor(self):
        """Background thread for processing memories and patterns"""
        while True:
            try:
                task_type, data = self.processing_queue.get(timeout=1)

                if task_type == "process_memory":
                    self._process_memory_associations(data)
                elif task_type == "detect_patterns":
                    self.detect_patterns()

                self.processing_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Background processing error: {e}")

    def _calculate_importance(self, content: str, memory_type: str) -> float:
        """Calculate memory importance based on content and type"""
        base_importance = {
            "conversation": 0.6,
            "pattern": 0.8,
            "energy": 0.4,
            "goal": 0.9,
            "crystal": 1.0,
        }.get(memory_type, 0.5)

        # Boost importance for certain keywords
        boost_keywords = ["broski", "ultra", "legendary", "genius", "breakthrough"]
        content_lower = content.lower()
        keyword_boost = sum(
            0.1 for keyword in boost_keywords if keyword in content_lower
        )

        # Length factor
        length_factor = min(len(content) / 1000, 0.2)

        return min(1.0, base_importance + keyword_boost + length_factor)

    def _extract_tags(self, content: str) -> List[str]:
        """Extract relevant tags from content"""
        content_lower = content.lower()

        # Predefined tag categories
        energy_tags = ["energy", "tired", "excited", "motivated", "exhausted"]
        work_tags = ["coding", "building", "creating", "developing", "designing"]
        emotion_tags = ["happy", "frustrated", "satisfied", "confused", "amazed"]
        broski_tags = ["broski", "ultra", "legendary", "epic", "incredible"]

        tags = []
        for tag_list in [energy_tags, work_tags, emotion_tags, broski_tags]:
            tags.extend([tag for tag in tag_list if tag in content_lower])

        return list(set(tags))  # Remove duplicates

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate simple embedding for text similarity"""
        # This is a simplified embedding - in production, use proper models
        words = text.lower().split()
        vocab_size = 1000
        embedding_dim = 100

        # Simple hash-based embedding
        embedding = np.zeros(embedding_dim)
        for word in words:
            word_hash = hash(word) % vocab_size
            embedding[word_hash % embedding_dim] += 1

        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _analyze_energy_patterns(self) -> List[Dict[str, Any]]:
        """Analyze energy level patterns"""
        # Implementation for energy pattern analysis
        return []

    def _analyze_conversation_patterns(self) -> List[Dict[str, Any]]:
        """Analyze conversation patterns"""
        # Implementation for conversation pattern analysis
        return []

    def _analyze_time_patterns(self) -> List[Dict[str, Any]]:
        """Analyze time-based patterns"""
        # Implementation for time pattern analysis
        return []

    def _store_pattern(self, pattern: Dict[str, Any]):
        """Store detected pattern in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO patterns
            (pattern_id, pattern_type, frequency, confidence, triggers,
             outcomes, energy_correlation, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                pattern["id"],
                pattern["type"],
                pattern["frequency"],
                pattern["confidence"],
                json.dumps(pattern.get("triggers", [])),
                json.dumps(pattern.get("outcomes", [])),
                pattern.get("energy_correlation", 0.0),
                time.time(),
            ),
        )

        conn.commit()
        conn.close()

    def _process_memory_associations(self, memory: BrainMemory):
        """Process memory associations in background"""
        # Find similar memories and create associations
        similar = self.find_similar_memories(memory.content, limit=5)

        associations = [m["id"] for m in similar if m["similarity"] > 0.5]

        if associations:
            # Update memory with associations
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE memories SET associations = ? WHERE id = ?
            """,
                (json.dumps(associations), memory.id),
            )

            conn.commit()
            conn.close()


# Example usage and testing
if __name__ == "__main__":
    # Initialize the brain
    brain = BROskiBrainEngine()

    # Store some test memories
    brain.store_memory(
        "Working on the ULTRA B.R.A.I.N.DROP system with incredible energy!",
        "conversation",
        {"activity": "coding", "mood": "excited"},
        energy_level=9,
    )

    brain.store_memory(
        "Detected amazing patterns in user engagement with BROski terminology",
        "pattern",
        {"confidence": 0.95},
        energy_level=8,
    )

    brain.update_energy_state(
        9, mood="ultra_motivated", activity="brain_building", productivity=0.95
    )

    # Retrieve and display stats
    stats = brain.get_brain_stats()
    print("🧠 BRAIN STATS:", json.dumps(stats, indent=2))

    # Find similar memories
    similar = brain.find_similar_memories("BROski energy patterns")
    print(f"🔍 Found {len(similar)} similar memories")

    print("🧠 BROski X ULTRA BRAIN ENGINE: Test complete! LEGENDARY! 🚀")
