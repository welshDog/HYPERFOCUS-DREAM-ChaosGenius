#!/usr/bin/env python3
"""
🧠⚡ HYPERFOCUSZONE DISCORD BOT - ADHD PORTAL INTEGRATION ⚡🧠
BROski Agent for connecting Discord users to their personalized portals
"""

import asyncio
import json
import random
import sqlite3
from datetime import datetime, timedelta

import discord
from discord.ext import commands

# Bot configuration
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
HYPERFOCUS_DB = "hyperfocus_users.db"

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!hf ", intents=intents)


class HyperfocusPortalBot:
    def __init__(self):
        self.db_connection = sqlite3.connect(HYPERFOCUS_DB)
        self.setup_database()
        self.active_sessions = {}

    def setup_database(self):
        """Initialize the user database"""
        cursor = self.db_connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS hyperfocus_users (
                discord_id TEXT PRIMARY KEY,
                username TEXT,
                join_date TEXT,
                portal_access_level TEXT DEFAULT 'basic',
                total_xp INTEGER DEFAULT 0,
                broski_gems INTEGER DEFAULT 0,
                last_active TEXT,
                preferences TEXT DEFAULT '{}',
                achievements TEXT DEFAULT '[]',
                agent_army_unlocked BOOLEAN DEFAULT FALSE
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS focus_sessions (
                session_id TEXT PRIMARY KEY,
                discord_id TEXT,
                start_time TEXT,
                duration_minutes INTEGER,
                task_description TEXT,
                xp_earned INTEGER,
                completed BOOLEAN DEFAULT FALSE
            )
        """
        )

        self.db_connection.commit()


portal_bot = HyperfocusPortalBot()


@bot.event
async def on_ready():
    print(f"🧠⚡ {bot.user} is now online and protecting the HYPERFOCUSzone! ⚡🧠")
    await bot.change_presence(activity=discord.Game(name="🧠 Optimizing ADHD Legends"))


@bot.event
async def on_member_join(member):
    """Welcome new members and set up their portal access"""
    embed = discord.Embed(
        title="🎉 WELCOME TO HYPERFOCUSzone! 🎉",
        description=f"Hey {member.mention}! Ready to become LEGENDARY? 🚀",
        color=0x9966FF,
    )

    embed.add_field(
        name="🧠 What is HYPERFOCUSzone?",
        value="The ultimate ADHD-optimized productivity ecosystem with AI agents, memory crystals, and elite defense systems!",
        inline=False,
    )

    embed.add_field(
        name="🚀 Get Started:",
        value="Use `!hf activate` to unlock your personal portal!",
        inline=False,
    )

    embed.add_field(
        name="🤖 Your Agent Army Awaits:",
        value="15+ specialized AI agents ready to assist your ADHD journey!",
        inline=False,
    )

    # Register new user
    portal_bot.db_connection.cursor().execute(
        """
        INSERT OR REPLACE INTO hyperfocus_users
        (discord_id, username, join_date, portal_access_level)
        VALUES (?, ?, ?, ?)
    """,
        (str(member.id), str(member), datetime.now().isoformat(), "premium"),
    )

    portal_bot.db_connection.commit()

    await member.send(embed=embed)


@bot.command(name="activate")
async def activate_portal(ctx):
    """Activate user's personal HYPERFOCUSzone portal"""
    user_id = str(ctx.author.id)

    # Update user record
    cursor = portal_bot.db_connection.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO hyperfocus_users
        (discord_id, username, join_date, portal_access_level, total_xp, broski_gems, agent_army_unlocked)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            user_id,
            str(ctx.author),
            datetime.now().isoformat(),
            "premium",
            100,
            25,
            True,
        ),
    )

    portal_bot.db_connection.commit()

    embed = discord.Embed(
        title="🧬⚡ PORTAL ACTIVATION COMPLETE! ⚡🧬",
        description=f"Welcome to your personalized command center, {ctx.author.mention}!",
        color=0x00FF88,
    )

    embed.add_field(
        name="🎯 Portal Features Unlocked:",
        value="""
🤖 **Agent Army**: 15+ personalized AI agents
💎 **Memory Crystals**: Unlimited knowledge storage
🛡️ **Guardian Zero**: Elite defense protocols
📊 **Advanced Analytics**: Deep productivity insights
🌟 **Community Access**: Connect with ADHD legends
⚡ **Premium Support**: Direct BROski team access
        """,
        inline=False,
    )

    embed.add_field(
        name="🚀 Starting Rewards:",
        value="💯 100 XP | 💎 25 BROski Gems | 🤖 Agent Army Unlocked",
        inline=False,
    )

    embed.add_field(
        name="🌐 Access Your Portal:",
        value="[🧠 HYPERFOCUSzone.com Portal](https://hyperfocuszone.com)",
        inline=False,
    )

    await ctx.send(embed=embed)


