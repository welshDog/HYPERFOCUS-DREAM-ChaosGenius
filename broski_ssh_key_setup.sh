#!/bin/bash
# 🔐 BROSKI ULTRA SSH KEY SETUP 🔐
# Eliminates password prompts forever!

echo "🔑 BROSKI SSH KEY MAGIC ACTIVATED!"

# 1. Generate SSH key pair if doesn't exist
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "🔧 Generating new SSH key pair..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "broski-ultra-key-$(date +%Y%m%d)"
    echo "✅ SSH key pair created!"
else
    echo "🔑 SSH key already exists - using existing key"
fi

# 2. Set proper permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 644 ~/.ssh/authorized_keys 2>/dev/null || touch ~/.ssh/authorized_keys && chmod 644 ~/.ssh/authorized_keys

# 3. Add key to authorized_keys if not already there
if ! grep -q "$(cat ~/.ssh/id_rsa.pub)" ~/.ssh/authorized_keys 2>/dev/null; then
    echo "🔗 Adding key to authorized_keys..."
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
fi

# 4. Create connection shortcuts
echo "⚡ Creating connection shortcuts..."
cat > ~/connect-broski << 'EOF'
#!/bin/bash
# Quick connection script
echo "🚀 BROski Ultra Connection Activated!"
if [ -n "$1" ]; then
    ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no "$1"
else
    echo "Usage: ./connect-broski user@server"
fi
EOF

chmod +x ~/connect-broski

# 5. Display your public key for copying to other servers
echo ""
echo "🎯 YOUR SSH PUBLIC KEY (copy this to other servers):"
echo "================================================"
cat ~/.ssh/id_rsa.pub
echo "================================================"
echo ""
echo "📋 To use on other servers, run:"
echo "   ssh-copy-id -i ~/.ssh/id_rsa.pub user@server"
echo ""
echo "🔥 Connection script created: ~/connect-broski"
echo "✅ SSH KEY SETUP COMPLETE!"