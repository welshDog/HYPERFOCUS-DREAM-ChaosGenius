#!/bin/bash

# 🗂️💪 ULTRA FILE KEEPER HYPER LAUNCHER 💪🗂️
# 🚀 One-command launch for the entire File Keeper ecosystem! 🚀

echo "🗂️💪🔥 ULTRA FILE KEEPER HYPER LAUNCHER ACTIVATED! 🔥💪🗂️"
echo "🌟 Launching the most LEGENDARY file management system! 🌟"

# Colors for epic output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to print epic headers
print_header() {
    echo -e "\n${CYAN}================================================${NC}"
    echo -e "${WHITE}🚀 $1 🚀${NC}"
    echo -e "${CYAN}================================================${NC}\n"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
print_header "CHECKING SYSTEM READINESS"

if command_exists python3; then
    echo -e "${GREEN}✅ Python3 detected${NC}"
else
    echo -e "${RED}❌ Python3 required but not found${NC}"
    exit 1
fi

if command_exists pip3; then
    echo -e "${GREEN}✅ pip3 detected${NC}"
else
    echo -e "${YELLOW}⚠️ pip3 not found, trying pip...${NC}"
    if ! command_exists pip; then
        echo -e "${RED}❌ pip required but not found${NC}"
        exit 1
    fi
fi

# Install required packages
print_header "INSTALLING HYPER DEPENDENCIES"

echo -e "${BLUE}📦 Installing required Python packages...${NC}"
pip3 install --quiet watchdog psutil sqlite3 || {
    echo -e "${YELLOW}⚠️ Some packages may already be installed${NC}"
}

# Set up the workspace
print_header "PREPARING ULTRA WORKSPACE"

WORKSPACE_DIR="/root/chaosgenius"
cd "$WORKSPACE_DIR" || {
    echo -e "${RED}❌ Could not access workspace directory: $WORKSPACE_DIR${NC}"
    exit 1
}

echo -e "${GREEN}✅ Workspace ready at: $WORKSPACE_DIR${NC}"

# Function to run file keeper agent
run_file_keeper() {
    print_header "LAUNCHING ULTRA FILE KEEPER AGENT"

    echo -e "${PURPLE}🤖 Starting Ultra File Keeper Agent...${NC}"
    python3 ultra_file_keeper_agent.py &
    AGENT_PID=$!
    echo -e "${GREEN}✅ Agent running with PID: $AGENT_PID${NC}"

    # Wait a moment for agent to initialize
    sleep 2

    return $AGENT_PID
}

# Function to run command portal
run_command_portal() {
    print_header "LAUNCHING COMMAND PORTAL"

    echo -e "${PURPLE}🎮 Starting Command Portal...${NC}"
    python3 ultra_file_keeper_command_portal.py &
    PORTAL_PID=$!
    echo -e "${GREEN}✅ Command Portal running with PID: $PORTAL_PID${NC}"

    return $PORTAL_PID
}

# Function to open dashboard
open_dashboard() {
    print_header "OPENING HYPER DASHBOARD"

    DASHBOARD_FILE="$WORKSPACE_DIR/ultra_file_keeper_dashboard.html"

    if [[ -f "$DASHBOARD_FILE" ]]; then
        echo -e "${CYAN}🌐 Dashboard available at: file://$DASHBOARD_FILE${NC}"

        # Try to open in browser (Linux)
        if command_exists xdg-open; then
            echo -e "${BLUE}🚀 Opening dashboard in browser...${NC}"
            xdg-open "$DASHBOARD_FILE" 2>/dev/null &
        elif command_exists firefox; then
            echo -e "${BLUE}🚀 Opening dashboard in Firefox...${NC}"
            firefox "$DASHBOARD_FILE" 2>/dev/null &
        elif command_exists chromium; then
            echo -e "${BLUE}🚀 Opening dashboard in Chromium...${NC}"
            chromium "$DASHBOARD_FILE" 2>/dev/null &
        else
            echo -e "${YELLOW}📖 Please open the dashboard manually in your browser${NC}"
        fi
    else
        echo -e "${RED}❌ Dashboard file not found${NC}"
    fi
}

# Function to show status
show_status() {
    print_header "SYSTEM STATUS CHECK"

    echo -e "${CYAN}📊 Ultra File Keeper System Status:${NC}"
    echo -e "  🗂️ Workspace: $WORKSPACE_DIR"
    echo -e "  📁 Total files in root: $(ls -1 | wc -l)"
    echo -e "  💾 Disk usage: $(df -h . | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')"
    echo -e "  🕒 Current time: $(date)"

    # Check if agents are running
    if pgrep -f "ultra_file_keeper_agent.py" > /dev/null; then
        echo -e "  ${GREEN}✅ File Keeper Agent: RUNNING${NC}"
    else
        echo -e "  ${RED}❌ File Keeper Agent: STOPPED${NC}"
    fi

    if pgrep -f "ultra_file_keeper_command_portal.py" > /dev/null; then
        echo -e "  ${GREEN}✅ Command Portal: RUNNING${NC}"
    else
        echo -e "  ${RED}❌ Command Portal: STOPPED${NC}"
    fi
}

# Function to stop all services
stop_services() {
    print_header "STOPPING SERVICES"

    echo -e "${YELLOW}🛑 Stopping Ultra File Keeper services...${NC}"

    pkill -f "ultra_file_keeper_agent.py" 2>/dev/null && echo -e "${GREEN}✅ File Keeper Agent stopped${NC}"
    pkill -f "ultra_file_keeper_command_portal.py" 2>/dev/null && echo -e "${GREEN}✅ Command Portal stopped${NC}"

    echo -e "${GREEN}✅ All services stopped${NC}"
}

# Function to run quick scan
quick_scan() {
    print_header "EXECUTING QUICK SCAN"

    echo -e "${PURPLE}🔍 Running quick file system scan...${NC}"
    python3 -c "
import asyncio
import sys
sys.path.append('.')

async def quick_scan():
    try:
        from ultra_file_keeper_agent import UltraFileKeeperAgent
        agent = UltraFileKeeperAgent()
        results = await agent.hyper_file_scan()

        print(f'📊 Quick Scan Results:')
        print(f'  📁 Total files: {results[\"total_files\"]}')
        print(f'  💾 Total size: {results[\"total_size\"]}')
        print(f'  📂 Categories found: {len(results[\"categories\"])}')
        print(f'  🔍 Large files: {len(results[\"large_files\"])}')
        print(f'  📋 Organization opportunities: {len(results[\"organization_opportunities\"])}')
        print(f'  🔄 Potential duplicates: {len(results[\"duplicates\"])}')

    except Exception as e:
        print(f'❌ Scan failed: {e}')

asyncio.run(quick_scan())
"
}

# Main menu
show_menu() {
    echo -e "\n${WHITE}🎮 ULTRA FILE KEEPER CONTROL CENTER 🎮${NC}"
    echo -e "${CYAN}Choose your command, commander:${NC}"
    echo ""
    echo -e "  ${GREEN}1)${NC} 🚀 Launch Full System (Agent + Portal + Dashboard)"
    echo -e "  ${GREEN}2)${NC} 🤖 Launch Agent Only"
    echo -e "  ${GREEN}3)${NC} 🎮 Launch Command Portal Only"
    echo -e "  ${GREEN}4)${NC} 🌐 Open Dashboard"
    echo -e "  ${GREEN}5)${NC} 🔍 Quick File Scan"
    echo -e "  ${GREEN}6)${NC} 📊 Show System Status"
    echo -e "  ${GREEN}7)${NC} 🛑 Stop All Services"
    echo -e "  ${GREEN}8)${NC} 📖 Show Help"
    echo -e "  ${GREEN}9)${NC} 🚪 Exit"
    echo ""
    echo -ne "${YELLOW}Enter your choice [1-9]: ${NC}"
}

# Help function
show_help() {
    print_header "ULTRA FILE KEEPER HELP GUIDE"

    echo -e "${CYAN}🎯 What each option does:${NC}"
    echo ""
    echo -e "${GREEN}🚀 Launch Full System:${NC}"
    echo -e "   Starts the complete Ultra File Keeper ecosystem:"
    echo -e "   • File Keeper Agent (background file monitoring & organization)"
    echo -e "   • Command Portal (API and command interface)"
    echo -e "   • Dashboard (web-based visual interface)"
    echo ""
    echo -e "${GREEN}🤖 Launch Agent Only:${NC}"
    echo -e "   Starts just the core File Keeper Agent for background operation"
    echo ""
    echo -e "${GREEN}🎮 Launch Command Portal:${NC}"
    echo -e "   Starts the command interface for manual control"
    echo ""
    echo -e "${GREEN}🌐 Open Dashboard:${NC}"
    echo -e "   Opens the web-based dashboard in your browser"
    echo ""
    echo -e "${GREEN}🔍 Quick File Scan:${NC}"
    echo -e "   Performs a rapid scan of your file system and shows results"
    echo ""
    echo -e "${GREEN}📊 Show System Status:${NC}"
    echo -e "   Displays current system status and running services"
    echo ""
    echo -e "${YELLOW}💡 Pro Tips:${NC}"
    echo -e "   • Use option 1 for first-time setup"
    echo -e "   • Option 5 is great for quick health checks"
    echo -e "   • Dashboard provides the best visual experience"
    echo -e "   • Command Portal allows advanced scripting and automation"
    echo ""
}

# Cleanup function for graceful exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down Ultra File Keeper...${NC}"
    stop_services
    echo -e "${CYAN}👋 Thanks for using Ultra File Keeper! Stay organized! 💪${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    # Show epic startup banner
    echo -e "${PURPLE}"
    echo "██╗   ██╗██╗  ████████╗██████╗  █████╗     ███████╗██╗██╗     ███████╗"
    echo "██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗    ██╔════╝██║██║     ██╔════╝"
    echo "██║   ██║██║     ██║   ██████╔╝███████║    █████╗  ██║██║     █████╗  "
    echo "██║   ██║██║     ██║   ██╔══██╗██╔══██║    ██╔══╝  ██║██║     ██╔══╝  "
    echo "╚██████╔╝███████╗██║   ██║  ██║██║  ██║    ██║     ██║███████╗███████╗"
    echo " ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝╚══════╝"
    echo ""
    echo "██╗  ██╗███████╗███████╗██████╗ ███████╗██████╗ "
    echo "██║ ██╔╝██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗"
    echo "█████╔╝ █████╗  █████╗  ██████╔╝█████╗  ██████╔╝"
    echo "██╔═██╗ ██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗"
    echo "██║  ██╗███████╗███████╗██║     ███████╗██║  ██║"
    echo "╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝"
    echo -e "${NC}"

    echo -e "${CYAN}🌟 The Ultimate File Organization and Management System 🌟${NC}"
    echo -e "${GREEN}💪 Ready to bring ORDER to your digital chaos! 💪${NC}"

    # Main menu loop
    while true; do
        show_menu
        read -r choice

        case $choice in
            1)
                print_header "LAUNCHING FULL SYSTEM"
                run_file_keeper
                sleep 1
                run_command_portal
                sleep 1
                open_dashboard
                echo -e "${GREEN}🚀 Full system launched! All services running!${NC}"
                ;;
            2)
                run_file_keeper
                ;;
            3)
                run_command_portal
                ;;
            4)
                open_dashboard
                ;;
            5)
                quick_scan
                ;;
            6)
                show_status
                ;;
            7)
                stop_services
                ;;
            8)
                show_help
                ;;
            9)
                cleanup
                ;;
            *)
                echo -e "${RED}❌ Invalid choice. Please enter 1-9.${NC}"
                ;;
        esac

        echo -e "\n${YELLOW}Press Enter to continue...${NC}"
        read -r
    done
}

# Run main function
main "$@"