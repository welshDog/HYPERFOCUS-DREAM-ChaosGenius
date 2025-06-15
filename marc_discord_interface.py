#!/usr/bin/env python3
"""
💬🤖 M.A.R.C. DISCORD INTEGRATION - LEGENDARY COMMAND INTERFACE 🤖💬
====================================================================
Mission: Natural language agent coordination via Discord
Agent: M.A.R.C. Discord Interface
Status: LEGENDARY MODE ACTIVATED
"""

import discord
from discord.ext import commands
import asyncio
import requests
import json
from datetime import datetime
import logging

class MARCDiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!marc ', intents=intents)

        self.marc_api_url = 'http://localhost:5002'
        self.setup_logging()

    def setup_logging(self):
        """🔧 Setup Discord bot logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - M.A.R.C.Discord - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('MARCDiscord')

    async def on_ready(self):
        """🚀 Bot ready event"""
        print(f'🤖💬 M.A.R.C. Discord Bot activated: {self.user}')
        print(f'🧠 Connected to {len(self.guilds)} servers')
        print(f'🎤 Ready to coordinate {await self.get_agent_count()} agents!')

        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="93+ Agents | !marc help"
            )
        )

    async def get_agent_count(self):
        """📊 Get current agent count from M.A.R.C."""
        try:
            response = requests.get(f'{self.marc_api_url}/api/marc/status', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('total_agents', 93)
        except:
            pass
        return 93  # Fallback

    @commands.command(name='command', aliases=['cmd', 'do'])
    async def process_command(self, ctx, *, command_text):
        """🎤 Process natural language command

        Examples:
        !marc command analyze all revenue streams
        !marc cmd run security sweep on all systems
        !marc do check immortality status
        """

        # Send typing indicator
        async with ctx.typing():
            # Create beautiful embed for processing
            processing_embed = discord.Embed(
                title="🧠 M.A.R.C. Processing Command",
                description=f"```{command_text}```",
                color=0x9333ea,
                timestamp=datetime.now()
            )
            processing_embed.add_field(
                name="🔄 Status",
                value="Parsing command and assigning agents...",
                inline=False
            )
            processing_embed.set_footer(text="M.A.R.C. Orchestrator")

            message = await ctx.send(embed=processing_embed)

            try:
                # Send command to M.A.R.C. API
                response = requests.post(
                    f'{self.marc_api_url}/api/marc/command',
                    json={'command': command_text},
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()

                    if result['success']:
                        # Success embed
                        success_embed = discord.Embed(
                            title="🚀 Mission Executed Successfully!",
                            color=0x10b981,
                            timestamp=datetime.now()
                        )

                        mission_results = result['mission_results']
                        success_embed.add_field(
                            name="🎯 Mission ID",
                            value=f"`{mission_results['mission_id']}`",
                            inline=True
                        )
                        success_embed.add_field(
                            name="🤖 Agents Deployed",
                            value=f"{len(mission_results['assigned_agents'])}",
                            inline=True
                        )
                        success_embed.add_field(
                            name="📈 Success Rate",
                            value=f"{mission_results.get('success_rate', 0):.1%}",
                            inline=True
                        )

                        # Add agent results summary
                        agent_summary = []
                        for agent_id, agent_result in mission_results['agent_results'].items():
                            status = "✅" if agent_result['success'] else "❌"
                            time_taken = f"{agent_result['execution_time']:.1f}s"
                            agent_name = agent_id.replace('agent', '').replace('_', ' ').title()
                            agent_summary.append(f"{status} {agent_name} ({time_taken})")

                        if agent_summary:
                            success_embed.add_field(
                                name="🤖 Agent Results",
                                value="\n".join(agent_summary[:5]),  # Show first 5
                                inline=False
                            )

                        success_embed.set_footer(text="M.A.R.C. Orchestrator | Mission Complete")
                        await message.edit(embed=success_embed)

                    else:
                        # Failure embed
                        error_embed = discord.Embed(
                            title="❌ Mission Failed",
                            description=result.get('message', 'Unknown error'),
                            color=0xef4444,
                            timestamp=datetime.now()
                        )
                        error_embed.set_footer(text="M.A.R.C. Orchestrator")
                        await message.edit(embed=error_embed)

                else:
                    raise Exception(f"API returned status {response.status_code}")

            except Exception as e:
                # Error embed
                error_embed = discord.Embed(
                    title="💥 M.A.R.C. Connection Error",
                    description=f"```{str(e)}```",
                    color=0xef4444,
                    timestamp=datetime.now()
                )
                error_embed.add_field(
                    name="🔧 Troubleshooting",
                    value="Make sure M.A.R.C. Orchestrator is running on port 5002",
                    inline=False
                )
                error_embed.set_footer(text="M.A.R.C. Discord Interface")
                await message.edit(embed=error_embed)

    @commands.command(name='status', aliases=['stat', 'info'])
    async def get_status(self, ctx):
        """📊 Get M.A.R.C. and agent army status"""

        async with ctx.typing():
            try:
                response = requests.get(f'{self.marc_api_url}/api/marc/status', timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    # Create status embed
                    status_embed = discord.Embed(
                        title="🤖 M.A.R.C. Agent Army Status",
                        color=0x06b6d4,
                        timestamp=datetime.now()
                    )

                    # Main stats
                    status_embed.add_field(
                        name="🎯 Total Agents",
                        value=f"**{data['total_agents']}**",
                        inline=True
                    )
                    status_embed.add_field(
                        name="⚡ Available",
                        value=f"**{data['available_agents']}**",
                        inline=True
                    )
                    status_embed.add_field(
                        name="🚀 Active Missions",
                        value=f"**{data['active_missions']}**",
                        inline=True
                    )

                    # Performance metrics
                    status_embed.add_field(
                        name="📈 Avg Performance",
                        value=f"**{data['average_performance']}/100**",
                        inline=True
                    )
                    status_embed.add_field(
                        name="⚡ Coordination Efficiency",
                        value=f"**{data['coordination_efficiency']}%**",
                        inline=True
                    )
                    status_embed.add_field(
                        name="🏆 Recent Missions",
                        value=f"**{data['recent_missions']}**",
                        inline=True
                    )

                    # Agent type distribution
                    if 'type_distribution' in data:
                        type_info = []
                        for agent_type, count in data['type_distribution'].items():
                            type_info.append(f"• {agent_type.title()}: {count}")

                        status_embed.add_field(
                            name="🤖 Agent Types",
                            value="\n".join(type_info[:6]),
                            inline=False
                        )

                    # Status indicator
                    if data['coordination_efficiency'] > 80:
                        status_embed.add_field(
                            name="🎯 Status",
                            value="🟢 **LEGENDARY PERFORMANCE**",
                            inline=False
                        )
                    elif data['coordination_efficiency'] > 60:
                        status_embed.add_field(
                            name="🎯 Status",
                            value="🟡 **OPTIMAL PERFORMANCE**",
                            inline=False
                        )
                    else:
                        status_embed.add_field(
                            name="🎯 Status",
                            value="🟠 **NEEDS OPTIMIZATION**",
                            inline=False
                        )

                    status_embed.set_footer(text="M.A.R.C. Orchestrator | Real-time Status")
                    await ctx.send(embed=status_embed)

                else:
                    raise Exception(f"API returned status {response.status_code}")

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Status Check Failed",
                    description=f"```{str(e)}```",
                    color=0xef4444,
                    timestamp=datetime.now()
                )
                await ctx.send(embed=error_embed)

    @commands.command(name='agents', aliases=['list', 'army'])
    async def list_agents(self, ctx):
        """🤖 List all registered agents"""

        async with ctx.typing():
            try:
                response = requests.get(f'{self.marc_api_url}/api/marc/agents', timeout=10)

                if response.status_code == 200:
                    agents = response.json()

                    if not agents:
                        await ctx.send("🤖 No agents registered yet!")
                        return

                    # Create agents embed
                    agents_embed = discord.Embed(
                        title=f"🤖 Agent Army Registry ({len(agents)} Agents)",
                        color=0x9333ea,
                        timestamp=datetime.now()
                    )

                    # Group agents by type
                    agents_by_type = {}
                    for agent_id, agent_data in agents.items():
                        agent_type = agent_data['type']
                        if agent_type not in agents_by_type:
                            agents_by_type[agent_type] = []
                        agents_by_type[agent_type].append(agent_data)

                    # Add fields for each type
                    for agent_type, type_agents in agents_by_type.items():
                        agent_list = []
                        for agent in type_agents[:8]:  # Show max 8 per type
                            status_emoji = "🟢" if agent['status'] == 'available' else "🔴"
                            performance = agent.get('performance_score', 85)
                            agent_list.append(f"{status_emoji} {agent['name']} ({performance:.0f}%)")

                        if len(type_agents) > 8:
                            agent_list.append(f"... and {len(type_agents) - 8} more")

                        agents_embed.add_field(
                            name=f"🎯 {agent_type.title()} Agents ({len(type_agents)})",
                            value="\n".join(agent_list),
                            inline=False
                        )

                    agents_embed.set_footer(text="M.A.R.C. Agent Registry | 🟢 Available | 🔴 Busy")
                    await ctx.send(embed=agents_embed)

                else:
                    raise Exception(f"API returned status {response.status_code}")

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Agent List Failed",
                    description=f"```{str(e)}```",
                    color=0xef4444,
                    timestamp=datetime.now()
                )
                await ctx.send(embed=error_embed)

    @commands.command(name='missions', aliases=['active', 'running'])
    async def active_missions(self, ctx):
        """📋 Show active missions"""

        async with ctx.typing():
            try:
                response = requests.get(f'{self.marc_api_url}/api/marc/missions', timeout=10)

                if response.status_code == 200:
                    missions = response.json()

                    if not missions:
                        embed = discord.Embed(
                            title="📋 Active Missions",
                            description="🌟 No active missions - Agent army is ready for commands!",
                            color=0x10b981,
                            timestamp=datetime.now()
                        )
                        await ctx.send(embed=embed)
                        return

                    # Create missions embed
                    missions_embed = discord.Embed(
                        title=f"📋 Active Missions ({len(missions)})",
                        color=0xf59e0b,
                        timestamp=datetime.now()
                    )

                    for mission_id, mission_data in list(missions.items())[:5]:  # Show max 5
                        mission_status = mission_data.get('overall_status', 'unknown')
                        assigned_count = len(mission_data.get('assigned_agents', []))
                        start_time = mission_data.get('start_time', 'unknown')

                        status_emoji = {
                            'running': '🔄',
                            'completed': '✅',
                            'failed': '❌'
                        }.get(mission_status, '❓')

                        missions_embed.add_field(
                            name=f"{status_emoji} {mission_id}",
                            value=f"Agents: {assigned_count}\nStarted: {start_time[:19] if start_time != 'unknown' else 'Unknown'}",
                            inline=True
                        )

                    if len(missions) > 5:
                        missions_embed.add_field(
                            name="📊 More Missions",
                            value=f"... and {len(missions) - 5} more active missions",
                            inline=False
                        )

                    missions_embed.set_footer(text="M.A.R.C. Mission Control")
                    await ctx.send(embed=missions_embed)

                else:
                    raise Exception(f"API returned status {response.status_code}")

            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Mission Check Failed",
                    description=f"```{str(e)}```",
                    color=0xef4444,
                    timestamp=datetime.now()
                )
                await ctx.send(embed=error_embed)

    @commands.command(name='help', aliases=['h'])
    async def help_command(self, ctx):
        """❓ Show M.A.R.C. command help"""

        help_embed = discord.Embed(
            title="🤖🧠 M.A.R.C. Command Center Help 🧠🤖",
            description="Natural Language Agent Coordination System",
            color=0x9333ea,
            timestamp=datetime.now()
        )

        # Commands
        help_embed.add_field(
            name="🎤 **Command Execution**",
            value="""
            `!marc command <natural_language>`
            `!marc cmd <natural_language>`
            `!marc do <natural_language>`

            Examples:
            • `!marc cmd analyze all revenue streams`
            • `!marc do run security sweep`
            • `!marc command check system health`
            """,
            inline=False
        )

        help_embed.add_field(
            name="📊 **Status & Monitoring**",
            value="""
            `!marc status` - Agent army status
            `!marc agents` - List all agents
            `!marc missions` - Active missions
            """,
            inline=False
        )

        help_embed.add_field(
            name="🎯 **Natural Language Examples**",
            value="""
            • "optimize all revenue streams"
            • "run analytics on databases"
            • "activate security fortress"
            • "check immortality status"
            • "coordinate all agents"
            """,
            inline=False
        )

        help_embed.add_field(
            name="🔥 **Power Features**",
            value="""
            • **Multi-agent coordination** - Deploy multiple agents per mission
            • **Real-time execution** - See results as they happen
            • **Performance tracking** - Agents learn and improve
            • **Mission history** - Full audit trail
            """,
            inline=False
        )

        help_embed.set_footer(text="M.A.R.C. v1.0 | Multi-Agent Relay Coordination")
        await ctx.send(embed=help_embed)

# Example usage and testing
if __name__ == '__main__':
    print("💬🤖 M.A.R.C. DISCORD INTERFACE READY! 🤖💬")
    print("=" * 50)
    print("🔧 To run the Discord bot:")
    print("1. Set your Discord bot token")
    print("2. Make sure M.A.R.C. Orchestrator is running on port 5002")
    print("3. Invite bot to your server with appropriate permissions")
    print("4. Use !marc help to see all commands")
    print("\n🎤 Example Commands:")
    print("• !marc cmd analyze all revenue streams")
    print("• !marc status")
    print("• !marc agents")
    print("🔥 NATURAL LANGUAGE AGENT COORDINATION ACTIVATED!")