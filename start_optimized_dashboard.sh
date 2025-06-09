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
