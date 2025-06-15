#!/usr/bin/env python3
"""
🎮💰 BROSKI PORTAL DISCORD COMMANDS - ULTRA LEGENDARY EDITION 💰🎮
Complete Discord integration with BROski$ payment system for portal upgrades!
Official Discord Server: https://discord.gg/chyXCC4zj2
🚀 NEW LEGENDARY FEATURES: Admin Dashboard, Revenue Tracking, Leaderboards! 🚀
"""

import asyncio
import json
import random
import sqlite3
from datetime import datetime

import discord
from discord.ext import commands

# 🔗 OFFICIAL BROSKI DISCORD SERVER - THE PORTAL GATEWAY! 🔗
OFFICIAL_DISCORD_INVITE = "https://discord.gg/chyXCC4zj2"

# 👑 LEGENDARY ADMIN USER IDs - FOUNDERS ONLY! 👑
ADMIN_USER_IDS = [
    # Add your Discord user ID here for admin access
    # Example: 123456789012345678
]

# 💰 BROSKI$ UPGRADE PRICING SYSTEM
UPGRADE_TIERS = {
    "basic": {
        "name": "🌟 Basic Portal",
        "price": 100,
        "features": [
            "Basic dashboard access",
            "3 AI agent slots",
            "Memory crystal storage",
            "Focus session tracking",
        ],
    },
    "premium": {
        "name": "🚀 Premium Portal",
        "price": 500,
        "features": [
            "15+ AI Agent Army",
            "Guardian Zero protection",
            "Money Maker Agent",
            "Advanced analytics",
            "Gaming mode interface",
            "Custom themes",
            "Priority support",
        ],
    },
    "legendary": {
        "name": "👑 Legendary Portal",
        "price": 2000,
        "features": [
            "Real-time neural bus connection",
            "BRAINVERSE link access",
            "Exclusive founder channels",
            "Personal BROski AI mentor",
            "Custom portal themes",
            "Direct founder access",
            "Unlimited AI agents",
            "VIP everything",
        ],
    },
}

# 🎁 SPECIAL EVENTS AND BONUSES
DAILY_BONUSES = {
    "chat_bonus": 10,
    "command_usage": 2,
    "help_others": 15,
    "creative_content": 25,
    "server_boost": 100,
}


