#!/bin/bash
# 🧠⚡ HYPERFOCUSZONE DEPLOYMENT SCRIPT ⚡🧠
# Quick setup script for the ultimate ADHD portal

echo "🚀 DEPLOYING HYPERFOCUSZONE.COM PORTAL..."
echo "🧠⚡ ADHD-OPTIMIZED PRODUCTIVITY ECOSYSTEM ⚡🧠"

# Create directories
mkdir -p hyperfocuszone/{static,templates,api,agents,database}
mkdir -p hyperfocuszone/static/{css,js,images}

# Install required packages
echo "📦 Installing dependencies..."
pip install flask discord.py sqlite3 requests asyncio

# Create Flask backend
cat > hyperfocuszone/app.py << 'EOF'
#!/usr/bin/env python3
"""
🧠⚡ HYPERFOCUSzone Flask Backend ⚡🧠
"""

from flask import Flask, render_template, jsonify, request, session
import sqlite3
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "hyperfocus-broski-legends-2025"

# Database setup
DB_FILE = "hyperfocus_portal.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portal_users (
            id TEXT PRIMARY KEY,
            discord_id TEXT UNIQUE,
            username TEXT,
            email TEXT,
            access_level TEXT DEFAULT 'demo',
            total_xp INTEGER DEFAULT 0,
            broski_gems INTEGER DEFAULT 0,
            created_at TEXT,
            last_login TEXT,
            preferences TEXT DEFAULT '{}'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            session_type TEXT,
            start_time TEXT,
            end_time TEXT,
            duration_minutes INTEGER,
            xp_earned INTEGER DEFAULT 0,
            data TEXT DEFAULT '{}'
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def portal_home():
    return render_template('hyperfocuszone_portal.html')

@app.route('/api/user/discord-status')
def check_discord_status():
    # Check if user has Discord connection
    discord_id = session.get('discord_id')
    if discord_id:
        conn = sqlite3.connect(DB_FILE)
        user = conn.execute('SELECT * FROM portal_users WHERE discord_id = ?', (discord_id,)).fetchone()
        conn.close()

        if user:
            return jsonify({
                'connected': True,
                'user': {
                    'id': user[1],
                    'username': user[2],
                    'access_level': user[4],
                    'total_xp': user[5],
                    'broski_gems': user[6]
                }
            })

    return jsonify({'connected': False})

@app.route('/api/portal/demo-session', methods=['POST'])
def start_demo_session():
    session_id = str(uuid.uuid4())
    session['demo_session_id'] = session_id
    session['demo_start_time'] = datetime.now().isoformat()

    return jsonify({
        'session_id': session_id,
        'demo_duration': 30,  # 30 minutes
        'features_unlocked': ['focus_tools', 'basic_dashboard'],
        'message': '🎮 Demo session started! 30 minutes of ADHD optimization ahead!'
    })

@app.route('/api/agents/status')
def get_agent_status():
    # Return demo or personalized agent status
    if session.get('discord_id'):
        # Full agent army for Discord users
        agents = {
            "GUARDIAN-ZERO": {"status": "active", "health": 100, "missions": 15},
            "FOCUS-BUDDY": {"status": "active", "health": 100, "sessions": 8},
            "MEMORY-CRYSTAL": {"status": "active", "health": 100, "memories": 1247},
            "AGENT-ARMY": {"status": "active", "health": 100, "deployments": 23}
        }
    else:
        # Limited demo agents
        agents = {
            "DEMO-GUARDIAN": {"status": "demo", "health": 75, "limitations": "30min sessions"}
        }

    return jsonify(agents)

@app.route('/guardian')
def guardian_hud():
    return render_template('guardian_hud.html')

if __name__ == '__main__':
    init_db()
    print("🧠⚡ HYPERFOCUSzone Portal starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF

# Copy portal files
echo "📁 Setting up portal files..."
cp hyperfocuszone_user_portal.html hyperfocuszone/templates/hyperfocuszone_portal.html
cp guardian_hud.html hyperfocuszone/templates/

# Create startup script
cat > hyperfocuszone/start_portal.sh << 'EOF'
#!/bin/bash
echo "🧠⚡ STARTING HYPERFOCUSZONE PORTAL..."
cd hyperfocuszone
python app.py &
echo "🌐 Portal running at http://localhost:5000"
echo "🚀 Ready for ADHD legends!"
EOF

chmod +x hyperfocuszone/start_portal.sh

# Create Discord bot startup
cat > start_discord_bot.sh << 'EOF'
#!/bin/bash
echo "🤖 STARTING HYPERFOCUSZONE DISCORD BOT..."
echo "💜 Make sure to set your BOT_TOKEN in hyperfocuszone_discord_bot.py"
python hyperfocuszone_discord_bot.py
EOF

chmod +x start_discord_bot.sh

echo ""
echo "🎉 HYPERFOCUSZONE DEPLOYMENT COMPLETE! 🎉"
echo ""
echo "🚀 NEXT STEPS:"
echo "1. Set your Discord bot token in hyperfocuszone_discord_bot.py"
echo "2. Run: ./hyperfocuszone/start_portal.sh"
echo "3. Run: ./start_discord_bot.sh (in another terminal)"
echo "4. Visit: http://localhost:5000"
echo ""
echo "🧠⚡ READY TO OPTIMIZE ADHD LEGENDS! ⚡🧠"