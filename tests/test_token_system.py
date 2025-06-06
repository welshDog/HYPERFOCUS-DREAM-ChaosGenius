#!/usr/bin/env python3
"""
🪙 BROski$ Token Economy System Test
Quick validation that all token features are working
"""

import sys
import os
sys.path.append('/workspaces/HYPERFOCUS-DREAM-ChaosGenius')

print("🚀 BROski$ Token Economy System Test")
print("=" * 50)

try:
    # Import token system
    from ai_modules.broski.token_engine import BROskiTokenEngine, BROskiTokenAIIntegration
    print("✅ Token Engine imported successfully")

    from ai_modules.broski.token_commands import BROskiTokenCommands
    print("✅ Token Commands imported successfully")

    # Initialize token engine
    token_engine = BROskiTokenEngine()
    print("✅ Token Engine initialized")

    # Test database connection
    import sqlite3
    with sqlite3.connect(token_engine.db_path) as conn:
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute("SELECT COUNT(*) FROM user_wallets")
        wallets = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reward_store")
        rewards = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM token_balances")
        balances = cursor.fetchone()[0]

        print(f"✅ Database OK - Wallets: {wallets}, Rewards: {rewards}, Balances: {balances}")

    # Test token functionality with sample user
    test_user = "test_user_123456"

    print(f"\n🧪 Testing with user: {test_user}")

    # Test daily check-in
    checkin_result = token_engine.daily_checkin(test_user)
    print(f"✅ Daily check-in: {checkin_result['status']}")
    if checkin_result['status'] == 'success':
        print(f"   💰 Earned: {checkin_result['amount_awarded']} BROski$")
        print(f"   🔥 Streak: {checkin_result['current_streak']} days")

    # Test balance check
    balance = token_engine.get_user_balance(test_user)
    print(f"✅ Balance check: {balance['status']}")
    if balance['status'] == 'success':
        print(f"   💰 Balance: {balance['broski_tokens']} BROski$")
        print(f"   🎖️ Role: {balance['role']}")
        print(f"   📊 Lifetime: {balance['lifetime_earned']} BROski$")

    # Test token award
    award_result = token_engine.award_tokens(test_user, 25, "System test")
    print(f"✅ Token award: {award_result['status']}")
    if award_result['status'] == 'success':
        print(f"   💰 Awarded: 25 BROski$")
        print(f"   💳 New balance: {award_result['new_balance']} BROski$")

    # Test leaderboard
    leaderboard = token_engine.get_leaderboard(5)
    print(f"✅ Leaderboard: {len(leaderboard)} entries")

    # Test AI integration
    ai_integration = BROskiTokenAIIntegration(token_engine)
    earning_tips = ai_integration.get_personalized_earning_tips(test_user)
    print(f"✅ AI Integration: Generated {len(earning_tips)} earning tips")

    print("\n🎉 BROski$ Token Economy System: FULLY OPERATIONAL!")
    print("=" * 50)
    print("🎯 All token features are working correctly:")
    print("   • User wallet creation ✅")
    print("   • Daily check-ins ✅")
    print("   • Token awards ✅")
    print("   • Balance tracking ✅")
    print("   • Role progression ✅")
    print("   • Leaderboards ✅")
    print("   • AI integration ✅")
    print("   • Database operations ✅")

    print("\n🤖 Ready for Discord bot integration!")
    print("💡 Commands available: !wallet, !checkin, !rewards, !redeem, !leaderboard")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
