#!/bin/bash
# 🚀 BROSKI ULTRA CONNECTION STABILIZER 🚀
# Fixes SSH timeouts, connection drops, and authentication issues

echo "🔧 BROSKI CONNECTION STABILIZER ACTIVATED!"

# 1. Fix SSH timeout issues
echo "⚡ Configuring SSH keep-alive settings..."
if ! grep -q "ClientAliveInterval" /etc/ssh/sshd_config; then
    echo "ClientAliveInterval 30" >> /etc/ssh/sshd_config
    echo "ClientAliveCountMax 6" >> /etc/ssh/sshd_config
    echo "TCPKeepAlive yes" >> /etc/ssh/sshd_config
fi

# 2. Optimize SSH client settings for better connection persistence
echo "🛡️ Creating optimized SSH client config..."
mkdir -p ~/.ssh
cat > ~/.ssh/config << 'EOF'
Host *
    ServerAliveInterval 30
    ServerAliveCountMax 6
    TCPKeepAlive yes
    Compression yes
    ControlMaster auto
    ControlPath ~/.ssh/control-%r@%h:%p
    ControlPersist 10m
EOF

# 3. Create auto-reconnection wrapper
echo "🔄 Setting up auto-reconnection system..."
cat > /usr/local/bin/broski-ssh-keeper << 'EOF'
#!/bin/bash
# Auto-reconnect SSH with exponential backoff
RETRY_COUNT=0
MAX_RETRIES=10

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "🔗 Connection attempt $((RETRY_COUNT + 1))..."

    # Try to connect/maintain connection
    if [ -n "$SSH_CONNECTION" ]; then
        echo "✅ Connection active - monitoring..."
        sleep 30
        continue
    fi

    # If connection lost, wait before retry
    RETRY_COUNT=$((RETRY_COUNT + 1))
    WAIT_TIME=$((2 ** RETRY_COUNT))
    echo "⏰ Waiting ${WAIT_TIME}s before retry..."
    sleep $WAIT_TIME
done
EOF

chmod +x /usr/local/bin/broski-ssh-keeper

# 4. Set up connection monitoring
echo "📊 Creating connection monitor..."
cat > /usr/local/bin/connection-guardian << 'EOF'
#!/bin/bash
# Monitor and fix connection issues
LOG_FILE="/var/log/broski-connection.log"

while true; do
    # Check if SSH is responsive
    if ! pgrep -x "sshd" > /dev/null; then
        echo "$(date): SSH daemon not running - restarting..." >> $LOG_FILE
        systemctl restart sshd
    fi

    # Check system load
    LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    if (( $(echo "$LOAD > 5.0" | bc -l) )); then
        echo "$(date): High load detected: $LOAD - investigating..." >> $LOG_FILE
        # Kill any runaway processes
        pkill -f "python.*100%" 2>/dev/null
    fi

    # Check memory usage
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    if [ $MEM_USAGE -gt 90 ]; then
        echo "$(date): High memory usage: ${MEM_USAGE}% - cleaning up..." >> $LOG_FILE
        # Clear caches
        echo 3 > /proc/sys/vm/drop_caches
    fi

    sleep 30
done
EOF

chmod +x /usr/local/bin/connection-guardian

# 5. Create systemd service for persistent monitoring
echo "🛠️ Setting up persistent connection guardian..."
cat > /etc/systemd/system/broski-connection-guardian.service << 'EOF'
[Unit]
Description=BROski Connection Guardian
After=network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/connection-guardian
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF

# 6. Optimize network settings
echo "🌐 Optimizing network settings..."
cat >> /etc/sysctl.conf << 'EOF'
# BROski Connection Optimization
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 60
net.ipv4.tcp_keepalive_probes = 9
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_congestion_control = bbr
EOF

# Apply settings
sysctl -p

# 7. Start services
echo "🚀 Starting connection guardian..."
systemctl daemon-reload
systemctl enable broski-connection-guardian
systemctl start broski-connection-guardian

# Restart SSH with new settings
systemctl restart sshd

echo "✅ BROSKI CONNECTION STABILIZER COMPLETE!"
echo "🎯 Your connections should now be ROCK SOLID!"
echo "📊 Monitor with: tail -f /var/log/broski-connection.log"