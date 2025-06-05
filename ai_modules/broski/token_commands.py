"""
🪙 BROski$ Token Commands - Discord Integration
Token economy commands for the BROski ClanVerse Ultra system
"""

from datetime import datetime
from typing import Dict, Optional

import discord

from .token_engine import BROskiTokenEngine


class BROskiTokenCommands:
    """🪙 BROski$ Token Commands for Discord Integration"""

    def __init__(self) -> None:
        self.token_engine = BROskiTokenEngine()

    async def handle_balance_command(
        self, user_id: str, username: Optional[str] = None
    ) -> Dict:
        """Handle !balance command"""
        balance = self.token_engine.get_balance(user_id)

        if username:
            display_name = username
        else:
            display_name = f"User {user_id[:8]}"

        return {
            "success": True,
            "balance": balance,
            "message": (
                f"💰 {display_name}'s BROski$ Balance: " f"**{balance:.1f}** tokens"
            ),
        }

    async def handle_send_command(
        self, from_user: str, to_user: str, amount: float, description: str = ""
    ) -> Dict:
        """Handle !send command"""
        try:
            amount = float(amount)
            if amount <= 0:
                return {"success": False, "error": "Amount must be positive"}

            result = self.token_engine.transfer_tokens(
                from_user, to_user, amount, description
            )

            if result["status"] == "success":
                return {
                    "success": True,
                    "message": f"🎉 Successfully sent {amount} BROski$ tokens!",
                    "tx_hash": result["tx_id"],
                }
            else:
                return {"success": False, "error": result["message"]}

        except ValueError:
            return {"success": False, "error": "Invalid amount specified"}

    async def handle_wallet_command(self, user_id: str) -> Dict:
        """Handle !wallet command"""
        # Check if wallet exists
        balance = self.token_engine.get_balance(user_id)

        if balance == 0:
            # Create new wallet (using _create_wallet since it's private)
            self.token_engine._create_wallet(user_id)
            # Award welcome bonus
            self.token_engine.award_tokens(user_id, 10.0, "Welcome bonus!")
            return {
                "success": True,
                "balance": 10.0,
                "message": (
                    "💳 Welcome to BROski$ ClanVerse! "
                    "Your wallet is ready with 10 welcome tokens! 🎉"
                ),
            }
        else:
            # Get wallet info
            return {
                "success": True,
                "balance": balance,
                "message": (
                    f"💳 Your BROski$ wallet is active with " f"{balance:.1f} tokens!"
                ),
            }

    async def handle_leaderboard_command(self, limit: int = 10) -> Dict:
        """Handle !leaderboard command"""
        leaderboard = self.token_engine.get_leaderboard(limit)

        leaderboard_text = "🏆 **BROski$ ClanVerse Leaderboard** 🏆\n\n"

        for i, entry in enumerate(leaderboard, 1):
            rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "🔹")
            leaderboard_text += (
                f"{rank_emoji} **#{i}** - " f"{entry['balance']:.1f} BROski$\n"
            )

        return {
            "success": True,
            "leaderboard": leaderboard,
            "message": leaderboard_text,
        }

    async def handle_history_command(self, user_id: str, limit: int = 5) -> Dict:
        """Handle !history command - simplified version"""
        # Since get_transaction_history doesn't exist, create simple history
        balance = self.token_engine.get_balance(user_id)

        if balance == 0:
            return {
                "success": True,
                "message": (
                    "📋 No transaction history found. "
                    "Start earning BROski$ by being awesome! 🌟"
                ),
            }

        # Simple transaction summary
        history_text = "📋 **Your BROski$ Transaction Summary** 📋\n\n"
        history_text += f"💰 Current Balance: {balance:.1f} BROski$\n"
        history_text += "🎯 Keep earning by participating in the community!\n"

        return {"success": True, "message": history_text}

    async def handle_stats_command(self) -> Dict:
        """Handle !tokenstats command - simplified version"""
        # Since get_system_stats doesn't exist, create basic stats
        total_supply = self.token_engine.get_total_supply()
        circulating = self.token_engine.get_circulating_supply()

        stats_message = f"""
🪙 **BROski$ ClanVerse Token Statistics** 🪙

🔄 **Total Supply**: {total_supply:.1f} BROski$
💎 **Circulating**: {circulating:.1f} BROski$
🟢 **System Status**: Operational

*Building the future of neurodivergent productivity, one token at a time!* 🚀
"""

        return {"success": True, "message": stats_message}

    async def award_activity_tokens(
        self, user_id: str, activity_type: str
    ) -> Optional[Dict]:
        """Award tokens for various activities"""
        activity_rewards = {
            "helpful_message": 2.0,
            "creative_share": 3.0,
            "question_answer": 1.5,
            "community_support": 2.5,
            "daily_checkin": 1.0,
            "hyperfocus_session": 5.0,
            "goal_completion": 4.0,
            "positive_vibes": 1.0,
        }

        amount = activity_rewards.get(activity_type, 0)
        if amount <= 0:
            return None

        activity_descriptions = {
            "helpful_message": "Being helpful to the community! 🤝",
            "creative_share": "Sharing your creative work! 🎨",
            "question_answer": "Answering questions! 🧠",
            "community_support": "Supporting community members! 💜",
            "daily_checkin": "Daily check-in completed! ☀️",
            "hyperfocus_session": "Completing a hyperfocus session! 🎯",
            "goal_completion": "Achieving your goals! 🏆",
            "positive_vibes": "Spreading positive energy! ✨",
        }

        description = activity_descriptions.get(
            activity_type, "Community participation"
        )

        result = self.token_engine.award_tokens(user_id, amount, description)

        if result["status"] == "success":
            return {
                "success": True,
                "amount": amount,
                "activity": activity_type,
                "message": f"🎉 Earned {amount} BROski$ for {description}",
            }

        return None

    async def create_reward_embed(
        self, reward_info: Dict, user_mention: Optional[str] = None
    ) -> discord.Embed:
        """Create Discord embed for reward notifications"""
        embed = discord.Embed(
            title="🪙 BROski$ Token Reward!",
            description=reward_info["message"],
            color=0x00FF88,
            timestamp=datetime.now(),
        )

        if user_mention:
            embed.add_field(name="🎯 Awarded To", value=user_mention, inline=True)

        embed.add_field(
            name="💰 Amount", value=f"{reward_info['amount']} BROski$", inline=True
        )

        if "daily_remaining" in reward_info:
            embed.add_field(
                name="📅 Daily Remaining",
                value=f"{reward_info['daily_remaining']} BROski$",
                inline=True,
            )

        embed.set_footer(text="BROski$ ClanVerse Ultra • Neurodivergent Token Economy")

        return embed

    async def create_balance_embed(
        self, balance_info: Dict, user_mention: Optional[str] = None
    ) -> discord.Embed:
        """Create Discord embed for balance display"""
        embed = discord.Embed(
            title="💰 BROski$ Wallet Balance",
            description=balance_info["message"],
            color=0x3498DB,
            timestamp=datetime.now(),
        )

        if user_mention:
            embed.add_field(name="👤 Wallet Owner", value=user_mention, inline=True)

        embed.add_field(
            name="💳 Current Balance",
            value=f"{balance_info['balance']:.1f} BROski$",
            inline=True,
        )

        # Add motivational message based on balance
        if balance_info["balance"] >= 100:
            motivation = "🚀 Token legend! You're building wealth!"
        elif balance_info["balance"] >= 50:
            motivation = "⚡ Great progress! Keep earning!"
        elif balance_info["balance"] >= 10:
            motivation = "🌱 Growing your stash! Nice work!"
        else:
            motivation = "🎯 Just getting started! Every token counts!"

        embed.add_field(name="💫 Status", value=motivation, inline=False)

        embed.set_footer(
            text="BROski$ ClanVerse Ultra • Your neurodivergent token journey"
        )

        return embed

    async def create_leaderboard_embed(self, leaderboard_info: Dict) -> discord.Embed:
        """Create Discord embed for leaderboard"""
        embed = discord.Embed(
            title="🏆 BROski$ ClanVerse Leaderboard",
            description="Top token holders in our neurodivergent community!",
            color=0xFFD700,
            timestamp=datetime.now(),
        )

        leaderboard_text = ""
        for i, entry in enumerate(leaderboard_info["leaderboard"][:10], 1):
            rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "🔹")
            leaderboard_text += (
                f"{rank_emoji} **#{i}** - " f"{entry['balance']:.1f} BROski$\n"
            )

        embed.add_field(
            name="🏅 Top Earners",
            value=leaderboard_text or "No data available",
            inline=False,
        )

        embed.add_field(
            name="🎯 How to Climb",
            value=(
                "• Be helpful and supportive\n"
                "• Complete hyperfocus sessions\n"
                "• Share your creative work\n"
                "• Spread positive vibes!"
            ),
            inline=False,
        )

        embed.set_footer(text="BROski$ ClanVerse Ultra • Community Excellence Rewards")

        return embed
