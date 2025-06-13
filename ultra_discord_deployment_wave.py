#!/usr/bin/env python3
"""
🎙️🚀 ULTRA DISCORD DEPLOYMENT WAVE 🚀🎙️
BROski Bot with welcome magic, role assignment, token drops, and mod pay scheduler!
Weekly dopamine booster missions included!
"""

import asyncio
import json
import os
import random
import sqlite3
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks


class UltraDiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!broski ", intents=intents)

        self.dopamine_missions = [
            "🧠 You've leveled up your coding brain today!",
            "⚡ Your Agent Army deployment was LEGENDARY!",
            "🔥 Cave Portal activated - productivity UNLEASHED!",
            "💎 Cloaked ideas crystallized into pure genius!",
            "🚀 BROski systems running at maximum efficiency!",
            "🛡️ Security fortress defended successfully!",
            "🧬 DNA-level optimization complete!",
            "👑 You're operating at ChaosGenius tier!",
        ]

        self.setup_database()

    def setup_database(self):
        """Initialize the ultra database system"""
        self.conn = sqlite3.connect("broski_discord_ultra.db")
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                join_date TEXT,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                tokens INTEGER DEFAULT 100,
                last_dopamine TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dopamine_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                mission TEXT,
                timestamp TEXT
            )
        """
        )

        self.conn.commit()

    async def on_ready(self):
        print(f"🎙️ {self.user} has entered the ULTRA DISCORD DEPLOYMENT WAVE!")
        print("🚀 BROski Bot systems online and ready for action!")
        self.weekly_dopamine_boost.start()

    async def on_member_join(self, member):
        """🌟 WELCOME MAGIC SYSTEM"""
        # Add to database
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO members (user_id, username, join_date, tokens)
            VALUES (?, ?, ?, ?)
        """,
            (member.id, str(member), datetime.now().isoformat(), 500),
        )
        self.conn.commit()

        # Welcome message with epic styling
        welcome_embed = discord.Embed(
            title="🌀 WELCOME TO THE CHAOS GENIUS EMPIRE! 🌀",
            description=f"**{member.mention}** has entered the digital fortress!",
            color=0x9932CC,
        )
        welcome_embed.add_field(
            name="🎯 Your Starting Kit:",
            value="💰 500 BROski Tokens\n🏆 Level 1 Agent Status\n🛡️ Cave Portal Access",
            inline=False,
        )
        welcome_embed.add_field(
            name="🚀 Quick Commands:",
            value="`!broski status` - Check your stats\n`!broski mission` - Get random mission\n`!broski cave` - Access portal",
            inline=False,
        )

        # Auto-role assignment
        role = discord.utils.get(member.guild.roles, name="🤖 Agent Recruit")
        if role:
            await member.add_roles(role)

        channel = discord.utils.get(member.guild.channels, name="welcome")
        if channel:
            await channel.send(embed=welcome_embed)

    @commands.command(name="status")
    async def user_status(self, ctx):
        """Check your ChaosGenius status"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM members WHERE user_id = ?", (ctx.author.id,))
        user_data = cursor.fetchone()

        if not user_data:
            await ctx.send("🔧 Registering you in the system...")
            cursor.execute(
                """
                INSERT INTO members (user_id, username, join_date)
                VALUES (?, ?, ?)
            """,
                (ctx.author.id, str(ctx.author), datetime.now().isoformat()),
            )
            self.conn.commit()
            user_data = (
                ctx.author.id,
                str(ctx.author),
                datetime.now().isoformat(),
                0,
                1,
                100,
                None,
            )

        embed = discord.Embed(
            title=f"🏆 {ctx.author.display_name}'s ChaosGenius Status", color=0x00FF00
        )
        embed.add_field(name="⚡ Level", value=user_data[4], inline=True)
        embed.add_field(name="🧠 XP", value=user_data[3], inline=True)
        embed.add_field(name="💰 BROski Tokens", value=user_data[5], inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="mission")
    async def random_mission(self, ctx):
        """Get a random dopamine boost mission"""
        mission = random.choice(self.dopamine_missions)

        # Add XP and log
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE members SET xp = xp + 25, last_dopamine = ?
            WHERE user_id = ?
        """,
            (datetime.now().isoformat(), ctx.author.id),
        )

        cursor.execute(
            """
            INSERT INTO dopamine_log (user_id, mission, timestamp)
            VALUES (?, ?, ?)
        """,
            (ctx.author.id, mission, datetime.now().isoformat()),
        )

        self.conn.commit()

        embed = discord.Embed(
            title="🎯 DOPAMINE BOOST MISSION DEPLOYED!",
            description=mission,
            color=0xFF69B4,
        )
        embed.add_field(
            name="🏆 Reward", value="+25 XP | Productivity Unlocked!", inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="cave")
    async def cave_portal(self, ctx):
        """Access the Cave Portal remotely"""
        embed = discord.Embed(
            title="🕋 CAVE PORTAL ACCESS GRANTED 🕋",
            description="Portal systems activated remotely!",
            color=0x8A2BE2,
        )
        embed.add_field(
            name="🌀 Portal Status",
            value="✅ Linux Desktop Portal: Active\n✅ PowerShell Ultra Portal: Ready\n✅ Mission Bank: Loaded",
            inline=False,
        )

        await ctx.send(embed=embed)

    @tasks.loop(hours=168)  # Weekly
    async def weekly_dopamine_boost(self):
        """Send weekly dopamine booster missions to all members"""
        for guild in self.guilds:
            channel = discord.utils.get(guild.channels, name="general")
            if channel:
                boost_embed = discord.Embed(
                    title="🌟 WEEKLY DOPAMINE BOOST WAVE! 🌟",
                    description="Time for your weekly productivity injection!",
                    color=0xFFD700,
                )
                boost_embed.add_field(
                    name="🎯 This Week's Challenge:",
                    value=random.choice(self.dopamine_missions),
                    inline=False,
                )

                await channel.send(embed=boost_embed)


# Bot setup and token management
def run_ultra_discord_bot():
    bot = UltraDiscordBot()

    # Try to load token from config
    try:
        with open("broski_token_config.json", "r") as f:
            config = json.load(f)
            token = config.get("discord_token")

        if token:
            print("🚀 Launching Ultra Discord Bot...")
            bot.run(token)
        else:
            print("🔧 Please add your Discord token to broski_token_config.json")

    except FileNotFoundError:
        print("🔧 Creating token config file...")
        config = {
            "discord_token": "YOUR_DISCORD_BOT_TOKEN_HERE",
            "webhook_url": "YOUR_WEBHOOK_URL_HERE",
        }
        with open("broski_token_config.json", "w") as f:
            json.dump(config, f, indent=4)
        print("✅ Config created! Add your Discord token and run again.")


if __name__ == "__main__":
    run_ultra_discord_bot()
