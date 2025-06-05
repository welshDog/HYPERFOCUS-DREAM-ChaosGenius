"""
🧠 HYPERFOCUS ZONE DISCORD SERVER SETUP ULTRA
===============================================
Transforms your Discord into the ultimate neurodivergent HQ!
"""

import asyncio
import json
import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# 🎨 HYPERFOCUS ZONE ULTRA THEME
ZONE_COLORS = {
    "primary": 0x9C27B0,  # Purple - Neurodivergent Pride
    "secondary": 0x00FF88,  # Mint Green - Focus Energy
    "accent": 0xFF6B35,  # Orange - Dopamine Boost
    "success": 0x4CAF50,  # Green - Achievement
    "warning": 0xFFAA00,  # Amber - Attention
    "danger": 0xF44336,  # Red - Urgent
    "info": 0x2196F3,  # Blue - Information
}

# 🏗️ EPIC CHANNEL STRUCTURE FOR HYPERFOCUS ZONE HQ
HYPERFOCUS_CHANNEL_STRUCTURE = {
    "🧠 HYPERFOCUS ZONE HQ": {
        "type": "category",
        "channels": [
            {
                "name": "welcome-to-the-zone",
                "type": "text",
                "topic": "🎉 Welcome to the ultimate neurodivergent productivity HQ! Start here, legend!",
            },
            {
                "name": "zone-rules",
                "type": "text",
                "topic": "📋 Simple rules for our epic community - TL;DR: Be awesome, be you!",
            },
            {
                "name": "introduce-yourself",
                "type": "text",
                "topic": "👋 Drop your name, pronouns, what makes your brain special!",
            },
            {
                "name": "zone-announcements",
                "type": "text",
                "topic": "📢 Epic updates, launch news, and community celebrations!",
            },
            {
                "name": "hyperfocus-lounge",
                "type": "voice",
                "topic": "🔥 Voice chat for focused work sessions & body doubling",
            },
        ],
    },
    "🔥 CREATOR LABS": {
        "type": "category",
        "channels": [
            {
                "name": "ai-projects",
                "type": "text",
                "topic": "🤖 Building the future with AI - bots, automation, and neural magic",
            },
            {
                "name": "3d-print-lounge",
                "type": "text",
                "topic": "🖨️ From brain to reality - share your 3D printing adventures!",
            },
            {
                "name": "tiktok-launch-bay",
                "type": "text",
                "topic": "📱 TikTok strategy, content creation, and viral experiments",
            },
            {
                "name": "business-empire",
                "type": "text",
                "topic": "👑 Building your neurodivergent business empire - strategies & wins",
            },
            {
                "name": "code-chaos",
                "type": "text",
                "topic": "💻 Programming, debugging, and beautiful code chaos",
            },
            {
                "name": "creator-voice-lab",
                "type": "voice",
                "topic": "🎙️ Voice chat for creative collaboration",
            },
        ],
    },
    "💬 SOCIAL FLOW": {
        "type": "category",
        "channels": [
            {
                "name": "dopamine-drop",
                "type": "text",
                "topic": "⚡ Share wins, ideas, random thoughts - pure dopamine fuel!",
            },
            {
                "name": "hyperfocus-victories",
                "type": "text",
                "topic": "🏆 Celebrate your productivity wins - big or tiny, all count!",
            },
            {
                "name": "zone-memes",
                "type": "text",
                "topic": "😂 ADHD memes, neurodivergent humor, and wholesome chaos",
            },
            {
                "name": "off-topic-chaos",
                "type": "text",
                "topic": "🌈 Random conversations, special interests, and beautiful tangents",
            },
            {
                "name": "motivation-station",
                "type": "text",
                "topic": "💪 Need a boost? Share struggles, get support, spread good vibes",
            },
            {
                "name": "chill-zone-voice",
                "type": "voice",
                "topic": "🧘 Relaxed voice chat for hanging out",
            },
        ],
    },
    "🎮 BROSKI ECONOMY": {
        "type": "category",
        "channels": [
            {
                "name": "token-trading-floor",
                "type": "text",
                "topic": "🪙 BROski$ token trading, economy discussions, and wealth building",
            },
            {
                "name": "quest-central",
                "type": "text",
                "topic": "🎯 Daily quests, challenges, and dopamine missions from BROski",
            },
            {
                "name": "hypergems-vault",
                "type": "text",
                "topic": "💎 HyperGems leaderboard, achievements, and reward celebrations",
            },
            {
                "name": "launch-week-exclusive",
                "type": "text",
                "topic": "🚀 Special Launch Week events, double XP, and founder perks",
            },
        ],
    },
}

