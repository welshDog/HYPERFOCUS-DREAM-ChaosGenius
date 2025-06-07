#!/bin/bash
# 🚀💥 ChaosGenius Quick Setup Script 💥🚀
# Get your neurodivergent productivity empire running in 60 seconds!

echo "🧠💥 Welcome to ChaosGenius Setup! 💥🧠"
echo "========================================"

# Check Python version
echo "🔍 Checking Python version..."
python3 --version

# Create virtual environment
echo "🏗️ Creating virtual environment..."
python3 -m venv project_env
source project_env/bin/activate

# Install requirements
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "📝 Installing core dependencies..."
    pip install flask flask-socketio sqlite3 psutil requests
fi

# Initialize database
echo "🗄️ Setting up database..."
python -c "
import sqlite3
conn = sqlite3.connect('chaosgenius.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, tokens INTEGER DEFAULT 0)')
cursor.execute('CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, user_id INTEGER, focus_type TEXT, duration INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS achievements (id INTEGER PRIMARY KEY, user_id INTEGER, achievement TEXT, unlocked_at TIMESTAMP)')
conn.commit()
conn.close()
print('✅ Database initialized!')
"

# Create .env template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << EOL
# 🧠 ChaosGenius Environment Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-key-here
DISCORD_TOKEN=your-discord-token-here
EOL
    echo "⚠️  Don't forget to update .env with your API keys!"
fi

echo ""
echo "🎉 SETUP COMPLETE! 🎉"
echo "===================="
echo ""
echo "🚀 Quick Start Commands:"
echo "   python dashboard_api.py          # Launch main dashboard"
echo "   python health_check.py           # Check system health"
echo "   python .secret_easter_eggs.py    # 🥚 Find hidden features"
echo ""
echo "🌐 Your dashboard will be at: http://localhost:5000"
echo "📖 Check README.md for full documentation"
echo ""
echo "🎯 Ready to transform chaos into creativity? Let's go! 💪"