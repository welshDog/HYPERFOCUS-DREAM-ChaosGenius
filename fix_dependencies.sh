#!/bin/bash
# 🔧💎 CHAOSGENIUS DEPENDENCY FIXER v2.0 💎🔧
# Fixes missing dependencies that caused service failures

echo "🔧💎 FIXING CHAOSGENIUS DEPENDENCIES 💎🔧"

# Install missing Python packages
echo "📦 Installing missing Python packages..."

# Check if we can use system packages first
if command -v apt &> /dev/null; then
    echo "📦 Using system package manager..."
    apt update
    apt install -y python3-fastapi python3-uvicorn python3-pydantic || echo "⚠️ Some system packages failed"
fi

# Install via pip as backup
echo "📦 Installing via pip..."
pip3 install --break-system-packages fastapi uvicorn pydantic python-multipart || echo "⚠️ Some pip packages failed"

# Additional packages that might be needed
pip3 install --break-system-packages aiofiles jinja2 || echo "⚠️ Some additional packages failed"

echo "✅ Dependency installation complete!"
echo "🚀 You can now run the sync system again!"