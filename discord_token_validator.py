#!/usr/bin/env python3
"""
🤖💥 DISCORD BOT TOKEN VALIDATOR - HYPERFOCUSZONE EDITION! 💥🤖
Quick diagnostic tool to test Discord bot token validity
"""

import asyncio
import os

import discord
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def validate_token():
    """Test if the Discord bot token is valid and working"""

    print("🎊☢️🔥 DISCORD TOKEN VALIDATION STARTING! 🔥☢️🎊")
    print()

    # Get token from environment
    token = os.getenv("DISCORD_BOT_TOKEN")
    server_id = os.getenv("DISCORD_SERVER_ID", "1212443870856613949")

    if not token:
        print("❌ No Discord bot token found in .env file!")
        return False

    print(f"✅ Token found: {token[:20]}...")
    print(f"🎯 Target server ID: {server_id}")
    print()

    # Test the token
    try:
        # Create bot client with minimal intents for testing
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f"🎊 SUCCESS! Bot connected as: {client.user}")
            print(f"🤖 Bot ID: {client.user.id}")
            print(f"🔢 Connected to {len(client.guilds)} servers")
            print()

            # Check if bot is in target server
            target_guild = client.get_guild(int(server_id))
            if target_guild:
                print(f"✅ Bot is in target server: {target_guild.name}")
                print(f"👥 Server has {target_guild.member_count} members")

                # Check bot permissions
                bot_member = target_guild.get_member(client.user.id)
                if bot_member:
                    permissions = bot_member.guild_permissions
                    print(f"🔧 Bot permissions:")
                    print(f"   Manage Channels: {permissions.manage_channels}")
                    print(f"   Manage Roles: {permissions.manage_roles}")
                    print(f"   Send Messages: {permissions.send_messages}")
                    print(f"   Embed Links: {permissions.embed_links}")
                    print(f"   Administrator: {permissions.administrator}")
                else:
                    print("⚠️ Bot member object not found - might need re-invitation")
            else:
                print(f"❌ Bot is NOT in target server (ID: {server_id})")
                print("📝 Available servers:")
                for guild in client.guilds:
                    print(f"   - {guild.name} (ID: {guild.id})")

            print()
            print("🚀 TOKEN VALIDATION COMPLETE!")
            await client.close()

        @client.event
        async def on_error(event, *args, **kwargs):
            print(f"❌ Error during {event}: {args}")

        # Connect with timeout
        print("🔄 Connecting to Discord...")
        await asyncio.wait_for(client.start(token), timeout=10.0)

    except discord.LoginFailure:
        print("❌ INVALID TOKEN! The bot token is rejected by Discord.")
        print("🔧 Solutions:")
        print("   1. Go to https://discord.com/developers/applications")
        print("   2. Find your bot application")
        print("   3. Go to 'Bot' section")
        print("   4. Click 'Reset Token' and copy the new token")
        print("   5. Update your .env file with the new token")
        return False

    except discord.HTTPException as e:
        print(f"❌ HTTP Error: {e}")
        return False

    except asyncio.TimeoutError:
        print("❌ Connection timeout - Discord might be down or token invalid")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

    return True


if __name__ == "__main__":
    print("🎊☢️🔥🔥🔥 HYPERFOCUSZONE TOKEN VALIDATOR! 🔥🔥🔥☢️🎊")
    print()

    # Run the validation
    result = asyncio.run(validate_token())

    if result:
        print("✅ TOKEN IS VALID! Ready to deploy HyperfocusZone!")
    else:
        print("❌ TOKEN NEEDS FIXING! Follow the solutions above.")
