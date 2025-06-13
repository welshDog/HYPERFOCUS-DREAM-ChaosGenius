#!/bin/bash
"""
🚀💜 ChaosGenius Agent Army Launcher
==================================
Launch all immortal agents on PythonAnywhere/VPS
"""

echo "🤖💜 LAUNCHING CHAOSGENIUS AGENT ARMY..."
echo "========================================="

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing agent requirements..."
pip install -r requirements.txt

# Set environment variables
export API_SECRET="broski-hybrid-secret-2025"
export AGENT_PORT=8080

# Launch the immortal guardian
echo "🛡️ LAUNCHING IMMORTAL GUARDIAN SYSTEM..."
echo "💜 Agent Army will run 24/7 in background"
echo "🔌 API Server accessible on port $AGENT_PORT"
echo "========================================="

# Run in background with nohup for persistence
nohup python3 immortal_guardian.py > agent_army_output.log 2>&1 &

# Save the process ID
echo $! > agent_army.pid

echo "✅ Agent Army launched successfully!"
echo "📊 Process ID: $(cat agent_army.pid)"
echo "📝 Logs: tail -f agent_army_output.log"
echo "🛑 Stop: kill $(cat agent_army.pid)"
echo "💜 IMMORTAL MODE ACTIVATED!"