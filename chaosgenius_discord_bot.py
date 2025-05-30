import discord
from discord.ext import commands, tasks
import sqlite3
import requests
import json
import os
import subprocess
from datetime import datetime, timedelta
import asyncio
import logging
from typing import Optional, Dict, Any, List
import random
import re
from dotenv import load_dotenv
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Add BROski AI integration
import sys
sys.path.append('/workspaces/HYPERFOCUS-DREAM-ChaosGenius')
from ai_modules.broski.broski_core import BROskiCore, BROskiResponse

# 🪙 Add BROski$ Token Economy integration
try:
    from ai_modules.broski.token_engine import BROskiTokenEngine
    from ai_modules.broski.token_commands import BROskiTokenCommands
    TOKENS_AVAILABLE = True
    logger.info("🪙 BROski$ Token Economy loaded successfully!")
except ImportError as e:
    logger.warning(f"⚠️ BROski$ Token system not available: {e}")
    TOKENS_AVAILABLE = False

# 🔐 Load environment variables securely
load_dotenv()

# 🚨 SECURE Bot Configuration
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    print("\ud83d\udea8 WARNING: DISCORD_BOT_TOKEN not found in environment variables!")
    print("\ud83d\udd0e Running in DEV MODE: Discord bot will not connect, but commands can be simulated.")
    TOKEN = None  # Dev mode: do not exit, allow script to run for local testing

# 📝 Enhanced logging for production - FIXED ENCODING ISSUE
# Ensure logs directory exists
logs_dir = Path("logs")
logs_dir.mkdir(parents=True, exist_ok=True)

# Configure logging with rotation
log_file = logs_dir / 'discord_bot.log'
rotating_handler = RotatingFileHandler(log_file, maxBytes=2*1024*1024, backupCount=3, encoding='utf-8', errors='replace')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        rotating_handler,
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ChaosGeniusBot')

# Log security status
logger.info("🔐 Security: Environment variables loaded successfully")
logger.info(f"🔐 Security: Token loaded: {'✅' if TOKEN else '❌'}")

# 🧠 Intents for full ChaosGenius integration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# 🧪 Bot setup with ChaosGenius prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# 🗄️ Database connection to ChaosGenius with enhanced error handling


def get_db_connection():
    try:
        conn = sqlite3.connect('chaosgenius.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


# 🌐 Dashboard API endpoints with health check
DASHBOARD_URL = "http://localhost:5000"


async def check_dashboard_health():
    """Check if dashboard is responding"""
    try:
        response = requests.get(f"{DASHBOARD_URL}/api/status", timeout=3)
        return response.status_code == 200
    except:
        return False

# 🧠 ULTRA MODE BROSKI X SYSTEMS (Phase 5+)

# 🎯 User Profile System for Dopamine Tracking
user_profiles = {}


def init_user_profile(user_id):
    """Initialize user profile with dopamine tracking"""
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            "dopamine": 75,
            "focus_level": "Balanced",
            "hypergems": 0,
            "daily_streak": 0,
            "last_active": datetime.now(),
            "quests_completed": 0,
            "mood_history": [],
            "preferences": {}
        }
    return user_profiles[user_id]


# 🧠 1. Broski's Dopamine Scanner™
MOOD_PATTERNS = {
    "tired": ["tired", "burnt out", "exhausted", "drained", "can't focus", "lost"],
    "excited": ["idea", "project", "help me build", "excited", "inspired", "motivated"],
    "bored": ["bored", "nothing to do", "stuck", "unmotivated"],
    "stressed": ["overwhelmed", "anxious", "too much", "stressed", "panic"],
    "creative": ["creating", "building", "making", "designing", "coding"]
}

MOOD_RESPONSES = {
    "tired": [
        "🛌 **Permission to Rest Granted!** Your brain needs recharge time. Here's a cozy meme: 😴",
        "⚡ Energy detected at low levels. Activating rest protocol... 🧘‍♀️",
        "🧠 Your neurodivergent brain is telling you something important. Listen to it! 💜"
    ],
    "excited": [
        "🚀 **IDEA ENERGY DETECTED!** Ready to `/hyperdump` that beautiful chaos?",
        "💡 Your excitement is contagious! Want to start a focus thread? 🧵",
        "🔥 That's the hyperfocus energy we love! Channel it into something epic!"
    ],
    "bored": [
        "🎯 **Dopamine Quest Incoming!** Share one weird skill you have in 60 seconds!",
        "🍄 Quick creativity spark: Name something purple that makes you happy!",
        "⚡ Boredom = Opportunity! Try the `/quest` command for instant dopamine!"
    ],
    "stressed": [
        "🫂 Overwhelm detected. Take 3 deep breaths with me... 1... 2... 3... 💙",
        "🧠 Your ADHD brain is just processing a lot right now. That's normal! 🌟",
        "⛑️ Stress protocol activated: What's ONE tiny thing you can do right now?"
    ],
    "creative": [
        "🎨 **CREATIVE MODE ACTIVATED!** The zone is calling you! ✨",
        "🧬 Your neurodivergent creativity is showing! Keep flowing! 🌊",
        "👑 That's the creative energy that builds empires! Keep going!"
    ]
}


