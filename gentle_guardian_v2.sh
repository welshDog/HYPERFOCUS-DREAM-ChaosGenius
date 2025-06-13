#!/bin/bash
# 🛡️ BROSKI GENTLE GUARDIAN v2.0 - DASHBOARD & DISCORD EDITION
# Protects server WITHOUT disconnecting users + logs to dashboard/Discord

LOG_FILE="/var/log/broski-gentle-guardian.log"
DASHBOARD_LOG="/var/log/broski-dashboard.log"
DISCORD_WEBHOOK_URL=""  # Add your Discord webhook URL here if you want Discord alerts

# Function to log to multiple destinations
log_message() {
    local message="$1"
    local level="$2"  # INFO, WARNING, CRITICAL
    local timestamp=$(date)

    # Log to file
    echo "[$level] $timestamp: $message" >> $LOG_FILE

    # Log to dashboard
    echo "{\"timestamp\": \"$timestamp\", \"level\": \"$level\", \"message\": \"$message\", \"source\": \"gentle_guardian\"}" >> $DASHBOARD_LOG

    # Optional Discord notification (only for WARNING and CRITICAL)
    if [[ "$level" == "WARNING" || "$level" == "CRITICAL" ]] && [[ -n "$DISCORD_WEBHOOK_URL" ]]; then
        curl -H "Content-Type: application/json" \
             -X POST \
             -d "{\"content\": \"🛡️ **Gentle Guardian Alert** [$level]\n$message\"}" \
             "$DISCORD_WEBHOOK_URL" 2>/dev/null
    fi
}

log_message "🛡️ Gentle Guardian v2.0 Started - Dashboard & Discord Edition" "INFO"

while true; do
    # GENTLE SSH monitoring - NO AGGRESSIVE RESTARTS!
    SSH_STATUS=$(systemctl is-active sshd)
    if [ "$SSH_STATUS" != "active" ]; then
        log_message "SSH service detected as down - performing gentle restart" "WARNING"
        systemctl start sshd  # start, not restart!
        sleep 5
        NEW_STATUS=$(systemctl is-active sshd)
        if [ "$NEW_STATUS" == "active" ]; then
            log_message "SSH service successfully restored" "INFO"
        else
            log_message "SSH service failed to start - manual intervention may be required" "CRITICAL"
        fi
    else
        log_message "SSH service healthy and running normally" "INFO"
    fi

    # Monitor system load but DON'T kill processes aggressively
    LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    log_message "Current system load: $LOAD" "INFO"

    # Only log high load, don't take action
    if (( $(echo "$LOAD > 8.0" | bc -l) 2>/dev/null )); then
        log_message "Very high system load detected: $LOAD - monitoring only, no action taken" "WARNING"
    elif (( $(echo "$LOAD > 15.0" | bc -l) 2>/dev/null )); then
        log_message "EXTREME system load detected: $LOAD - consider manual intervention" "CRITICAL"
    fi

    # Gentle memory monitoring
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    log_message "Memory usage: ${MEM_USAGE}%" "INFO"

    # Only clear caches if EXTREMELY high memory (95%+)
    if [ $MEM_USAGE -gt 95 ]; then
        log_message "CRITICAL memory usage detected (${MEM_USAGE}%) - clearing system caches only" "CRITICAL"
        sync && echo 1 > /proc/sys/vm/drop_caches
        sleep 2
        NEW_MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
        log_message "Memory usage after cache clear: ${NEW_MEM_USAGE}%" "INFO"
    elif [ $MEM_USAGE -gt 85 ]; then
        log_message "High memory usage detected (${MEM_USAGE}%) - monitoring closely" "WARNING"
    fi

    # Log connection count without killing connections
    CONNECTIONS=$(netstat -tn | grep :22 | grep ESTABLISHED | wc -l 2>/dev/null || echo "0")
    log_message "Active SSH connections: $CONNECTIONS" "INFO"

    # Monitor disk space
    DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    log_message "Root disk usage: ${DISK_USAGE}%" "INFO"

    if [ $DISK_USAGE -gt 90 ]; then
        log_message "CRITICAL disk space warning: ${DISK_USAGE}% full - cleanup recommended" "CRITICAL"
    elif [ $DISK_USAGE -gt 80 ]; then
        log_message "High disk usage detected: ${DISK_USAGE}% full - monitoring" "WARNING"
    fi

    # Check web server status (gentle monitoring)
    WEB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null)
    if [ "$WEB_STATUS" == "200" ]; then
        log_message "Web server responding normally (HTTP 200)" "INFO"
    else
        log_message "Web server not responding (HTTP $WEB_STATUS) - may need attention" "WARNING"
    fi

    # GENTLE 5-minute sleep - much more relaxed than aggressive guardians
    log_message "Gentle Guardian cycle complete - sleeping for 5 minutes" "INFO"
    sleep 300
done