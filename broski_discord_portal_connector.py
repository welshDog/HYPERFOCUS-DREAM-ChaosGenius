#!/usr/bin/env python3
"""
🎮🚀 BROSKI DISCORD PORTAL CONNECTOR - ULTIMATE EDITION 🚀🎮
Connect Discord to Unlock Full Portal + BROski$ Upgrade Sales System
By Command of Chief Lyndz - BROski∞ Empire Edition

LEGENDARY FEATURES:
🔗 Official Discord Server Connection: https://discord.gg/chyXCC4zj2
💰 BROski$ Upgrade Purchase System
🎯 Portal Unlock Authentication
⚡ Real-time Token Balance Integration
🛡️ Secure OAuth2 Flow
"""

import asyncio
import json
import logging
import os
import sqlite3

# Import BROski$ token system
import sys
from datetime import datetime, timedelta
from typing import Dict, Optional

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

sys.path.append("/root/chaosgenius")
from ai_modules.broski.token_engine import BROskiTokenEngine
from broski_oauth2_manager import BROskiOAuth2Manager

load_dotenv()

# 🔥 OFFICIAL BROSKI DISCORD SERVER
OFFICIAL_DISCORD_INVITE = "https://discord.gg/chyXCC4zj2"
PORTAL_UNLOCK_COST = 100.0  # BROski$ cost to unlock full portal


