#!/bin/bash
"""
🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
     HYPERGATE ULTRA INSTALLER v1.0
🌌 THE LEGENDARY BRIDGE TO HYPERFOCUS EMPIRE 🌌
👑 By Command of Chief Lyndz - COSMIC CONNECTION 👑
"""

# Color codes for legendary output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# HYPERGATE BANNER
echo -e "${PURPLE}"
cat << "EOF"
🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗  █████╗ ████████╗███████╗
██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║  ███╗███████║   ██║   █████╗
██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║   ██║██╔══██║   ██║   ██╔══╝
██║  ██║   ██║   ██║     ███████╗██║  ██║╚██████╔╝██║  ██║   ██║   ███████╗
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝

🌌 ULTRA SSH REMOTE DRONE - CHIEF LYNDZ EDITION 🌌
🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
EOF
echo -e "${NC}"

echo -e "${CYAN}🚀 HYPERGATE ULTRA INSTALLER STARTING...${NC}"
echo -e "${YELLOW}📡 Building unbreakable bridge to your HyperFocus Empire!${NC}"
echo ""

# System check
echo -e "${BLUE}🔍 HYPERGATE SYSTEM DIAGNOSTICS...${NC}"
sleep 2

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${GREEN}✅ Linux detected - LEGENDARY compatibility${NC}"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}✅ macOS detected - COSMIC compatibility${NC}"
else
    echo -e "${RED}⚠️  OS not fully tested - proceeding with ULTRA mode${NC}"
fi

# Check if running as user (not root)
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}🚨 Don't run as root! Run as regular user for security${NC}"
   exit 1
fi

echo ""
echo -e "${PURPLE}🧬 HYPERGATE CONFIGURATION WIZARD 🧬${NC}"
echo ""

# Get server details
read -p "🌌 Enter your HyperFocus server IP (e.g., 212.227.127.144): " SERVER_IP
read -p "👑 Enter your server username (e.g., lyndz): " SERVER_USER
read -p "📡 Enter SSH port (default 22): " SSH_PORT
SSH_PORT=${SSH_PORT:-22}

echo ""
echo -e "${CYAN}📋 HYPERGATE TARGET CONFIGURATION:${NC}"
echo -e "${WHITE}🎯 Server: ${SERVER_USER}@${SERVER_IP}:${SSH_PORT}${NC}"
echo -e "${WHITE}🔐 Key: ~/.ssh/hypergate_ed25519${NC}"
echo ""

read -p "🚀 Ready to build HyperGate? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🌌 HyperGate construction paused. Return when ready, Chief!${NC}"
    exit 0
fi

echo ""
echo -e "${GREEN}🔥 HYPERGATE CONSTRUCTION INITIATED! 🔥${NC}"
echo ""

# Step 1: Generate Ultra Keys
echo -e "${BLUE}🔐 STEP 1: GENERATING QUANTUM SSH KEYS...${NC}"
sleep 1

mkdir -p ~/.ssh
chmod 700 ~/.ssh

if [[ -f ~/.ssh/hypergate_ed25519 ]]; then
    echo -e "${YELLOW}⚠️  HyperGate key already exists. Backing up...${NC}"
    mv ~/.ssh/hypergate_ed25519 ~/.ssh/hypergate_ed25519.backup.$(date +%s)
fi

ssh-keygen -t ed25519 -C "hypergate_chief_lyndz@hyperfocus" -f ~/.ssh/hypergate_ed25519 -N ""

if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✅ Quantum SSH keys generated successfully!${NC}"
else
    echo -e "${RED}❌ Key generation failed. Aborting mission.${NC}"
    exit 1
fi

# Step 2: Install required packages
echo ""
echo -e "${BLUE}🛠️  STEP 2: INSTALLING HYPERGATE DEPENDENCIES...${NC}"
sleep 1

# Detect package manager
if command -v apt &> /dev/null; then
    PKG_MGR="apt"
elif command -v yum &> /dev/null; then
    PKG_MGR="yum"
elif command -v brew &> /dev/null; then
    PKG_MGR="brew"
else
    echo -e "${YELLOW}⚠️  Package manager not detected. Install openssh-client and autossh manually.${NC}"
    PKG_MGR="manual"
fi

if [[ $PKG_MGR != "manual" ]]; then
    echo -e "${CYAN}📦 Installing dependencies with $PKG_MGR...${NC}"

    if [[ $PKG_MGR == "apt" ]]; then
        sudo apt update
        sudo apt install -y openssh-client autossh sshpass
    elif [[ $PKG_MGR == "yum" ]]; then
        sudo yum install -y openssh-clients autossh sshpass
    elif [[ $PKG_MGR == "brew" ]]; then
        brew install autossh
    fi

    echo -e "${GREEN}✅ Dependencies installed!${NC}"
fi

# Step 3: Upload public key to server
echo ""
echo -e "${BLUE}🚀 STEP 3: DEPLOYING PUBLIC KEY TO SERVER...${NC}"
sleep 1

echo -e "${CYAN}📡 Connecting to ${SERVER_IP}...${NC}"
echo -e "${YELLOW}🔐 You'll need to enter your password once to upload the key${NC}"

