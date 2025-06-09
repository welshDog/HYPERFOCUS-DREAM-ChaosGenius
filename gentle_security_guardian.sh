#!/bin/bash
# 🛡️ BROSKI GENTLE SECURITY GUARDIAN - FIXED VERSION
# Protects server WITHOUT disconnecting legitimate users

LOG_FILE="/var/log/broski-gentle-guardian.log"
echo "🛡️ Gentle Security Guardian Started - $(date)" >> $LOG_FILE

while true; do
    # GENTLE SSH monitoring - NO AGGRESSIVE RESTARTS!
    SSH_STATUS=$(systemctl is-active sshd)
    if [ "$SSH_STATUS" != "active" ]; then
        echo "$(date): SSH truly down - gentle restart..." >> $LOG_FILE
        systemctl start sshd  # start, not restart!
    else
        echo "$(date): SSH healthy - no action needed" >> $LOG_FILE
    fi

    # Monitor system load but DON'T kill processes aggressively
    LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    echo "$(date): Current load: $LOAD" >> $LOG_FILE

    # Only log high load, don't take action
    if (( $(echo "$LOAD > 8.0" | bc -l) 2>/dev/null )); then
        echo "$(date): WARNING - Very high load detected: $LOAD" >> $LOG_FILE
        # Just log it, don't kill anything!
    fi

    # Gentle memory monitoring
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    echo "$(date): Memory usage: ${MEM_USAGE}%" >> $LOG_FILE

    # Only clear caches if EXTREMELY high memory (95%+)
    if [ $MEM_USAGE -gt 95 ]; then
        echo "$(date): CRITICAL memory usage - clearing caches only" >> $LOG_FILE
        sync && echo 1 > /proc/sys/vm/drop_caches
    fi

    # Log connection count without killing connections
    CONNECTIONS=$(netstat -tn | grep :22 | grep ESTABLISHED | wc -l)
    echo "$(date): Active SSH connections: $CONNECTIONS" >> $LOG_FILE

    # MUCH longer sleep - check every 5 minutes instead of 30 seconds
    sleep 300
done