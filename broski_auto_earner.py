#!/usr/bin/env python3
"""
🎮🚀 BROSKI DISCORD AUTO-EARNER & SPECIAL EVENTS - ULTRA EDITION 🚀🎮
Automatic BROski$ earning system for Discord activity + LEGENDARY events!
"""

import asyncio
import json
import random
import sqlite3
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

# 🎁 SPECIAL EVENT CONFIGURATIONS
SPECIAL_EVENTS = {
    "double_tokens": {
        "name": "💰 DOUBLE TOKEN WEEKEND",
        "description": "All token earnings are DOUBLED!",
        "multiplier": 2.0,
        "duration_hours": 48,
    },
    "mega_bonus": {
        "name": "🚀 MEGA BONUS HOUR",
        "description": "Random 100-500 token drops!",
        "bonus_range": (100, 500),
        "duration_hours": 1,
    },
    "founder_giveaway": {
        "name": "👑 FOUNDER'S LEGENDARY GIVEAWAY",
        "description": "10,000 BROski$ prize pool!",
        "prize_pool": 10000,
        "winner_count": 10,
        "duration_hours": 24,
    },
}

# 🎯 AUTO-EARNING RATES
EARNING_RATES = {
    "message": {"min": 1, "max": 3},
    "command_use": {"min": 2, "max": 5},
    "reaction_add": {"min": 1, "max": 2},
    "voice_minute": {"min": 2, "max": 4},
    "server_boost": {"fixed": 100},
    "invite_friend": {"fixed": 50},
}


