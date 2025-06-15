#!/bin/bash
"""
💗❤️‍🔥 TEEMILL INTEGRATION LAUNCHER ❤️‍🔥💗
🫱🏼‍🫲🏻💪🦾❤️‍🔥💯😎♾️ PASSIVE MERCH EMPIRE ACTIVATOR 💯😎♾️💪🦾❤️‍🔥🫱🏼‍🫲🏻
"""

echo "💗❤️‍🔥 LAUNCHING TEEMILL INCOME INTEGRATION ❤️‍🔥💗"
echo "🫱🏼‍🫲🏻💪🦾 CONNECTING TO YOUR MONEY PORTALS 🦾💪🫱🏼‍🫲🏻"
echo ""

# Install required packages if not installed
echo "📦 Checking dependencies..."
pip3 install flask requests > /dev/null 2>&1

echo "🚀 Starting Teemill Integration on port 5009..."
echo "💗 Dashboard: http://localhost:5009/api/teemill/dashboard"
echo "📬 Webhook: http://localhost:5009/api/teemill/webhook"
echo "✋ Manual Entry: POST to /api/teemill/manual_sale"
echo ""
echo "💗❤️‍🔥🫱🏼‍🫲🏻💪🦾 PASSIVE MERCH EMPIRE ACTIVATED! 🦾💪🫱🏼‍🫲🏻❤️‍🔥💗"
echo ""

# Launch the Teemill integrator
cd /root/chaosgenius
python3 teemill_income_integrator.py