def detect_mood(message_content):
    """Detect mood from message content"""
    content_lower = message_content.lower()

    for mood, patterns in MOOD_PATTERNS.items():
        for pattern in patterns:
            if pattern in content_lower:
                return mood
    return None


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 🧠 Dopamine Scanner in action
    detected_mood = detect_mood(message.content)

    # Avoid responding to short messages
    if detected_mood and len(message.content) > 20:
        user_profile = init_user_profile(message.author.id)

        # Update mood history
        user_profile["mood_history"].append({
            "mood": detected_mood,
            "timestamp": datetime.now().isoformat(),
            "channel": message.channel.name
        })

        # Keep only last 10 mood entries
        if len(user_profile["mood_history"]) > 10:
            user_profile["mood_history"] = user_profile["mood_history"][-10:]

        # Random chance to respond (30% to avoid spam)
        if random.random() < 0.3:
            response = random.choice(MOOD_RESPONSES[detected_mood])

            # Add user-specific touches
            if detected_mood == "excited":
                response += f"\n*BROski senses {message.author.mention}'s hyperfocus energy! 🧠⚡*"
            elif detected_mood == "tired":
                response += f"\n*Sending gentle vibes to {message.author.mention} 💜*"

            await message.channel.send(response)

            # Award HyperGems for engagement
            user_profile["hypergems"] += 1

            # Log mood detection
            logger.info(
                f"Mood detected: {detected_mood} for {message.author.name}")

    await bot.process_commands(message)

# 🔔 2. Focus Bar HUD™ (Daily Status Overlay)


@bot.command()
async def hud(ctx, user: discord.Member = None):
    """Show daily energy HUD"""
    target_user = user or ctx.author
    profile = init_user_profile(target_user.id)

    # Calculate dynamic stats
    hours_since_active = (
        datetime.now() - profile["last_active"]).total_seconds() / 3600
    dopamine_level = max(20, profile["dopamine"] - int(hours_since_active * 2))

    # Determine focus level
    focus_levels = ["Scattered", "Balanced",
                    "Focused", "HyperSpicy", "ULTRA ZONE"]
    focus_index = min(4, max(0, int(dopamine_level / 20)))
    current_focus = focus_levels[focus_index]

    # Create HUD embed
    embed = discord.Embed(
        title=f"🧠 BROski X Focus HUD - {target_user.display_name}",
        description="*Real-time neurodivergent energy analysis*",
        color=0xff6b35 if dopamine_level > 60 else 0xffaa00 if dopamine_level > 30 else 0x666666
    )

    # Energy bars
    dopamine_bar = "█" * int(dopamine_level / 10) + \
        "░" * (10 - int(dopamine_level / 10))
    embed.add_field(
        name="⚡ Dopamine Level",
        value=f"`{dopamine_bar}` {dopamine_level}%",
        inline=True
    )

    embed.add_field(name="🎯 Focus Level", value=current_focus, inline=True)
    embed.add_field(name="💎 HyperGems", value=str(
        profile["hypergems"]), inline=True)

    # Idea overload calculation
    recent_moods = [m for m in profile["mood_history"] if
                    datetime.fromisoformat(m["timestamp"]) > datetime.now() - timedelta(hours=6)]
    idea_overload = "High" if len(recent_moods) > 5 else "Medium" if len(
        recent_moods) > 2 else "Low"

    embed.add_field(name="🧩 Idea Overload", value=idea_overload, inline=True)
    embed.add_field(name="🔥 Daily Streak",
                    value=f"{profile['daily_streak']} days", inline=True)
    embed.add_field(name="🏆 Quests Done", value=str(
        profile["quests_completed"]), inline=True)

    # Suggested actions
    if dopamine_level < 40:
        suggestion = "🧘 Take a break or try a dopamine quest"
    elif dopamine_level > 80:
        suggestion = "🚀 Perfect for hyperfocus mode - build something!"
    else:
        suggestion = "⚡ Good energy for balanced productivity"

    embed.add_field(name="🎯 Suggested Action", value=suggestion, inline=False)

    # Recent mood trend
    if recent_moods:
        mood_trend = " → ".join([m["mood"].title() for m in recent_moods[-3:]])
        embed.add_field(name="📈 Recent Mood Flow",
                        value=mood_trend, inline=False)

    embed.set_footer(
        text=f"Last updated: {datetime.now().strftime('%H:%M')} | BROski X Ultra Systems")

    await ctx.send(embed=embed)

# 📅 3. Daily ChaosGenius Rituals