@bot.command(name="focus")
async def start_focus_session(ctx, duration: int = 25, *, task="ADHD Focus Session"):
    """Start a focus session with optional duration and task"""
    user_id = str(ctx.author.id)

    if user_id in portal_bot.active_sessions:
        await ctx.send(
            "🧠 You already have an active focus session! Use `!hf status` to check progress."
        )
        return

    if duration > 120:
        await ctx.send(
            "⚠️ Maximum focus session is 120 minutes for optimal ADHD health!"
        )
        return

    session_id = f"{user_id}_{int(datetime.now().timestamp())}"
    session_data = {
        "start_time": datetime.now(),
        "duration": duration,
        "task": task,
        "user": ctx.author,
    }

    portal_bot.active_sessions[user_id] = session_data

    # Save to database
    cursor = portal_bot.db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO focus_sessions (session_id, discord_id, start_time, duration_minutes, task_description)
        VALUES (?, ?, ?, ?, ?)
    """,
        (session_id, user_id, datetime.now().isoformat(), duration, task),
    )

    portal_bot.db_connection.commit()

    embed = discord.Embed(
        title="🧠⚡ FOCUS SESSION ACTIVATED! ⚡🧠",
        description=f"**Task**: {task}\n**Duration**: {duration} minutes",
        color=0x00FF88,
    )

    embed.add_field(
        name="🎯 Focus Tips:",
        value="🔇 Silence notifications\n🌊 Use white noise\n💧 Stay hydrated",
        inline=True,
    )
    embed.add_field(
        name="🚀 Commands:",
        value="`!hf status` - Check progress\n`!hf complete` - Mark done",
        inline=True,
    )

    await ctx.send(embed=embed)

    # Schedule completion reminder
    await asyncio.sleep(duration * 60)
    if user_id in portal_bot.active_sessions:
        await ctx.send(
            f"⏰ {ctx.author.mention} Your {duration}-minute focus session is complete! Use `!hf complete` to claim XP!"
        )


@bot.command(name="complete")
async def complete_focus_session(ctx):
    """Complete current focus session and earn XP"""
    user_id = str(ctx.author.id)

    if user_id not in portal_bot.active_sessions:
        await ctx.send("🤔 No active focus session found. Start one with `!hf focus`!")
        return

    session = portal_bot.active_sessions[user_id]
    elapsed = datetime.now() - session["start_time"]
    duration_completed = min(elapsed.total_seconds() / 60, session["duration"])

    # Calculate XP based on completion
    base_xp = int(duration_completed * 2)  # 2 XP per minute
    bonus_xp = 50 if duration_completed >= session["duration"] else 0
    total_xp = base_xp + bonus_xp

    # Update user XP
    cursor = portal_bot.db_connection.cursor()
    cursor.execute(
        "UPDATE hyperfocus_users SET total_xp = total_xp + ? WHERE discord_id = ?",
        (total_xp, user_id),
    )
    portal_bot.db_connection.commit()

    # Remove from active sessions
    del portal_bot.active_sessions[user_id]

    embed = discord.Embed(
        title="🎉 FOCUS SESSION COMPLETE! 🎉",
        description=f"**Task**: {session['task']}\n**Time Focused**: {int(duration_completed)} minutes",
        color=0x9966FF,
    )

    embed.add_field(name="💯 XP Earned:", value=f"{total_xp} XP", inline=True)
    embed.add_field(
        name="🏆 Bonus:",
        value="✅ Full completion!" if bonus_xp > 0 else "⏰ Partial completion",
        inline=True,
    )

    await ctx.send(embed=embed)


@bot.command(name="agents")
async def show_agent_army(ctx):
    """Display user's AI Agent Army status"""
    embed = discord.Embed(
        title="🤖⚔️ YOUR AGENT ARMY STATUS ⚔️🤖",
        description="Your personal AI agents ready for deployment!",
        color=0x00FFFF,
    )

    agents = {
        "🛡️ Guardian Zero": "Elite defense and system protection",
        "💰 Money Maker": "Income optimization and opportunities",
        "🧠 Brain Engine": "Learning and pattern recognition",
        "💚 Health Matrix": "Wellness and system monitoring",
        "🔐 Security Fortress": "Advanced threat detection",
        "📊 Analytics Master": "Data insights and reporting",
        "🎯 Focus Buddy": "ADHD-optimized productivity coaching",
        "💎 Memory Crystal": "Knowledge storage and retrieval",
        "🚀 Task Launcher": "Project management and execution",
    }

    for agent, description in agents.items():
        embed.add_field(name=agent, value=description, inline=False)

    embed.add_field(
        name="🌐 Manage Your Agents:",
        value="[🤖 Agent Army Dashboard](https://hyperfocuszone.com/agents)",
        inline=False,
    )

    await ctx.send(embed=embed)