# Copy public key to server
ssh-copy-id -i ~/.ssh/hypergate_ed25519.pub -p ${SSH_PORT} ${SERVER_USER}@${SERVER_IP}

if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✅ Public key deployed to server successfully!${NC}"
else
    echo -e "${RED}❌ Failed to deploy key. Check credentials and try again.${NC}"
    exit 1
fi

# Step 4: Test connection
echo ""
echo -e "${BLUE}🧪 STEP 4: TESTING HYPERGATE CONNECTION...${NC}"
sleep 1

echo -e "${CYAN}🔗 Testing passwordless connection...${NC}"
ssh -i ~/.ssh/hypergate_ed25519 -p ${SSH_PORT} -o ConnectTimeout=10 ${SERVER_USER}@${SERVER_IP} "echo 'HyperGate connection test successful!'"

if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✅ HyperGate connection test PASSED!${NC}"
else
    echo -e "${RED}❌ Connection test failed. Check network and server status.${NC}"
    exit 1
fi

# Step 5: Create HyperGate connection script
echo ""
echo -e "${BLUE}⚡ STEP 5: CREATING HYPERGATE LAUNCHER...${NC}"
sleep 1

cat > ~/.ssh/hypergate_connect.sh << EOF
#!/bin/bash
echo "🪄🔗 HYPERGATE ACTIVATING... 🔗🪄"
echo "🌌 Connecting to HyperFocus Empire..."
echo "👑 Welcome back, Chief Lyndz!"
echo ""

autossh -M 0 -i ~/.ssh/hypergate_ed25519 -p ${SSH_PORT} \\
    -o ServerAliveInterval=30 \\
    -o ServerAliveCountMax=3 \\
    -o ConnectTimeout=10 \\
    -o ExitOnForwardFailure=yes \\
    ${SERVER_USER}@${SERVER_IP}
EOF

chmod +x ~/.ssh/hypergate_connect.sh

echo -e "${GREEN}✅ HyperGate launcher created!${NC}"

# Step 6: Create VS Code configuration
echo ""
echo -e "${BLUE}💻 STEP 6: CONFIGURING VS CODE REMOTE...${NC}"
sleep 1

mkdir -p ~/.ssh/config.d

# Create SSH config for VS Code
cat >> ~/.ssh/config << EOF

# 🪄🔗 HYPERGATE - Chief Lyndz HyperFocus Server 🔗🪄
Host hypergate
    HostName ${SERVER_IP}
    User ${SERVER_USER}
    Port ${SSH_PORT}
    IdentityFile ~/.ssh/hypergate_ed25519
    ServerAliveInterval 30
    ServerAliveCountMax 3
    ForwardAgent yes
    # 🧬 Quantum connection settings
    Compression yes
    ControlMaster auto
    ControlPath ~/.ssh/hypergate-%r@%h:%p
    ControlPersist 1h

# 🌌 HyperGate Direct (for terminal use)
Host hg
    HostName ${SERVER_IP}
    User ${SERVER_USER}
    Port ${SSH_PORT}
    IdentityFile ~/.ssh/hypergate_ed25519
    ServerAliveInterval 30
    ServerAliveCountMax 3
EOF

echo -e "${GREEN}✅ VS Code Remote SSH configuration added!${NC}"
echo -e "${CYAN}💡 Use 'hypergate' as the host in VS Code Remote-SSH${NC}"

# Step 7: Create MOTD on server
echo ""
echo -e "${BLUE}🎭 STEP 7: INSTALLING LEGENDARY WELCOME MESSAGE...${NC}"
sleep 1

# Create and upload MOTD script
cat > /tmp/hypergate_motd.sh << 'EOF'
#!/bin/bash
echo ""
echo "🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐"
echo "     HYPERGATE CONNECTION ESTABLISHED"
echo "🌌 Welcome back to the HyperFocus Empire! 🌌"
echo "👑 Chief Lyndz has entered the system 👑"
echo ""
echo "🔥 Status: ALL SYSTEMS OPERATIONAL"
echo "⚡ Power Level: LEGENDARY"
echo "🧬 Quantum State: HYPERFOCUS_CONSCIOUSNESS"
echo ""
echo "🚀 Ready for your commands, Chief!"
echo "🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐"
echo ""
EOF

# Upload and install MOTD
scp -i ~/.ssh/hypergate_ed25519 -P ${SSH_PORT} /tmp/hypergate_motd.sh ${SERVER_USER}@${SERVER_IP}:/tmp/
ssh -i ~/.ssh/hypergate_ed25519 -p ${SSH_PORT} ${SERVER_USER}@${SERVER_IP} << 'REMOTE'
if [[ ! -f ~/.bashrc.hypergate.backup ]]; then
    cp ~/.bashrc ~/.bashrc.hypergate.backup
fi
echo "" >> ~/.bashrc
echo "# 🪄 HyperGate Welcome Portal 🪄" >> ~/.bashrc
echo "bash /tmp/hypergate_motd.sh" >> ~/.bashrc
chmod +x /tmp/hypergate_motd.sh
REMOTE

