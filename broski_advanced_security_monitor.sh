#!/bin/bash
# 🛡️ BROSKI ADVANCED SECURITY MONITOR
# Enhanced security monitoring based on agent recommendations

LOG_FILE="/var/log/broski_advanced_security.log"
echo "🛡️ Advanced Security Scan - $(date)" >> $LOG_FILE

# Check for failed login attempts
FAILED_LOGINS=$(grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l)
echo "Failed login attempts: $FAILED_LOGINS" >> $LOG_FILE

# Monitor SSH connections
ACTIVE_SSH=$(netstat -tn | grep :22 | grep ESTABLISHED | wc -l)
echo "Active SSH connections: $ACTIVE_SSH" >> $LOG_FILE

# Check system integrity
if command -v aide >/dev/null 2>&1; then
    echo "AIDE integrity checker available" >> $LOG_FILE
else
    echo "AIDE integrity checker not installed" >> $LOG_FILE
fi

# Monitor critical file changes
find /etc /root -type f -mtime -1 2>/dev/null | head -10 >> $LOG_FILE

echo "✅ Advanced security scan completed" >> $LOG_FILE
