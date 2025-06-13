#!/usr/bin/env python3
"""
🚀💥 BROSKI DISCORD INTERACTIONS ENDPOINT 💥🚀
HTTP POST-based Discord interactions instead of Gateway connection
LEGENDARY webhook system with agent army integration!
By Command of Chief Lyndz - BROski∞ Webhook Edition
"""

import hashlib
import hmac
import json
import os
import random
import sqlite3
import time
from datetime import datetime
from typing import Any, Dict, Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from flask import Flask, jsonify, request

# Import existing systems
try:
    from broski_oauth2_manager import BROskiOAuth2Manager
    from super_ai_agent_orchestrator import get_orchestrator

    ORCHESTRATOR_AVAILABLE = True
except ImportError:
    ORCHESTRATOR_AVAILABLE = False

if load_dotenv:
    load_dotenv()


class BROskiInteractionsEndpoint:
    """🚀 LEGENDARY Discord Interactions Webhook Handler"""

    def __init__(self, app: Flask):
        self.app = app
        self.public_key = os.getenv("PUBLIC_KEY")
        self.app_id = os.getenv("DISCORD_APPLICATION_ID")
        self.db_path = "/root/chaosgenius/fresh_broski_bot.db"

        # Agent orchestrator integration
        if ORCHESTRATOR_AVAILABLE:
            self.orchestrator = get_orchestrator()
            print("🤖 Agent Orchestrator connected to interactions endpoint!")

        # Register webhook endpoint
        self.setup_webhook_routes()

        # Initialize command handlers
        self.command_handlers = {
            "fresh_start": self.handle_fresh_start,
            "agent_assist": self.handle_agent_assist,
            "focus_mode": self.handle_focus_mode,
            "daily_boost": self.handle_daily_boost,
            "wallet": self.handle_wallet,
            "agent_status": self.handle_agent_status,
            "cosmic_transform": self.handle_cosmic_transform,
        }

    def verify_signature(self, signature: str, timestamp: str, body: bytes) -> bool:
        """🔐 Verify Discord webhook signature"""
        if not self.public_key:
            print("⚠️ No public key configured for signature verification")
            return True  # Skip verification in development

        try:
            # Discord signature verification
            message = timestamp.encode() + body
            expected = hmac.new(
                bytes.fromhex(self.public_key), message, hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(signature, expected)
        except Exception as e:
            print(f"❌ Signature verification error: {e}")
            return False

    def setup_webhook_routes(self):
        """🎯 Setup webhook routes in Flask app"""

        @self.app.route("/discord/interactions", methods=["POST"])
        def handle_discord_interaction():
            """🤖 Main Discord interactions webhook endpoint"""

            # Get headers
            signature = request.headers.get("X-Signature-Ed25519", "")
            timestamp = request.headers.get("X-Signature-Timestamp", "")

            # Verify signature
            if not self.verify_signature(signature, timestamp, request.data):
                return jsonify({"error": "Invalid signature"}), 401

            # Parse interaction data
            try:
                interaction = request.json
                return self.process_interaction(interaction)
            except Exception as e:
                print(f"❌ Interaction processing error: {e}")
                return jsonify({"error": "Processing failed"}), 500

        @self.app.route("/discord/commands", methods=["GET"])
        def list_discord_commands():
            """📋 List available Discord commands"""
            commands = [
                {
                    "name": "fresh_start",
                    "description": "🚀 Begin your fresh BROski journey!",
                    "type": 1,
                },
                {
                    "name": "agent_assist",
                    "description": "🤖 Get help from the Agent Army!",
                    "type": 1,
                    "options": [
                        {
                            "name": "task",
                            "description": "What do you need help with?",
                            "type": 3,
                            "required": True,
                        }
                    ],
                },
                {
                    "name": "focus_mode",
                    "description": "🧠 Start a hyperfocus productivity session!",
                    "type": 1,
                    "options": [
                        {
                            "name": "project",
                            "description": "What project are you working on?",
                            "type": 3,
                            "required": True,
                        },
                        {
                            "name": "minutes",
                            "description": "How many minutes? (default: 25)",
                            "type": 4,
                            "required": False,
                        },
                    ],
                },
                {
                    "name": "daily_boost",
                    "description": "⚡ Get your daily dopamine boost and tokens!",
                    "type": 1,
                },
                {
                    "name": "wallet",
                    "description": "💰 Check your BROski$ wallet and cosmic status",
                    "type": 1,
                },
                {
                    "name": "agent_status",
                    "description": "📊 Check the Agent Army status",
                    "type": 1,
                },
                {
                    "name": "cosmic_transform",
                    "description": "🌌 Transform your server into a cosmic base!",
                    "type": 1,
                },
            ]

            return jsonify(
                {
                    "commands": commands,
                    "total": len(commands),
                    "endpoint": "/discord/interactions",
                    "status": "LEGENDARY",
                }
            )

    def process_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """🎯 Process Discord interaction"""
        interaction_type = interaction.get("type")

        # Handle different interaction types
        if interaction_type == 1:  # PING
            return {"type": 1}  # PONG

        elif interaction_type == 2:  # APPLICATION_COMMAND
            return self.handle_application_command(interaction)

        elif interaction_type == 3:  # MESSAGE_COMPONENT
            return self.handle_message_component(interaction)

        else:
            return {
                "type": 4,
                "data": {
                    "content": "❌ Unknown interaction type!",
                    "flags": 64,  # Ephemeral
                },
            }

    def handle_application_command(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """⚡ Handle slash command interactions"""
        command_name = interaction["data"]["name"]
        user = (
            interaction["member"]["user"]
            if "member" in interaction
            else interaction["user"]
        )

        # Log the command
        print(f"🎯 Command received: /{command_name} from {user['username']}")

        # Add to agent orchestrator if available
        if ORCHESTRATOR_AVAILABLE:
            self.orchestrator.add_task(
                f"Discord Command: /{command_name} from {user['username']}",
                priority=2,
                complexity=1.0,
            )

        # Route to command handler
        if command_name in self.command_handlers:
            return self.command_handlers[command_name](interaction)
        else:
            return {
                "type": 4,
                "data": {
                    "content": f"❌ Unknown command: `/{command_name}`",
                    "flags": 64,
                },
            }

    def handle_fresh_start(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """🚀 Handle fresh_start command"""
        user = (
            interaction["member"]["user"]
            if "member" in interaction
            else interaction["user"]
        )
        user_id = user["id"]
        username = user["username"]

        # Get or create user data
        user_data = self.get_or_create_user(user_id, username)

        embed = {
            "title": "🚀💥 FRESH BROSKI JOURNEY INITIATED! 💥🚀",
            "description": "Welcome to your LEGENDARY productivity empire!",
            "color": 0x00FF88,
            "fields": [
                {
                    "name": "💎 Your BROski$ Balance",
                    "value": f"{user_data['broski_tokens']} tokens",
                    "inline": True,
                },
                {
                    "name": "🏆 Cosmic Rank",
                    "value": user_data["cosmic_rank"],
                    "inline": True,
                },
                {
                    "name": "🔥 Daily Streak",
                    "value": f"{user_data['daily_streak']} days",
                    "inline": True,
                },
                {
                    "name": "🎯 Available Commands",
                    "value": (
                        "`/agent_assist` - Get AI agent help\n"
                        "`/focus_mode` - Start hyperfocus session\n"
                        "`/daily_boost` - Daily dopamine drop\n"
                        "`/wallet` - Check your cosmic wealth"
                    ),
                    "inline": False,
                },
            ],
        }

        return {"type": 4, "data": {"embeds": [embed]}}

    def handle_agent_assist(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """🤖 Handle agent_assist command"""
        user = (
            interaction["member"]["user"]
            if "member" in interaction
            else interaction["user"]
        )
        options = interaction["data"].get("options", [])

        # Get task from options
        task = None
        for option in options:
            if option["name"] == "task":
                task = option["value"]
                break

        if not task:
            return {
                "type": 4,
                "data": {
                    "content": "❌ Please specify a task for the Agent Army!",
                    "flags": 64,
                },
            }

        # Add to agent orchestrator
        task_id = "manual_task"
        if ORCHESTRATOR_AVAILABLE:
            task_id = self.orchestrator.add_task(
                f"User Request: {task}",
                priority=2,
                complexity=1.5,
                required_skills=["User Support", "Problem Solving"],
            )

        embed = {
            "title": "🤖💥 AGENT ARMY DISPATCHED! 💥🤖",
            "description": f"Task: **{task}**",
            "color": 0x0099FF,
            "fields": [
                {
                    "name": "🎯 Status",
                    "value": "Agent Army is analyzing your request...",
                    "inline": False,
                },
                {"name": "📋 Task ID", "value": f"`{task_id}`", "inline": True},
                {"name": "⏱️ Estimated Time", "value": "2-5 minutes", "inline": True},
            ],
        }

        return {"type": 4, "data": {"embeds": [embed]}}

    def handle_focus_mode(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """🧠 Handle focus_mode command"""
        user = (
            interaction["member"]["user"]
            if "member" in interaction
            else interaction["user"]
        )
        options = interaction["data"].get("options", [])

        # Parse options
        project = None
        minutes = 25  # default

        for option in options:
            if option["name"] == "project":
                project = option["value"]
            elif option["name"] == "minutes":
                minutes = min(option["value"], 120)  # Cap at 2 hours

        if not project:
            return {
                "type": 4,
                "data": {"content": "❌ Please specify a project name!", "flags": 64},
            }

        token_reward = minutes * 2

        embed = {
            "title": "🧠⚡ HYPERFOCUS MODE ACTIVATED! ⚡🧠",
            "description": (
                f"🎯 **Project:** {project}\n⏰ **Duration:** {minutes} minutes"
            ),
            "color": 0xFF6B35,
            "fields": [
                {
                    "name": "💎 Token Reward",
                    "value": f"{token_reward} BROski$ upon completion",
                    "inline": True,
                },
                {
                    "name": "🎯 Focus Tips",
                    "value": (
                        "• Turn off notifications\n"
                        "• Close social media\n"
                        "• Trust your neurodivergent superpowers!"
                    ),
                    "inline": False,
                },
            ],
        }

        # Log focus session
        self.start_focus_session(user["id"], project, minutes, token_reward)

        return {"type": 4, "data": {"embeds": [embed]}}

    def handle_daily_boost(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """⚡ Handle daily_boost command"""
        user = (
            interaction["member"]["user"]
            if "member" in interaction
            else interaction["user"]
        )
        result = self.daily_checkin(user["id"], user["username"])

        if result["success"]:
            embed = {
                "title": "⚡💥 DAILY DOPAMINE BOOST! 💥⚡",
                "description": result["message"],
                "color": 0xFFAA00,
                "fields": [
                    {
                        "name": "💎 Tokens Earned",
                        "value": f"+{result['tokens']} BROski$",
                        "inline": True,
                    },
                    {
                        "name": "🔥 Streak",
                        "value": f"{result['streak']} days",
                        "inline": True,
                    },
                ],
            }
        else:
            embed = {
                "title": "✅ Already Boosted Today!",
                "description": (
                    "Come back tomorrow for your next cosmic energy boost!"
                ),
                "color": 0x9932CC,
                "fields": [
                    {
                        "name": "🔥 Current Streak",
                        "value": f"{result['streak']} days",
                        "inline": True,
                    }
                ],
            }

        return {"type": 4, "data": {"embeds": [embed]}}

    def handle_wallet(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """💰 Handle wallet command"""
        user = (
            interaction["member"]["user"]
            if "member" in interaction
            else interaction["user"]
        )
        user_data = self.get_or_create_user(user["id"], user["username"])

        embed = {
            "title": f"💎 {user['username']}'s Cosmic Wallet",
            "color": 0x9932CC,
            "fields": [
                {
                    "name": "💰 BROski$ Balance",
                    "value": f"{user_data['broski_tokens']} tokens",
                    "inline": True,
                },
                {
                    "name": "🏆 Cosmic Rank",
                    "value": user_data["cosmic_rank"],
                    "inline": True,
                },
                {
                    "name": "🔥 Daily Streak",
                    "value": f"{user_data['daily_streak']} days",
                    "inline": True,
                },
                {
                    "name": "🧠 Total Focus Time",
                    "value": f"{user_data['total_focus_minutes']} minutes",
                    "inline": True,
                },
            ],
        }

        return {"type": 4, "data": {"embeds": [embed]}}

    def handle_agent_status(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """📊 Handle agent_status command"""
        if not ORCHESTRATOR_AVAILABLE:
            return {
                "type": 4,
                "data": {
                    "content": (
                        "🤖 Agent Orchestrator not available - " "running in test mode"
                    ),
                    "flags": 64,
                },
            }

        status = self.orchestrator.get_agent_status()

        # Get top 3 agents
        top_agents = sorted(
            status["agents"], key=lambda x: x["performance_score"], reverse=True
        )[:3]

        agent_text = ""
        for i, agent in enumerate(top_agents, 1):
            status_emoji = (
                "🟢"
                if agent["status"] == "READY"
                else "🔄" if agent["status"] == "WORKING" else "🔴"
            )
            agent_text += (
                f"{i}. {status_emoji} **{agent['name']}**\n"
                f"   Performance: {agent['performance_score']}% | "
                f"Energy: {agent['energy_level']}%\n"
            )

        embed = {
            "title": "🤖💥 AGENT ARMY STATUS 💥🤖",
            "description": "Real-time agent performance metrics",
            "color": 0x00AAFF,
            "fields": [
                {
                    "name": "📊 Overview",
                    "value": (
                        f"**Total Agents:** {status['total_agents']}\n"
                        f"**Active:** {status['active_agents']}\n"
                        f"**Tasks Completed:** {status['completed_tasks']}"
                    ),
                    "inline": False,
                },
                {
                    "name": "🏆 Top Performing Agents",
                    "value": agent_text,
                    "inline": False,
                },
            ],
        }

        return {"type": 4, "data": {"embeds": [embed]}}

    def handle_cosmic_transform(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """🌌 Handle cosmic_transform command"""
        embed = {
            "title": "🌌💥 COSMIC TRANSFORMATION INITIATED! 💥🌌",
            "description": (
                "Your Discord server is being transformed into a "
                "LEGENDARY cosmic base!"
            ),
            "color": 0xFF4444,
            "fields": [
                {
                    "name": "🚀 Transformation Features",
                    "value": (
                        "• ADHD-optimized channel structure\n"
                        "• BROski$ token economy\n"
                        "• Agent army integration\n"
                        "• Productivity command suite\n"
                        "• Cosmic role system"
                    ),
                    "inline": False,
                },
                {
                    "name": "⚡ Status",
                    "value": "Transformation in progress...",
                    "inline": True,
                },
                {"name": "🎯 ETA", "value": "2-3 minutes", "inline": True},
            ],
        }

        if ORCHESTRATOR_AVAILABLE:
            self.orchestrator.add_task(
                "Cosmic server transformation requested",
                priority=1,
                complexity=3.0,
                required_skills=["Server Management", "Discord API", "User Experience"],
            )

        return {"type": 4, "data": {"embeds": [embed]}}

    def handle_message_component(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """🎛️ Handle button/component interactions"""
        return {
            "type": 4,
            "data": {"content": "🎛️ Button interactions coming soon!", "flags": 64},
        }

    # Database methods (same as in fresh bot)
    def get_or_create_user(self, discord_id: str, username: str) -> Dict:
        """👤 Get or create user data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM fresh_users WHERE discord_id = ?", (str(discord_id),)
            )
            result = cursor.fetchone()

            if result:
                columns = [description[0] for description in cursor.description]
                user_data = dict(zip(columns, result))
                conn.close()
                return user_data
            else:
                # Create new user
                cursor.execute(
                    """
                    INSERT INTO fresh_users
                    (discord_id, username, broski_tokens, cosmic_rank)
                    VALUES (?, ?, 100, 'Rookie')
                """,
                    (str(discord_id), username),
                )
                conn.commit()
                conn.close()
                return self.get_or_create_user(discord_id, username)

        except Exception as e:
            print(f"❌ Error with user data: {e}")
            return {
                "discord_id": discord_id,
                "username": username,
                "broski_tokens": 100,
                "cosmic_rank": "Rookie",
                "daily_streak": 0,
                "total_focus_minutes": 0,
            }

    def daily_checkin(self, discord_id: str, username: str) -> Dict:
        """⚡ Handle daily check-in"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            today = datetime.now().date()

            cursor.execute(
                """SELECT last_checkin, daily_streak
                   FROM fresh_users WHERE discord_id = ?""",
                (str(discord_id),),
            )
            result = cursor.fetchone()

            if not result:
                self.get_or_create_user(discord_id, username)
                return self.daily_checkin(discord_id, username)

            last_checkin_str, current_streak = result
            last_checkin = (
                datetime.strptime(last_checkin_str, "%Y-%m-%d").date()
                if last_checkin_str
                else None
            )

            if last_checkin == today:
                return {
                    "success": False,
                    "streak": current_streak,
                    "message": "Already checked in today!",
                }

            # Calculate new streak
            if last_checkin and (today - last_checkin).days == 1:
                new_streak = current_streak + 1
            else:
                new_streak = 1

            # Calculate tokens
            base_tokens = 50
            streak_bonus = min(new_streak * 10, 200)
            total_tokens = base_tokens + streak_bonus

            # Update database
            cursor.execute(
                """
                UPDATE fresh_users
                SET last_checkin = ?, daily_streak = ?,
                    broski_tokens = broski_tokens + ?
                WHERE discord_id = ?
            """,
                (str(today), new_streak, total_tokens, str(discord_id)),
            )

            conn.commit()
            conn.close()

            dopamine_messages = [
                "🔥 Your brain is a WEAPON of creative destruction!",
                "⚡ Hyperfocus mode: ENGAGED! Time to build something legendary!",
                "💎 You're not broken, you're EVOLVED for this digital age!",
                "🚀 Channel that chaos into pure creative genius!",
                "🧠 Your neurodivergent superpower is ACTIVATED!",
            ]

            return {
                "success": True,
                "tokens": total_tokens,
                "streak": new_streak,
                "message": random.choice(dopamine_messages),
            }

        except Exception as e:
            print(f"❌ Check-in error: {e}")
            return {"success": False, "streak": 0, "message": "Something went wrong!"}

    def start_focus_session(
        self, discord_id: str, project: str, minutes: int, tokens: int
    ):
        """🧠 Start a focus session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO focus_sessions
                (discord_id, project_name, start_time, duration_minutes,
                 tokens_earned)
                VALUES (?, ?, ?, ?, ?)
            """,
                (str(discord_id), project, datetime.now(), minutes, tokens),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Focus session error: {e}")


def setup_interactions_endpoint(app: Flask) -> BROskiInteractionsEndpoint:
    """🚀 Setup Discord interactions endpoint in Flask app"""
    print("🚀💥 SETTING UP BROSKI INTERACTIONS ENDPOINT! 💥🚀")

    endpoint = BROskiInteractionsEndpoint(app)

    print("✅ Discord interactions endpoint configured!")
    print("📡 Endpoint: /discord/interactions")
    print("📋 Commands list: /discord/commands")
    print("🤖 Agent army integration: ACTIVE")

    return endpoint


# Example usage
if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    endpoint = setup_interactions_endpoint(app)

    @app.route("/")
    def home():
        return jsonify(
            {
                "service": "BROski Discord Interactions Endpoint",
                "status": "LEGENDARY",
                "version": "1.0.0",
                "endpoints": {
                    "interactions": "/discord/interactions",
                    "commands": "/discord/commands",
                },
            }
        )

    print("🚀 Starting BROski Interactions Endpoint server...")
    app.run(host="0.0.0.0", port=8080, debug=True)
