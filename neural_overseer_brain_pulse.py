#!/usr/bin/env python3
"""
🧠💥 NEURAL OVERSEER: Brain Pulse Engine 💥🧠
Real-time neural pattern generation and brain state simulation
Generates live brain activity data for the Neural Pulse Visualizer
"""

import asyncio
import json
import logging
import random
import sqlite3
import threading
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="🧠 %(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class BrainPulse:
    """Represents a single brain pulse measurement"""

    frequency: float
    amplitude: float
    coherence: float
    timestamp: datetime
    wave_type: str  # alpha, beta, theta, gamma, delta


@dataclass
class NeuralState:
    """Complete neural state snapshot"""

    focus_level: int  # 0-100
    chaos_energy: int  # 0-100
    coherence: float  # 0-1
    neural_connections: int
    memory_formation_rate: int  # memories per minute
    patterns_detected: int
    emotional_resonance: float  # 0-1
    creativity_index: float  # 0-1
    timestamp: datetime


@dataclass
class NeuralPattern:
    """Detected neural pattern"""

    type: str
    description: str
    confidence: float  # 0-1
    frequency_range: tuple
    amplitude: float
    detected_at: datetime


@dataclass
class MemoryCrystal:
    """Memory crystal formation"""

    id: str
    type: str
    content: str
    strength: float  # 0-1
    connections: List[str]
    formed_at: datetime
    access_count: int


