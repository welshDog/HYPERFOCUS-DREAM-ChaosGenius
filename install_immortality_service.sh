#!/bin/bash
"""
🛡️ IMMORTALITY PROTOCOL SYSTEMD INSTALLER 🛡️
=============================================
Install immortality as a system service for ETERNAL OPERATION
"""

# Create the systemd service file
cat > /etc/systemd/system/chaosgenius-immortality.service << 'EOF'
[Unit]
Description=🛡️ ChaosGenius Immortality Protocol - Quantum Redundancy System
Documentation=https://github.com/chaosgenius/immortality
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/chaosgenius
Environment=PYTHONPATH=/root/chaosgenius
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 /root/chaosgenius/immortality_protocol_core.py
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
Restart=always
RestartSec=10
StartLimitInterval=300
StartLimitBurst=5

# Immortality-level security and isolation
NoNewPrivileges=false
PrivateTmp=false
PrivateDevices=false
ProtectHome=false
ProtectSystem=false
ReadWritePaths=/root/chaosgenius /tmp /var/log

# Resource management for optimal performance
LimitNOFILE=65536
LimitNPROC=32768
OOMScoreAdjust=-100

# Logging configuration
StandardOutput=journal
StandardError=journal
SyslogIdentifier=chaosgenius-immortality

[Install]
WantedBy=multi-user.target
EOF

echo "🛡️ Systemd service file created!"

# Install required Python packages
echo "📦 Installing immortality dependencies..."
pip3 install psutil requests asyncio

# Create logs directory
mkdir -p /root/chaosgenius/logs
chmod 755 /root/chaosgenius/logs

# Create immortality configuration
cat > /root/chaosgenius/immortality_config.json << 'EOF'
{
  "check_interval": 15,
  "auto_restart_enabled": true,
  "max_restart_attempts": 5,
  "health_check_timeout": 10,
  "quantum_redundancy_enabled": true,
  "emergency_protocols": {
    "cpu_threshold": 90.0,
    "memory_threshold": 85.0,
    "disk_threshold": 95.0
  },
  "notification_webhooks": [],
  "backup_locations": [
    "/root/chaosgenius/backups",
    "/tmp/chaosgenius_emergency_backup"
  ],
  "critical_services": [
    "chaosgenius_discord_bot.py",
    "dashboard_api.py",
    "app.py",
    "broski_ultra_launcher.py",
    "agent_army_forge_master.py"
  ]
}
EOF

echo "⚙️ Immortality configuration created!"

# Set proper permissions
chmod +x /root/chaosgenius/immortality_protocol_core.py
chmod 644 /root/chaosgenius/immortality_config.json

# Reload systemd
systemctl daemon-reload

# Enable the service to start on boot
systemctl enable chaosgenius-immortality.service

echo "🛡️ Immortality Protocol systemd service installed!"
echo "🚀 Starting immortality service..."

# Start the service
systemctl start chaosgenius-immortality.service

# Check status
systemctl status chaosgenius-immortality.service

echo ""
echo "🛡️ IMMORTALITY PROTOCOL STATUS:"
echo "================================"
echo "Service Status: $(systemctl is-active chaosgenius-immortality.service)"
echo "Boot Enabled: $(systemctl is-enabled chaosgenius-immortality.service)"
echo ""
echo "📋 IMMORTALITY COMMANDS:"
echo "========================"
echo "🔍 Check Status: systemctl status chaosgenius-immortality"
echo "📊 View Logs: journalctl -fu chaosgenius-immortality"
echo "🔄 Restart: systemctl restart chaosgenius-immortality"
echo "🛑 Stop: systemctl stop chaosgenius-immortality"
echo "⚡ Reload Config: systemctl reload chaosgenius-immortality"
echo ""
echo "🛡️ IMMORTALITY PROTOCOL IS NOW ETERNAL! 🛡️"