@tasks.loop(hours=24)
async def daily_rituals():
    """Send daily ritual messages"""
    for guild in bot.guilds:
        # Find general or announcements channel
        channel = discord.utils.get(guild.channels, name="general") or \
            discord.utils.get(guild.channels, name="announcements") or \
            guild.text_channels[0] if guild.text_channels else None

        if not channel:
            continue

        weekday = datetime.now().weekday()
        ritual_messages = {
            0: "🍄 **Monday Mind Melt!** Drop your wildest weekly idea below! No judgment, pure chaos welcome! 🧠✨",
            1: "🔧 **Tuesday Toolkit!** Share one tool, app, or hack that saved your ADHD brain this week! 🛠️",
            2: "🧘 **Wednesday Wellness Check!** How are we feeling? React with your energy: 🔥⚡🧘😴",
            3: "🎯 **Thursday Thoughts!** What's one tiny win you had today? I'll add it to the victory vault! 🏆",
            4: "🎉 **Friday Flex!** What was your biggest win this week? Time to celebrate! 🎊",
            5: "🌈 **Saturday Scatter!** Share something that made you smile today! Wholesome vibes only! 😊",
            6: "🔮 **Sunday Prep!** What's one thing you're excited about for next week? Future-you will thank you! ✨"
        }

        message = ritual_messages.get(
            weekday, "🧠 **Daily ChaosGenius Check-in!** How's your beautiful brain doing today?")

        try:
            await channel.send(message)
            logger.info(f"Daily ritual sent to {guild.name}")
        except Exception as e:
            logger.error(f"Failed to send daily ritual to {guild.name}: {e}")


@daily_rituals.before_loop
async def before_daily_rituals():
    await bot.wait_until_ready()

# 📂 4. Hyperfocus Folder System™


@bot.command()
async def hyperdump(ctx, *, brain_dump):
    """AI-powered idea categorization and sorting"""
    user_profile = init_user_profile(ctx.author.id)

    # Simple AI categorization (can be enhanced with OpenAI API)
    categories = {
        "creative": ["art", "design", "music", "creative", "draw", "paint", "video", "content"],
        "strategy": ["business", "plan", "strategy", "goal", "launch", "market", "money", "growth"],
        "tech": ["code", "app", "website", "tool", "ai", "bot", "script", "program", "tech"],
        "life": ["health", "routine", "habit", "self", "mental", "wellness", "life", "personal"]
    }

    dump_lower = brain_dump.lower()
    detected_category = "general"

    for category, keywords in categories.items():
        if any(keyword in dump_lower for keyword in keywords):
            detected_category = category
            break

    # Create categorized response
    category_info = {
        "creative": {"emoji": "🎨", "channel": "#art-and-expression", "color": 0xff69b4},
        "strategy": {"emoji": "🧠", "channel": "#hyperfocus-hub-app-projekt", "color": 0x9c27b0},
        "tech": {"emoji": "🧰", "channel": "#ai-zone", "color": 0x00ff41},
        "life": {"emoji": "🌱", "channel": "#personal-growth-and-self-awareness", "color": 0x4caf50},
        "general": {"emoji": "💭", "channel": "#general", "color": 0x607d8b}
    }

    cat_info = category_info[detected_category]

    embed = discord.Embed(
        title=f"{cat_info['emoji']} Brain Dump Categorized!",
        description=f"**Your beautiful chaos has been sorted:**\n\n{brain_dump}",
        color=cat_info['color']
    )

    embed.add_field(
        name="🗂️ Category Detected",
        value=f"{detected_category.title()} {cat_info['emoji']}",
        inline=True
    )
    embed.add_field(
        name="📍 Suggested Channel",
        value=cat_info['channel'],
        inline=True
    )
    embed.add_field(
        name="💎 HyperGems Earned",
        value="+3",
        inline=True
    )

    # Award HyperGems and update profile
    user_profile["hypergems"] += 3
    user_profile["last_active"] = datetime.now()

    # Add quick action buttons (as text for now)
    quick_actions = {
        "creative": "Try: `/quest creative` for inspiration boost!",
        "strategy": "Try: `/focus-timer 25` for deep work session!",
        "tech": "Try: `/tools` for helpful resources!",
        "life": "Try: `/motivate` for neurodivergent power boost!"
    }

    embed.add_field(
        name="⚡ Quick Action",
        value=quick_actions.get(
            detected_category, "Try: `/status` to check your energy!"),
        inline=False
    )

    embed.set_footer(
        text=f"Dumped by {ctx.author.display_name} | BROski X Hyperfocus System")

    await ctx.send(embed=embed)

    # Log the brain dump
    await log_discord_activity("brain_dump", ctx.author.name, f"Category: {detected_category}")

