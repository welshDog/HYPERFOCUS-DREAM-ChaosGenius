# 🌟💜 DREAM DISCORD COMMUNITY BOT - SETUP GUIDE 💜🌟

## 🚀 **QUICK START GUIDE**

Your Discord bot is now ready to launch! Follow these simple steps:

### **Step 1: Configure Your Bot** 🔧

1. **Get Your Discord Bot Token:**
   - Go to https://discord.com/developers/applications
   - Create a new application or select existing one
   - Go to "Bot" section
   - Copy your bot token

2. **Get Your Discord Server ID:**
   - Open Discord in your browser or enable Developer Mode in app
   - Right-click your server name
   - Select "Copy Server ID"

3. **Update Environment Variables:**
   ```bash
   # Edit the .env file
   nano .env

   # Replace these values:
   DISCORD_BOT_TOKEN=your_actual_bot_token_here
   DISCORD_GUILD_ID=your_actual_server_id_here
   ```

### **Step 2: Install Dependencies** 📦

Run this command to install required Python packages:
```bash
pip install discord.py python-dotenv openai textblob aiohttp --break-system-packages
```

Or if you prefer system packages:
```bash
sudo apt update
sudo apt install python3-pip python3-discord python3-openai python3-textblob python3-aiohttp python3-dotenv
```

### **Step 3: Set Bot Permissions** 🛡️

Your bot needs these Discord permissions:
- Read Messages/View Channels
- Send Messages
- Send Messages in Threads
- Embed Links
- Attach Files
- Read Message History
- Add Reactions
- Use Slash Commands
- Manage Messages (optional)
- Manage Roles (optional)

### **Step 4: Launch Your Bot** 🚀

**Option A: Using the launcher script (recommended):**
```bash
cd /root/chaosgenius
./launch_discord_bot.sh
```

**Option B: Direct launch:**
```bash
cd /root/chaosgenius
python3 dream_discord_community_bot.py
```

---

## 🎮 **BOT FEATURES OVERVIEW**

Your Discord bot includes these amazing features:

### **🏆 Core Community Features**
- `/profile` - View your community profile with stats
- `/daily` - Claim daily BROski$ token rewards
- `/leaderboard` - See top community members
- `/tokens` - Check your token balance
- `/vibe` - Check community energy levels

### **🧠 ADHD-Focused Features**
- `/focus start` - Begin hyperfocus sessions
- `/check_in mood` - Daily mental health check-ins
- `/challenge today` - View daily community challenges
- `/mentor find` - Connect with community mentors

### **🎮 Interactive Games & Fun**
- `/minigame quiz` - ADHD knowledge quizzes
- `/minigame emoji` - Collaborative emoji stories
- `/showcase project` - Share your creative work
- `/mood energetic` - Set community vibes

### **🎪 Community Events**
- `/events` - See upcoming community events
- `/weekly_challenge` - Join weekly challenges
- `/achievements` - View your earned badges
- `/resources adhd` - Access knowledge library

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues & Solutions:**

**❌ Bot won't start:**
- Check your bot token is correct
- Ensure bot has permissions in your server
- Verify internet connection
- Check Python dependencies are installed

**❌ Commands not working:**
- Make sure bot has "Use Slash Commands" permission
- Try reinviting bot with updated permissions
- Check bot is online in your server

**❌ Database errors:**
- Bot automatically creates database on first run
- Ensure write permissions in the bot directory

**❌ Memory/space issues:**
- The bot uses SQLite for lightweight storage
- Monitor log files in `/root/chaosgenius/logs/`

### **Getting Help:**

If you need assistance:
1. Check the bot's error messages in terminal
2. Review Discord Developer Portal for API issues
3. Ensure all environment variables are set correctly
4. Try running with debug mode: `DEBUG_MODE=true`

---

## 🌟 **WHAT'S NEXT?**

Once your bot is running:

1. **Test Core Features:** Try `/profile` and `/daily` commands
2. **Set Community Mood:** Use `/mood energetic` to boost server energy
3. **Start Focus Sessions:** Try `/focus start 25` for a Pomodoro session
4. **Engage Members:** Encourage use of `/check_in` and `/showcase`
5. **Monitor Growth:** Use `/leaderboard` to see community engagement

Your Discord server now has a complete community engagement platform designed specifically for neurodivergent communities with ADHD support, mental health features, and productivity tools! 🎉

---

## 📊 **Bot Status Dashboard**

Once running, your bot provides:
- **Real-time member engagement tracking**
- **Token economy with daily rewards**
- **Achievement system with badges**
- **Focus session analytics**
- **Community mood monitoring**
- **Mental health check-in support**

Welcome to the most advanced neurodivergent-friendly Discord community bot! 🌈✨