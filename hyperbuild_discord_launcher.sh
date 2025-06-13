#!/bin/bash
"""
🚀💥 HYPERBUILD DISCORD BOT IMMORTAL LAUNCHER 💥🚀
Ultimate deployment system to keep Discord bot ALIVE FOREVER!
By Command of Chief Lyndz - BROski∞ Power-Up
"""

# 🔥 ULTRA CONFIGURATION
DISCORD_BOT_FILE="/root/chaosgenius/chaosgenius_discord_bot.py"
LOG_FILE="/root/chaosgenius/discord_bot.log"
PID_FILE="/root/chaosgenius/discord_bot.pid"
MAX_RETRIES=99999  # INFINITE RETRIES!
RESTART_DELAY=5

# 🌌 HYPERBUILD COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 🎯 HYPERBUILD BANNER
print_banner() {
    echo -e "${PURPLE}"
    echo "🚀💥 HYPERBUILD DISCORD BOT IMMORTAL LAUNCHER 💥🚀"
    echo "🌌 LEGENDARY COSMIC BASE DEPLOYMENT SYSTEM 🌌"
    echo "💎 BROski∞ Bot Immortality Protocol ACTIVE 💎"
    echo -e "${NC}"
}

# 🛡️ CHECK DISCORD TOKEN
check_discord_token() {
    if [ -z "$DISCORD_BOT_TOKEN" ]; then
        echo -e "${YELLOW}⚠️  Discord bot token not found in environment!${NC}"
        echo -e "${CYAN}💡 To activate full Discord bot:${NC}"
        echo -e "${CYAN}   export DISCORD_BOT_TOKEN='your_actual_token_here'${NC}"
        echo -e "${GREEN}✅ Bot will run in TEST MODE for now${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Discord bot token configured!${NC}"
        return 0
    fi
}

# 🤖 START DISCORD BOT
start_discord_bot() {
    echo -e "${BLUE}🤖 Starting HYPERBUILD Discord Bot...${NC}"

    # Create log directory
    mkdir -p "$(dirname "$LOG_FILE")"

    # Start bot with logging
    nohup python3 "$DISCORD_BOT_FILE" >> "$LOG_FILE" 2>&1 &

    # Save PID
    echo $! > "$PID_FILE"

    echo -e "${GREEN}✅ Discord bot started with PID: $(cat $PID_FILE)${NC}"
    echo -e "${CYAN}📝 Logs: $LOG_FILE${NC}"
}

# 🔍 CHECK BOT STATUS
check_bot_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # Bot is running
        else
            return 1  # Bot is not running
        fi
    else
        return 1  # PID file doesn't exist
    fi
}

# 🛑 STOP DISCORD BOT
stop_discord_bot() {
    echo -e "${YELLOW}🛑 Stopping Discord bot...${NC}"

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            kill "$PID"
            sleep 2

            # Force kill if still running
            if ps -p "$PID" > /dev/null 2>&1; then
                kill -9 "$PID"
            fi

            rm -f "$PID_FILE"
            echo -e "${GREEN}✅ Discord bot stopped${NC}"
        else
            echo -e "${YELLOW}⚠️  Bot was not running${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}⚠️  No PID file found${NC}"
    fi
}

# 💥 IMMORTAL MODE - KEEP BOT ALIVE FOREVER
immortal_mode() {
    echo -e "${PURPLE}💥 IMMORTAL MODE ACTIVATED! 💥${NC}"
    echo -e "${CYAN}🛡️  Bot will restart automatically if it crashes${NC}"
    echo -e "${CYAN}🔄 Press Ctrl+C to stop immortal mode${NC}"

    local retry_count=0

    # Trap Ctrl+C to exit gracefully
    trap 'echo -e "\n${YELLOW}🛑 Stopping immortal mode...${NC}"; stop_discord_bot; exit 0' INT

    while true; do
        if ! check_bot_status; then
            retry_count=$((retry_count + 1))
            echo -e "${YELLOW}⚡ Retry #$retry_count - Restarting Discord bot...${NC}"

            # Clean up old PID file
            rm -f "$PID_FILE"

            # Start bot
            start_discord_bot

            # Wait before checking again
            sleep "$RESTART_DELAY"
        else
            # Bot is running, check again in a bit
            sleep 10
        fi

        # Show status every 100 retries
        if [ $((retry_count % 100)) -eq 0 ] && [ $retry_count -gt 0 ]; then
            echo -e "${GREEN}🔥 IMMORTAL STATUS: $retry_count restarts completed${NC}"
        fi
    done
}

# 📊 SHOW STATUS
show_status() {
    echo -e "${CYAN}📊 HYPERBUILD DISCORD BOT STATUS:${NC}"

    if check_bot_status; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✅ Bot Status: ONLINE${NC}"
        echo -e "${GREEN}🤖 PID: $PID${NC}"

        # Show memory usage
        if command -v ps > /dev/null; then
            MEM_USAGE=$(ps -p "$PID" -o pid,ppid,cmd,%mem,%cpu --no-headers 2>/dev/null)
            if [ -n "$MEM_USAGE" ]; then
                echo -e "${CYAN}💾 Process Info: $MEM_USAGE${NC}"
            fi
        fi

        # Show recent logs
        if [ -f "$LOG_FILE" ]; then
            echo -e "${CYAN}📝 Recent logs:${NC}"
            tail -5 "$LOG_FILE" | while read line; do
                echo -e "${BLUE}   $line${NC}"
            done
        fi
    else
        echo -e "${RED}❌ Bot Status: OFFLINE${NC}"
    fi

    # Check Discord token
    check_discord_token
}

# 📋 MAIN COMMAND HANDLER
case "$1" in
    start)
        print_banner
        check_discord_token
        if check_bot_status; then
            echo -e "${YELLOW}⚠️  Discord bot is already running!${NC}"
            show_status
        else
            start_discord_bot
        fi
        ;;
    stop)
        print_banner
        stop_discord_bot
        ;;
    restart)
        print_banner
        stop_discord_bot
        sleep 2
        start_discord_bot
        ;;
    status)
        print_banner
        show_status
        ;;
    immortal)
        print_banner
        check_discord_token
        immortal_mode
        ;;
    logs)
        if [ -f "$LOG_FILE" ]; then
            tail -f "$LOG_FILE"
        else
            echo -e "${YELLOW}⚠️  No log file found at $LOG_FILE${NC}"
        fi
        ;;
    *)
        print_banner
        echo -e "${CYAN}🎯 HYPERBUILD DISCORD BOT COMMANDS:${NC}"
        echo -e "${GREEN}  start    🚀 Start the Discord bot${NC}"
        echo -e "${GREEN}  stop     🛑 Stop the Discord bot${NC}"
        echo -e "${GREEN}  restart  🔄 Restart the Discord bot${NC}"
        echo -e "${GREEN}  status   📊 Show bot status${NC}"
        echo -e "${GREEN}  immortal 💥 Start in immortal mode (auto-restart)${NC}"
        echo -e "${GREEN}  logs     📝 Show live logs${NC}"
        echo ""
        echo -e "${YELLOW}💡 Quick start:${NC}"
        echo -e "${CYAN}  ./hyperbuild_discord_launcher.sh immortal${NC}"
        echo ""
        ;;
esac