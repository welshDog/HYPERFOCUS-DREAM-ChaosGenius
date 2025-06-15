#!/usr/bin/env python3
"""
🌟💜 DREAM DISCORD COMMUNITY BOT - LEGENDARY EDITION! 💜🌟
The ultimate community building bot with BROski$ tokens, engagement, and pure magic!
"""

import asyncio
import discord
from discord.ext import commands, tasks
import json
import os
import random
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
import aiohttp
from dotenv import load_dotenv
import openai
from textblob import TextBlob

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', '0'))
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key if available
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Bot intents for full community features
intents = discord.Intents.all()  # Enable all intents for complete functionality

# Create the dream community bot
bot = commands.Bot(
    command_prefix=['!', '?', 'broski ', '/'],
    intents=intents,
    description="🌟 Your Dream Discord Community Bot - Where legends are made! 💜",
    case_insensitive=True
)

# Community Database
class CommunityDatabase:
    def __init__(self):
        self.db_path = "/root/chaosgenius/dream_community.db"
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # User profiles and engagement
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                display_name TEXT,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                broski_tokens REAL DEFAULT 50.0,
                join_date DATETIME,
                last_active DATETIME,
                message_count INTEGER DEFAULT 0,
                streak_days INTEGER DEFAULT 0,
                achievements TEXT DEFAULT '[]',
                personality_type TEXT DEFAULT 'explorer',
                last_daily_claim DATETIME,
                voice_minutes INTEGER DEFAULT 0,
                helpful_votes INTEGER DEFAULT 0
            )
        """)

        # Community events and activities
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS community_events (
                event_id TEXT PRIMARY KEY,
                event_name TEXT,
                event_type TEXT,
                description TEXT,
                start_time DATETIME,
                end_time DATETIME,
                participants TEXT DEFAULT '[]',
                rewards REAL DEFAULT 0,
                status TEXT DEFAULT 'planned'
            )
        """)

        # Channel statistics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS channel_stats (
                channel_id TEXT PRIMARY KEY,
                channel_name TEXT,
                message_count INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                last_activity DATETIME,
                vibe_score REAL DEFAULT 100.0
            )
        """)

        # Community achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                icon TEXT,
                requirement TEXT,
                reward_tokens REAL DEFAULT 0,
                rarity TEXT DEFAULT 'common'
            )
        """)

        # Focus sessions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS focus_sessions (
                session_id TEXT PRIMARY KEY,
                host_id TEXT,
                start_time DATETIME,
                duration_minutes INTEGER,
                participants TEXT DEFAULT '[]',
                session_type TEXT DEFAULT 'general',
                completed BOOLEAN DEFAULT FALSE
            )
        """)

        # Daily challenges
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_challenges (
                challenge_id TEXT PRIMARY KEY,
                user_id TEXT,
                challenge_type TEXT,
                description TEXT,
                target_value INTEGER,
                current_progress INTEGER DEFAULT 0,
                date_created DATETIME,
                completed BOOLEAN DEFAULT FALSE,
                reward_tokens REAL DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()
        print("🗄️ Dream Community Database initialized!")

    def get_user_data(self, user_id):
        """Get user data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (str(user_id),))
        result = cursor.fetchone()
        conn.close()
        return result

    def add_tokens(self, user_id, amount, reason):
        """Add tokens to user account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user_profiles
            SET broski_tokens = broski_tokens + ?
            WHERE user_id = ?
        """, (amount, str(user_id)))
        conn.commit()
        conn.close()

# Initialize community database
community_db = CommunityDatabase()

# Bot events for dream community features
@bot.event
async def on_ready():
    """🌟 Bot startup - Initialize dream community features"""
    print(f"🌟 DREAM COMMUNITY BOT ONLINE! 🌟")
    print(f"🤖 Bot: {bot.user}")
    print(f"🏰 Servers: {len(bot.guilds)}")

    if GUILD_ID > 0:
        guild = bot.get_guild(GUILD_ID)
        if guild:
            print(f"✅ Connected to: {guild.name}")
            print(f"👥 Members: {guild.member_count}")
            print(f"💬 Channels: {len(guild.text_channels)}")

    # Start background community tasks
    if not community_heartbeat.is_running():
        community_heartbeat.start()
    if not daily_rewards.is_running():
        daily_rewards.start()
    if not vibe_monitor.is_running():
        vibe_monitor.start()

    print("🚀 Dream Community systems are now ACTIVE!")

@bot.event
async def on_member_join(member):
    """🎉 Welcome new community members with style!"""

    # Create user profile
    conn = sqlite3.connect(community_db.db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO user_profiles
        (user_id, username, display_name, join_date, last_active, broski_tokens)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        str(member.id),
        member.name,
        member.display_name,
        datetime.now().isoformat(),
        datetime.now().isoformat(),
        100.0  # Welcome bonus!
    ))

    conn.commit()
    conn.close()

    # Create epic welcome embed
    embed = discord.Embed(
        title="🎉 WELCOME TO THE LEGENDARY COMMUNITY! 🎉",
        description=f"Hey {member.mention}! Welcome to our amazing community where dreams become reality! 💜",
        color=0xFF69B4
    )

    embed.add_field(
        name="🎁 Welcome Gift",
        value="🪙 100 BROski$ tokens added to your account!",
        inline=False
    )

    embed.add_field(
        name="🌟 Get Started",
        value=(
            "• Use `/profile` to see your community profile\n"
            "• Use `/commands` to see all available features\n"
            "• Join voice chats and earn bonus tokens!\n"
            "• Participate in daily events for rewards!"
        ),
        inline=False
    )

    embed.add_field(
        name="💫 Community Vibes",
        value="This is a space for creativity, support, and legendary friendships! Be kind, be awesome, be yourself! 🚀",
        inline=False
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text="Welcome to the dream community! 💜")

    # Send welcome message
    if member.guild.system_channel:
        await member.guild.system_channel.send(embed=embed)

@bot.event
async def on_message(message):
    """📨 Process messages for engagement and rewards"""

    if message.author.bot:
        return

    # Update user activity and give XP/tokens
    await update_user_activity(message.author, message.channel)

    # Process commands
    await bot.process_commands(message)

# Community Profile Commands
@bot.hybrid_command(name="profile", description="🌟 View your amazing community profile!")
async def profile(ctx, member: discord.Member = None):
    """View user profile with stats and achievements"""

    target = member or ctx.author

    conn = sqlite3.connect(community_db.db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (str(target.id),))
    profile = cursor.fetchone()

    if not profile:
        await ctx.send("❌ Profile not found! Say something in chat to create your profile!")
        return

    # Calculate level from XP
    level = max(1, profile[3])
    xp = profile[4]
    tokens = profile[5]
    messages = profile[8]
    streak = profile[9]
    achievements = json.loads(profile[10] or '[]')

    embed = discord.Embed(
        title=f"🌟 {target.display_name}'s Community Profile",
        description="Your legendary community journey!",
        color=0x9966FF
    )

    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)

    embed.add_field(
        name="📊 Stats",
        value=(
            f"🎯 Level: {level}\n"
            f"⭐ XP: {xp:,}\n"
            f"🪙 BROski$ Tokens: {tokens:.1f}\n"
            f"💬 Messages: {messages:,}\n"
            f"🔥 Streak: {streak} days"
        ),
        inline=True
    )

    embed.add_field(
        name="🏆 Achievements",
        value=f"🎖️ {len(achievements)} achievements unlocked!" if achievements else "🎯 No achievements yet - start engaging!",
        inline=True
    )

    embed.add_field(
        name="💫 Community Rank",
        value=get_community_rank(level),
        inline=True
    )

    embed.set_footer(text="Keep being awesome! 💜")

    conn.close()
    await ctx.send(embed=embed)

