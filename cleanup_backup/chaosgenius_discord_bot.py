#!/usr/bin/env python3
"""
🎮👑 BROSKI DISCORD BOT - ULTRA LEGENDARY EDITION 👑🎮
The most INSANE Discord bot ever created with BROski$ economy system!
Official Discord Server: https://discord.gg/chyXCC4zj2
🚀 FEATURING: Auto-earning, Events, Portal upgrades, AI integration! 🚀
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime

import discord
from discord.ext import commands

# Add the chaosgenius directory to Python path
sys.path.append("/root/chaosgenius")

# Import our LEGENDARY modules
try:
    from broski_auto_earner import BROskiAutoEarner
    from broski_portal_discord_commands import BROskiPortalCommands

    print("✅ LEGENDARY modules loaded!")
except ImportError as e:
    print(f"❌ Module import error: {e}")
    print("💡 Make sure all BROski modules are in the correct directory!")

# 🔥 Load the new Focus Engine commands
try:
    from broski_focus_engine import BroskiFocusCommands

    print("✅ BROski Focus Engine loaded!")
    FOCUS_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Focus Engine not available: {e}")
    FOCUS_ENGINE_AVAILABLE = False

# 🚶‍♂️ Load the Community Walker system
try:
    from broski_community_walker import BroskiCommunityWalkerCommands

    print("✅ BROski Community Walker loaded!")
    COMMUNITY_WALKER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Community Walker not available: {e}")
    COMMUNITY_WALKER_AVAILABLE = False

# 💼 Load the Gig Marketplace system
try:
    from broski_gig_marketplace import BroskiGigMarketplaceCommands

    print("✅ BROski Gig Marketplace loaded!")
    GIG_MARKETPLACE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Gig Marketplace not available: {e}")
    GIG_MARKETPLACE_AVAILABLE = False

# 🎮 BOT CONFIGURATION
DISCORD_TOKEN_FILE = "/root/chaosgenius/broski_token_config.json"
OFFICIAL_DISCORD_INVITE = "https://discord.gg/chyXCC4zj2"

# 🔥 LEGENDARY BOT INTENTS
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.reactions = True

# 🚀 CREATE THE LEGENDARY BOT
bot = commands.Bot(
    command_prefix=["!broski ", "!b ", "/"],
    intents=intents,
    description="🎮 BROski Discord Portal - The most LEGENDARY Discord bot ever created!",
    help_command=None,  # We'll create our own LEGENDARY help command
)

# 📊 BOT STATS TRACKING
bot_stats = {
    "start_time": None,
    "commands_used": 0,
    "tokens_distributed": 0,
    "active_users": set(),
    "servers_count": 0,
}


def load_discord_token():
    """Load Discord bot token from config"""
    try:
        if os.path.exists(DISCORD_TOKEN_FILE):
            with open(DISCORD_TOKEN_FILE, "r") as f:
                config = json.load(f)
                return config.get("discord_token")
        else:
            print(f"❌ Token file not found: {DISCORD_TOKEN_FILE}")
            print("💡 Create the token file with your Discord bot token!")
            return None
    except Exception as e:
        print(f"❌ Token loading error: {e}")
        return None


@bot.event
async def on_ready():
    """Bot startup - LEGENDARY ACTIVATION SEQUENCE!"""
    bot_stats["start_time"] = datetime.now()
    bot_stats["servers_count"] = len(bot.guilds)

    print("🚀" * 50)
    print("💥 BROSKI DISCORD BOT - ULTRA LEGENDARY EDITION 💥")
    print("🚀" * 50)
    print(f"🤖 Bot Name: {bot.user.name}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"🌐 Connected to {len(bot.guilds)} servers")
    print(f"👥 Total users: {sum(guild.member_count for guild in bot.guilds)}")
    print(f"🔗 Official Discord: {OFFICIAL_DISCORD_INVITE}")
    print("🚀" * 50)

    # Set LEGENDARY status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="🎮 BROski Portal | /help | discord.gg/chyXCC4zj2",
        ),
        status=discord.Status.online,
    )

    # Load LEGENDARY cogs
    try:
        await bot.add_cog(BROskiPortalCommands(bot))
        await bot.add_cog(BROskiAutoEarner(bot))

        # Load Focus Engine if available
        if FOCUS_ENGINE_AVAILABLE:
            await bot.add_cog(BroskiFocusCommands(bot))
            print("🧠 Focus Engine cog loaded!")

        # Load Community Walker if available
        if COMMUNITY_WALKER_AVAILABLE:
            await bot.add_cog(BroskiCommunityWalkerCommands(bot))
            print("🚶‍♂️ Community Walker cog loaded!")

        # Load Gig Marketplace if available
        if GIG_MARKETPLACE_AVAILABLE:
            await bot.add_cog(BroskiGigMarketplaceCommands(bot))
            print("💼 Gig Marketplace cog loaded!")

        print("✅ LEGENDARY cogs loaded successfully!")
    except Exception as e:
        print(f"❌ Cog loading error: {e}")


@bot.event
async def on_guild_join(guild):
    """Welcome message when bot joins a server"""
    bot_stats["servers_count"] = len(bot.guilds)

    # Find the best channel to send welcome message
    channel = None
    for c in guild.text_channels:
        if c.permissions_for(guild.me).send_messages:
            if "general" in c.name.lower() or "welcome" in c.name.lower():
                channel = c
                break

    if not channel:
        channel = guild.system_channel or guild.text_channels[0]

    if channel:
        embed = discord.Embed(
            title="🎮👑 BROSKI DISCORD BOT HAS ARRIVED! 👑🎮",
            description="The most LEGENDARY Discord bot experience is now live!",
            color=0xFFD700,
        )

        embed.add_field(
            name="🚀 What's Included",
            value=(
                "💰 BROski$ token economy system\n"
                "🎁 Auto-earning from Discord activity\n"
                "🎉 Special events and giveaways\n"
                "🏆 Leaderboards and achievements\n"
                "🔗 Portal upgrade system\n"
                "👑 VIP features and more!"
            ),
            inline=False,
        )

        embed.add_field(
            name="📚 Get Started",
            value="Use `/help` to see all commands!",
            inline=True,
        )

        embed.add_field(
            name="🔗 Official Discord",
            value=f"[Join the BROski Discord!]({OFFICIAL_DISCORD_INVITE})",
            inline=True,
        )

        embed.set_footer(text="Thanks for adding BROski Bot! 🚀")

        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"❌ Welcome message error: {e}")


@bot.event
async def on_command(ctx):
    """Track command usage"""
    bot_stats["commands_used"] += 1
    bot_stats["active_users"].add(ctx.author.id)


@bot.event
async def on_message(message):
    """Process messages and track activity"""
    if not message.author.bot:
        bot_stats["active_users"].add(message.author.id)

    await bot.process_commands(message)


# 🎮 LEGENDARY HELP COMMAND
@bot.hybrid_command(name="help", description="🚀 Show all LEGENDARY BROski commands")
async def help_command(ctx):
    """Custom LEGENDARY help command"""
    embed = discord.Embed(
        title="🎮👑 BROSKI BOT - COMMAND CENTER 👑🎮",
        description="The most LEGENDARY Discord bot commands!",
        color=0xFFD700,
    )

    # Economy Commands
    embed.add_field(
        name="💰 BROski$ Economy",
        value=(
            "`/balance` - Check your BROski$ balance\n"
            "`/leaderboard` - View top token earners\n"
            "`/daily-bonus` - Claim daily token bonus\n"
            "`/gift-tokens @user amount` - Gift tokens to friends\n"
            "`/transactions` - View your transaction history"
        ),
        inline=False,
    )

    # Portal Commands
    embed.add_field(
        name="🚀 Portal System",
        value=(
            "`/portal-status` - Check your portal connection\n"
            "`/upgrade-portal tier` - Upgrade your portal\n"
            "`/portal-features` - View available features\n"
            "`/connect-portal` - Connect to BROski Portal"
        ),
        inline=False,
    )

    # Events Commands
    embed.add_field(
        name="🎉 Events & Activities",
        value=(
            "`/active-events` - Check running events\n"
            "`/stats` - View bot statistics\n"
            "`/invite` - Get bot invite link"
        ),
        inline=False,
    )

    # Auto-earning info
    embed.add_field(
        name="🎯 Auto-Earning",
        value=(
            "💬 **Chat Activity**: 1-3 tokens per message\n"
            "❤️ **Reactions**: 1-2 tokens per reaction\n"
            "🚀 **Server Boost**: 100 tokens bonus\n"
            "📝 **Long Messages**: Bonus tokens\n"
            "🎁 **Special Events**: Double tokens & more!"
        ),
        inline=False,
    )

    embed.add_field(
        name="🔗 Official Discord",
        value=f"[Join the BROski Community!]({OFFICIAL_DISCORD_INVITE})",
        inline=False,
    )

    embed.set_footer(text="💡 All commands earn you BROski$ tokens automatically!")

    await ctx.send(embed=embed)


# 📊 BOT STATISTICS COMMAND
@bot.hybrid_command(name="stats", description="📊 View LEGENDARY bot statistics")
async def stats_command(ctx):
    """Show bot statistics"""
    uptime = (
        datetime.now() - bot_stats["start_time"]
        if bot_stats["start_time"]
        else "Unknown"
    )

    embed = discord.Embed(
        title="📊 BROSKI BOT STATISTICS 📊",
        description="Real-time LEGENDARY bot stats!",
        color=0x00FF00,
    )

    embed.add_field(
        name="🤖 Bot Info",
        value=(
            f"🆔 Bot ID: {bot.user.id}\n"
            f"⏰ Uptime: {str(uptime).split('.')[0]}\n"
            f"🌐 Servers: {bot_stats['servers_count']}\n"
            f"👥 Total Users: {sum(guild.member_count for guild in bot.guilds)}"
        ),
        inline=True,
    )

    embed.add_field(
        name="📈 Activity Stats",
        value=(
            f"🎮 Commands Used: {bot_stats['commands_used']}\n"
            f"👤 Active Users: {len(bot_stats['active_users'])}\n"
            f"💰 Tokens Distributed: {bot_stats['tokens_distributed']}\n"
            f"⚡ Status: LEGENDARY"
        ),
        inline=True,
    )

    embed.add_field(
        name="🔗 Links",
        value=f"[Official Discord]({OFFICIAL_DISCORD_INVITE})",
        inline=False,
    )

    await ctx.send(embed=embed)


# 🔗 INVITE LINK COMMAND
@bot.hybrid_command(name="invite", description="🔗 Get bot invite link")
async def invite_command(ctx):
    """Get bot invite link"""
    invite_url = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(administrator=True),
        scopes=("bot", "applications.commands"),
    )

    embed = discord.Embed(
        title="🔗 INVITE BROSKI BOT! 🔗",
        description="Bring the LEGENDARY experience to your server!",
        color=0xFF69B4,
    )

    embed.add_field(
        name="🚀 Bot Invite",
        value=f"[Add BROski Bot to Your Server!]({invite_url})",
        inline=False,
    )

    embed.add_field(
        name="🌐 Official Discord",
        value=f"[Join BROski Community]({OFFICIAL_DISCORD_INVITE})",
        inline=False,
    )

    embed.add_field(
        name="💰 Features",
        value=(
            "🎮 BROski$ token economy\n"
            "🎁 Auto-earning system\n"
            "🏆 Leaderboards\n"
            "🎉 Special events\n"
            "👑 Portal upgrades"
        ),
        inline=False,
    )

    await ctx.send(embed=embed)


# 🚀 LEGENDARY BOT LAUNCHER
async def main():
    """LEGENDARY bot startup sequence"""
    print("🚀 Starting LEGENDARY BROski Discord Bot...")

    # Load Discord token
    token = load_discord_token()
    if not token:
        print("❌ No Discord token found!")
        print("💡 Add your Discord bot token to broski_token_config.json")
        print('💡 Format: {"discord_token": "YOUR_TOKEN_HERE"}')
        return

    try:
        # Start the LEGENDARY bot
        await bot.start(token)
    except Exception as e:
        print(f"❌ Bot startup error: {e}")
        print("💡 Check your Discord token and bot permissions!")


if __name__ == "__main__":
    """🎮 LEGENDARY EXECUTION STARTS HERE! 🎮"""
    print("💥" * 50)
    print("🎮 BROSKI DISCORD BOT - ULTRA LEGENDARY EDITION 🎮")
    print("💥" * 50)

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Run the LEGENDARY bot
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("👋 BROski Bot shutdown complete!")