# 🧩 5. Dopamine Quests™ – Mini Games + XP
QUEST_TYPES = {
    "social": [
        "Make someone smile in a random channel",
        "Share a wholesome meme or GIF",
        "Give someone a genuine compliment",
        "Share what you're grateful for today"
    ],
    "creative": [
        "Describe your dream creative space in 3 emojis",
        "Share a photo of something purple nearby",
        "Write a haiku about your current mood",
        "Draw your energy level as a simple doodle"
    ],
    "focus": [
        "Share one tool that helped you focus today",
        "Set a 10-minute timer and organize one small area",
        "Write down 3 things you want to accomplish tomorrow",
        "Share your current hyperfocus subject"
    ],
    "chaos": [
        "Share the weirdest skill you have",
        "Describe your personality as a mythical creature",
        "Share what your ADHD superpower is",
        "Tell us about a random thing that fascinated you recently"
    ]
}


@bot.command()
async def quest(ctx, quest_type: Optional[str] = None):
    """Get a dopamine quest for instant engagement"""
    user_profile = init_user_profile(ctx.author.id)

    if not quest_type:
        available_types = ", ".join(QUEST_TYPES.keys())
        await ctx.send(f"🎯 **Quest Types Available:** {available_types}\nOr just use `/quest` for a random one!")
        return

    # Get random quest
    if quest_type.lower() == "random" or quest_type.lower() not in QUEST_TYPES:
        quest_type = random.choice(list(QUEST_TYPES.keys()))

    quest = random.choice(QUEST_TYPES[quest_type.lower()])

    # Calculate rewards
    gem_reward = random.randint(2, 5)

    embed = discord.Embed(
        title="🎯 Dopamine Quest Activated!",
        description=f"**Your Mission:** {quest}",
        color=0xff6b35
    )

    embed.add_field(name="🎮 Quest Type", value=quest_type.title(), inline=True)
    embed.add_field(name="💎 Reward",
                    value=f"{gem_reward} HyperGems", inline=True)
    embed.add_field(name="⏰ Time Limit", value="No pressure!", inline=True)

    embed.add_field(
        name="📝 How to Complete",
        value="Just do the quest and react with ✅ when done!\nBROski will detect your awesome energy!",
        inline=False
    )

    embed.set_footer(
        text=f"Quest for {ctx.author.display_name} | Complete for HyperGems!")

    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")

    # Store quest info for completion tracking
    user_profile["active_quest"] = {
        "message_id": message.id,
        "quest": quest,
        "reward": gem_reward,
        "type": quest_type
    }


@bot.event
async def on_reaction_add(reaction, user):
    """Handle quest completion via reactions"""
    if user == bot.user:
        return

    user_profile = init_user_profile(user.id)

    # Check if this is a quest completion
    if ("active_quest" in user_profile and
        reaction.message.id == user_profile["active_quest"]["message_id"] and
            str(reaction.emoji) == "✅"):

        quest_info = user_profile["active_quest"]

        # Award rewards - Legacy HyperGems + New BROski$ Tokens!
        user_profile["hypergems"] += quest_info["reward"]
        user_profile["quests_completed"] += 1
        user_profile["dopamine"] = min(100, user_profile["dopamine"] + 10)

        # 🪙 Award BROski$ tokens for quest completion!
        if TOKENS_AVAILABLE and token_engine:
            try:
                # Award BROski$ based on quest type
                token_reward_map = {
                    'social': 8,
                    'creative': 10,
                    'focus': 15,
                    'chaos': 5
                }
                token_reward = token_reward_map.get(quest_info.get('type', 'social'), 8)

                token_result = token_engine.award_tokens(
                    str(user.id),
                    token_reward,
                    f"Quest completion: {quest_info['quest'][:50]}..."
                )

                if token_result['status'] == 'success':
                    quest_info['broski_tokens_earned'] = token_reward
                    logger.info(f"Awarded {token_reward} BROski$ to {user.name} for quest completion")
            except Exception as e:
                logger.error(f"Failed to award BROski$ tokens: {e}")

        # Remove active quest
        del user_profile["active_quest"]

        # Send completion message
        completion_embed = discord.Embed(
            title="🏆 Quest Complete!",
            description=f"**Awesome work, {user.display_name}!**\nYour neurodivergent brain just earned some sweet rewards!",
            color=0x4caf50
        )

        completion_embed.add_field(name="💎 HyperGems Earned", value=str(
            quest_info["reward"]), inline=True)
        completion_embed.add_field(
            name="⚡ Dopamine Boost", value="+10", inline=True)
        completion_embed.add_field(name="🎯 Total Quests", value=str(
            user_profile["quests_completed"]), inline=True)

        await reaction.message.channel.send(embed=completion_embed)

        # Log quest completion
        logger.info(f"Quest completed by {user.name}: {quest_info['quest']}")

# 🔐 6. Admin Overdrive Panel™ (Only for Server Admins)


