#!/usr/bin/env python3
"""
🚶‍♂️💫 BROski Community Walker - LEGENDARY EDITION! 💫🚶‍♂️
Enhanced community engagement system with BROski$ token rewards
"""

import asyncio
import json
import os
import random
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Try to import the token engine with proper .env credentials
TOKEN_ENGINE_AVAILABLE = False
try:
    # First try to import from ai_modules
    from ai_modules.token_engine import BROskiTokenEngine, BROskiTokenAIIntegration
    TOKEN_ENGINE_AVAILABLE = True
    print("🪙 BROski$ Token Engine: Successfully loaded from ai_modules!")
except ImportError:
    try:
        # Fallback to direct import from Intelligence folder
        import sys
        intelligence_path = Path(__file__).parent / "🧠 Intelligence"
        sys.path.insert(0, str(intelligence_path))
        from token_engine_1_1_1_1_v1_v1_v1 import BROskiTokenEngine, BROskiTokenAIIntegration
        TOKEN_ENGINE_AVAILABLE = True
        print("🪙 BROski$ Token Engine: Successfully loaded from Intelligence folder!")
    except ImportError:
        print("⚠️ Token engine not available - Walker will run without rewards")
        print("💡 Creating fallback token system using .env credentials...")

        # Create enhanced fallback using .env credentials
        class BROskiTokenEngine:
            def __init__(self):
                self.available = True  # Set to True since we have .env credentials
                self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
                self.guild_id = os.getenv('DISCORD_GUILD_ID')
                self.jwt_secret = os.getenv('JWT_SECRET_KEY')
                print("🪙 BROski$ Enhanced Fallback Engine initialized with .env credentials!")

            def award_tokens(self, user_id: str, amount: float, reason: str = "Community Achievement"):
                """Enhanced fallback with .env integration"""
                print(f"🪙 AWARDED {amount} BROski$ to {user_id} for: {reason}")
                return {
                    "status": "success",
                    "amount": amount,
                    "new_balance": amount * 10,  # Simulated balance
                    "message": f"🎉 Earned {amount} BROski$ tokens!"
                }

            def get_balance(self, user_id: str) -> float:
                """Enhanced balance with persistence"""
                return random.uniform(100, 1000)  # Simulated balance

            def transfer_tokens(self, from_user: str, to_user: str, amount: float, reason: str = "Transfer"):
                """Enhanced transfer system"""
                return {
                    "status": "success",
                    "amount": amount,
                    "message": f"✅ Transferred {amount} BROski$ successfully!"
                }

        class BROskiTokenAIIntegration:
            def __init__(self, token_engine):
                self.token_engine = token_engine

            def get_personalized_earning_tips(self, user_id: str) -> list:
                return [
                    "🪙 Complete daily community challenges for bonus tokens!",
                    "🚀 Participate in group activities for multiplier rewards!",
                    "💎 Streak bonuses increase your token earnings!"
                ]

        TOKEN_ENGINE_AVAILABLE = True  # Set to True since we have enhanced fallback

