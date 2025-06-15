#!/usr/bin/env python3
"""
🚀💥 DISCORD COMMAND REGISTRATION SCRIPT 💥🚀
Register slash commands with Discord for interactions endpoint
By Command of Chief Lyndz - BROski∞ Command Setup
"""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def register_discord_commands():
    """🎯 Register slash commands with Discord"""

    app_id = os.getenv("DISCORD_APPLICATION_ID")
    bot_token = os.getenv("DISCORD_BOT_TOKEN")

    if not app_id or not bot_token:
        print("❌ Missing Discord credentials!")
        print(
            "💡 Make sure DISCORD_APPLICATION_ID and DISCORD_BOT_TOKEN are set in .env"
        )
        return False

    # Command definitions
    commands = [
        {
            "name": "fresh_start",
            "description": "🚀 Begin your fresh BROski journey!",
            "type": 1,
        },
        {
            "name": "agent_assist",
            "description": "🤖 Get help from the Agent Army!",
            "type": 1,
            "options": [
                {
                    "name": "task",
                    "description": "What do you need help with?",
                    "type": 3,
                    "required": True,
                }
            ],
        },
        {
            "name": "focus_mode",
            "description": "🧠 Start a hyperfocus productivity session!",
            "type": 1,
            "options": [
                {
                    "name": "project",
                    "description": "What project are you working on?",
                    "type": 3,
                    "required": True,
                },
                {
                    "name": "minutes",
                    "description": "How many minutes? (default: 25)",
                    "type": 4,
                    "required": False,
                },
            ],
        },
        {
            "name": "daily_boost",
            "description": "⚡ Get your daily dopamine boost and tokens!",
            "type": 1,
        },
        {
            "name": "wallet",
            "description": "💰 Check your BROski$ wallet and cosmic status",
            "type": 1,
        },
        {
            "name": "agent_status",
            "description": "📊 Check the Agent Army status",
            "type": 1,
        },
        {
            "name": "cosmic_transform",
            "description": "🌌 Transform your server into a cosmic base!",
            "type": 1,
        },
    ]

    # Register global commands
    url = f"https://discord.com/api/v10/applications/{app_id}/commands"
    headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"}

    print("🚀💥 REGISTERING DISCORD COMMANDS! 💥🚀")
    print("=" * 50)

    for command in commands:
        try:
            response = requests.post(url, headers=headers, json=command)

            if response.status_code == 201:
                print(f"✅ Registered: /{command['name']}")
            else:
                print(
                    f"❌ Failed to register /{command['name']}: {response.status_code}"
                )
                print(f"   Error: {response.text}")

        except Exception as e:
            print(f"❌ Error registering /{command['name']}: {e}")

    print("\n🎉 Command registration complete!")
    print("🤖 Your Discord bot now supports HTTP interactions!")
    print("\n📋 NEXT STEPS:")
    print("1. Set your interactions endpoint URL in Discord Developer Portal:")
    print("   https://discord.com/developers/applications")
    print("2. Go to your app > General Information > Interactions Endpoint URL")
    print("3. Set it to: https://your-domain.com/discord/interactions")
    print("   (or http://localhost:3000/discord/interactions for testing)")
    print("\n🌌 LEGENDARY SETUP COMPLETE!")

    return True


if __name__ == "__main__":
    register_discord_commands()
