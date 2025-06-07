# 🔧 ChaosGenius Configuration Guide

## 🛡️ Security First Setup

### Environment Variables Setup

1. **Copy the template files:**

   ```bash
   cp .env.dev .env.local
   cp .env.prod .env.production
   ```

2. **Add your actual tokens to the local files:**

   - Replace `your_discord_bot_token_here` with your actual Discord bot token
   - Replace `your_application_id_here` with your Discord application ID
   - Update database URLs and secret keys

3. **Keep your local .env files secure:**
   - Add `.env.local` and `.env.production` to your `.gitignore`
   - Never commit actual tokens to version control

### 🎯 Discord Bot Setup

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token to your local .env file
5. Copy the application ID from "General Information"

### 🚀 Quick Start

```bash
# Load your environment
source config/.env.local

# Run the system
python chaosgenius_discord_bot.py
```

## 📋 Configuration Files

- `.env.dev` - Development template (safe to commit)
- `.env.prod` - Production template (safe to commit)
- `.env.local` - Your local development config (DO NOT COMMIT)
- `.env.production` - Your production config (DO NOT COMMIT)

## 🔐 Security Best Practices

✅ Use environment variables for sensitive data
✅ Keep actual tokens in local files only
✅ Use templates for version control
✅ Rotate tokens regularly
✅ Use different tokens for dev/prod

❌ Never commit actual tokens
❌ Don't share .env files
❌ Don't hardcode secrets in source code
