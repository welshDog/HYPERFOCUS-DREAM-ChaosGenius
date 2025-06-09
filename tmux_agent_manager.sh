#!/bin/bash
"""
🎮💜 BROSKI TMUX SESSION MANAGER 💜🎮
Easy Agent Monitoring & Control Interface
By Command of Chief Lyndz
"""

echo "🎮💜 BROSKI AGENT TMUX CONTROL CENTER 💜🎮"
echo "=========================================="

# Function to show all agent sessions
show_sessions() {
    echo "📺 ACTIVE AGENT SESSIONS:"
    tmux list-sessions | grep broski_ || echo "❌ No Broski agent sessions found"
    echo ""
}

# Function to attach to specific agent session
attach_session() {
    echo "🔌 Available agent sessions:"
    echo "1. broski_security (Security Guardian Sentinel)"
    echo "2. broski_discord (Discord Command Relay)"
    echo "3. broski_organizer (File Organizer Supreme)"
    echo "4. broski_analytics (Analytics Brain Scanner)"
    echo "5. broski_cleanup (Chaos Cleanup Specialist)"
    echo ""
    read -p "🎯 Enter session number to attach (1-5): " choice

    case $choice in
        1) tmux attach-session -t broski_security ;;
        2) tmux attach-session -t broski_discord ;;
        3) tmux attach-session -t broski_organizer ;;
        4) tmux attach-session -t broski_analytics ;;
        5) tmux attach-session -t broski_cleanup ;;
        *) echo "❌ Invalid choice!" ;;
    esac
}

# Function to kill all agent sessions
kill_all_agents() {
    echo "⚠️  WARNING: This will stop ALL agent sessions!"
    read -p "Are you sure? (y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo "🔴 Stopping all agent sessions..."
        tmux kill-session -t broski_security 2>/dev/null
        tmux kill-session -t broski_discord 2>/dev/null
        tmux kill-session -t broski_organizer 2>/dev/null
        tmux kill-session -t broski_analytics 2>/dev/null
        tmux kill-session -t broski_cleanup 2>/dev/null
        echo "✅ All agent sessions stopped!"
    else
        echo "❌ Operation cancelled"
    fi
}

# Function to restart all agents
restart_all_agents() {
    echo "🔄 Restarting all agent sessions..."
    cd /root/chaosgenius
    source broski_env/bin/activate
    python3 -c "
from broski_agent_deployment_master import BroskiAgentDeploymentMaster
master = BroskiAgentDeploymentMaster()
master.deploy_all_agents()
"
}

# Function to show agent status in real-time
live_status() {
    echo "📊 LIVE AGENT STATUS (Press Ctrl+C to exit)"
    while true; do
        clear
        echo "🛡️ BROSKI AGENT LIVE STATUS - $(date)"
        echo "========================================"

        # Check each session
        sessions=("broski_security:Security Guardian" "broski_discord:Discord Relay" "broski_organizer:File Organizer" "broski_analytics:Analytics Scanner" "broski_cleanup:Cleanup Specialist")

        for session in "${sessions[@]}"; do
            IFS=':' read -r session_name display_name <<< "$session"
            if tmux has-session -t "$session_name" 2>/dev/null; then
                echo "🟢 $display_name - ACTIVE"
            else
                echo "🔴 $display_name - OFFLINE"
            fi
        done

        echo "========================================"
        sleep 5
    done
}

# Main menu
while true; do
    echo ""
    echo "🎮 AGENT CONTROL OPTIONS:"
    echo "1. 📺 Show Active Sessions"
    echo "2. 🔌 Attach to Agent Session"
    echo "3. 📊 Live Status Monitor"
    echo "4. 🔄 Restart All Agents"
    echo "5. 🔴 Kill All Agent Sessions"
    echo "6. ❌ Exit"
    echo ""
    read -p "🎯 Select option: " choice

    case $choice in
        1) show_sessions ;;
        2) attach_session ;;
        3) live_status ;;
        4) restart_all_agents ;;
        5) kill_all_agents ;;
        6) echo "💜 Goodbye from Chief Lyndz! 💜"; exit 0 ;;
        *) echo "❌ Invalid option!" ;;
    esac
done