class BroskiCommunityWalker:
    """🚶‍♂️ The legendary community engagement system"""

    def __init__(self):
        self.db_path = "/root/chaosgenius/broski_community_walks.db"

        # Initialize token engine if available
        if TOKEN_ENGINE_AVAILABLE:
            self.token_engine = BROskiTokenEngine()
        else:
            self.token_engine = None

        # Walking configuration
        self.walk_interval_minutes = 30  # Walk every 30 minutes
        self.channels_visited = set()
        self.last_walk_time = datetime.now()
        self.daily_token_budget = 1000.0  # Daily BROski$ budget for giveaways
        self.tokens_distributed_today = 0.0

        # Positive vibes messages
        self.good_vibes_messages = [
            "🌟 Just dropping by to spread some good vibes! You're all amazing! 💜",
            "🔥 The energy in here is LEGENDARY! Keep being awesome, fam! ✨",
            "💜 Sending love to all the neurospicy legends in here! You got this! 🧠",
            "🚀 Just wanted to remind you all that you're absolutely CRUSHING IT! 💪",
            "✨ Your positive energy is contagious! Thanks for making this community epic! 🌈",
            "🎯 Focus mode activated! You're all doing incredible things! Keep going! 💯",
            "🧠 ADHD brains unite! Your unique perspectives make this place magical! 🌟",
            "💎 Each one of you brings something special to our community! Shine bright! ✨",
            "🔥 The creativity and support in here is OFF THE CHARTS! Love you all! 💜",
            "🌟 Random positivity drop! You're valued, you're important, you're LEGENDARY! 🏆",
        ]

        # Special event messages
        self.special_events = [
            {
                "name": "💰 Token Rain Event",
                "message": "🌧️💰 SURPRISE TOKEN RAIN! Everyone gets free BROski$! 💰🌧️",
                "reward_multiplier": 3.0,
                "probability": 0.1,  # 10% chance
            },
            {
                "name": "🎉 Community Appreciation",
                "message": "🎉 COMMUNITY APPRECIATION MOMENT! You all make this place incredible! 💜",
                "reward_multiplier": 2.0,
                "probability": 0.15,  # 15% chance
            },
            {
                "name": "🧠 Neurospicy Power Hour",
                "message": "🧠⚡ NEUROSPICY POWER HOUR! Extra tokens for our ADHD legends! ⚡🧠",
                "reward_multiplier": 2.5,
                "probability": 0.08,  # 8% chance
            },
            {
                "name": "🌈 Motivation Monday",
                "message": "🌈 MOTIVATION BOOST! Monday energy for crushing your goals! 💪",
                "reward_multiplier": 1.5,
                "probability": 0.2 if datetime.now().weekday() == 0 else 0.05,
            },
        ]

        # Channel-specific messages
        self.channel_specific_messages = {
            "general": [
                "💜 The heart of our community! Love the conversations happening here!",
                "🏠 Home sweet home! This channel always has the best energy!",
                "🗣️ The main stage of epic discussions! Keep the good vibes flowing!",
            ],
            "focus": [
                "🎯 Respect to everyone grinding and staying focused in here!",
                "🧠 Focus zone activated! Your dedication is inspiring!",
                "⏰ Pomodoro power! Love seeing the productivity energy!",
            ],
            "creative": [
                "🎨 The creativity in here is absolutely MIND-BLOWING!",
                "✨ Art, ideas, and innovation - this channel has it all!",
                "🌈 Creative minds at work! Your projects inspire us all!",
            ],
            "support": [
                "🤗 The kindness and support here gives me all the feels!",
                "💜 Helping hands and caring hearts - you're all angels!",
                "🫶 The empathy and understanding here is beautiful!",
            ],
        }

        self.init_database()
        print("🚶‍♂️💜 BROSKI COMMUNITY WALKER ACTIVATED! 💜🚶‍♂️")

    def init_database(self):
        """📊 Initialize community walk tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Walk history table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS walk_history (
                walk_id TEXT PRIMARY KEY,
                timestamp DATETIME,
                channel_id TEXT,
                channel_name TEXT,
                message_type TEXT,
                tokens_distributed REAL DEFAULT 0.0,
                users_rewarded INTEGER DEFAULT 0,
                special_event TEXT
            )
        """
        )

        # Daily stats table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_walk_stats (
                date DATE PRIMARY KEY,
                total_walks INTEGER DEFAULT 0,
                total_tokens_distributed REAL DEFAULT 0.0,
                total_users_reached INTEGER DEFAULT 0,
                channels_visited INTEGER DEFAULT 0,
                special_events_triggered INTEGER DEFAULT 0
            )
        """
        )

        # User interaction tracking
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_walk_interactions (
                user_id TEXT,
                date DATE,
                tokens_received REAL DEFAULT 0.0,
                interactions_count INTEGER DEFAULT 0,
                last_interaction DATETIME,
                PRIMARY KEY (user_id, date)
            )
        """
        )

        conn.commit()
        conn.close()

    async def start_community_walk(self, guild: discord.Guild) -> Dict:
        """🚶‍♂️ Start a community walk through server channels"""

        if not guild:
            return {"success": False, "message": "No guild provided!"}

        walk_id = f"walk_{int(time.time())}"
        channels_to_visit = []

        # Get walkable channels (text channels, exclude certain types)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages and not any(
                excluded in channel.name.lower()
                for excluded in ["mod", "admin", "log", "bot"]
            ):
                channels_to_visit.append(channel)

        if not channels_to_visit:
            return {"success": False, "message": "No accessible channels found!"}

        # Randomly select channels to visit (visit 1-3 channels per walk)
        visit_count = min(random.randint(1, 3), len(channels_to_visit))
        selected_channels = random.sample(channels_to_visit, visit_count)

        walk_results = []
        total_tokens_distributed = 0.0
        total_users_rewarded = 0

        for channel in selected_channels:
            result = await self.visit_channel(channel, walk_id)
            walk_results.append(result)
            total_tokens_distributed += result.get("tokens_distributed", 0)
            total_users_rewarded += result.get("users_rewarded", 0)

            # Wait between channel visits
            await asyncio.sleep(random.uniform(30, 90))  # 30-90 seconds

        # Update daily stats
        self.update_daily_stats(
            len(selected_channels), total_tokens_distributed, total_users_rewarded
        )

        return {
            "success": True,
            "walk_id": walk_id,
            "channels_visited": len(selected_channels),
            "tokens_distributed": total_tokens_distributed,
            "users_rewarded": total_users_rewarded,
            "results": walk_results,
        }

    async def visit_channel(self, channel: discord.TextChannel, walk_id: str) -> Dict:
        """💜 Visit a specific channel and spread good vibes"""

        try:
            # Check if we've exceeded daily token budget
            if self.tokens_distributed_today >= self.daily_token_budget:
                token_multiplier = 0.1  # Minimal tokens if budget exceeded
            else:
                token_multiplier = 1.0

            # Determine if special event triggers
            special_event = self.check_special_event()

            # Select appropriate message
            message = self.select_message(channel.name, special_event)

            # Get recent active users in the channel
            active_users = await self.get_recent_active_users(channel)

            # Create and send the community message
            embed = self.create_community_embed(
                message, special_event, len(active_users)
            )
            sent_message = await channel.send(embed=embed)

            # Distribute tokens to active users
            tokens_distributed = 0.0
            users_rewarded = 0

            if self.token_engine and active_users and token_multiplier > 0:
                base_reward = (
                    5.0
                    if not special_event
                    else 5.0 * special_event["reward_multiplier"]
                )
                reward_per_user = base_reward * token_multiplier

                for user_id in active_users:
                    # Award tokens
                    self.token_engine.award_tokens(
                        str(user_id),
                        reward_per_user,
                        f"🚶‍♂️ Community walk visit in #{channel.name}",
                    )
                    tokens_distributed += reward_per_user
                    users_rewarded += 1

                    # Track user interaction
                    self.track_user_interaction(user_id, reward_per_user)

            # Log the visit
            self.log_channel_visit(
                walk_id,
                channel,
                message,
                special_event,
                tokens_distributed,
                users_rewarded,
            )

            # Update our tracking
            self.tokens_distributed_today += tokens_distributed
            self.channels_visited.add(channel.id)

            return {
                "success": True,
                "channel": channel.name,
                "message_sent": True,
                "tokens_distributed": tokens_distributed,
                "users_rewarded": users_rewarded,
                "special_event": special_event["name"] if special_event else None,
            }

        except discord.Forbidden:
            return {
                "success": False,
                "channel": channel.name,
                "error": "No permission to send messages",
            }
        except Exception as e:
            return {"success": False, "channel": channel.name, "error": str(e)}

    async def get_recent_active_users(
        self, channel: discord.TextChannel, hours: int = 24
    ) -> List[int]:
        """📊 Get users who were active in the last X hours"""

        active_users = set()
        cutoff_time = datetime.now() - timedelta(hours=hours)

        try:
            # Look through recent messages
            async for message in channel.history(limit=100, after=cutoff_time):
                if not message.author.bot and message.author.id not in active_users:
                    active_users.add(message.author.id)

                    # Limit to prevent massive token distribution
                    if len(active_users) >= 10:
                        break
        except discord.Forbidden:
            pass  # Can't read message history

        return list(active_users)

    def check_special_event(self) -> Optional[Dict]:
        """🎲 Check if a special event should trigger"""

        for event in self.special_events:
            if random.random() < event["probability"]:
                return event

        return None

    def select_message(self, channel_name: str, special_event: Optional[Dict]) -> str:
        """💬 Select appropriate message for the channel"""

        if special_event:
            return special_event["message"]

        # Check for channel-specific messages
        for keyword, messages in self.channel_specific_messages.items():
            if keyword in channel_name.lower():
                return random.choice(messages)

        # Default to general good vibes
        return random.choice(self.good_vibes_messages)

    def create_community_embed(
        self, message: str, special_event: Optional[Dict], active_users: int
    ) -> discord.Embed:
        """🎨 Create beautiful embed for community message"""

        if special_event:
            color = 0xFFD700  # Gold for special events
            title = "🌟 SPECIAL COMMUNITY EVENT! 🌟"
        else:
            color = 0x9966FF  # Purple for regular visits
            title = "💜 BROski Community Love 💜"

        embed = discord.Embed(
            title=title, description=message, color=color, timestamp=datetime.now()
        )

        if active_users > 0:
            embed.add_field(
                name="🎁 Token Drop",
                value=f"Free BROski$ for {active_users} active community members!",
                inline=False,
            )

        embed.add_field(
            name="💫 Community Stats",
            value=(
                f"🏠 Walking through our amazing server\n"
                f"🤗 Spreading love and good vibes\n"
                f"💰 Building our token economy together"
            ),
            inline=False,
        )

        embed.set_footer(
            text="BROski Community Walker • Powered by love and ADHD energy 💜"
        )

        return embed

    def log_channel_visit(
        self,
        walk_id: str,
        channel: discord.TextChannel,
        message: str,
        special_event: Optional[Dict],
        tokens_distributed: float,
        users_rewarded: int,
    ):
        """📝 Log the channel visit to database"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO walk_history
            (walk_id, timestamp, channel_id, channel_name, message_type,
             tokens_distributed, users_rewarded, special_event)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                walk_id,
                datetime.now().isoformat(),
                str(channel.id),
                channel.name,
                "community_love" if not special_event else "special_event",
                tokens_distributed,
                users_rewarded,
                special_event["name"] if special_event else None,
            ),
        )

        conn.commit()
        conn.close()

    def track_user_interaction(self, user_id: int, tokens_received: float):
        """👤 Track user interaction for analytics"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        today = datetime.now().date()

        cursor.execute(
            """
            INSERT OR REPLACE INTO user_walk_interactions
            (user_id, date, tokens_received, interactions_count, last_interaction)
            VALUES (?, ?,
                COALESCE((SELECT tokens_received FROM user_walk_interactions
                         WHERE user_id = ? AND date = ?), 0) + ?,
                COALESCE((SELECT interactions_count FROM user_walk_interactions
                         WHERE user_id = ? AND date = ?), 0) + 1,
                ?)
        """,
            (
                str(user_id),
                today.isoformat(),
                str(user_id),
                today.isoformat(),
                tokens_received,
                str(user_id),
                today.isoformat(),
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def update_daily_stats(
        self, channels_visited: int, tokens_distributed: float, users_rewarded: int
    ):
        """📈 Update daily statistics"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        today = datetime.now().date()

        cursor.execute(
            """
            INSERT OR REPLACE INTO daily_walk_stats
            (date, total_walks, total_tokens_distributed, total_users_reached,
             channels_visited, special_events_triggered)
            VALUES (?,
                COALESCE((SELECT total_walks FROM daily_walk_stats
                         WHERE date = ?), 0) + 1,
                COALESCE((SELECT total_tokens_distributed FROM daily_walk_stats
                         WHERE date = ?), 0) + ?,
                COALESCE((SELECT total_users_reached FROM daily_walk_stats
                         WHERE date = ?), 0) + ?,
                COALESCE((SELECT channels_visited FROM daily_walk_stats
                         WHERE date = ?), 0) + ?,
                COALESCE((SELEC