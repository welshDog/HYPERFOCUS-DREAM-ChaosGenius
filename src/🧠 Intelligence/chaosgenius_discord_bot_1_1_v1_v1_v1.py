"""🧠 ChaosGenius Discord Bot - HYPERFOCUSZONE EDITION"""

# Remove unused imports
import asyncio
import json
import logging
import os
import random
import sqlite3

# BROski AI integration
import sys
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import discord
import requests
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

sys.path.append("/root/chaosgenius")
from ai_modules.broski.broski_core import BROskiCore

# 🪙 Add BROski$ Token Economy integration
try:
    from ai_modules.broski.token_commands import BROskiTokenCommands
    from ai_modules.broski.token_engine import BROskiTokenEngine

    TOKENS_AVAILABLE = True
    logger = logging.getLogger("ChaosGeniusBot")
    logger.info("🪙 BROski$ Token Economy loaded successfully!")
except ImportError as e:
    logger = logging.getLogger("ChaosGeniusBot")
    logger.warning("⚠️ BROski$ Token system not available: %s", e)
    TOKENS_AVAILABLE = False

# 🔐 Load environment variables securely
load_dotenv()

# 🚨 SECURE Bot Configuration
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("🚨 WARNING: DISCORD_BOT_TOKEN not found in environment variables!")
    print(
        "🔎 Running in DEV MODE: Discord bot will not connect, but commands can be simulated."
    )
    TOKEN = None  # Dev mode: do not exit, allow script to run for local testing

# 📝 Enhanced logging for production - FIXED ENCODING ISSUE
# Ensure logs directory exists
logs_dir = Path("logs")
logs_dir.mkdir(parents=True, exist_ok=True)

# Configure logging with rotation
log_file = logs_dir / "discord_bot.log"
rotating_handler = RotatingFileHandler(
    log_file,
    maxBytes=2 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8",
    errors="replace",
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[rotating_handler, logging.StreamHandler()],
)
logger = logging.getLogger("ChaosGeniusBot")

# Log security status
logger.info("🔐 Security: Environment variables loaded successfully")
logger.info(f"🔐 Security: Token loaded: {'✅' if TOKEN else '❌'}")

# 🧠 Intents for full ChaosGenius integration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


