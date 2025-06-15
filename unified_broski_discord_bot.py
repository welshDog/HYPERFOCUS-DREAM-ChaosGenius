#!/usr/bin/env python3
"""
🚀💥 UNIFIED BROSKI DISCORD BOT - ULTIMATE EDITION 💥🚀
The ONE bot to rule them all! Combines all features from multiple bot files.
Built for LEGENDARY performance and zero conflicts!

🌌 FEATURES:
- Unified Command System (no conflicts)
- Real-time Performance Monitoring
- Advanced BROski$ Token Economy
- ADHD-Optimized Productivity Tools
- Agent Army Integration
- Welcome & Role Management
- Focus Sessions & Productivity Tracking
- 🚀 NEW: ULTIMATE REMOTE COMMAND CENTER 🚀
"""

import asyncio
import json
import os
import random
import sqlite3
import sys
import subprocess
import psutil
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Enhanced Discord imports with error handling
try:
    import discord
    from discord import app_commands
    from discord.ext import commands, tasks

    DISCORD_AVAILABLE = True
    print("✅ Discord.py loaded successfully!")
except ImportError as e:
    DISCORD_AVAILABLE = False
    print(f"❌ Discord.py not available: {e}")
    print("🔧 Install with: pip install discord.py")

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class UnifiedBROskiBot:
    """🚀 The UNIFIED BROski Discord Bot - All features in one place"""

    def __init__(self):
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        self.guild_id = int(os.getenv("DISCORD_GUILD_ID", "0"))

        print(f"🔑 Token loaded: {'✅ Yes' if self.token else '❌ No'}")
        print(f"🏠 Guild ID: {self.guild_id}")

        # Database setup
        self.db_path = "/root/chaosgenius/unified_broski_bot.db"
        self.initialize_database()

        # Initialize Remote Command Center
        self.orchestrator_path = "/root/chaosgenius/LEGENDARY_SYSTEM_ORCHESTRATOR.py"
        self.empire_active = False

        # Bot setup if Discord is available
        if DISCORD_AVAILABLE and self.token:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True

            self.bot = commands.Bot(
                command_prefix=["!broski ", "!b ", "/"],
                intents=intents,
                help_command=None,
            )

            self.setup_events()
            self.setup_commands()
            self.setup_empire_commands()  # 🚀 NEW: Empire control commands
            self.setup_tasks()
        else:
            self.bot = None
            print("⚠️ Bot will run in test mode")

    def initialize_database(self):
        """💎 Initialize unified database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    discord_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    broski_tokens INTEGER DEFAULT 0,
                    daily_streak INTEGER DEFAULT 0,
                    last_checkin TEXT,
                    total_focus_minutes INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Focus sessions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS focus_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_id TEXT,
                    project TEXT,
                    minutes INTEGER,
                    tokens_earned INTEGER,
                    started_at TEXT,
                    completed_at TEXT,
                    FOREIGN KEY (discord_id) REFERENCES users (discord_id)
                )
            """
            )

            # Server stats table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS server_stats (
                    stat_name TEXT PRIMARY KEY,
                    stat_value INTEGER DEFAULT 0,
                    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()
            conn.close()
            print("✅ Unified database initialized!")

        except Exception as e:
            print(f"❌ Database error: {e}")

    def setup_events(self):
        """🎯 Setup Discord bot events"""

        # Store bot start time
        self.bot_start_time = time.time()

        @self.bot.event
        async def on_ready():
            print(f"🚀 {self.bot.user} is now ONLINE and LEGENDARY!")
            print(f"🏠 Serving {len(self.bot.guilds)} guilds")
            print("🎭 REMOTE COMMAND CENTER ACTIVATED!")

            # Sync slash commands
            try:
                guild = discord.Object(id=self.guild_id) if self.guild_id else None
                synced = await self.bot.tree.sync(guild=guild)
                print(f"✅ Synced {len(synced)} slash commands")
            except Exception as e:
                print(f"❌ Failed to sync commands: {e}")

        @self.bot.event
        async def on_member_join(member):
            """🌟 Welcome new members"""
            welcome_channel = discord.utils.get(
                member.guild.channels, name="🌟-start-here"
            )
            if welcome_channel:
                embed = discord.Embed(
                    title="🚀 Welcome to the BROski Empire!",
                    description=f"Hey {member.mention}! Ready to unlock your LEGENDARY potential?",
                    color=0x00FF88,
                )
                embed.add_field(
                    name="🎯 Getting Started",
                    value="• Use `/checkin` for daily BROski$ tokens\n• Start focus sessions with `/focus`\n• Check your stats with `/stats`\n• 🚀 NEW: Control the empire with `/empire_status`!",
                    inline=False,
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
                await welcome_channel.send(embed=embed)

            # Add new user to database
            self.add_user(str(member.id), member.display_name)

        @self.bot.event
        async def on_message(message):
            """📝 Handle messages"""
            if message.author == self.bot.user:
                return

            # Process commands
            await self.bot.process_commands(message)

    def setup_commands(self):
        """⚡ Setup slash commands"""

        @self.bot.tree.command(
            name="checkin", description="Daily check-in for BROski$ tokens!"
        )
        async def checkin(interaction: discord.Interaction):
            """💰 Daily check-in command"""
            user_id = str(interaction.user.id)
            username = interaction.user.display_name

            result = self.daily_checkin(user_id, username)

            embed = discord.Embed(
                title="🎯 Daily Check-in Complete!",
                color=0x00FF88 if result["success"] else 0xFF4444,
            )

            if result["success"]:
                embed.add_field(
                    name="💰 Tokens Earned",
                    value=f"**+{result['tokens_earned']}** BROski$",
                    inline=True,
                )
                embed.add_field(
                    name="🔥 Streak", value=f"**{result['streak']} days**", inline=True
                )
                embed.add_field(
                    name="💎 Total Tokens",
                    value=f"**{result['total_tokens']}** BROski$",
                    inline=True,
                )
            else:
                embed.description = result["message"]

            await interaction.response.send_message(embed=embed)

        @self.bot.tree.command(
            name="focus", description="Start a focus session and earn tokens!"
        )
        async def focus(
            interaction: discord.Interaction, project: str, minutes: int = 25
        ):
            """🧠 Start focus session"""
            if minutes < 5 or minutes > 120:
                await interaction.response.send_message(
                    "⚠️ Focus sessions must be between 5-120 minutes!", ephemeral=True
                )
                return

            user_id = str(interaction.user.id)
            tokens_to_earn = max(10, minutes // 5 * 2)  # 2 tokens per 5-minute block

            # Start the session
            session_id = self.start_focus_session(
                user_id, project, minutes, tokens_to_earn
            )

            embed = discord.Embed(
                title="🧠 Focus Session Started!",
                description=f"**Project:** {project}\n**Duration:** {minutes} minutes",
                color=0x0099FF,
            )
            embed.add_field(
                name="💰 Potential Reward",
                value=f"{tokens_to_earn} BROski$ tokens",
                inline=True,
            )
            embed.add_field(
                name="⏰ Time Remaining", value=f"{minutes} minutes", inline=True
            )
            embed.set_footer(text=f"Session ID: {session_id}")

            await interaction.response.send_message(embed=embed)

            # Set up timer to award tokens
            await asyncio.sleep(minutes * 60)

            # Award tokens after completion
            self.complete_focus_session(user_id, session_id, tokens_to_earn)

            try:
                completion_embed = discord.Embed(
                    title="🎉 Focus Session Complete!",
                    description=f"Great work on **{project}**!",
                    color=0x00FF88,
                )
                completion_embed.add_field(
                    name="💰 Tokens Earned",
                    value=f"+{tokens_to_earn} BROski$",
                    inline=True,
                )
                await interaction.followup.send(embed=completion_embed)
            except:
                pass  # Channel might be unavailable

        @self.bot.tree.command(name="stats", description="Check your BROski stats!")
        async def stats(interaction: discord.Interaction, user: discord.Member = None):
            """📊 Show user stats"""
            target_user = user or interaction.user
            user_data = self.get_user(str(target_user.id))

            if not user_data:
                await interaction.response.send_message(
                    "❌ User not found in database!", ephemeral=True
                )
                return

            embed = discord.Embed(
                title=f"📊 BROski Stats for {target_user.display_name}", color=0x9C59B6
            )
            embed.set_thumbnail(
                url=target_user.avatar.url if target_user.avatar else None
            )

            embed.add_field(
                name="💰 BROski$ Tokens",
                value=f"**{user_data['broski_tokens']}** tokens",
                inline=True,
            )
            embed.add_field(
                name="🔥 Daily Streak",
                value=f"**{user_data['daily_streak']}** days",
                inline=True,
            )
            embed.add_field(
                name="⭐ Level",
                value=f"**{user_data['level']}** (XP: {user_data['xp']})",
                inline=True,
            )
            embed.add_field(
                name="🧠 Total Focus Time",
                value=f"**{user_data['total_focus_minutes']}** minutes",
                inline=True,
            )
            embed.add_field(
                name="📅 Last Check-in",
                value=user_data["last_checkin"] or "Never",
                inline=True,
            )
            embed.add_field(
                name="📆 Member Since", value=user_data["created_at"][:10], inline=True
            )

            await interaction.response.send_message(embed=embed)

        @self.bot.tree.command(
            name="leaderboard", description="See the top BROski performers!"
        )
        async def leaderboard(interaction: discord.Interaction):
            """🏆 Show leaderboard"""
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT username, broski_tokens, daily_streak, total_focus_minutes
                    FROM users
                    ORDER BY broski_tokens DESC
                    LIMIT 10
                """
                )

                results = cursor.fetchall()
                conn.close()

                if not results:
                    await interaction.response.send_message(
                        "📊 No users found in leaderboard yet!"
                    )
                    return

                embed = discord.Embed(
                    title="🏆 BROski Empire Leaderboard", color=0xF39C12
                )

                leaderboard_text = ""
                medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

                for i, (username, tokens, streak, focus_time) in enumerate(results):
                    medal = medals[i] if i < len(medals) else f"{i+1}."
                    leaderboard_text += f"{medal} **{username}**\n"
                    leaderboard_text += f"   💰 {tokens} tokens | 🔥 {streak} streak | 🧠 {focus_time}min\n\n"

                embed.description = leaderboard_text
                await interaction.response.send_message(embed=embed)

            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Error loading leaderboard: {e}"
                )

        @self.bot.tree.command(name="help", description="Show all available commands!")
        async def help_command(interaction: discord.Interaction):
            """❓ Help command"""
            embed = discord.Embed(
                title="🤖 BROski Bot Commands",
                description="Your ultimate productivity companion!",
                color=0x3498DB,
            )

            embed.add_field(
                name="💰 Economy Commands",
                value="• `/checkin` - Daily token rewards\n• `/stats` - View your progress\n• `/leaderboard` - Top performers",
                inline=False,
            )
            embed.add_field(
                name="🧠 Productivity Commands",
                value="• `/focus <project> [minutes]` - Start focus session\n• `/stats` - Track your focus time",
                inline=False,
            )
            embed.add_field(
                name="🎯 Tips",
                value="• Check in daily for streak bonuses!\n• Longer focus sessions = more tokens\n• Compete on the leaderboard!",
                inline=False,
            )

            await interaction.response.send_message(embed=embed)

    def setup_empire_commands(self):
        """🚀 ULTIMATE REMOTE COMMAND CENTER - Control your digital empire from Discord!"""

        @self.bot.tree.command(
            name="empire_status", description="🚀 Check the status of your LEGENDARY digital empire!"
        )
        async def empire_status(interaction: discord.Interaction):
            """💎 Display complete empire status"""
            await interaction.response.defer()

            try:
                # Check system resources
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')

                # Check if orchestrator is running
                orchestrator_running = self.check_orchestrator_status()

                # Check active agents
                active_agents = self.get_active_agents()

                embed = discord.Embed(
                    title="🚀 EMPIRE STATUS REPORT 🚀",
                    description="Your digital empire at a glance!",
                    color=0x00FF88 if orchestrator_running else 0xFF4444
                )

                # System metrics
                embed.add_field(
                    name="💻 System Resources",
                    value=f"🔥 CPU: {cpu_percent}%\n💾 RAM: {memory.percent}%\n💽 Disk: {disk.percent}%",
                    inline=True
                )

                # Empire status
                empire_status = "🟢 LEGENDARY" if orchestrator_running else "🔴 SLEEPING"
                embed.add_field(
                    name="👑 Empire Status",
                    value=f"Status: {empire_status}\nAgents: {len(active_agents)}\nUptime: {self.get_uptime()}",
                    inline=True
                )

                # Active agents
                if active_agents:
                    agent_list = "\n".join([f"🤖 {agent}" for agent in active_agents[:5]])
                    if len(active_agents) > 5:
                        agent_list += f"\n... and {len(active_agents) - 5} more"
                else:
                    agent_list = "No active agents"

                embed.add_field(
                    name="🤖 Active Agents",
                    value=agent_list,
                    inline=False
                )

                await interaction.followup.send(embed=embed)

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Empire Status Error",
                    description=f"Failed to get empire status: {str(e)}",
                    color=0xFF4444
                )
                await interaction.followup.send(embed=error_embed)

        @self.bot.tree.command(
            name="empire_wake", description="🔥 WAKE UP THE EMPIRE! Activate the System Orchestrator!"
        )
        async def empire_wake(interaction: discord.Interaction):
            """💥 Wake up the digital empire"""
            await interaction.response.defer()

            try:
                if self.check_orchestrator_status():
                    embed = discord.Embed(
                        title="🚀 Empire Already Active!",
                        description="Your empire is already running at LEGENDARY levels!",
                        color=0x00FF88
                    )
                else:
                    # Start the orchestrator
                    result = subprocess.run([
                        "python3", self.orchestrator_path
                    ], capture_output=True, text=True, timeout=10)

                    if result.returncode == 0:
                        embed = discord.Embed(
                            title="🔥 EMPIRE AWAKENED! 🔥",
                            description="Your LEGENDARY System Orchestrator is now ONLINE!",
                            color=0x00FF88
                        )
                        embed.add_field(
                            name="🚀 Status",
                            value="All systems are GO!\nAgent army is mobilizing!\nEmpire is now LEGENDARY!",
                            inline=False
                        )
                        self.empire_active = True
                    else:
                        embed = discord.Embed(
                            title="❌ Empire Wake Failed",
                            description=f"Failed to wake empire: {result.stderr}",
                            color=0xFF4444
                        )

                await interaction.followup.send(embed=embed)

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Empire Wake Error",
                    description=f"Error waking empire: {str(e)}",
                    color=0xFF4444
                )
                await interaction.followup.send(embed=error_embed)

        @self.bot.tree.command(
            name="empire_sleep", description="😴 Put the empire to sleep (careful with this one!)"
        )
        async def empire_sleep(interaction: discord.Interaction):
            """💤 Put empire to sleep"""
            await interaction.response.defer()

            # Confirmation required
            view = EmpireSleepConfirmation()
            embed = discord.Embed(
                title="⚠️ EMPIRE SLEEP CONFIRMATION",
                description="Are you SURE you want to put your LEGENDARY empire to sleep?\n\nThis will stop all active agents and processes!",
                color=0xFFAA00
            )

            await interaction.followup.send(embed=embed, view=view)

        @self.bot.tree.command(
            name="deploy_agent", description="🤖 Deploy a specific agent from your army!"
        )
        @app_commands.describe(
            agent_type="Choose which type of agent to deploy",
            target="Optional target or parameter for the agent"
        )
        @app_commands.choices(agent_type=[
            app_commands.Choice(name="🧙‍♂️ Code Quality Agent", value="code_quality"),
            app_commands.Choice(name="🛡️ Security Fortress Agent", value="security"),
            app_commands.Choice(name="🔍 Project Discovery Agent", value="discovery"),
            app_commands.Choice(name="💰 Business Agent", value="business"),
            app_commands.Choice(name="🧠 Analytics Brain", value="analytics"),
            app_commands.Choice(name="🎯 Focus Engine", value="focus")
        ])
        async def deploy_agent(interaction: discord.Interaction, agent_type: str, target: str = None):
            """🚀 Deploy specific agents"""
            await interaction.response.defer()

            try:
                agent_scripts = {
                    "code_quality": "agent_army_mission_1_code_quality.py",
                    "security": "agent_army_mission_2_security_fortress.py",
                    "discovery": "agent_army_project_discovery.py",
                    "business": "ai_business_agent_sales_strategy.py",
                    "analytics": "broski_advanced_analytics.py",
                    "focus": "broski_focus_engine.py"
                }

                if agent_type not in agent_scripts:
                    raise ValueError(f"Unknown agent type: {agent_type}")

                script_path = f"/root/chaosgenius/{agent_scripts[agent_type]}"

                # Deploy the agent
                cmd = ["python3", script_path]
                if target:
                    cmd.append(target)

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    embed = discord.Embed(
                        title=f"🚀 Agent Deployed Successfully!",
                        description=f"Your {agent_type.replace('_', ' ').title()} Agent is now ACTIVE!",
                        color=0x00FF88
                    )
                    if result.stdout:
                        embed.add_field(
                            name="📋 Agent Report",
                            value=f"```{result.stdout[:800]}...```" if len(result.stdout) > 800 else f"```{result.stdout}```",
                            inline=False
                        )
                else:
                    embed = discord.Embed(
                        title="❌ Agent Deployment Failed",
                        description=f"Failed to deploy {agent_type} agent",
                        color=0xFF4444
                    )
                    if result.stderr:
                        embed.add_field(name="Error", value=f"```{result.stderr[:400]}```", inline=False)

                await interaction.followup.send(embed=embed)

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Agent Deployment Error",
                    description=f"Error deploying agent: {str(e)}",
                    color=0xFF4444
                )
                await interaction.followup.send(embed=error_embed)

        @self.bot.tree.command(
            name="empire_stats", description="📊 Get detailed empire analytics and performance metrics!"
        )
        async def empire_stats(interaction: discord.Interaction):
            """📊 Display detailed empire statistics"""
            await interaction.response.defer()

            try:
                # Get system performance
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                network = psutil.net_io_counters()

                # Get process information
                processes = len(psutil.pids())

                # Get user statistics from database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]

                cursor.execute("SELECT SUM(broski_tokens) FROM users")
                total_tokens = cursor.fetchone()[0] or 0

                cursor.execute("SELECT SUM(total_focus_minutes) FROM users")
                total_focus_minutes = cursor.fetchone()[0] or 0

                cursor.execute("SELECT COUNT(*) FROM focus_sessions")
                total_sessions = cursor.fetchone()[0]

                conn.close()

                # Create detailed stats embed
                embed = discord.Embed(
                    title="📊 EMPIRE ANALYTICS DASHBOARD 📊",
                    description="Your complete empire performance report!",
                    color=0x0099FF
                )

                # System Performance
                embed.add_field(
                    name="💻 System Performance",
                    value=f"🔥 CPU: {cpu_percent}%\n💾 RAM: {memory.percent}%\n💽 Disk: {disk.percent}%\n🔢 Processes: {processes}",
                    inline=True
                )

                # Network Stats
                embed.add_field(
                    name="🌐 Network Activity",
                    value=f"📤 Sent: {self.format_bytes(network.bytes_sent)}\n📥 Received: {self.format_bytes(network.bytes_recv)}",
                    inline=True
                )

                # BROski Economy
                embed.add_field(
                    name="💎 BROski Economy",
                    value=f"👥 Total Users: {total_users}\n💰 Total Tokens: {total_tokens:,}\n⏱️ Focus Hours: {total_focus_minutes // 60:,}h {total_focus_minutes % 60}m\n🎯 Sessions: {total_sessions}",
                    inline=True
                )

                # Empire Health Score
                health_score = self.calculate_empire_health(cpu_percent, memory.percent, disk.percent)
                health_color = "🟢" if health_score > 80 else "🟡" if health_score > 60 else "🔴"

                embed.add_field(
                    name="🏥 Empire Health",
                    value=f"{health_color} Health Score: {health_score}%\nUptime: {self.get_uptime()}\nStatus: {'LEGENDARY' if health_score > 80 else 'GOOD' if health_score > 60 else 'NEEDS ATTENTION'}",
                    inline=False
                )

                await interaction.followup.send(embed=embed)

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Stats Error",
                    description=f"Failed to get empire stats: {str(e)}",
                    color=0xFF4444
                )
                await interaction.followup.send(embed=error_embed)

    def check_orchestrator_status(self):
        """🔍 Check if the System Orchestrator is running"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmdline = proc.info.get('cmdline', [])
                if any('LEGENDARY_SYSTEM_ORCHESTRATOR.py' in str(cmd) for cmd in cmdline):
                    return True
            return False
        except:
            return False

    def get_active_agents(self):
        """🤖 Get list of active agent processes"""
        active_agents = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmdline = proc.info.get('cmdline', [])
                cmdline_str = ' '.join(cmdline) if cmdline else ''

                if any(agent in cmdline_str for agent in [
                    'agent_army', 'broski_', 'ai_business', 'analytics_brain'
                ]):
                    # Extract agent name from cmdline
                    for cmd in cmdline:
                        if any(keyword in cmd for keyword in ['agent', 'broski', 'ai_']):
                            agent_name = cmd.split('/')[-1].replace('.py', '')
                            if agent_name not in active_agents:
                                active_agents.append(agent_name)
                            break
        except:
            pass
        return active_agents

    def get_uptime(self):
        """⏰ Get bot uptime"""
        if hasattr(self, 'bot_start_time'):
            uptime_seconds = time.time() - self.bot_start_time
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        return "Unknown"

    def format_bytes(self, bytes_value):
        """📊 Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f}TB"

    def calculate_empire_health(self, cpu, memory, disk):
        """🏥 Calculate overall empire health score"""
        cpu_score = max(0, 100 - cpu)
        memory_score = max(0, 100 - memory)
        disk_score = max(0, 100 - disk)
        return int((cpu_score + memory_score + disk_score) / 3)


class EmpireSleepConfirmation(discord.ui.View):
    """⚠️ Confirmation view for putting empire to sleep"""

    def __init__(self):
        super().__init__(timeout=30)

    @discord.ui.button(label="💤 Yes, Sleep Empire", style=discord.ButtonStyle.danger)
    async def confirm_sleep(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            # Kill orchestrator processes
            killed_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                cmdline = proc.info.get('cmdline', [])
                if any('LEGENDARY_SYSTEM_ORCHESTRATOR.py' in str(cmd) for cmd in cmdline):
                    proc.terminate()
                    killed_processes.append(f"PID {proc.info['pid']}")

            embed = discord.Embed(
                title="💤 Empire Put to Sleep",
                description="Your empire is now resting. Use `/empire_wake` to reactivate!",
                color=0x888888
            )

            if killed_processes:
                embed.add_field(
                    name="🔄 Processes Stopped",
                    value=f"Stopped {len(killed_processes)} processes",
                    inline=False
                )

            await interaction.response.edit_message(embed=embed, view=None)

        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Sleep Error",
                description=f"Error putting empire to sleep: {str(e)}",
                color=0xFF4444
            )
            await interaction.response.edit_message(embed=error_embed, view=None)

    @discord.ui.button(label="🚀 Cancel, Keep Empire Active", style=discord.ButtonStyle.success)
    async def cancel_sleep(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🚀 Empire Remains Active!",
            description="Your LEGENDARY empire continues to dominate!",
            color=0x00FF88
        )
        await interaction.response.edit_message(embed=embed, view=None)
