#!/bin/bash
# 🔑💜 CHAOSGENIUS API KEYS SETUP WIZARD
# Quick setup for your Cloudflare Empire

echo "🌩️💜 CHAOSGENIUS API KEYS SETUP WIZARD"
echo "======================================"
echo ""

# Copy template to .env if it doesn't exist
if [ ! -f .env ]; then
    cp .env.template .env
    echo "✅ Created .env from template"
else
    echo "⚠️  .env already exists - will not overwrite"
fi

echo ""
echo "🎯 PRIORITY API KEYS YOU NEED:"
echo ""

echo "1️⃣ 🌩️ CLOUDFLARE (CRITICAL - You're already paying!)"
echo "   📍 Get from: Cloudflare Dashboard → My Profile → API Tokens"
echo "   🔗 Direct link: https://dash.cloudflare.com/profile/api-tokens"
echo "   📝 Need: CLOUDFLARE_API_TOKEN + CLOUDFLARE_ZONE_ID"
echo ""

echo "2️⃣ 🔒 FLASK SECRET KEY (Generate NOW)"
echo "   🎲 Random secure key:"
python3 -c "import secrets; print('   ' + secrets.token_urlsafe(32))"
echo ""

echo "3️⃣ 🎮 DISCORD BOT (For community features)"
echo "   📍 Get from: https://discord.com/developers/applications"
echo "   📝 Need: DISCORD_BOT_TOKEN"
echo ""

echo "4️⃣ 🤖 AI SERVICES (Optional but powerful)"
echo "   📍 OpenAI: https://platform.openai.com/api-keys"
echo "   📍 Anthropic: https://console.anthropic.com/"
echo ""

echo "🚀 QUICK START COMMANDS:"
echo ""
echo "# Edit your .env file:"
echo "nano .env"
echo ""
echo "# Test Cloudflare connection:"
echo "python3 -c \"from src.src.cloudflare_setup_helper_1 import CloudflareSetupHelper; CloudflareSetupHelper().verify_token()\""
echo ""
echo "# Launch empire:"
echo "python3 cloudflare_dashboard.py"
echo ""

echo "💜 Your Cloudflare empire awaits! Add those keys and dominate! 🌍"