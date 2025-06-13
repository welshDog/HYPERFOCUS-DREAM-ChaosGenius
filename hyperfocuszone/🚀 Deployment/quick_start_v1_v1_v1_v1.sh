#!/bin/bash
"""
🧠💥 HYPERFOCUSzone QUICK START LAUNCHER 💥🧠
One-click launch for your ADHD empire!
"""

echo "🚀💜 HYPERFOCUSZONE ULTRA LAUNCHER ACTIVATED! 💜🚀"
echo "=================================================================="
echo "🧠 Starting your neurodivergent empire management system..."
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "🔍 Navigating to HYPERFOCUSzone directory..."
    cd /root/chaosgenius/hyperfocuszone
fi

# Activate virtual environment
echo "🔋 Activating virtual environment..."
source venv/bin/activate

# Install any missing dependencies
echo "📦 Checking dependencies..."
pip install flask psutil requests > /dev/null 2>&1

echo "🎯 Launching HYPERFOCUSzone with auto-monitoring..."
echo ""
echo "🌐 Your portals will be available at:"
echo "   Main Portal: http://localhost:5000"
echo "   Command Center: http://localhost:5000/ultimate-command-center"
echo "   API Status: http://localhost:5000/api/status"
echo ""
echo "💜 ADHD-optimized features activated!"
echo "🤖 Agent army will deploy automatically!"
echo ""
echo "Press Ctrl+C to stop the monitoring system"
echo "=================================================================="

# Launch with auto-monitoring
python3 launcher.py