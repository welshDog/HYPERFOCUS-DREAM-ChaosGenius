#!/usr/bin/env python3
"""
💬🎯 DISCORD COMMAND RELAY - LEGENDARY COMMUNICATION BRIDGE 🎯💬
================================================================
Mission: Bridge Discord commands to AI Agent Army with NLP intelligence
Agent: Discord Command Relay
Status: LEGENDARY MODE ACTIVATED
"""

import discord
from discord.ext import commands
import asyncio
import json
import sqlite3
import os
import re
from datetime import datetime
import logging
import subprocess

class DiscordCommandRelay:
    def __init__(self):
        self.project_root = "/root/chaosgenius"
        self.command_history = []
        self.agent_connections = {}
        self.setup_logging()
        self.load_command_mappings()

    def setup_logging(self):
        """🔧 Setup Discord relay logging"""
        logging.basicConfig(
            filename='logs/discord_relay.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_command_mappings(self):
        """📋 Load command mappings to agent functions"""
        self.command_map = {
            # Analytics Commands
            'scan': 'analytics_brain_scanner.py',
            'analyze': 'analytics_brain_scanner.py',
            'insights': 'analytics_brain_scanner.py',
            'report': 'analytics_brain_scanner.py',

            # Revenue Commands
            'money': 'broski_money_maker_portal.py',
            'revenue': 'broski_money_maker_portal.py',
            'earnings': 'broski_money_maker_portal.py',
            'optimize': 'broski_money_maker_portal.py',

            # Agent Commands
            'agents': 'broski_agent_army_command_portal.py',
            'deploy': 'broski_agent_army_command_portal.py',
            'status': 'broski_agent_army_command_portal.py',
            'coordinate': 'broski_agent_army_command_portal.py',

            # Security Commands
            'secure': 'broski_security_fortress_portal.py',
            'protect': 'broski_security_fortress_portal.py',
            'fortress': 'broski_security_fortress_portal.py',
            'guard': 'broski_security_fortress_portal.py',

            # System Commands
            'health': 'broski_health_matrix.py',
            'monitor': 'broski_health_matrix.py',
            'backup': 'immortality_protocol_core.py',
            'immortal': 'immortality_protocol_core.py'
        }

    def process_natural_language(self, message):
        """🧠 Process natural language commands with AI"""
        print(f"🧠 PROCESSING: {message}")

        # Convert to lowercase for processing
        msg_lower = message.lower()

        # Extract command intent
        intent = self.extract_intent(msg_lower)

        # Extract parameters
        params = self.extract_parameters(msg_lower)

        # Determine target agent
        target_agent = self.determine_target_agent(intent, params)

        command_data = {
            'original_message': message,
            'intent': intent,
            'parameters': params,
            'target_agent': target_agent,
            'timestamp': datetime.now().isoformat(),
            'confidence': self.calculate_confidence(intent, params)
        }

        logging.info(f"Command processed: {json.dumps(command_data)}")
        return command_data

    def extract_intent(self, message):
        """🎯 Extract command intent from message"""
        # Define intent patterns
        intent_patterns = {
            'analyze': [r'analyz', r'scan', r'check', r'inspect', r'review'],
            'revenue': [r'money', r'revenue', r'earn', r'profit', r'income'],
            'deploy': [r'deploy', r'launch', r'start', r'activate', r'run'],
            'status': [r'status', r'health', r'how.*doing', r'report'],
            'secure': [r'secur', r'protect', r'defend', r'guard', r'safe'],
            'optimize': [r'optim', r'improv', r'boost', r'enhance', r'upgrade'],
            'backup': [r'backup', r'save', r'immortal', r'preserve'],
            'help': [r'help', r'what.*can', r'command', r'assist']
        }

        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    return intent

        return 'unknown'

    def extract_parameters(self, message):
        """📊 Extract parameters from command"""
        params = {}

        # Extract time parameters
        time_match = re.search(r'(\d+)\s*(day|hour|minute|week)', message)
        if time_match:
            params['timeframe'] = f"{time_match.group(1)} {time_match.group(2)}s"

        # Extract target parameters
        if 'all' in message:
            params['scope'] = 'all'
        elif 'agent' in message:
            params['scope'] = 'agents'
        elif 'revenue' in message:
            params['scope'] = 'revenue'
        elif 'security' in message:
            params['scope'] = 'security'

        # Extract action parameters
        if 'emergency' in message or 'urgent' in message:
            params['priority'] = 'high'
        elif 'quick' in message or 'fast' in message:
            params['mode'] = 'quick'
        elif 'detailed' in message or 'full' in message:
            params['mode'] = 'detailed'

        return params

    def determine_target_agent(self, intent, params):
        """🎯 Determine which agent should handle the command"""
        # Intent-based routing
        agent_routing = {
            'analyze': 'analytics_brain_scanner.py',
            'revenue': 'broski_money_maker_portal.py',
            'deploy': 'broski_agent_army_command_portal.py',
            'status': 'broski_health_matrix.py',
            'secure': 'broski_security_fortress_portal.py',
            'optimize': 'broski_agent_evolution_engine.py',
            'backup': 'immortality_protocol_core.py',
            'help': 'broski_natural_language_commander.py'
        }

        # Scope-based routing override
        if params.get('scope') == 'revenue':
            return 'broski_money_maker_portal.py'
        elif params.get('scope') == 'security':
            return 'broski_security_fortress_portal.py'
        elif params.get('scope') == 'agents':
            return 'broski_agent_army_command_portal.py'

        return agent_routing.get(intent, 'broski_natural_language_commander.py')

    def calculate_confidence(self, intent, params):
        """📈 Calculate confidence score for command interpretation"""
        confidence = 0.5  # Base confidence

        if intent != 'unknown':
            confidence += 0.3

        if params:
            confidence += 0.2

        if len(params) > 1:
            confidence += 0.1

        return min(confidence, 1.0)

    def execute_agent_command(self, command_data):
        """🚀 Execute command through target agent"""
        print(f"🚀 EXECUTING: {command_data['intent']} -> {command_data['target_agent']}")

        try:
            # Build command execution
            agent_path = os.path.join(self.project_root, command_data['target_agent'])

            if os.path.exists(agent_path):
                # Execute the agent
                result = subprocess.run(
                    ['python3', agent_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                execution_result = {
                    'success': result.returncode == 0,
                    'output': result.stdout,
                    'error': result.stderr,
                    'agent': command_data['target_agent'],
                    'timestamp': datetime.now().isoformat()
                }

                # Log execution
                logging.info(f"Agent execution: {json.dumps(execution_result)}")

                return execution_result
            else:
                return {
                    'success': False,
                    'error': f"Agent not found: {command_data['target_agent']}",
                    'timestamp': datetime.now().isoformat()
                }

        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'agent': command_data['target_agent'],
                'timestamp': datetime.now().isoformat()
            }

            logging.error(f"Execution error: {json.dumps(error_result)}")
            return error_result

    def relay_command(self, discord_message):
        """🔄 Full command relay pipeline"""
        print(f"🔄 RELAYING COMMAND: {discord_message}")

        # Process the message
        command_data = self.process_natural_language(discord_message)

        # Execute the command
        execution_result = self.execute_agent_command(command_data)

        # Format response for Discord
        response = self.format_discord_response(command_data, execution_result)

        # Store in command history
        self.command_history.append({
            'command': command_data,
            'result': execution_result,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })

        return response

    def format_discord_response(self, command_data, execution_result):
        """💬 Format response for Discord"""
        if execution_result['success']:
            response = f"""
🚀 **Command Executed Successfully!**
🎯 **Intent**: {command_data['intent']}
🤖 **Agent**: {command_data['target_agent'].replace('.py', '')}
📊 **Confidence**: {command_data['confidence']:.0%}
⚡ **Status**: ✅ COMPLETED

```
{execution_result['output'][:500]}...
```
            """
        else:
            response = f"""
❌ **Command Execution Failed**
🎯 **Intent**: {command_data['intent']}
🤖 **Agent**: {command_data['target_agent'].replace('.py', '')}
📊 **Confidence**: {command_data['confidence']:.0%}
⚡ **Error**: {execution_result['error'][:200]}
            """

        return response.strip()

    def get_command_suggestions(self, partial_command):
        """💡 Get command suggestions based on partial input"""
        suggestions = []

        for command, agent in self.command_map.items():
            if partial_command.lower() in command.lower():
                suggestions.append({
                    'command': command,
                    'agent': agent.replace('.py', ''),
                    'description': self.get_command_description(command)
                })

        return suggestions[:5]  # Top 5 suggestions

    def get_command_description(self, command):
        """📝 Get description for command"""
        descriptions = {
            'scan': 'Analyze system data and generate insights',
            'money': 'Check revenue status and optimize earnings',
            'agents': 'Manage and coordinate AI agent army',
            'secure': 'Activate security protocols and monitoring',
            'health': 'Check system health and performance',
            'backup': 'Activate immortality backup protocols'
        }

        return descriptions.get(command, 'Execute specialized agent command')

    def get_relay_stats(self):
        """📊 Get command relay statistics"""
        total_commands = len(self.command_history)
        successful_commands = sum(1 for cmd in self.command_history
                                if cmd['result']['success'])

        stats = {
            'total_commands': total_commands,
            'successful_commands': successful_commands,
            'success_rate': successful_commands / total_commands if total_commands > 0 else 0,
            'most_used_agents': self.get_most_used_agents(),
            'avg_confidence': self.get_average_confidence(),
            'last_activity': self.command_history[-1]['timestamp'] if self.command_history else None
        }

        return stats

    def get_most_used_agents(self):
        """📈 Get most frequently used agents"""
        agent_counts = {}
        for cmd in self.command_history:
            agent = cmd['command']['target_agent']
            agent_counts[agent] = agent_counts.get(agent, 0) + 1

        return sorted(agent_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    def get_average_confidence(self):
        """📊 Calculate average confidence score"""
        if not self.command_history:
            return 0

        total_confidence = sum(cmd['command']['confidence']
                             for cmd in self.command_history)
        return total_confidence / len(self.command_history)

# Discord Bot Integration
class DiscordRelayBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

        self.relay = DiscordCommandRelay()

    async def on_ready(self):
        print(f'💬 Discord Command Relay Bot activated: {self.user}')

    @commands.command(name='relay')
    async def relay_command(self, ctx, *, message):
        """Relay command to AI Agent Army"""
        response = self.relay.relay_command(message)
        await ctx.send(response)

    @commands.command(name='suggest')
    async def suggest_commands(self, ctx, *, partial):
        """Get command suggestions"""
        suggestions = self.relay.get_command_suggestions(partial)

        if suggestions:
            response = "💡 **Command Suggestions:**\n"
            for i, suggestion in enumerate(suggestions, 1):
                response += f"{i}. `{suggestion['command']}` - {suggestion['description']}\n"
        else:
            response = "❓ No matching commands found. Try: scan, money, agents, secure, health"

        await ctx.send(response)

    @commands.command(name='stats')
    async def relay_stats(self, ctx):
        """Show relay statistics"""
        stats = self.relay.get_relay_stats()

        response = f"""
📊 **Discord Command Relay Stats**
🎯 **Total Commands**: {stats['total_commands']}
✅ **Success Rate**: {stats['success_rate']:.1%}
📈 **Avg Confidence**: {stats['avg_confidence']:.1%}
🤖 **Top Agents**: {', '.join([agent.replace('.py', '') for agent, _ in stats['most_used_agents']])}
        """

        await ctx.send(response)

if __name__ == "__main__":
    print("💬🎯 DISCORD COMMAND RELAY ACTIVATED! 🎯💬")
    print("=" * 50)

    # Initialize relay system
    relay = DiscordCommandRelay()

    # Test command processing
    test_commands = [
        "scan all systems",
        "check revenue status",
        "deploy security agents",
        "show me system health",
        "optimize all agents"
    ]

    print("🧪 TESTING COMMAND PROCESSING...")
    for cmd in test_commands:
        result = relay.process_natural_language(cmd)
        print(f"✅ '{cmd}' -> {result['intent']} ({result['confidence']:.0%})")

    print("\n🚀 DISCORD COMMAND RELAY READY!")
    print("💬 Commands can now be relayed to AI Agent Army!")
    print("🔥 Natural language processing ACTIVATED!")