class BROskiDiscordPortalConnector:
    """🎮 Ultimate Discord Portal Connection & Upgrade System"""

    def __init__(self):
        self.token_engine = BROskiTokenEngine()
        self.oauth_manager = BROskiOAuth2Manager()
        self.connected_users = {}
        self.pending_upgrades = {}

        # Portal upgrade tiers
        self.upgrade_tiers = {
            "basic_portal": {
                "name": "🌟 Basic Portal Access",
                "cost": 100,
                "description": "Unlock basic portal features + Discord integration",
                "features": [
                    "📊 Basic Dashboard Access",
                    "🤖 3 AI Agent Slots",
                    "💎 Memory Crystal Storage",
                    "🎯 Focus Session Tracking",
                ],
            },
            "premium_portal": {
                "name": "🚀 Premium Portal Experience",
                "cost": 500,
                "description": "Full portal access + exclusive Discord perks",
                "features": [
                    "🌟 All Basic Features",
                    "🤖 15+ AI Agent Army",
                    "🛡️ Guardian Zero Protection",
                    "💰 Money Maker Agent",
                    "📈 Advanced Analytics",
                    "🎮 Gaming Mode Interface",
                ],
            },
            "legendary_portal": {
                "name": "👑 LEGENDARY Portal Empire",
                "cost": 2000,
                "description": "Ultimate BROski experience + founder perks",
                "features": [
                    "🚀 All Premium Features",
                    "⚡ Real-time Neural Bus Connection",
                    "🧬 BRAINVERSE Link Access",
                    "💎 Exclusive Founder Channels",
                    "🎯 Personal BROski AI Mentor",
                    "🌟 Custom Portal Themes",
                    "👑 Direct Founder Access",
                ],
            },
        }

        # Setup database
        self.setup_database()

    def setup_database(self):
        """Initialize portal connection database"""
        conn = sqlite3.connect("broski_portal_connections.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS portal_connections (
                user_id TEXT PRIMARY KEY,
                discord_id TEXT UNIQUE,
                username TEXT,
                portal_tier TEXT DEFAULT 'none',
                connection_date TEXT,
                last_active TEXT,
                total_spent REAL DEFAULT 0.0,
                upgrades_purchased TEXT DEFAULT '[]',
                special_perks TEXT DEFAULT '[]'
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS upgrade_transactions (
                tx_id TEXT PRIMARY KEY,
                user_id TEXT,
                upgrade_tier TEXT,
                cost REAL,
                timestamp TEXT,
                status TEXT,
                payment_method TEXT DEFAULT 'broski_tokens'
            )
        """
        )

        conn.commit()
        conn.close()

    async def connect_discord_portal(self, user_id: str, discord_user: dict) -> Dict:
        """🔗 Connect user's Discord to unlock portal access"""
        try:
            # Check if user has enough tokens for basic portal
            balance = self.token_engine.get_balance(user_id)

            if balance < PORTAL_UNLOCK_COST:
                return {
                    "success": False,
                    "error": f"Insufficient BROski$ tokens! Need {PORTAL_UNLOCK_COST}, you have {balance}",
                    "invite_link": OFFICIAL_DISCORD_INVITE,
                    "message": "💰 Earn more BROski$ in our Discord server to unlock portal access!",
                }

            # Deduct portal unlock cost
            result = self.token_engine.spend_tokens(
                user_id, PORTAL_UNLOCK_COST, "🔗 Discord Portal Connection Unlock"
            )

            if not result["success"]:
                return {"success": False, "error": result["message"]}

            # Save connection to database
            conn = sqlite3.connect("broski_portal_connections.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO portal_connections
                (user_id, discord_id, username, portal_tier, connection_date, last_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    discord_user.get("id"),
                    discord_user.get("username"),
                    "basic_portal",
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ),
            )

            conn.commit()
            conn.close()

            # Store in memory for quick access
            self.connected_users[user_id] = {
                "discord_id": discord_user.get("id"),
                "username": discord_user.get("username"),
                "tier": "basic_portal",
                "connected_at": datetime.now(),
            }

            return {
                "success": True,
                "message": "🎉 PORTAL ACCESS UNLOCKED!",
                "tier": "basic_portal",
                "remaining_balance": balance - PORTAL_UNLOCK_COST,
                "portal_url": "https://hyperfocuszone.com/portal",
                "discord_perks": [
                    "🎮 Access to #broski-portal channel",
                    "🤖 Personal AI agent commands",
                    "💎 Daily BROski$ rewards",
                    "🏆 Exclusive role: Portal User",
                ],
            }

        except Exception as e:
            logging.error(f"Portal connection error: {e}")
            return {
                "success": False,
                "error": "Portal connection failed. Please try again!",
            }

    async def purchase_upgrade(self, user_id: str, upgrade_tier: str) -> Dict:
        """💰 Purchase portal upgrade with BROski$ tokens"""
        try:
            if upgrade_tier not in self.upgrade_tiers:
                return {"success": False, "error": "Invalid upgrade tier!"}

            upgrade_info = self.upgrade_tiers[upgrade_tier]
            cost = upgrade_info["cost"]

            # Check user balance
            balance = self.token_engine.get_balance(user_id)

            if balance < cost:
                return {
                    "success": False,
                    "error": f"Insufficient BROski$ tokens! Need {cost}, you have {balance}",
                    "message": "💰 Earn more tokens in Discord to afford this upgrade!",
                }

            # Process payment
            payment_result = self.token_engine.spend_tokens(
                user_id, cost, f"🚀 Portal Upgrade: {upgrade_info['name']}"
            )

            if not payment_result["success"]:
                return {"success": False, "error": payment_result["message"]}

            # Update user's portal tier
            conn = sqlite3.connect("broski_portal_connections.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE portal_connections
                SET portal_tier = ?, total_spent = total_spent + ?, last_active = ?
                WHERE user_id = ?
            """,
                (upgrade_tier, cost, datetime.now().isoformat(), user_id),
            )

            # Record transaction
            tx_id = f"upgrade_{user_id}_{int(datetime.now().timestamp())}"
            cursor.execute(
                """
                INSERT INTO upgrade_transactions
                (tx_id, user_id, upgrade_tier, cost, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    tx_id,
                    user_id,
                    upgrade_tier,
                    cost,
                    datetime.now().isoformat(),
                    "completed",
                ),
            )

            conn.commit()
            conn.close()

            # Update memory cache
            if user_id in self.connected_users:
                self.connected_users[user_id]["tier"] = upgrade_tier

            return {
                "success": True,
                "message": f"🎉 UPGRADE SUCCESSFUL! Welcome to {upgrade_info['name']}!",
                "tier": upgrade_tier,
                "features_unlocked": upgrade_info["features"],
                "remaining_balance": balance - cost,
                "tx_id": tx_id,
                "special_perks": self._get_tier_perks(upgrade_tier),
            }

        except Exception as e:
            logging.error(f"Upgrade purchase error: {e}")
            return {
                "success": False,
                "error": "Upgrade purchase failed. Please try again!",
            }

    def _get_tier_perks(self, tier: str) -> list:
        """Get special Discord perks for each tier"""
        perks = {
            "basic_portal": [
                "🎮 Access to #broski-portal",
                "🤖 Basic AI commands",
                "💎 5 BROski$/day rewards",
            ],
            "premium_portal": [
                "🚀 Access to #premium-zone",
                "🤖 Full AI Agent Army",
                "💎 15 BROski$/day rewards",
                "🎯 Priority support",
                "🎮 Gaming mode channels",
            ],
            "legendary_portal": [
                "👑 Access to #founder-lounge",
                "🧬 BRAINVERSE channels",
                "💎 50 BROski$/day rewards",
                "⚡ Direct founder chat",
                "🌟 Custom commands",
                "🎯 VIP everything",
            ],
        }
        return perks.get(tier, [])

    async def get_user_portal_status(self, user_id: str) -> Dict:
        """📊 Get user's current portal status and available upgrades"""
        try:
            # Check database
            conn = sqlite3.connect("broski_portal_connections.db")
            cursor = conn.cursor()

            user_data = cursor.execute(
                "SELECT * FROM portal_connections WHERE user_id = ?", (user_id,)
            ).fetchone()

            conn.close()

            if not user_data:
                return {
                    "connected": False,
                    "message": "🔗 Connect your Discord to unlock portal access!",
                    "discord_invite": OFFICIAL_DISCORD_INVITE,
                    "unlock_cost": PORTAL_UNLOCK_COST,
                }

            current_tier = user_data[3]  # portal_tier column
            balance = self.token_engine.get_balance(user_id)

            # Get available upgrades
            available_upgrades = []
            for tier_key, tier_info in self.upgrade_tiers.items():
                if tier_key != current_tier and tier_info["cost"] <= balance:
                    available_upgrades.append(
                        {
                            "tier": tier_key,
                            "name": tier_info["name"],
                            "cost": tier_info["cost"],
                            "description": tier_info["description"],
                            "affordable": True,
                        }
                    )
                elif tier_key != current_tier:
                    available_upgrades.append(
                        {
                            "tier": tier_key,
                            "name": tier_info["name"],
                            "cost": tier_info["cost"],
                            "description": tier_info["description"],
                            "affordable": False,
                        }
                    )

            return {
                "connected": True,
                "current_tier": current_tier,
                "tier_info": self.upgrade_tiers.get(current_tier, {}),
                "current_perks": self._get_tier_perks(current_tier),
                "balance": balance,
                "available_upgrades": available_upgrades,
                "total_spent": user_data[5],  # total_spent column
                "member_since": user_data[4],  # connection_date column
            }

        except Exception as e:
            logging.error(f"Portal status error: {e}")
            return {"connected": False, "error": "Could not retrieve portal status"}

    async def generate_discord_connection_embed(self) -> discord.Embed:
        """🎨 Generate beautiful Discord connection embed"""
        embed = discord.Embed(
            title="🎮 CONNECT DISCORD TO UNLOCK FULL PORTAL 🎮",
            description="Join the BROski Empire and unlock your personalized portal experience!",
            color=0x9966FF,
            url=OFFICIAL_DISCORD_INVITE,
        )

        embed.add_field(
            name="🔗 Official BROski Discord Server",
            value=f"[🚀 JOIN NOW: {OFFICIAL_DISCORD_INVITE}]({OFFICIAL_DISCORD_INVITE})",
            inline=False,
        )

        embed.add_field(
            name="💰 Portal Unlock Cost",
            value=f"{PORTAL_UNLOCK_COST} BROski$ tokens",
            inline=True,
        )

        embed.add_field(
            name="🎯 What You Get",
            value="🤖 AI Agent Army\n💎 Memory Crystals\n🛡️ Guardian Zero\n📊 Analytics Dashboard",
            inline=True,
        )

        embed.add_field(
            name="🚀 Available Upgrades",
            value=f"🌟 Basic Portal: {self.upgrade_tiers['basic_portal']['cost']} BROski$\n🚀 Premium: {self.upgrade_tiers['premium_portal']['cost']} BROski$\n👑 Legendary: {self.upgrade_tiers['legendary_portal']['cost']} BROski$",
            inline=False,
        )

        embed.set_footer(text="💎 Earn BROski$ tokens by being active in Discord!")

        return embed

    async def generate_upgrade_shop_embed(self, user_status: Dict) -> discord.Embed:
        """🛒 Generate upgrade shop embed for user"""
        embed = discord.Embed(
            title="🛒 BROSKI PORTAL UPGRADE SHOP 🛒",
            description="Spend your BROski$ tokens to unlock LEGENDARY portal features!",
            color=0x00FF88,
        )

        embed.add_field(
            name="💰 Your Balance",
            value=f"{user_status.get('balance', 0)} BROski$",
            inline=True,
        )

        embed.add_field(
            name="🏆 Current Tier",
            value=user_status.get("current_tier", "None").replace("_", " ").title(),
            inline=True,
        )

        # Show available upgrades
        for upgrade in user_status.get("available_upgrades", []):
            affordable_emoji = "✅" if upgrade["affordable"] else "❌"
            embed.add_field(
                name=f"{affordable_emoji} {upgrade['name']}",
                value=f"💰 Cost: {upgrade['cost']} BROski$\n📝 {upgrade['description']}",
                inline=False,
            )

        embed.set_footer(text="💎 Use /buy-upgrade [tier] to purchase!")

        return embed


# Export the connector for Discord bot integration
__all__ = ["BROskiDiscordPortalConnector", "OFFICIAL_DISCORD_INVITE"]
