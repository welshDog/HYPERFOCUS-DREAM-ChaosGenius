#!/bin/bash
# 🚀 BROSKI ULTRA LOAD OPTIMIZER 🚀
# Optimizes server performance and reduces resource usage

echo "⚡ BROSKI LOAD OPTIMIZER ACTIVATED!"

# 1. Kill runaway processes
echo "🔥 Terminating resource-heavy processes..."

# Stop the runaway gunicorn process
pkill -f "gunicorn.*dashboard_api" 2>/dev/null && echo "✅ Killed runaway gunicorn process"

# Optimize VS Code server memory usage
echo "🧠 Optimizing VS Code server settings..."
mkdir -p ~/.vscode-server/data/User
cat > ~/.vscode-server/data/User/settings.json << 'EOF'
{
    "python.analysis.memory.keepLibraryAst": false,
    "python.analysis.autoImportCompletions": false,
    "python.analysis.indexing": false,
    "pylint.enabled": false,
    "flake8.enabled": false,
    "python.linting.enabled": false,
    "extensions.autoUpdate": false,
    "telemetry.telemetryLevel": "off",
    "search.followSymlinks": false,
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/**": true,
        "**/.hg/store/**": true,
        "**/venv/**": true,
        "**/__pycache__/**": true,
        "**/.mypy_cache/**": true
    }
}
EOF

# 2. Create optimized process manager
echo "⚙️ Setting up optimized process management..."
cat > /usr/local/bin/broski-process-optimizer << 'EOF'
#!/bin/bash
# Intelligent process management and optimization

LOG_FILE="/var/log/broski-optimizer.log"

optimize_processes() {
    echo "$(date): Starting process optimization..." >> $LOG_FILE

    # Kill duplicate Python processes
    PYTHON_PROCS=$(pgrep -f "python.*lsp_server" | wc -l)
    if [ $PYTHON_PROCS -gt 3 ]; then
        echo "$(date): Too many Python LSP servers ($PYTHON_PROCS), killing extras..." >> $LOG_FILE
        pkill -f "python.*lsp_server.py" 2>/dev/null
        sleep 2
    fi

    # Check for runaway gunicorn processes
    GUNICORN_CPU=$(ps aux | grep -v grep | grep gunicorn | awk '{sum+=$3} END {print sum+0}')
    if (( $(echo "$GUNICORN_CPU > 50" | bc -l) 2>/dev/null )); then
        echo "$(date): Gunicorn using too much CPU ($GUNICORN_CPU%), restarting..." >> $LOG_FILE
        pkill -f gunicorn 2>/dev/null
        sleep 3
        # Restart with optimized settings
        cd /root/chaosgenius
        nohup gunicorn --workers 1 --threads 2 --max-requests 1000 --max-requests-jitter 50 --preload --bind 0.0.0.0:5000 dashboard_api:app > /dev/null 2>&1 &
    fi

    # Clean up zombie processes
    ps aux | awk '$8 ~ /^Z/ { print $2 }' | xargs -r kill -9 2>/dev/null

    # Optimize memory usage
    echo 1 > /proc/sys/vm/drop_caches 2>/dev/null
}

# Run optimization every 2 minutes
while true; do
    optimize_processes
    sleep 120
done
EOF

chmod +x /usr/local/bin/broski-process-optimizer

# 3. Create systemd service for process optimization
echo "🛠️ Creating process optimizer service..."
cat > /etc/systemd/system/broski-process-optimizer.service << 'EOF'
[Unit]
Description=BROski Process Optimizer
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/broski-process-optimizer
Restart=always
RestartSec=30
User=root

[Install]
WantedBy=multi-user.target
EOF

# 4. Optimize system settings for better performance
echo "🚀 Applying system optimizations..."
cat >> /etc/sysctl.conf << 'EOF'
# BROski Performance Optimization
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.overcommit_memory = 1
kernel.sched_migration_cost_ns = 5000000
kernel.sched_autogroup_enabled = 0
EOF

# Apply settings
sysctl -p

# 5. Create optimized dashboard launcher
echo "📊 Creating optimized dashboard launcher..."
cat > /root/chaosgenius/start_optimized_dashboard.sh << 'EOF'
#!/bin/bash
# Optimized dashboard with resource limits

echo "🚀 Starting Optimized BROski Dashboard..."

# Kill any existing instances
pkill -f "gunicorn.*dashboard_api" 2>/dev/null
sleep 2

# Start with optimized settings
cd /root/chaosgenius

# Set resource limits
ulimit -v 2097152  # 2GB virtual memory limit
ulimit -m 1048576  # 1GB physical memory limit

# Start gunicorn with optimal settings
exec gunicorn \
    --workers 1 \
    --threads 2 \
    --worker-class sync \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --preload \
    --timeout 30 \
    --keep-alive 5 \
    --bind 0.0.0.0:5000 \
    dashboard_api:app
EOF

chmod +x /root/chaosgenius/start_optimized_dashboard.sh

# 6. Start services
echo "🚀 Starting optimization services..."
systemctl daemon-reload
systemctl enable broski-process-optimizer
systemctl start broski-process-optimizer

# 7. Restart dashboard with optimized settings
echo "📊 Restarting dashboard with optimization..."
pkill -f "gunicorn.*dashboard_api" 2>/dev/null
sleep 3
nohup /root/chaosgenius/start_optimized_dashboard.sh > /var/log/broski-dashboard.log 2>&1 &

echo "✅ BROSKI LOAD OPTIMIZER COMPLETE!"
echo "📊 Dashboard restarted with optimizations"
echo "🔧 Process optimizer running in background"
echo "📈 Monitor with: htop or systemctl status broski-process-optimizer"