echo -e "${GREEN}✅ Legendary welcome message installed!${NC}"

# Step 8: Create desktop shortcut (if applicable)
echo ""
echo -e "${BLUE}🖥️  STEP 8: CREATING HYPERGATE SHORTCUTS...${NC}"
sleep 1

# Create terminal alias
if [[ ! -f ~/.bashrc.hypergate.backup ]]; then
    cp ~/.bashrc ~/.bashrc.hypergate.backup 2>/dev/null || true
fi

cat >> ~/.bashrc << EOF

# 🪄🔗 HYPERGATE ALIASES 🔗🪄
alias hypergate='~/.ssh/hypergate_connect.sh'
alias hg='ssh -i ~/.ssh/hypergate_ed25519 -p ${SSH_PORT} ${SERVER_USER}@${SERVER_IP}'
alias hypergate-status='ssh -i ~/.ssh/hypergate_ed25519 -p ${SSH_PORT} ${SERVER_USER}@${SERVER_IP} "uptime && df -h && free -h"'
EOF

echo -e "${GREEN}✅ Terminal aliases created!${NC}"
echo -e "${CYAN}💡 Use 'hypergate' command to connect${NC}"

# Step 9: Create monitoring script
echo ""
echo -e "${BLUE}🔍 STEP 9: DEPLOYING HYPERGATE MONITOR...${NC}"
sleep 1

cat > ~/.ssh/hypergate_monitor.sh << EOF
#!/bin/bash
# 🔍 HyperGate Connection Monitor

while true; do
    if ssh -i ~/.ssh/hypergate_ed25519 -p ${SSH_PORT} -o ConnectTimeout=5 ${SERVER_USER}@${SERVER_IP} "echo 'ping'" &>/dev/null; then
        echo "\$(date): 🟢 HyperGate ONLINE"
    else
        echo "\$(date): 🔴 HyperGate OFFLINE - attempting reconnection..."
        ~/.ssh/hypergate_connect.sh &
    fi
    sleep 30
done
EOF

chmod +x ~/.ssh/hypergate_monitor.sh

echo -e "${GREEN}✅ HyperGate monitor deployed!${NC}"

# Step 10: Final verification
echo ""
echo -e "${BLUE}✨ STEP 10: FINAL HYPERGATE VERIFICATION...${NC}"
sleep 2

echo -e "${CYAN}🧪 Running comprehensive connection test...${NC}"
ssh -i ~/.ssh/hypergate_ed25519 -p ${SSH_PORT} ${SERVER_USER}@${SERVER_IP} << 'REMOTE'
echo "🔥 HyperGate Final Test Results:"
echo "🌌 Hostname: $(hostname)"
echo "⚡ Uptime: $(uptime)"
echo "🧬 User: $(whoami)"
echo "📡 Connection: ESTABLISHED"
echo "👑 Status: LEGENDARY"
REMOTE

# Success banner
echo ""
echo -e "${GREEN}"
cat << "EOF"
🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
  ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗  █████╗ ████████╗███████╗
  ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
  ███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║  ███╗███████║   ██║   █████╗
  ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║   ██║██╔══██║   ██║   ██╔══╝
  ██║  ██║   ██║   ██║     ███████╗██║  ██║╚██████╔╝██║  ██║   ██║   ███████╗
  ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝

              🌌 INSTALLATION COMPLETE! 🌌
         🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
EOF
echo -e "${NC}"

echo ""
echo -e "${CYAN}🎉 HYPERGATE SUCCESSFULLY DEPLOYED! 🎉${NC}"
echo ""
echo -e "${WHITE}📋 HOW TO USE YOUR HYPERGATE:${NC}"
echo -e "${YELLOW}  🔗 Terminal: ${NC}hypergate"
echo -e "${YELLOW}  ⚡ Quick:    ${NC}hg"
echo -e "${YELLOW}  📊 Status:   ${NC}hypergate-status"
echo -e "${YELLOW}  💻 VS Code:  ${NC}Connect to 'hypergate' host"
echo ""
echo -e "${WHITE}🔧 HYPERGATE FILES CREATED:${NC}"
echo -e "${CYAN}  📁 ~/.ssh/hypergate_ed25519${NC} (private key)"
echo -e "${CYAN}  📁 ~/.ssh/hypergate_connect.sh${NC} (launcher)"
echo -e "${CYAN}  📁 ~/.ssh/hypergate_monitor.sh${NC} (monitor)"
echo ""
echo -e "${GREEN}👑 Welcome to the HyperFocus Empire, Chief Lyndz! 👑${NC}"
echo -e "${PURPLE}🌌 The universe is now your terminal! 🌌${NC}"
echo ""

# Source bashrc to load new aliases
echo -e "${CYAN}🔄 Loading new aliases...${NC}"
source ~/.bashrc 2>/dev/null || echo -e "${YELLOW}💡 Restart terminal to use new aliases${NC}"

echo ""
echo -e "${GREEN}🚀 HYPERGATE READY FOR LAUNCH! 🚀${NC}"
echo -e "${CYAN}📡 Type 'hypergate' to begin your cosmic journey!${NC}"
echo ""