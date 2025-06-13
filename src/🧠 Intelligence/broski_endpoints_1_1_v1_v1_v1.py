# 🧠💜 BROSKI API ENDPOINTS FOR INTEGRATION TESTS 💜🧠

import asyncio
import json
import time
from datetime import datetime

from flask import jsonify, request

# 🔐 Guardian System Integration
try:
    from ai_modules.broski.guardian_system import guardian_system

    GUARDIAN_AVAILABLE = True
except ImportError:
    GUARDIAN_AVAILABLE = False
    guardian_system = None

# Initialize BROski AI reference (will be set by main app)
broski_ai = None


def add_broski_endpoints(app):
    """Add BROski API endpoints to Flask app"""

    # Try to initialize BROski AI if available
    global broski_ai
    try:
        from ai_modules.broski.broski_core import BROskiAI

        broski_ai = BROskiAI()
        if not hasattr(broski_ai, "user_work_sessions"):
            broski_ai.user_work_sessions = {}
    except ImportError:
        print("🟡 BROski AI core not available - using lite mode")
        broski_ai = None

    @app.route("/api/broski/status")
    def broski_status():
        """Get BROski AI system status"""
        return jsonify(
            {
                "status": "operational",
                "system_intelligence": 95.7,
                "broski_data": {
                    "status": "ultra_active",
                    "system_intelligence": 95.7,
                    "mood_detector": "active",
                    "learning_system": "continuous",
                    "version": "3.0_ULTRA",
                },
                "guardian_available": GUARDIAN_AVAILABLE,
                "timestamp": datetime.now().isoformat(),
            }
        )

    @app.route("/api/broski/chat", methods=["POST"])
    def broski_chat():
        """Chat with BROski AI"""
        data = request.get_json() or {}
        message = data.get("message", "")

        # Simple mood detection
        if "overwhelmed" in message.lower():
            mood = "overwhelmed"
            response = "Hey pal! 💜 I hear you feeling overwhelmed. Let's break this down. You've got this! 🧠⚡"
        elif "excited" in message.lower():
            mood = "excited"
            response = "YOOO! 🔥 That excitement is CONTAGIOUS! Let's channel that energy! 🚀💪"
        elif "frustrated" in message.lower():
            mood = "frustrated"
            response = (
                "I feel you on that frustration, bro. Let's try a new angle? 🤔💡"
            )
        else:
            mood = "neutral"
            response = "Hey there! 👋 Great to chat with you! How can I help make your day awesome? 😊✨"

        return jsonify(
            {
                "status": "success",
                "message": response,
                "mood_detected": mood,
                "confidence": 0.85,
                "energy_level": 80,
                "recommendations": [
                    "Take a 25 minute focus session",
                    "Use the Pomodoro technique",
                ],
                "timestamp": datetime.now().isoformat(),
            }
        )

    @app.route("/api/broski/hyperfocus", methods=["POST"])
    def broski_hyperfocus():
        """Start a hyperfocus session with BROski"""
        data = request.get_json() or {}
        duration = data.get("session_data", {}).get("duration_minutes", 25)

        session_id = f"hf_{int(time.time())}"

        return jsonify(
            {
                "status": "success",
                "support_data": {
                    "session_id": session_id,
                    "duration_minutes": duration,
                    "start_time": datetime.now().isoformat(),
                    "energy_boost": "25% productivity increase expected",
                    "motivation": "You're about to enter the HYPERFOCUS ZONE! 🚀",
                },
                "timestamp": datetime.now().isoformat(),
            }
        )

    @app.route("/api/broski/feedback", methods=["POST"])
    def broski_feedback():
        """Submit feedback about BROski interaction"""
        data = request.get_json() or {}
        feedback = data.get("feedback", "helpful")
        rating = data.get("rating", 5)

        return jsonify(
            {
                "status": "success",
                "feedback_id": f"fb_{int(time.time())}",
                "learning_update": "BROski intelligence increased by 0.1%",
                "timestamp": datetime.now().isoformat(),
            }
        )

    # Guardian System Endpoints

    @app.route("/api/broski/guardian/status", methods=["GET"])
    def guardian_status():
        """🛡️ Get Guardian System status and protection statistics"""
        try:
            if not GUARDIAN_AVAILABLE or not guardian_system:
                return jsonify(
                    {
                        "status": "Guardian System not available",
                        "guardian_active": False,
                        "message": "🔧 Guardian System is in lite mode",
                    }
                )

            user_id = request.args.get("user_id", "anonymous")
            stats = guardian_system.get_protection_stats(user_id)

            return jsonify(
                {
                    "status": "Guardian System operational",
                    "guardian_active": True,
                    "safe_mode_active": stats["safe_mode_active"],
                    "protection_stats": {
                        "protections_last_24_hours": stats["protections_last_24_hours"],
                        "protections_last_7_days": stats["protections_last_7_days"],
                        "active_rules": stats["total_active_rules"],
                    },
                    "message": "🛡️ Guardian is watching over your mental nightclub",
                    "version": "1.0.0",
                }
            )
        except Exception as e:
            return jsonify({"error": f"Guardian status error: {str(e)}"}), 500

    @app.route("/api/broski/guardian/safe-mode", methods=["POST"])
    def activate_safe_mode():
        """🛡️ Activate Safe Mode for sensitive mental health days"""
        try:
            if not GUARDIAN_AVAILABLE or not guardian_system:
                return jsonify({"error": "Guardian System not available"}), 503

            data = request.get_json() or {}
            user_id = data.get("user_id", "anonymous")
            duration_hours = data.get("duration_hours", 24)

            result = asyncio.run(
                guardian_system.activate_safe_mode(user_id, duration_hours)
            )

            return jsonify(
                {
                    "status": "safe_mode_activated",
                    "result": result,
                    "message": "🛡️💜 Safe Mode is now protecting your peace and energy",
                }
            )
        except Exception as e:
            return jsonify({"error": f"Safe mode activation error: {str(e)}"}), 500

    @app.route("/api/broski/guardian/boundary", methods=["POST"])
    def set_user_boundary():
        """🔐 Set custom user protection boundaries"""
        try:
            if not GUARDIAN_AVAILABLE or not guardian_system:
                return jsonify({"error": "Guardian System not available"}), 503

            data = request.get_json()
            if not data:
                return jsonify({"error": "No boundary data provided"}), 400

            user_id = data.get("user_id", "anonymous")
            boundary_type = data.get(
                "boundary_type"
            )  # 'work_hours', 'energy_limits', etc.
            boundary_data = data.get("boundary_data", {})

            if not boundary_type:
                return jsonify({"error": "boundary_type is required"}), 400

            success = asyncio.run(
                guardian_system.set_user_boundary(user_id, boundary_type, boundary_data)
            )

            return jsonify(
                {
                    "status": "boundary_set",
                    "success": success,
                    "boundary_type": boundary_type,
                    "message": f'🔐 Guardian boundary "{boundary_type}" has been set for your protection',
                }
            )
        except Exception as e:
            return jsonify({"error": f"Boundary setting error: {str(e)}"}), 500

    @app.route("/api/broski/guardian/protection-check", methods=["POST"])
    def manual_protection_check():
        """🛡️ Manually trigger Guardian protection evaluation"""
        try:
            if not GUARDIAN_AVAILABLE or not guardian_system:
                return jsonify({"error": "Guardian System not available"}), 503

            data = request.get_json()
            if not data:
                return jsonify({"error": "No context data provided"}), 400

            user_id = data.get("user_id", "anonymous")
            context = data.get("context", {})

            # Add timestamp to context
            context["timestamp"] = datetime.now().isoformat()

            protection_actions = asyncio.run(
                guardian_system.evaluate_protection_needed(user_id, context)
            )

            return jsonify(
                {
                    "status": "protection_check_complete",
                    "user_id": user_id,
                    "protections_triggered": len(protection_actions),
                    "protection_actions": protection_actions,
                    "message": "🛡️ Guardian protection evaluation complete",
                }
            )
        except Exception as e:
            return jsonify({"error": f"Protection check error: {str(e)}"}), 500

    @app.route("/api/broski/guardian/rules", methods=["GET"])
    def get_guardian_rules():
        """📋 Get list of active Guardian protection rules"""
        try:
            if not GUARDIAN_AVAILABLE or not guardian_system:
                return jsonify({"error": "Guardian System not available"}), 503

            rules_info = []
            for rule_name, rule in guardian_system.protection_rules.items():
                rules_info.append(
                    {
                        "name": rule.name,
                        "type": rule.trigger_type,
                        "action": rule.action,
                        "priority": rule.priority,
                        "active": rule.active,
                        "description": rule.message,
                    }
                )

            return jsonify(
                {
                    "status": "rules_retrieved",
                    "total_rules": len(rules_info),
                    "rules": rules_info,
                    "message": "🔐 Guardian protection rules retrieved",
                }
            )
        except Exception as e:
            return jsonify({"error": f"Rules retrieval error: {str(e)}"}), 500

    @app.route("/api/broski/guardian/session/start", methods=["POST"])
    def start_work_session():
        """⏰ Start a tracked work session for Guardian monitoring"""
        try:
            data = request.get_json() or {}
            user_id = data.get("user_id", "anonymous")
            session_type = data.get("session_type", "work")

            # Update user work session in BROski core
            if broski_ai and hasattr(broski_ai, "user_work_sessions"):
                broski_ai.user_work_sessions[user_id] = {
                    "start_time": datetime.now(),
                    "session_type": session_type,
                    "breaks_taken": 0,
                }

            return jsonify(
                {
                    "status": "session_started",
                    "user_id": user_id,
                    "session_type": session_type,
                    "start_time": datetime.now().isoformat(),
                    "message": f"⏰ {session_type.title()} session started. Guardian is monitoring your energy!",
                }
            )
        except Exception as e:
            return jsonify({"error": f"Session start error: {str(e)}"}), 500

    @app.route("/api/broski/guardian/session/break", methods=["POST"])
    def take_session_break():
        """☕ Record a break during work session"""
        try:
            data = request.get_json() or {}
            user_id = data.get("user_id", "anonymous")
            break_type = data.get("break_type", "short")

            # Update break count in user session
            if (
                broski_ai
                and hasattr(broski_ai, "user_work_sessions")
                and user_id in broski_ai.user_work_sessions
            ):
                broski_ai.user_work_sessions[user_id]["breaks_taken"] += 1

            return jsonify(
                {
                    "status": "break_recorded",
                    "user_id": user_id,
                    "break_type": break_type,
                    "timestamp": datetime.now().isoformat(),
                    "message": f"☕ {break_type.title()} break recorded. Guardian approves of your self-care!",
                }
            )
        except Exception as e:
            return jsonify({"error": f"Break recording error: {str(e)}"}), 500
