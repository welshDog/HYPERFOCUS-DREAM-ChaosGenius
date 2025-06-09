# 🚀 DEPLOYMENT GUIDE - ChaosGenius Empire

## 🌩️💜 BROSKI ULTRA SERVER IMMORTALITY DEPLOYMENT

This guide covers all deployment scenarios for the ChaosGenius Empire ecosystem.

## 🎯 Deployment Options

### 1. 🚀 Quick Local Development

```bash
# Clone and setup
git clone <your-repo-url>
cd chaosgenius
pip install -r requirements_minimal.txt

# Quick launch
./quick_launch.sh
# OR
python quick_launch.py
```

### 2. ☁️ Cloudflare Edge Deployment

```bash
# Deploy to Cloudflare
./deploy_cloudflare_empire.sh

# Manual Cloudflare setup
wrangler deploy cloudflare-worker.js
```

### 3. 🐳 Docker Deployment

```bash
# Build minimal image
docker build -f Dockerfile.minimal -t chaosgenius:latest .

# Run container
docker run -d \
  --name chaosgenius-empire \
  -p 8080:8080 \
  -e DISCORD_TOKEN=your_token \
  -e CLOUDFLARE_API_KEY=your_key \
  chaosgenius:latest
```

### 4. 🚂 Railway Deployment

```bash
# Railway configuration is in railway.json
railway login
railway deploy
```

### 5. 📦 Production Server

```bash
# Full production setup
./broski_ultra_server_manager.sh
./start_immortal_system.sh
```

## 🔧 Configuration Setup

### Environment Variables

Create `.env` file:

```env
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_guild_id

# Cloudflare Configuration
CLOUDFLARE_API_KEY=your_cloudflare_api_key
CLOUDFLARE_EMAIL=your_cloudflare_email
CLOUDFLARE_ZONE_ID=your_zone_id

# Database Configuration
DATABASE_URL=sqlite:///broski_overseer.db

# Security Configuration
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
DEBUG=false
```

### Token Configuration

Update `broski_token_config.json`:

```json
{
  "discord": {
    "token": "your_discord_token",
    "guild_id": "your_guild_id",
    "permissions": "administrator"
  },
  "cloudflare": {
    "api_key": "your_api_key",
    "email": "your_email",
    "zone_id": "your_zone_id"
  },
  "security": {
    "encryption_enabled": true,
    "token_rotation": true,
    "secure_storage": true
  }
}
```

## 🛡️ Security Setup

### 1. SSH Key Configuration

```bash
./broski_ssh_key_setup.sh
```

### 2. Firewall Setup

```bash
./broski_firewall_guardian.sh
```

### 3. Security Monitoring

```bash
./broski_advanced_security_monitor.sh
```

## 📊 Monitoring Setup

### Health Checks

```bash
# System health
python empire_health_check.py

# Service monitoring
./broski_service_monitor.sh

# Load optimization
./broski_load_optimizer.sh
```

### Dashboard Access

- Main Dashboard: `http://your-domain:8080/dashboard`
- Guardian HUD: `http://your-domain:8080/guardian`
- Analytics: `http://your-domain:8080/analytics`
- Neural Pulse: `http://your-domain:8080/neural`

## 🤖 AI Agent Army Deployment

### Agent Configuration

```python
# agent_army_manifest.json
{
  "agents": [
    {
      "name": "CodeQualityAgent",
      "script": "agent_army_mission_1_code_quality.py",
      "schedule": "*/5 * * * *",
      "enabled": true
    },
    {
      "name": "SecurityFortressAgent",
      "script": "agent_army_mission_2_security_fortress.py",
      "schedule": "0 */2 * * *",
      "enabled": true
    }
  ]
}
```

### Agent Deployment

```bash
# Deploy agent army
python agent_army_forge_master.py

# Manual agent execution
python agent_army_mission_1_code_quality.py
python agent_army_mission_2_security_fortress.py
```

## 🔄 Automated Deployment

### Cron Jobs Setup

```bash
# Setup automated tasks
./broski_agent_cron_scheduler.sh

# Example cron entries:
# */5 * * * * /path/to/chaosgenius/broski_service_monitor.sh
# 0 2 * * * /path/to/chaosgenius/broski_automated_maintenance.sh
# */10 * * * * /path/to/chaosgenius/broski_connection_stabilizer.sh
```

### TMUX Session Management

```bash
# Start TMUX sessions
./tmux_agent_manager.sh

# Manual TMUX setup
tmux new-session -d -s chaosgenius
tmux send-keys -t chaosgenius "cd /path/to/chaosgenius && python broski_ultra_launcher.py" Enter
```

## 📱 Platform-Specific Deployments

### Heroku Deployment

```bash
# Procfile is included
git push heroku main
```

### AWS Deployment

```bash
# Use Docker image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag chaosgenius:latest <account>.dkr.ecr.us-east-1.amazonaws.com/chaosgenius:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/chaosgenius:latest
```

### DigitalOcean Deployment

```bash
# Deploy to DigitalOcean Apps
doctl apps create --spec .do/app.yaml
```

## 🌐 IPFS Deployment

### IPFS Setup

```bash
# IPFS build configuration in ipfs_build/
cd ipfs_build
npm install
npm run build
ipfs add -r dist/
```

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Kill process on port 8080
sudo fuser -k 8080/tcp
# OR find and kill specific process
sudo netstat -tulpn | grep 8080
sudo kill -9 <PID>
```

#### Database Connection Issues

```bash
# Reset databases
rm *.db
python broski_brain_data_engine.py --reset
```

#### Discord Token Issues

```bash
# Validate token
python -c "import discord; print('Token valid')"
```

#### Cloudflare Connection Issues

```bash
# Test Cloudflare API
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
  -H "Content-Type: application/json"
```

### Logs and Debugging

```bash
# View logs
tail -f logs/broski_*.log

# Debug mode
DEBUG=true python app.py

# System diagnostics
python empire_health_check.py --verbose
```

## 🚀 Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Firewall configured
- [ ] Backup system setup
- [ ] Monitoring enabled
- [ ] Health checks configured
- [ ] Agent army deployed
- [ ] Security scans completed
- [ ] Performance optimized
- [ ] Documentation updated

## 📞 Support

If you encounter issues during deployment:

1. Check the logs in `logs/` directory
2. Run `python empire_health_check.py`
3. Review the troubleshooting section
4. Contact support: support@chaosgenius.com

---

**Deployment completed successfully! 🌩️💜**
_Your ChaosGenius Empire is now IMMORTAL!_
