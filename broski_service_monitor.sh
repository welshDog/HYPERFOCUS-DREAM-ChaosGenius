#!/bin/bash
"""
💜🛡️ BROSKI SERVICE MONITOR - ULTRA GUARDIAN PACK 🛡️💜
Complete System Health Monitor + Auto-Heal
By Command of Chief Lyndz - NEVER LOSE YOUR EMPIRE!
"""

LOG_FILE="/var/log/broski_service_monitor.log"
EMERGENCY_LOG="/var/log/broski_emergency.log"

echo "🛡️ BROSKI SERVICE MONITOR ACTIVATED - $(date)" >> $LOG_FILE

# 1️⃣ CHECK CRITICAL SERVICES
check_critical_services() {
    SERVICES=("ssh" "networking" "systemd-resolved")

    for service in "${SERVICES[@]}"; do
        if ! systemctl is-active --quiet $service; then
            echo "🚨 CRITICAL SERVICE DOWN: $service - RESTARTING!" >> $EMERGENCY_LOG
            sudo systemctl restart $service
            echo "🔄 Restarted $service at $(date)" >> $LOG_FILE
        else
            echo "✅ $service is running healthy" >> $LOG_FILE
        fi
    done
}

# 2️⃣ CHECK NETWORK CONNECTIVITY
check_network() {
    if ! ping -c 1 8.8.8.8 &> /dev/null; then
        echo "🚨 NETWORK CONNECTIVITY LOST - ATTEMPTING REPAIR!" >> $EMERGENCY_LOG
        sudo systemctl restart networking
        sudo systemctl restart systemd-networkd
        echo "🔄 Network services restarted at $(date)" >> $LOG_FILE
    else
        echo "✅ Network connectivity OK" >> $LOG_FILE
    fi
}

# 3️⃣ CHECK DISK SPACE
check_disk_space() {
    DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ $DISK_USAGE -gt 90 ]; then
        echo "🚨 DISK SPACE CRITICAL: ${DISK_USAGE}% - CLEANING!" >> $EMERGENCY_LOG
        # Emergency cleanup
        sudo apt-get autoremove -y &>/dev/null
        sudo apt-get autoclean -y &>/dev/null
        echo "🧹 Emergency disk cleanup completed at $(date)" >> $LOG_FILE
    else
        echo "✅ Disk space OK: ${DISK_USAGE}%" >> $LOG_FILE
    fi
}

# 4️⃣ CHECK MEMORY USAGE
check_memory() {
    MEM_USAGE=$(free | awk '/^Mem:/ {printf "%.0f", ($3/$2)*100}')
    if [ $MEM_USAGE -gt 95 ]; then
        echo "🚨 MEMORY CRITICAL: ${MEM_USAGE}% - CLEARING CACHE!" >> $EMERGENCY_LOG
        sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
        echo "🧠 Memory cache cleared at $(date)" >> $LOG_FILE
    else
        echo "✅ Memory usage OK: ${MEM_USAGE}%" >> $LOG_FILE
    fi
}

# 5️⃣ CHECK BROSKI PROCESSES
check_broski_processes() {
    if ! pgrep -f "FORGE THE BROSKI NEURAL OVERSEER" > /dev/null; then
        echo "🚨 BROSKI NEURAL OVERSEER OFFLINE - ATTEMPTING RESTART!" >> $EMERGENCY_LOG
        cd /root/chaosgenius
        source broski_env/bin/activate
        nohup python3 "FORGE THE BROSKI NEURAL OVERSEER SYSTEM" > /dev/null 2>&1 &
        echo "🧠 Broski Neural Overseer restarted at $(date)" >> $LOG_FILE
    else
        echo "✅ Broski Neural Overseer running" >> $LOG_FILE
    fi
}

# 6️⃣ NUCLEAR OPTION - LAST RESORT REBOOT
nuclear_reboot_check() {
    CRITICAL_FAILURES=$(grep -c "CRITICAL" $EMERGENCY_LOG)
    if [ $CRITICAL_FAILURES -gt 10 ]; then
        echo "🚨 NUCLEAR OPTION: Too many critical failures - SCHEDULING REBOOT!" >> $EMERGENCY_LOG
        echo "System will reboot in 5 minutes due to critical failures" | wall
        sudo shutdown -r +5 "BROSKI EMERGENCY REBOOT - Critical system failures detected"
    fi
}

# 🚀 MAIN EXECUTION
main() {
    echo "🛡️ Starting ULTRA GUARDIAN health check at $(date)"

    check_critical_services
    check_network
    check_disk_space
    check_memory
    check_broski_processes
    nuclear_reboot_check

    echo "✅ ULTRA GUARDIAN health check completed at $(date)" >> $LOG_FILE
}

# Execute the guardian
main