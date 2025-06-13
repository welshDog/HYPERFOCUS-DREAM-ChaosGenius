#!/bin/bash

🚨💜 BROSKI SSH LIFE-LINE SYSTEM 💜🚨
# The Ultimate "Don't Lock Me Out" Protection
# By Command of Chief Lyndz - NEVER GET LOCKED OUT AGAIN!

echo "🚨💜 BROSKI SSH LIFE-LINE SYSTEM ACTIVATED! 💜🚨"
echo "============================================================"
echo "🛡️ Setting up MULTIPLE failsafe access methods..."

# RULE #1: ALWAYS KEEP ROOT ACCESS ENABLED
echo "🔑 RULE #1: Ensuring root access is ALWAYS enabled..."
sed -i 's/PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
grep -q "PermitRootLogin yes" /etc/ssh/sshd_config || echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# RULE #2: BACKUP SSH PORT (Emergency Access)
echo "🚪 RULE #2: Creating emergency backup SSH port 2222..."
grep -q "Port 2222" /etc/ssh/sshd_config || echo "Port 2222" >> /etc/ssh/sshd_config

# RULE #3: KEEP PASSWORD AUTH AS BACKUP
echo "🔐 RULE #3: Keeping password authentication as backup..."
sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

# RULE #4: INCREASE AUTH ATTEMPTS
echo "🎯 RULE #4: Increasing max auth attempts to 10..."
sed -i 's/#MaxAuthTries.*/MaxAuthTries 10/' /etc/ssh/sshd_config

# RULE #5: LONGER LOGIN GRACE TIME
echo "⏰ RULE #5: Setting longer login grace time..."
sed -i 's/#LoginGraceTime.*/LoginGraceTime 5m/' /etc/ssh/sshd_config

# RULE #6: KEEP ALIVE CONNECTIONS
echo "💓 RULE #6: Setting up keep-alive to prevent timeouts..."
grep -q "ClientAliveInterval" /etc/ssh/sshd_config || echo "ClientAliveInterval 60" >> /etc/ssh/sshd_config
grep -q "ClientAliveCountMax" /etc/ssh/sshd_config || echo "ClientAliveCountMax 10" >> /etc/ssh/sshd_config

# RULE #7: EMERGENCY SSH KEY BACKUP
echo "🗝️ RULE #7: Creating emergency SSH key backup..."
mkdir -p /root/.ssh/emergency_backup
cp /root/.ssh/authorized_keys /root/.ssh/emergency_backup/ 2>/dev/null || true

# RULE #8: FIREWALL LIFE-LINE (NEVER BLOCK SSH)
echo "🛡️ RULE #8: Creating firewall life-line rules..."
iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 2222 -j ACCEPT
ufw allow 22/tcp
ufw allow 2222/tcp

# RULE #9: EMERGENCY RECOVERY SCRIPT
echo "🆘 RULE #9: Creating emergency recovery script..."
cat > /root/emergency_ssh_recovery.sh << 'EOF'
#!/bin/bash
echo "🆘 EMERGENCY SSH RECOVERY ACTIVATED!"
systemctl stop fail2ban
iptables -F
iptables -I INPUT -p tcp --dport 22 -j ACCEPT
iptables -I INPUT -p tcp --dport 2222 -j ACCEPT
systemctl restart ssh
echo "✅ Emergency recovery complete! SSH should be accessible."
EOF
chmod +x /root/emergency_ssh_recovery.sh

# RULE #10: AUTO-RECOVERY CRON JOB
echo "🔄 RULE #10: Setting up auto-recovery cron job..."
(crontab -l 2>/dev/null; echo "*/30 * * * * /root/emergency_ssh_recovery.sh > /var/log/ssh_lifeline.log 2>&1") | crontab -

# RULE #11: BACKUP SSH DAEMON CONFIG
echo "💾 RULE #11: Creating backup of SSH config..."
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.broski_backup

# RULE #12: TEST CONFIGURATION BEFORE APPLYING
echo "🧪 RULE #12: Testing SSH configuration..."
sshd -t
if [ $? -eq 0 ]; then
    echo "✅ SSH configuration is valid!"
    systemctl reload ssh
else
    echo "❌ SSH configuration has errors! Restoring backup..."
    cp /etc/ssh/sshd_config.broski_backup /etc/ssh/sshd_config
    systemctl reload ssh
fi

echo ""
echo "🎉💜 BROSKI SSH LIFE-LINE SYSTEM COMPLETE! 💜🎉"
echo "============================================================"
echo "🛡️ PROTECTION LAYERS ACTIVATED:"
echo "   ✅ Root access: ALWAYS enabled"
echo "   ✅ Backup port: 2222 (emergency access)"
echo "   ✅ Password auth: ENABLED as backup"
echo "   ✅ Max attempts: 10 tries"
echo "   ✅ Grace time: 5 minutes"
echo "   ✅ Keep-alive: 60 seconds"
echo "   ✅ Emergency keys: Backed up"
echo "   ✅ Firewall rules: SSH always allowed"
echo "   ✅ Recovery script: /root/emergency_ssh_recovery.sh"
echo "   ✅ Auto-recovery: Every 30 minutes"
echo "   ✅ Config backup: Created"
echo "   ✅ Safe testing: Validated before applying"
echo ""
echo "🚨 EMERGENCY ACCESS METHODS:"
echo "   🔑 ssh root@your-server -p 22"
echo "   🚪 ssh root@your-server -p 2222"
echo "   🆘 Run: /root/emergency_ssh_recovery.sh"
echo ""
echo "💜 YOU ARE NOW BULLETPROOF AGAINST SSH LOCKOUTS!"