class NeuralOverseerBrainPulse:
    """🧠💥 Main Neural Overseer Brain Pulse Engine 💥🧠"""

    def __init__(self, db_path: str = "broski_neural_overseer.db"):
        self.db_path = db_path
        self.is_running = False
        self.current_state = None
        self.pulse_history = []
        self.pattern_history = []
        self.memory_crystals = []
        self.neural_frequency = 10.0  # Base frequency in Hz
        self.chaos_factor = 0.5
        self.focus_boost = False

        # Neural wave patterns
        self.wave_patterns = {
            "delta": (0.5, 4.0),  # Deep sleep
            "theta": (4.0, 8.0),  # Meditation/creativity
            "alpha": (8.0, 13.0),  # Relaxed awareness
            "beta": (13.0, 30.0),  # Active thinking
            "gamma": (30.0, 100.0),  # High-level cognitive processing
        }

        # Initialize database and start systems
        self.init_database()
        self.load_existing_data()

        logger.info("🧠💥 NEURAL OVERSEER: Brain Pulse Engine initialized!")

    def init_database(self):
        """Initialize the neural database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create tables
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS neural_pulses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frequency REAL,
                    amplitude REAL,
                    coherence REAL,
                    wave_type TEXT,
                    timestamp TEXT
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS neural_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    focus_level INTEGER,
                    chaos_energy INTEGER,
                    coherence REAL,
                    neural_connections INTEGER,
                    memory_formation_rate INTEGER,
                    patterns_detected INTEGER,
                    emotional_resonance REAL,
                    creativity_index REAL,
                    timestamp TEXT
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS neural_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    description TEXT,
                    confidence REAL,
                    frequency_min REAL,
                    frequency_max REAL,
                    amplitude REAL,
                    detected_at TEXT
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_crystals (
                    id TEXT PRIMARY KEY,
                    type TEXT,
                    content TEXT,
                    strength REAL,
                    connections TEXT,
                    formed_at TEXT,
                    access_count INTEGER
                )
            """
            )

            conn.commit()
            conn.close()
            logger.info("🗄️ Neural database initialized successfully!")

        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")

    def load_existing_data(self):
        """Load existing neural data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Load recent pulses
            cursor.execute(
                """
                SELECT frequency, amplitude, coherence, wave_type, timestamp
                FROM neural_pulses
                ORDER BY timestamp DESC
                LIMIT 100
            """
            )

            for row in cursor.fetchall():
                pulse = BrainPulse(
                    frequency=row[0],
                    amplitude=row[1],
                    coherence=row[2],
                    timestamp=datetime.fromisoformat(row[4]),
                    wave_type=row[3],
                )
                self.pulse_history.append(pulse)

            # Load memory crystals
            cursor.execute(
                "SELECT * FROM memory_crystals ORDER BY formed_at DESC LIMIT 50"
            )
            for row in cursor.fetchall():
                crystal = MemoryCrystal(
                    id=row[0],
                    type=row[1],
                    content=row[2],
                    strength=row[3],
                    connections=json.loads(row[4]) if row[4] else [],
                    formed_at=datetime.fromisoformat(row[5]),
                    access_count=row[6],
                )
                self.memory_crystals.append(crystal)

            conn.close()
            logger.info(
                f"📊 Loaded {len(self.pulse_history)} pulses and {len(self.memory_crystals)} memory crystals"
            )

        except Exception as e:
            logger.error(f"❌ Failed to load existing data: {e}")

    def generate_brain_pulse(self) -> BrainPulse:
        """Generate a realistic brain pulse measurement"""

        # Calculate dynamic frequency based on current state and chaos
        base_freq = self.neural_frequency
        chaos_variation = random.uniform(-5, 5) * self.chaos_factor
        focus_boost_factor = 1.5 if self.focus_boost else 1.0

        frequency = max(0.5, base_freq + chaos_variation) * focus_boost_factor

        # Determine wave type based on frequency
        wave_type = "beta"  # default
        for wave, (min_freq, max_freq) in self.wave_patterns.items():
            if min_freq <= frequency <= max_freq:
                wave_type = wave
                break

        # Generate amplitude with natural variation
        amplitude = random.uniform(0.3, 1.0) * (1 + 0.2 * np.sin(time.time() * 0.1))

        # Calculate coherence (higher when focused, lower when chaotic)
        base_coherence = 0.7 if self.focus_boost else 0.5
        coherence_variation = random.uniform(-0.2, 0.2) * self.chaos_factor
        coherence = max(0.1, min(1.0, base_coherence + coherence_variation))

        pulse = BrainPulse(
            frequency=frequency,
            amplitude=amplitude,
            coherence=coherence,
            timestamp=datetime.now(),
            wave_type=wave_type,
        )

        # Store pulse
        self.pulse_history.append(pulse)
        if len(self.pulse_history) > 1000:
            self.pulse_history.pop(0)

        # Save to database
        self.save_pulse_to_db(pulse)

        return pulse

    def generate_neural_state(self) -> NeuralState:
        """Generate comprehensive neural state"""

        # Calculate metrics based on recent pulse history
        recent_pulses = self.pulse_history[-10:] if self.pulse_history else []

        # Focus level (higher for beta/gamma waves)
        avg_frequency = (
            np.mean([p.frequency for p in recent_pulses]) if recent_pulses else 15.0
        )
        focus_level = min(100, max(0, int((avg_frequency - 5) * 5)))
        if self.focus_boost:
            focus_level = min(100, focus_level + 25)

        # Chaos energy (inverse of coherence)
        avg_coherence = (
            np.mean([p.coherence for p in recent_pulses]) if recent_pulses else 0.5
        )
        chaos_energy = max(0, min(100, int((1 - avg_coherence) * 100)))

        # Neural connections (simulated growth)
        base_connections = 847293
        connection_growth = (
            len(self.pattern_history) * 1247 + len(self.memory_crystals) * 5432
        )
        neural_connections = base_connections + connection_growth

        # Memory formation rate
        memory_rate = max(1, int(15 + focus_level * 0.3 + random.uniform(-5, 5)))

        # Emotional resonance and creativity
        emotional_resonance = max(0, min(1, 0.6 + 0.3 * np.sin(time.time() * 0.05)))
        creativity_index = max(0, min(1, chaos_energy * 0.01 + 0.3))

        state = NeuralState(
            focus_level=focus_level,
            chaos_energy=chaos_energy,
            coherence=avg_coherence,
            neural_connections=neural_connections,
            memory_formation_rate=memory_rate,
            patterns_detected=len(self.pattern_history),
            emotional_resonance=emotional_resonance,
            creativity_index=creativity_index,
            timestamp=datetime.now(),
        )

        self.current_state = state
        self.save_state_to_db(state)

        return state

    def detect_neural_patterns(self) -> List[NeuralPattern]:
        """Detect patterns in recent brain activity"""

        if len(self.pulse_history) < 10:
            return []

        recent_pulses = self.pulse_history[-20:]
        detected_patterns = []

        # Pattern detection algorithms
        frequencies = [p.frequency for p in recent_pulses]
        amplitudes = [p.amplitude for p in recent_pulses]

        # 1. Frequency Synchronization Pattern
        freq_std = np.std(frequencies)
        if freq_std < 2.0:  # Low variation = synchronization
            pattern = NeuralPattern(
                type="frequency_sync",
                description="Neural frequency synchronization detected",
                confidence=max(0.5, 1 - freq_std / 2),
                frequency_range=(min(frequencies), max(frequencies)),
                amplitude=np.mean(amplitudes),
                detected_at=datetime.now(),
            )
            detected_patterns.append(pattern)

        # 2. Gamma Burst Pattern
        gamma_count = sum(1 for f in frequencies if f > 30)
        if gamma_count > len(frequencies) * 0.3:
            pattern = NeuralPattern(
                type="gamma_burst",
                description="High-frequency gamma burst activity",
                confidence=gamma_count / len(frequencies),
                frequency_range=(30, max(frequencies)),
                amplitude=np.mean(
                    [a for p, a in zip(recent_pulses, amplitudes) if p.frequency > 30]
                ),
                detected_at=datetime.now(),
            )
            detected_patterns.append(pattern)

        # 3. Alpha Wave Dominance
        alpha_count = sum(1 for f in frequencies if 8 <= f <= 13)
        if alpha_count > len(frequencies) * 0.4:
            pattern = NeuralPattern(
                type="alpha_dominance",
                description="Relaxed awareness state - alpha wave dominance",
                confidence=alpha_count / len(frequencies),
                frequency_range=(8, 13),
                amplitude=np.mean(
                    [
                        a
                        for p, a in zip(recent_pulses, amplitudes)
                        if 8 <= p.frequency <= 13
                    ]
                ),
                detected_at=datetime.now(),
            )
            detected_patterns.append(pattern)

        # 4. Coherence Spike
        recent_coherence = [p.coherence for p in recent_pulses[-5:]]
        if np.mean(recent_coherence) > 0.8:
            pattern = NeuralPattern(
                type="coherence_spike",
                description="High neural coherence - optimal brain state",
                confidence=np.mean(recent_coherence),
                frequency_range=(min(frequencies), max(frequencies)),
                amplitude=np.mean(amplitudes),
                detected_at=datetime.now(),
            )
            detected_patterns.append(pattern)

        # 5. Creative Flow State
        if self.current_state and self.current_state.creativity_index > 0.7:
            pattern = NeuralPattern(
                type="creative_flow",
                description="Creative flow state - optimal for innovation",
                confidence=self.current_state.creativity_index,
                frequency_range=(6, 20),  # Theta-Alpha bridge
                amplitude=np.mean(amplitudes),
                detected_at=datetime.now(),
            )
            detected_patterns.append(pattern)

        # Store patterns
        for pattern in detected_patterns:
            self.pattern_history.append(pattern)
            self.save_pattern_to_db(pattern)

        # Keep pattern history manageable
        if len(self.pattern_history) > 100:
            self.pattern_history = self.pattern_history[-100:]

        return detected_patterns

    def form_memory_crystal(
        self, trigger_pattern: Optional[NeuralPattern] = None
    ) -> Optional[MemoryCrystal]:
        """Form a new memory crystal based on current neural activity"""

        if not self.current_state or random.random() > 0.1:  # 10% chance per cycle
            return None

        # Memory types based on current state
        memory_types = {
            "insight": "💡 Sudden insight crystallized",
            "pattern": "🧩 Pattern recognition memory formed",
            "emotion": "❤️ Emotional memory crystallized",
            "skill": "🎯 Skill-based memory consolidated",
            "creative": "🎨 Creative breakthrough recorded",
            "focus": "🔥 Deep focus state remembered",
            "chaos": "🌀 Chaos energy pattern stored",
        }

        # Choose memory type based on current state
        if self.current_state.creativity_index > 0.7:
            memory_type = "creative"
        elif self.current_state.focus_level > 80:
            memory_type = "focus"
        elif self.current_state.chaos_energy > 70:
            memory_type = "chaos"
        elif trigger_pattern:
            memory_type = "pattern"
        else:
            memory_type = random.choice(list(memory_types.keys()))

        crystal_id = f"MC_{int(time.time())}_{random.randint(1000, 9999)}"

        # Generate connections to existing crystals
        connections = []
        if len(self.memory_crystals) > 0:
            num_connections = min(3, random.randint(1, len(self.memory_crystals)))
            connections = random.sample(
                [c.id for c in self.memory_crystals], num_connections
            )

        crystal = MemoryCrystal(
            id=crystal_id,
            type=memory_type,
            content=memory_types[memory_type],
            strength=self.current_state.coherence,
            connections=connections,
            formed_at=datetime.now(),
            access_count=0,
        )

        self.memory_crystals.append(crystal)
        self.save_crystal_to_db(crystal)

        # Keep memory crystal collection manageable
        if len(self.memory_crystals) > 200:
            # Remove weakest crystals
            self.memory_crystals.sort(key=lambda c: c.strength)
            self.memory_crystals = self.memory_crystals[50:]

        logger.info(f"💎 Memory crystal formed: {crystal.type} - {crystal.content}")
        return crystal

    def save_pulse_to_db(self, pulse: BrainPulse):
        """Save brain pulse to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO neural_pulses (frequency, amplitude, coherence, wave_type, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    pulse.frequency,
                    pulse.amplitude,
                    pulse.coherence,
                    pulse.wave_type,
                    pulse.timestamp.isoformat(),
                ),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"❌ Failed to save pulse: {e}")

    def save_state_to_db(self, state: NeuralState):
        """Save neural state to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO neural_states
                (focus_level, chaos_energy, coherence, neural_connections, memory_formation_rate,
                 patterns_detected, emotional_resonance, creativity_index, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    state.focus_level,
                    state.chaos_energy,
                    state.coherence,
                    state.neural_connections,
                    state.memory_formation_rate,
                    state.patterns_detected,
                    state.emotional_resonance,
                    state.creativity_index,
                    state.timestamp.isoformat(),
                ),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"❌ Failed to save state: {e}")

    def save_pattern_to_db(self, pattern: NeuralPattern):
        """Save neural pattern to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO neural_patterns
                (type, description, confidence, frequency_min, frequency_max, amplitude, detected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    pattern.type,
                    pattern.description,
                    pattern.confidence,
                    pattern.frequency_range[0],
                    pattern.frequency_range[1],
                    pattern.amplitude,
                    pattern.detected_at.isoformat(),
                ),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"❌ Failed to save pattern: {e}")

    def save_crystal_to_db(self, crystal: MemoryCrystal):
        """Save memory crystal to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO memory_crystals
                (id, type, content, strength, connections, formed_at, access_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    crystal.id,
                    crystal.type,
                    crystal.content,
                    crystal.strength,
                    json.dumps(crystal.connections),
                    crystal.formed_at.isoformat(),
                    crystal.access_count,
                ),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"❌ Failed to save crystal: {e}")

    def get_current_data(self) -> Dict[str, Any]:
        """Get current neural data for API"""
        pulse = self.generate_brain_pulse()
        state = self.generate_neural_state()
        patterns = self.detect_neural_patterns()

        # Possibly form new memory crystal
        new_crystal = self.form_memory_crystal(patterns[0] if patterns else None)

        return {
            "pulse": asdict(pulse),
            "state": asdict(state),
            "patterns": [asdict(p) for p in patterns],
            "recent_patterns": [asdict(p) for p in self.pattern_history[-5:]],
            "memory_crystals": len(self.memory_crystals),
            "new_crystal": asdict(new_crystal) if new_crystal else None,
            "timestamp": datetime.now().isoformat(),
        }

    def get_memory_data(self) -> Dict[str, Any]:
        """Get memory-related data"""
        recent_memories = sorted(
            self.memory_crystals, key=lambda c: c.formed_at, reverse=True
        )[:10]

        return {
            "recent_memories": [
                {
                    "type": crystal.type,
                    "content": crystal.content,
                    "strength": crystal.strength,
                    "timestamp": crystal.formed_at.isoformat(),
                }
                for crystal in recent_memories
            ],
            "total_crystals": len(self.memory_crystals),
            "strongest_memory": (
                max(self.memory_crystals, key=lambda c: c.strength).__dict__
                if self.memory_crystals
                else None
            ),
        }

    def boost_focus(self):
        """Activate focus boost mode"""
        self.focus_boost = True
        threading.Timer(
            30.0, self.reset_focus_boost
        ).start()  # Auto-reset after 30 seconds
        logger.info("🚀 FOCUS BOOST ACTIVATED!")

    def reset_focus_boost(self):
        """Reset focus boost mode"""
        self.focus_boost = False
        logger.info("🔄 Focus boost reset")

    def adjust_chaos_factor(self, factor: float):
        """Adjust chaos factor (0.0 - 1.0)"""
        self.chaos_factor = max(0.0, min(1.0, factor))
        logger.info(f"🌀 Chaos factor adjusted to {self.chaos_factor}")

    def start_neural_engine(self):
        """Start the neural engine (for continuous operation)"""
        self.is_running = True
        logger.info("🧠💥 NEURAL ENGINE STARTED!")

        def neural_loop():
            while self.is_running:
                try:
                    self.get_current_data()  # This generates and processes all neural data
                    time.sleep(0.5)  # Update every 500ms
                except Exception as e:
                    logger.error(f"❌ Neural loop error: {e}")
                    time.sleep(1)

        neural_thread = threading.Thread(target=neural_loop, daemon=True)
        neural_thread.start()

    def stop_neural_engine(self):
        """Stop the neural engine"""
        self.is_running = False
        logger.info("🛑 Neural engine stopped")


# Global neural engine instance
neural_engine = None


def get_neural_engine() -> NeuralOverseerBrainPulse:
    """Get or create the neural engine instance"""
    global neural_engine
    if neural_engine is None:
        neural_engine = NeuralOverseerBrainPulse()
        neural_engine.start_neural_engine()
    return neural_engine


if __name__ == "__main__":
    # Test the neural engine
    print("🧠💥 TESTING NEURAL OVERSEER BRAIN PULSE ENGINE 💥🧠")

    engine = NeuralOverseerBrainPulse("test_neural.db")

    # Generate some test data
    for i in range(10):
        data = engine.get_current_data()
        print(
            f"🧠 Pulse {i+1}: {data['pulse']['frequency']:.1f} Hz, State: {data['state']['focus_level']}% focus"
        )
        time.sleep(1)

    print("💎 Memory Crystals:", len(engine.memory_crystals))
    print("🧩 Patterns Detected:", len(engine.pattern_history))
    print("✅ Neural Engine test completed!")
