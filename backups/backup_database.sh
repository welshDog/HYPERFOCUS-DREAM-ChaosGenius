#!/bin/bash
# ChaosGenius Production Database Backup Script

DB_PATH="/workspaces/HYPERFOCUS-DREAM-ChaosGenius/chaosgenius.db"
BACKUP_DIR="/workspaces/HYPERFOCUS-DREAM-ChaosGenius/backups/database"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup with compression
sqlite3 "$DB_PATH" ".backup $BACKUP_DIR/chaosgenius_backup_$TIMESTAMP.db"
gzip "$BACKUP_DIR/chaosgenius_backup_$TIMESTAMP.db"

# Cleanup old backups (keep last 30 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "Database backup completed: chaosgenius_backup_$TIMESTAMP.db.gz"