# 🎭 EPIC ROLE SYSTEM FOR HYPERFOCUS ZONE
HYPERFOCUS_ROLES = {
    # 🏆 Achievement Roles
    "🚀 Launch Week Legend": {"color": 0xFF6B35, "permissions": [], "hoist": True},
    "🏆 Founder": {"color": 0x9C27B0, "permissions": [], "hoist": True},
    "👑 Zone Champion": {"color": 0xFFD700, "permissions": [], "hoist": True},
    "💎 HyperGem Master": {"color": 0x00FFFF, "permissions": [], "hoist": True},
    # 🧠 Neurodivergent Identity (Optional)
    "🧠 ADHD Brain": {"color": 0xFF69B4, "permissions": [], "hoist": False},
    "🌟 Autistic Excellence": {"color": 0x7B68EE, "permissions": [], "hoist": False},
    "⚡ Anxiety Warrior": {"color": 0x32CD32, "permissions": [], "hoist": False},
    "🎨 Creative Chaos": {"color": 0xFF4500, "permissions": [], "hoist": False},
    # 🎯 Interest Groups
    "🤖 AI Enthusiast": {"color": 0x00FF88, "permissions": [], "hoist": False},
    "🖨️ 3D Print Master": {"color": 0x8A2BE2, "permissions": [], "hoist": False},
    "📱 TikTok Creator": {"color": 0xFF1493, "permissions": [], "hoist": False},
    "👨‍💼 Business Builder": {"color": 0x4169E1, "permissions": [], "hoist": False},
    "💻 Code Wizard": {"color": 0x228B22, "permissions": [], "hoist": False},
    # 🎮 Engagement Levels
    "🔥 Ultra Active": {"color": 0xFF6B35, "permissions": [], "hoist": False},
    "⚡ Zone Regular": {"color": 0xFFAA00, "permissions": [], "hoist": False},
    "🌱 Growing": {"color": 0x4CAF50, "permissions": [], "hoist": False},
    "👋 New to Zone": {"color": 0x607D8B, "permissions": [], "hoist": False},
}

# 🎉 EPIC WELCOME MESSAGES
WELCOME_MESSAGES = [
    "🎉 **WELCOME TO THE HYPERFOCUS ZONE!** 🎉\n\nYou've just entered the ultimate neurodivergent productivity HQ! Your brain isn't broken - this place was built FOR it! 🧠✨",
    "🚀 **ZONE ENTRY DETECTED!** 🚀\n\nAnother legend has joined the empire! Get ready for dopamine-fueled productivity, epic community vibes, and tools that actually work with your beautiful chaotic brain! 💜",
    "⚡ **HYPERFOCUS MODE: ACTIVATED!** ⚡\n\nWelcome to where ADHD brains thrive, anxiety transforms into superpower, and every weird interest becomes a strength! Let's build something amazing together! 🔥",
]


