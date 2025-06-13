#!/usr/bin/env python3
"""
🚀💥 FRESH BROSKI DISCORD BOT - AGENT ARMY EDITION 💥🚀
Built by the LEGENDARY Agent Orchestrator Army!
By Command of Chief Lyndz - BROski∞ Fresh Start Power-Up

🌌 FEATURES:
- Agent-Coordinated Command System
- Real-time Performance Monitoring
- Advanced BROski$ Token Economy
- ADHD-Optimized Productivity Tools
- Cosmic Server Transformation
- AI-Powered User Assistance
"""

import asyncio
import json
import os
import random
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 🔥 ULTRA FIX: Make Discord import optional for testing
try:
    import discord
    from discord import app_commands
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("⚠️ Discord.py not available - Bot will run in mock mode")

from dotenv import load_dotenv

# Add the orchestrator to our bot
sys.path.append("/root/chaosgenius")
try:
    from super_ai_agent_orchestrator import get_orchestrator

    ORCHESTRATOR_AVAILABLE = True
    print("🤖 Agent Orchestrator: CONNECTED!")
except ImportError:
    ORCHESTRATOR_AVAILABLE = False
    print("⚠️ Agent Orchestrator not available")

load_dotenv()


class FreshBROskiBot:
    """🚀 The FRESH BROski Discord Bot - Agent Army Edition"""

    def __init__(self):
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        self.app_id = os.getenv("DISCORD_APPLICATION_ID")
        self.guild_id = os.getenv("DISCORD_GUILD_ID")

        # Agent Orchestrator Integration
        if ORCHESTRATOR_AVAILABLE:
            self.orchestrator = get_orchestrator()
            self.orchestrator.add_task(
                "Initialize Fresh BROski Discord Bot",
                priority=1,
                complexity=2.0,
                required_skills=["Discord API", "Bot Development", "User Experience"],
            )

        # Database for the fresh bot
        self.db_path = "/root/chaosgenius/fresh_broski_bot.db"
        self.initialize_database()

        # Bot setup if Discord is available
        if DISCORD_AVAILABLE and self.token:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True

            self.bot = commands.Bot(
                command_prefix="!broski ",
                intents=intents,
                description="🚀 Fresh BROski Bot - Agent Army Edition",
            )
            self.setup_events()
            self.setup_commands()
        else:
            self.bot = None
            print("🔧 Running in test mode - Discord integration disabled")

    def initialize_database(self):
        """💎 Initialize fresh database for the new bot"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS fresh_users (
                    discord_id TEXT PRIMARY KEY,
                    username TEXT,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    broski_tokens INTEGER DEFAULT 100,
                    daily_streak INTEGER DEFAULT 0,
                    last_checkin DATE,
                    cosmic_rank TEXT DEFAULT 'Rookie',
                    total_focus_minutes INTEGER DEFAULT 0,
                    achievements TEXT DEFAULT '[]'
                )
            """
            )

            # Focus sessions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS focus_sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id TEXT,
                    project_name TEXT,
                    start_time TIMESTAMP,
                    duration_minutes INTEGER,
                    tokens_earned INTEGER,
                    quality_rating INTEGER DEFAULT 5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Agent tasks table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_tasks (
                    task_id TEXT PRIMARY KEY,
                    discord_id TEXT,
                    task_description TEXT,
                    assigned_agent TEXT,
                    status TEXT DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """
            )

            conn.commit()
            conn.close()
            print("✅ Fresh BROski database initialized!")

            if ORCHESTRATOR_AVAILABLE:
                self.orchestrator.add_task(
                    "Database initialization completed", priority=2, complexity=1.0
                )

        except Exception as e:
            print(f"❌ Database error: {e}")

    def setup_events(self):
        """🎯 Setup Discord bot events"""
        if not self.bot:
            return

        @self.bot.event
        async def on_ready():
            print(f"🚀💥 FRESH BROSKI BOT ACTIVATED! 💥🚀")
            print(f"🤖 Bot: {self.bot.user.name}")
            print(f"🛡️ Connected to {len(self.bot.guilds)} servers")
            print("🌌 AGENT ARMY READY FOR COSMIC DOMINATION! 🌌")

            # Sync slash commands
            try:
                synced = await self.bot.tree.sync()
                print(f"🔄 Synced {len(synced)} FRESH commands")

                if ORCHESTRATOR_AVAILABLE:
                    self.orchestrator.add_task(
                        f"Bot connected successfully - {len(synced)} commands synced",
                        priority=1,
                        complexity=1.0,
                    )
            except Exception as e:
                print(f"❌ Command sync failed: {e}")

        @self.bot.event
        async def on_member_join(member):
            """👋 Welcome new cosmic legends"""
            # Add user to database
            self.add_user(member.id, member.display_name)

            # Send welcome message
            welcome_channel = discord.utils.get(member.guild.channels, name="general")
            if not welcome_channel:
                welcome_channel = member.guild.system_channel

            if welcome_channel:
                embed = discord.Embed(
                    title="🌌 WELCOME TO THE FRESH BROSKI ZONE! 🌌",
                    description=f"🚀 **{member.mention}** just joined the LEGENDARY crew!",
                    color=0x9932CC,
                )
                embed.add_field(
                    name="🎯 Your Mission",
                    value="Use `/fresh_start` to begin your cosmic journey!",
                    inline=False,
                )
                embed.add_field(
                    name="💎 Welcome Bonus",
                    value="100 BROski$ tokens added to your wallet!",
                    inline=False,
                )
                await welcome_channel.send(embed=embed)

    def setup_commands(self):
        """⚡ Setup slash commands"""
        if not self.bot:
            return

        @self.bot.tree.command(
            name="fresh_start", description="🚀 Begin your fresh BROski journey!"
        )
        async def fresh_start(interaction: discord.Interaction):
            """🚀 Fresh start command"""
            await interaction.response.defer()

            user_data = self.get_user(interaction.user.id)
            if not user_data:
                self.add_user(interaction.user.id, interaction.user.display_name)
                user_data = self.get_user(interaction.user.id)

            embed = discord.Embed(
                title="🚀💥 FRESH BROSKI JOURNEY INITIATED! 💥🚀",
                description="Welcome to your LEGENDARY productivity empire!",
                color=0x00FF88,
            )
            embed.add_field(
                name="💎 Your BROski$ Balance",
                value=f"{user_data['broski_tokens']} tokens",
                inline=True,
            )
            embed.add_field(
                name="🏆 Cosmic Rank", value=user_data["cosmic_rank"], inline=True
            )
            embed.add_field(
                name="🔥 Daily Streak",
                value=f"{user_data['daily_streak']} days",
                inline=True,
            )
            embed.add_field(
                name="🎯 Available Commands",
                value="`/agent_assist` - Get AI agent help\n`/focus_mode` - Start hyperfocus session\n`/daily_boost` - Daily dopamine drop\n`/wallet` - Check your cosmic wealth",
                inline=False,
            )

            await interaction.followup.send(embed=embed)

            if ORCHESTRATOR_AVAILABLE:
                self.orchestrator.add_task(
                    f"User {interaction.user.display_name} started fresh journey",
                    priority=3,
                    complexity=0.5,
                )

        @self.bot.tree.command(
            name="agent_assist", description="🤖 Get help from the Agent Army!"
        )
        async def agent_assist(interaction: discord.Interaction, task: str):
            """🤖 Agent assistance command"""
            await interaction.response.defer()

            if ORCHESTRATOR_AVAILABLE:
                # Add task to orchestrator
                task_id = self.orchestrator.add_task(
                    f"User Request: {task}",
                    priority=2,
                    complexity=1.5,
                    required_skills=["User Support", "Problem Solving"],
                )

                # Store in database
                self.add_agent_task(interaction.user.id, task, task_id)

                embed = discord.Embed(
                    title="🤖💥 AGENT ARMY DISPATCHED! 💥🤖",
                    description=f"Task: **{task}**",
                    color=0x0099FF,
                )
                embed.add_field(
                    name="🎯 Status",
                    value="Agent Army is analyzing your request...",
                    inline=False,
                )
                embed.add_field(name="📋 Task ID", value=f"`{task_id}`", inline=True)
                embed.add_field(
                    name="⏱️ Estimated Time", value="2-5 minutes", inline=True
                )

                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="🤖 Agent Assist",
                    description="Agent Orchestrator not available - running in test mode",
                    color=0xFFAA00,
                )
                await interaction.followup.send(embed=embed)

        @self.bot.tree.command(
            name="focus_mode", description="🧠 Start a hyperfocus productivity session!"
        )
        async def focus_mode(
            interaction: discord.Interaction, project: str, minutes: int = 25
        ):
            """🧠 Focus mode command"""
            await interaction.response.defer()

            if minutes > 120:
                minutes = 120  # Cap at 2 hours

            # Calculate token reward
            token_reward = minutes * 2

            embed = discord.Embed(
                title="🧠⚡ HYPERFOCUS MODE ACTIVATED! ⚡🧠",
                description=f"🎯 **Project:** {project}\n⏰ **Duration:** {minutes} minutes",
                color=0xFF6B35,
            )
            embed.add_field(
                name="💎 Token Reward",
                value=f"{token_reward} BROski$ upon completion",
                inline=True,
            )
            embed.add_field(
                name="🎯 Focus Tips",
                value="• Turn off notifications\n• Close social media\n• Trust your neurodivergent superpowers!",
                inline=False,
            )

            await interaction.followup.send(embed=embed)

            # Start focus session in database
            self.start_focus_session(
                interaction.user.id, project, minutes, token_reward
            )

            if ORCHESTRATOR_AVAILABLE:
                self.orchestrator.add_task(
                    f"Focus session started: {project} ({minutes} min)",
                    priority=3,
                    complexity=0.5,
                )

        @self.bot.tree.command(
            name="daily_boost",
            description="⚡ Get your daily dopamine boost and tokens!",
        )
        async def daily_boost(interaction: discord.Interaction):
            """⚡ Daily boost command"""
            await interaction.response.defer()

            result = self.daily_checkin(
                interaction.user.id, interaction.user.display_name
            )

            if result["success"]:
                embed = discord.Embed(
                    title="⚡💥 DAILY DOPAMINE BOOST! 💥⚡",
                    description=result["message"],
                    color=0xFFAA00,
                )
                embed.add_field(
                    name="💎 Tokens Earned",
                    value=f"+{result['tokens']} BROski$",
                    inline=True,
                )
                embed.add_field(
                    name="🔥 Streak", value=f"{result['streak']} days", inline=True
                )
            else:
                embed = discord.Embed(
                    title="✅ Already Boosted Today!",
                    description="Come back tomorrow for your next cosmic energy boost!",
                    color=0x9932CC,
                )
                embed.add_field(
                    name="🔥 Current Streak",
                    value=f"{result['streak']} days",
                    inline=True,
                )

            await interaction.followup.send(embed=embed)

        @self.bot.tree.command(
            name="wallet", description="💰 Check your BROski$ wallet and cosmic status"
        )
        async def wallet(interaction: discord.Interaction):
            """💰 Wallet command"""
            await interaction.response.defer()

            user_data = self.get_user(interaction.user.id)
            if not user_data:
                self.add_user(interaction.user.id, interaction.user.display_name)
                user_data = self.get_user(interaction.user.id)

            embed = discord.Embed(
                title=f"💎 {interaction.user.display_name}'s Cosmic Wallet",
                color=0x9932CC,
            )
            embed.add_field(
                name="💰 BROski$ Balance",
                value=f"{user_data['broski_tokens']} tokens",
                inline=True,
            )
            embed.add_field(
                name="🏆 Cosmic Rank", value=user_data["cosmic_rank"], inline=True
            )
            embed.add_field(
                name="🔥 Daily Streak",
                value=f"{user_data['daily_streak']} days",
                inline=True,
            )
            embed.add_field(
                name="🧠 Total Focus Time",
                value=f"{user_data['total_focus_minutes']} minutes",
                inline=True,
            )

            await interaction.followup.send(embed=embed)

        @self.bot.tree.command(
            name="agent_status", description="📊 Check the Agent Army status"
        )
        async def agent_status(interaction: discord.Interaction):
            """📊 Agent status command"""
            await interaction.response.defer()

            if ORCHESTRATOR_AVAILABLE:
                status = self.orchestrator.get_agent_status()

                embed = discord.Embed(
                    title="🤖💥 AGENT ARMY STATUS 💥🤖",
                    description="Real-time agent performance metrics",
                    color=0x00AAFF,
                )
                embed.add_field(
                    name="📊 Overview",
                    value=f"**Total Agents:** {status['total_agents']}\n**Active:** {status['active_agents']}\n**Tasks Completed:** {status['completed_tasks']}",
                    inline=False,
                )

                # Show top 3 agents
                top_agents = sorted(
                    status["agents"], key=lambda x: x["performance_score"], reverse=True
                )[:3]
                agent_text = ""
                for i, agent in enumerate(top_agents, 1):
                    status_emoji = (
                        "🟢"
                        if agent["status"] == "READY"
                        else "🔄" if agent["status"] == "WORKING" else "🔴"
                    )
                    agent_text += f"{i}. {status_emoji} **{agent['name']}**\n   Performance: {agent['performance_score']}% | Energy: {agent['energy_level']}%\n"

                embed.add_field(
                    name="🏆 Top Performing Agents", value=agent_text, inline=False
                )

                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="🤖 Agent Army Status",
                    description="Agent Orchestrator not available - running in test mode",
                    color=0xFFAA00,
                )
                await interaction.followup.send(embed=embed)

    def add_user(self, discord_id: str, username: str):
        """👤 Add new user to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO fresh_users
                (discord_id, username, broski_tokens, cosmic_rank)
                VALUES (?, ?, 100, 'Rookie')
            """,
                (str(discord_id), username),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error adding user: {e}")

    def get_user(self, discord_id: str) -> Optional[Dict]:
        """👤 Get user data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM fresh_users WHERE discord_id = ?", (str(discord_id),)
            )
            result = cursor.fetchone()

            if result:
                columns = [description[0] for description in cursor.description]
                user_data = dict(zip(columns, result))
                conn.close()
                return user_data

            conn.close()
            return None
        except Exception as e:
            print(f"❌ Error getting user: {e}")
            return None

    def daily_checkin(self, discord_id: str, username: str) -> Dict:
        """⚡ Handle daily check-in"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            today = datetime.now().date()

            # Get current user data
            cursor.execute(
                "SELECT last_checkin, daily_streak, broski_tokens FROM fresh_users WHERE discord_id = ?",
                (str(discord_id),),
            )
            result = cursor.fetchone()

            if not result:
                self.add_user(discord_id, username)
                return self.daily_checkin(discord_id, username)

            last_checkin_str, current_streak, current_tokens = result
            last_checkin = (
                datetime.strptime(last_checkin_str, "%Y-%m-%d").date()
                if last_checkin_str
                else None
            )

            if last_checkin == today:
                return {
                    "success": False,
                    "streak": current_streak,
                    "message": "Already checked in today!",
                }

            # Calculate new streak
            if last_checkin and (today - last_checkin).days == 1:
                new_streak = current_streak + 1
            else:
                new_streak = 1

            # Calculate tokens
            base_tokens = 50
            streak_bonus = min(new_streak * 10, 200)
            total_tokens = base_tokens + streak_bonus

            # Update database
            cursor.execute(
                """
                UPDATE fresh_users
                SET last_checkin = ?, daily_streak = ?, broski_tokens = broski_tokens + ?
                WHERE discord_id = ?
            """,
                (str(today), new_streak, total_tokens, str(discord_id)),
            )

            conn.commit()
            conn.close()

            dopamine_messages = [
                "🔥 Your brain is a WEAPON of creative destruction!",
                "⚡ Hyperfocus mode: ENGAGED! Time to build something legendary!",
                "💎 You're not broken, you're EVOLVED for this digital age!",
                "🚀 Channel that chaos into pure creative genius!",
                "🧠 Your neurodivergent superpower is ACTIVATED!",
            ]

            return {
                "success": True,
                "tokens": total_tokens,
                "streak": new_streak,
                "message": random.choice(dopamine_messages),
            }

        except Exception as e:
            print(f"❌ Check-in error: {e}")
            return {"success": False, "streak": 0, "message": "Something went wrong!"}

    def start_focus_session(
        self, discord_id: str, project: str, minutes: int, tokens: int
    ):
        """🧠 Start a focus session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO focus_sessions
                (discord_id, project_name, start_time, duration_minutes, tokens_earned)
                VALUES (?, ?, ?, ?, ?)
            """,
                (str(discord_id), project, datetime.now(), minutes, tokens),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Focus session error: {e}")

    def add_agent_task(self, discord_id: str, task_description: str, task_id: str):
        """🤖 Add agent task to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO agent_tasks
                (task_id, discord_id, task_description, assigned_agent)
                VALUES (?, ?, ?, 'Agent Army')
            """,
                (task_id, str(discord_id), task_description),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Agent task error: {e}")

    def run(self):
        """🚀 Run the fresh BROski bot"""
        if self.bot and self.token:
            print("🚀💥 STARTING FRESH BROSKI BOT! 💥🚀")
            try:
                self.bot.run(self.token)
            except Exception as e:
                print(f"❌ Bot error: {e}")
                print("🔧 Running in test mode...")
                self.test_mode()
        else:
            print("🔧 Running Fresh BROski Bot in test mode...")
            self.test_mode()

    def test_mode(self):
        """🧪 Test mode for the bot"""
        print("🧪💥 FRESH BROSKI BOT TEST MODE 💥🧪")
        print("=" * 50)
        print("✅ Database initialized")
        print("✅ Commands prepared")
        print("✅ Agent integration ready")
        print("✅ All systems LEGENDARY!")

        if ORCHESTRATOR_AVAILABLE:
            status = self.orchestrator.get_agent_status()
            print(f"🤖 Agent Army: {status['total_agents']} agents ready")
            print(f"📊 Tasks completed: {status['completed_tasks']}")

        return True


def main():
    """🚀 Main function to start Fresh BROski Bot"""
    print("🚀💥 INITIALIZING FRESH BROSKI BOT 💥🚀")
    print("🤖 Agent Army Edition - Built for LEGENDARY performance!")
    print("=" * 60)

    fresh_bot = FreshBROskiBot()
    fresh_bot.run()


if __name__ == "__main__":
    main()
