#!/bin/bash
# 🧠💜 HYPERFOCUS ZONE ULTRA EDITION - QUICK START 💜🧠
# One-command launch for the entire quantum synchronization ecosystem!
# By Command of Chief Lyndz - BRO POWER ACTIVATED! 🚀🪄🧬🪛

echo "🧠💜 HYPERFOCUS ZONE ULTRA EDITION - QUICK START 💜🧠"
echo "🚀 Launching quantum synchronization ecosystem..."
echo ""

# Change to the chaosgenius directory
cd /root/chaosgenius

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed!"
    exit 1
fi

# Install required packages if needed
echo "🔍 Checking and installing required packages..."
python3 -m pip install --quiet flask flask-socketio psutil requests websockets

# Launch the ultra launcher
echo "🚀 Starting HYPERFOCUS ZONE ULTRA LAUNCHER..."
echo "💜 BROski AI systems coming online..."
echo ""

python3 hyperfocus_zone_ultra_launcher.py

echo ""
echo "🎉 Launch sequence complete!"
echo "💜 Thank you for using HyperFocus Zone Ultra Edition!"