#!/usr/bin/env python3
"""
🤖💜 CHAOSGENIUS DISCORD BOT 💜🤖
Ultra-Powered Discord Integration for Broski Neural Overseer
By Command of Chief Lyndz
"""

import asyncio
import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime

import discord
from discord.ext import commands

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_TOKEN_HERE")
COMMAND_PREFIX = "!"
BROSKI_DB_PATH = "/root/chaosgenius/broski_overseer.db"

# Bot Setup with Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


class BroskiDiscordInterface:
    """🧠 Interface between Discord and Broski Neural Overseer"""

    @staticmethod
    def get_neural_status():
        """📊 Get current neural system status"""
        try:
            conn = sqlite3.connect(BROSKI_DB_PATH)
            cursor = conn.cursor()

            # Get file counts
            cursor.execute(
                "SELECT file_type, COUNT(*) FROM neural_files GROUP BY file_type"
            )
            file_counts = dict(cursor.fetchall())

            # Get recent guardian activity
            cursor.execute(
                "SELECT COUNT(*) FROM guardian_log WHERE datetime(timestamp) > datetime('now', '-1 hour')"
            )
            recent_activity = cursor.fetchone()[0]

            # Get agent count
            cursor.execute("SELECT COUNT(*) FROM ai_agents WHERE status = 'active'")
            active_agents = cursor.fetchone()[0]

            conn.close()

            return {
                "files": file_counts,
                "recent_activity": recent_activity,
                "active_agents": active_agents,
                "status": "OPERATIONAL",
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    @staticmethod
    def forge_agent_via_discord(agent_name, agent_type):
        """🧙 Forge new agent via Discord command"""
        try:
            # Import the overseer system
            sys.path.append("/root/chaosgenius")
            from importlib import import_module

            # Basic agent config
            agent_config = {
                "name": agent_name,
                "type": agent_type,
                "input_source": "discord",
                "output_target": "discord",
                "crystal_attached": "none",
                "database_attached": BROSKI_DB_PATH,
            }

            # Log to database
            conn = sqlite3.connect(BROSKI_DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ai_agents
                (agent_name, agent_type, input_source, output_target, crystal_attached, database_attached)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (agent_name, agent_type, "discord", "discord", "none", BROSKI_DB_PATH),
            )
            conn.commit()
            conn.close()

            return f"🧙 Agent '{agent_name}' forged successfully via Discord!"
        except Exception as e:
            return f"❌ Agent forge failed: {str(e)}"


@bot.event
async def on_ready():
    """🚀 Bot startup event"""
    print(f"🤖 {bot.user.name} has connected to Discord!")
    print(f"🛡️ Connected to {len(bot.guilds)} servers")
    print("💜 Broski Discord Bot ONLINE! 💜")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")


@bot.tree.command(
    name="neural_status", description="🧠 Get Broski Neural Overseer status"
)
async def neural_status(interaction: discord.Interaction):
    """Get current neural system status"""
    await interaction.response.defer()

    status = BroskiDiscordInterface.get_neural_status()

    if status["status"] == "ERROR":
        embed = discord.Embed(
            title="❌ Neural System Error",
            description=f"Error: {status.get('error', 'Unknown error')}",
            color=0xFF0000,
        )
    else:
        embed = discord.Embed(
            title="🧠 Broski Neural Overseer Status",
            description="💜 System Status: OPERATIONAL 💜",
            color=0x9400D3,
        )

        # File counts
        files_text = ""
        for file_type, count in status["files"].items():
            emoji = {
                "crystals": "🔮",
                "databases": "🗄️",
                "modules": "⚙️",
                "agents": "🤖",
            }.get(file_type, "📄")
            files_text += f"{emoji} {file_type.title()}: {count}\n"

        embed.add_field(
            name="📊 Neural Files", value=files_text or "No files tracked", inline=True
        )
        embed.add_field(
            name="🛡️ Guardian Activity",
            value=f"{status['recent_activity']} events (last hour)",
            inline=True,
        )
        embed.add_field(
            name="🤖 Active Agents", value=str(status["active_agents"]), inline=True
        )
        embed.set_footer(
            text=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="forge_agent", description="🧙 Forge a new AI agent")
async def forge_agent(
    interaction: discord.Interaction, agent_name: str, agent_type: str = "basic"
):
    """Forge a new AI agent"""
    await interaction.response.defer()

    if len(agent_name) < 3 or len(agent_name) > 50:
        await interaction.followup.send("❌ Agent name must be 3-50 characters long!")
        return

    # Valid agent types
    valid_types = ["basic", "monitor", "guardian", "analyzer", "forger"]
    if agent_type not in valid_types:
        await interaction.followup.send(
            f"❌ Invalid agent type! Use: {', '.join(valid_types)}"
        )
        return

    result = BroskiDiscordInterface.forge_agent_via_discord(agent_name, agent_type)

    embed = discord.Embed(
        title="🧙 Agent Forge Result",
        description=result,
        color=0x9400D3 if "successfully" in result else 0xFF0000,
    )
    embed.add_field(name="Agent Name", value=agent_name, inline=True)
    embed.add_field(name="Agent Type", value=agent_type, inline=True)
    embed.add_field(name="Forged By", value=interaction.user.mention, inline=True)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="system_pulse", description="💜 Get quick system pulse")
