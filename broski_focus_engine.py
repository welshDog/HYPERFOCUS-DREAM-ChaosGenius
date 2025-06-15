#!/usr/bin/env python3
"""
🧠🔥 BROSKI FOCUS ENGINE - BODY DOUBLING + POMODORO SYSTEM 🔥🧠
ADHD-Optimized Focus Sessions with Social Accountability & BROski$ Rewards
By Command of Chief Lyndz - NEUROSPICY FAM UNITE!

🌟 FEATURES:
- /start-focus → Start pomodoro with XP + BROski$ rewards
- /join-focus → Join active focus sessions
- /set-goal → State your task (displayed to others)
- Auto-matching users in voice channels or threads
- Streak bonuses and achievement system
- Real-time session tracking and encouragement
"""

import asyncio
import json
import random
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set

import discord
from discord.ext import commands, tasks

# Import BROski$ token system
sys.path.append("/root/chaosgenius")

try:
    from ai_modules.broski.token_engine import BROskiTokenEngine
    TOKEN_ENGINE_AVAILABLE = True
except ImportError:
    print("⚠️ Token engine not available - Focus Engine will run without rewards")
    TOKEN_ENGINE_AVAILABLE = False


class BroskiFocusEngine:
    """🧠 ADHD-Optimized Focus Session Manager"""

    def __init__(self):
        self.db_path = "/root/chaosgenius/broski_focus_sessions.db"
        
        # Initialize token engine if available
        if TOKEN_ENGINE_AVAILABLE:
            self.token_engine = BROskiTokenEngine()
        else:
            self.token_engine = None

        # Active sessions tracking
        self.active_sessions: Dict[str, Dict] = {}
        self.session_participants: Dict[str, Set[str]] = {}
        self.user_goals: Dict[str, str] = {}

        # Reward multipliers
        self.base_reward = 15.0  # Base BROski$ for completing 25min session
        self.streak_multiplier = 1.2  # 20% bonus per consecutive day
        self.group_bonus = 1.5  # 50% bonus for group sessions

        # Pomodoro settings
        self.work_duration = 25 * 60  # 25 minutes
        self.break_duration = 5 * 60  # 5 minutes
        self.long_break_duration = 15 * 60  # 15 minutes

        self.init_database()

        print("🧠🔥 BROSKI FOCUS ENGINE ACTIVATED! 🔥🧠")
        print("💜 Ready to boost neurospicy focus sessions!")

    def init_database(self):
        """📊 Initialize focus session database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Focus sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS focus_sessions (
                session_id TEXT PRIMARY KEY,
                creator_id TEXT NOT NULL,
                goal TEXT,
                start_time DATETIME,
                end_time DATETIME,
                duration_minutes INTEGER,
                participants TEXT,
                status TEXT DEFAULT 'active',
                session_type TEXT DEFAULT 'pomodoro',
                voice_channel_id TEXT,
                thread_id TEXT,
                rewards_distributed BOOLEAN DEFAULT FALSE
            )
        """)

        # User focus stats
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_focus_stats (
                user_id TEXT PRIMARY KEY,
                total_sessions INTEGER DEFAULT 0,
                completed_sessions INTEGER DEFAULT 0,
                total_focus_minutes INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                last_session_date DATE,
                total_rewards_earned REAL DEFAULT 0.0,
                favorite_goal_tags TEXT DEFAULT '[]'
            )
        """)

        # Session achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS focus_achievements (
                user_id TEXT,
                achievement_id TEXT,
                earned_date DATETIME,
                reward_amount REAL,
                PRIMARY KEY (user_id, achievement_id)
            )
        """)

        conn.commit()
        conn.close()

    async def start_focus_session(self, user_id: str, username: str, 
                                 guild: Optional[discord.Guild],
                                 goal: str = "", duration: int = 25) -> Dict:
        """🚀 Start a new focus session"""

        # Check if user already has active session
        if self.has_active_session(user_id):
            return {
                "success": False,
                "message": ("🔥 You already have an active focus session! "
                           "Use `/join-focus` to continue or `/end-focus`.")
            }

        # Generate session ID
        session_id = f"focus_{user_id}_{int(time.time())}"

        # Create session data
        session_data = {
            "session_id": session_id,
            "creator_id": user_id,
            "creator_username": username,
            "goal": goal or "🎯 General focus session",
            "start_time": datetime.now(),
            "duration_minutes": duration,
            "participants": {user_id},
            "status": "active",
            "session_type": "pomodoro" if duration == 25 else "custom",
            "voice_channel_id": None,
            "thread_id": None
        }

        # Store in memory and database
        self.active_sessions[session_id] = session_data
        self.session_participants[session_id] = {user_id}
        self.user_goals[user_id] = goal or "🎯 General focus session"

        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO focus_sessions
            (session_id, creator_id, goal, start_time, duration_minutes,
             participants, status, session_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, user_id, goal, datetime.now().isoformat(),
            duration, json.dumps([user_id]), "active", 
            session_data["session_type"]
        ))
        conn.commit()
        conn.close()

        # Try to create voice channel or thread for the session
        if guild:
            try:
                await self.setup_session_space(guild, session_data)
            except Exception as e:
                print(f"⚠️ Couldn't create session space: {e}")

        return {
            "success": True,
            "session_id": session_id,
            "message": f"🔥 Focus session started! **{goal}** - {duration} min",
            "session_data": session_data
        }

    async def join_focus_session(self, user_id: str, 
                                session_id: Optional[str] = None) -> Dict:
        """🤝 Join an existing focus session"""

        # If no session specified, find active sessions to join
        if not session_id:
            available_sessions = self.get_available_sessions()
            if not available_sessions:
                return {
                    "success": False,
                    "message": ("🔍 No active focus sessions to join! "
                               "Start one with `/start-focus`")
                }

            # Auto-join the most recent session
            session_id = available_sessions[0]["session_id"]

        if session_id not in self.active_sessions:
            return {
                "success": False,
                "message": "❌ Session not found or already ended!"
            }

        # Add user to session
        session = self.active_sessions[session_id]
        session["participants"].add(user_id)
        self.session_participants[session_id].add(user_id)

        # Update database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        participants_list = list(session["participants"])
        cursor.execute("""
            UPDATE focus_sessions
            SET participants = ?
            WHERE session_id = ?
        """, (json.dumps(participants_list), session_id))
        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": f"🤝 Joined focus session: **{session['goal']}**",
            "session_data": session,
            "participant_count": len(session["participants"])
        }

    async def set_user_goal(self, user_id: str, goal: str) -> Dict:
        """🎯 Set user's current focus goal"""
        self.user_goals[user_id] = goal

        # If user has active session, update it
        for session_id, session in self.active_sessions.items():
            if user_id in session["participants"]:
                if user_id == session["creator_id"]:
                    session["goal"] = goal
                    # Update database
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE focus_sessions
                        SET goal = ?
                        WHERE session_id = ?
                    """, (goal, session_id))
                    conn.commit()
                    conn.close()
                break

        return {
            "success": True,
            "message": f"🎯 Goal set: **{goal}**"
        }

    async def complete_focus_session(self, user_id: str, 
                                   session_id: Optional[str] = None) -> Dict:
        """✅ Complete a focus session and distribute rewards"""

        # Find user's active session if not specified
        if not session_id:
            session_id = self.get_user_active_session(user_id)
            if not session_id:
                return {
                    "success": False,
                    "message": "❌ No active focus session found!"
                }

        if session_id not in self.active_sessions:
            return {
                "success": False,
                "message": "❌ Session not found!"
            }

        session = self.active_sessions[session_id]

        # Calculate session duration
        start_time = session["start_time"]
        end_time = datetime.now()
        actual_duration = (end_time - start_time).total_seconds() / 60
        target_duration = session["duration_minutes"]

        # Determine completion percentage
        completion_percentage = min(100, 
                                  (actual_duration / target_duration) * 100)

        # Calculate rewards for all participants
        rewards_data = []
        for participant_id in session["participants"]:
            reward_amount = self.calculate_session_reward(
                participant_id, completion_percentage, 
                len(session["participants"])
            )

            if reward_amount > 0 and self.token_engine:
                # Award tokens
                self.token_engine.award_tokens(
                    participant_id,
                    reward_amount,
                    f"🧠 Focus session: {session['goal'][:50]}"
                )

                rewards_data.append({
                    "user_id": participant_id,
                    "reward": reward_amount,
                    "completion": completion_percentage
                })

                # Update user stats
                self.update_user_stats(participant_id, actual_duration, True)

        # Mark session as completed
        session["status"] = "completed"
        session["end_time"] = end_time

        # Update database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE focus_sessions
            SET status = ?, end_time = ?, rewards_distributed = TRUE
            WHERE session_id = ?
        """, ("completed", end_time.isoformat(), session_id))
        conn.commit()
        conn.close()

        # Remove from active sessions
        del self.active_sessions[session_id]
        del self.session_participants[session_id]

        return {
            "success": True,
            "message": (f"🎉 Focus session completed! "
                       f"{completion_percentage:.0f}% of target duration"),
            "rewards": rewards_data,
            "actual_duration": actual_duration,
            "target_duration": target_duration
        }

    def calculate_session_reward(self, user_id: str, 
                               completion_percentage: float,
                               participant_count: int) -> float:
        """💰 Calculate BROski$ reward for focus session"""

        # Base reward scaled by completion
        reward = self.base_reward * (completion_percentage / 100)

        # Minimum completion for rewards (50%)
        if completion_percentage < 50:
            return 0

        # Group session bonus
        if participant_count > 1:
            reward *= self.group_bonus

        # Streak bonus
        streak = self.get_user_streak(user_id)
        if streak > 0:
            streak_bonus = min(streak * 0.1, 2.0)  # Max 200% bonus
            reward *= (1 + streak_bonus)

        # Random bonus for good luck
        if random.random() < 0.1:  # 10% chance
            reward *= 1.5

        return round(reward, 1)

    def get_user_streak(self, user_id: str) -> int:
        """📈 Get user's current focus streak"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT current_streak FROM user_focus_stats
            WHERE user_id = ?
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else 0

    def update_user_stats(self, user_id: str, duration_minutes: float, 
                         completed: bool):
        """📊 Update user focus statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        today = datetime.now().date()

        # Get current stats
        cursor.execute("""
            SELECT * FROM user_focus_stats WHERE user_id = ?
        """, (user_id,))
        stats = cursor.fetchone()

        if stats:
            # Update existing stats
            total_sessions = stats[1] + 1
            completed_sessions = stats[2] + (1 if completed else 0)
            total_minutes = stats[3] + int(duration_minutes)
            current_streak = stats[4]
            best_streak = stats[5]
            last_session_date = (datetime.fromisoformat(stats[6]).date() 
                                if stats[6] else None)

            # Update streak
            if completed:
                if last_session_date == today - timedelta(days=1):
                    current_streak += 1
                elif last_session_date == today:
                    pass  # Same day, no change
                else:
                    current_streak = 1  # Reset streak

                best_streak = max(best_streak, current_streak)

            cursor.execute("""
                UPDATE user_focus_stats
                SET total_sessions = ?, completed_sessions = ?,
                    total_focus_minutes = ?, current_streak = ?,
                    best_streak = ?, last_session_date = ?
                WHERE user_id = ?
            """, (total_sessions, completed_sessions, total_minutes,
                  current_streak, best_streak, today.isoformat(), user_id))
        else:
            # Create new stats
            cursor.execute("""
                INSERT INTO user_focus_stats
                (user_id, total_sessions, completed_sessions, 
                 total_focus_minutes, current_streak, best_streak, 
                 last_session_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, 1, 1 if completed else 0, int(duration_minutes),
                  1 if completed else 0, 1 if completed else 0, 
                  today.isoformat()))

        conn.commit()
        conn.close()

    def has_active_session(self, user_id: str) -> bool:
        """Check if user has an active focus session"""
        for session in self.active_sessions.values():
            if user_id in session["participants"]:
                return True
        return False

    def get_user_active_session(self, user_id: str) -> Optional[str]:
        """Get user's active session ID"""
        for session_id, session in self.active_sessions.items():
            if user_id in session["participants"]:
                return session_id
        return None

    def get_available_sessions(self) -> List[Dict]:
        """Get list of available sessions to join"""
        return [
            {
                "session_id": session_id,
                "goal": session["goal"],
                "creator": session["creator_username"],
                "participants": len(session["participants"]),
                "duration": session["duration_minutes"],
                "elapsed": int((datetime.now() - 
                              session["start_time"]).total_seconds() / 60)
            }
            for session_id, session in self.active_sessions.items()
            if session["status"] == "active"
        ]

    async def setup_session_space(self, guild: discord.Guild, 
                                 session_data: Dict):
        """🎙️ Create voice channel or thread for focus session"""
        try:
            # Try to create a temporary voice channel
            category = discord.utils.get(guild.categories, name="FOCUS ZONE")
            if not category:
                # Create focus category if it doesn't exist
                category = await guild.create_category("🧠 FOCUS ZONE")

            # Create voice channel for session
            channel_name = f"🔥 {session_data['goal'][:30]}"
            voice_channel = await guild.create_voice_channel(
                name=channel_name,
                category=category,
                user_limit=10,  # Max 10 people per focus session
                reason="BROski Focus Session"
            )

            session_data["voice_channel_id"] = str(voice_channel.id)

            # Update database with channel info
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE focus_sessions
                SET voice_channel_id = ?
                WHERE session_id = ?
            """, (str(voice_channel.id), session_data["session_id"]))
            conn.commit()
            conn.close()

        except discord.Forbidden:
            print("⚠️ No permission to create voice channels")
        except Exception as e:
            print(f"⚠️ Error creating session space: {e}")

    def get_user_stats(self, user_id: str) -> Dict:
        """📊 Get comprehensive user focus statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM user_focus_stats WHERE user_id = ?
        """, (user_id,))
        stats = cursor.fetchone()

        if not stats:
            return {
                "total_sessions": 0,
                "completed_sessions": 0,
                "completion_rate": 0,
                "total_hours": 0,
                "current_streak": 0,
                "best_streak": 0
            }

        completion_rate = (stats[2] / stats[1] * 100) if stats[1] > 0 else 0
        total_hours = stats[3] / 60

        conn.close()

        return {
            "total_sessions": stats[1],
            "completed_sessions": stats[2],
            "completion_rate": round(completion_rate, 1),
            "total_hours": round(total_hours, 1),
            "current_streak": stats[4],
            "best_streak": stats[5]
        }


class BroskiFocusCommands(commands.Cog):
    """🧠 Discord commands for the Focus Engine"""

    def __init__(self, bot):
        self.bot = bot
        self.focus_engine = BroskiFocusEngine()
        self.session_timers.start()

    @discord.app_commands.command(
        name="start-focus",
        description="🔥 Start a focus session with BROski$ rewards!"
    )
    @discord.app_commands.describe(
        goal="What are you focusing on? (e.g., 'Study for exam')",
        duration="Session duration in minutes (default: 25)"
    )
    async def start_focus(self, interaction: discord.Interaction,
                         goal: str = "", duration: int = 25):
        """Start a new focus session"""
        user_id = str(interaction.user.id)
        username = interaction.user.display_name

        result = await self.focus_engine.start_focus_session(
            user_id, username, interaction.guild, goal, duration
        )

        if result["success"]:
            embed = discord.Embed(
                title="🔥 FOCUS SESSION STARTED! 🔥",
                description=f"**{result['session_data']['goal']}**",
                color=0xFF6B35
            )
            embed.add_field(
                name="⏱️ Duration",
                value=f"{duration} minutes",
                inline=True
            )
            embed.add_field(
                name="💰 Potential Reward",
                value=f"Up to {self.focus_engine.base_reward} BROski$",
                inline=True
            )
            embed.add_field(
                name="🤝 Body Doubling",
                value="Others can join with `/join-focus`",
                inline=False
            )
            embed.set_footer(text="Stay focused! Complete 50%+ for rewards 🎯")

            await interaction.response.send_message(embed=embed)

            # Send encouragement after 10 minutes
            await asyncio.sleep(600)  # 10 minutes
            if self.focus_engine.has_active_session(user_id):
                await interaction.followup.send(
                    f"🔥 Keep going {username}! You're doing amazing! 💜",
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                result["message"], ephemeral=True
            )

    @discord.app_commands.command(
        name="join-focus",
        description="🤝 Join an active focus session for body doubling!"
    )
    async def join_focus(self, interaction: discord.Interaction):
        """Join an existing focus session"""
        user_id = str(interaction.user.id)

        # Get available sessions
        available = self.focus_engine.get_available_sessions()

        if not available:
            embed = discord.Embed(
                title="🔍 No Active Sessions",
                description="No focus sessions available to join right now.",
                color=0x9966FF
            )
            embed.add_field(
                name="💡 Start Your Own",
                value="Use `/start-focus` to create a new session!",
                inline=False
            )
            await interaction.response.send_message(embed=embed, 
                                                   ephemeral=True)
            return

        # Join the most recent session
        result = await self.focus_engine.join_focus_session(user_id)

        if result["success"]:
            embed = discord.Embed(
                title="🤝 JOINED FOCUS SESSION!",
                description=f"**{result['session_data']['goal']}**",
                color=0x00D4AA
            )
            embed.add_field(
                name="👥 Participants",
                value=f"{result['participant_count']} focused friends",
                inline=True
            )
            embed.add_field(
                name="💰 Group Bonus",
                value="+50% BROski$ rewards!",
                inline=True
            )

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                result["message"], ephemeral=True
            )

    @discord.app_commands.command(
        name="set-goal",
        description="🎯 Set your current focus goal"
    )
    @discord.app_commands.describe(
        goal="What are you working on right now?"
    )
    async def set_goal(self, interaction: discord.Interaction, goal: str):
        """Set user's focus goal"""
        user_id = str(interaction.user.id)

        await self.focus_engine.set_user_goal(user_id, goal)

        embed = discord.Embed(
            title="🎯 GOAL SET!",
            description=f"**{goal}**",
            color=0xFFD700
        )
        embed.set_footer(text="You've got this! Stay focused! 💜")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.app_commands.command(
        name="end-focus",
        description="✅ Complete your focus session and claim rewards!"
    )
    async def end_focus(self, interaction: discord.Interaction):
        """Complete a focus session"""
        user_id = str(interaction.user.id)

        result = await self.focus_engine.complete_focus_session(user_id)

        if result["success"]:
            embed = discord.Embed(
                title="🎉 FOCUS SESSION COMPLETE! 🎉",
                description="Amazing work! You stayed focused!",
                color=0x00FF88
            )

            # Show completion stats
            completion = (result["rewards"][0]["completion"] 
                         if result["rewards"] else 0)
            reward = (result["rewards"][0]["reward"] 
                     if result["rewards"] else 0)

            embed.add_field(
                name="📊 Completion",
                value=f"{completion:.0f}% of target",
                inline=True
            )
            embed.add_field(
                name="💰 BROski$ Earned",
                value=f"+{reward} tokens!",
                inline=True
            )
            embed.add_field(
                name="⏱️ Time Focused",
                value=f"{result['actual_duration']:.0f} minutes",
                inline=True
            )

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                result["message"], ephemeral=True
            )

    @discord.app_commands.command(
        name="focus-stats",
        description="📊 View your focus session statistics"
    )
    async def focus_stats(self, interaction: discord.Interaction):
        """Show user's focus statistics"""
        user_id = str(interaction.user.id)
        stats = self.focus_engine.get_user_stats(user_id)

        embed = discord.Embed(
            title=f"📊 {interaction.user.display_name}'s Focus Stats",
            color=0x9966FF
        )

        embed.add_field(
            name="🎯 Sessions Completed",
            value=f"{stats['completed_sessions']}/{stats['total_sessions']}",
            inline=True
        )
        embed.add_field(
            name="📈 Success Rate",
            value=f"{stats['completion_rate']:.1f}%",
            inline=True
        )
        embed.add_field(
            name="⏰ Total Focus Time",
            value=f"{stats['total_hours']:.1f} hours",
            inline=True
        )
        embed.add_field(
            name="🔥 Current Streak",
            value=f"{stats['current_streak']} days",
            inline=True
        )
        embed.add_field(
            name="🏆 Best Streak",
            value=f"{stats['best_streak']} days",
            inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.app_commands.command(
        name="focus-leaderboard",
        description="🏆 See the top focused members!"
    )
    async def focus_leaderboard(self, interaction: discord.Interaction):
        """Show focus session leaderboard"""
        conn = sqlite3.connect(self.focus_engine.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, completed_sessions, total_focus_minutes, 
                   current_streak
            FROM user_focus_stats
            ORDER BY completed_sessions DESC, total_focus_minutes DESC
            LIMIT 10
        """)

        results = cursor.fetchall()
        conn.close()

        if not results:
            await interaction.response.send_message(
                ("🔍 No focus sessions completed yet! "
                 "Be the first with `/start-focus`"),
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🏆 FOCUS CHAMPIONS LEADERBOARD 🏆",
            description="The most dedicated focused members!",
            color=0xFFD700
        )

        for i, (user_id, sessions, minutes, streak) in enumerate(
                results[:5], 1):
            try:
                user = self.bot.get_user(int(user_id))
                username = (user.display_name if user 
                           else f"User {user_id[:8]}")
            except Exception:
                username = f"User {user_id[:8]}"

            medal = ["🥇", "🥈", "🥉", "🏅", "🏅"][i-1]
            hours = minutes / 60

            embed.add_field(
                name=f"{medal} #{i} {username}",
                value=(f"**{sessions}** sessions • **{hours:.1f}h** "
                      f"focused • **{streak}** day streak"),
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @tasks.loop(minutes=5)  # Check every 5 minutes
    async def session_timers(self):
        """Background task to manage session timers and send updates"""
        current_time = datetime.now()

        for session_id, session in list(
                self.focus_engine.active_sessions.items()):
            elapsed = ((current_time - 
                       session["start_time"]).total_seconds() / 60)
            target = session["duration_minutes"]

            # Send progress updates
            if elapsed >= target * 0.5 and not session.get("halfway_sent"):
                session["halfway_sent"] = True
                # Send halfway encouragement
                for participant_id in session["participants"]:
                    try:
                        user = self.bot.get_user(int(participant_id))
                        if user:
                            await user.send(
                                f"🔥 Halfway there! Keep focusing on: "
                                f"**{session['goal']}** 💜"
                            )
                    except Exception:
                        pass

            # Auto-complete very long sessions (2x target duration)
            elif elapsed >= target * 2:
                await self.focus_engine.complete_focus_session(
                    session["creator_id"], session_id
                )


async def setup(bot):
    """Setup function for Discord bot"""
    await bot.add_cog(BroskiFocusCommands(bot))


# Export classes
__all__ = ["BroskiFocusEngine", "BroskiFocusCommands"]
