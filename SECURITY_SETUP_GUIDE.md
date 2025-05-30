# 🔐 SECURITY SETUP GUIDE

## 🎯 IMPORTANT: API Keys & Credentials Setup

This repository is designed to be publicly shareable while keeping your sensitive API keys and credentials secure. Follow this guide to set up your environment safely.

## 🚨 NEVER COMMIT THESE FILES:
- `.env` (your actual environment variables)
- Any files containing API keys, tokens, or passwords
- Database files with user data
- Private encryption keys

## ✅ SAFE SETUP PROCESS:

### 1️⃣ Environment Variables
```bash
# Copy the template and add your actual keys
cp .env.template .env

# Edit .env with your real credentials (this file is gitignored)
nano .env
```

### 2️⃣ Required API Keys

#### 🤖 AI Services (Optional but Recommended)
- **OpenAI API Key**: For AI-powered features
- **Anthropic API Key**: For Claude AI integration

#### 🎮 Discord Integration
- **Discord Bot Token**: Create a bot at https://discord.com/developers/applications
- **Discord Guild ID**: Your Discord server ID

#### 🛒 E-commerce APIs (Optional)
- **Etsy API Key**: For Etsy shop integration
- **TikTok Shop API Key**: For TikTok commerce features

### 3️⃣ Quick Start Without API Keys
You can run the basic portal without any API keys:

```bash
# Navigate to portal
cd broski_hyperportal

# Install and run
npm install
npm run dev

# Visit: http://localhost:5173
# Admin password: chaosgeniusultra
```

### 4️⃣ Full System with APIs
```bash
# Set up environment variables first
cp .env.template .env
# Edit .env with your credentials

# Install Python dependencies
pip install -r requirements.txt

# Start the backend
python dashboard_api.py

# In another terminal, start the portal
cd broski_hyperportal
npm run dev
```

## 🛡️ SECURITY BEST PRACTICES:

### ✅ DO:
- Use `.env` files for sensitive data
- Keep API keys in environment variables
- Use the provided templates
- Check `.gitignore` before committing

### ❌ DON'T:
- Commit `.env` files
- Put API keys directly in code
- Share credentials in public repositories
- Commit database files with user data

## 🔧 TESTING WITHOUT REAL KEYS:

The system includes demo modes and fallbacks:

- **Portal**: Works without any APIs
- **Dashboard**: Basic functionality without external APIs
- **Discord Bot**: Will show "Demo Mode" without token
- **AI Features**: Will use mock responses without API keys

## 🆘 TROUBLESHOOTING:

### Environment Variables Not Loading?
```bash
# Check if .env exists
ls -la .env

# Verify format (key=value, no spaces around =)
cat .env
```

### API Keys Not Working?
- Verify keys are active and not expired
- Check API rate limits
- Ensure proper permissions for Discord bots
- Test keys with simple API calls first

### Still Having Issues?
- Check the logs in `/logs/` directory
- Run health check: `python health_check.py`
- Verify all dependencies are installed

## 🎯 PRODUCTION DEPLOYMENT:

For production deployment:
1. Use production-grade secret management
2. Enable HTTPS/SSL
3. Use environment-specific `.env` files
4. Implement proper backup strategies
5. Set up monitoring and alerts

---

**Remember: Security first! Never commit your actual API keys or sensitive data.** 🔐

*This guide ensures you can share your awesome project publicly while keeping your credentials private.*
