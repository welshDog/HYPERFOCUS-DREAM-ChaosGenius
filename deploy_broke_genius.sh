#!/bin/bash
# 🚀💜 BROKE GENIUS DEPLOYMENT SCRIPT 💜🚀
# Deploy your ChaosGenius empire for FREE/ULTRA-CHEAP!

echo "🧠💜 BROKE GENIUS DEPLOYMENT ACTIVATED! 💜🧠"
echo "Getting your neurodivergent empire online for PENNIES!"

# Create deployment files for Railway
cat > railway.json << EOF
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python dashboard_api.py",
    "healthcheckPath": "/api/status"
  }
}
EOF

# Create Procfile for Heroku-style platforms
cat > Procfile << EOF
web: python dashboard_api.py
worker: python broski_agent_deployment_master.py
EOF

# Create requirements.txt with minimal dependencies
cat > requirements_minimal.txt << EOF
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
sqlite3
EOF

# Create environment template
cat > .env.template << EOF
# 🔥 BROKE GENIUS CONFIG 🔥
FLASK_ENV=production
DISCORD_BOT_TOKEN=your_discord_token_here
DATABASE_URL=sqlite:///chaosgenius.db
PORT=5000
EOF

# Create Docker setup for ultra-lightweight deployment
cat > Dockerfile.minimal << EOF
FROM python:3.11-slim

WORKDIR /app
COPY requirements_minimal.txt .
RUN pip install --no-cache-dir -r requirements_minimal.txt

COPY dashboard_api.py .
COPY *.db ./
COPY broski_*.py ./

EXPOSE 5000
CMD ["python", "dashboard_api.py"]
EOF

echo "✅ Deployment files created!"
echo ""
echo "🚀 NEXT STEPS - Choose Your Adventure:"
echo ""
echo "🔥 OPTION 1: Railway.app (RECOMMENDED)"
echo "   1. Install: npm install -g @railway/cli"
echo "   2. Login: railway login"
echo "   3. Deploy: railway up"
echo "   4. FREE $5 credits monthly!"
echo ""
echo "🔥 OPTION 2: Render.com"
echo "   1. Connect GitHub repo"
echo "   2. Auto-deploy on push"
echo "   3. FREE 750 hours/month"
echo ""
echo "🔥 OPTION 3: PythonAnywhere ($5/month)"
echo "   1. Upload files via web interface"
echo "   2. Perfect for background agents"
echo "   3. Always-on tasks included"
echo ""
echo "💜 Your empire will rise, even on a budget! 💜"