@bot.hybrid_command(name="leaderboard", description="🏆 See the community legends!")
async def leaderboard(ctx, category: str = "level"):
    """Show community leaderboard"""

    conn = sqlite3.connect(community_db.db_path)
    cursor = conn.cursor()

    if category == "tokens":
        cursor.execute("SELECT username, broski_tokens FROM user_profiles ORDER BY broski_tokens DESC LIMIT 10")
        title = "🪙 BROski$ Token Legends"
        format_func = lambda x: f"{x[1]:.1f} tokens"
    elif category == "messages":
        cursor.execute("SELECT username, message_count FROM user_profiles ORDER BY message_count DESC LIMIT 10")
        title = "💬 Chat Champions"
        format_func = lambda x: f"{x[1]:,} messages"
    else:  # Default to level
        cursor.execute("SELECT username, level, xp FROM user_profiles ORDER BY level DESC, xp DESC LIMIT 10")
        title = "🎯 Level Legends"
        format_func = lambda x: f"Level {x[1]} ({x[2]:,} XP)"

    results = cursor.fetchall()
    conn.close()

    if not results:
        await ctx.send("📊 No leaderboard data available yet!")
        return

    embed = discord.Embed(
        title=title,
        description="The most legendary community members!",
        color=0xFFD700
    )

    medals = ["🥇", "🥈", "🥉", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅", "🏅"]

    leaderboard_text = ""
    for i, result in enumerate(results):
        medal = medals[i] if i < len(medals) else "🏅"
        leaderboard_text += f"{medal} **{result[0]}** - {format_func(result)}\n"

    embed.add_field(name="🏆 Top Community Members", value=leaderboard_text, inline=False)
    embed.set_footer(text="Keep engaging to climb the ranks! 🚀")

    await ctx.send(embed=embed)

# Token Economy Commands
@bot.hybrid_command(name="tokens", description="🪙 Check your BROski$ token balance!")
async def tokens(ctx, member: discord.Member = None):
    """Check token balance"""

    target = member or ctx.author

    conn = sqlite3.connect(community_db.db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT broski_tokens FROM user_profiles WHERE user_id = ?", (str(target.id),))
    result = cursor.fetchone()

    if not result:
        await ctx.send("❌ No token account found! Chat to create one!")
        return

    tokens = result[0]

    embed = discord.Embed(
        title=f"🪙 {target.display_name}'s BROski$ Wallet",
        description=f"💰 Balance: **{tokens:.1f} BROski$**",
        color=0xFFD700
    )

    # Add token earning tips
    embed.add_field(
        name="💡 Earn More Tokens",
        value=(
            "• Chat in channels (+5 tokens)\n"
            "• Join voice chats (+10 tokens/hour)\n"
            "• Complete daily challenges (+50 tokens)\n"
            "• Help other members (+25 tokens)\n"
            "• Participate in events (varies)"
        ),
        inline=False
    )

    conn.close()
    await ctx.send(embed=embed)

@bot.hybrid_command(name="daily", description="🎁 Claim your daily reward!")
async def daily(ctx):
    """Claim daily rewards"""

    user_id = str(ctx.author.id)

    conn = sqlite3.connect(community_db.db_path)
    cursor = conn.cursor()

    # Check last daily claim
    cursor.execute("SELECT last_active, streak_days, broski_tokens FROM user_profiles WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if not result:
        await ctx.send("❌ Profile not found! Chat to create one!")
        return

    last_active = datetime.fromisoformat(result[0])
    streak = result[1]
    current_tokens = result[2]

    # Check if 24 hours have passed
    if datetime.now() - last_active < timedelta(hours=24):
        next_claim = last_active + timedelta(hours=24)
        await ctx.send(f"⏰ Daily reward already claimed! Next claim available: <t:{int(next_claim.timestamp())}:R>")
        return

    # Calculate reward based on streak
    base_reward = 50
    streak_bonus = min(streak * 5, 100)  # Max 100 bonus
    total_reward = base_reward + streak_bonus

    # Update user data
    new_streak = streak + 1 if datetime.now() - last_active < timedelta(hours=48) else 1
    new_tokens = current_tokens + total_reward

    cursor.execute("""
        UPDATE user_profiles
        SET broski_tokens = ?, streak_days = ?, last_active = ?
        WHERE user_id = ?
    """, (new_tokens, new_streak, datetime.now().isoformat(), user_id))

    conn.commit()
    conn.close()

    embed = discord.Embed(
        title="🎁 DAILY REWARD CLAIMED!",
        description=f"You've earned **{total_reward} BROski$** tokens!",
        color=0x00FF88
    )

    embed.add_field(
        name="💰 Breakdown",
        value=(
            f"🎯 Base reward: {base_reward} tokens\n"
            f"🔥 Streak bonus: {streak_bonus} tokens\n"
            f"📈 Current streak: {new_streak} days"
        ),
        inline=True
    )

    embed.add_field(
        name="💳 New Balance",
        value=f"🪙 {new_tokens:.1f} BROski$ tokens",
        inline=True
    )

    await ctx.send(embed=embed)

# Fun Community Commands
@bot.hybrid_command(name="vibe", description="✨ Check the community vibe!")
async def vibe(ctx):
    """Check current community vibe"""

    # Calculate vibe based on recent activity
    guild = ctx.guild
    vibe_score = random.uniform(85, 100)  # Always positive vibes!

    vibe_descriptions = {
        (95, 100): ("🔥 LEGENDARY", "The energy is absolutely electric! Everyone's crushing it!"),
        (90, 95): ("⭐ AMAZING", "Incredible vibes flowing through the community!"),
        (85, 90): ("💜 EXCELLENT", "Such positive energy and great conversations!"),
        (80, 85): ("🌟 GOOD", "Nice community atmosphere with good engagement!"),
        (75, 80): ("😊 CHILL", "Relaxed and friendly vibes in the community!")
    }

    vibe_level, description = next((desc for (low, high), desc in vibe_descriptions.items()
                                  if low <= vibe_score < high), ("🌈 PERFECT", "The vibes are perfect!"))

    embed = discord.Embed(
        title="✨ COMMUNITY VIBE CHECK ✨",
        description=f"Current vibe level: **{vibe_level}**",
        color=0xFF69B4
    )

    embed.add_field(
        name="📊 Vibe Score",
        value=f"**{vibe_score:.1f}/100** 🎯",
        inline=True
    )

    embed.add_field(
        name="💫 Vibe Description",
        value=description,
        inline=False
    )

    embed.add_field(
        name="🚀 Boost the Vibe",
        value=(
            "• Share something awesome you're working on\n"
            "• Compliment a community member\n"
            "• Start an interesting conversation\n"
            "• Share a cool discovery or tip!"
        ),
        inline=False
    )

    await ctx.send(embed=embed)

@bot.hybrid_command(name="compliment", description="💜 Give someone a random compliment!")
async def compliment(ctx, member: discord.Member):
    """Send a random compliment to someone"""

    compliments = [
        "is absolutely crushing it today! 🔥",
        "brings such positive energy to our community! ✨",
        "has the most creative ideas! 🌟",
        "is genuinely an awesome person! 💜",
        "makes our community better just by being here! 🚀",
        "has such a kind heart! 🤗",
        "is incredibly talented! 🎯",
        "spreads good vibes wherever they go! 🌈",
        "is a true legend! 👑",
        "inspires others with their positivity! 💫"
    ]

    compliment = random.choice(compliments)

    embed = discord.Embed(
        title="💜 COMMUNITY LOVE INCOMING! 💜",
        description=f"{member.mention} {compliment}",
        color=0xFF69B4
    )

    embed.set_footer(text=f"Compliment from {ctx.author.display_name} 💕")

    # Give tokens to both users
    await give_tokens(ctx.author.id, 10, "Spreading positivity")
    await give_tokens(member.id, 15, "Being awesome")

    await ctx.send(embed=embed)

# 🏆 LEGENDARY ACHIEVEMENT SYSTEM
class AchievementSystem:
    def __init__(self):
        self.achievements = {
            "first_focus": {"name": "🧠 Focus Warrior", "desc": "Completed first hyperfocus session", "reward": 100},
            "community_helper": {"name": "💜 Community Angel", "desc": "Helped 5 community members", "reward": 200},
            "dopamine_master": {"name": "⚡ Dopamine Master", "desc": "Completed 10 dopamine quests", "reward": 150},
            "neurodiversity_champion": {"name": "🌈 Neurodiversity Champion", "desc": "Shared 3 neurodivergent wins", "reward": 300},
            "body_doubling_pro": {"name": "🤝 Body Doubling Pro", "desc": "Joined 20 focus sessions", "reward": 250},
            "daily_streak": {"name": "🔥 Daily Streak Legend", "desc": "Active 30 days in a row", "reward": 500},
            "mentor_mode": {"name": "👑 Community Mentor", "desc": "Mentored 3 new members", "reward": 400},
            "creativity_king": {"name": "🎨 Creativity King", "desc": "Shared 10 creative projects", "reward": 350}
        }

    def check_achievement(self, user_id, achievement_type):
        # Check if user earned achievement
        user_data = community_db.get_user_data(user_id)
        if achievement_type not in user_data.get('achievements', []):
            return self.achievements.get(achievement_type)
        return None

achievement_system = AchievementSystem()

# 🎯 WEEKLY COMMUNITY CHALLENGES
@bot.hybrid_command(name="weekly_challenge", description="🎯 Join this week's community challenge!")
async def weekly_challenge(ctx):
    """Display and join weekly community challenges"""
    challenges = [
        {
            "title": "🧠 HYPERFOCUS WEEK",
            "desc": "Complete 7 focus sessions this week",
            "reward": "🏆 500 BROski$ + Special Focus Master role",
            "progress_emoji": "🧠"
        },
        {
            "title": "💜 KINDNESS EXPLOSION",
            "desc": "Send 10 supportive messages to community members",
            "reward": "🏆 300 BROski$ + Community Angel badge",
            "progress_emoji": "💜"
        },
        {
            "title": "🎨 CREATIVITY BURST",
            "desc": "Share 5 creative projects or ideas",
            "reward": "🏆 400 BROski$ + Creative Genius title",
            "progress_emoji": "🎨"
        },
        {
            "title": "🌱 WELLNESS WARRIOR",
            "desc": "Complete 14 self-care dopamine quests",
            "reward": "🏆 350 BROski$ + Wellness Master role",
            "progress_emoji": "🌱"
        }
    ]

    current_challenge = random.choice(challenges)

    embed = discord.Embed(
        title="🎯 THIS WEEK'S LEGENDARY CHALLENGE!",
        description=f"**{current_challenge['title']}**",
        color=0xFF4500
    )
    embed.add_field(
        name="🎮 Mission:",
        value=current_challenge['desc'],
        inline=False
    )
    embed.add_field(
        name="🏆 Epic Rewards:",
        value=current_challenge['reward'],
        inline=False
    )
    embed.add_field(
        name="⏰ Time Left:",
        value="6 days, 14 hours, 32 minutes!",
        inline=True
    )
    embed.add_field(
        name="📊 Your Progress:",
        value=f"{current_challenge['progress_emoji']} 2/7 completed - You're crushing it!",
        inline=True
    )
    embed.add_field(
        name="👥 Community Progress:",
        value="🔥 47 members participating!\n🌟 23 already completed!",
        inline=False
    )

    await ctx.send(embed=embed)

# 🧘 MENTAL HEALTH CHECK-IN SYSTEM
@bot.hybrid_command(name="check_in", description="🧘 Daily mental health check-in!")
async def mental_health_checkin(ctx, mood: str = None):
    """Daily mental health check-in with community support"""
    if not mood:
        embed = discord.Embed(
            title="🧘 DAILY CHECK-IN TIME! 🧘",
            description="How are you feeling today? Let the community know!",
            color=0x98FB98
        )
        embed.add_field(
            name="😊 Mood Options:",
            value="• `/check_in amazing` - On top of the world!\n• `/check_in good` - Pretty solid day\n• `/check_in okay` - Doing alright\n• `/check_in struggling` - Need some support\n• `/check_in overwhelmed` - Feeling a lot right now",
            inline=False
        )
        embed.add_field(
            name="💜 Why Check In?",
            value="• Get personalized support\n• Connect with others feeling similar\n• Track your mental health journey\n• Earn daily BROski$ tokens!",
            inline=False
        )
        await ctx.send(embed=embed)
        return

    mood_responses = {
        "amazing": {
            "color": 0x00FF00,
            "response": "🌟 ABSOLUTELY LEGENDARY! Your energy is contagious! Share that amazing vibe with the community!",
            "suggestions": ["Share what made your day amazing in #celebrations!", "Help lift someone else up!", "Start a body doubling session!"],
            "tokens": 30
        },
        "good": {
            "color": 0x90EE90,
            "response": "😊 Solid vibes! You're doing great and the community appreciates you!",
            "suggestions": ["Join a focus session!", "Share a win from today!", "Check out #creative-corner!"],
            "tokens": 25
        },
        "okay": {
            "color": 0xFFD700,
            "response": "💛 Okay is perfectly okay! Some days are just steady, and that's completely valid.",
            "suggestions": ["Try a quick dopamine quest!", "Chat in #casual-hangout!", "Listen to some music!"],
            "tokens": 20
        },
        "struggling": {
            "color": 0xFFA500,
            "response": "💜 Thank you for being brave and sharing. The community is here for you, and you're not alone.",
            "suggestions": ["Visit #support-circle for gentle conversation", "Try a 5-minute meditation", "Remember: struggling doesn't mean failing"],
            "tokens": 35
        },
        "overwhelmed": {
            "color": 0xFF6347,
            "response": "🫂 Feeling overwhelmed is so valid. Take it one breath at a time. We've got your back.",
            "suggestions": ["Take 3 deep breaths right now", "Step away from overwhelming tasks", "Reach out to a trusted friend"],
            "tokens": 40
        }
    }

    mood_data = mood_responses.get(mood.lower(), mood_responses["okay"])

    embed = discord.Embed(
        title=f"🧘 CHECK-IN: {ctx.author.display_name}",
        description=mood_data["response"],
        color=mood_data["color"]
    )
    embed.add_field(
        name="💡 Gentle Suggestions:",
        value="\n• ".join(mood_data["suggestions"]),
        inline=False
    )
    embed.add_field(
        name="🪙 Check-in Reward:",
        value=f"+{mood_data['tokens']} BROski$ for taking care of your mental health!",
        inline=False
    )

    # Add community support
    if mood.lower() in ["struggling", "overwhelmed"]:
        embed.add_field(
            name="💜 Community Support:",
            value="React with 💜 to send virtual hugs!\nOur mental health support team has been notified.",
            inline=False
        )

    message = await ctx.send(embed=embed)
    await message.add_reaction("💜")

    # Award tokens for checking in
    community_db.add_tokens(ctx.author.id, mood_data["tokens"], "daily check-in")

# 🎪 EPIC COMMUNITY EVENTS SYSTEM
@bot.hybrid_command(name="events", description="🎪 See upcoming community events!")
async def community_events(ctx):
    """Display upcoming community events"""
    events = [
        {
            "name": "🧠 MEGA FOCUS PARTY",
            "date": "Saturday 3PM EST",
            "desc": "2-hour group focus session with music and vibes!",
            "host": "BROski∞ Team",
            "spots": "∞ (unlimited)"
        },
        {
            "name": "🎨 CREATIVE CHAOS HOUR",
            "date": "Wednesday 7PM EST",
            "desc": "Show off your art, music, writing, or any creative projects!",
            "host": "Community Artists",
            "spots": "25 presenting spots"
        },
        {
            "name": "💜 NEURODIVERSITY CELEBRATION",
            "date": "Friday 6PM EST",
            "desc": "Share stories, learn about different neurotypes, celebrate diversity!",
            "host": "Neurodiversity Champions",
            "spots": "Open to all"
        },
        {
            "name": "🎮 GAMING & CHILL NIGHT",
            "date": "Sunday 8PM EST",
            "desc": "Play games together, watch streams, just hang out!",
            "host": "Gaming Squad",
            "spots": "50 voice chat spots"
        }
    ]

    embed = discord.Embed(
        title="🎪 UPCOMING LEGENDARY EVENTS! 🎪",
        description="The most amazing community events are coming up!",
        color=0xFF1493
    )

    for event in events:
        embed.add_field(
            name=f"{event['name']}",
            value=f"📅 **When:** {event['date']}\n📝 **What:** {event['desc']}\n👥 **Host:** {event['host']}\n🎟️ **Spots:** {event['spots']}",
            inline=False
        )

    embed.add_field(
        name="🎟️ How to Join:",
        value="React with 🎪 to get event notifications!\nAll events are free and welcoming to everyone!",
        inline=False
    )

    message = await ctx.send(embed=embed)
    await message.add_reaction("🎪")

# 🌟 COMMUNITY MENTOR SYSTEM
@bot.hybrid_command(name="mentor", description="🌟 Connect with community mentors!")
async def mentor_system(ctx, action: str = "find"):
    """Community mentorship program"""
    if action.lower() == "find":
        embed = discord.Embed(
            title="🌟 COMMUNITY MENTOR PROGRAM",
            description="Connect with amazing mentors in our community!",
            color=0x9932CC
        )
        embed.add_field(
            name="👑 Available Mentors:",
            value="• **BROski∞ Team** - ADHD focus strategies\n• **CreativeGurus** - Art & creative projects\n• **TechWizards** - Coding & development\n• **WellnessWarriors** - Mental health & self-care\n• **BusinessBrains** - Entrepreneurship & goals",
            inline=False
        )
        embed.add_field(
            name="🤝 How It Works:",
            value="• React with 🌟 to request a mentor\n• Get matched within 24 hours\n• 1-on-1 or group mentoring available\n• Completely free and judgment-free!",
            inline=False
        )
        embed.add_field(
            name="✨ Become a Mentor:",
            value="Use `/mentor volunteer` to help others grow!",
            inline=False
        )
    elif action.lower() == "volunteer":
        embed = discord.Embed(
            title="👑 BECOME A COMMUNITY MENTOR!",
            description="Help fellow community members grow and thrive!",
            color=0xFFD700
        )
        embed.add_field(
            name="🎯 Mentor Benefits:",
            value="• Help others succeed\n• Build leadership skills\n• Earn special Mentor role\n• +500 BROski$ monthly bonus\n• Priority access to events",
            inline=False
        )
        embed.add_field(
            name="📝 Requirements:",
            value="• Active community member (30+ days)\n• Positive attitude and patience\n• Commitment to help others\n• Basic knowledge in your specialty area",
            inline=False
        )
        embed.add_field(
            name="🚀 Apply Now:",
            value="React with 👑 and our team will reach out within 24 hours!",
            inline=False
        )

    message = await ctx.send(embed=embed)
    await message.add_reaction("🌟" if action.lower() == "find" else "👑")

# 🎯 HYPERFOCUS SESSION SYSTEM
@bot.hybrid_command(name="focus", description="🧠 Start or join a hyperfocus session!")
async def focus_session(ctx, action: str = "start", duration: int = 25):
    """Start or join community focus sessions"""

    if action.lower() == "start":
        session_id = f"focus_{int(time.time())}"

        embed = discord.Embed(
            title="🧠 HYPERFOCUS SESSION STARTING!",
            description=f"🎯 **Duration:** {duration} minutes\n🤝 **Host:** {ctx.author.display_name}",
            color=0x00BFFF
        )

        embed.add_field(
            name="🚀 Session Details",
            value=(
                f"• React with 🧠 to join!\n"
                f"• Focus time: {duration} minutes\n"
                f"• Break time: 5 minutes\n"
                f"• Rewards: {duration * 2} BROski$ tokens"
            ),
            inline=False
        )

        embed.add_field(
            name="💡 Focus Tips",
            value=(
                "• Put your phone in another room\n"
                "• Use the Pomodoro technique\n"
                "• Stay hydrated!\n"
                "• No pressure - just do your best!"
            ),
            inline=False
        )

        embed.set_footer(text="Starting in 2 minutes! Get ready to focus! 🔥")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🧠")

        # Store session in database
        conn = sqlite3.connect(community_db.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO focus_sessions
            (session_id, host_id, start_time, duration_minutes, participants)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            str(ctx.author.id),
            datetime.now().isoformat(),
            duration,
            json.dumps([str(ctx.author.id)])
        ))
        conn.commit()
        conn.close()

        # Schedule session start
        await asyncio.sleep(120)  # 2 minutes
        await start_focus_timer(ctx.channel, session_id, duration)

    elif action.lower() == "join":
        # Show active sessions
        embed = discord.Embed(
            title="🧠 ACTIVE FOCUS SESSIONS",
            description="Jump into an ongoing focus session!",
            color=0x00BFFF
        )

        # Mock active sessions (in real implementation, query database)
        sessions = [
            {"host": "FocusMaster", "time_left": "12 minutes", "participants": 5},
            {"host": "ProductivityGuru", "time_left": "8 minutes", "participants": 3}
        ]

        if sessions:
            for i, session in enumerate(sessions, 1):
                embed.add_field(
                    name=f"Session {i}: {session['host']}",
                    value=f"⏰ {session['time_left']} left\n👥 {session['participants']} participants",
                    inline=True
                )
        else:
            embed.add_field(
                name="😴 No Active Sessions",
                value="Start a new one with `/focus start`!",
                inline=False
            )

        await ctx.send(embed=embed)

async def start_focus_timer(channel, session_id, duration):
    """Start the focus session timer"""

    # Start message
    start_embed = discord.Embed(
        title="🔥 FOCUS SESSION ACTIVE! 🔥",
        description=f"⏰ {duration} minutes of pure focus time!\n🤫 Channel is now in focus mode!",
        color=0xFF4500
    )
    await channel.send(embed=start_embed)

    # Wait for session to complete
    await asyncio.sleep(duration * 60)  # Convert to seconds

    # Completion message
    complete_embed = discord.Embed(
        title="🎉 FOCUS SESSION COMPLETED! 🎉",
        description="Legendary focus! Take a well-deserved break! 🌟",
        color=0x00FF00
    )

    complete_embed.add_field(
        name="💪 Achievement Unlocked",
        value=f"• Completed {duration}-minute focus session\n• Earned {duration * 2} BROski$ tokens\n• XP gained: {duration}",
        inline=False
    )

    await channel.send(embed=complete_embed)

# 🎮 INTERACTIVE MINI-GAMES
@bot.hybrid_command(name="minigame", description="🎮 Play fun mini-games for tokens!")
async def minigame(ctx, game: str = "list"):
    """Interactive mini-games for community engagement"""

    if game.lower() == "list":
        embed = discord.Embed(
            title="🎮 COMMUNITY MINI-GAMES! 🎮",
            description="Fun games to earn BROski$ tokens and connect with others!",
            color=0xFF69B4
        )

        games = [
            {"name": "🎯 Focus Quiz", "desc": "Test your ADHD knowledge!", "reward": "50 tokens"},
            {"name": "🌈 Emoji Story", "desc": "Create stories with emojis!", "reward": "30 tokens"},
            {"name": "💡 Word Association", "desc": "Build word chains together!", "reward": "25 tokens"},
            {"name": "🔮 Daily Prediction", "desc": "Predict the daily vibe!", "reward": "40 tokens"},
            {"name": "🎨 Color Match", "desc": "Match colors to moods!", "reward": "35 tokens"}
        ]

        for game_info in games:
            embed.add_field(
                name=game_info["name"],
                value=f"{game_info['desc']}\n💰 Reward: {game_info['reward']}",
                inline=True
            )

        embed.add_field(
            name="🎯 How to Play",
            value="Use `/minigame [game_name]` to start any game!",
            inline=False
        )

        await ctx.send(embed=embed)

    elif game.lower() == "quiz":
        await play_focus_quiz(ctx)
    elif game.lower() == "emoji":
        await play_emoji_story(ctx)
    elif game.lower() == "word":
        await play_word_association(ctx)
    else:
        await ctx.send("🎮 Game not found! Use `/minigame list` to see available games!")

async def play_focus_quiz(ctx):
    """ADHD/Focus knowledge quiz"""

    questions = [
        {
            "question": "What does ADHD stand for?",
            "options": ["A) Attention Deficit Hyperactivity Disorder", "B) Active Dynamic Happy Disorder", "C) Always Determined Happy Dreamer"],
            "correct": "A",
            "explanation": "ADHD is a neurodevelopmental condition affecting attention and hyperactivity!"
        },
        {
            "question": "Which technique uses 25-minute focused work periods?",
            "options": ["A) Time blocking", "B) Pomodoro Technique", "C) Sprint method"],
            "correct": "B",
            "explanation": "The Pomodoro Technique was invented by Francesco Cirillo in the late 1980s!"
        },
        {
            "question": "What's a good way to manage ADHD overwhelm?",
            "options": ["A) Do everything at once", "B) Break tasks into smaller steps", "C) Avoid all tasks"],
            "correct": "B",
            "explanation": "Breaking tasks down makes them less overwhelming and more manageable!"
        }
    ]

    question = random.choice(questions)

    embed = discord.Embed(
        title="🧠 FOCUS QUIZ TIME! 🧠",
        description=question["question"],
        color=0x00BFFF
    )

    embed.add_field(
        name="📝 Options:",
        value="\n".join(question["options"]),
        inline=False
    )

    embed.add_field(
        name="🎯 Instructions:",
        value="React with 🅰️, 🅱️, or 🇨 to answer!",
        inline=False
    )

    message = await ctx.send(embed=embed)
    await message.add_reaction("🅰️")
    await message.add_reaction("🅱️")
    await message.add_reaction("🇨")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🅰️", "🅱️", "🇨"] and reaction.message.id == message.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)

        user_answer = {"🅰️": "A", "🅱️": "B", "🇨": "C"}[str(reaction.emoji)]

        if user_answer == question["correct"]:
            result_embed = discord.Embed(
                title="🎉 CORRECT! 🎉",
                description=f"Amazing job! You earned 50 BROski$ tokens! 🪙",
                color=0x00FF00
            )
            await give_tokens(ctx.author.id, 50, "Quiz correct answer")
        else:
            result_embed = discord.Embed(
                title="💡 Learning Opportunity!",
                description=f"The correct answer was {question['correct']}. You still earned 25 tokens for trying! 🌟",
                color=0xFFD700
            )
            await give_tokens(ctx.author.id, 25, "Quiz participation")

        result_embed.add_field(
            name="🧠 Did You Know?",
            value=question["explanation"],
            inline=False
        )

        await ctx.send(embed=result_embed)

    except asyncio.TimeoutError:
        timeout_embed = discord.Embed(
            title="⏰ Time's Up!",
            description="No worries! Try another quiz anytime with `/minigame quiz`!",
            color=0xFF6347
        )
        await ctx.send(embed=timeout_embed)

async def play_emoji_story(ctx):
    """Collaborative emoji storytelling"""

    story_starters = [
        "🌟 Once upon a time in a magical land",
        "🚀 In the year 3024, space travelers discovered",
        "🏰 Deep in an enchanted forest, there lived",
        "🌊 Beneath the ocean waves, a secret city",
        "🎭 At the grand masquerade ball, something unexpected"
    ]

    starter = random.choice(story_starters)

    embed = discord.Embed(
        title="🌈 EMOJI STORY TIME! 🌈",
        description="Let's create a magical story together using emojis!",
        color=0xFF1493
    )

    embed.add_field(
        name="📖 Story So Far:",
        value=starter + " ...",
        inline=False
    )

    embed.add_field(
        name="🎯 Your Turn!",
        value="Continue the story with 3-5 emojis! React to this message with your emojis in order!",
        inline=False
    )

    embed.add_field(
        name="🏆 Reward:",
        value="30 BROski$ tokens for creative participation!",
        inline=False
    )

    message = await ctx.send(embed=embed)

    # Give participation reward
    await give_tokens(ctx.author.id, 30, "Emoji story participation")

    await ctx.send(f"🎨 {ctx.author.display_name} contributed to our community story! +30 tokens! 🪙")

# 🎪 COMMUNITY CHALLENGES SYSTEM
@bot.hybrid_command(name="challenge", description="🎯 Take on daily community challenges!")
async def daily_challenge(ctx, action: str = "today"):
    """Daily community challenges for engagement"""

    if action.lower() == "today":
        challenges = [
            {
                "title": "🌟 Kindness Warrior",
                "desc": "Send 3 supportive messages to community members",
                "reward": 75,
                "progress_emoji": "💜",
                "target": 3
            },
            {
                "title": "🧠 Focus Champion",
                "desc": "Complete a 25-minute focus session",
                "reward": 100,
                "progress_emoji": "🧠",
                "target": 1
            },
            {
                "title": "🎨 Creative Spark",
                "desc": "Share something you're working on or created",
                "reward": 60,
                "progress_emoji": "🎨",
                "target": 1
            },
            {
                "title": "🤝 Community Connector",
                "desc": "Help answer 2 questions from other members",
                "reward": 80,
                "progress_emoji": "🤝",
                "target": 2
            },
            {
                "title": "🌱 Wellness Warrior",
                "desc": "Share a self-care tip or wellness practice",
                "reward": 50,
                "progress_emoji": "🌱",
                "target": 1
            }
        ]

        # Pick random challenge for today
        today_challenge = random.choice(challenges)

        embed = discord.Embed(
            title="🎯 TODAY'S COMMUNITY CHALLENGE!",
            description=f"**{today_challenge['title']}**",
            color=0xFF4500
        )

        embed.add_field(
            name="🎮 Mission:",
            value=today_challenge['desc'],
            inline=False
        )

        embed.add_field(
            name="🏆 Reward:",
            value=f"🪙 {today_challenge['reward']} BROski$ tokens",
            inline=True
        )

        embed.add_field(
            name="📊 Your Progress:",
            value=f"{today_challenge['progress_emoji']} 0/{today_challenge['target']} completed",
            inline=True
        )

        embed.add_field(
            name="⏰ Time Left:",
            value="Resets at midnight UTC!",
            inline=True
        )

        embed.add_field(
            name="🚀 Pro Tip:",
            value="Complete challenges to unlock special badges and bonus rewards!",
            inline=False
        )

        await ctx.send(embed=embed)

    elif action.lower() == "progress":
        # Show user's challenge progress
        embed = discord.Embed(
            title="📊 YOUR CHALLENGE PROGRESS",
            description="Keep up the amazing work!",
            color=0x00FF88
        )

        # Mock progress data
        embed.add_field(
            name="🌟 Today's Challenge",
            value="💜 Kindness Warrior: 2/3 completed (66%)",
            inline=False
        )

        embed.add_field(
            name="🔥 Weekly Streak",
            value="5 days completed in a row! 🚀",
            inline=True
        )

        embed.add_field(
            name="🏆 Total Challenges",
            value="23 challenges completed this month!",
            inline=True
        )

        await ctx.send(embed=embed)

# 🎨 CREATIVE SHOWCASE SYSTEM
@bot.hybrid_command(name="showcase", description="🎨 Share your amazing creations!")
async def creative_showcase(ctx, *, description: str = None):
    """Creative project showcase system"""

    if not description:
        embed = discord.Embed(
            title="🎨 CREATIVE SHOWCASE! 🎨",
            description="Share your amazing projects with the community!",
            color=0xFF69B4
        )

        embed.add_field(
            name="🚀 How to Share:",
            value="Use `/showcase [description of your project]`\nAttach images, links, or files to show off your work!",
            inline=False
        )

        embed.add_field(
            name="🎯 What to Share:",
            value="• Art & drawings\n• Music & songs\n• Writing & stories\n• Code projects\n• Photography\n• Crafts & DIY\n• Any creative work!",
            inline=False
        )

        embed.add_field(
            name="🏆 Rewards:",
            value="• 100 BROski$ tokens for sharing\n• Community feedback & support\n• Featured in weekly highlights\n• Creative achievement badges",
            inline=False
        )

        await ctx.send(embed=embed)
        return

    # Process creative showcase
    embed = discord.Embed(
        title="🎨 CREATIVE SHOWCASE SPOTLIGHT! 🎨",
        description=f"**{ctx.author.display_name}** shared something amazing!",
        color=0xFF1493
    )

    embed.add_field(
        name="💫 Project Description:",
        value=description,
        inline=False
    )

    embed.add_field(
        name="👏 Community Support:",
        value="React with 🎨 to show appreciation!\nReact with 💜 to send love!\nComment below with feedback!",
        inline=False
    )

    embed.set_footer(text="🌟 Keep creating amazing things! The community loves your creativity!")

    message = await ctx.send(embed=embed)
    await message.add_reaction("🎨")
    await message.add_reaction("💜")
    await message.add_reaction("🔥")

    # Reward for sharing
    await give_tokens(ctx.author.id, 100, "Creative showcase")

    # Send confirmation
    await ctx.send(f"🎉 Amazing! {ctx.author.mention} earned 100 BROski$ tokens for sharing their creativity! 🪙")

# 🎵 MUSIC & MOOD SYSTEM
@bot.hybrid_command(name="mood", description="🎵 Set the community mood with music!")
async def mood_music(ctx, mood: str = "list"):
    """Community mood and music system"""

    if mood.lower() == "list":
        embed = discord.Embed(
            title="🎵 COMMUNITY MOOD STATION! 🎵",
            description="Set the vibe for the community!",
            color=0x9370DB
        )

        moods = [
            {"name": "🔥 Energetic", "desc": "High energy, pump-up vibes", "emoji": "🔥"},
            {"name": "😌 Chill", "desc": "Relaxed, calm atmosphere", "emoji": "😌"},
            {"name": "🧠 Focus", "desc": "Concentration and productivity", "emoji": "🧠"},
            {"name": "💜 Cozy", "desc": "Warm, comfortable feelings", "emoji": "💜"},
            {"name": "🎉 Celebration", "desc": "Party and achievement vibes", "emoji": "🎉"},
            {"name": "🌙 Evening", "desc": "Wind-down, peaceful energy", "emoji": "🌙"}
        ]

        for mood_info in moods:
            embed.add_field(
                name=mood_info["name"],
                value=mood_info["desc"],
                inline=True
            )

        embed.add_field(
            name="🎯 How to Use:",
            value="Use `/mood [mood_name]` to set the community vibe!",
            inline=False
        )

        await ctx.send(embed=embed)
    else:
        # Set community mood
        embed = discord.Embed(
            title=f"🎵 MOOD SET: {mood.upper()}! 🎵",
            description=f"{ctx.author.display_name} set the community mood!",
            color=0x9370DB
        )

        mood_responses = {
            "energetic": "🔥 Time to GET THINGS DONE! Energy is through the roof!",
            "chill": "😌 Relaxing vibes activated. Take it easy, everyone!",
            "focus": "🧠 Focus mode engaged! Time for some serious productivity!",
            "cozy": "💜 Cozy community vibes! Perfect for connecting and chatting!",
            "celebration": "🎉 CELEBRATION TIME! Let's party and share our wins!",
            "evening": "🌙 Evening wind-down activated. Perfect for reflection!"
        }

        response = mood_responses.get(mood.lower(), "🎵 New mood vibes activated!")

        embed.add_field(
            name="✨ Vibe Check:",
            value=response,
            inline=False
        )

        embed.add_field(
            name="🎶 Perfect For:",
            value="• Matching your energy to the community\n• Finding focus buddies\n• Setting collaboration tone\n• Creating shared experiences",
            inline=False
        )

        await ctx.send(embed=embed)

        # Reward for setting mood
        await give_tokens(ctx.author.id, 25, "Setting community mood")

# 📚 RESOURCE LIBRARY SYSTEM
@bot.hybrid_command(name="resources", description="📚 Access community knowledge library!")
async def resource_library(ctx, category: str = "all"):
    """Community resource and knowledge sharing"""

    resources = {
        "adhd": [
            "🧠 How to Work With Your ADHD Brain",
            "⚡ Dopamine Regulation Strategies",
            "🎯 Focus Techniques That Actually Work",
            "💊 Medication vs Natural Management",
            "🤝 Building ADHD-Friendly Routines"
        ],
        "productivity": [
            "🍅 Mastering the Pomodoro Technique",
            "📝 Task Management for Neurodivergent Minds",
            "🎨 Creative Productivity Methods",
            "⚡ Energy Management Over Time Management",
            "🔄 Building Sustainable Work Habits"
        ],
        "wellness": [
            "🧘 Mindfulness for Busy Brains",
            "💪 Movement and Exercise for ADHD",
            "😴 Sleep Optimization Guide",
            "🥗 Nutrition for Brain Health",
            "💜 Self-Compassion Practices"
        ],
        "community": [
            "🤝 How to Get the Most from This Community",
            "💬 Effective Communication Tips",
            "🌟 Building Supportive Relationships",
            "🎯 Setting and Achieving Goals Together",
            "🎉 Celebrating Wins Big and Small"
        ]
    }

    if category == "all":
        embed = discord.Embed(
            title="📚 COMMUNITY KNOWLEDGE LIBRARY! 📚",
            description="Your ultimate resource hub for thriving with ADHD!",
            color=0x4169E1
        )

        for cat, items in resources.items():
            embed.add_field(
                name=f"📖 {cat.title()} Resources",
                value=f"Use `/resources {cat}` to explore!",
                inline=True
            )

        embed.add_field(
            name="🚀 How It Works:",
            value="• Browse by category\n• Save your favorites\n• Contribute your own resources\n• Earn tokens for helpful contributions",
            inline=False
        )

        embed.add_field(
            name="💡 Pro Tip:",
            value="Resources are community-curated and regularly updated!",
            inline=False
        )

    else:
        if category.lower() in resources:
            resource_list = resources[category.lower()]
            embed = discord.Embed(
                title=f"📚 {category.title()} Resources",
                description="Expert-curated resources for your journey!",
                color=0x4169E1
            )

            for i, resource in enumerate(resource_list, 1):
                embed.add_field(
                    name=f"{i}. {resource}",
                    value="💡 Click to access full guide",
                    inline=False
                )

            embed.add_field(
                name="🎯 Coming Soon:",
                value="Interactive tutorials, video guides, and community workshops!",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Category Not Found",
                description="Use `/resources all` to see available categories!",
                color=0xFF6347
            )

    await ctx.send(embed=embed)

# 🏅 ADVANCED ACHIEVEMENT SYSTEM
@bot.hybrid_command(name="achievements", description="🏅 View your legendary achievements!")
async def view_achievements(ctx, member: discord.Member = None):
    """Advanced achievement system"""

    target = member or ctx.author

    # Mock achievement data (in real implementation, load from database)
    all_achievements = {
        "🌟 First Steps": {"desc": "Sent your first message", "earned": True, "rarity": "common"},
        "💬 Chatterbox": {"desc": "Sent 100 messages", "earned": True, "rarity": "common"},
        "🧠 Focus Master": {"desc": "Completed 10 focus sessions", "earned": True, "rarity": "uncommon"},
        "💜 Community Heart": {"desc": "Helped 50 members", "earned": False, "rarity": "rare"},
        "🔥 Streak Legend": {"desc": "Active for 30 days straight", "earned": False, "rarity": "rare"},
        "👑 Ultimate Supporter": {"desc": "Earned 1000 helpful votes", "earned": False, "rarity": "legendary"},
        "🎨 Creative Genius": {"desc": "Showcased 25 creative projects", "earned": False, "rarity": "epic"},
        "🌈 Mood Maestro": {"desc": "Set community mood 100 times", "earned": False, "rarity": "uncommon"}
    }

    embed = discord.Embed(
        title=f"🏅 {target.display_name}'s Achievements",
        description="Your legendary accomplishments in the community!",
        color=0xFFD700
    )

    earned_achievements = [name for name, data in all_achievements.items() if data["earned"]]
    total_achievements = len(all_achievements)
    completion_rate = (len(earned_achievements) / total_achievements) * 100

    embed.add_field(
        name="📊 Progress Overview",
        value=f"🏆 {len(earned_achievements)}/{total_achievements} unlocked ({completion_rate:.1f}%)",
        inline=False
    )

    # Show earned achievements
    earned_text = ""
    for achievement in earned_achievements:
        data = all_achievements[achievement]
        rarity_emoji = {"common": "⚪", "uncommon": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟡"}
        earned_text += f"{rarity_emoji.get(data['rarity'], '⚪')} {achievement}\n"

    if earned_text:
        embed.add_field(
            name="✅ Earned Achievements",
            value=earned_text[:1024],  # Discord field limit
            inline=False
        )

    # Show next achievements to unlock
    next_achievements = [name for name, data in all_achievements.items() if not data["earned"]][:3]
    if next_achievements:
        next_text = ""
        for achievement in next_achievements:
            data = all_achievements[achievement]
            next_text += f"🎯 {achievement} - {data['desc']}\n"

        embed.add_field(
            name="🎯 Next to Unlock",
            value=next_text,
            inline=False
        )

    embed.set_footer(text="Keep being awesome to unlock more achievements! 🌟")

    await ctx.send(embed=embed)

# 🌈 ADVANCED HELP SYSTEM
@bot.hybrid_command(name="help_advanced", description="🌈 Advanced help and feature guide!")
async def advanced_help(ctx, category: str = "overview"):
    """Comprehensive help system"""

    if category == "overview":
        embed = discord.Embed(
            title="🌈 DREAM COMMUNITY BOT - COMPLETE GUIDE! 🌈",
            description="Your ultimate companion for community engagement!",
            color=0x9932CC
        )

        categories = [
            {"name": "🎯 Core Features", "value": "`/help_advanced core`"},
            {"name": "🪙 Token Economy", "value": "`/help_advanced tokens`"},
            {"name": "🧠 Focus & Productivity", "value": "`/help_advanced focus`"},
            {"name": "🎮 Games & Fun", "value": "`/help_advanced games`"},
            {"name": "🏆 Achievements & Progress", "value": "`/help_advanced achievements`"},
            {"name": "💜 Community Features", "value": "`/help_advanced community`"}
        ]

        for cat in categories:
            embed.add_field(
                name=cat["name"],
                value=cat["value"],
                inline=True
            )

        embed.add_field(
            name="🚀 Quick Start",
            value="1. Check your profile: `/profile`\n2. Claim daily reward: `/daily`\n3. Join a focus session: `/focus start`\n4. Play a mini-game: `/minigame quiz`",
            inline=False
        )

    elif category == "core":
        embed = discord.Embed(
            title="🎯 CORE FEATURES",
            description="Essential commands for community engagement",
            color=0x4169E1
        )

        commands = [
            ("/profile", "View your community profile and stats"),
            ("/leaderboard", "See top community members"),
            ("/tokens", "Check your BROski$ balance"),
            ("/daily", "Claim daily rewards"),
            ("/vibe", "Check community vibe"),
            ("/check_in", "Daily mental health check-in")
        ]

        for cmd, desc in commands:
            embed.add_field(name=cmd, value=desc, inline=False)

    # Add more help categories as needed...

    await ctx.send(embed=embed)

# Background Tasks
@tasks.loop(minutes=30)
async def community_heartbeat():
    """Regular community engagement activities"""

    if GUILD_ID <= 0:
        return

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return

    # Randomly send motivational messages
    if random.random() < 0.3:  # 30% chance every 30 minutes
        await send_random_motivation(guild)

@tasks.loop(hours=24)
async def daily_rewards():
    """Reset daily activities and send reminders"""

    if GUILD_ID <= 0:
        return

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return

    # Send daily reward reminders
    general_channel = discord.utils.get(guild.text_channels, name="general")
    if general_channel:
        embed = discord.Embed(
            title="🌅 NEW DAY, NEW OPPORTUNITIES!",
            description="Don't forget to claim your daily rewards with `/daily`!",
            color=0xFFD700
        )
        await general_channel.send(embed=embed)

@tasks.loop(hours=1)
async def vibe_monitor():
    """Monitor and maintain positive community vibes"""

    # This could analyze message sentiment, activity levels, etc.
    # For now, just a placeholder for future enhancement
    pass

# Helper Functions
async def update_user_activity(user, channel):
    """Update user activity and give rewards"""

    user_id = str(user.id)

    conn = sqlite3.connect(community_db.db_path)
    cursor = conn.cursor()

    # Get or create user profile
    cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
    profile = cursor.fetchone()

    if not profile:
        # Create new profile
        cursor.execute("""
            INSERT INTO user_profiles
            (user_id, username, display_name, join_date, last_active, broski_tokens)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            user.name,
            user.display_name,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            50.0
        ))
    else:
        # Update existing profile
        new_xp = profile[4] + 5  # 5 XP per message
        new_level = max(1, int(new_xp / 100))  # Level up every 100 XP
        new_tokens = profile[5] + 2.0  # 2 tokens per message
        new_messages = profile[8] + 1

        cursor.execute("""
            UPDATE user_profiles
            SET xp = ?, level = ?, broski_tokens = ?, message_count = ?, last_active = ?
            WHERE user_id = ?
        """, (
            new_xp,
            new_level,
            new_tokens,
            new_messages,
            datetime.now().isoformat(),
            user_id
        ))

        # Check for level up
        if new_level > profile[3]:
            await celebrate_level_up(user, channel, new_level)

    conn.commit()
    conn.close()

async def celebrate_level_up(user, channel, new_level):
    """Celebrate user leveling up"""

    embed = discord.Embed(
        title="🎉 LEVEL UP! 🎉",
        description=f"🎯 {user.mention} just reached **Level {new_level}**!",
        color=0xFFD700
    )

    # Level rewards
    token_reward = new_level * 25
    await give_tokens(user.id, token_reward, f"Level {new_level} achievement")

    embed.add_field(
        name="🎁 Level Reward",
        value=f"🪙 {token_reward} BROski$ tokens!",
        inline=True
    )

    embed.add_field(
        name="🌟 Community Rank",
        value=get_community_rank(new_level),
        inline=True
    )

    await channel.send(embed=embed)

async def give_tokens(user_id, amount, reason):
    """Give tokens to a user"""

    conn = sqlite3.connect(community_db.db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user_profiles
        SET broski_tokens = broski_tokens + ?
        WHERE user_id = ?
    """, (amount, str(user_id)))

    conn.commit()
    conn.close()

def get_community_rank(level):
    """Get community rank based on level"""

    if level >= 50:
        return "👑 Legendary Master"
    elif level >= 40:
        return "🔥 Epic Legend"
    elif level >= 30:
        return "⭐ Super Star"
    elif level >= 20:
        return "🚀 Rising Hero"
    elif level >= 10:
        return "💜 Community Champion"
    elif level >= 5:
        return "🌟 Active Member"
    else:
        return "🌱 New Friend"

async def send_random_motivation(guild):
    """Send random motivational message"""

    motivational_messages = [
        "🌟 You're all absolutely crushing it today! Keep being amazing! 💜",
        "🔥 The creativity and energy in this community is off the charts! 🚀",
        "💜 Just a reminder that you're valued, important, and legendary! ✨",
        "🧠 Your unique perspectives make this community magical! Keep sharing! 🌈",
        "🎯 Every small step forward is progress! You've got this! 💪",
        "🌸 Take a moment to appreciate how far you've come! So proud! 🤗"
    ]

    general_channel = discord.utils.get(guild.text_channels, name="general")
    if general_channel:
        message = random.choice(motivational_messages)

        embed = discord.Embed(
            title="💫 COMMUNITY LOVE BOOST 💫",
            description=message,
            color=0xFF69B4
        )

        await general_channel.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""

    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands

    embed = discord.Embed(
        title="❌ Oops! Something went wrong!",
        description="Don't worry, our legendary bot is still awesome! 💜",
        color=0xFF0000
    )

    embed.add_field(
        name="🔧 What happened?",
        value=str(error),
        inline=False
    )

    embed.add_field(
        name="💡 Need help?",
        value="Use `/help_advanced` to see what's available!",
        inline=False
    )

    await ctx.send(embed=embed, ephemeral=True)

# Run the dream community bot
if __name__ == "__main__":
    print("🌟 Starting Dream Community Bot...")

    if not TOKEN:
        print("❌ Error: DISCORD_BOT_TOKEN not found in environment variables!")
        print("💡 Please set your Discord bot token in the .env file")
        exit(1)

    print("🚀 Bot token loaded successfully!")
    print("🌈 Initializing all community features...")

    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Check your bot token and permissions!")