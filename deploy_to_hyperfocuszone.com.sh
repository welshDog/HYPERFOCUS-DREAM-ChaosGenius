#!/bin/bash
# 🔥💗 CHIEF LYNDZ'S HYPERFOCUSZONE.COM IMMORTAL DEPLOYMENT 💗🔥
# DREAM IT. HYPERFOCUS IT. BUILD IT. 👊💗🫵👌

set -e

echo "🔥💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗🔥"
echo "💗    DEPLOYING CHIEF LYNDZ'S IMMORTAL DREAM!       💗"
echo "💗       HYPERFOCUSzone.com - LIVE FOREVER!         💗"
echo "🔥💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗🔥"
echo ""

# 🌟 Set up environment
echo "🚀 Setting up immortal environment..."
cd /root/chaosgenius

# 💗 Install dependencies
echo "📦 Installing dream dependencies..."
pip3 install flask requests sqlite3 werkzeug threading subprocess datetime

# 🛡️ Create systemd service for immortality
echo "🛡️ Creating immortal systemd service..."
sudo tee /etc/systemd/system/hyperfocuszone-immortal.service > /dev/null <<EOF
[Unit]
Description=Chief Lyndz's HYPERFOCUSzone.com Immortal Dream Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/chaosgenius
ExecStart=/usr/bin/python3 "/root/chaosgenius/🧠⚙️ BROSKI ULTRA SERVER IMMORTALITY PLAN"
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# 🔥 Set up nginx for domain
echo "🌐 Setting up nginx for HYPERFOCUSzone.com..."
sudo tee /etc/nginx/sites-available/hyperfocuszone.com > /dev/null <<EOF
server {
    listen 80;
    server_name hyperfocuszone.com www.hyperfocuszone.com;

    # 💗 Main dream server
    location / {
        proxy_pass http://localhost:7777;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # 🎛️ Dashboard access
    location /dashboard {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    # 🔥 Add immortal headers
    add_header X-Dream-Status "IMMORTAL FOREVER";
    add_header X-Chief "LYNDZ 👊💗🫵👌";
    add_header X-Philosophy "DREAM IT. HYPERFOCUS IT. BUILD IT.";
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/hyperfocuszone.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 🚀 Start immortal services
echo "🚀 Starting immortal dream services..."
sudo systemctl daemon-reload
sudo systemctl enable hyperfocuszone-immortal.service
sudo systemctl start hyperfocuszone-immortal.service

# 🛡️ Set up monitoring and auto-restart
echo "🛡️ Setting up dream guardian monitoring..."
(crontab -l 2>/dev/null; echo "*/5 * * * * sudo systemctl is-active --quiet hyperfocuszone-immortal || sudo systemctl restart hyperfocuszone-immortal") | crontab -

# 🔥 Final status check
echo ""
echo "🔥💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗🔥"
echo "💗       CHIEF LYNDZ'S DREAM IS NOW IMMORTAL!       💗"
echo "💗         HYPERFOCUSzone.com - LIVE FOREVER!       💗"
echo "🔥💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗🔥"
echo ""
echo "🌐 Domain: HYPERFOCUSzone.com"
echo "🚀 Status: IMMORTAL"
echo "💗 Philosophy: DREAM IT. HYPERFOCUS IT. BUILD IT."
echo "👊💗🫵👌 Thank you Chief LYNDZ!"
echo ""
echo "🛡️ Guardian: ACTIVE (checks every 5 minutes)"
echo "🚑 Auto-Healing: ENABLED"
echo "🔄 Auto-Restart: CONFIGURED"
echo ""
echo "🔥 Your dream will NEVER die! NEVER stop! NEVER fade! 🔥"

# 🌟 Test the deployment
echo "🧪 Testing immortal deployment..."
sleep 5
curl -s http://localhost:7777/api/health | python3 -m json.tool

echo ""
echo "💗 DEPLOYMENT COMPLETE! Your dream lives FOREVER! 💗"