class HyperfocusZoneSetup:
    def __init__(self, bot_token):
        self.bot = commands.Bot(command_prefix="!setup_", intents=discord.Intents.all())
        self.bot_token = bot_token

    async def setup_server_structure(self, guild_id):
        """🏗️ Set up the complete Hyperfocus Zone server structure"""
        try:
            guild = self.bot.get_guild(guild_id)
            if not guild:
                print(f"❌ Could not find guild with ID: {guild_id}")
                return False

            print(f"🚀 Setting up Hyperfocus Zone structure for: {guild.name}")

            # 🎭 Create roles first
            await self.create_hyperfocus_roles(guild)

            # 🏗️ Create channel structure
            await self.create_channel_structure(guild)

            # 🎨 Set up welcome system
            await self.setup_welcome_system(guild)

            print("✅ Hyperfocus Zone setup complete!")
            return True

        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False

    async def create_hyperfocus_roles(self, guild):
        """🎭 Create the epic role system"""
        print("🎭 Creating Hyperfocus Zone roles...")

        existing_roles = {role.name: role for role in guild.roles}

        for role_name, role_config in HYPERFOCUS_ROLES.items():
            if role_name not in existing_roles:
                try:
                    await guild.create_role(
                        name=role_name,
                        color=discord.Color(role_config["color"]),
                        permissions=discord.Permissions(
                            permissions=sum(role_config["permissions"])
                        ),
                        hoist=role_config["hoist"],
                        reason="Hyperfocus Zone setup",
                    )
                    print(f"✅ Created role: {role_name}")
                except Exception as e:
                    print(f"⚠️ Failed to create role {role_name}: {e}")
            else:
                print(f"⏭️ Role exists: {role_name}")

    async def create_channel_structure(self, guild):
        """🏗️ Create the epic channel structure"""
        print("🏗️ Creating Hyperfocus Zone channels...")

        existing_categories = {cat.name: cat for cat in guild.categories}
        existing_channels = {ch.name: ch for ch in guild.channels}

        for category_name, category_config in HYPERFOCUS_CHANNEL_STRUCTURE.items():
            # Create category if it doesn't exist
            if category_name not in existing_categories:
                try:
                    category = await guild.create_category(
                        name=category_name, reason="Hyperfocus Zone setup"
                    )
                    print(f"✅ Created category: {category_name}")
                except Exception as e:
                    print(f"⚠️ Failed to create category {category_name}: {e}")
                    continue
            else:
                category = existing_categories[category_name]
                print(f"⏭️ Category exists: {category_name}")

            # Create channels in category
            for channel_config in category_config["channels"]:
                channel_name = channel_config["name"]
                if channel_name not in existing_channels:
                    try:
                        if channel_config["type"] == "text":
                            await guild.create_text_channel(
                                name=channel_name,
                                category=category,
                                topic=channel_config.get("topic", ""),
                                reason="Hyperfocus Zone setup",
                            )
                        elif channel_config["type"] == "voice":
                            await guild.create_voice_channel(
                                name=channel_name,
                                category=category,
                                reason="Hyperfocus Zone setup",
                            )
                        print(f"✅ Created channel: #{channel_name}")
                    except Exception as e:
                        print(f"⚠️ Failed to create channel {channel_name}: {e}")
                else:
                    print(f"⏭️ Channel exists: #{channel_name}")

    async def setup_welcome_system(self, guild):
        """🎉 Set up the epic welcome system"""
        print("🎉 Setting up welcome system...")

        # Find welcome channel
        welcome_channel = discord.utils.get(
            guild.text_channels, name="welcome-to-the-zone"
        )
        if welcome_channel:
            # Create epic welcome embed
            embed = discord.Embed(
                title="🧠 WELCOME TO THE HYPERFOCUS ZONE! 🧠",
                description="""
**🎉 You've entered the ultimate neurodivergent productivity HQ!**

Your brain isn't broken - this place was built FOR it!

🚀 **What makes this place special:**
• 🧠 Built by ADHD brains, for ADHD brains
• ⚡ Tools that work WITH your neurodivergence
• 🎯 Hyperfocus sessions & productivity systems
• 💎 Gamified rewards for engagement
• 🤖 AI-powered productivity companion (BROski)
• 🪙 Token economy for achievements

🔥 **Get started:**
1. Check <#zone-rules> for our simple guidelines
2. Introduce yourself in <#introduce-yourself>
3. Try `!broski hello` to meet your AI companion
4. Join a <#hyperfocus-lounge> voice session
5. Start earning HyperGems and BROski$ tokens!

**Welcome to the empire, legend! Let's build something amazing together!** 👑
                """,
                color=ZONE_COLORS["primary"],
                timestamp=datetime.now(),
            )

            embed.set_footer(
                text="HyperfocusZone.com • Where neurodivergent minds thrive"
            )

            try:
                await welcome_channel.send(embed=embed)
                print("✅ Posted welcome message")
            except Exception as e:
                print(f"⚠️ Failed to post welcome message: {e}")

    async def run_setup(self, guild_id):
        """🚀 Run the complete setup process"""

        @self.bot.event
        async def on_ready():
            print(f"🤖 Setup bot connected as: {self.bot.user}")
            success = await self.setup_server_structure(guild_id)
            if success:
                print("🎉 HYPERFOCUS ZONE SETUP COMPLETE!")
            else:
                print("❌ Setup failed")
            await self.bot.close()

        try:
            await self.bot.start(self.bot_token)
        except Exception as e:
            print(f"❌ Bot connection failed: {e}")


