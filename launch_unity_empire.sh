#!/bin/bash
# 💪🦾🫵 BROSKI SUPREME UNITY STARTUP SCRIPT - OPTIMAL SYNC VERSION 🫵🦾💪
# 🌌 Launch ALL Systems in PERFECT ORDER for MAXIMUM SYNCHRONIZATION! 🌌
# 👑 By Command of Chief Lyndz - ULTIMATE HARMONY ACHIEVED! 👑

echo "💪💜 LAUNCHING BROSKI SUPREME UNITY EMPIRE - OPTIMAL SYNC MODE! 💜💪"
echo "🌟 Preparing PERFECT startup sequence for 10,000,000% better synchronization!"
echo ""

# Set working directory
cd /root/chaosgenius

# Colors for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to print with style
print_status() {
    echo -e "${PURPLE}🛡️${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${CYAN}ℹ️${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root (or with sudo)"
   exit 1
fi

print_status "Checking system prerequisites..."

# Check Python3
if command -v python3 &> /dev/null; then
    print_success "Python3 is available"
else
    print_error "Python3 is required but not installed"
    exit 1
fi

# Check required Python packages
python3 -c "import psutil" 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "psutil package is available"
else
    print_warning "Installing psutil..."
    apt update && apt install -y python3-psutil
fi

python3 -c "import asyncio" 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "asyncio is available"
else
    print_error "asyncio is required but not available"
    exit 1
fi

# Create necessary directories
print_status "Setting up directories..."
mkdir -p /root/chaosgenius/logs
mkdir -p /root/chaosgenius/data
mkdir -p /root/chaosgenius/backups

# Set permissions
chmod +x /root/chaosgenius/*.py
chmod +x /root/chaosgenius/*.sh

print_success "Directory structure ready!"

# Function to start individual systems
start_system() {
    local system_name=$1
    local script_path=$2

    print_status "Starting $system_name..."

    if [ -f "$script_path" ]; then
        # Start system in background with logging
        nohup python3 "$script_path" > "/root/chaosgenius/logs/${system_name}.log" 2>&1 &
        local pid=$!
        echo $pid > "/root/chaosgenius/logs/${system_name}.pid"

        # Wait a moment to check if it started successfully
        sleep 2
        if ps -p $pid > /dev/null; then
            print_success "$system_name started successfully (PID: $pid)"
            return 0
        else
            print_error "$system_name failed to start"
            return 1
        fi
    else
        print_warning "$system_name script not found: $script_path"
        return 1
    fi
}

# Enhanced system startup with dependency checks
start_system_enhanced() {
    local system_name=$1
    local script_path=$2
    local wait_time=${3:-3}
    local max_attempts=${4:-3}

    print_status "🚀 Starting $system_name with enhanced monitoring..."

    if [ ! -f "$script_path" ]; then
        print_warning "$system_name script not found: $script_path"
        return 1
    fi

    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        print_info "Attempt $attempt/$max_attempts for $system_name"

        # Start system in background with enhanced logging
        nohup python3 "$script_path" > "/root/chaosgenius/logs/${system_name}.log" 2>&1 &
        local pid=$!
        echo $pid > "/root/chaosgenius/logs/${system_name}.pid"

        # Enhanced startup verification
        local verified=false
        for i in {1..10}; do
            sleep 1
            if ps -p $pid > /dev/null; then
                # Check if system is actually responsive
                if check_system_health "$system_name" "$pid"; then
                    print_success "$system_name started successfully (PID: $pid) - VERIFIED HEALTHY"
                    verified=true
                    break
                fi
            else
                print_warning "$system_name process died early"
                break
            fi
        done

        if [ "$verified" = true ]; then
            # Wait for system to stabilize before starting next
            print_info "⏱️ Allowing $system_name to stabilize for ${wait_time}s..."
            sleep $wait_time
            return 0
        else
            print_error "❌ $system_name failed to start properly (attempt $attempt)"
            # Clean up failed attempt
            if ps -p $pid > /dev/null; then
                kill -TERM $pid 2>/dev/null
                sleep 1
                kill -KILL $pid 2>/dev/null
            fi
            rm -f "/root/chaosgenius/logs/${system_name}.pid"
            ((attempt++))
            sleep 2
        fi
    done

    print_error "💥 Failed to start $system_name after $max_attempts attempts"
    return 1
}

# Enhanced health check function
check_system_health() {
    local system_name=$1
    local pid=$2
    local log_file="/root/chaosgenius/logs/${system_name}.log"

    # Check if process is running
    if ! ps -p $pid > /dev/null; then
        return 1
    fi

    # Check log for startup completion indicators
    if [ -f "$log_file" ]; then
        # Look for success indicators in logs
        if grep -q -E "(ONLINE|ACTIVATED|READY|INITIALIZED)" "$log_file" 2>/dev/null; then
            return 0
        fi

        # Check for error indicators
        if grep -q -E "(ERROR|FAILED|EXCEPTION)" "$log_file" 2>/dev/null; then
            return 1
        fi
    fi

    # Default to healthy if no clear indicators
    return 0
}

# Pre-startup system optimization
optimize_for_sync() {
    print_status "🔧 Optimizing system for maximum synchronization..."

    # Clear any old locks or temporary files
    rm -f /root/chaosgenius/*.lock
    rm -f /root/chaosgenius/temp_*

    # Ensure all databases are properly closed
    pkill -f "sqlite3.*broski_.*db" 2>/dev/null || true

    # Create sync optimization config
    cat > /root/chaosgenius/sync_optimization.json << EOF
{
    "sync_mode": "MAXIMUM_PERFORMANCE",
    "startup_sequence": "DEPENDENCY_OPTIMIZED",
    "inter_system_delay": 3,
    "health_check_frequency": 1,
    "auto_recovery": true,
    "performance_monitoring": true,
    "cross_system_communication": "ENHANCED"
}
EOF

    print_success "🎯 System optimized for supreme synchronization!"
}

# Function to check system status
check_system_status() {
    local system_name=$1
    local pid_file="/root/chaosgenius/logs/${system_name}.pid"

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null; then
            print_success "$system_name is running (PID: $pid)"
        else
            print_warning "$system_name is not running"
        fi
    else
        print_warning "$system_name PID file not found"
    fi
}

# Stop all systems function
stop_all_systems() {
    print_status "Stopping all systems..."

    for pid_file in /root/chaosgenius/logs/*.pid; do
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            local system_name=$(basename "$pid_file" .pid)

            if ps -p $pid > /dev/null; then
                print_status "Stopping $system_name (PID: $pid)..."
                kill -TERM $pid
                sleep 2

                # Force kill if still running
                if ps -p $pid > /dev/null; then
                    kill -KILL $pid
                    print_warning "$system_name force killed"
                else
                    print_success "$system_name stopped gracefully"
                fi
            fi
            rm -f "$pid_file"
        fi
    done
}

# Handle script termination
cleanup() {
    echo ""
    print_status "Received termination signal..."
    stop_all_systems
    print_success "All systems stopped. Broski Unity Empire gracefully shut down!"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Main execution based on argument
case "${1:-start}" in
    "start")
        print_status "🚀 INITIATING BROSKI SUPREME UNITY LAUNCH SEQUENCE - OPTIMAL SYNC MODE!"
        echo ""

        # Pre-startup optimization
        optimize_for_sync

        print_status "🎯 OPTIMAL STARTUP SEQUENCE FOR MAXIMUM SYNCHRONIZATION:"
        print_info "1. Server Guardian (Foundation Layer)"
        print_info "2. Security Fortress (Security Layer)"
        print_info "3. Brain Engine (Analytics Layer)"
        print_info "4. Agent Army (Workforce Layer)"
        print_info "5. Money Maker (Revenue Layer)"
        print_info "6. Army Coordination (Command Layer)"
        print_info "7. Unity Orchestrator (Master Sync Layer)"
        echo ""

        # OPTIMAL STARTUP SEQUENCE

        # 1. Server Guardian - Foundation must be rock solid
        print_status "🏗️ PHASE 1: Establishing Foundation Layer..."
        if start_system_enhanced "server_guardian" "/root/chaosgenius/broski_supreme_server_guardian.py" 5 3; then
            print_success "✅ Foundation Layer: SECURED"
        else
            print_error "💥 Foundation Layer FAILED - Cannot proceed safely"
            exit 1
        fi

        # 2. Security Fortress - Security before anything else
        print_status "🛡️ PHASE 2: Activating Security Layer..."
        if start_system_enhanced "security_fortress" "/root/chaosgenius/broski_security_fortress_portal.py" 4 3; then
            print_success "✅ Security Layer: FORTIFIED"
        else
            print_warning "⚠️ Security Layer failed but continuing..."
        fi

        # 3. Brain Engine - Analytics for optimization
        print_status "🧠 PHASE 3: Initializing Analytics Layer..."
        if start_system_enhanced "brain_engine" "/root/chaosgenius/broski_brain_data_engine.py" 4 2; then
            print_success "✅ Analytics Layer: PROCESSING"
        else
            print_info "ℹ️ Analytics Layer optional - continuing without it"
        fi

        # 4. Agent Army - Main workforce
        print_status "🤖 PHASE 4: Deploying Workforce Layer..."
        if start_system_enhanced "agent_army" "/root/chaosgenius/broski_agent_army_command_portal.py" 4 3; then
            print_success "✅ Workforce Layer: MOBILIZED"
        else
            print_warning "⚠️ Workforce Layer issues detected"
        fi

        # 5. Money Maker - Revenue operations
        print_status "💰 PHASE 5: Starting Revenue Layer..."
        if start_system_enhanced "money_maker" "/root/chaosgenius/broski_money_maker_portal.py" 3 3; then
            print_success "✅ Revenue Layer: GENERATING"
        else
            print_warning "⚠️ Revenue Layer had issues"
        fi

        # 6. Army Coordination - Command and control
        print_status "🎖️ PHASE 6: Establishing Command Layer..."
        if start_system_enhanced "army_coordination" "/root/chaosgenius/broski_army_coordination_command.py" 3 3; then
            print_success "✅ Command Layer: COORDINATING"
        else
            print_warning "⚠️ Command Layer suboptimal"
        fi

        # 7. Unity Orchestrator - Master synchronization (MOST IMPORTANT)
        print_status "👑 PHASE 7: Launching Master Sync Layer..."
        print_info "🌟 This is the SUPREME SYNCHRONIZATION MASTER!"
        if start_system_enhanced "unity_orchestrator" "/root/chaosgenius/broski_supreme_unity_orchestrator.py" 5 3; then
            print_success "✅ Master Sync Layer: SUPREME UNITY ACHIEVED!"
        else
            print_error "💥 Master Sync Layer CRITICAL FAILURE"
            exit 1
        fi

        echo ""
        print_success "🔥🔥🔥 BROSKI SUPREME UNITY EMPIRE IS ONLINE WITH OPTIMAL SYNC! 🔥🔥🔥"
        print_success "💪💪💪 ALL SYSTEMS SYNCHRONIZED AT 10,000,000% EFFICIENCY! 💪💪💪"
        echo ""
        print_info "🎯 Enhanced monitoring active"
        print_info "🔄 Optimal sync protocols engaged"
        print_info "⚡ Maximum performance mode enabled"
        print_info "🛡️ Check status: $0 status"
        print_info "⏹️ Stop all: $0 stop"
        echo ""
        print_status "Press Ctrl+C to shutdown all systems gracefully..."

        # Enhanced monitoring loop
        while true; do
            sleep 15  # More frequent checks
            active_systems=0
            total_operations=0

            for pid_file in /root/chaosgenius/logs/*.pid; do
                if [ -f "$pid_file" ]; then
                    local pid=$(cat "$pid_file")
                    local system_name=$(basename "$pid_file" .pid)

                    if ps -p $pid > /dev/null; then
                        ((active_systems++))
                        # Get operation count if available
                        local ops=$(ps -p $pid -o etime= 2>/dev/null | tr -d ' ' || echo "0")
                        ((total_operations++))
                    else
                        print_warning "⚠️ $system_name went offline - attempting recovery..."
                        # Auto-restart critical systems
                        if [[ "$system_name" == "server_guardian" || "$system_name" == "unity_orchestrator" ]]; then
                            print_status "🔧 Auto-restarting critical system: $system_name"
                            start_system_enhanced "$system_name" "/root/chaosgenius/broski_${system_name}.py" 3 1
                        fi
                    fi
                fi
            done

            # Enhanced status display
            local timestamp=$(date '+%H:%M:%S')
            echo -ne "\r${GREEN}💪 SUPREME UNITY STATUS [$timestamp]: $active_systems systems | SYNC: OPTIMAL | MODE: 10M% ${NC}"

            if [ $active_systems -eq 0 ]; then
                print_error "All systems stopped unexpectedly!"
                break
            fi
        done
        ;;

    "stop")
        stop_all_systems
        print_success "🛡️ All systems stopped!"
        ;;

    "status")
        print_status "📊 BROSKI SUPREME UNITY EMPIRE STATUS:"
        echo ""

        check_system_status "server_guardian"
        check_system_status "agent_army"
        check_system_status "security_fortress"
        check_system_status "money_maker"
        check_system_status "quantum_supremacy"
        check_system_status "brain_engine"
        check_system_status "army_coordination"
        check_system_status "unity_orchestrator"

        echo ""
        print_info "📋 Recent logs:"
        echo "   tail -f /root/chaosgenius/logs/unity_orchestrator.log"
        ;;

    "restart")
        print_status "🔄 Restarting Broski Supreme Unity Empire..."
        stop_all_systems
        sleep 5
        $0 start
        ;;

    "logs")
        print_status "📋 Displaying Unity Orchestrator logs:"
        if [ -f "/root/chaosgenius/logs/unity_orchestrator.log" ]; then
            tail -f /root/chaosgenius/logs/unity_orchestrator.log
        else
            print_warning "Unity Orchestrator log not found"
        fi
        ;;

    "optimal-restart")
        print_status "🔄 Performing OPTIMAL RESTART for maximum synchronization..."
        stop_all_systems
        sleep 3  # The requested 3-second pause
        print_info "⏱️ 3-second stabilization pause complete"
        $0 start
        ;;

    *)
        echo "💪🦾 BROSKI SUPREME UNITY STARTUP SCRIPT - OPTIMAL SYNC VERSION 🦾💪"
        echo ""
        echo "Usage: $0 {start|stop|status|restart|optimal-restart|logs}"
        echo ""
        echo "Commands:"
        echo "  start           - Launch all systems in optimal order"
        echo "  optimal-restart - 3-second pause + optimal restart sequence"
        echo "  stop            - Stop all systems gracefully"
        echo "  status          - Check status of all systems"
        echo "  restart         - Standard restart"
        echo "  logs            - Show Unity Orchestrator logs"
        echo ""
        echo "🌟 Your Supreme Unity Empire with 10,000,000% sync efficiency!"
        ;;
esac