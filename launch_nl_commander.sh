#!/bin/bash
"""
🚀🧠 BROSKI NATURAL LANGUAGE COMMANDER LAUNCHER 🧠🚀
🌌 One-Click Agent Army Control System! 🌌
👑 Your voice commands the infinite digital realm! 👑
"""

echo "🧠💜 BROSKI NATURAL LANGUAGE COMMANDER STARTUP! 💜🧠"
echo "================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🌌 Initializing ChaosGenius Natural Language Control System...${NC}"

# Set working directory
cd /root/chaosgenius

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found! Please install Python3${NC}"
    exit 1
fi

echo -e "${BLUE}🔧 Installing required dependencies...${NC}"

# Install pip dependencies
pip3 install -r requirements_nl_api.txt

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ Installing dependencies individually...${NC}"
    pip3 install fastapi uvicorn pydantic requests aiofiles python-multipart
fi

echo -e "${GREEN}✅ Dependencies installed!${NC}"

# Create systemd service file for auto-restart
echo -e "${BLUE}🛠️ Setting up systemd service...${NC}"

sudo tee /etc/systemd/system/broski-nl-commander.service > /dev/null <<EOF
[Unit]
Description=BROSKI Natural Language Commander
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/chaosgenius
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 broski_nl_web_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable broski-nl-commander.service

echo -e "${GREEN}✅ Systemd service configured!${NC}"

# Check if port 8000 is available
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️ Port 8000 is already in use. Stopping any existing processes...${NC}"
    sudo pkill -f "broski_nl_web_api"
    sleep 2
fi

echo -e "${PURPLE}🚀 Starting BROSKI Natural Language Commander...${NC}"
echo -e "${BLUE}📡 API will be available at: http://localhost:8000${NC}"
echo -e "${BLUE}📚 API Documentation: http://localhost:8000/docs${NC}"
echo -e "${BLUE}🎮 Interactive Dashboard: http://localhost:8000${NC}"

# Start the service
sudo systemctl start broski-nl-commander.service

# Wait a moment for startup
sleep 3

# Check if service is running
if systemctl is-active --quiet broski-nl-commander.service; then
    echo -e "${GREEN}✅ BROSKI Natural Language Commander is ONLINE!${NC}"
    echo -e "${PURPLE}🎯 Ready to accept commands like:${NC}"
    echo -e "${YELLOW}   • 'deploy 3 money bots'${NC}"
    echo -e "${YELLOW}   • 'run NFT campaign overnight'${NC}"
    echo -e "${YELLOW}   • 'check agent status'${NC}"
    echo -e "${YELLOW}   • 'boost neural performance'${NC}"

    echo -e "${BLUE}📊 Checking system status...${NC}"
    sleep 2

    # Test the API
    curl -s http://localhost:8000/api/health | python3 -m json.tool

    echo -e "${GREEN}🎉 SYSTEM FULLY OPERATIONAL!${NC}"
    echo -e "${PURPLE}💬 Open http://localhost:8000 in your browser to control your agent army!${NC}"

    # Show service logs
    echo -e "${BLUE}📋 Service logs (press Ctrl+C to exit):${NC}"
    sudo journalctl -u broski-nl-commander.service -f
else
    echo -e "${RED}❌ Failed to start BROSKI Natural Language Commander${NC}"
    echo -e "${YELLOW}📋 Check logs with: sudo journalctl -u broski-nl-commander.service${NC}"
fi