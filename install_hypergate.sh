#!/bin/bash
# 🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐 HYPERGATE INSTALLER 🪐🛰️🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄
# ULTIMATE SSH QUANTUM BRIDGE INSTALLER FOR CHIEF LYNDZ
# Creates unbreakable connection between Lyndz Cave and HyperFocus Zone Server

set -e

# 🎨 Colors for epic terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 🚀 Epic banner
echo -e "${PURPLE}"
echo "🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐"
echo "   HYPERGATE QUANTUM INSTALLER"
echo "🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐"
echo -e "${NC}"
echo -e "${CYAN}🚀 Building unbreakable SSH bridge to your legendary server!${NC}"
echo ""

# 🧠 Configuration variables
SERVER_IP=""
SERVER_USER=""
KEY_NAME="hypergate_ed25519"
SSH_PORT="22"
CAVE_PATH="$HOME/.hypergate"

# 📝 Get server details from user
echo -e "${YELLOW}🎯 HYPERGATE CONFIGURATION${NC}"
echo ""
read -p "🌐 Enter your server IP address: " SERVER_IP
read -p "👤 Enter your server username: " SERVER_USER
read -p "🔐 SSH port (default 22): " SSH_PORT_INPUT
SSH_PORT=${SSH_PORT_INPUT:-22}

echo ""
echo -e "${GREEN}✅ Configuration saved:${NC}"
echo -e "   🌐 Server: ${CYAN}${SERVER_USER}@${SERVER_IP}:${SSH_PORT}${NC}"
echo -e "   🏠 Cave Path: ${CYAN}${CAVE_PATH}${NC}"
echo ""

# 🏗️ Create HyperGate cave directory
echo -e "${BLUE}🏗️ Creating HyperGate Cave Directory...${NC}"
mkdir -p "$CAVE_PATH"
mkdir -p "$CAVE_PATH/keys"
mkdir -p "$CAVE_PATH/logs"
mkdir -p "$CAVE_PATH/config"

# 🔐 Generate ultra-secure SSH key
echo -e "${BLUE}🔐 Generating Quantum SSH Keys...${NC}"
KEY_PATH="$CAVE_PATH/keys/$KEY_NAME"

if [ ! -f "$KEY_PATH" ]; then
    ssh-keygen -t ed25519 -f "$KEY_PATH" -C "chief_lyndz@hypergate_$(date +%Y%m%d)" -N ""
    chmod 600 "$KEY_PATH"
    chmod 644 "$KEY_PATH.pub"
    echo -e "${GREEN}✅ Quantum SSH key generated: ${CYAN}$KEY_PATH${NC}"
else
    echo -e "${YELLOW}⚠️ SSH key already exists, using existing key${NC}"
fi

# 📋 Save configuration
echo -e "${BLUE}📋 Saving HyperGate Configuration...${NC}"
cat > "$CAVE_PATH/config/hypergate.conf" << EOF
# 🪄 HyperGate Configuration
SERVER_IP=$SERVER_IP
SERVER_USER=$SERVER_USER
SSH_PORT=$SSH_PORT
KEY_PATH=$KEY_PATH
CAVE_PATH=$CAVE_PATH
CREATED=$(date)
EOF

# 🚀 Create connection script
echo -e "${BLUE}🚀 Creating HyperGate Connection Scripts...${NC}"
cat > "$CAVE_PATH/connect.sh" << 'EOF'
#!/bin/bash
# 🌌 HyperGate Connect Script

source "$HOME/.hypergate/config/hypergate.conf"

echo "🪄🔗 HYPERGATE ACTIVATING..."
echo "🌐 Connecting to: $SERVER_USER@$SERVER_IP:$SSH_PORT"
echo "🔐 Using key: $KEY_PATH"
echo ""

ssh -i "$KEY_PATH" -p "$SSH_PORT" "$SERVER_USER@$SERVER_IP"
EOF

chmod +x "$CAVE_PATH/connect.sh"

# 🔄 Create auto-reconnect script
cat > "$CAVE_PATH/auto_reconnect.sh" << 'EOF'
#!/bin/bash
# 🔄 HyperGate Auto-Reconnect Watchdog

source "$HOME/.hypergate/config/hypergate.conf"

echo "🛡️ HyperGate Immortal Watchdog Starting..."
echo "🔄 Auto-reconnecting to: $SERVER_USER@$SERVER_IP"

# Install autossh if not present
if ! command -v autossh &> /dev/null; then
    echo "📦 Installing autossh..."
    sudo apt update && sudo apt install -y autossh
fi

