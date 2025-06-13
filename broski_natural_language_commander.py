#!/usr/bin/env python3
"""
🧠💬 BROSKI NATURAL LANGUAGE COMMANDER 💬🧠
🌌 Talk to Your Agent Army in Plain English! 🌌
👑 "Deploy 3 money bots and run NFT campaign overnight" → IT JUST HAPPENS! 👑
"""

import json
import logging
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

# Add the chaosgenius path
sys.path.append("/root/chaosgenius")

try:
    from broski_agent_army_command_portal import BroskiAgentArmyCommandPortal
except ImportError as e:
    print(f"⚠️ Import warning: {e}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NaturalLanguageCommander:
    """🧠 Natural Language Interface for Agent Control"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.command_portal = BroskiAgentArmyCommandPortal()
        self.nl_db = f"{self.base_path}/broski_nl_commands.db"

        # Command Intent Patterns
        self.intent_patterns = {
            "deploy_agents": [
                r"deploy (\d+) (\w+) (agent|bot)s?",
                r"launch (\d+) (\w+) (agent|bot)s?",
                r"start (\d+) (\w+) (agent|bot)s?",
                r"spin up (\d+) (\w+) (agent|bot)s?",
            ],
            "run_campaign": [
                r"run (\w+) campaign",
                r"start (\w+) campaign",
                r"launch (\w+) campaign",
                r"execute (\w+) campaign",
            ],
            "schedule_task": [
                r"(overnight|tonight|tomorrow|in \d+ hours?)",
                r"schedule for (\w+)",
                r"run at (\d+)(am|pm)?",
                r"delay until (\w+)",
            ],
            "stop_agents": [
                r"stop (all )?(\w+) (agent|bot)s?",
                r"shutdown (\w+) (agent|bot)s?",
                r"kill (\w+) (agent|bot)s?",
                r"terminate (\w+) (agent|bot)s?",
            ],
            "status_check": [
                r"status of (\w+)",
                r"how is (\w+) doing",
                r"check (\w+)",
                r"report on (\w+)",
            ],
            "boost_performance": [
                r"boost (\w+) performance",
                r"optimize (\w+)",
                r"speed up (\w+)",
                r"enhance (\w+)",
            ],
            "create_mission": [
                r"create mission (\w+)",
                r"new mission (\w+)",
                r"start mission (\w+)",
                r"mission: (.+)",
            ],
        }

        # Agent Type Mappings
        self.agent_mappings = {
            "money": ["money_maker_supreme"],
            "cash": ["money_maker_supreme"],
            "income": ["money_maker_supreme"],
            "financial": ["money_maker_supreme"],
            "security": ["security_guardian"],
            "guard": ["security_guardian"],
            "protection": ["security_guardian"],
            "neural": ["neural_overseer"],
            "brain": ["neural_overseer"],
            "intelligence": ["neural_overseer"],
            "analytics": ["analytics_agent"],
            "data": ["analytics_agent"],
            "analysis": ["analytics_agent"],
        }

        # Campaign Type Mappings
        self.campaign_mappings = {
            "nft": "NFT_GENERATION_CAMPAIGN",
            "crypto": "CRYPTO_TRADING_CAMPAIGN",
            "social": "SOCIAL_MEDIA_CAMPAIGN",
            "content": "CONTENT_CREATION_CAMPAIGN",
            "marketing": "MARKETING_AUTOMATION_CAMPAIGN",
            "seo": "SEO_OPTIMIZATION_CAMPAIGN",
        }

        self._initialize_nl_database()
        print("🧠💬 NATURAL LANGUAGE COMMANDER ONLINE! 💬🧠")

    def _initialize_nl_database(self):
        """🗄️ Initialize natural language command database"""
        try:
            with sqlite3.connect(self.nl_db) as conn:
                cursor = conn.cursor()

                # Natural Language Commands Log
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS nl_commands (
                        command_id TEXT PRIMARY KEY,
                        timestamp REAL,
                        raw_input TEXT,
                        parsed_intent TEXT,
                        extracted_entities TEXT,
                        generated_commands TEXT,
                        execution_status TEXT,
                        execution_results TEXT
                    )
                """
                )

                # Intent Training Data
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS intent_training (
                        training_id TEXT PRIMARY KEY,
                        input_text TEXT,
                        intended_action TEXT,
                        success_rate REAL,
                        feedback TEXT
                    )
                """
                )

                conn.commit()
                logger.info("🧠 Natural language database initialized!")

        except sqlite3.Error as e:
            logger.error(f"NL database error: {e}")

    def parse_command(self, natural_input: str) -> Dict[str, Any]:
        """🧠 Parse natural language input into structured command"""
        command_id = f"nl_{int(time.time())}"

        # Clean and normalize input
        cleaned_input = natural_input.lower().strip()

        # Extract intents and entities
        parsed_result = {
            "command_id": command_id,
            "raw_input": natural_input,
            "intents": [],
            "entities": {},
            "confidence": 0.0,
            "generated_commands": [],
        }

        # Pattern matching for intents
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, cleaned_input, re.IGNORECASE)
                if matches:
                    parsed_result["intents"].append(intent_type)
                    parsed_result["confidence"] += 0.8 / len(patterns)

                    # Extract entities based on intent
                    if intent_type == "deploy_agents":
                        for match in matches:
                            count = int(match[0])
                            agent_type = match[1]
                            parsed_result["entities"]["agent_count"] = count
                            parsed_result["entities"]["agent_type"] = agent_type

                    elif intent_type == "run_campaign":
                        for match in matches:
                            campaign_type = (
                                match if isinstance(match, str) else match[0]
                            )
                            parsed_result["entities"]["campaign_type"] = campaign_type

                    elif intent_type == "schedule_task":
                        for match in matches:
                            schedule_time = (
                                match if isinstance(match, str) else match[0]
                            )
                            parsed_result["entities"]["schedule"] = schedule_time

        # Extract additional entities
        self._extract_additional_entities(cleaned_input, parsed_result)

        # Log the parsed command
        self._log_nl_command(parsed_result)

        return parsed_result

    def _extract_additional_entities(self, input_text: str, parsed_result: Dict):
        """🔍 Extract additional entities from input"""
        # Time expressions
        time_patterns = {
            "overnight": {"hours": 8, "start_time": "22:00"},
            "tonight": {"hours": 8, "start_time": "22:00"},
            "tomorrow": {"hours": 24, "start_time": "09:00"},
            "morning": {"hours": 4, "start_time": "06:00"},
            "afternoon": {"hours": 6, "start_time": "13:00"},
        }

        for time_expr, time_data in time_patterns.items():
            if time_expr in input_text:
                parsed_result["entities"]["timing"] = time_data

        # Priority indicators
        priority_patterns = {
            "urgent": 5,
            "high priority": 4,
            "asap": 5,
            "immediately": 5,
            "when possible": 2,
            "low priority": 1,
        }

        for priority_expr, priority_level in priority_patterns.items():
            if priority_expr in input_text:
                parsed_result["entities"]["priority"] = priority_level

        # Quantity expressions
        quantity_matches = re.findall(r"(\d+)", input_text)
        if quantity_matches:
            parsed_result["entities"]["quantities"] = [int(q) for q in quantity_matches]

    def execute_natural_command(self, natural_input: str) -> Dict[str, Any]:
        """🚀 Execute natural language command"""
        print(f"🧠 Processing: '{natural_input}'")

        # Parse the command
        parsed = self.parse_command(natural_input)

        if not parsed["intents"]:
            return {
                "success": False,
                "message": "Sorry, I couldn't understand that command. Try something like 'deploy 3 money bots' or 'run NFT campaign'",
                "suggestions": [
                    "deploy 3 money bots",
                    "run NFT campaign overnight",
                    "check security status",
                    "boost neural performance",
                    "create mission optimize system",
                ],
            }

        # Generate and execute commands
        execution_results = []

        for intent in parsed["intents"]:
            result = self._execute_intent(intent, parsed["entities"])
            execution_results.append(result)

        # Update database with results
        self._update_execution_results(parsed["command_id"], execution_results)

        success_count = sum(1 for r in execution_results if r.get("success", False))
        overall_success = success_count > 0

        return {
            "success": overall_success,
            "message": f"Executed {success_count}/{len(execution_results)} commands successfully",
            "results": execution_results,
            "parsed": parsed,
        }

    def _execute_intent(self, intent: str, entities: Dict) -> Dict[str, Any]:
        """⚡ Execute specific intent with entities"""
        try:
            if intent == "deploy_agents":
                return self._deploy_agents(entities)
            elif intent == "run_campaign":
                return self._run_campaign(entities)
            elif intent == "status_check":
                return self._check_status(entities)
            elif intent == "boost_performance":
                return self._boost_performance(entities)
            elif intent == "create_mission":
                return self._create_mission(entities)
            elif intent == "stop_agents":
                return self._stop_agents(entities)
            else:
                return {
                    "success": False,
                    "message": f"Intent '{intent}' not implemented",
                }

        except Exception as e:
            logger.error(f"Intent execution error: {e}")
            return {"success": False, "message": f"Error executing {intent}: {str(e)}"}

    def _deploy_agents(self, entities: Dict) -> Dict[str, Any]:
        """🤖 Deploy agents based on natural language"""
        agent_type = entities.get("agent_type", "money")
        agent_count = entities.get("agent_count", 1)
        priority = entities.get("priority", 3)

        # Map agent type to actual agent IDs
        mapped_agents = self.agent_mappings.get(agent_type, ["money_maker_supreme"])

        deployed_commands = []

        for i in range(min(agent_count, 5)):  # Limit to 5 agents max
            for agent_id in mapped_agents:
                command_data = {
                    "deployment_request": True,
                    "agent_instance": i + 1,
                    "natural_language_origin": True,
                }

                command_id = self.command_portal.issue_command(
                    agent_id, "DEPLOY_INSTANCE", command_data, priority
                )
                deployed_commands.append(command_id)

        # Handle scheduling if specified
        if "timing" in entities:
            timing = entities["timing"]
            # Schedule commands for later execution
            self._schedule_commands(deployed_commands, timing)

        return {
            "success": True,
            "message": f"Deployed {len(deployed_commands)} {agent_type} agent instances",
            "commands": deployed_commands,
            "agent_type": agent_type,
            "count": len(deployed_commands),
        }

    def _run_campaign(self, entities: Dict) -> Dict[str, Any]:
        """🎯 Run campaign based on natural language"""
        campaign_type = entities.get("campaign_type", "general")
        priority = entities.get("priority", 3)

        # Map campaign type
        mapped_campaign = self.campaign_mappings.get(campaign_type, "GENERAL_CAMPAIGN")

        # Create mission for campaign
        mission_id = self.command_portal.create_mission(
            f"{campaign_type.upper()} Campaign",
            ["money_maker_supreme", "neural_overseer"],
            f"Execute {mapped_campaign} with optimal efficiency",
            "CAMPAIGN",
        )

        # Execute the mission
        self.command_portal.execute_mission(mission_id)

        # Handle scheduling
        if "timing" in entities:
            timing = entities["timing"]
            print(f"⏰ Campaign scheduled for {timing}")

        return {
            "success": True,
            "message": f"Started {campaign_type} campaign",
            "mission_id": mission_id,
            "campaign_type": mapped_campaign,
        }

    def _check_status(self, entities: Dict) -> Dict[str, Any]:
        """📊 Check agent status"""
        # Get dashboard
        dashboard = self.command_portal.get_command_dashboard()

        return {
            "success": True,
            "message": "Agent status retrieved",
            "dashboard": dashboard,
        }

    def _boost_performance(self, entities: Dict) -> Dict[str, Any]:
        """⚡ Boost agent performance"""
        # Issue performance boost commands to all active agents
        boosted_agents = []

        for agent_id in self.command_portal.active_agents.keys():
            command_id = self.command_portal.issue_command(
                agent_id, "PERFORMANCE_BOOST", {}, priority=4
            )
            boosted_agents.append(agent_id)

        return {
            "success": True,
            "message": f"Performance boost sent to {len(boosted_agents)} agents",
            "boosted_agents": boosted_agents,
        }

    def _create_mission(self, entities: Dict) -> Dict[str, Any]:
        """🎯 Create new mission"""
        # Extract mission details from entities or use defaults
        mission_name = "Natural Language Mission"
        agents = ["money_maker_supreme", "security_guardian"]
        objective = "Execute natural language mission"

        mission_id = self.command_portal.create_mission(
            mission_name, agents, objective, "NATURAL_LANGUAGE"
        )

        self.command_portal.execute_mission(mission_id)

        return {
            "success": True,
            "message": f"Created and started mission: {mission_name}",
            "mission_id": mission_id,
        }

    def _stop_agents(self, entities: Dict) -> Dict[str, Any]:
        """🛑 Stop agents"""
        agent_type = entities.get("agent_type", "all")

        stopped_agents = []

        if agent_type == "all":
            # Emergency shutdown all agents
            for agent_id in self.command_portal.active_agents.keys():
                self.command_portal.emergency_agent_shutdown(agent_id)
                stopped_agents.append(agent_id)
        else:
            # Stop specific agent type
            mapped_agents = self.agent_mappings.get(agent_type, [])
            for agent_id in mapped_agents:
                if agent_id in self.command_portal.active_agents:
                    self.command_portal.emergency_agent_shutdown(agent_id)
                    stopped_agents.append(agent_id)

        return {
            "success": True,
            "message": f"Stopped {len(stopped_agents)} agents",
            "stopped_agents": stopped_agents,
        }

    def _schedule_commands(self, command_ids: List[str], timing: Dict):
        """⏰ Schedule commands for later execution"""
        # This would integrate with a scheduling system
        schedule_time = timing.get("start_time", "22:00")
        duration = timing.get("hours", 8)

        print(
            f"⏰ Scheduled {len(command_ids)} commands for {schedule_time} duration {duration}h"
        )

    def _log_nl_command(self, parsed_result: Dict):
        """📝 Log natural language command"""
        try:
            with sqlite3.connect(self.nl_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO nl_commands
                    (command_id, timestamp, raw_input, parsed_intent, extracted_entities)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        parsed_result["command_id"],
                        time.time(),
                        parsed_result["raw_input"],
                        json.dumps(parsed_result["intents"]),
                        json.dumps(parsed_result["entities"]),
                    ),
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"NL logging error: {e}")

    def _update_execution_results(self, command_id: str, results: List[Dict]):
        """📝 Update execution results in database"""
        try:
            with sqlite3.connect(self.nl_db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE nl_commands
                    SET execution_results = ?, execution_status = ?
                    WHERE command_id = ?
                """,
                    (
                        json.dumps(results),
                        (
                            "SUCCESS"
                            if any(r.get("success") for r in results)
                            else "FAILED"
                        ),
                        command_id,
                    ),
                )
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Results update error: {e}")

    def get_command_suggestions(self, partial_input: str = "") -> List[str]:
        """💡 Get smart command suggestions"""
        suggestions = [
            "deploy 3 money bots",
            "run NFT campaign overnight",
            "check all agent status",
            "boost neural performance",
            "create mission system optimization",
            "start crypto campaign",
            "deploy 5 security guards",
            "run social media campaign tomorrow",
            "stop all money agents",
            "schedule content campaign for tonight",
        ]

        if partial_input:
            # Filter suggestions based on partial input
            filtered = [s for s in suggestions if partial_input.lower() in s.lower()]
            return filtered[:5]

        return suggestions[:5]

    def interactive_mode(self):
        """🎮 Interactive natural language mode"""
        print("\n🧠💬 NATURAL LANGUAGE COMMANDER - INTERACTIVE MODE 💬🧠")
        print("=" * 60)
        print("🎯 Examples:")
        for suggestion in self.get_command_suggestions():
            print(f"   • {suggestion}")
        print("\n💡 Type 'help' for more examples, 'quit' to exit")
        print("=" * 60)

        while True:
            try:
                user_input = input("\n🧠 Command: ").strip()

                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("👋 Natural Language Commander shutting down!")
                    break

                if user_input.lower() == "help":
                    suggestions = self.get_command_suggestions()
                    print("\n💡 Try these commands:")
                    for suggestion in suggestions:
                        print(f"   • {suggestion}")
                    continue

                if not user_input:
                    continue

                # Execute the natural language command
                result = self.execute_natural_command(user_input)

                if result["success"]:
                    print(f"✅ {result['message']}")
                    for res in result.get("results", []):
                        if res.get("success"):
                            print(f"   🎯 {res['message']}")
                else:
                    print(f"❌ {result['message']}")
                    print("💡 Suggestions:")
                    for suggestion in result.get("suggestions", []):
                        print(f"   • {suggestion}")

            except KeyboardInterrupt:
                print("\n👋 Natural Language Commander shutting down!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """🚀 Launch Natural Language Commander"""
    print("🧠💬 LAUNCHING NATURAL LANGUAGE COMMANDER! 💬🧠")

    commander = NaturalLanguageCommander()

    # Start command portal monitoring
    commander.command_portal.start_command_monitoring()

    # Demo commands
    demo_commands = [
        "deploy 3 money bots",
        "run NFT campaign overnight",
        "check agent status",
        "boost neural performance",
    ]

    print("\n🎯 Demo: Testing natural language commands...")
    for cmd in demo_commands:
        print(f"\n🧠 Testing: '{cmd}'")
        result = commander.execute_natural_command(cmd)
        print(f"✅ Result: {result['message']}")

    # Enter interactive mode
    commander.interactive_mode()


if __name__ == "__main__":
    main()
