#!/bin/bash
"""
🚀 CHAOSGENIUS EMPIRE QUICK LAUNCHER 🚀
======================================
One-click launch for the entire empire!
"""

echo "🚀 CHAOSGENIUS EMPIRE QUICK LAUNCHER"
echo "===================================="
echo ""
echo "🎯 Choose your launch option:"
echo ""
echo "1. 👑 FULL EMPIRE LAUNCH (All Systems)"
echo "2. 🚀 Command Center Only"
echo "3. 🤖 Agent Orchestrator Demo"
echo "4. 🎛️ Main Dashboard Only"
echo "5. 📊 System Status Check"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "👑 LAUNCHING FULL CHAOSGENIUS EMPIRE..."
        echo "🎯 This will start ALL systems!"
        python3 empire_master_launcher.py
        ;;
    2)
        echo "🚀 LAUNCHING COMMAND CENTER..."
        echo "🌐 Access at: http://localhost:8080"
        python3 ultimate_command_center.py
        ;;
    3)
        echo "🤖 LAUNCHING AGENT ORCHESTRATOR DEMO..."
        python3 super_ai_agent_orchestrator.py
        ;;
    4)
        echo "🎛️ LAUNCHING MAIN DASHBOARD..."
        echo "🌐 Access at: http://localhost:3000"
        python3 app.py
        ;;
    5)
        echo "📊 SYSTEM STATUS CHECK..."
        echo "🔧 Checking dependencies..."
        python3 -c "
import sys
try:
    import flask, flask_socketio, psutil, requests
    print('✅ All dependencies installed!')
    print('🚀 Ready for LEGENDARY launch!')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('🔧 Run: pip install flask flask-socketio psutil requests')
"
        echo ""
        echo "📁 Checking key files..."
        files=("empire_master_launcher.py" "ultimate_command_center.py" "super_ai_agent_orchestrator.py" "app.py")
        for file in "${files[@]}"; do
            if [ -f "$file" ]; then
                echo "✅ $file"
            else
                echo "❌ $file - MISSING"
            fi
        done
        echo ""
        echo "🎯 Empire Status: READY FOR DOMINATION!"
        ;;
    *)
        echo "❌ Invalid choice! Please run again and choose 1-5."
        exit 1
        ;;
esac