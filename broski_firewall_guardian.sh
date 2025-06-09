#!/bin/bash
"""
🛡️💜 BROSKI FIREWALL GUARDIAN v2.0 💜🛡️
UNBREAKABLE STEEL LINK™ - SSH Protection System
By Command of Chief Lyndz - NEVER GET LOCKED OUT AGAIN!
"""

# 🔥 ULTRA SSH PROTECTION PROTOCOL
LOG_FILE="/var/log/broski_firewall.log"
EMERGENCY_LOG="/var/log/broski_emergency.log"

echo "🛡️ BROSKI FIREWALL GUARDIAN ACTIVATED - $(date)" >> $LOG_FILE

# 1️⃣ CHECK SSH PORT 22 STATUS
check_ssh_port() {
    if ! sudo netstat -tuln | grep -q ":22 "; then
        echo "🚨 EMERGENCY: SSH Port 22 NOT LISTENING!" >> $EMERGENCY_LOG
        sudo systemctl restart ssh
        sudo systemctl restart sshd 2>/dev/null
        echo "🔄 SSH service restarted at $(date)" >> $LOG_FILE
    fi
}

# 2️⃣ FORCE OPEN SSH PORT WITH MULTIPLE METHODS
force_open_ssh() {
    echo "🔓 FORCING SSH PORT 22 OPEN..." >> $LOG_FILE

    # UFW method
    sudo ufw allow 22/tcp 2>/dev/null
    sudo ufw allow ssh 2>/dev/null

    # iptables method (backup)
    sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT 2>/dev/null
    sudo iptables -A INPUT -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT 2>/dev/null

    # ip6tables for IPv6
    sudo ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT 2>/dev/null

    echo "✅ SSH PORT 22 FORCED OPEN with multiple methods at $(date)" >> $LOG_FILE
}

# 3️⃣ CHECK AND FIX SSH CONFIGURATION
fix_ssh_config() {
    SSH_CONFIG="/etc/ssh/sshd_config"

    if [ -f "$SSH_CONFIG" ]; then
        # Backup original config
        sudo cp $SSH_CONFIG $SSH_CONFIG.broski_backup_$(date +%Y%m%d) 2>/dev/null

        # Ensure SSH is enabled and configured properly
        sudo sed -i 's/#Port 22/Port 22/g' $SSH_CONFIG
        sudo sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/g' $SSH_CONFIG
        sudo sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' $SSH_CONFIG

        echo "🔧 SSH config verified/fixed at $(date)" >> $LOG_FILE
    fi
}

# 4️⃣ EMERGENCY SSH RESTART IF NEEDED
emergency_ssh_restart() {
    if ! pgrep -f "sshd" > /dev/null; then
        echo "🚨 EMERGENCY: SSH daemon not running! Restarting..." >> $EMERGENCY_LOG
        sudo systemctl enable ssh
        sudo systemctl start ssh
        sudo service ssh restart
        echo "🆘 Emergency SSH restart completed at $(date)" >> $EMERGENCY_LOG
    fi
}

# 5️⃣ MAIN GUARDIAN EXECUTION
main() {
    echo "🛡️ Starting Guardian check at $(date)"

    # Run all protection methods
    check_ssh_port
    force_open_ssh
    fix_ssh_config
    emergency_ssh_restart

    # Final verification
    if sudo netstat -tuln | grep -q ":22 " && pgrep -f "sshd" > /dev/null; then
        echo "✅ SSH Port 22 is SECURE and OPEN at $(date)" >> $LOG_FILE
    else
        echo "🚨 CRITICAL: SSH still has issues after guardian run!" >> $EMERGENCY_LOG
        # Nuclear option - restart networking
        sudo systemctl restart networking 2>/dev/null
    fi
}

# 🚀 EXECUTE GUARDIAN
main

# 💜 BROSKI SIGNATURE
echo "💜 BROSKI FIREWALL GUARDIAN COMPLETED PROTECTION SWEEP 💜" >> $LOG_FILE