# 🧪 Bot setup with ChaosGenius prefix - ENHANCED FOR SLASH COMMANDS
class ChaosGeniusBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Setup slash commands on startup"""
        await self.tree.sync()
        logger.info("🚀 Slash commands synchronized!")


bot = ChaosGeniusBot()


# 🗄️ Database connection to ChaosGenius with enhanced error handling
def get_db_connection():
    try:
        conn = sqlite3.connect("chaosgenius.db")
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
            "broski$": 0,
            "daily_streak": 0,
            "last_active": datetime.now(),
            "quests_completed": 0,
            "mood_history": [],
            "preferences": {},
        }
    return user_profiles[user_id]


# 💥💜☢️ NEXT-GEN DISCORD FEATURES - ULTRA BROSKI ARSENAL ☢️💜💥


# 🎯 1. SLASH COMMANDS - THE BROSKI ARSENAL
@bot.tree.command(
    name="broski",
    description="🧠 Chat with BROski AI - Your neurodivergent productivity companion",
)
@app_commands.describe(message="What's on your mind? BROski is here to help!")
async def broski_slash(interaction: discord.Interaction, message: str = None):
    """🧠 Enhanced slash command for BROski AI chat"""

    if not message:
        embed = discord.Embed(
            title="🧠 BROski ClanVerse Ultra AI",
            description="Your neurodivergent productivity companion is here!",
            color=0x00FF88,
        )
        embed.add_field(
            name="💬 How to Chat",
            value="`/broski [your message]`\nExample: `/broski I'm feeling overwhelmed with my tasks`",
            inline=False,
        )
        embed.add_field(
            name="🎯 What I Can Help With",
            value="• ADHD-friendly productivity tips\n• Mood analysis & support\n• Hyperfocus session guidance\n• Personalized motivation\n• Task organization strategies",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    await interaction.response.defer()

    try:
        # Build context for BROski
        context = {
            "platform": "discord_slash",
            "server_name": interaction.guild.name if interaction.guild else "DM",
            "channel_name": (
                interaction.channel.name
                if hasattr(interaction.channel, "name")
                else "direct"
            ),
            "interaction_type": "slash_command",
        }

        # Process with BROski AI
        broski_ai = BROskiCore()
        response = await broski_ai.process_user_interaction(
            str(interaction.user.id), message, context
        )

        # Create rich embed response with interactive buttons
        embed = discord.Embed(
            title=f"🧠 BROski {response.style.replace('_', ' ').title()}",
            description=response.message,
            color=0x00FF88,
            timestamp=datetime.now(),
        )

        # Add mood and energy info
        embed.add_field(
            name="🎭 Detected Mood",
            value=f"{response.mood_detected.title()} (Confidence: {response.confidence:.1%})",
            inline=True,
        )
        embed.add_field(
            name="⚡ Energy Level",
            value=f"{response.energy_level}/100",
            inline=True,
        )

        # Add motivation boost if available
        if response.motivation_boost:
            embed.add_field(
                name="💪 Motivation Boost",
                value=response.motivation_boost,
                inline=False,
            )

        # Create interactive view with buttons
        view = BROskiInteractiveView(response, interaction.user.id)

        await interaction.followup.send(embed=embed, view=view)

    except Exception as e:
        logger.error(f"Error in BROski slash command: {e}")
        embed = discord.Embed(
            title="🔧 BROski Brain Glitch",
            description="I'm having a quick moment, but I'm still here for you! Try again in a sec.",
            color=0xFF9900,
        )
        await interaction.followup.send(embed=embed, ephemeral=True)


@bot.tree.command(
    name="energy-check", description="⚡ Check your current dopamine and energy levels"
)
async def energy_check_slash(interaction: discord.Interaction):
    """⚡ Slash command for energy level checking"""
    profile = init_user_profile(interaction.user.id)

    # Calculate dynamic stats
    hours_since_active = (
        datetime.now() - profile["last_active"]
    ).total_seconds() / 3600
    dopamine_level = max(20, profile["dopamine"] - int(hours_since_active * 2))

    # Create energy HUD
    embed = discord.Embed(
        title=f"⚡ Energy Check - {interaction.user.display_name}",
        color=(
            0xFF6B35
            if dopamine_level > 60
            else 0xFFAA00 if dopamine_level > 30 else 0x666666
        ),
    )

    # Energy bars
    dopamine_bar = "█" * int(dopamine_level / 10) + "░" * (
        10 - int(dopamine_level / 10)
    )
    embed.add_field(
        name="⚡ Dopamine Level",
        value=f"`{dopamine_bar}` {dopamine_level}%",
        inline=False,
    )
    embed.add_field(name="💎 BROski$", value=str(profile["broski$"]), inline=True)
    embed.add_field(
        name="🔥 Daily Streak", value=f"{profile['daily_streak']} days", inline=True
    )

    # Add interactive buttons for energy management
    view = EnergyManagementView(profile, interaction.user.id)

    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(
    name="token-balance", description="💰 Check your BROski$ token balance"
)
async def token_balance_slash(interaction: discord.Interaction):
    """💰 Check BROski$ token balance via slash command"""
    if not TOKENS_AVAILABLE:
        await interaction.response.send_message(
            "🚧 Token system is currently in development mode!", ephemeral=True
        )
        return

    try:
        token_engine = BROskiTokenEngine()
        balance_info = token_engine.get_balance(str(interaction.user.id))

        embed = discord.Embed(
            title="💰 BROski$ Wallet",
            description=f"**{interaction.user.display_name}'s Token Empire**",
            color=0xFFD700,
        )

        embed.add_field(
            name="💎 Current Balance",
            value=f"{balance_info.get('balance', 0)} BROski$",
            inline=True,
        )
        embed.add_field(
            name="📈 Total Earned",
            value=f"{balance_info.get('total_earned', 0)} BROski$",
            inline=True,
        )
        embed.add_field(
            name="🏆 Rank", value=balance_info.get("rank", "Newcomer"), inline=True
        )

        # Add token earning buttons
        view = TokenManagementView(interaction.user.id)

        await interaction.response.send_message(embed=embed, view=view)

    except Exception as e:
        logger.error(f"Token balance error: {e}")
        await interaction.response.send_message(
            "🔧 Token system temporarily unavailable!", ephemeral=True
        )


@bot.tree.command(
    name="support-me",
    description="🧠 Summon the dopamine squad for motivation and support",
)
async def support_me_slash(interaction: discord.Interaction, mood: str = None):
    """🧠 Summon personalized support from the dopamine squad"""

    # Mood options for better targeting
    mood_options = {
        "overwhelmed": "🫂 Overwhelm protocol activated! You're not alone in this.",
        "bored": "🎯 Boredom detected! Time for a dopamine quest!",
        "excited": "🚀 High energy detected! Let's channel this into something epic!",
        "tired": "🛌 Rest mode engaged. Your brain needs recharge time.",
        "stuck": "🧩 Problem-solving mode activated! Let's break this down.",
        "anxious": "⛑️ Anxiety support incoming. Deep breaths with BROski.",
    }

    if mood and mood.lower() in mood_options:
        support_message = mood_options[mood.lower()]
    else:
        support_message = (
            "💜 The dopamine squad is here! You're doing better than you think."
        )

    embed = discord.Embed(
        title="🧠 Dopamine Squad Activated!",
        description=support_message,
        color=0x9C27B0,
    )

    embed.add_field(
        name="🎯 Instant Support Options",
        value="• Take 3 deep breaths\n• Drink some water\n• Do a 2-minute body scan\n• Share what you're feeling\n• Start a 10-minute focus session",
        inline=False,
    )

    # Add support action buttons
    view = SupportSquadView(interaction.user.id, mood)

    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(
    name="upgrade-role", description="🚀 Trade tokens for cooler Discord roles"
)
async def upgrade_role_slash(interaction: discord.Interaction):
    """🚀 Role upgrade system with token trading"""

    embed = discord.Embed(
        title="🚀 Role Upgrade Shop",
        description="Trade your BROski$ tokens for exclusive roles!",
        color=0xFF6B35,
    )

    # Available role upgrades
    role_upgrades = {
        "🌟 Rising Star": {
            "cost": 500,
            "description": "Special color + priority support",
        },
        "💎 BROski$ Master": {
            "cost": 1000,
            "description": "Exclusive channels + custom emoji",
        },
        "🚀 Rocket Booster": {
            "cost": 2000,
            "description": "Voice channel privileges + beta access",
        },
        "👑 Zone Champion": {
            "cost": 5000,
            "description": "All perks + direct line to founders",
        },
    }

    role_text = ""
    for role, info in role_upgrades.items():
        role_text += (
            f"**{role}**\nCost: {info['cost']} BROski$\n{info['description']}\n\n"
        )

    embed.add_field(name="🛍️ Available Upgrades", value=role_text, inline=False)

    # Add role selection buttons
    view = RoleUpgradeView(interaction.user.id, role_upgrades)

    await interaction.response.send_message(embed=embed, view=view)


# 🧠 2. BROSKI BOOST MODALS (POP-UP FORMS)
class IdeaSubmissionModal(discord.ui.Modal, title="💡 Share Your Brainwave"):
    """Modal for submitting creative ideas to the Ultra Squad"""

    idea_title = discord.ui.TextInput(
        label="🎯 Idea Title",
        placeholder="What's your amazing idea called?",
        max_length=100,
    )

    idea_description = discord.ui.TextInput(
        label="💭 Description",
        placeholder="Tell us about your idea! No judgment, pure creativity welcome.",
        style=discord.TextStyle.paragraph,
        max_length=2000,
    )

    category = discord.ui.TextInput(
        label="🗂️ Category (optional)",
        placeholder="e.g., business, creative, tech, life",
        required=False,
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Save idea to database or file
        idea_data = {
            "title": self.idea_title.value,
            "description": self.idea_description.value,
            "category": self.category.value or "general",
            "user": interaction.user.name,
            "user_id": interaction.user.id,
            "timestamp": datetime.now().isoformat(),
            "status": "submitted",
        }

        # Create ideas directory if it doesn't exist
        ideas_dir = Path("production_assets/community_ideas")
        ideas_dir.mkdir(parents=True, exist_ok=True)

        # Save idea to file
        idea_file = (
            ideas_dir
            / f"idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{interaction.user.id}.json"
        )
        with open(idea_file, "w", encoding="utf-8") as f:
            json.dump(idea_data, f, indent=2)

        # Award tokens for sharing
        profile = init_user_profile(interaction.user.id)
        profile["broski$"] += 10

        embed = discord.Embed(
            title="💡 Idea Captured!",
            description=f"**{self.idea_title.value}** has been added to the Ultra Squad review queue!",
            color=0x4CAF50,
        )
        embed.add_field(name="💎 Reward", value="10 BROski$ earned!", inline=True)
        embed.add_field(
            name="🎯 Status", value="Under review by the Ultra Squad", inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Log idea submission
        logger.info(
            f"Idea submitted by {interaction.user.name}: {self.idea_title.value}"
        )


class BugReportModal(discord.ui.Modal, title="🐛 Bug Report with Style"):
    """Modal for reporting bugs in a fun way"""

    bug_title = discord.ui.TextInput(
        label="🐛 What's Acting Up?",
        placeholder="Give your bug a creative name!",
        max_length=100,
    )

    bug_description = discord.ui.TextInput(
        label="📝 What Happened?",
        placeholder="Describe the chaos! When did it happen? What were you trying to do?",
        style=discord.TextStyle.paragraph,
        max_length=2000,
    )

    reproduction_steps = discord.ui.TextInput(
        label="🔄 How to Recreate It",
        placeholder="Step-by-step instructions to make the bug appear again",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=1000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Save bug report
        bug_data = {
            "title": self.bug_title.value,
            "description": self.bug_description.value,
            "reproduction_steps": self.reproduction_steps.value,
            "reporter": interaction.user.name,
            "user_id": interaction.user.id,
            "timestamp": datetime.now().isoformat(),
            "status": "open",
        }

        # Create bug reports directory
        bugs_dir = Path("logs/bug_reports")
        bugs_dir.mkdir(parents=True, exist_ok=True)

        # Save bug report
        bug_file = (
            bugs_dir
            / f"bug_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{interaction.user.id}.json"
        )
        with open(bug_file, "w", encoding="utf-8") as f:
            json.dump(bug_data, f, indent=2)

        # Award tokens for helpful reporting
        profile = init_user_profile(interaction.user.id)
        profile["broski$"] += 15

        embed = discord.Embed(
            title="🐛 Bug Captured!",
            description=f"**{self.bug_title.value}** is now in our bug-hunting queue!",
            color=0xFFAA00,
        )
        embed.add_field(
            name="💎 Bug Hunter Reward", value="15 BROski$ earned!", inline=True
        )
        embed.add_field(
            name="🔧 Status", value="Our devs are on the case!", inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Log bug report
        logger.info(f"Bug reported by {interaction.user.name}: {self.bug_title.value}")


# 🎛️ 3. HYPERCONTROL PANEL (BUTTONS & DROPDOWNS)
class BROskiInteractiveView(discord.ui.View):
    """Interactive buttons for BROski AI responses"""

    def __init__(self, broski_response, user_id):
        super().__init__(timeout=300)  # 5 minutes
        self.broski_response = broski_response
        self.user_id = user_id

    @discord.ui.button(
        label="💡 More Tips", style=discord.ButtonStyle.primary, emoji="💡"
    )
    async def more_tips(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This panel is for someone else! Use `/broski` to get your own.",
                ephemeral=True,
            )
            return

        # Get additional recommendations
        additional_tips = (
            self.broski_response.recommendations[1:4]
            if len(self.broski_response.recommendations) > 1
            else [
                "Take a 5-minute movement break",
                "Hydrate your beautiful brain",
                "Celebrate this moment of self-awareness",
            ]
        )

        embed = discord.Embed(
            title="💡 Additional BROski Tips",
            description="\n".join(f"• {tip}" for tip in additional_tips),
            color=0x00FF88,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🎯 Start Focus Session", style=discord.ButtonStyle.green, emoji="🎯"
    )
    async def start_focus(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This panel is for someone else!", ephemeral=True
            )
            return

        # Quick focus session embed
        embed = discord.Embed(
            title="🎯 Quick Focus Session Started!",
            description="25-minute hyperfocus session activated! BROski believes in you!",
            color=0xFF6600,
        )
        embed.add_field(name="⏰ Duration", value="25 minutes", inline=True)
        embed.add_field(name="🧠 Mode", value="Neurodivergent Optimized", inline=True)
        embed.add_field(
            name="🎵 Suggestion", value="Try lo-fi or brown noise", inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="💎 Daily Quest", style=discord.ButtonStyle.secondary, emoji="💎"
    )
    async def daily_quest(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This panel is for someone else!", ephemeral=True
            )
            return

        # Generate a quick quest based on current mood
        quest_types = {
            "tired": "Share something that made you smile today",
            "excited": "Channel that energy into a 10-minute creative burst",
            "stressed": "Do 3 deep breaths and name 3 things you're grateful for",
            "creative": "Sketch your current mood in emoji form",
            "default": "Do one small thing that future-you will thank you for",
        }

        mood = self.broski_response.mood_detected
        quest = quest_types.get(mood, quest_types["default"])

        embed = discord.Embed(
            title="💎 Daily Quest Activated!",
            description=f"**Your Quest:** {quest}",
            color=0xFF6B35,
        )
        embed.add_field(
            name="💰 Reward", value="5 BROski$ + dopamine boost!", inline=True
        )
        embed.add_field(
            name="⏰ Time Limit", value="No pressure - when you're ready!", inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class EnergyManagementView(discord.ui.View):
    """Energy level management buttons"""

    def __init__(self, profile, user_id):
        super().__init__(timeout=300)
        self.profile = profile
        self.user_id = user_id

    @discord.ui.button(
        label="⚡ Energy Boost", style=discord.ButtonStyle.green, emoji="⚡"
    )
    async def energy_boost(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This is someone else's energy panel!", ephemeral=True
            )
            return

        # Boost energy
        self.profile["dopamine"] = min(100, self.profile["dopamine"] + 15)
        self.profile["last_active"] = datetime.now()

        embed = discord.Embed(
            title="⚡ Energy Boost Applied!",
            description="Your dopamine levels have been recharged! You're ready to take on the world!",
            color=0x4CAF50,
        )
        embed.add_field(
            name="New Energy Level", value=f"{self.profile['dopamine']}%", inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🧘 Rest Mode", style=discord.ButtonStyle.secondary, emoji="🧘"
    )
    async def rest_mode(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This is someone else's energy panel!", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🧘 Rest Mode Activated",
            description="Permission to rest granted! Your brain needs recharge time.",
            color=0x9C27B0,
        )
        embed.add_field(
            name="🛌 Rest Tips",
            value="• Close your eyes for 5 minutes\n• Do gentle stretches\n• Listen to calming music\n• Practice gratitude",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class SupportSquadView(discord.ui.View):
    """Support options for when users need help"""

    def __init__(self, user_id, mood):
        super().__init__(timeout=600)  # 10 minutes for support
        self.user_id = user_id
        self.mood = mood

    @discord.ui.button(
        label="💬 Talk to Someone", style=discord.ButtonStyle.primary, emoji="💬"
    )
    async def talk_to_someone(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = discord.Embed(
            title="💬 Community Support",
            description="The Hyperfocus Zone community is here for you!",
            color=0x9C27B0,
        )
        embed.add_field(
            name="🫂 Where to Connect",
            value="• #support-circle - For serious conversations\n• #hyperfocus-lounge - For body doubling\n• #random-dopamine - For light chat\n• #wins-and-struggles - Share your journey",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🎯 Quick Focus", style=discord.ButtonStyle.green, emoji="🎯"
    )
    async def quick_focus(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = discord.Embed(
            title="🎯 Quick Focus Protocol",
            description="Let's get you back in the zone!",
            color=0xFF6600,
        )
        embed.add_field(
            name="5-Minute Reset",
            value="1. Take 3 deep breaths\n2. Drink some water\n3. Look at something far away\n4. Set one tiny goal\n5. Start with 2 minutes of that goal",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


# 🎛️ 4. DROPDOWN SELECTORS FOR BROSKI PATHS
class BROskiPathSelector(discord.ui.Select):
    """Dropdown for selecting your BROski path/specialty"""

    def __init__(self):
        options = [
            discord.SelectOption(
                label="🎨 Creative Chaos",
                description="Art, design, content creation",
                emoji="🎨",
            ),
            discord.SelectOption(
                label="💻 Code Wizard",
                description="Programming, tech, automation",
                emoji="💻",
            ),
            discord.SelectOption(
                label="📈 Business Builder",
                description="Entrepreneurship, strategy, growth",
                emoji="📈",
            ),
            discord.SelectOption(
                label="🧠 Wellness Warrior",
                description="Mental health, self-care, balance",
                emoji="🧠",
            ),
            discord.SelectOption(
                label="🎮 Community Champion",
                description="Helping others, moderation, support",
                emoji="🎮",
            ),
            discord.SelectOption(
                label="🔬 Researcher",
                description="Analysis, deep dives, learning",
                emoji="🔬",
            ),
        ]

        super().__init__(
            placeholder="Choose your BROski specialization...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]

        # Update user profile with chosen path
        profile = init_user_profile(interaction.user.id)
        profile["broski_path"] = selected

        # Award path selection bonus
        profile["broski$"] += 25

        path_info = {
            "🎨 Creative Chaos": {
                "welcome": "Welcome to the Creative Chaos path! Your imagination is your superpower!",
                "perks": "• Access to #creative-chaos channel\n• Daily creative prompts\n• Art showcase opportunities\n• Design collaboration invites",
            },
            "💻 Code Wizard": {
                "welcome": "Welcome to the Code Wizard path! Logic meets creativity in your brain!",
                "perks": "• Access to #code-realm channel\n• Programming challenges\n• Code review requests\n• Tech project collaboration",
            },
            "📈 Business Builder": {
                "welcome": "Welcome to the Business Builder path! Your entrepreneurial spirit is unstoppable!",
                "perks": "• Access to #empire-builders channel\n• Business idea feedback\n• Startup resources\n• Networking opportunities",
            },
            "🧠 Wellness Warrior": {
                "welcome": "Welcome to the Wellness Warrior path! You understand that health is wealth!",
                "perks": "• Access to #wellness-zone channel\n• Self-care reminders\n• Wellness challenges\n• Mental health resources",
            },
            "🎮 Community Champion": {
                "welcome": "Welcome to the Community Champion path! You make this place special!",
                "perks": "• Helper role consideration\n• Community event planning\n• Moderation training\n• Leadership opportunities",
            },
            "🔬 Researcher": {
                "welcome": "Welcome to the Researcher path! Your curiosity drives innovation!",
                "perks": "• Access to #deep-dives channel\n• Research collaboration\n• Fact-checking privileges\n• Knowledge sharing rewards",
            },
        }

        info = path_info.get(
            selected, {"welcome": "Path selected!", "perks": "Coming soon!"}
        )

        embed = discord.Embed(
            title=f"🎯 Path Chosen: {selected}",
            description=info["welcome"],
            color=0x4CAF50,
        )
        embed.add_field(name="🎁 Your Perks", value=info["perks"], inline=False)
        embed.add_field(
            name="💎 Bonus Reward",
            value="25 BROski$ for choosing your path!",
            inline=True,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class BROskiPathView(discord.ui.View):
    """View containing the BROski path selector"""

    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(BROskiPathSelector())


@bot.tree.command(
    name="dashboard", description="🎛️ Open your personal BROski control dashboard"
)
async def dashboard_slash(interaction: discord.Interaction):
    """🎛️ Personal dashboard with all controls"""

    profile = init_user_profile(interaction.user.id)

    embed = discord.Embed(
        title="🎛️ Your BROski Dashboard",
        description=f"Welcome back, {interaction.user.display_name}! Ready to conquer the day?",
        color=0x9C27B0,
    )

    # User stats
    embed.add_field(name="⚡ Energy", value=f"{profile['dopamine']}%", inline=True)
    embed.add_field(name="💎 BROski$", value=str(profile["broski$"]), inline=True)
    embed.add_field(
        name="🏆 Quests", value=str(profile["quests_completed"]), inline=True
    )

    # Quick stats
    embed.add_field(
        name="🔥 Streak", value=f"{profile['daily_streak']} days", inline=True
    )
    embed.add_field(
        name="🎯 Path", value=profile.get("broski_path", "Not chosen"), inline=True
    )
    embed.add_field(
        name="📊 Level", value=f"{min(10, profile['broski$'] // 100)}", inline=True
    )

    # Create dashboard view with all controls
    view = DashboardView(profile, interaction.user.id)

    await interaction.response.send_message(embed=embed, view=view)


class DashboardView(discord.ui.View):
    """Complete dashboard with all BROski controls"""

    def __init__(self, profile, user_id):
        super().__init__(timeout=600)  # 10 minutes
        self.profile = profile
        self.user_id = user_id

        # Add path selector if not chosen
        if not profile.get("broski_path"):
            self.add_item(BROskiPathSelector())

    @discord.ui.button(
        label="💡 Submit Idea", style=discord.ButtonStyle.primary, emoji="💡", row=0
    )
    async def submit_idea(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Open idea submission modal"""
        await interaction.response.send_modal(IdeaSubmissionModal())

    @discord.ui.button(
        label="🐛 Report Bug", style=discord.ButtonStyle.secondary, emoji="🐛", row=0
    )
    async def report_bug(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Open bug report modal"""
        await interaction.response.send_modal(BugReportModal())

    @discord.ui.button(
        label="🎯 Quick Focus", style=discord.ButtonStyle.green, emoji="🎯", row=0
    )
    async def quick_focus_session(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Start a quick focus session"""
        embed = discord.Embed(
            title="🎯 Quick Focus Session",
            description="15-minute hyperfocus mode activated!",
            color=0xFF6600,
        )
        embed.add_field(
            name="🧠 Focus Tips",
            value="• Close unnecessary tabs\n• Put phone in another room\n• Set a clear micro-goal\n• Use pomodoro timer",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🎲 Random Quest", style=discord.ButtonStyle.secondary, emoji="🎲", row=1
    )
    async def random_quest(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Get a random dopamine quest"""
        quests = [
            "Share a photo of your workspace",
            "Compliment someone in a random channel",
            "Share your current hyperfocus subject",
            "Do 10 jumping jacks and report back",
            "Share a random skill you have",
            "Post your favorite productivity tip",
            "Share what you're grateful for today",
        ]

        quest = random.choice(quests)

        embed = discord.Embed(
            title="🎲 Random Quest Activated!",
            description=f"**Your Mission:** {quest}",
            color=0xFF6B35,
        )
        embed.add_field(name="💰 Reward", value="5-10 BROski$", inline=True)
        embed.add_field(name="⏰ Deadline", value="When you feel like it!", inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🎮 Mini-Game", style=discord.ButtonStyle.primary, emoji="🎮", row=1
    )
    async def mini_game(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Start a mini-game"""
        # Create a simple reaction-based game
        embed = discord.Embed(
            title="🎮 Reaction Game!",
            description="First to react with 🚀 wins BROski$!\nGame starts in 3... 2... 1...",
            color=0xFF6B35,
        )

        message = await interaction.response.send_message(embed=embed)

        # Add reaction after a random delay
        await asyncio.sleep(random.uniform(2, 5))
        try:
            msg = await interaction.original_response()
            await msg.add_reaction("🚀")
        except:
            pass


# 💰 TOKEN MANAGEMENT VIEW
class TokenManagementView(discord.ui.View):
    """Token earning and management buttons"""

    def __init__(self, user_id):
        super().__init__(timeout=300)
        self.user_id = user_id

    @discord.ui.button(
        label="💰 Earn Tokens", style=discord.ButtonStyle.green, emoji="💰"
    )
    async def earn_tokens(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This wallet belongs to someone else!", ephemeral=True
            )
            return

        # Show token earning methods
        embed = discord.Embed(
            title="💰 Token Earning Guide",
            description="Here's how to build your BROski$ empire!",
            color=0xFFD700,
        )

        earning_methods = """
        **🎯 Daily Activities:**
        • Chat with BROski AI - 5 BROski$
        • Complete daily quests - 10-25 BROski$
        • Submit creative ideas - 15 BROski$
        • Help other members - 20 BROski$

        **🏆 Special Rewards:**
        • Bug reports - 30 BROski$
        • Community events - 50 BROski$
        • Content creation - 100 BROski$
        • Epic contributions - 500 BROski$
        """

        embed.add_field(name="💎 How to Earn", value=earning_methods, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="📊 Leaderboard", style=discord.ButtonStyle.secondary, emoji="📊"
    )
    async def leaderboard(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # Show top token holders (mock data for now)
        embed = discord.Embed(
            title="📊 BROski$ Leaderboard",
            description="The top token earners in our neurodivergent empire!",
            color=0xFF6B35,
        )

        # Mock leaderboard data
        leaderboard_data = """
        🥇 **HyperFocus_Hero** - 15,420 BROski$
        🥈 **Creative_Chaos** - 12,890 BROski$
        🥉 **Code_Wizard_Pro** - 9,560 BROski$
        4️⃣ **Dopamine_Queen** - 7,230 BROski$
        5️⃣ **Focus_Master** - 6,780 BROski$
        """

        embed.add_field(name="🏆 Top Earners", value=leaderboard_data, inline=False)
        embed.add_field(
            name="🎯 Your Position",
            value="Check back after earning more tokens!",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


# 🚀 ROLE UPGRADE VIEW
class RoleUpgradeView(discord.ui.View):
    """Role upgrade selection buttons"""

    def __init__(self, user_id, role_upgrades):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.role_upgrades = role_upgrades

        # Create buttons for each role
        for i, (role_name, info) in enumerate(role_upgrades.items()):
            if i < 4:  # Discord limit of 5 buttons per row
                button = discord.ui.Button(
                    label=f"{role_name.split()[1]} - {info['cost']} BROski$",
                    style=discord.ButtonStyle.primary,
                    custom_id=f"role_{i}",
                    emoji=role_name.split()[0],
                )
                button.callback = self.create_role_callback(role_name, info)
                self.add_item(button)

    def create_role_callback(self, role_name, info):
        async def role_callback(interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(
                    "This shop is for someone else!", ephemeral=True
                )
                return

            # Check if user has enough tokens (mock check for now)
            profile = init_user_profile(interaction.user.id)
            current_gems = profile["broski$"]

            if current_gems < info["cost"]:
                embed = discord.Embed(
                    title="💸 Insufficient Funds",
                    description=f"You need {info['cost']} BROski$ but only have {current_gems}!",
                    color=0xFF4444,
                )
                embed.add_field(
                    name="💡 How to Earn More",
                    value="Use `/dashboard` to find earning opportunities!",
                    inline=False,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # Process role upgrade
            profile["broski$"] -= info["cost"]

            embed = discord.Embed(
                title="🚀 Role Upgrade Successful!",
                description=f"Congratulations! You've unlocked **{role_name}**!",
                color=0x4CAF50,
            )
            embed.add_field(
                name="✨ New Perks", value=info["description"], inline=False
            )
            embed.add_field(
                name="💰 Remaining Balance",
                value=f"{profile['broski$']} BROski$",
                inline=True,
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Log role upgrade
            logger.info(f"Role upgrade: {interaction.user.name} purchased {role_name}")

        return role_callback


# 🎮 5. VOICE CHANNEL INTEGRATION - BROSKI VOICE COMPANION
@bot.tree.command(
    name="voice-summon",
    description="🎤 Summon BROski to your voice channel for motivation",
)
async def voice_summon_slash(interaction: discord.Interaction):
    """🎤 Summon BROski to voice channels for motivation"""

    # Check if user is in a voice channel
    if not interaction.user.voice or not interaction.user.voice.channel:
        embed = discord.Embed(
            title="🎤 Voice Channel Required",
            description="Join a voice channel first, then summon me for some epic motivation!",
            color=0xFF9900,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    voice_channel = interaction.user.voice.channel

    embed = discord.Embed(
        title="🎤 BROski Voice Mode Activated!",
        description=f"I'm virtually joining **{voice_channel.name}** for some neurodivergent excellence!",
        color=0x9C27B0,
    )

    # Voice mode features
    features = """
    **🧠 Available Features:**
    • Pomodoro timer announcements
    • Hourly motivation check-ins
    • Focus session guidance
    • Background lo-fi suggestions
    • Group accountability mode
    """

    embed.add_field(name="🎯 Voice Features", value=features, inline=False)
    embed.add_field(
        name="⏰ Duration", value="Active while you're in the channel", inline=True
    )
    embed.add_field(
        name="🔧 Controls", value="Use `/voice-stop` to end session", inline=True
    )

    # Create voice control view
    view = VoiceControlView(interaction.user.id, voice_channel.id)

    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(
    name="focus-room",
    description="🧘 Transform voice channel into a focus room with timer",
)
async def focus_room_slash(interaction: discord.Interaction, duration: int = 25):
    """🧘 Create a focus room in voice channel"""

    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message(
            "Join a voice channel first!", ephemeral=True
        )
        return

    if duration < 5 or duration > 120:
        await interaction.response.send_message(
            "Duration must be between 5-120 minutes!", ephemeral=True
        )
        return

    voice_channel = interaction.user.voice.channel

    embed = discord.Embed(
        title="🧘 Focus Room Activated!",
        description=f"**{voice_channel.name}** is now a hyperfocus zone for {duration} minutes!",
        color=0xFF6600,
    )

    focus_tips = f"""
    **🎯 {duration}-Minute Focus Protocol:**
    • Silence notifications
    • Set clear micro-goals
    • Stay hydrated
    • Trust the process

    **🎵 Recommended Audio:**
    • Brown noise or lo-fi
    • Nature sounds
    • Instrumental music
    • Binaural beats
    """

    embed.add_field(name="🧠 Focus Guide", value=focus_tips, inline=False)
    embed.add_field(
        name="⏰ Timer", value=f"{duration} minutes starting now!", inline=True
    )
    embed.add_field(name="🔔 Check-in", value="I'll ping when time's up!", inline=True)

    # Create focus room controls
    view = FocusRoomView(interaction.user.id, voice_channel.id, duration)

    await interaction.response.send_message(embed=embed, view=view)

    # Start focus timer (simplified version)
    logger.info(f"Focus room started: {duration} minutes in {voice_channel.name}")


class VoiceControlView(discord.ui.View):
    """Controls for voice channel features"""

    def __init__(self, user_id, channel_id):
        super().__init__(timeout=3600)  # 1 hour
        self.user_id = user_id
        self.channel_id = channel_id

    @discord.ui.button(
        label="⏰ Start Pomodoro", style=discord.ButtonStyle.green, emoji="⏰"
    )
    async def start_pomodoro(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = discord.Embed(
            title="⏰ Pomodoro Timer Started!",
            description="25 minutes of focused work ahead! BROski believes in you!",
            color=0xFF6600,
        )
        embed.add_field(
            name="🎯 Focus Mode", value="Deep work session activated", inline=True
        )
        embed.add_field(
            name="🔔 Break Alert",
            value="I'll remind you when it's break time",
            inline=True,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🎵 Lo-Fi Vibes", style=discord.ButtonStyle.secondary, emoji="🎵"
    )
    async def lofi_recommendation(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        lofi_suggestions = [
            "🎵 Search 'lofi hip hop radio' on YouTube",
            "🌧️ Try 'rain sounds for studying' playlist",
            "🌊 Brown noise generators are perfect for ADHD",
            "🎼 'Chillhop' playlists on Spotify",
            "🕯️ 'Study with me' videos for body doubling",
        ]

        suggestion = random.choice(lofi_suggestions)

        embed = discord.Embed(
            title="🎵 Audio Recommendation",
            description=f"**Perfect for your neurodivergent brain:** {suggestion}",
            color=0x9C27B0,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🧠 Motivation Boost", style=discord.ButtonStyle.primary, emoji="🧠"
    )
    async def motivation_boost(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        motivational_quotes = [
            "Your ADHD brain is wired for innovation! 🚀",
            "Hyperfocus is your superpower - channel it! ⚡",
            "Every small step counts in your empire! 👑",
            "Your neurodivergent perspective is valuable! 💎",
            "Rest is productive too - honor your brain! 🧘",
            "You're exactly where you need to be! 🌟",
        ]

        quote = random.choice(motivational_quotes)

        embed = discord.Embed(
            title="🧠 BROski Motivation Boost",
            description=quote,
            color=0x4CAF50,
        )
        embed.add_field(
            name="💪 Remember",
            value="You're building something amazing, one step at a time!",
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class FocusRoomView(discord.ui.View):
    """Controls for focus room sessions"""

    def __init__(self, user_id, channel_id, duration):
        super().__init__(timeout=duration * 60)  # Duration in seconds
        self.user_id = user_id
        self.channel_id = channel_id
        self.duration = duration
        self.start_time = datetime.now()

    @discord.ui.button(
        label="📊 Progress Check", style=discord.ButtonStyle.secondary, emoji="📊"
    )
    async def progress_check(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        elapsed = (datetime.now() - self.start_time).total_seconds() / 60
        remaining = max(0, self.duration - elapsed)
        progress = min(100, (elapsed / self.duration) * 100)

        embed = discord.Embed(
            title="📊 Focus Session Progress",
            description=f"You're {progress:.1f}% through your focus session!",
            color=0xFF6600,
        )

        progress_bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
        embed.add_field(
            name="⏰ Progress",
            value=f"`{progress_bar}` {remaining:.1f} min left",
            inline=False,
        )

        if progress > 50:
            embed.add_field(
                name="🎉 Great Work!",
                value="You're over halfway! Keep that momentum!",
                inline=True,
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="🛑 End Session", style=discord.ButtonStyle.danger, emoji="🛑"
    )
    async def end_session(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        elapsed = (datetime.now() - self.start_time).total_seconds() / 60

        embed = discord.Embed(
            title="🛑 Focus Session Ended",
            description=f"Session completed! You focused for {elapsed:.1f} minutes.",
            color=0x4CAF50,
        )

        if elapsed >= self.duration * 0.8:  # 80% completion
            embed.add_field(
                name="🏆 Achievement",
                value="Focus Champion! You completed most of your session!",
                inline=False,
            )
            # Award bonus gems
            profile = init_user_profile(interaction.user.id)
            profile["broski$"] += 20

            embed.add_field(
                name="💎 Focus Reward",
                value="20 BROski$ for focus excellence!",
                inline=True,
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)


# 🎮 6. MINI-GAMES & INTERACTIVE CHALLENGES
@bot.tree.command(name="gem-rush", description="💎 Quick reaction game to earn BROski$")
async def gem_rush_slash(interaction: discord.Interaction):
    """💎 Reaction-based mini-game for earning gems"""

    embed = discord.Embed(
        title="💎 BROski$ Rush!",
        description="Get ready for a reaction challenge! First to react wins gems!",
        color=0xFF6B35,
    )
    embed.add_field(
        name="🎯 How to Play",
        value="Watch for the 💎 emoji and be first to react!",
        inline=False,
    )
    embed.add_field(name="🏆 Rewards", value="Winner gets 25 BROski$!", inline=True)
    embed.add_field(name="⏰ Game starts in", value="3... 2... 1...", inline=True)

    await interaction.response.send_message(embed=embed)

    # Random delay before adding reaction
    delay = random.uniform(3, 8)
    await asyncio.sleep(delay)

    try:
        message = await interaction.original_response()
        await message.add_reaction("💎")

        # Set up reaction handler
        def check(reaction, user):
            return (
                str(reaction.emoji) == "💎"
                and user != bot.user
                and reaction.message.id == message.id
            )

        try:
            reaction, user = await bot.wait_for(
                "reaction_add", timeout=30.0, check=check
            )

            # Award winner
            profile = init_user_profile(user.id)
            profile["broski$"] += 25

            winner_embed = discord.Embed(
                title="🏆 We Have a Winner!",
                description=f"**{user.display_name}** wins the BROski$ Rush!",
                color=0x4CAF50,
            )
            winner_embed.add_field(name="💎 Prize", value="25 BROski$!", inline=True)
            winner_embed.add_field(
                name="⚡ Reaction Time", value="Lightning fast!", inline=True
            )

            await message.edit(embed=winner_embed)

        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="⏰ Time's Up!",
                description="No one claimed the gems this time! Better luck next round!",
                color=0xFF9900,
            )
            await message.edit(embed=timeout_embed)

    except Exception as e:
        logger.error(f"Gem rush game error: {e}")


@bot.tree.command(
    name="brain-quiz", description="🧠 Neurodivergent trivia quiz for tokens"
)
async def brain_quiz_slash(interaction: discord.Interaction):
    """🧠 Educational quiz about neurodivergence and productivity"""

    quiz_questions = [
        {
            "question": "What percentage of the population is estimated to have ADHD?",
            "options": ["A) 2-3%", "B) 5-10%", "C) 15-20%", "D) 25-30%"],
            "correct": "B",
            "explanation": "About 5-10% of the population has ADHD, making it quite common!",
        },
        {
            "question": "Which of these is a common ADHD superpower?",
            "options": [
                "A) Hyperfocus",
                "B) Creative thinking",
                "C) Problem-solving",
                "D) All of the above",
            ],
            "correct": "D",
            "explanation": "ADHD brains often excel at hyperfocus, creativity, and innovative problem-solving!",
        },
        {
            "question": "What's the best way to support someone with executive dysfunction?",
            "options": [
                "A) Tell them to try harder",
                "B) Break tasks into tiny steps",
                "C) Set strict deadlines",
                "D) Work in complete silence",
            ],
            "correct": "B",
            "explanation": "Breaking tasks into small, manageable steps helps overcome executive dysfunction!",
        },
        {
            "question": "Which environment often works best for neurodivergent focus?",
            "options": [
                "A) Complete silence",
                "B) Busy coffee shop",
                "C) Whatever feels right for that person",
                "D) Bright fluorescent lighting",
            ],
            "correct": "C",
            "explanation": "Every neurodivergent brain is unique - the best environment is what works for that individual!",
        },
    ]

    question = random.choice(quiz_questions)

    embed = discord.Embed(
        title="🧠 BROski Brain Quiz",
        description=question["question"],
        color=0x9C27B0,
    )

    options_text = "\n".join(question["options"])
    embed.add_field(name="📝 Options", value=options_text, inline=False)
    embed.add_field(name="💎 Reward", value="Correct answer = 15 BROski$!", inline=True)
    embed.add_field(name="⏰ Time Limit", value="30 seconds to answer!", inline=True)

    # Create quiz view
    view = QuizView(question, interaction.user.id)

    await interaction.response.send_message(embed=embed, view=view)


class QuizView(discord.ui.View):
    """Interactive quiz with multiple choice buttons"""

    def __init__(self, question_data, user_id):
        super().__init__(timeout=30)
        self.question_data = question_data
        self.user_id = user_id
        self.answered = False

        # Create buttons for each option
        for option in question_data["options"]:
            letter = option[0]  # A, B, C, or D
            button = discord.ui.Button(
                label=option,
                style=discord.ButtonStyle.secondary,
                custom_id=f"quiz_{letter}",
            )
            button.callback = self.create_answer_callback(letter)
            self.add_item(button)

    def create_answer_callback(self, selected_letter):
        async def answer_callback(interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(
                    "This quiz is for someone else!", ephemeral=True
                )
                return

            if self.answered:
                await interaction.response.send_message(
                    "You already answered this question!", ephemeral=True
                )
                return

            self.answered = True

            is_correct = selected_letter == self.question_data["correct"]

            if is_correct:
                # Award gems for correct answer
                profile = init_user_profile(interaction.user.id)
                profile["broski$"] += 15

                embed = discord.Embed(
                    title="🎉 Correct!",
                    description=f"**{selected_letter})** is the right answer!",
                    color=0x4CAF50,
                )
                embed.add_field(
                    name="💎 Reward", value="15 BROski$ earned!", inline=True
                )
            else:
                embed = discord.Embed(
                    title="❌ Not Quite",
                    description=f"The correct answer was **{self.question_data['correct']})**",
                    color=0xFF9900,
                )
                embed.add_field(
                    name="💡 Keep Learning",
                    value="Every question helps you grow!",
                    inline=True,
                )

            embed.add_field(
                name="🧠 Explanation",
                value=self.question_data["explanation"],
                inline=False,
            )

            # Disable all buttons
            for item in self.children:
                item.disabled = True

            await interaction.response.edit_message(embed=embed, view=self)

        return answer_callback


# 🎯 7. DAILY MISSIONS & QUEST SYSTEM
@bot.tree.command(
    name="daily-mission", description="🎯 Get your personalized daily mission"
)
async def daily_mission_slash(interaction: discord.Interaction):
    """🎯 Generate personalized daily missions"""

    profile = init_user_profile(interaction.user.id)
    user_path = profile.get("broski_path", "general")

    # Mission categories based on user's chosen path
    mission_categories = {
        "🎨 Creative Chaos": [
            "Create something for 15 minutes",
            "Share a creative tip in #creative-chaos",
            "Sketch your current mood",
            "Try a new creative technique",
            "Inspire someone with your art",
        ],
        "💻 Code Wizard": [
            "Write 25 lines of code",
            "Debug a tricky problem",
            "Share a coding tip",
            "Learn one new programming concept",
            "Help someone with their code",
        ],
        "📈 Business Builder": [
            "Brainstorm 3 business ideas",
            "Research a successful entrepreneur",
            "Plan one business task",
            "Network with another builder",
            "Share a business insight",
        ],
        "🧠 Wellness Warrior": [
            "Practice 10 minutes of mindfulness",
            "Share a wellness tip",
            "Do gentle movement for 15 minutes",
            "Check in with your emotions",
            "Help someone feel better",
        ],
        "general": [
            "Complete one important task",
            "Help another community member",
            "Share something you're grateful for",
            "Learn something new",
            "Do something kind for yourself",
        ],
    }

    missions = mission_categories.get(user_path, mission_categories["general"])
    daily_mission = random.choice(missions)

    # Calculate mission reward based on complexity
    base_reward = 20
    bonus_multiplier = profile.get("daily_streak", 0) // 7 + 1  # Bonus for streaks
    total_reward = base_reward * bonus_multiplier

    embed = discord.Embed(
        title="🎯 Your Daily Mission",
        description=f"**Today's Challenge:** {daily_mission}",
        color=0xFF6B35,
    )

    embed.add_field(name="💰 Reward", value=f"{total_reward} BROski$", inline=True)
    embed.add_field(
        name="🔥 Streak Bonus", value=f"x{bonus_multiplier} multiplier!", inline=True
    )
    embed.add_field(name="⏰ Deadline", value="Complete anytime today!", inline=True)

    # Add mission completion tracking
    embed.add_field(
        name="✅ How to Complete",
        value="React with ✅ when done, or use `/complete-mission` with proof!",
        inline=False,
    )

    # Create mission tracking view
    view = MissionView(daily_mission, total_reward, interaction.user.id)

    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(
    name="complete-mission", description="✅ Mark your daily mission as complete"
)
@app_commands.describe(proof="Optional: Share what you accomplished!")
async def complete_mission_slash(interaction: discord.Interaction, proof: str = None):
    """✅ Complete daily mission and earn rewards"""

    profile = init_user_profile(interaction.user.id)

    # Check if mission already completed today
    last_mission = profile.get("last_mission_date")
    today = datetime.now().strftime("%Y-%m-%d")

    if last_mission == today:
        embed = discord.Embed(
            title="✅ Mission Already Complete!",
            description="You've already completed today's mission! Come back tomorrow for a new challenge.",
            color=0x4CAF50,
        )
        embed.add_field(
            name="🎉 Great Job!",
            value="Your consistency is building your empire!",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Complete the mission
    profile["last_mission_date"] = today
    profile["daily_streak"] = profile.get("daily_streak", 0) + 1
    profile["quests_completed"] = profile.get("quests_completed", 0) + 1

    # Calculate rewards
    base_reward = 20
    streak_bonus = profile["daily_streak"] // 7 * 10
    total_reward = base_reward + streak_bonus
    profile["broski$"] += total_reward

    embed = discord.Embed(
        title="🎉 Mission Complete!",
        description="Outstanding work! Your consistency is paying off!",
        color=0x4CAF50,
    )

    embed.add_field(
        name="💎 Rewards Earned", value=f"{total_reward} BROski$", inline=True
    )
    embed.add_field(
        name="🔥 Daily Streak", value=f"{profile['daily_streak']} days", inline=True
    )
    embed.add_field(
        name="🏆 Total Quests", value=f"{profile['quests_completed']}", inline=True
    )

    if proof:
        embed.add_field(name="📝 Your Accomplishment", value=proof, inline=False)

    # Special rewards for streak milestones
    if profile["daily_streak"] % 7 == 0:  # Weekly milestone
        bonus_gems = profile["daily_streak"] * 5
        profile["broski$"] += bonus_gems
        embed.add_field(
            name="🌟 Streak Bonus!",
            value=f"{bonus_gems} extra gems for {profile['daily_streak']} day streak!",
            inline=False,
        )

    await interaction.response.send_message(embed=embed)

    # Log mission completion
    logger.info(
        f"Mission completed by {interaction.user.name}: {profile['daily_streak']} day streak"
    )


class MissionView(discord.ui.View):
    """Interactive mission completion tracking"""

    def __init__(self, mission_text, reward, user_id):
        super().__init__(timeout=86400)  # 24 hours
        self.mission_text = mission_text
        self.reward = reward
        self.user_id = user_id

    @discord.ui.button(
        label="✅ Complete Mission", style=discord.ButtonStyle.green, emoji="✅"
    )
    async def complete_mission(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This mission belongs to someone else!", ephemeral=True
            )
            return

        # Open completion modal
        await interaction.response.send_modal(
            MissionCompletionModal(self.mission_text, self.reward)
        )

    @discord.ui.button(
        label="🎲 New Mission", style=discord.ButtonStyle.secondary, emoji="🎲"
    )
    async def new_mission(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "Get your own mission with `/daily-mission`!", ephemeral=True
            )
            return

        # Generate a quick alternative mission
        quick_missions = [
            "Do 5 minutes of deep breathing",
            "Organize one small area",
            "Send a supportive message to someone",
            "Write down 3 things you're grateful for",
            "Take a 10-minute walk",
        ]

        alternative = random.choice(quick_missions)

        embed = discord.Embed(
            title="🎲 Alternative Mission",
            description=f"**Quick Option:** {alternative}",
            color=0xFF6B35,
        )
        embed.add_field(name="💰 Reward", value="15 BROski$", inline=True)
        embed.add_field(name="⏰ Duration", value="Quick & easy!", inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)


class MissionCompletionModal(discord.ui.Modal, title="🎉 Mission Complete!"):
    """Modal for mission completion with optional proof"""

    def __init__(self, mission_text, reward):
        super().__init__()
        self.mission_text = mission_text
        self.reward = reward

    accomplishment = discord.ui.TextInput(
        label="📝 What did you accomplish?",
        placeholder="Share your success! What did you do? How did it feel?",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=500,
    )

    feeling = discord.ui.TextInput(
        label="🎭 How are you feeling?",
        placeholder="Accomplished? Proud? Tired? Share your vibe!",
        required=False,
        max_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction):
        profile = init_user_profile(interaction.user.id)

        # Check if already completed today
        today = datetime.now().strftime("%Y-%m-%d")
        if profile.get("last_mission_date") == today:
            await interaction.response.send_message(
                "You already completed today's mission!", ephemeral=True
            )
            return

        # Complete mission
        profile["last_mission_date"] = today
        profile["daily_streak"] = profile.get("daily_streak", 0) + 1
        profile["quests_completed"] = profile.get("quests_completed", 0) + 1
        profile["broski$"] += self.reward

        embed = discord.Embed(
            title="🎉 Mission Accomplished!",
            description=f"**Mission:** {self.mission_text}",
            color=0x4CAF50,
        )

        embed.add_field(name="💎 Rewards", value=f"{self.reward} BROski$", inline=True)
        embed.add_field(
            name="🔥 Streak", value=f"{profile['daily_streak']} days", inline=True
        )

        if self.accomplishment.value:
            embed.add_field(
                name="📝 Your Success", value=self.accomplishment.value, inline=False
            )

        if self.feeling.value:
            embed.add_field(name="🎭 Your Vibe", value=self.feeling.value, inline=True)

        await interaction.response.send_message(embed=embed)


# Enhanced message processing for mood detection and responses
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 🧠 Dopamine Scanner in action
    detected_mood = detect_mood(message.content)

    # Avoid responding to short messages or commands
    if (
        detected_mood
        and len(message.content) > 20
        and not message.content.startswith("/")
    ):
        user_profile = init_user_profile(message.author.id)

        # Update mood history
        user_profile["mood_history"].append(
            {
                "mood": detected_mood,
                "timestamp": datetime.now().isoformat(),
                "channel": (
                    message.channel.name if hasattr(message.channel, "name") else "DM"
                ),
            }
        )

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

            # Award BROski$ for engagement
            user_profile["broski$"] += 1

            # Log mood detection
            logger.info(f"Mood detected: {detected_mood} for {message.author.name}")

    await bot.process_commands(message)


# 🚀 BOT STARTUP AND STATUS
@bot.event
async def on_ready():
    """Enhanced startup sequence with feature announcements"""
    logger.info(f"🚀 {bot.user} is online and ready for neurodivergent excellence!")

    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="for /broski commands | Hyperfocus Zone",
    )
    await bot.change_presence(activity=activity)

    # Log all available slash commands
    commands = [cmd.name for cmd in bot.tree.get_commands()]
    logger.info(f"📋 Available slash commands: {', '.join(commands)}")

    print("\n💥💜☢️ ULTRA BROSKI BOT IS LIVE! ☢️💜💥")
    print("🎯 Next-Gen Features Activated:")
    print("  • Slash Commands (/broski, /energy-check, /dashboard)")
    print("  • Interactive Modals & Forms")
    print("  • Voice Channel Integration")
    print("  • Mini-Games & Quests")
    print("  • Token Economy & Role Upgrades")
    print("  • Advanced Mood Detection")
    print("🚀 Ready to transform Discord into a neurodivergent empire!")


# 🔧 ERROR HANDLING AND LOGGING
@bot.event
async def on_application_command_error(
    interaction: discord.Interaction, error: Exception
):
    """Handle slash command errors gracefully"""
    logger.error(f"Slash command error: {error}")

    if not interaction.response.is_done():
        embed = discord.Embed(
            title="🔧 Oops! Something Went Wrong",
            description="BROski had a quick brain glitch, but we're still here for you!",
            color=0xFF9900,
        )
        embed.add_field(
            name="💡 Try This",
            value="• Wait a moment and try again\n• Use `/broski help` for command info\n• Report bugs with `/dashboard`",
            inline=False,
        )

        try:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            try:
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                pass  # Can't send message, log it instead
                logger.error(f"Could not send error message to {interaction.user.name}")


# 🎮 MAIN EXECUTION
if __name__ == "__main__":
    if TOKEN:
        logger.info("🚀 Starting ChaosGenius Discord Bot...")
        try:
            bot.run(TOKEN)
        except Exception as e:
            logger.error(f"Bot startup failed: {e}")
            print(f"🚨 Bot failed to start: {e}")
    else:
        logger.info("🔧 Running in development mode (no Discord token)")
        print("🔧 Development mode: Discord bot would start here with a valid token")
        print(
            "💡 Add DISCORD_BOT_TOKEN to your .env file to enable Discord integration"
        )