class BROskiAutoEarner(commands.Cog):
    """🎮 Automatic BROski$ earning system"""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "/root/chaosgenius/broski_overseer.db"
        self.active_events = {}
        self.user_cooldowns = {}
        self.check_events.start()

    def cog_unload(self):
        self.check_events.cancel()

    @tasks.loop(minutes=5)
    async def check_events(self):
        """Check and manage special events"""
        try:
            # Check if we should start random events
            if random.randint(1, 100) <= 2:  # 2% chance every 5 minutes
                await self.start_random_event()

            # Check active events
            current_time = datetime.now()
            expired_events = []

            for event_id, event_data in self.active_events.items():
                if current_time >= event_data["end_time"]:
                    expired_events.append(event_id)
                    await self.end_event(event_id, event_data)

            # Remove expired events
            for event_id in expired_events:
                del self.active_events[event_id]

        except Exception as e:
            print(f"❌ Event check error: {e}")

    async def start_random_event(self):
        """Start a random special event"""
        if len(self.active_events) >= 2:  # Max 2 concurrent events
            return

        event_type = random.choice(list(SPECIAL_EVENTS.keys()))
        event_config = SPECIAL_EVENTS[event_type]

        event_id = f"{event_type}_{int(datetime.now().timestamp())}"
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=event_config["duration_hours"])

        self.active_events[event_id] = {
            "type": event_type,
            "config": event_config,
            "start_time": start_time,
            "end_time": end_time,
            "participants": set(),
        }

        # Announce event in all servers
        for guild in self.bot.guilds:
            try:
                # Find general channel
                channel = (
                    discord.utils.get(guild.text_channels, name="general")
                    or guild.text_channels[0]
                )

                embed = discord.Embed(
                    title=f"🎉 {event_config['name']} STARTED! 🎉",
                    description=event_config["description"],
                    color=0xFFD700,
                )
                embed.add_field(
                    name="⏰ Duration",
                    value=f"{event_config['duration_hours']} hours",
                    inline=True,
                )
                embed.add_field(
                    name="🎯 How to Participate",
                    value="Just be active in Discord!",
                    inline=True,
                )

                await channel.send(embed=embed)

            except Exception as e:
                print(f"❌ Event announcement error: {e}")

    async def end_event(self, event_id, event_data):
        """End a special event and distribute rewards"""
        event_config = event_data["config"]
        participants = list(event_data["participants"])

        if event_data["type"] == "founder_giveaway" and participants:
            # Distribute giveaway prizes
            winners = random.sample(
                participants, min(event_config["winner_count"], len(participants))
            )
            prize_per_winner = event_config["prize_pool"] // len(winners)

            for winner_id in winners:
                self.add_tokens(
                    winner_id,
                    prize_per_winner,
                    "giveaway_win",
                    "Founder's Giveaway Winner!",
                )

        # Announce event end
        for guild in self.bot.guilds:
            try:
                channel = (
                    discord.utils.get(guild.text_channels, name="general")
                    or guild.text_channels[0]
                )

                embed = discord.Embed(
                    title=f"🏁 {event_config['name']} ENDED! 🏁",
                    description=f"Thanks to all {len(participants)} participants!",
                    color=0xFF6600,
                )

                if event_data["type"] == "founder_giveaway" and participants:
                    winner_mentions = [f"<@{winner_id}>" for winner_id in winners[:5]]
                    embed.add_field(
                        name="🏆 Winners",
                        value="\n".join(winner_mentions)
                        + (f"\n+{len(winners)-5} more!" if len(winners) > 5 else ""),
                        inline=False,
                    )

                await channel.send(embed=embed)

            except Exception as e:
                print(f"❌ Event end announcement error: {e}")

    def add_tokens(self, user_id, amount, transaction_type, description):
        """Add tokens to user with event multipliers"""
        try:
            # Apply event multipliers
            multiplier = 1.0
            for event_data in self.active_events.values():
                if event_data["type"] == "double_tokens":
                    multiplier *= event_data["config"]["multiplier"]
                    event_data["participants"].add(str(user_id))

            final_amount = int(amount * multiplier)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create user if doesn't exist
            cursor.execute(
                """INSERT OR IGNORE INTO broski_tokens
                   (user_id, balance, total_earned)
                   VALUES (?, 50, 50)""",
                (str(user_id),),
            )

            # Update balance
            cursor.execute(
                """UPDATE broski_tokens
                   SET balance = balance + ?,
                       total_earned = total_earned + ?,
                       last_activity = CURRENT_TIMESTAMP
                   WHERE user_id = ?""",
                (final_amount, final_amount, str(user_id)),
            )

            # Record transaction
            cursor.execute(
                """INSERT INTO broski_transactions
                   (user_id, amount, type, description)
                   VALUES (?, ?, ?, ?)""",
                (str(user_id), final_amount, transaction_type, description),
            )

            conn.commit()
            conn.close()

            return final_amount

        except Exception as e:
            print(f"❌ Token add error: {e}")
            return 0

    def is_on_cooldown(self, user_id, action):
        """Check if user is on cooldown for an action"""
        now = datetime.now()
        user_key = f"{user_id}_{action}"

        if user_key in self.user_cooldowns:
            if now < self.user_cooldowns[user_key]:
                return True

        # Set cooldown (30 seconds for messages, 10 seconds for reactions)
        cooldown_seconds = 30 if action == "message" else 10
        self.user_cooldowns[user_key] = now + timedelta(seconds=cooldown_seconds)
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        """Auto-earn tokens from messages"""
        if message.author.bot:
            return

        user_id = message.author.id

        # Check cooldown
        if self.is_on_cooldown(user_id, "message"):
            return

        # Calculate earnings
        base_amount = random.randint(
            EARNING_RATES["message"]["min"], EARNING_RATES["message"]["max"]
        )

        # Bonus for longer messages
        if len(message.content) > 100:
            base_amount += 1
        if len(message.content) > 300:
            base_amount += 2

        # Bonus for helpful keywords
        helpful_keywords = [
            "help",
            "thanks",
            "awesome",
            "great",
            "amazing",
            "broski",
            "legendary",
        ]
        for keyword in helpful_keywords:
            if keyword.lower() in message.content.lower():
                base_amount += 1
                break

        earned = self.add_tokens(
            user_id, base_amount, "chat_activity", "Discord Chat Activity"
        )

        # Random bonus announcements (1% chance)
        if random.randint(1, 100) == 1:
            embed = discord.Embed(
                title="💰 BROSKI$ EARNED! 💰",
                description=f"{message.author.mention} earned {earned} BROski$ tokens!",
                color=0x00FF00,
            )
            await message.channel.send(embed=embed, delete_after=10)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Auto-earn tokens from reactions"""
        if user.bot:
            return

        user_id = user.id

        # Check cooldown
        if self.is_on_cooldown(user_id, "reaction"):
            return

        base_amount = random.randint(
            EARNING_RATES["reaction_add"]["min"], EARNING_RATES["reaction_add"]["max"]
        )
        self.add_tokens(
            user_id, base_amount, "reaction_activity", "Discord Reaction Activity"
        )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Auto-earn tokens from server boosts"""
        if before.premium_since is None and after.premium_since is not None:
            # User just boosted the server!
            amount = EARNING_RATES["server_boost"]["fixed"]
            earned = self.add_tokens(
                after.id, amount, "server_boost", "Server Boost Bonus!"
            )

            # Announce boost bonus
            try:
                channel = (
                    discord.utils.get(after.guild.text_channels, name="general")
                    or after.guild.text_channels[0]
                )
                embed = discord.Embed(
                    title="🚀 SERVER BOOST BONUS! 🚀",
                    description=f"{after.mention} boosted the server and earned {earned} BROski$ tokens!",
                    color=0xFF69B4,
                )
                await channel.send(embed=embed)
            except:
                pass

    @discord.app_commands.command(
        name="active-events", description="🎉 Check active special events"
    )
    async def active_events(self, interaction: discord.Interaction):
        """Show active special events"""
        if not self.active_events:
            embed = discord.Embed(
                title="🎯 No Active Events",
                description="Special events happen randomly! Keep being active in Discord!",
                color=0xFF6600,
            )
        else:
            embed = discord.Embed(
                title="🎉 ACTIVE SPECIAL EVENTS 🎉",
                description="Amazing events happening RIGHT NOW!",
                color=0xFFD700,
            )

            for event_id, event_data in self.active_events.items():
                config = event_data["config"]
                time_left = event_data["end_time"] - datetime.now()
                hours_left = int(time_left.total_seconds() // 3600)
                minutes_left = int((time_left.total_seconds() % 3600) // 60)

                embed.add_field(
                    name=config["name"],
                    value=f"{config['description']}\n⏰ Time left: {hours_left}h {minutes_left}m\n👥 Participants: {len(event_data['participants'])}",
                    inline=False,
                )

        embed.add_field(
            name="💡 How to Participate",
            value="Just be active! Chat, react, use commands, and earn tokens!",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(
        name="start-event", description="👑 Start special event (Admin only)"
    )
    @discord.app_commands.describe(
        event_type="Type of event: double_tokens, mega_bonus, founder_giveaway"
    )
    async def start_event(self, interaction: discord.Interaction, event_type: str):
        """Start a special event (admin only)"""
        # Check if user is admin (you can add your Discord ID to the check)
        admin_ids = ["YOUR_DISCORD_ID_HERE"]  # Replace with actual admin IDs

        if str(interaction.user.id) not in admin_ids:
            await interaction.response.send_message(
                "❌ Admin access required!", ephemeral=True
            )
            return

        if event_type not in SPECIAL_EVENTS:
            await interaction.response.send_message(
                "❌ Invalid event type!", ephemeral=True
            )
            return

        # Start the event
        event_config = SPECIAL_EVENTS[event_type]
        event_id = f"{event_type}_{int(datetime.now().timestamp())}"
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=event_config["duration_hours"])

        self.active_events[event_id] = {
            "type": event_type,
            "config": event_config,
            "start_time": start_time,
            "end_time": end_time,
            "participants": set(),
        }

        embed = discord.Embed(
            title=f"🎉 {event_config['name']} STARTED! 🎉",
            description=f"Event started by {interaction.user.mention}!",
            color=0xFFD700,
        )
        embed.add_field(
            name="📝 Description",
            value=event_config["description"],
            inline=False,
        )
        embed.add_field(
            name="⏰ Duration",
            value=f"{event_config['duration_hours']} hours",
            inline=True,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Setup function for the cog"""
    await bot.add_cog(BROskiAutoEarner(bot))


# Export for bot integration
__all__ = ["BROskiAutoEarner"]
