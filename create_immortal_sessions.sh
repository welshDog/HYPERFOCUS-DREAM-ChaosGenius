#!/bin/bash
# Create persistent tmux sessions that survive disconnections

# Kill any existing sessions first
tmux kill-server 2>/dev/null || true

# Create immortal sessions
tmux new-session -d -s "broski_immortal_main" -c "/root/chaosgenius"
tmux new-session -d -s "broski_immortal_backup" -c "/root/chaosgenius"
tmux new-session -d -s "broski_emergency_shell" -c "/root/chaosgenius"

# Set up auto-restart for critical sessions
tmux send-keys -t "broski_immortal_main" "while true; do echo 'BROski Immortal Session Active'; sleep 60; done" Enter
tmux send-keys -t "broski_immortal_backup" "python3 app.py" Enter

echo "🌌 Immortal tmux sessions created!"
echo "🔓 Access with: tmux attach -t broski_immortal_main"
