#!/usr/bin/env python3
"""
🌐💰 BROski$ Wallet API - Flask Backend for Web Dashboard
Connects the beautiful web interface with the secure wallet system

Endpoints:
- GET /api/wallet/{user_id} - Get wallet info
- POST /api/wallet/transfer - Send tokens
- GET /api/wallet/balance/{user_id} - Get balance
- POST /api/wallet/daily/{user_id} - Claim daily reward
- GET /api/leaderboard - Get top users
- GET /api/shop - Get shop items
- POST /api/shop/buy - Purchase items
"""

import asyncio
import json
import logging

# Import our BROski$ systems
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.append("/root/chaosgenius")
from ai_modules.broski.enhanced_wallet_commands import BROskiEnhancedWalletCommands
from ai_modules.broski.token_engine import BROskiTokenEngine
from broski_secure_wallet_manager import BROskiSecureWalletManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web dashboard

# Initialize BROski$ systems
token_engine = BROskiTokenEngine()
wallet_commands = BROskiEnhancedWalletCommands()
secure_wallet = BROskiSecureWalletManager()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - 🌐 BROski API - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_async(coro):
    """Helper to run async functions in Flask routes"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "🔥 BROski$ API is ALIVE!",
            "timestamp": datetime.now().isoformat(),
            "systems": {
                "token_engine": "✅ Online",
                "wallet_manager": "✅ Online",
                "enhanced_commands": "✅ Online",
            },
        }
    )


@app.route("/api/wallet/<user_id>", methods=["GET"])
def get_wallet_info(user_id: str):
    """Get comprehensive wallet information"""
    try:
        # Get basic wallet info
        wallet_result = run_async(wallet_commands.handle_wallet_command(user_id))

        # Get secure wallet details
        secure_info = secure_wallet.get_wallet_info(user_id)

        # Get balance
        balance = token_engine.get_balance(user_id)

        # Combine information
        wallet_data = {
            "user_id": user_id,
            "balance": balance,
            "wallet_exists": wallet_result.get("success", False),
            "address": secure_info.get("wallet", {}).get("address", "Not found"),
            "security_level": secure_info.get("wallet", {}).get("security_level", 1),
            "daily_limit": secure_info.get("wallet", {}).get(
                "spending_limit_daily", 1000
            ),
            "transaction_limit": secure_info.get("wallet", {}).get(
                "spending_limit_transaction", 500
            ),
            "two_factor_enabled": secure_info.get("wallet", {}).get(
                "two_factor_enabled", False
            ),
            "created_at": secure_info.get("wallet", {}).get("created_at", "Unknown"),
            "recent_transactions": secure_info.get("wallet", {}).get(
                "recent_transactions", 0
            ),
        }

        return jsonify(
            {
                "success": True,
                "wallet": wallet_data,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error getting wallet info: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/wallet/balance/<user_id>", methods=["GET"])
def get_balance(user_id: str):
    """Get user's current balance"""
    try:
        balance = token_engine.get_balance(user_id)

        return jsonify(
            {
                "success": True,
                "user_id": user_id,
                "balance": balance,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error getting balance: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/wallet/transfer", methods=["POST"])
def transfer_tokens():
    """Transfer tokens between users"""
    try:
        data = request.get_json()

        from_user = data.get("from_user")
        to_user = data.get("to_user")
        amount = float(data.get("amount", 0))
        message = data.get("message", "")

        if not all([from_user, to_user]) or amount <= 0:
            return (
                jsonify({"success": False, "error": "Invalid transfer parameters"}),
                400,
            )

        # Use enhanced wallet commands for transfer
        result = run_async(
            wallet_commands.handle_send_command(from_user, to_user, amount, message)
        )

        return jsonify(
            {
                "success": result["success"],
                "message": result.get("message", "Transfer completed"),
                "amount": amount,
                "from_user": from_user,
                "to_user": to_user,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error transferring tokens: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/wallet/daily/<user_id>", methods=["POST"])
def claim_daily_reward(user_id: str):
    """Claim daily reward for user"""
    try:
        result = run_async(wallet_commands.handle_daily_command(user_id))

        return jsonify(
            {
                "success": result["success"],
                "message": result.get("message", "Daily reward processed"),
                "reward": result.get("reward", 0),
                "streak": result.get("streak", 0),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error claiming daily reward: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """Get BROski$ leaderboard"""
    try:
        limit = request.args.get("limit", 10, type=int)

        result = run_async(wallet_commands.handle_rank_command(limit))

        return jsonify(
            {
                "success": result["success"],
                "leaderboard": result.get("leaderboard", []),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error getting leaderboard: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/shop", methods=["GET"])
def get_shop_items():
    """Get available shop items"""
    try:
        user_id = request.args.get("user_id")

        if user_id:
            result = run_async(wallet_commands.handle_shop_command(user_id))
            return jsonify(
                {
                    "success": result["success"],
                    "shop_items": wallet_commands.shop_items,
                    "user_balance": result.get("balance", 0),
                    "message": result.get("message", ""),
                    "timestamp": datetime.now().isoformat(),
                }
            )
        else:
            return jsonify(
                {
                    "success": True,
                    "shop_items": wallet_commands.shop_items,
                    "timestamp": datetime.now().isoformat(),
                }
            )

    except Exception as e:
        logger.error(f"❌ Error getting shop items: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/shop/buy", methods=["POST"])
def buy_shop_item():
    """Purchase item from shop"""
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        item_id = data.get("item_id")

        if not all([user_id, item_id]):
            return (
                jsonify({"success": False, "error": "Missing user_id or item_id"}),
                400,
            )

        result = run_async(wallet_commands.handle_buy_command(user_id, item_id))

        return jsonify(
            {
                "success": result["success"],
                "message": result.get("message", "Purchase processed"),
                "item": result.get("item", {}),
                "cost": result.get("cost", 0),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error buying item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/wallet/tip", methods=["POST"])
def tip_user():
    """Tip another user with bonus"""
    try:
        data = request.get_json()

        from_user = data.get("from_user")
        to_user = data.get("to_user")
        amount = float(data.get("amount", 0))
        message = data.get("message", "")

        if not all([from_user, to_user]) or amount <= 0:
            return jsonify({"success": False, "error": "Invalid tip parameters"}), 400

        result = run_async(
            wallet_commands.handle_tip_command(from_user, to_user, amount, message)
        )

        return jsonify(
            {
                "success": result["success"],
                "message": result.get("message", "Tip sent"),
                "amount": result.get("amount", 0),
                "bonus": result.get("bonus", 0),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error sending tip: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/wallet/history/<user_id>", methods=["GET"])
def get_transaction_history(user_id: str):
    """Get transaction history for user"""
    try:
        limit = request.args.get("limit", 10, type=int)

        result = run_async(wallet_commands.handle_history_command(user_id, limit))

        return jsonify(
            {
                "success": result["success"],
                "transactions": result.get("transactions", []),
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error getting transaction history: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/wallet/vault/<user_id>", methods=["GET"])
def get_vault_info(user_id: str):
    """Get security vault information"""
    try:
        result = run_async(wallet_commands.handle_vault_command(user_id))

        return jsonify(
            {
                "success": result["success"],
                "message": result.get("message", ""),
                "wallet_info": result.get("wallet_info", {}),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"❌ Error getting vault info: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_system_stats():
    """Get overall system statistics"""
    try:
        total_supply = token_engine.get_total_supply()
        circulating_supply = token_engine.get_circulating_supply()

        # Get additional stats
        stats = {
            "total_supply": total_supply,
            "circulating_supply": circulating_supply,
            "total_wallets": 0,  # Could implement wallet count
            "daily_active_users": 0,  # Could implement DAU tracking
            "total_transactions": 0,  # Could implement tx count
            "average_balance": circulating_supply / max(1, 100),  # Estimate
            "timestamp": datetime.now().isoformat(),
        }

        return jsonify({"success": True, "stats": stats})

    except Exception as e:
        logger.error(f"❌ Error getting system stats: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/", methods=["GET"])
def serve_dashboard():
    """Serve the wallet dashboard"""
    try:
        dashboard_path = Path("/root/chaosgenius/broski_wallet_dashboard.html")
        if dashboard_path.exists():
            with open(dashboard_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return (
                jsonify(
                    {
                        "error": "Dashboard not found",
                        "message": "Please ensure broski_wallet_dashboard.html exists",
                    }
                ),
                404,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": "Endpoint not found",
                "message": "Check the BROski$ API documentation for available endpoints",
            }
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        jsonify(
            {
                "error": "Internal server error",
                "message": "Something went wrong with the BROski$ system",
            }
        ),
        500,
    )


if __name__ == "__main__":
    print("🌐💰 Starting BROski Wallet API Server...")
    print("💜 Token system integration: ACTIVE")
    print("🔒 Secure wallet management: ONLINE")
    print(f"🌐 API will be available at: http://localhost:5006")
    print("🪙 Ready to manage BROski$ empire!")

    # Run the Flask app
    app.run(host="0.0.0.0", port=5006, debug=False)
