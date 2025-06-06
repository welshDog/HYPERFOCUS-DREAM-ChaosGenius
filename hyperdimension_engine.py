#!/usr/bin/env python3
"""
💥🎮 HYPERDIMENSION ENGINE 🎮💥
The Ultimate Neurodivergent Productivity Gaming System

Transforms tasks into epic boss battles with:
- Boss HP systems tied to work progress
- Loot drops and BROski$ rewards
- NFT generation for focus sessions
- Level progression and achievements
- Discord integration ready

Built for ADHD brains who need EPIC DOPAMINE HITS! 🧠⚡
"""

import hashlib
import json
import math
import random
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class HyperDimensionEngine:
    """🎮 Core engine for gamified productivity"""

    def __init__(self, db_path: str = "chaosgenius.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize HyperDimension database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Boss Battles table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS boss_battles (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                boss_name TEXT NOT NULL,
                boss_type TEXT NOT NULL,
                task_description TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                boss_max_hp INTEGER NOT NULL,
                boss_current_hp INTEGER NOT NULL,
                total_damage_dealt INTEGER DEFAULT 0,
                battle_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                battle_end TIMESTAMP NULL,
                completed BOOLEAN DEFAULT FALSE,
                victory BOOLEAN DEFAULT FALSE
            )
        """
        )

        # User Stats table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS hyperdimension_stats (
                user_id TEXT PRIMARY KEY,
                level INTEGER DEFAULT 1,
                total_xp INTEGER DEFAULT 0,
                bosses_defeated INTEGER DEFAULT 0,
                total_damage_dealt INTEGER DEFAULT 0,
                total_broski_earned INTEGER DEFAULT 0,
                nfts_minted INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                last_battle TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Loot Drops table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS loot_drops (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                battle_id INTEGER NOT NULL,
                loot_type TEXT NOT NULL,
                loot_name TEXT NOT NULL,
                broski_reward INTEGER NOT NULL,
                rarity TEXT NOT NULL,
                claimed BOOLEAN DEFAULT FALSE,
                nft_minted BOOLEAN DEFAULT FALSE,
                nft_metadata TEXT NULL,
                dropped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (battle_id) REFERENCES boss_battles (id)
            )
        """
        )

        conn.commit()
        conn.close()

    def get_boss_templates(self) -> Dict[str, Dict]:
        """🎯 Epic boss templates based on task difficulty"""
        return {
            "easy": {
                "names": [
                    "Distraction Imp",
                    "Procrastination Pixie",
                    "Minor Chaos Goblin",
                    "Quick Task Troll",
                ],
                "hp_range": (50, 100),
                "loot_multiplier": 1.0,
                "xp_reward": (10, 25),
            },
            "medium": {
                "names": [
                    "Focus Breaker",
                    "Attention Phantom",
                    "Deadline Dragon",
                    "Workflow Wraith",
                ],
                "hp_range": (150, 250),
                "loot_multiplier": 1.5,
                "xp_reward": (30, 60),
            },
            "hard": {
                "names": [
                    "Executive Dysfunction Beast",
                    "Hyperfocus Hydra",
                    "Burnout Behemoth",
                    "Perfectionism Phoenix",
                ],
                "hp_range": (300, 500),
                "loot_multiplier": 2.0,
                "xp_reward": (70, 120),
            },
            "nightmare": {
                "names": [
                    "The Infinite Scroll",
                    "Supreme Overwhelm Entity",
                    "Master of All Distractions",
                    "Ultimate ADHD Challenge",
                ],
                "hp_range": (600, 1000),
                "loot_multiplier": 3.0,
                "xp_reward": (150, 300),
            },
        }

    def start_boss_battle(
        self, user_id: str, task_description: str, difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """🎮 Start a new boss battle!"""
        # Check for existing active battle
        if self.get_active_battle(user_id):
            return {"error": "You already have an active battle! Finish it first."}

        boss_templates = self.get_boss_templates()
        if difficulty not in boss_templates:
            difficulty = "medium"

        template = boss_templates[difficulty]
        boss_name = random.choice(template["names"])
        boss_hp = random.randint(*template["hp_range"])

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create new battle
        cursor.execute(
            """
            INSERT INTO boss_battles
            (user_id, boss_name, boss_type, task_description, difficulty, boss_max_hp, boss_current_hp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                user_id,
                boss_name,
                difficulty,
                task_description,
                difficulty,
                boss_hp,
                boss_hp,
            ),
        )

        battle_id = cursor.lastrowid

        # Initialize user stats if needed
        cursor.execute(
            """
            INSERT OR IGNORE INTO hyperdimension_stats (user_id) VALUES (?)
        """,
            (user_id,),
        )

        conn.commit()
        conn.close()

        return {
            "battle_id": battle_id,
            "boss": {
                "name": boss_name,
                "type": difficulty,
                "max_hp": boss_hp,
                "current_hp": boss_hp,
                "hp_percentage": 100,
            },
            "task_description": task_description,
            "difficulty": difficulty,
            "battle_start": datetime.now().isoformat(),
            "message": f"🎮 Boss Battle Started! Face the mighty {boss_name}!",
        }

    def deal_damage(
        self, user_id: str, damage_amount: int, work_type: str = "focused_work"
    ) -> Dict[str, Any]:
        """⚔️ Deal damage to the current boss"""
        battle = self.get_active_battle(user_id)
        if not battle:
            return {"error": "No active battle found!"}

        # Calculate actual damage with multipliers
        work_multipliers = {
            "focused_work": 1.0,
            "deep_focus": 1.4,
            "task_breakdown": 1.6,
            "time_management": 1.2,
            "creative_flow": 1.8,
            "problem_solving": 1.5,
        }

        multiplier = work_multipliers.get(work_type, 1.0)
        actual_damage = int(damage_amount * multiplier)

        # Critical hit chance (10% base, higher for certain work types)
        critical_chance = 0.15 if work_type in ["deep_focus", "creative_flow"] else 0.10
        critical_hit = random.random() < critical_chance

        if critical_hit:
            actual_damage = int(actual_damage * 1.75)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update battle
        new_hp = max(0, battle["boss_current_hp"] - actual_damage)
        total_damage = battle["total_damage_dealt"] + actual_damage

        cursor.execute(
            """
            UPDATE boss_battles
            SET boss_current_hp = ?, total_damage_dealt = ?
            WHERE id = ?
        """,
            (new_hp, total_damage, battle["id"]),
        )

        # Check for victory
        victory = new_hp <= 0
        loot_drops = []
        level_up_data = None

        if victory:
            # Mark battle as completed
            cursor.execute(
                """
                UPDATE boss_battles
                SET completed = TRUE, victory = TRUE, battle_end = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (battle["id"],),
            )

            # Generate loot drops
            loot_drops = self._generate_loot_drops(
                user_id, battle["id"], battle["difficulty"]
            )

            # Update user stats and check for level up
            level_up_data = self._update_user_stats(
                user_id, battle["difficulty"], total_damage
            )

            # Insert loot drops
            for loot in loot_drops:
                cursor.execute(
                    """
                    INSERT INTO loot_drops
                    (user_id, battle_id, loot_type, loot_name, broski_reward, rarity, nft_minted, nft_metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        battle["id"],
                        loot["type"],
                        loot["name"],
                        loot["broski_value"],
                        loot["rarity"],
                        loot["nft_minted"],
                        (
                            json.dumps(loot["nft_metadata"])
                            if loot.get("nft_metadata")
                            else None
                        ),
                    ),
                )

        conn.commit()
        conn.close()

        response = {
            "boss_name": battle["boss_name"],
            "boss_hp": new_hp,
            "boss_max_hp": battle["boss_max_hp"],
            "hp_percentage": (new_hp / battle["boss_max_hp"]) * 100,
            "damage_dealt": actual_damage,
            "total_damage": total_damage,
            "critical_hit": critical_hit,
            "work_type": work_type,
            "victory": victory,
        }

        if victory:
            response.update(
                {
                    "loot_drops": loot_drops,
                    "level_up": level_up_data,
                    "message": f"🎉 VICTORY! {battle['boss_name']} has been defeated!",
                }
            )

        return response

    def get_active_battle(self, user_id: str) -> Optional[Dict[str, Any]]:
        """📊 Get user's current active battle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, boss_name, boss_type, task_description, difficulty,
                   boss_max_hp, boss_current_hp, total_damage_dealt, battle_start
            FROM boss_battles
            WHERE user_id = ? AND completed = FALSE
            ORDER BY battle_start DESC LIMIT 1
        """,
            (user_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        battle_start = datetime.fromisoformat(row[8])
        duration = datetime.now() - battle_start

        return {
            "id": row[0],
            "boss_name": row[1],
            "boss_type": row[2],
            "task_description": row[3],
            "difficulty": row[4],
            "boss_max_hp": row[5],
            "boss_current_hp": row[6],
            "total_damage_dealt": row[7],
            "battle_start": row[8],
            "duration": str(duration).split(".")[0],  # Remove microseconds
            "hp_percentage": (row[6] / row[5]) * 100,
        }

    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """📈 Get comprehensive user statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get main stats
        cursor.execute(
            """
            SELECT level, total_xp, bosses_defeated, total_damage_dealt,
                   total_broski_earned, nfts_minted, longest_streak, current_streak
            FROM hyperdimension_stats
            WHERE user_id = ?
        """,
            (user_id,),
        )

        stats_row = cursor.fetchone()
        if not stats_row:
            # Initialize user if not exists
            cursor.execute(
                """
                INSERT INTO hyperdimension_stats (user_id) VALUES (?)
            """,
                (user_id,),
            )
            conn.commit()
            stats_row = (1, 0, 0, 0, 0, 0, 0, 0)

        # Get unclaimed loot
        cursor.execute(
            """
            SELECT loot_name, broski_reward, rarity, nft_minted
            FROM loot_drops
            WHERE user_id = ? AND NOT claimed
            ORDER BY dropped_at DESC
        """,
            (user_id,),
        )

        unclaimed_loot = [
            {
                "name": row[0],
                "broski_value": row[1],
                "rarity": row[2],
                "nft_minted": bool(row[3]),
            }
            for row in cursor.fetchall()
        ]

        # Get recent battles
        cursor.execute(
            """
            SELECT boss_name, difficulty, victory, battle_start
            FROM boss_battles
            WHERE user_id = ? AND completed = TRUE
            ORDER BY battle_end DESC LIMIT 5
        """,
            (user_id,),
        )

        recent_battles = [
            {
                "boss_name": row[0],
                "difficulty": row[1],
                "victory": bool(row[2]),
                "date": row[3],
            }
            for row in cursor.fetchall()
        ]

        conn.close()

        # Calculate XP to next level
        level = stats_row[0]
        current_xp = stats_row[1]
        xp_for_next_level = self._calculate_xp_for_level(level + 1)
        xp_needed = xp_for_next_level - current_xp

        return {
            "level": level,
            "total_xp": current_xp,
            "xp_to_next_level": max(0, xp_needed),
            "bosses_defeated": stats_row[2],
            "total_damage_dealt": stats_row[3],
            "total_broski_earned": stats_row[4],
            "nfts_minted": stats_row[5],
            "longest_streak": stats_row[6],
            "current_streak": stats_row[7],
            "unclaimed_loot": unclaimed_loot,
            "recent_battles": recent_battles,
        }

    def _generate_loot_drops(
        self, user_id: str, battle_id: int, difficulty: str
    ) -> List[Dict[str, Any]]:
        """🎁 Generate epic loot drops based on battle difficulty"""
        boss_templates = self.get_boss_templates()
        loot_multiplier = boss_templates[difficulty]["loot_multiplier"]

        # Base loot chance and quantities
        num_drops = random.randint(1, max(1, int(3 * loot_multiplier)))
        drops = []

        loot_tables = {
            "common": {
                "names": [
                    "Focus Potion",
                    "Productivity Boost",
                    "Time Crystal",
                    "Motivation Spark",
                ],
                "broski_range": (10, 30),
                "chance": 0.6,
            },
            "rare": {
                "names": [
                    "Hyperfocus Elixir",
                    "ADHD Power Core",
                    "Neurodivergent Badge",
                    "Flow State Gem",
                ],
                "broski_range": (40, 80),
                "chance": 0.25,
            },
            "epic": {
                "names": [
                    "Executive Function Enhancer",
                    "Dopamine Reactor",
                    "Chaos-to-Order Converter",
                ],
                "broski_range": (100, 200),
                "chance": 0.12,
            },
            "legendary": {
                "names": [
                    "Ultimate ADHD Mastery Crystal",
                    "Neurodivergent Crown",
                    "Infinite Focus Artifact",
                ],
                "broski_range": (250, 500),
                "chance": 0.03,
            },
        }

        for _ in range(num_drops):
            # Determine rarity
            roll = random.random()
            if roll < loot_tables["legendary"]["chance"] * loot_multiplier:
                rarity = "legendary"
            elif roll < loot_tables["epic"]["chance"] * loot_multiplier:
                rarity = "epic"
            elif roll < loot_tables["rare"]["chance"] * loot_multiplier:
                rarity = "rare"
            else:
                rarity = "common"

            loot_data = loot_tables[rarity]
            loot_name = random.choice(loot_data["names"])
            broski_value = int(
                random.randint(*loot_data["broski_range"]) * loot_multiplier
            )

            # Chance for NFT generation (higher for rarer items)
            nft_chances = {
                "common": 0.05,
                "rare": 0.15,
                "epic": 0.30,
                "legendary": 0.60,
            }
            nft_minted = random.random() < nft_chances[rarity]

            nft_metadata = None
            if nft_minted:
                nft_metadata = self._generate_nft_metadata(loot_name, rarity, user_id)

            drops.append(
                {
                    "type": "battle_loot",
                    "name": loot_name,
                    "rarity": rarity,
                    "broski_value": broski_value,
                    "nft_minted": nft_minted,
                    "nft_metadata": nft_metadata,
                }
            )

        return drops

    def _generate_nft_metadata(
        self, item_name: str, rarity: str, user_id: str
    ) -> Dict[str, Any]:
        """🎨 Generate NFT metadata for special loot"""
        timestamp = datetime.now().isoformat()
        unique_id = hashlib.md5(
            f"{user_id}_{item_name}_{timestamp}".encode()
        ).hexdigest()[:8]

        rarity_colors = {
            "common": "#808080",
            "rare": "#0099ff",
            "epic": "#9933ff",
            "legendary": "#ff9900",
        }

        return {
            "name": f"{item_name} #{unique_id}",
            "description": f"A {rarity} {item_name} earned through epic boss battle victory in the HyperDimension. This NFT represents the triumph of neurodivergent focus over chaos.",
            "image": f"ipfs://QmHyperDim{unique_id}",
            "attributes": [
                {"trait_type": "Rarity", "value": rarity.title()},
                {"trait_type": "Item Type", "value": item_name},
                {"trait_type": "Earned By", "value": user_id},
                {"trait_type": "Battle Victory", "value": "Yes"},
                {"trait_type": "HyperDimension Level", "value": "9999"},
                {"trait_type": "Rarity Color", "value": rarity_colors[rarity]},
            ],
            "external_url": f"https://hyperfocuszone.com/loot/{unique_id}",
            "hyperdimension_data": {
                "type": "battle_loot",
                "rarity": rarity,
                "earned_through": "boss_battle",
                "unique_id": unique_id,
            },
        }

    def _update_user_stats(
        self, user_id: str, difficulty: str, total_damage: int
    ) -> Optional[Dict[str, Any]]:
        """📊 Update user stats and check for level up"""
        boss_templates = self.get_boss_templates()
        xp_range = boss_templates[difficulty]["xp_reward"]
        xp_gained = random.randint(*xp_range)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get current stats
        cursor.execute(
            """
            SELECT level, total_xp FROM hyperdimension_stats WHERE user_id = ?
        """,
            (user_id,),
        )

        current_level, current_xp = cursor.fetchone()
        new_xp = current_xp + xp_gained

        # Check for level up
        level_up_data = None
        new_level = current_level

        while True:
            xp_needed_for_next = self._calculate_xp_for_level(new_level + 1)
            if new_xp >= xp_needed_for_next:
                new_level += 1
            else:
                break

        if new_level > current_level:
            level_up_data = {
                "old_level": current_level,
                "new_level": new_level,
                "xp_gained": xp_gained,
            }

        # Update stats
        cursor.execute(
            """
            UPDATE hyperdimension_stats
            SET level = ?, total_xp = ?, bosses_defeated = bosses_defeated + 1,
                total_damage_dealt = total_damage_dealt + ?, last_battle = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """,
            (new_level, new_xp, total_damage, user_id),
        )

        conn.commit()
        conn.close()

        return level_up_data

    def _calculate_xp_for_level(self, level: int) -> int:
        """🎯 Calculate XP needed for a specific level"""
        # Exponential scaling: Level 1=100, Level 2=250, Level 3=450, etc.
        return int(100 * (level**1.5))


# Global instance for the dashboard to use
hyperdimension = HyperDimensionEngine()

if __name__ == "__main__":
    # Test the engine
    engine = HyperDimensionEngine()

    print("🎮 Testing HyperDimension Engine...")

    # Start a test battle
    battle = engine.start_boss_battle("test_user", "Complete documentation", "medium")
    print(f"✅ Battle started: {battle}")

    # Deal some damage
    damage1 = engine.deal_damage("test_user", 50, "deep_focus")
    print(f"⚔️ Damage dealt: {damage1}")

    # Get user stats
    stats = engine.get_user_stats("test_user")
    print(f"📊 User stats: {stats}")

    print("🚀 HyperDimension Engine is ready for epic battles!")
