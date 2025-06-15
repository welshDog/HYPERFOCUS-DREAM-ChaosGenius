#!/bin/bash
# 🚀 ChaosGenius Empire Quick Launcher

echo "🚀💎 LAUNCHING CHAOSGENIUS EMPIRE! 💎🚀"
echo "🦾💪 Starting Ultimate Sync System... 💪🦾"

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start the ultimate sync system
python3 ULTIMATE_CHAOSGENIUS_SYNC.py