@bot.command()
@commands.has_permissions(administrator=True)
async def broski_intel(ctx):
    """Admin-only community intelligence dashboard"""

    # Gather community analytics
    guild = ctx.guild
    total_members = len(guild.members)
    online_members = len(
        [m for m in guild.members if m.status != discord.Status.offline])

    # Analyze user profiles
    top_contributors = sorted(
        [(uid, profile["hypergems"])
         for uid, profile in user_profiles.items()],
        key=lambda x: x[1], reverse=True
    )[:3]

    # Channel activity analysis
    channel_activity = {}
    for channel in guild.text_channels:
        try:
            messages = []
            async for message in channel.history(limit=50):
                if message.created_at > datetime.now() - timedelta(hours=24):
                    messages.append(message)
            channel_activity[channel.name] = len(messages)
        except:
            channel_activity[channel.name] = 0

    # Sort channels by activity
    most_active_channels = sorted(
        channel_activity.items(), key=lambda x: x[1], reverse=True)[:3]

    # Mood analysis
    recent_moods = []
    for profile in user_profiles.values():
        recent_moods.extend([
            m for m in profile.get("mood_history", [])
            if datetime.fromisoformat(m["timestamp"]) > datetime.now() - timedelta(hours=6)
        ])

    mood_counts = {}
    for mood_entry in recent_moods:
        mood = mood_entry["mood"]
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

    # Create intel report
    embed = discord.Embed(
        title="📊 HYPERFOCUS ZONE LIVE STATUS",
        description="*Admin Intelligence Dashboard - BROski X Ultra*",
        color=0x9c27b0
    )

    embed.add_field(
        name="👥 Community Health",
        value=f"**Total Members:** {total_members}\n**Online Now:** {online_members}\n**Activity Rate:** {int((online_members/total_members)*100)}%",
        inline=True
    )

    if top_contributors:
        contributor_text = "\n".join([
            f"{i+1}. <@{uid}> ({gems} 💎)"
            for i, (uid, gems) in enumerate(top_contributors)
        ])
        embed.add_field(name="💎 Top Contributors",
                        value=contributor_text, inline=True)

    if most_active_channels:
        channel_text = "\n".join([
            f"#{name}: {count} msgs"
            for name, count in most_active_channels
        ])
        embed.add_field(name="🔥 Most Active Channels",
                        value=channel_text, inline=True)

    if mood_counts:
        mood_text = "\n".join([
            f"{mood.title()}: {count}"
            for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True)
        ])
        embed.add_field(name="🧠 Community Mood (6h)",
                        value=mood_text, inline=True)

    # Energy recommendations
    total_dopamine = sum(profile.get("dopamine", 75)
                         for profile in user_profiles.values())
    avg_dopamine = total_dopamine / len(user_profiles) if user_profiles else 75

    if avg_dopamine < 50:
        suggestion = "🚨 Low community energy - Consider focus event or meme blast"
    elif avg_dopamine > 80:
        suggestion = "🚀 High energy detected - Perfect for community building!"
    else:
        suggestion = "⚡ Balanced community energy - Steady engagement recommended"

    embed.add_field(name="🎯 Suggested Actions", value=suggestion, inline=False)

    embed.add_field(
        name="⚡ Quick Commands",
        value="`/community-boost` | `/focus-event` | `/meme-blast` | `/energy-check`",
        inline=False
    )

    embed.set_footer(
        text=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M')} | BROski X Admin Panel")

    await ctx.send(embed=embed)

# 🏓 Enhanced ping with empire stats


@bot.command()
async def ping(ctx):
    try:
        # Get empire status from dashboard
        response = requests.get(
            f"{DASHBOARD_URL}/api/empire-status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="🏓 ChaosGenius Engine Status",
                description=f"🏰 Empire Health: {data.get('empire_health', 'Unknown')}",
                color=0x00ff00
            )
            embed.add_field(name="🤖 Bot Latency",
                            value=f"{round(bot.latency * 1000)}ms", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("🏓 Pong! (Dashboard offline)")
    except:
        await ctx.send("🏓 Pong! (Empire status unavailable)")

# 🛡️ Rate limiting decorator
user_cooldowns = {}


def rate_limit(seconds):
    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            user_id = ctx.author.id
            now = datetime.now()

            if user_id in user_cooldowns:
                time_diff = (now - user_cooldowns[user_id]).seconds
                if time_diff < seconds:
                    await ctx.send(f"⏱️ Please wait {seconds - time_diff} seconds before using this command again.")
                    return

            user_cooldowns[user_id] = now
            return await func(ctx, *args, **kwargs)
        return wrapper
    return decorator

# 🔥 Ultra Mode - Launch AI Squad


@bot.command()
@rate_limit(30)  # 30 second cooldown
async def ultra(ctx, squad_type: str = "business_creator"):
    logger.info(f"Ultra command triggered by {ctx.author.name}")
    await ctx.send("🚀 **ULTRA MODE ACTIVATED!** Launching AI Squad...")

    try:
        # Map squad types to actual script paths
        script_map = {
            "business_creator": "Setup & Deploy/setup1",
            "advanced_analyzer": "Setup & Deploy/setup2",
            "ultra_mode": "Setup & Deploy/Ultra Mode upgades"
        }

        script_path = script_map.get(squad_type, "Setup & Deploy/setup1")

        # Check if script exists before running
        if not os.path.exists(script_path):
            await ctx.send(f"⚠️ Script not found: {script_path}\nRunning simulated AI Squad instead...")
            # Simulate AI Squad execution
            await simulate_ai_squad(ctx, squad_type)
            return

        # Send request to dashboard API
        payload = {
            "type": squad_type,
            "energy_level": "high",
            "focus": "discord_triggered"
        }
        response = requests.post(
            f"{DASHBOARD_URL}/api/launch-ai-squad", json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="🤖 AI Squad Deployed!",
                description=data.get('message', 'Squad launched successfully'),
                color=0xff6b35
            )
            embed.add_field(name="🧠 Energy Boost", value=data.get(
                'energy_boost', ''), inline=False)
            embed.add_field(name="⏱️ ETA", value=data.get(
                'estimated_completion', ''), inline=True)
            await ctx.send(embed=embed)
            # Log successful deployment
            await log_discord_activity(f"ultra_mode_{squad_type}", ctx.author.name, "AI Squad deployed")
        else:
            await ctx.send("❌ AI Squad deployment failed. Check dashboard status.")
    except Exception as e:
        logger.error(f"Ultra Mode error: {e}")
        await ctx.send(f"🚨 Ultra Mode error: Falling back to local simulation...")
        await simulate_ai_squad(ctx, squad_type)


async def simulate_ai_squad(ctx, squad_type):
    """Simulate AI Squad execution when scripts aren't available"""
    await ctx.send("🧠 **AI Squad Neural Simulation Active...**")

    squad_responses = {
        "business_creator": {
            "title": "🚀 Business Creator Squad Deployed!",
            "description": "Neural agents analyzing your empire...",
            "fields": [
                ("🎯 Vision Agent", "Mission clarity: ENHANCED", True),
                ("💡 Ideas Agent", "Product concepts: OPTIMIZED", True),
                ("📦 Offer Agent", "Revenue streams: ACTIVATED", True),
                ("🎭 Brand Agent", "Identity matrix: STRENGTHENED", True),
                ("🧲 Audience Agent", "Community targeting: LOCKED", True),
                ("💬 Pitch Agent", "Narrative power: AMPLIFIED", True),
                ("💼 Structure Agent", "Growth framework: ESTABLISHED", True)
            ]
        },
        "advanced_analyzer": {
            "title": "🔍 Advanced Analyzer Squad Active!",
            "description": "Deep system analysis in progress...",
            "fields": [
                ("🛠️ Code Analyzer", "Optimization opportunities: FOUND", True),
                ("📊 Performance Scout", "Bottlenecks: IDENTIFIED", True),
                ("🔒 Security Auditor", "Vulnerabilities: PATCHED", True),
                ("📈 Growth Predictor", "Scaling paths: MAPPED", True)
            ]
        },
        "ultra_mode": {
            "title": "⚡ ULTRA MODE ENGAGED!",
            "description": "Maximum neural capacity activated...",
            "fields": [
                ("🧠 Hyperfocus Engine", "Peak performance: ACHIEVED", True),
                ("🚀 Quantum Accelerator", "Time dilation: ACTIVE", True),
                ("💎 Chaos Converter", "Disorder → Order: COMPLETE", True),
                ("🌟 Empire Builder", "Dominance mode: ENGAGED", True)
            ]
        }
    }

    squad_config = squad_responses.get(
        squad_type, squad_responses["business_creator"])

    embed = discord.Embed(
        title=squad_config["title"],
        description=squad_config["description"],
        color=0x9c27b0
    )

    for field_name, field_value, inline in squad_config["fields"]:
        embed.add_field(name=field_name, value=field_value, inline=inline)

    embed.add_field(
        name="🎯 Status", value="Neural simulation complete! Ready for real deployment.", inline=False)
    embed.set_footer(
        text="ChaosGenius AI Squad - Neurodivergent Excellence Engine")

    await ctx.send(embed=embed)

    # Log simulated deployment
    await log_discord_activity(f"simulated_{squad_type}", ctx.author.name, "AI Squad simulation completed")

# 🛠️ Create Product - Direct integration with logging


@bot.command()
async def create(ctx, *, product_idea):
    await ctx.send("🛠️ **CAPTURING PRODUCT IDEA...**")

    try:
        payload = {
            "name": product_idea[:50],  # Truncate for filename
            "description": product_idea,
            "energy_level": "high",
            "source": f"Discord - {ctx.author.name}"
        }
        response = requests.post(
            f"{DASHBOARD_URL}/api/create-product", json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(
                title="🎉 Product Idea Captured!",
                description=f"**Idea:** {product_idea}",
                color=0x4caf50
            )
            embed.add_field(name="📁 Saved to", value=data.get(
                'file', 'Production assets'), inline=False)
            embed.add_field(name="⏰ Timestamp", value=data.get(
                'timestamp', ''), inline=True)
            embed.set_footer(text=f"Created by {ctx.author.name}")
            await ctx.send(embed=embed)
            # Log product creation
            await log_discord_activity("product_created", ctx.author.name, product_idea[:100])
        else:
            await ctx.send("❌ Failed to save product idea. Dashboard may be offline.")
    except Exception as e:
        logger.error(f"Product creation error: {e}")
        # Fallback to local storage
        await create_product_locally(ctx, product_idea)


async def create_product_locally(ctx, product_idea):
    """Create product locally when API is unavailable"""
    try:
        # Create products directory if it doesn't exist
        products_dir = Path("production_assets/product_ideas")
        products_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamp for unique filename
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        product_file = products_dir / f"discord_product_{now}.txt"

        # Create product file with initial content
        with open(product_file, 'w', encoding='utf-8') as f:
            f.write(f"Product: {product_idea}\n")
            f.write(
                f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source: Discord - {ctx.author.name}\n")
            f.write(f"Channel: {ctx.channel.name}\n\n")
            f.write("--- DEVELOPMENT NOTES ---\n")
            f.write("Add your ideas, features, and implementation notes here.\n")

        embed = discord.Embed(
            title="💾 Product Saved Locally!",
            description=f"**Idea:** {product_idea}",
            color=0x4caf50
        )
        embed.add_field(name="📁 File", value=str(product_file), inline=False)
        embed.add_field(
            name="🔄 Status", value="Saved locally - will sync when dashboard is available", inline=False)
        await ctx.send(embed=embed)

        logger.info(f"Product saved locally: {product_file}")

    except Exception as e:
        logger.error(f"Local product creation failed: {e}")
        await ctx.send(f"❌ Could not save product: {str(e)}")

# 📝 Activity Logging Function (MISSING - CRITICAL FIX)


async def log_discord_activity(action: str, user: str, details: str = ""):
    """Log Discord bot activity to database and files"""
    try:
        # Log to database
        conn = sqlite3.connect('chaosgenius.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activity_log (action, type, details)
            VALUES (?, ?, ?)
        ''', (f"Discord: {action}", "discord_bot", f"User: {user} | {details}"))
        conn.commit()
        conn.close()

        # Also log to file for backup
        log_dir = Path("logs/discord_bot")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / \
            f"discord_activity_{datetime.now().strftime('%Y%m%d')}.log"

        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {action} | User: {user} | {details}\n")

        logger.info(f"Discord activity logged: {action} by {user}")

    except Exception as e:
        logger.error(f"Failed to log Discord activity: {e}")

# 🧠 Initialize BROski AI Core
broski_ai = BROskiCore()
logger.info("🚀 BROski ClanVerse Ultra AI System ACTIVATED!")

# 🪙 Initialize BROski$ Token Engine
if TOKENS_AVAILABLE:
    token_engine = BROskiTokenEngine()
    logger.info("🪙 BROski$ Token Economy Engine ACTIVATED!")
else:
    token_engine = None
    logger.warning("⚠️ Token Economy running in simulation mode")

# Add after the bot initialization
@bot.event
async def on_ready():
    print(f'\n🚀 {bot.user} has landed in the ClanVerse!')
    print(f'🔗 Connected to {len(bot.guilds)} server(s)')
    print(f'🧠 BROski AI Intelligence: {broski_ai.system_intelligence}%')
    print(f'🎯 ClanVerse Ultra Mode: ACTIVATED')

    # 🪙 Load BROski$ Token Commands
    if TOKENS_AVAILABLE and token_engine:
        try:
            await bot.add_cog(BROskiTokenCommands(bot, token_engine))
            print(f'🪙 BROski$ Token Economy Commands: LOADED')
        except Exception as e:
            logger.error(f"Failed to load token commands: {e}")
            print(f'⚠️ Token commands failed to load, running without tokens')

    # Set BROski status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="the ClanVerse 🧠💰 | !broski for AI help | !wallet for tokens"
    )
    await bot.change_presence(activity=activity)

# 🧠 BROski AI Chat Command
@bot.command(name='broski', aliases=['ai', 'help', 'chat'])
async def broski_chat(ctx, *, message: str = None):
    """🧠 Chat with BROski AI - Your neurodivergent productivity companion"""

    if not message:
        embed = discord.Embed(
            title="🧠 BROski ClanVerse Ultra AI",
            description="Your neurodivergent productivity companion is here!",
            color=0x00ff88
        )
        embed.add_field(
            name="💬 How to Chat",
            value="`!broski [your message]`\nExample: `!broski I'm feeling overwhelmed with my tasks`",
            inline=False
        )
        embed.add_field(
            name="🎯 What I Can Help With",
            value="• ADHD-friendly productivity tips\n• Mood analysis & support\n• Hyperfocus session guidance\n• Personalized motivation\n• Task organization strategies",
            inline=False
        )
        embed.add_field(
            name="🚀 System Status",
            value=f"Intelligence: {broski_ai.system_intelligence}%\nStatus: FULLY OPERATIONAL",
            inline=False
        )
        await ctx.send(embed=embed)
        return

    try:
        # Show typing indicator
        async with ctx.typing():
            # Build context for BROski
            context = {
                'platform': 'discord',
                'server_name': ctx.guild.name if ctx.guild else 'DM',
                'channel_name': ctx.channel.name if hasattr(ctx.channel, 'name') else 'direct',
                'interaction_type': 'discord_command'
            }

            # Process with BROski AI
            response = await broski_ai.process_user_interaction(
                str(ctx.author.id),
                message,
                context
            )

            # Create rich embed response
            embed = discord.Embed(
                title=f"🧠 BROski {response.style.replace('_', ' ').title()}",
                description=response.message,
                color=0x00ff88,
                timestamp=datetime.now()
            )

            # Add mood and energy info
            embed.add_field(
                name="🎭 Detected Mood",
                value=f"{response.mood_detected.title()} (Confidence: {response.confidence:.1%})",
                inline=True
            )
            embed.add_field(
                name="⚡ Energy Level",
                value=f"{response.energy_level}/100",
                inline=True
            )

            # Add motivation boost if available
            if response.motivation_boost:
                embed.add_field(
                    name="💪 Motivation Boost",
                    value=response.motivation_boost,
                    inline=False
                )

            # Add top recommendation
            if response.recommendations:
                embed.add_field(
                    name="💡 BROski's Recommendation",
                    value=response.recommendations[0],
                    inline=False
                )

            embed.set_footer(text=f"BROski ClanVerse Ultra • Learning from every interaction")

            await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Error in BROski chat command: {e}")
        embed = discord.Embed(
            title="🔧 BROski Brain Glitch",
            description="I'm having a quick moment, but I'm still here for you! Try again in a sec.",
            color=0xff9900
        )
        await ctx.send(embed=embed)

# 🔥 Hyperfocus Session Support
@bot.command(name='hyperfocus', aliases=['focus', 'zone'])
async def hyperfocus_session(ctx, duration: int = 25, *, task_description: str = "focus session"):
    """🔥 Start a hyperfocus session with BROski support"""

    try:
        user_id = str(ctx.author.id)

        # Get session support from BROski
        session_data = {
            'duration_minutes': duration,
            'task_type': task_description,
            'user_id': user_id
        }

        support = await broski_ai.get_hyperfocus_session_support(user_id, session_data)

        embed = discord.Embed(
            title="🔥 HYPERFOCUS SESSION ACTIVATED",
            description=support['motivation_message'],
            color=0xff6600,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="⏰ Duration",
            value=f"{duration} minutes",
            inline=True
        )
        embed.add_field(
            name="🎯 Task",
            value=task_description,
            inline=True
        )
        embed.add_field(
            name="🧠 Session Type",
            value=support['session_type'].replace('_', ' ').title(),
            inline=True
        )

        if support['recommendations']:
            embed.add_field(
                name="💡 BROski's Session Tips",
                value="\n".join(f"• {tip}" for tip in support['recommendations'][:3]),
                inline=False
            )

        if support.get('hyperfocus_phrase'):
            embed.add_field(
                name="🚀 Hyperfocus Activation",
                value=support['hyperfocus_phrase'],
                inline=False
            )

        embed.set_footer(text="React with ✅ when you complete your session!")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('⏸️')
        await message.add_reaction('🔥')

    except Exception as e:
        logger.error(f"Error in hyperfocus command: {e}")
        await ctx.send("🔧 BROski's hyperfocus system is recalibrating! Try again in a moment.")

# 📊 BROski System Status
@bot.command(name='broski_status', aliases=['ai_status', 'system'])
async def broski_system_status(ctx):
    """📊 Check BROski AI system status and intelligence"""

    try:
        status = broski_ai.get_system_status()

        embed = discord.Embed(
            title="🧠 BROski ClanVerse Ultra - System Status",
            description=f"**{status['status']}** • Intelligence: {status['system_intelligence']}%",
            color=0x00ff88,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="🤖 AI Modules",
            value=f"✅ Motivation Engine\n✅ Mood Detector\n✅ Learning System\n✅ Communication Style",
            inline=True
        )

        embed.add_field(
            name="📊 Activity Stats",
            value=f"Active Users: {status['active_users']}\nConversations: {status['total_conversations']}",
            inline=True
        )

        if 'learning_stats' in status:
            learning = status['learning_stats']
            embed.add_field(
                name="🎓 Learning Progress",
                value=f"System Maturity: {learning.get('system_maturity', 'Learning')}\nInteractions Learned: {learning.get('total_interactions_learned', 0)}",
                inline=True
            )

        embed.add_field(
            name="🎯 Mission",
            value=status['personality_core']['mission'],
            inline=False
        )

        embed.set_footer(text=f"BROski {status['version']} • Neurodivergent Excellence Engine")

        await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Error getting BROski status: {e}")
        await ctx.send("🔧 BROski status check is experiencing a glitch! System still operational though!")