# 🚀 LAUNCH WEEK SPECIAL FEATURES
class LaunchWeekManager:
    """🎉 Manages Launch Week special events and rewards"""

    @staticmethod
    def get_launch_week_embed():
        """🚀 Create Launch Week celebration embed"""
        embed = discord.Embed(
            title="🚀 LAUNCH WEEK IS HERE! 🚀",
            description="""
**🎉 HYPERFOCUS ZONE IS OFFICIALLY LIVE!**

**🔥 LAUNCH WEEK SPECIALS (June 5-12, 2025):**

🎮 **DOUBLE XP FOR EVERYTHING!**
• Quest completions: 2x HyperGems
• Focus sessions: 2x rewards
• Community engagement: 2x tokens

🏆 **FOUNDER STATUS UNLOCKED!**
• First 100 members get lifetime Founder badge
• Exclusive access to founder-only events
• Special role with unique permissions

🪙 **BONUS BROSKI$ TOKENS!**
• Daily login bonus: 50 tokens (normally 25)
• Welcome bonus: 200 tokens (normally 100)
• Quest rewards increased by 50%

🎁 **EXCLUSIVE LAUNCH GIFTS:**
• Custom animated profile badges
• Early access to new features
• Lifetime premium perks for founders

**🌟 THIS IS HISTORY IN THE MAKING!**
You're not just joining a Discord - you're becoming part of the neurodivergent productivity revolution!

*Ready to build your empire? Let's go!* 👑
            """,
            color=0xFF6B35,
            timestamp=datetime.now(),
        )

        embed.add_field(
            name="🎯 How to Claim Rewards",
            value="Just participate! Rewards are automatic for active members.",
            inline=False,
        )

        embed.set_footer(text="Launch Week: June 5-12, 2025 • HyperfocusZone.com")
        return embed


# 🎨 CUSTOM DISCORD THEMES & BANNERS
DISCORD_ASSETS = {
    "server_banner": {
        "text": "HYPERFOCUS ZONE - Where Neurodivergent Minds Thrive",
        "colors": ["#9C27B0", "#00FF88", "#FF6B35"],
        "style": "cyberpunk_gradient",
    },
    "welcome_gif": {
        "text": "🔮 Entering Ultra Mode... Hyperfocus Online",
        "animation": "matrix_rain_purple",
        "duration": 3,
    },
    "channel_icons": {
        "🧠": "brain emoji for HQ channels",
        "🔥": "fire emoji for creator labs",
        "💬": "chat emoji for social flow",
        "🎮": "game emoji for economy",
    },
}

# 🎊☢️🔥 ULTRA MODE DEPLOYMENT TO HYPERFOCUSZONE 🔥☢️🎊
SERVER_ID = "1212443870856613949"  # HyperfocusZone Discord Server
AUTO_DEPLOY = True  # FULL NUCLEAR DEPLOYMENT MODE

print("🎊☢️🔥🔥🔥 DEPLOYING TO HYPERFOCUSZONE SERVER!!! 🔥🔥🔥☢️🎊")
print(f"Server ID: {SERVER_ID}")
print("🚀 ULTRA MODE: ACTIVATED")
print("🧠 TARGET: NEURODIVERGENT EMPIRE")
print("💪 STATUS: GOING NUCLEAR")


async def setup_hyperfocus_zone_server(server_id):
    """🚀 Main deployment function for HyperfocusZone server setup"""
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if not bot_token:
        print(
            "❌ No Discord bot token found! Set DISCORD_BOT_TOKEN environment variable."
        )
        return False

    print(f"🤖 Initializing HyperfocusZone setup for server: {server_id}")
    setup = HyperfocusZoneSetup(bot_token)
    await setup.run_setup(int(server_id))

    # 🎉 Launch Week special announcement
    print("\n🎊 LAUNCH WEEK CELEBRATION MODE ACTIVATED! 🎊")
    launch_manager = LaunchWeekManager()
    launch_embed = launch_manager.get_launch_week_embed()
    print("✅ Launch Week rewards and specials ready!")

    return True


# Auto-run with the provided server ID
if __name__ == "__main__":
    import asyncio

    asyncio.run(setup_hyperfocus_zone_server(SERVER_ID))