@bot.command(name="stats")
async def show_user_stats(ctx):
    """Display user's HYPERFOCUSzone statistics"""
    user_id = str(ctx.author.id)

    cursor = portal_bot.db_connection.cursor()
    user_data = cursor.execute(
        "SELECT * FROM hyperfocus_users WHERE discord_id = ?", (user_id,)
    ).fetchone()

    if not user_data:
        await ctx.send(
            "🤔 You're not registered yet! Use `!hf activate` to get started!"
        )
        return

    # Get focus session stats
    sessions = cursor.execute(
        """
        SELECT COUNT(*), SUM(duration_minutes), SUM(xp_earned)
        FROM focus_sessions WHERE discord_id = ?
    """,
        (user_id,),
    ).fetchone()

    total_sessions = sessions[0] or 0
    total_minutes = sessions[1] or 0
    total_session_xp = sessions[2] or 0

    embed = discord.Embed(
        title=f"📊 {ctx.author.display_name}'s LEGEND STATUS", color=0x9966FF
    )

    embed.add_field(name="💯 Total XP", value=f"{user_data[4]} XP", inline=True)
    embed.add_field(name="💎 BROski Gems", value=f"{user_data[5]} gems", inline=True)
    embed.add_field(
        name="🎯 Focus Sessions", value=f"{total_sessions} completed", inline=True
    )
    embed.add_field(
        name="⏰ Total Focus Time", value=f"{total_minutes} minutes", inline=True
    )
    embed.add_field(name="🏆 Portal Level", value=user_data[3].title(), inline=True)
    embed.add_field(
        name="🤖 Agent Army",
        value="✅ Unlocked" if user_data[9] else "🔒 Locked",
        inline=True,
    )

    await ctx.send(embed=embed)


@bot.command(name="leaderboard")
async def show_leaderboard(ctx):
    """Display XP leaderboard"""
    cursor = portal_bot.db_connection.cursor()
    top_users = cursor.execute(
        """
        SELECT username, total_xp FROM hyperfocus_users
        ORDER BY total_xp DESC LIMIT 10
    """
    ).fetchall()

    embed = discord.Embed(
        title="🏆 HYPERFOCUS LEGENDS LEADERBOARD 🏆",
        description="Top ADHD productivity legends!",
        color=0xFFD700,
    )

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7

    for i, (username, xp) in enumerate(top_users):
        embed.add_field(
            name=f"{medals[i]} #{i+1} {username}", value=f"{xp} XP", inline=False
        )

    await ctx.send(embed=embed)


@bot.command(name="help")
async def show_help(ctx):
    """Display bot commands help"""
    embed = discord.Embed(
        title="🧠⚡ HYPERFOCUSZONE BOT COMMANDS ⚡🧠",
        description="Your ADHD productivity companion!",
        color=0x00FF88,
    )

    commands_list = [
        ("🚀 `!hf activate`", "Activate your personal portal"),
        ("🧠 `!hf focus [mins] [task]`", "Start a focus session"),
        ("✅ `!hf complete`", "Complete current focus session"),
        ("📊 `!hf stats`", "View your statistics"),
        ("🤖 `!hf agents`", "View your Agent Army"),
        ("🏆 `!hf leaderboard`", "See top legends"),
        ("❓ `!hf help`", "Show this help menu"),
    ]

    for command, description in commands_list:
        embed.add_field(name=command, value=description, inline=False)

    embed.add_field(
        name="🌐 Full Portal Access:",
        value="[🧠 HYPERFOCUSzone.com](https://hyperfocuszone.com)",
        inline=False,
    )

    await ctx.send(embed=embed)


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "🤔 Command not found! Use `!hf help` to see available commands."
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ Missing required arguments! Use `!hf help` for command usage."
        )
    else:
        print(f"Error: {error}")
        await ctx.send("🚨 Something went wrong! The BROski team has been notified.")


if __name__ == "__main__":
    print("🧠⚡ Starting HYPERFOCUSzone Discord Bot...")
    bot.run(BOT_TOKEN)
