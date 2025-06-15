#!/usr/bin/env python3
"""
🤖🧠 M.A.R.C. - MULTI-AGENT RELAY COORDINATION 🧠🤖
==================================================
Mission: Orchestrate 93+ agents across Discord, Flask, Terminal, and AutoTasks
Agent: M.A.R.C. (Multi-Agent Relay Coordination)
Status: LEGENDARY MODE ACTIVATED
"""

import asyncio
import json
import os
import sqlite3
import subprocess
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import signal
import psutil

class MARCOrchestrator:
    def __init__(self):
        self.project_root = "/root/chaosgenius"
        self.agents_registry = {}
        self.active_missions = {}
        self.task_queue = []
        self.agent_assignments = {}
        self.performance_metrics = {}
        self.setup_logging()
        self.setup_database()
        self.discover_agents()
        self.running = True

    def setup_logging(self):
        """🔧 Setup M.A.R.C. logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - M.A.R.C. - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/marc_orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('MARC')

    def setup_database(self):
        """🗄️ Setup M.A.R.C. coordination database"""
        self.db_path = os.path.join(self.project_root, "marc_coordination.db")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Agents registry table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents_registry (
                agent_id TEXT PRIMARY KEY,
                agent_name TEXT,
                agent_type TEXT,
                file_path TEXT,
                capabilities TEXT,
                status TEXT,
                last_seen TIMESTAMP,
                performance_score REAL
            )
        ''')

        # Mission logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mission_logs (
                mission_id TEXT PRIMARY KEY,
                mission_type TEXT,
                assigned_agents TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT,
                results TEXT,
                performance_metrics TEXT
            )
        ''')

        # Task queue table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_queue (
                task_id TEXT PRIMARY KEY,
                task_type TEXT,
                priority INTEGER,
                assigned_agent TEXT,
                command TEXT,
                status TEXT,
                created_time TIMESTAMP,
                scheduled_time TIMESTAMP,
                completed_time TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def discover_agents(self):
        """🔍 Discover all available agents in the system"""
        print("🔍 M.A.R.C. DISCOVERING AGENTS...")

        agent_patterns = [
            ('broski_', 'core'),
            ('agent_', 'specialized'),
            ('ai_', 'intelligence'),
            ('analytics_', 'analytics'),
            ('fusion_', 'revenue'),
            ('immortality_', 'system'),
            ('discord_', 'communication'),
            ('hyperview_', 'monitoring')
        ]

        discovered_count = 0

        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)

                    for pattern, agent_type in agent_patterns:
                        if pattern in file.lower():
                            agent_id = self.generate_agent_id(file)
                            capabilities = self.analyze_agent_capabilities(file_path)

                            self.agents_registry[agent_id] = {
                                'name': file.replace('.py', '').replace('_', ' ').title(),
                                'type': agent_type,
                                'file_path': file_path,
                                'capabilities': capabilities,
                                'status': 'available',
                                'last_seen': datetime.now().isoformat(),
                                'performance_score': 85.0  # Default score
                            }

                            discovered_count += 1
                            break

        self.save_agents_to_db()
        print(f"🤖 M.A.R.C. DISCOVERED {discovered_count} AGENTS!")
        return discovered_count

    def generate_agent_id(self, filename):
        """🆔 Generate unique agent ID"""
        return f"agent_{filename.replace('.py', '').replace('_', '').lower()}"

    def analyze_agent_capabilities(self, file_path):
        """🧠 Analyze agent capabilities from file content"""
        capabilities = []

        try:
            with open(file_path, 'r') as f:
                content = f.read().lower()

                # Capability keywords
                capability_map = {
                    'analytics': ['analyze', 'scan', 'insight', 'metric', 'data'],
                    'revenue': ['money', 'revenue', 'income', 'earning', 'profit'],
                    'security': ['security', 'protect', 'fortress', 'guard', 'safe'],
                    'communication': ['discord', 'message', 'command', 'relay'],
                    'automation': ['auto', 'schedule', 'cron', 'task', 'loop'],
                    'monitoring': ['monitor', 'health', 'status', 'watch', 'check'],
                    'optimization': ['optimize', 'improve', 'enhance', 'boost'],
                    'coordination': ['coordinate', 'manage', 'control', 'orchestrate']
                }

                for capability, keywords in capability_map.items():
                    if any(keyword in content for keyword in keywords):
                        capabilities.append(capability)

        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")

        return capabilities

    def save_agents_to_db(self):
        """💾 Save agents registry to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for agent_id, agent_data in self.agents_registry.items():
            cursor.execute('''
                INSERT OR REPLACE INTO agents_registry
                (agent_id, agent_name, agent_type, file_path, capabilities, status, last_seen, performance_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                agent_id,
                agent_data['name'],
                agent_data['type'],
                agent_data['file_path'],
                json.dumps(agent_data['capabilities']),
                agent_data['status'],
                agent_data['last_seen'],
                agent_data['performance_score']
            ))

        conn.commit()
        conn.close()

    def natural_language_mission_parser(self, command: str) -> Dict[str, Any]:
        """🎤 Parse natural language commands into structured missions"""
        print(f"🎤 M.A.R.C. PARSING: '{command}'")

        # Mission patterns
        mission_patterns = {
            'analytics': {
                'keywords': ['analyze', 'scan', 'check', 'report', 'insight', 'data'],
                'agents': ['analytics', 'core'],
                'priority': 'medium'
            },
            'revenue_optimization': {
                'keywords': ['money', 'revenue', 'optimize', 'profit', 'income', 'fusion'],
                'agents': ['revenue', 'core'],
                'priority': 'high'
            },
            'security_sweep': {
                'keywords': ['secure', 'protect', 'fortress', 'guard', 'safety'],
                'agents': ['security', 'system'],
                'priority': 'high'
            },
            'system_health': {
                'keywords': ['health', 'monitor', 'status', 'immortality', 'backup'],
                'agents': ['system', 'monitoring'],
                'priority': 'medium'
            },
            'agent_coordination': {
                'keywords': ['coordinate', 'deploy', 'manage', 'agents', 'army'],
                'agents': ['specialized', 'core'],
                'priority': 'medium'
            },
            'communication': {
                'keywords': ['discord', 'message', 'relay', 'command', 'chat'],
                'agents': ['communication', 'specialized'],
                'priority': 'low'
            }
        }

        command_lower = command.lower()

        # Determine mission type
        mission_type = 'general'
        for mission, config in mission_patterns.items():
            if any(keyword in command_lower for keyword in config['keywords']):
                mission_type = mission
                break

        # Extract parameters
        params = {}

        # Time parameters
        import re
        time_match = re.search(r'(\d+)\s*(minute|hour|day|week)', command_lower)
        if time_match:
            params['duration'] = f"{time_match.group(1)} {time_match.group(2)}s"

        # Urgency
        if any(word in command_lower for word in ['urgent', 'emergency', 'asap', 'now']):
            params['urgency'] = 'high'
        elif any(word in command_lower for word in ['later', 'schedule', 'when convenient']):
            params['urgency'] = 'low'
        else:
            params['urgency'] = 'medium'

        # Target scope
        if 'all' in command_lower:
            params['scope'] = 'all'
        elif any(word in command_lower for word in ['revenue', 'money']):
            params['scope'] = 'revenue'
        elif any(word in command_lower for word in ['security', 'safety']):
            params['scope'] = 'security'
        elif any(word in command_lower for word in ['system', 'health']):
            params['scope'] = 'system'

        mission_data = {
            'mission_id': f"mission_{int(time.time())}",
            'type': mission_type,
            'original_command': command,
            'parameters': params,
            'priority': mission_patterns.get(mission_type, {}).get('priority', 'medium'),
            'required_agent_types': mission_patterns.get(mission_type, {}).get('agents', ['core']),
            'created_time': datetime.now().isoformat()
        }

        return mission_data

    def assign_mission_to_agents(self, mission_data: Dict[str, Any]) -> List[str]:
        """🎯 Assign mission to appropriate agents"""
        print(f"🎯 M.A.R.C. ASSIGNING MISSION: {mission_data['type']}")

        required_types = mission_data['required_agent_types']
        assigned_agents = []

        # Find best agents for each required type
        for agent_type in required_types:
            best_agent = None
            best_score = 0

            for agent_id, agent_data in self.agents_registry.items():
                if (agent_data['type'] == agent_type or
                    agent_type in agent_data['capabilities']):

                    # Calculate suitability score
                    score = agent_data['performance_score']

                    # Boost score if agent is available
                    if agent_data['status'] == 'available':
                        score += 20

                    # Boost score for exact capability match
                    if mission_data['type'] in agent_data['capabilities']:
                        score += 30

                    if score > best_score:
                        best_score = score
                        best_agent = agent_id

            if best_agent:
                assigned_agents.append(best_agent)
                self.agents_registry[best_agent]['status'] = 'assigned'

        return assigned_agents

    def execute_mission(self, mission_data: Dict[str, Any], assigned_agents: List[str]) -> Dict[str, Any]:
        """🚀 Execute mission with assigned agents"""
        mission_id = mission_data['mission_id']
        print(f"🚀 M.A.R.C. EXECUTING MISSION: {mission_id}")

        mission_results = {
            'mission_id': mission_id,
            'start_time': datetime.now().isoformat(),
            'assigned_agents': assigned_agents,
            'agent_results': {},
            'overall_status': 'running',
            'performance_metrics': {}
        }

        # Store active mission
        self.active_missions[mission_id] = mission_results

        # Execute agents in parallel
        with ThreadPoolExecutor(max_workers=min(len(assigned_agents), 5)) as executor:
            future_to_agent = {}

            for agent_id in assigned_agents:
                if agent_id in self.agents_registry:
                    agent_data = self.agents_registry[agent_id]
                    future = executor.submit(self.execute_agent, agent_data, mission_data)
                    future_to_agent[future] = agent_id

            # Collect results
            for future in as_completed(future_to_agent):
                agent_id = future_to_agent[future]
                try:
                    result = future.result(timeout=60)  # 60-second timeout
                    mission_results['agent_results'][agent_id] = result

                    # Update agent performance
                    if result['success']:
                        self.agents_registry[agent_id]['performance_score'] += 2
                    else:
                        self.agents_registry[agent_id]['performance_score'] -= 1

                    # Ensure score stays within bounds
                    self.agents_registry[agent_id]['performance_score'] = max(0, min(100,
                        self.agents_registry[agent_id]['performance_score']))

                except Exception as e:
                    mission_results['agent_results'][agent_id] = {
                        'success': False,
                        'error': str(e),
                        'execution_time': 0
                    }
                    self.logger.error(f"Agent {agent_id} failed: {e}")

        # Finalize mission
        mission_results['end_time'] = datetime.now().isoformat()
        mission_results['overall_status'] = 'completed'

        # Calculate overall success rate
        successful_agents = sum(1 for result in mission_results['agent_results'].values()
                              if result.get('success', False))
        total_agents = len(mission_results['agent_results'])
        mission_results['success_rate'] = successful_agents / total_agents if total_agents > 0 else 0

        # Update agent statuses
        for agent_id in assigned_agents:
            if agent_id in self.agents_registry:
                self.agents_registry[agent_id]['status'] = 'available'
                self.agents_registry[agent_id]['last_seen'] = datetime.now().isoformat()

        # Save mission to database
        self.save_mission_to_db(mission_results)

        return mission_results

    def execute_agent(self, agent_data: Dict[str, Any], mission_data: Dict[str, Any]) -> Dict[str, Any]:
        """⚡ Execute individual agent"""
        start_time = time.time()

        try:
            file_path = agent_data['file_path']

            # Execute the agent
            result = subprocess.run(
                ['python3', file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120  # 2-minute timeout
            )

            execution_time = time.time() - start_time

            return {
                'success': result.returncode == 0,
                'output': result.stdout[-500:] if result.stdout else '',  # Last 500 chars
                'error': result.stderr[-200:] if result.stderr else '',   # Last 200 chars
                'execution_time': execution_time,
                'return_code': result.returncode
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Agent execution timed out',
                'execution_time': time.time() - start_time,
                'return_code': -1
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time,
                'return_code': -1
            }

    def save_mission_to_db(self, mission_results: Dict[str, Any]):
        """💾 Save mission results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO mission_logs
            (mission_id, mission_type, assigned_agents, start_time, end_time, status, results, performance_metrics)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            mission_results['mission_id'],
            mission_results.get('mission_type', 'unknown'),
            json.dumps(mission_results['assigned_agents']),
            mission_results['start_time'],
            mission_results.get('end_time'),
            mission_results['overall_status'],
            json.dumps(mission_results['agent_results']),
            json.dumps(mission_results.get('performance_metrics', {}))
        ))

        conn.commit()
        conn.close()

    def process_natural_language_command(self, command: str) -> Dict[str, Any]:
        """🧠 Complete pipeline for natural language command processing"""
        print(f"\n🧠 M.A.R.C. PROCESSING COMMAND: '{command}'")

        # Parse command into mission
        mission_data = self.natural_language_mission_parser(command)

        # Assign agents
        assigned_agents = self.assign_mission_to_agents(mission_data)

        if not assigned_agents:
            return {
                'success': False,
                'message': 'No suitable agents found for this mission',
                'mission_data': mission_data
            }

        # Execute mission
        mission_results = self.execute_mission(mission_data, assigned_agents)

        return {
            'success': True,
            'message': f'Mission executed with {len(assigned_agents)} agents',
            'mission_results': mission_results
        }

    def get_agent_army_status(self) -> Dict[str, Any]:
        """📊 Get comprehensive status of agent army"""
        total_agents = len(self.agents_registry)
        available_agents = sum(1 for agent in self.agents_registry.values()
                             if agent['status'] == 'available')
        assigned_agents = sum(1 for agent in self.agents_registry.values()
                            if agent['status'] == 'assigned')

        # Agent type distribution
        type_distribution = {}
        for agent in self.agents_registry.values():
            agent_type = agent['type']
            type_distribution[agent_type] = type_distribution.get(agent_type, 0) + 1

        # Average performance
        avg_performance = sum(agent['performance_score'] for agent in self.agents_registry.values()) / total_agents if total_agents > 0 else 0

        # Recent missions
        recent_missions = len([mission for mission in self.active_missions.values()
                             if mission['overall_status'] == 'completed'])

        return {
            'total_agents': total_agents,
            'available_agents': available_agents,
            'assigned_agents': assigned_agents,
            'active_missions': len(self.active_missions),
            'type_distribution': type_distribution,
            'average_performance': round(avg_performance, 1),
            'recent_missions': recent_missions,
            'coordination_efficiency': round((available_agents / total_agents) * 100, 1) if total_agents > 0 else 0
        }

    def start_task_loop_scheduler(self):
        """🔄 Start continuous task loop scheduler"""
        def scheduler_loop():
            while self.running:
                try:
                    # Check for scheduled tasks
                    self.process_scheduled_tasks()

                    # Health check on agents
                    self.perform_agent_health_check()

                    # Cleanup completed missions
                    self.cleanup_old_missions()

                    # Update performance metrics
                    self.update_performance_metrics()

                    time.sleep(30)  # Run every 30 seconds

                except Exception as e:
                    self.logger.error(f"Scheduler loop error: {e}")
                    time.sleep(60)

        scheduler_thread = threading.Thread(target=scheduler_loop)
        scheduler_thread.daemon = True
        scheduler_thread.start()

    def process_scheduled_tasks(self):
        """⏰ Process any scheduled tasks"""
        # Implementation for scheduled task processing
        pass

    def perform_agent_health_check(self):
        """🏥 Perform health check on all agents"""
        for agent_id, agent_data in self.agents_registry.items():
            # Check if agent file still exists
            if not os.path.exists(agent_data['file_path']):
                agent_data['status'] = 'missing'
            else:
                # Update last seen if available
                if agent_data['status'] == 'available':
                    agent_data['last_seen'] = datetime.now().isoformat()

    def cleanup_old_missions(self):
        """🧹 Clean up old completed missions"""
        cutoff_time = datetime.now() - timedelta(hours=24)

        missions_to_remove = []
        for mission_id, mission_data in self.active_missions.items():
            if mission_data['overall_status'] == 'completed':
                try:
                    mission_time = datetime.fromisoformat(mission_data.get('end_time', ''))
                    if mission_time < cutoff_time:
                        missions_to_remove.append(mission_id)
                except:
                    missions_to_remove.append(mission_id)

        for mission_id in missions_to_remove:
            del self.active_missions[mission_id]

    def update_performance_metrics(self):
        """📈 Update overall performance metrics"""
        self.performance_metrics = {
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(self.agents_registry),
            'agent_army_status': self.get_agent_army_status(),
            'mission_success_rate': self.calculate_mission_success_rate(),
            'coordination_efficiency': self.calculate_coordination_efficiency()
        }

    def calculate_mission_success_rate(self) -> float:
        """📊 Calculate overall mission success rate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get recent missions (last 24 hours)
        cutoff_time = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute('''
            SELECT results FROM mission_logs
            WHERE start_time > ? AND status = 'completed'
        ''', (cutoff_time,))

        results = cursor.fetchall()
        conn.close()

        if not results:
            return 0.0

        total_success = 0
        total_missions = len(results)

        for result_json, in results:
            try:
                result_data = json.loads(result_json)
                successful_agents = sum(1 for agent_result in result_data.values()
                                      if agent_result.get('success', False))
                total_agents = len(result_data)
                if total_agents > 0:
                    total_success += successful_agents / total_agents
            except:
                continue

        return round((total_success / total_missions) * 100, 1) if total_missions > 0 else 0.0

    def calculate_coordination_efficiency(self) -> float:
        """⚡ Calculate coordination efficiency"""
        available_ratio = sum(1 for agent in self.agents_registry.values()
                            if agent['status'] == 'available') / len(self.agents_registry)

        avg_performance = sum(agent['performance_score'] for agent in self.agents_registry.values()) / len(self.agents_registry)

        return round((available_ratio * 0.4 + (avg_performance / 100) * 0.6) * 100, 1)

# Flask API Integration
from flask import Flask, jsonify, request

app = Flask(__name__)
marc = MARCOrchestrator()

@app.route('/api/marc/command', methods=['POST'])
def process_command():
    """🎤 Process natural language command via API"""
    data = request.get_json()
    command = data.get('command', '')

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    result = marc.process_natural_language_command(command)
    return jsonify(result)

@app.route('/api/marc/status')
def get_status():
    """📊 Get M.A.R.C. status via API"""
    return jsonify(marc.get_agent_army_status())

@app.route('/api/marc/agents')
def get_agents():
    """🤖 Get all registered agents"""
    return jsonify(marc.agents_registry)

@app.route('/api/marc/missions')
def get_missions():
    """📋 Get active missions"""
    return jsonify(marc.active_missions)

if __name__ == '__main__':
    print("🤖🧠 M.A.R.C. ORCHESTRATOR ACTIVATED! 🧠🤖")
    print("=" * 50)

    # Initialize M.A.R.C.
    marc.start_task_loop_scheduler()

    # Test natural language processing
    test_commands = [
        "analyze all revenue streams and optimize them",
        "run security fortress sweep on all systems",
        "check system health and immortality status",
        "coordinate agents for maximum efficiency"
    ]

    print("🧪 TESTING NATURAL LANGUAGE PROCESSING...")
    for cmd in test_commands:
        result = marc.natural_language_mission_parser(cmd)
        print(f"✅ '{cmd}' -> {result['type']} mission (Priority: {result['priority']})")

    # Show agent army status
    status = marc.get_agent_army_status()
    print(f"\n🤖 AGENT ARMY STATUS:")
    print(f"📊 Total Agents: {status['total_agents']}")
    print(f"⚡ Available: {status['available_agents']}")
    print(f"🎯 Coordination Efficiency: {status['coordination_efficiency']}%")
    print(f"📈 Average Performance: {status['average_performance']}/100")

    print("\n🚀 M.A.R.C. ORCHESTRATOR READY!")
    print("💬 Send commands via Discord, API, or direct function calls!")
    print("🔥 93+ AGENTS UNDER LEGENDARY COORDINATION!")

    # Start Flask API server
    app.run(host='0.0.0.0', port=5002, debug=False)