class BROskiPortalCommands(commands.Cog):
    """🎮 Portal connection and upgrade commands"""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "/root/chaosgenius/broski_overseer.db"
        self.init_database()

    def init_database(self):
        """Initialize the BROski$ database with LEGENDARY tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create tokens table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS broski_tokens (
                    user_id TEXT PRIMARY KEY,
                    balance INTEGER DEFAULT 0,
                    portal_tier TEXT DEFAULT 'none',
                    total_earned INTEGER DEFAULT 0,
                    total_spent INTEGER DEFAULT 0,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    referral_code TEXT,
                    referred_by TEXT
                )
            """
            )

            # Create transactions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS broski_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    amount INTEGER,
                    type TEXT,
                    description TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create daily activity tracking
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_activity (
                    user_id TEXT,
                    date TEXT,
                    messages_sent INTEGER DEFAULT 0,
                    commands_used INTEGER DEFAULT 0,
                    tokens_earned INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, date)
                )
            """
            )

            # Create leaderboard table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS leaderboard (
                    user_id TEXT PRIMARY KEY,
                    username TEXT,
                    total_tokens INTEGER DEFAULT 0,
                    portal_tier TEXT,
                    achievements TEXT DEFAULT '[]',
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()
            conn.close()
            print("✅ BROski$ LEGENDARY database initialized!")

        except Exception as e:
            print(f"❌ Database init error: {e}")

    def is_admin(self, user_id):
        """Check if user is a LEGENDARY admin"""
        return str(user_id) in [str(id) for id in ADMIN_USER_IDS]

    def get_user_balance(self, user_id):
        """Get user's BROski$ balance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance, portal_tier, total_earned, total_spent FROM broski_tokens WHERE user_id = ?",
                (str(user_id),),
            )
            result = cursor.fetchone()

            if result:
                balance, tier, earned, spent = result
                conn.close()
                return balance, tier, earned, spent
            else:
                # Create new user with 50 starter tokens
                cursor.execute(
                    "INSERT INTO broski_tokens (user_id, balance, total_earned) VALUES (?, ?, ?)",
                    (str(user_id), 50, 50),
                )
                conn.commit()
                conn.close()
                return 50, "none", 50, 0

        except Exception as e:
            print(f"❌ Balance check error: {e}")
            return 0, "none", 0, 0

    def update_balance(self, user_id, amount, transaction_type, description):
        """Update user's BROski$ balance with LEGENDARY tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Update balance and stats
            if amount > 0:
                cursor.execute(
                    """UPDATE broski_tokens
                       SET balance = balance + ?,
                           total_earned = total_earned + ?,
                           last_activity = CURRENT_TIMESTAMP
                       WHERE user_id = ?""",
                    (amount, amount, str(user_id)),
                )
            else:
                cursor.execute(
                    """UPDATE broski_tokens
                       SET balance = balance + ?,
                           total_spent = total_spent + ?,
                           last_activity = CURRENT_TIMESTAMP
                       WHERE user_id = ?""",
                    (amount, abs(amount), str(user_id)),
                )

            # Record transaction
            cursor.execute(
                "INSERT INTO broski_transactions (user_id, amount, type, description) VALUES (?, ?, ?, ?)",
                (str(user_id), amount, transaction_type, description),
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Balance update error: {e}")
            return False

    def upgrade_portal_tier(self, user_id, tier):
        """Upgrade user's portal tier"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE broski_tokens SET portal_tier = ? WHERE user_id = ?",
                (tier, str(user_id)),
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Portal upgrade error: {e}")
            return False

    @discord.app_commands.command(
        name="connect-portal", description="🎮 Connect Discord to Unlock Full Portal!"
    )
    async def connect_portal(self, interaction: discord.Interaction):
        """Connect to the BROski Portal system"""
        user_id = interaction.user.id
        balance, current_tier = self.get_user_balance(user_id)

        if current_tier != "none":
            embed = discord.Embed(
                title="🎮 Portal Already Connected! 🎮",
                description=f"Your {UPGRADE_TIERS[current_tier]['name']} is active!",
                color=0x00FF00,
            )
            embed.add_field(name="💰 Balance", value=f"{balance} BROski$", inline=True)
            embed.add_field(
                name="🔗 Discord Server",
                value=f"[Join Official Server]({OFFICIAL_DISCORD_INVITE})",
                inline=True,
            )
            await interaction.response.send_message(embed=embed)
            return

        if balance < 100:
            embed = discord.Embed(
                title="❌ Insufficient BROski$ Tokens",
                description=f"Need 100 BROski$ to connect portal (You have {balance})",
                color=0xFF0000,
            )
            embed.add_field(
                name="💰 Earn More Tokens",
                value="Use `/earn-tokens` to learn how to get more BROski$!",
                inline=False,
            )
            await interaction.response.send_message(embed=embed)
            return

        # Deduct tokens and upgrade to basic
        if self.update_balance(user_id, -100, "purchase", "Basic Portal Connection"):
            if self.upgrade_portal_tier(user_id, "basic"):
                embed = discord.Embed(
                    title="🎉 PORTAL CONNECTED SUCCESSFULLY! 🎉",
                    description="Welcome to the BROski Empire!",
                    color=0x9966FF,
                )
                embed.add_field(
                    name="🌟 Basic Portal Activated",
                    value="\n".join(UPGRADE_TIERS["basic"]["features"]),
                    inline=False,
                )
                embed.add_field(
                    name="💰 New Balance", value=f"{balance - 100} BROski$", inline=True
                )
                embed.add_field(
                    name="🔗 Official Discord",
                    value=f"[Join Here: {OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})",
                    inline=False,
                )
                embed.add_field(
                    name="🚀 Next Steps",
                    value="Use `/upgrade-shop` to see Premium and Legendary tiers!",
                    inline=False,
                )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(
                    "❌ Portal connection failed. Try again!"
                )
        else:
            await interaction.response.send_message("❌ Transaction failed. Try again!")

    @discord.app_commands.command(
        name="portal-status",
        description="📊 Check your portal tier and BROski$ balance",
    )
    async def portal_status(self, interaction: discord.Interaction):
        """Check portal status and balance"""
        user_id = interaction.user.id
        balance, tier = self.get_user_balance(user_id)

        if tier == "none":
            embed = discord.Embed(
                title="🎮 Portal Not Connected",
                description="Connect your portal to unlock the full BROski experience!",
                color=0xFF6600,
            )
            embed.add_field(name="💰 Balance", value=f"{balance} BROski$", inline=True)
            embed.add_field(
                name="🎯 Required", value="100 BROski$ to connect", inline=True
            )
            embed.add_field(
                name="🚀 Action", value="Use `/connect-portal` to start!", inline=False
            )
        else:
            tier_info = UPGRADE_TIERS[tier]
            embed = discord.Embed(
                title=f"🎮 {tier_info['name']} Active! 🎮",
                description="Your portal is connected and ready!",
                color=0x00FF00,
            )
            embed.add_field(name="💰 Balance", value=f"{balance} BROski$", inline=True)
            embed.add_field(name="🎯 Tier", value=tier_info["name"], inline=True)
            embed.add_field(
                name="✨ Features", value="\n".join(tier_info["features"]), inline=False
            )

        embed.add_field(
            name="🔗 Official Discord",
            value=f"[Join: {OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(
        name="upgrade-shop", description="🏪 Browse portal upgrades with BROski$"
    )
    async def upgrade_shop(self, interaction: discord.Interaction):
        """Show upgrade shop"""
        user_id = interaction.user.id
        balance, current_tier = self.get_user_balance(user_id)

        embed = discord.Embed(
            title="🏪 BROSKI$ UPGRADE SHOP 🏪",
            description=f"Your Balance: {balance} BROski$",
            color=0x9966FF,
        )

        for tier_key, tier_info in UPGRADE_TIERS.items():
            status = (
                "✅ OWNED"
                if current_tier == tier_key
                else f"💰 {tier_info['price']} BROski$"
            )
            if current_tier == "none" and tier_key != "basic":
                status = "🔒 Unlock Basic First"
            elif tier_key == "premium" and current_tier == "basic":
                status = f"💰 {tier_info['price']} BROski$"
            elif tier_key == "legendary" and current_tier in ["basic", "premium"]:
                status = f"💰 {tier_info['price']} BROski$"

            embed.add_field(
                name=f"{tier_info['name']} - {status}",
                value="\n".join(tier_info["features"][:3]) + "\n...",
                inline=True,
            )

        embed.add_field(
            name="💡 How to Purchase",
            value="Use `/buy-upgrade [tier]` to purchase!\nExample: `/buy-upgrade premium`",
            inline=False,
        )

        embed.add_field(
            name="🔗 Official Discord",
            value=f"[Join: {OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(
        name="buy-upgrade", description="💰 Purchase portal upgrade with BROski$"
    )
    @discord.app_commands.describe(
        tier="Choose upgrade tier: basic, premium, or legendary"
    )
    async def buy_upgrade(self, interaction: discord.Interaction, tier: str):
        """Purchase portal upgrade"""
        user_id = interaction.user.id
        balance, current_tier = self.get_user_balance(user_id)
        tier = tier.lower()

        if tier not in UPGRADE_TIERS:
            await interaction.response.send_message(
                "❌ Invalid tier! Choose: basic, premium, or legendary"
            )
            return

        tier_info = UPGRADE_TIERS[tier]

        # Check if already owned
        if current_tier == tier:
            await interaction.response.send_message(
                f"✅ You already own {tier_info['name']}!"
            )
            return

        # Check prerequisites
        if tier == "premium" and current_tier not in ["basic"]:
            await interaction.response.send_message("❌ Need Basic Portal first!")
            return

        if tier == "legendary" and current_tier not in ["basic", "premium"]:
            await interaction.response.send_message("❌ Need Premium Portal first!")
            return

        # Check balance
        if balance < tier_info["price"]:
            await interaction.response.send_message(
                f"❌ Insufficient funds! Need {tier_info['price']} BROski$ (You have {balance})"
            )
            return

        # Process purchase
        if self.update_balance(
            user_id, -tier_info["price"], "purchase", f"{tier_info['name']} Upgrade"
        ):
            if self.upgrade_portal_tier(user_id, tier):
                embed = discord.Embed(
                    title=f"🎉 {tier_info['name']} ACTIVATED! 🎉",
                    description="Your portal has been upgraded!",
                    color=0x00FF00,
                )
                embed.add_field(
                    name="✨ New Features",
                    value="\n".join(tier_info["features"]),
                    inline=False,
                )
                embed.add_field(
                    name="💰 New Balance",
                    value=f"{balance - tier_info['price']} BROski$",
                    inline=True,
                )
                embed.add_field(
                    name="🔗 Official Discord",
                    value=f"[Join: {OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})",
                    inline=False,
                )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("❌ Upgrade failed. Try again!")
        else:
            await interaction.response.send_message("❌ Transaction failed. Try again!")

    @discord.app_commands.command(
        name="portal-invite",
        description="🔗 Get the official BROski Discord server link",
    )
    async def portal_invite(self, interaction: discord.Interaction):
        """Get Discord server invite"""
        embed = discord.Embed(
            title="🔗 OFFICIAL BROSKI DISCORD PORTAL",
            description="Join the LEGENDARY BROski Empire!",
            color=0x9966FF,
        )
        embed.add_field(
            name="🎮 Discord Server",
            value=f"**[{OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})**",
            inline=False,
        )
        embed.add_field(
            name="🚀 What You Get",
            value="• AI Agent Army access\n• BROski$ earning opportunities\n• Exclusive portal features\n• Direct founder interaction",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(
        name="earn-tokens", description="💰 Learn how to earn more BROski$ tokens"
    )
    async def earn_tokens(self, interaction: discord.Interaction):
        """Show ways to earn BROski$ tokens"""
        embed = discord.Embed(
            title="💰 EARN BROSKI$ TOKENS 💰",
            description="Multiple ways to earn tokens in Discord!",
            color=0xFFD700,
        )

        embed.add_field(
            name="💬 Chat Activity",
            value="• 1-3 BROski$ per message\n• Bonus for helpful messages\n• Daily chat bonuses",
            inline=True,
        )

        embed.add_field(
            name="🎯 Challenges",
            value="• Daily focus challenges\n• Weekly creativity quests\n• Monthly tournaments",
            inline=True,
        )

        embed.add_field(
            name="🤖 AI Interactions",
            value="• Use bot commands: +2 BROski$\n• Share AI art: +5 BROski$\n• Help others: +10 BROski$",
            inline=True,
        )

        embed.add_field(
            name="🏆 Special Events",
            value="• Server boosts: +100 BROski$\n• Referrals: +50 BROski$\n• Community contributions: +25 BROski$",
            inline=False,
        )

        embed.add_field(
            name="🔗 Join Official Discord",
            value=f"[{OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(
        name="admin-dashboard", description="👑 LEGENDARY Admin Dashboard (Admins Only)"
    )
    async def admin_dashboard(self, interaction: discord.Interaction):
        """LEGENDARY admin dashboard"""
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message(
                "❌ Admin access required!", ephemeral=True
            )
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get total stats
            cursor.execute("SELECT COUNT(*) FROM broski_tokens")
            total_users = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(total_spent) FROM broski_tokens")
            total_revenue = cursor.fetchone()[0] or 0

            cursor.execute(
                "SELECT COUNT(*) FROM broski_tokens WHERE portal_tier != 'none'"
            )
            connected_users = cursor.fetchone()[0]

            cursor.execute(
                "SELECT portal_tier, COUNT(*) FROM broski_tokens GROUP BY portal_tier"
            )
            tier_distribution = cursor.fetchall()

            # Recent transactions
            cursor.execute(
                """
                SELECT bt.user_id, bt.amount, bt.description, bt.timestamp
                FROM broski_transactions bt
                WHERE bt.type = 'purchase'
                ORDER BY bt.timestamp DESC
                LIMIT 5
            """
            )
            recent_sales = cursor.fetchall()

            conn.close()

            embed = discord.Embed(
                title="👑 LEGENDARY ADMIN DASHBOARD 👑",
                description="BROski$ Empire Statistics",
                color=0xFFD700,
            )

            embed.add_field(
                name="📊 Empire Stats",
                value=f"👥 Total Users: {total_users}\n💰 Total Revenue: {total_revenue} BROski$\n🔗 Connected: {connected_users}",
                inline=True,
            )

            tier_text = ""
            for tier, count in tier_distribution:
                tier_text += f"{tier}: {count}\n"

            embed.add_field(
                name="🏆 Tier Distribution",
                value=tier_text or "No data",
                inline=True,
            )

            if recent_sales:
                sales_text = ""
                for sale in recent_sales[:3]:
                    sales_text += f"User {sale[0]}: {sale[1]} BROski$ - {sale[2]}\n"
                embed.add_field(
                    name="💵 Recent Sales",
                    value=sales_text,
                    inline=False,
                )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Dashboard error: {e}", ephemeral=True
            )

    @discord.app_commands.command(
        name="leaderboard", description="🏆 BROski$ Token Leaderboard"
    )
    async def leaderboard(self, interaction: discord.Interaction):
        """Show the LEGENDARY leaderboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT user_id, total_earned, portal_tier
                FROM broski_tokens
                ORDER BY total_earned DESC
                LIMIT 10
            """
            )
            top_users = cursor.fetchall()
            conn.close()

            embed = discord.Embed(
                title="🏆 BROSKI$ LEADERBOARD 🏆",
                description="Top Token Earners in the Empire!",
                color=0xFFD700,
            )

            if top_users:
                leaderboard_text = ""
                for i, (user_id, earned, tier) in enumerate(top_users, 1):
                    try:
                        user = self.bot.get_user(int(user_id))
                        username = user.display_name if user else f"User {user_id[-4:]}"
                    except:
                        username = f"User {user_id[-4:]}"

                    tier_emoji = {
                        "basic": "🌟",
                        "premium": "🚀",
                        "legendary": "👑",
                    }.get(tier, "⚫")
                    leaderboard_text += (
                        f"{i}. {tier_emoji} {username}: {earned} BROski$\n"
                    )

                embed.add_field(
                    name="💰 Top Earners",
                    value=leaderboard_text,
                    inline=False,
                )
            else:
                embed.add_field(
                    name="💰 Top Earners",
                    value="No data yet - be the first!",
                    inline=False,
                )

            embed.add_field(
                name="🔗 Join Discord",
                value=f"[{OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})",
                inline=False,
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Leaderboard error: {e}")

    @discord.app_commands.command(
        name="daily-bonus", description="🎁 Claim your daily BROski$ bonus!"
    )
    async def daily_bonus(self, interaction: discord.Interaction):
        """Claim daily bonus tokens"""
        user_id = interaction.user.id
        today = datetime.now().strftime("%Y-%m-%d")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if already claimed today
            cursor.execute(
                "SELECT tokens_earned FROM daily_activity WHERE user_id = ? AND date = ?",
                (str(user_id), today),
            )
            result = cursor.fetchone()

            if result and result[0] > 0:
                await interaction.response.send_message(
                    "❌ Daily bonus already claimed! Come back tomorrow! 🌅"
                )
                return

            # Generate bonus (10-50 tokens)
            bonus_amount = random.randint(10, 50)

            # Update balance
            self.update_balance(
                user_id, bonus_amount, "daily_bonus", "Daily Login Bonus"
            )

            # Record daily activity
            cursor.execute(
                """INSERT OR REPLACE INTO daily_activity
                   (user_id, date, tokens_earned)
                   VALUES (?, ?, ?)""",
                (str(user_id), today, bonus_amount),
            )

            conn.commit()
            conn.close()

            embed = discord.Embed(
                title="🎁 DAILY BONUS CLAIMED! 🎁",
                description=f"You earned {bonus_amount} BROski$ tokens!",
                color=0x00FF00,
            )

            embed.add_field(
                name="💰 Bonus Amount",
                value=f"{bonus_amount} BROski$",
                inline=True,
            )

            embed.add_field(
                name="⏰ Next Bonus",
                value="Tomorrow! 🌅",
                inline=True,
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Bonus error: {e}")

    @discord.app_commands.command(
        name="gift-tokens", description="🎁 Gift BROski$ tokens to another user"
    )
    @discord.app_commands.describe(
        recipient="The user to gift tokens to", amount="Amount of tokens to gift"
    )
    async def gift_tokens(
        self, interaction: discord.Interaction, recipient: discord.Member, amount: int
    ):
        """Gift tokens to another user"""
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive!")
            return

        if amount > 1000:
            await interaction.response.send_message(
                "❌ Maximum gift is 1000 BROski$ per transaction!"
            )
            return

        sender_id = interaction.user.id
        recipient_id = recipient.id

        if sender_id == recipient_id:
            await interaction.response.send_message(
                "❌ You can't gift tokens to yourself!"
            )
            return

        balance, _, _, _ = self.get_user_balance(sender_id)

        if balance < amount:
            await interaction.response.send_message(
                f"❌ Insufficient funds! You have {balance} BROski$"
            )
            return

        # Process gift
        if self.update_balance(
            sender_id, -amount, "gift_sent", f"Gift to {recipient.display_name}"
        ) and self.update_balance(
            recipient_id,
            amount,
            "gift_received",
            f"Gift from {interaction.user.display_name}",
        ):

            embed = discord.Embed(
                title="🎁 TOKENS GIFTED SUCCESSFULLY! 🎁",
                description=f"{interaction.user.display_name} gifted {amount} BROski$ to {recipient.display_name}!",
                color=0xFF69B4,
            )

            embed.add_field(
                name="💝 Gift Amount",
                value=f"{amount} BROski$",
                inline=True,
            )

            embed.add_field(
                name="👥 Recipient",
                value=recipient.mention,
                inline=True,
            )

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Gift failed. Try again!")

    # ...existing code...


async def setup(bot):
    """Setup function for the cog"""
    await bot.add_cog(BROskiPortalCommands(bot))


# Export for bot integration
__all__ = ["BROskiPortalCommands"]