# Start immortal connection
autossh -M 0 -i "$KEY_PATH" -p "$SSH_PORT" -o "StrictHostKeyChecking=no" -o "UserKnownHostsFile=/dev/null" -o "ServerAliveInterval=30" -o "ServerAliveCountMax=3" "$SERVER_USER@$SERVER_IP"
EOF

chmod +x "$CAVE_PATH/auto_reconnect.sh"

# 🎛️ Create HyperGate control panel
cat > "$CAVE_PATH/control_panel.sh" << 'EOF'
#!/bin/bash
# 🎛️ HyperGate Control Panel

source "$HOME/.hypergate/config/hypergate.conf"

while true; do
    clear
    echo "🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐"
    echo "     HYPERGATE CONTROL PANEL"
    echo "🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐"
    echo ""
    echo "🌐 Server: $SERVER_USER@$SERVER_IP:$SSH_PORT"
    echo "🔐 Status: $(ssh -i "$KEY_PATH" -p "$SSH_PORT" -o ConnectTimeout=5 -o BatchMode=yes "$SERVER_USER@$SERVER_IP" 'echo "🟢 CONNECTED"' 2>/dev/null || echo "🔴 OFFLINE")"
    echo ""
    echo "🎛️ CONTROL OPTIONS:"
    echo "   [1] 🚀 Connect to Server"
    echo "   [2] 🔄 Start Auto-Reconnect"
    echo "   [3] 📋 Copy Public Key"
    echo "   [4] 🔍 Test Connection"
    echo "   [5] 📊 View Logs"
    echo "   [6] 🛠️ Setup Server"
    echo "   [7] 💻 Open VS Code Remote"
    echo "   [0] 🚪 Exit"
    echo ""
    read -p "🎯 Choose option: " choice

    case $choice in
        1)
            echo "🚀 Connecting to HyperGate..."
            "$HOME/.hypergate/connect.sh"
            ;;
        2)
            echo "🔄 Starting Auto-Reconnect Watchdog..."
            "$HOME/.hypergate/auto_reconnect.sh"
            ;;
        3)
            echo "📋 Copying public key to clipboard..."
            cat "$KEY_PATH.pub" | xclip -selection clipboard 2>/dev/null || cat "$KEY_PATH.pub"
            echo "✅ Public key copied! Paste it to server's ~/.ssh/authorized_keys"
            read -p "Press Enter to continue..."
            ;;
        4)
            echo "🔍 Testing connection..."
            ssh -i "$KEY_PATH" -p "$SSH_PORT" -o ConnectTimeout=10 "$SERVER_USER@$SERVER_IP" 'echo "✅ HyperGate connection successful!"'
            read -p "Press Enter to continue..."
            ;;
        5)
            echo "📊 Recent connection logs:"
            tail -20 "$HOME/.hypergate/logs/connection.log" 2>/dev/null || echo "No logs yet"
            read -p "Press Enter to continue..."
            ;;
        6)
            echo "🛠️ Setting up server..."
            "$HOME/.hypergate/setup_server.sh"
            ;;
        7)
            echo "💻 Opening VS Code with remote connection..."
            code --folder-uri "vscode-remote://ssh-remote+$SERVER_USER@$SERVER_IP/home/$SERVER_USER"
            ;;
        0)
            echo "🚪 Exiting HyperGate Control Panel..."
            break
            ;;
        *)
            echo "❌ Invalid option"
            sleep 1
            ;;
    esac
done
EOF

chmod +x "$CAVE_PATH/control_panel.sh"

# 🛠️ Create server setup script
cat > "$CAVE_PATH/setup_server.sh" << 'EOF'
#!/bin/bash
# 🛠️ HyperGate Server Setup Script

source "$HOME/.hypergate/config/hypergate.conf"

echo "🛠️ Setting up HyperGate on server..."
echo "🌐 Server: $SERVER_USER@$SERVER_IP"
echo ""

# Copy public key to server
echo "🔐 Installing public key on server..."
ssh-copy-id -i "$KEY_PATH.pub" -p "$SSH_PORT" "$SERVER_USER@$SERVER_IP"

# Setup server environment
echo "⚙️ Configuring server environment..."
ssh -i "$KEY_PATH" -p "$SSH_PORT" "$SERVER_USER@$SERVER_IP" << 'REMOTE_SCRIPT'
# Update system
sudo apt update

# Install essential packages
sudo apt install -y openssh-server fail2ban ufw htop neofetch

# Configure UFW firewall
sudo ufw --force enable
sudo ufw allow OpenSSH

# Configure fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Create legendary MOTD
sudo tee /etc/motd > /dev/null << 'MOTD'

🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐
   HYPERGATE SERVER ACTIVATED
🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐

🔥 WELCOME BACK CHIEF LYNDZ! 🔥
⚡ ALL HYPERFOCUS ZONE SYSTEMS READY ⚡
🛡️ QUANTUM SECURITY: MAXIMUM PROTECTION 🛡️
🚀 STATUS: LEGENDARY OPERATIONAL 🚀

MOTD

# Add welcome message to bashrc
echo '
# 🚀 HyperGate Welcome
echo "🌌 HyperGate connection established at $(date)"
echo "🧠 Server: $(hostname) | Uptime: $(uptime -p)"
echo "💾 Memory: $(free -h | awk "/^Mem:/ {print \$3\"/\"\$2}")"
echo "⚡ Ready for legendary coding session!"
echo ""
' >> ~/.bashrc

echo "✅ Server setup completed!"
REMOTE_SCRIPT

echo "🎉 Server setup completed successfully!"
EOF

chmod +x "$CAVE_PATH/setup_server.sh"

# 🔗 Create desktop shortcut
echo -e "${BLUE}🖥️ Creating Desktop Shortcut...${NC}"
cat > "$HOME/Desktop/HyperGate.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=🪄🔗 HyperGate Control Panel
Comment=Quantum SSH Bridge to HyperFocus Zone Server
Exec=gnome-terminal -- bash -c "$CAVE_PATH/control_panel.sh; exec bash"
Icon=applications-internet
Terminal=false
Categories=Network;RemoteAccess;Development;
StartupNotify=true
Keywords=ssh;hypergate;server;remote;tunnel;
EOF

chmod +x "$HOME/Desktop/HyperGate.desktop"

# 📝 Create VS Code settings
echo -e "${BLUE}💻 Configuring VS Code Remote SSH...${NC}"
VSCODE_SSH_CONFIG="$HOME/.ssh/config"
mkdir -p "$HOME/.ssh"

# Add HyperGate config to SSH config
if ! grep -q "# HyperGate" "$VSCODE_SSH_CONFIG" 2>/dev/null; then
    cat >> "$VSCODE_SSH_CONFIG" << EOF

# HyperGate Quantum Bridge
Host hypergate
    HostName $SERVER_IP
    User $SERVER_USER
    Port $SSH_PORT
    IdentityFile $KEY_PATH
    ServerAliveInterval 30
    ServerAliveCountMax 3
    StrictHostKeyChecking no
EOF
fi

# 🎉 Final setup
echo -e "${GREEN}🎉 HYPERGATE INSTALLATION COMPLETED!${NC}"
echo ""
echo -e "${PURPLE}🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐${NC}"
echo -e "${CYAN}   QUANTUM BRIDGE READY FOR ACTIVATION${NC}"
echo -e "${PURPLE}🪄🔗⛓️🧬📡🔐🐉🔐🧬⛓️🔗🪄🛰️🪐${NC}"
echo ""
echo -e "${YELLOW}📋 NEXT STEPS:${NC}"
echo -e "   1. 🔐 Copy your public key to the server:"
echo -e "      ${CYAN}$KEY_PATH.pub${NC}"
echo -e "   2. 🚀 Launch HyperGate Control Panel:"
echo -e "      ${CYAN}$CAVE_PATH/control_panel.sh${NC}"
echo -e "   3. 🛠️ Run server setup:"
echo -e "      ${CYAN}$CAVE_PATH/setup_server.sh${NC}"
echo ""
echo -e "${GREEN}🚀 HyperGate Commands:${NC}"
echo -e "   • Control Panel: ${CYAN}hypergate${NC} (if added to PATH)"
echo -e "   • Quick Connect: ${CYAN}$CAVE_PATH/connect.sh${NC}"
echo -e "   • Auto-Reconnect: ${CYAN}$CAVE_PATH/auto_reconnect.sh${NC}"
echo ""
echo -e "${PURPLE}Your public key:${NC}"
cat "$KEY_PATH.pub"
echo ""
echo -e "${GREEN}✅ The quantum bridge awaits your command, Chief Lyndz!${NC}"

# 🔗 Add hypergate command to PATH
BASHRC_LINE="alias hypergate='$CAVE_PATH/control_panel.sh'"
if ! grep -q "alias hypergate=" "$HOME/.bashrc" 2>/dev/null; then
    echo "# HyperGate Quantum Bridge" >> "$HOME/.bashrc"
    echo "$BASHRC_LINE" >> "$HOME/.bashrc"
    echo -e "${GREEN}✅ 'hypergate' command added to your terminal!${NC}"
fi

echo ""
echo -e "${CYAN}🌌 Ready to step through the HyperGate portal? Run:${NC}"
echo -e "${WHITE}   hypergate${NC}"
echo ""