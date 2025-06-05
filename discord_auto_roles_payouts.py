#!/usr/bin/env python3
"""
🎮 BROSKI X EMPIRE - DISCORD AUTO-ROLES + BROSKI$ PAYOUTS
Advanced community management with automated rewards
"""
import asyncio
import json
import os
import random
import sqlite3

# Import our token system
import sys
from datetime import datetime, timedelta
from pathlib import Path

import discord
from discord.ext import commands, tasks

sys.path.append("/root/chaosgenius")
from ai_modules.broski.token_engine import BROskiTokenEngine


class BROskiDiscordManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token_engine = BROskiTokenEngine()

        # Role progression system
        self.role_hierarchy = {
            "Neuro Friend": {"min_tokens": 0, "color": 0x3498DB},
            "Neuro Helper": {"min_tokens": 100, "color": 0x9B59B6},
            "Neuro Champion": {"min_tokens": 500, "color": 0xE67E22},
            "Neuro Legend": {"min_tokens": 1000, "color": 0xE74C3C},
            "Neuro Emperor": {"min_tokens": 2500, "color": 0xF1C40F},
        }

        # Weekly mod rewards
        self.weekly_mod_tasks.start()
        self.daily_activity_check.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """🎊 Welcome new members with starter tokens and role"""
        try:
            # Create wallet and award welcome tokens
            wallet_result = self.token_engine.create_wallet(str(member.id))
            welcome_tokens = self.token_engine.award_tokens(
                str(member.id), 25.0, "🎊 Welcome to BROski Empire!"
            )

            # Assign starter role
            neuro_friend_role = discord.utils.get(
                member.guild.roles, name="Neuro Friend"
            )
            if neuro_friend_role:
                await member.add_roles(neuro_friend_role)

            # Send welcome DM with gift code
            gift_code = self.generate_gift_code(member.id)
            welcome_embed = discord.Embed(
                title="🎊 Welcome to the BROski Empire!",
                description=f"Hey {member.mention}! You've been awarded **25 BROski$** to start your journey!",
                color=0x00FF00,
            )
            welcome_embed.add_field(
                name="🎁 Your Gift Code", value=f"`{gift_code}`", inline=False
            )
            welcome_embed.add_field(
                name="💰 Token Balance", value="25 BROski$", inline=True
            )
            welcome_embed.add_field(
                name="🏆 Current Role", value="Neuro Friend", inline=True
            )

            await member.send(embed=welcome_embed)

            print(f"🎊 New member welcomed: {member.name} - 25 BROski$ awarded!")

        except Exception as e:
            print(f"❌ Error welcoming member {member.name}: {e}")

    @commands.command(name="check_role")
    async def check_role_progression(self, ctx):
        """🏆 Check if user qualifies for role upgrade"""
        user_id = str(ctx.author.id)
        current_balance = self.token_engine.get_balance(user_id)

        # Determine appropriate role
        target_role = "Neuro Friend"
        for role_name, requirements in self.role_hierarchy.items():
            if current_balance >= requirements["min_tokens"]:
                target_role = role_name

        # Check if user needs role update
        current_roles = [role.name for role in ctx.author.roles]
        hierarchy_roles = list(self.role_hierarchy.keys())

        # Remove old hierarchy roles and add new one
        for role_name in hierarchy_roles:
            if role_name in current_roles and role_name != target_role:
                old_role = discord.utils.get(ctx.guild.roles, name=role_name)
                if old_role:
                    await ctx.author.remove_roles(old_role)

        # Add new role if needed
        if target_role not in current_roles:
            new_role = discord.utils.get(ctx.guild.roles, name=target_role)
            if new_role:
                await ctx.author.add_roles(new_role)

                # Celebrate role upgrade!
                upgrade_embed = discord.Embed(
                    title="🎉 ROLE UPGRADE!",
                    description=f"Congratulations {ctx.author.mention}! You've been promoted to **{target_role}**!",
                    color=self.role_hierarchy[target_role]["color"],
                )
                upgrade_embed.add_field(
                    name="💰 Current Balance",
                    value=f"{current_balance} BROski$",
                    inline=True,
                )

                # Award bonus tokens for upgrade
                bonus_tokens = self.role_hierarchy[target_role]["min_tokens"] * 0.1
                self.token_engine.award_tokens(
                    user_id, bonus_tokens, f"🎉 Role upgrade bonus: {target_role}"
                )

                upgrade_embed.add_field(
                    name="🎁 Upgrade Bonus",
                    value=f"+{bonus_tokens} BROski$",
                    inline=True,
                )

                await ctx.send(embed=upgrade_embed)
            else:
                await ctx.send(
                    f"✅ You qualify for **{target_role}** but the role doesn't exist yet!"
                )
        else:
            await ctx.send(
                f"✅ You already have the correct role: **{target_role}** ({current_balance} BROski$)"
            )

    @tasks.loop(hours=168)  # Weekly
    async def weekly_mod_tasks(self):
        """💎 Weekly moderator rewards"""
        try:
            # Get all guilds the bot is in
            for guild in self.bot.guilds:
                mod_roles = ["Moderator", "Admin", "Neuro Mod"]

                for role_name in mod_roles:
                    role = discord.utils.get(guild.roles, name=role_name)
                    if role:
                        for member in role.members:
                            # Award weekly mod tokens
                            weekly_reward = 150.0
                            self.token_engine.award_tokens(
                                str(member.id),
                                weekly_reward,
                                "💎 Weekly moderator reward",
                            )

                            # Send DM notification
                            try:
                                reward_embed = discord.Embed(
                                    title="💎 Weekly Mod Reward!",
                                    description=f"Thank you for keeping the BROski Empire safe!",
                                    color=0xFFD700,
                                )
                                reward_embed.add_field(
                                    name="💰 Reward",
                                    value=f"+{weekly_reward} BROski$",
                                    inline=True,
                                )

                                await member.send(embed=reward_embed)
                                print(f"💎 Weekly reward sent to mod: {member.name}")

                            except discord.Forbidden:
                                print(f"⚠️ Couldn't DM mod reward to {member.name}")

        except Exception as e:
            print(f"❌ Error in weekly mod rewards: {e}")

    @tasks.loop(hours=24)  # Daily
    async def daily_activity_check(self):
        """⚡ Daily activity rewards"""
        try:
            # Reward active users who sent messages in last 24 hours
            for guild in self.bot.guilds:
                active_users = set()

                # Check recent messages in all channels
                for channel in guild.text_channels:
                    try:
                        async for message in channel.history(
                            limit=100, after=datetime.utcnow() - timedelta(days=1)
                        ):
                            if not message.author.bot:
                                active_users.add(message.author.id)
                    except discord.Forbidden:
                        continue

                # Reward active users
                for user_id in active_users:
                    daily_reward = random.uniform(5.0, 15.0)
                    self.token_engine.award_tokens(
                        str(user_id), daily_reward, "⚡ Daily activity reward"
                    )

                print(
                    f"⚡ Daily rewards distributed to {len(active_users)} active users"
                )

        except Exception as e:
            print(f"❌ Error in daily activity check: {e}")

    def generate_gift_code(self, user_id):
        """🎁 Generate unique gift codes for new members"""
        import hashlib
        import time

        # Create unique code based on user ID and timestamp
        raw_string = f"BROSKI{user_id}{int(time.time())}"
        hash_object = hashlib.md5(raw_string.encode())
        gift_code = f"NEURO-{hash_object.hexdigest()[:8].upper()}"

        # Store gift code in database
        try:
            conn = sqlite3.connect("broski_gift_codes.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS gift_codes (
                    code TEXT PRIMARY KEY,
                    user_id TEXT,
                    created_at TIMESTAMP,
                    redeemed BOOLEAN DEFAULT FALSE
                )
            """
            )

            cursor.execute(
                "INSERT INTO gift_codes (code, user_id, created_at) VALUES (?, ?, ?)",
                (gift_code, str(user_id), datetime.now()),
            )

            conn.commit()
            conn.close()

            return gift_code

        except Exception as e:
            print(f"❌ Error generating gift code: {e}")
            return f"NEURO-{user_id}"

    @commands.command(name="redeem")
    async def redeem_gift_code(self, ctx, code: str):
        """🎁 Redeem gift codes for bonus tokens"""
        try:
            conn = sqlite3.connect("broski_gift_codes.db")
            cursor = conn.cursor()

            # Check if code exists and hasn't been redeemed
            cursor.execute(
                "SELECT * FROM gift_codes WHERE code = ? AND redeemed = FALSE",
                (code.upper(),),
            )

            gift_data = cursor.fetchone()

            if gift_data:
                # Mark as redeemed
                cursor.execute(
                    "UPDATE gift_codes SET redeemed = TRUE WHERE code = ?",
                    (code.upper(),),
                )

                # Award bonus tokens
                bonus_amount = random.uniform(50.0, 100.0)
                self.token_engine.award_tokens(
                    str(ctx.author.id), bonus_amount, f"🎁 Gift code redeemed: {code}"
                )

                redeem_embed = discord.Embed(
                    title="🎁 Gift Code Redeemed!",
                    description=f"Success! You've received **{bonus_amount:.1f} BROski$**!",
                    color=0x00FF00,
                )

                await ctx.send(embed=redeem_embed)

            else:
                await ctx.send("❌ Invalid or already redeemed gift code!")

            conn.commit()
            conn.close()

        except Exception as e:
            await ctx.send(f"❌ Error redeeming gift code: {e}")

    @commands.command(name="power_surge")
    @commands.has_permissions(administrator=True)
    async def power_surge(self, ctx, amount: float = 50.0):
        """💥 Send surge of BROski$ to random online member"""
        online_members = [
            member
            for member in ctx.guild.members
            if member.status != discord.Status.offline and not member.bot
        ]

        if online_members:
            lucky_member = random.choice(online_members)

            # Award surge tokens
            self.token_engine.award_tokens(
                str(lucky_member.id), amount, "💥 Power Surge reward!"
            )

            surge_embed = discord.Embed(
                title="💥 POWER SURGE ACTIVATED!",
                description=f"⚡ {lucky_member.mention} has been struck by lightning and received **{amount} BROski$**!",
                color=0xFFFF00,
            )

            await ctx.send(embed=surge_embed)

            # DM the lucky winner
            try:
                winner_embed = discord.Embed(
                    title="⚡ You've Been Power Surged!",
                    description=f"You randomly received **{amount} BROski$** from the universe!",
                    color=0xFFFF00,
                )
                await lucky_member.send(embed=winner_embed)
            except discord.Forbidden:
                pass

        else:
            await ctx.send("❌ No online members to surge!")


# Setup function for the bot
async def setup(bot):
    await bot.add_cog(BROskiDiscordManager(bot))
