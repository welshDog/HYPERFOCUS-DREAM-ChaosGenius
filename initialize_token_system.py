#!/usr/bin/env python3
"""
🪙 BROski$ Token Economy Initialization Script
Initialize the database schema and reward store for the token economy
"""

import sys
import sqlite3
from pathlib import Path

# Add project path
sys.path.append(str(Path(__file__).parent))

try:
    from ai_modules.broski.token_engine import BROskiTokenEngine
    print("🪙 BROski$ Token Engine imported successfully!")

    # Initialize token engine
    print("📊 Initializing token engine...")
    token_engine = BROskiTokenEngine()
    print("✅ Token engine created!")

    # Initialize database schema
    print("🏗️ Setting up database schema...")
    token_engine._initialize_token_database()
    print("✅ Database schema initialized!")

    # Initialize reward store
    print("🏪 Populating reward store...")
    token_engine.initialize_reward_store()
    print("✅ Reward store populated!")

    # Check database
    print("\n📋 Database Status Check:")
    conn = sqlite3.connect('chaosgenius.db')
    cursor = conn.cursor()

    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"📊 Total tables: {len(tables)}")

    # Check token-specific tables
    token_tables = ['user_wallets', 'token_balances', 'token_transactions', 'reward_store', 'user_redemptions']
    for table_name in token_tables:
        cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        exists = cursor.fetchone()[0]
        status = '✅' if exists else '❌'
        if exists:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"{status} {table_name} ({count} records)")
        else:
            print(f"{status} {table_name}")

    conn.close()

    print("\n🚀 BROski$ Token Economy is READY!")
    print("💰 Users can now use !wallet, !checkin, !rewards commands in Discord!")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're in the HYPERFOCUS-DREAM-ChaosGenius directory")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
