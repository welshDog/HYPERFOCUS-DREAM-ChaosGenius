#!/bin/bash
# 🌟💜 DREAM DISCORD BOT LAUNCHER 💜🌟
# Quick launcher for the Discord Community Bot

echo "🌟 Starting Dream Discord Community Bot..."
echo "💜 Loading BROski∞ community features..."

# Check if required environment variables are set
if [ -z "$DISCORD_BOT_TOKEN" ] || [ "$DISCORD_BOT_TOKEN" = "your_bot_token_here" ]; then
    echo "❌ Error: Please set your DISCORD_BOT_TOKEN in the .env file"
    echo "💡 Edit the .env file and replace 'your_bot_token_here' with your actual bot token"
    exit 1
fi

if [ -z "$DISCORD_GUILD_ID" ] || [ "$DISCORD_GUILD_ID" = "your_server_id_here" ]; then
    echo "❌ Error: Please set your DISCORD_GUILD_ID in the .env file"
    echo "💡 Edit the .env file and replace 'your_server_id_here' with your actual server ID"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

echo "🚀 Environment loaded successfully!"
echo "🤖 Bot Token: ${DISCORD_BOT_TOKEN:0:10}..."
echo "🏰 Guild ID: $DISCORD_GUILD_ID"

# Try to run the bot with error handling
echo "🌈 Initializing all community features..."
python3 dream_discord_community_bot.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Bot failed to start. Common issues:"
    echo "💡 1. Install missing dependencies: pip install discord.py python-dotenv openai textblob aiohttp"
    echo "💡 2. Check your bot token is valid"
    echo "💡 3. Ensure bot has proper permissions in your Discord server"
    echo "💡 4. Check internet connection"
    echo ""
    echo "🔧 Try running manually: python3 dream_discord_community_bot.py"
fi