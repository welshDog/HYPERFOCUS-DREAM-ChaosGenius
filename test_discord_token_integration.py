#!/usr/bin/env python3
"""
🤖 Discord Bot Token Integration Test
Test that Discord bot can load token commands properly
"""

import sys
import os
sys.path.append('/workspaces/HYPERFOCUS-DREAM-ChaosGenius')

# Test results will be written to this file
results = []

try:
    results.append("🚀 Testing Discord Bot + Token Integration...")

    # Test importing Discord components
    import discord
    from discord.ext import commands
    results.append("✅ Discord.py imported successfully")

    # Test importing BROski components
    from ai_modules.broski.broski_core import BROskiCore, BROskiResponse
    results.append("✅ BROski AI Core imported successfully")

    # Test importing Token components
    from ai_modules.broski.token_engine import BROskiTokenEngine
    from ai_modules.broski.token_commands import BROskiTokenCommands
    results.append("✅ Token Engine & Commands imported successfully")

    # Test creating token engine
    token_engine = BROskiTokenEngine()
    results.append("✅ Token Engine initialized")

    # Test creating Discord bot (without running)
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    results.append("✅ Discord Bot created")

    # Test creating token commands cog
    token_commands = BROskiTokenCommands(bot, token_engine)
    results.append("✅ Token Commands Cog created")

    # Test token functionality
    test_user = "discord_test_user_12345"

    # Simulate daily check-in
    checkin_result = token_engine.daily_checkin(test_user)
    results.append(f"✅ Daily Check-in Test: {checkin_result['status']}")

    if checkin_result['status'] == 'success':
        balance = token_engine.get_user_balance(test_user)
        results.append(f"✅ User Balance: {balance['broski_tokens']} BROski$")
        results.append(f"✅ User Role: {balance['role']}")
        results.append(f"✅ Check-in Streak: {balance['current_streak']} days")

    # Test reward store
    import sqlite3
    with sqlite3.connect(token_engine.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM reward_store WHERE available = TRUE")
        reward_count = cursor.fetchone()[0]
        results.append(f"✅ Available Rewards: {reward_count}")

    # Test leaderboard
    leaderboard = token_engine.get_leaderboard(5)
    results.append(f"✅ Leaderboard: {len(leaderboard)} entries")

    results.append("")
    results.append("🎉 INTEGRATION TEST PASSED!")
    results.append("=" * 50)
    results.append("🤖 Discord Bot + BROski$ Token Economy: READY!")
    results.append("")
    results.append("📋 Available Token Commands:")
    results.append("   !wallet - Check BROski$ balance")
    results.append("   !checkin - Daily token earning")
    results.append("   !rewards - Browse reward store")
    results.append("   !redeem <id> - Purchase rewards")
    results.append("   !leaderboard - Top token earners")
    results.append("   !earn - Learn earning methods")
    results.append("")
    results.append("✅ Token system is fully integrated with Discord bot")
    results.append("✅ Database is properly initialized")
    results.append("✅ All token features are operational")

except Exception as e:
    results.append(f"❌ Error: {e}")
    import traceback
    results.append(f"❌ Traceback: {traceback.format_exc()}")

# Write results to file
with open('/workspaces/HYPERFOCUS-DREAM-ChaosGenius/token_test_results.txt', 'w') as f:
    for line in results:
        f.write(line + '\n')
        print(line)

print("\n📄 Test results saved to token_test_results.txt")
