#!/bin/bash
# 🔍 ChaosGenius Empire Monitor

echo "📊 CHAOSGENIUS EMPIRE STATUS MONITOR"
echo "===================================="

# Check if sync dashboard is running
if curl -s http://localhost:9999/api/status > /dev/null 2>&1; then
    echo "✅ Sync Dashboard: RUNNING (http://localhost:9999)"

    # Get detailed status
    status=$(curl -s http://localhost:9999/api/status | python3 -m json.tool 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$status" | grep -E '"empire_status"|"running_services"|"total_services"'
    fi
else
    echo "❌ Sync Dashboard: OFFLINE"
    echo "   Run: ./start_empire.sh to launch"
fi

echo ""
echo "🔗 Quick Access URLs:"
echo "   📊 Sync Dashboard: http://localhost:9999"
echo "   🎛️ Main Dashboard: http://localhost:3000"
echo "   🚀 API Dashboard: http://localhost:5000"
echo "   🧠 HyperFocus Zone: http://localhost:5100"
echo "   💚 Health Matrix: http://localhost:5001"

