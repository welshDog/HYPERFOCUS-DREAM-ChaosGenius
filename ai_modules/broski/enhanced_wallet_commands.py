#!/usr/bin/env python3
"""
🎮💰 BROski$ Enhanced Wallet Commands - ULTRA DISCORD EDITION
Advanced Discord commands for the BROski$ ecosystem

New Commands:
- /shop - Browse and purchase rewards
- /daily - Claim daily streak rewards
- /rank - BROski$ leaderboard rankings
- /tip - Quick tip other users
- /vault - Security settings
"""

import asyncio
import json
import random

# Fix imports to use correct module paths
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import discord
from discord.ext import commands

sys.path.append("/root/chaosgenius")
from ai_modules.broski.token_engine import BROskiTokenEngine
from broski_secure_wallet_manager import BROskiSecureWalletManager


class BROskiEnhancedWalletCommands:
    """🎮 Enhanced wallet commands for Discord integration"""

    def __init__(self):
        self.token_engine = BROskiTokenEngine()
        self.wallet_manager = BROskiSecureWalletManager()
        self.daily_rewards = {}

        # Shop items configuration
        self.shop_items = {
            "discord_boost": {
                "name": "🚀 Discord Boost Badge",
                "price": 25,
                "description": "Show off your BROski$ wealth!",
                "type": "badge",
            },
            "custom_role": {
                "name": "🎨 Custom Role Color",
                "price": 50,
                "description": "Pick your own role color!",
                "type": "role",
            },
            "vip_access": {
                "name": "💎 VIP Channel Access",
                "price": 100,
                "description": "Access exclusive VIP channels",
                "type": "access",
            },
            "adhd_focus_session": {
                "name": "🧠 Personal Focus Session",
                "price": 75,
                "description": "1-on-1 ADHD productivity coaching",
                "type": "service",
            },
            "chaos_organize": {
                "name": "🌪️ Chaos Organization Service",
                "price": 60,
                "description": "Help organize your scattered thoughts",
                "type": "service",
            },
        }

    async def handle_wallet_command(self, user_id: str) -> Dict:
        """Handle basic wallet info command"""
        try:
            balance = self.token_engine.get_balance(user_id)

            return {
                "success": True,
                "message": f"💰 Your BROski$ Balance: {balance:.2f}",
                "balance": balance,
            }

        except Exception as e:
            return {"success": False, "error": f"Wallet error: {str(e)}"}

    async def handle_shop_command(self, user_id: str) -> Dict:
        """Handle /shop command - browse available rewards"""
        try:
            balance = self.token_engine.get_balance(user_id)

            shop_display = "🛒 **BROski$ ULTRA SHOP** 🛒\n\n"
            shop_display += f"💰 Your Balance: **{balance:.1f} BROski$**\n\n"

            for item_id, item in self.shop_items.items():
                affordable = "✅" if balance >= item["price"] else "❌"
                shop_display += f"{affordable} **{item['name']}**\n"
                shop_display += (
                    f"   💲 {item['price']} BROski$ - {item['description']}\n"
                )
                shop_display += f"   Use: `/buy {item_id}`\n\n"

            return {"success": True, "message": shop_display, "balance": balance}

        except Exception as e:
            return {"success": False, "error": f"Shop error: {str(e)}"}

    async def handle_daily_command(self, user_id: str) -> Dict:
        """Handle /daily command - claim daily streak rewards"""
        try:
            today = datetime.now().date().isoformat()
            user_daily_data = self.daily_rewards.get(user_id, {})

            last_claim = user_daily_data.get("last_claim")
            streak = user_daily_data.get("streak", 0)

            if last_claim == today:
                return {
                    "success": False,
                    "message": "⏰ You've already claimed your daily reward today! Come back tomorrow! 🌅",
                }

            # Calculate streak
            yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
            if last_claim == yesterday:
                streak += 1
            else:
                streak = 1

            # Calculate reward based on streak
            base_reward = 10
            streak_bonus = min(streak * 2, 50)  # Max 50 bonus
            total_reward = base_reward + streak_bonus

            # Award tokens
            result = self.token_engine.award_tokens(
                user_id, total_reward, f"Daily reward - Day {streak}"
            )

            # Update daily data
            self.daily_rewards[user_id] = {"last_claim": today, "streak": streak}

            streak_emoji = "🔥" * min(streak, 10)

            return {
                "success": True,
                "message": f"🎉 **DAILY REWARD CLAIMED!** 🎉\n\n"
                f"💰 +{total_reward} BROski$ earned!\n"
                f"{streak_emoji} Streak: {streak} days\n"
                f"🎯 Next reward in 24 hours!",
                "reward": total_reward,
                "streak": streak,
            }

        except Exception as e:
            return {"success": False, "error": f"Daily reward error: {str(e)}"}

    async def handle_rank_command(self, limit: int = 10) -> Dict:
        """Handle /rank command - show BROski$ leaderboard"""
        try:
            # Get top users from token engine
            leaderboard_data = self.token_engine.get_leaderboard(limit)

            rank_display = "🏆 **BROski$ ULTRA LEADERBOARD** 🏆\n\n"

            medals = ["🥇", "🥈", "🥉"]
            for i, user_data in enumerate(leaderboard_data[:limit]):
                medal = medals[i] if i < 3 else f"{i+1}."
                username = user_data.get("username", f"User#{user_data['user_id'][:8]}")
                balance = user_data["balance"]

                rank_display += f"{medal} **{username}** - {balance:.1f} BROski$\n"

            rank_display += "\n💪 Keep earning to climb the ranks!"

            return {
                "success": True,
                "message": rank_display,
                "leaderboard": leaderboard_data,
            }

        except Exception as e:
            return {"success": False, "error": f"Leaderboard error: {str(e)}"}

    async def handle_send_command(
        self, from_user: str, to_user: str, amount: float, message: str = ""
    ) -> Dict:
        """Handle send tokens command"""
        try:
            if amount <= 0:
                return {"success": False, "error": "Amount must be positive!"}

            # Check balance
            balance = self.token_engine.get_balance(from_user)
            if balance < amount:
                return {
                    "success": False,
                    "error": f"Insufficient balance! You have {balance:.1f} BROski$",
                }

            # Execute transfer
            result = self.token_engine.transfer_tokens(
                from_user,
                to_user,
                amount,
                f"Transfer: {message}" if message else "Token transfer",
            )

            if result["status"] == "success":
                return {
                    "success": True,
                    "message": (
                        f"💸 **TRANSFER SUCCESSFUL!** 💸\n\n"
                        f"💰 {amount} BROski$ sent to {to_user}!\n"
                        f"📝 Note: {message}"
                        if message
                        else ""
                    ),
                    "amount": amount,
                }
            else:
                return {"success": False, "error": result["message"]}

        except Exception as e:
            return {"success": False, "error": f"Transfer error: {str(e)}"}

    async def handle_tip_command(
        self, from_user: str, to_user: str, amount: float, message: str = ""
    ) -> Dict:
        """Handle /tip command - quick tip other users"""
        try:
            if amount <= 0:
                return {"success": False, "error": "Tip amount must be positive!"}

            if amount < 1:
                return {"success": False, "error": "Minimum tip is 1 BROski$!"}

            # Check balance
            balance = self.token_engine.get_balance(from_user)
            if balance < amount:
                return {
                    "success": False,
                    "error": f"Insufficient balance! You have {balance:.1f} BROski$",
                }

            # Add tip bonus (10% extra to recipient)
            tip_bonus = amount * 0.1
            total_to_recipient = amount + tip_bonus

            # Execute transfer
            result = self.token_engine.transfer_tokens(
                from_user,
                to_user,
                amount,
                f"Tip: {message}" if message else "Friendly tip",
            )

            if result["status"] == "success":
                # Award bonus
                self.token_engine.award_tokens(to_user, tip_bonus, "Tip bonus (10%)")

                return {
                    "success": True,
                    "message": (
                        f"💝 **TIP SENT!** 💝\n\n"
                        f"💰 {amount} BROski$ sent!\n"
                        f"🎁 +{tip_bonus:.1f} bonus for recipient!\n"
                        f"💫 Total received: {total_to_recipient:.1f} BROski$\n"
                        f"📝 Note: {message}"
                        if message
                        else ""
                    ),
                    "amount": amount,
                    "bonus": tip_bonus,
                }
            else:
                return {"success": False, "error": result["message"]}

        except Exception as e:
            return {"success": False, "error": f"Tip error: {str(e)}"}

    async def handle_vault_command(self, user_id: str) -> Dict:
        """Handle /vault command - show wallet security settings"""
        try:
            wallet_info = self.wallet_manager.get_wallet_info(user_id)

            if not wallet_info["success"]:
                return {"success": False, "error": "Wallet not found!"}

            wallet = wallet_info["wallet"]

            vault_display = "🛡️ **YOUR SECURITY VAULT** 🛡️\n\n"
            vault_display += f"📍 **Address:** `{wallet['address'][:10]}...{wallet['address'][-6:]}`\n"
            vault_display += f"🔐 **Security Level:** {wallet['security_level']}/5\n"
            vault_display += (
                f"💳 **Daily Limit:** {wallet['spending_limit_daily']} BROski$\n"
            )
            vault_display += f"💸 **Transaction Limit:** {wallet['spending_limit_transaction']} BROski$\n"
            vault_display += f"🔒 **2FA Enabled:** {'✅ Yes' if wallet['two_factor_enabled'] else '❌ No'}\n"
            vault_display += (
                f"📊 **Recent Transactions:** {wallet['recent_transactions']}\n"
            )
            vault_display += f"📅 **Created:** {wallet['created_at'][:10]}\n\n"
            vault_display += "💡 Use `/security upgrade` to enhance protection!"

            return {"success": True, "message": vault_display, "wallet_info": wallet}

        except Exception as e:
            return {"success": False, "error": f"Vault error: {str(e)}"}

    async def handle_buy_command(self, user_id: str, item_id: str) -> Dict:
        """Handle /buy command - purchase shop items"""
        try:
            if item_id not in self.shop_items:
                return {"success": False, "error": "Item not found in shop!"}

            item = self.shop_items[item_id]
            balance = self.token_engine.get_balance(user_id)

            if balance < item["price"]:
                return {
                    "success": False,
                    "error": f"Insufficient funds! Need {item['price']} BROski$, you have {balance:.1f}",
                }

            # Deduct tokens
            result = self.token_engine.transfer_tokens(
                user_id, "SHOP_SYSTEM", item["price"], f"Purchased: {item['name']}"
            )

            if result["status"] == "success":
                return {
                    "success": True,
                    "message": f"🛒 **PURCHASE SUCCESSFUL!** 🛒\n\n"
                    f"✅ {item['name']} purchased!\n"
                    f"💰 -{item['price']} BROski$\n"
                    f"💼 Item will be activated shortly!\n\n"
                    f"📧 Check your DMs for instructions!",
                    "item": item,
                    "cost": item["price"],
                }
            else:
                return {"success": False, "error": "Purchase failed!"}

        except Exception as e:
            return {"success": False, "error": f"Purchase error: {str(e)}"}

    async def handle_history_command(self, user_id: str, limit: int = 10) -> Dict:
        """Handle transaction history command"""
        try:
            # Get transaction history from token engine
            transactions = self.token_engine.get_user_transactions(user_id, limit)

            return {
                "success": True,
                "transactions": transactions,
                "message": f"📊 Recent {len(transactions)} transactions",
            }

        except Exception as e:
            return {"success": False, "error": f"History error: {str(e)}"}

    async def handle_leaderboard_command(self, limit: int = 10) -> Dict:
        """Handle leaderboard command"""
        return await self.handle_rank_command(limit)


# Export for Discord bot integration
__all__ = ["BROskiEnhancedWalletCommands"]
