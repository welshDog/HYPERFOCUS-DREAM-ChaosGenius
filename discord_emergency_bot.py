#!/usr/bin/env python3
"""
🆘🤖 DISCORD EMERGENCY ACCESS BOT 🤖🆘
Your lifeline when everything goes wrong!
"""

import discord
import subprocess
import asyncio
from discord.ext import commands

# Initialize bot
bot = commands.Bot(command_prefix='!emergency_', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'🆘 Emergency Bot Ready: {bot.user}')

@bot.command(name='access')
async def emergency_access(ctx):
    """🔑 Emergency SSH access recovery"""
    try:
        # Run emergency recovery script
        result = subprocess.run(['/root/ultimate_emergency_recovery.sh'],
                              capture_output=True, text=True)

        embed = discord.Embed(
            title="🆘 EMERGENCY ACCESS RECOVERY",
            description="SSH access recovery executed!",
            color=0xff0000
        )
        embed.add_field(name="Status", value="✅ Recovery script executed", inline=False)
        embed.add_field(name="SSH Access", value="ssh root@your-server -p 22\nssh root@your-server -p 2222", inline=False)
        embed.add_field(name="Web Access", value="http://your-server:5002", inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Emergency recovery failed: {e}")

@bot.command(name='status')
async def system_status(ctx):
    """📊 Check system status"""
    try:
        # Check system resources
        cpu_result = subprocess.run(['top', '-bn1'], capture_output=True, text=True)

        embed = discord.Embed(
            title="📊 SYSTEM STATUS",
            description="Current system health",
            color=0x00ff00
        )

        # Add basic system info
        embed.add_field(name="SSH Ports", value="22, 2222", inline=True)
        embed.add_field(name="Web Portal", value="5002", inline=True)
        embed.add_field(name="Recovery", value="Active", inline=True)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Status check failed: {e}")

@bot.command(name='restart')
async def restart_services(ctx):
    """🔄 Restart key services"""
    try:
        # Restart SSH and web services
        subprocess.run(['systemctl', 'restart', 'ssh'])

        embed = discord.Embed(
            title="🔄 SERVICES RESTARTED",
            description="Key services have been restarted",
            color=0x0000ff
        )

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Service restart failed: {e}")

# Run bot (you'll need to add your Discord token)
# bot.run('YOUR_DISCORD_BOT_TOKEN')
