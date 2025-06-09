#!/bin/bash
# 🧹 BROSKI AUTOMATED MAINTENANCE
# Advanced system cleanup and optimization

LOG_FILE="/var/log/broski_maintenance.log"
echo "🧹 Automated Maintenance Started - $(date)" >> $LOG_FILE

# Clean temporary files
find /tmp -type f -mtime +7 -delete 2>/dev/null
echo "✅ Cleaned old temporary files" >> $LOG_FILE

# Rotate logs if they get too large
find /var/log -name "*.log" -size +100M -exec gzip {} \; 2>/dev/null
echo "✅ Rotated large log files" >> $LOG_FILE

# Clean package cache
apt-get autoclean -y >/dev/null 2>&1
echo "✅ Cleaned package cache" >> $LOG_FILE

# Update file database
updatedb 2>/dev/null &
echo "✅ Updated file database" >> $LOG_FILE

# Optimize database files
cd /root/chaosgenius
for db in *.db; do
    if [ -f "$db" ]; then
        sqlite3 "$db" "VACUUM;" 2>/dev/null
        echo "✅ Optimized database: $db" >> $LOG_FILE
    fi
done

echo "🎉 Automated Maintenance Completed - $(date)" >> $LOG_FILE