async def system_pulse(interaction: discord.Interaction):
    """Quick system health check"""
    await interaction.response.defer()

    # Check if Broski Overseer is running
    try:
        result = subprocess.run(
            ["pgrep", "-f", "FORGE THE BROSKI NEURAL OVERSEER SYSTEM"],
            capture_output=True,
            text=True,
        )
        overseer_running = bool(result.stdout.strip())
    except:
        overseer_running = False

    # Check database
    db_accessible = os.path.exists(BROSKI_DB_PATH)

    embed = discord.Embed(
        title="💜 System Pulse Check",
        color=0x9400D3 if overseer_running and db_accessible else 0xFFAA00,
    )

    status_emoji = "✅" if overseer_running else "❌"
    embed.add_field(
        name="🧠 Neural Overseer",
        value=f"{status_emoji} {'RUNNING' if overseer_running else 'OFFLINE'}",
        inline=True,
    )

    db_emoji = "✅" if db_accessible else "❌"
    embed.add_field(
        name="🗄️ Neural Database",
        value=f"{db_emoji} {'ACCESSIBLE' if db_accessible else 'UNAVAILABLE'}",
        inline=True,
    )

    embed.add_field(name="🤖 Discord Bot", value="✅ ONLINE", inline=True)

    overall_status = "OPERATIONAL" if overseer_running and db_accessible else "DEGRADED"
    embed.add_field(name="🛡️ Overall Status", value=overall_status, inline=False)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="guardian_log", description="🛡️ View recent guardian activity")
async def guardian_log(interaction: discord.Interaction, limit: int = 5):
    """View recent guardian activity"""
    await interaction.response.defer()

    if limit > 20:
        limit = 20

    try:
        conn = sqlite3.connect(BROSKI_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT event_type, target_file, action_taken, timestamp
            FROM guardian_log
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (limit,),
        )

        logs = cursor.fetchall()
        conn.close()

        if not logs:
            embed = discord.Embed(
                title="🛡️ Guardian Activity Log",
                description="No recent activity found",
                color=0x9400D3,
            )
        else:
            embed = discord.Embed(
                title="🛡️ Guardian Activity Log",
                description=f"Last {len(logs)} activities:",
                color=0x9400D3,
            )

            for i, (event_type, target_file, action, timestamp) in enumerate(logs, 1):
                file_name = os.path.basename(target_file)
                embed.add_field(
                    name=f"{i}. {event_type.upper()}",
                    value=f"📄 {file_name}\n⚡ {action}\n🕒 {timestamp[:19]}",
                    inline=True,
                )

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Error accessing guardian logs: {str(e)}")


@bot.command(name="ping")
async def ping(ctx):
    """🏓 Ping command for legacy support"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms\n💜 Broski Bot is ALIVE! 💜")


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "❌ Command not found! Use `/` for slash commands or `!help` for legacy commands."
        )
    else:
        print(f"❌ Command error: {error}")


def main():
    """🚀 Main bot startup"""
    if DISCORD_TOKEN == "YOUR_DISCORD_TOKEN_HERE":
        print("❌ Please set your DISCORD_BOT_TOKEN environment variable!")
        print("Export it like: export DISCORD_BOT_TOKEN='your_token_here'")
        return

    print("🤖 Starting Broski Discord Bot...")
    print("💜 By Command of Chief Lyndz 💜")

    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid Discord token!")
    except Exception as e:
        print(f"❌ Bot startup error: {e}")


if __name__ == "__main__":
    main()
