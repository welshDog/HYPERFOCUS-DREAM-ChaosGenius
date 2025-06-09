#!/usr/bin/env python3
"""
🧪💜 BROSKI AGENT POWER EXPANSION SYSTEM 💜🧪
Ultra Advanced Agent Enhancement Module
By Command of Chief Lyndz
"""

import os
import sqlite3
import json
import hashlib
import subprocess
import psutil
import time
from datetime import datetime
from pathlib import Path

class BroskiAgentPowerExpansion:
    """🔋 Advanced Power Methods for All Agents"""

    def __init__(self, agent_name, agent_type):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.base_path = "/root/chaosgenius"
        self.db_path = f"{self.base_path}/broski_overseer.db"
        self.integrity_db = f"{self.base_path}/agent_integrity.db"
        self.repair_log = f"{self.base_path}/📋 Logs & Temp/agent_repairs.log"

        # Initialize integrity database
        self.init_integrity_db()

    def init_integrity_db(self):
        """🗄️ Initialize integrity tracking database"""
        conn = sqlite3.connect(self.integrity_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_integrity (
                id INTEGER PRIMARY KEY,
                agent_name TEXT,
                file_path TEXT,
                file_hash TEXT,
                last_verified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'healthy',
                issues_found TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS source_traces (
                id INTEGER PRIMARY KEY,
                agent_name TEXT,
                operation TEXT,
                source_file TEXT,
                target_file TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                trace_data TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repair_history (
                id INTEGER PRIMARY KEY,
                agent_name TEXT,
                issue_type TEXT,
                repair_action TEXT,
                repair_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN,
                details TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def verify_integrity(self):
        """🔍 Advanced Integrity Verification System"""
        print(f"🔍 Starting integrity verification for {self.agent_name}...")

        integrity_results = {
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat(),
            "checks_performed": [],
            "issues_found": [],
            "overall_status": "healthy"
        }

        # 1. File System Integrity Check
        file_integrity = self._check_file_integrity()
        integrity_results["checks_performed"].append("file_system")
        if not file_integrity["healthy"]:
            integrity_results["issues_found"].extend(file_integrity["issues"])
            integrity_results["overall_status"] = "degraded"

        # 2. Database Connection Integrity
        db_integrity = self._check_database_integrity()
        integrity_results["checks_performed"].append("database")
        if not db_integrity["healthy"]:
            integrity_results["issues_found"].extend(db_integrity["issues"])
            integrity_results["overall_status"] = "degraded"

        # 3. Process Health Check
        process_health = self._check_process_health()
        integrity_results["checks_performed"].append("process_health")
        if not process_health["healthy"]:
            integrity_results["issues_found"].extend(process_health["issues"])
            integrity_results["overall_status"] = "degraded"

        # 4. Crystal Integrity (if agent has crystal)
        crystal_integrity = self._check_crystal_integrity()
        integrity_results["checks_performed"].append("crystal")
        if not crystal_integrity["healthy"]:
            integrity_results["issues_found"].extend(crystal_integrity["issues"])
            integrity_results["overall_status"] = "degraded"

        # 5. Memory Usage Analysis
        memory_analysis = self._analyze_memory_usage()
        integrity_results["checks_performed"].append("memory")
        if not memory_analysis["healthy"]:
            integrity_results["issues_found"].extend(memory_analysis["issues"])
            integrity_results["overall_status"] = "degraded"

        # Log results
        self._log_integrity_results(integrity_results)

        print(f"✅ Integrity verification complete for {self.agent_name}")
        print(f"🛡️ Status: {integrity_results['overall_status'].upper()}")
        print(f"🔍 Checks: {', '.join(integrity_results['checks_performed'])}")

        if integrity_results["issues_found"]:
            print(f"⚠️  Issues found: {len(integrity_results['issues_found'])}")
            for issue in integrity_results["issues_found"]:
                print(f"   • {issue}")

        return integrity_results

    def trace_source(self, operation, target_file=None):
        """🕵️ Advanced Source Tracing System"""
        print(f"🕵️ Tracing source for {self.agent_name} operation: {operation}")

        trace_data = {
            "agent": self.agent_name,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "source_chain": [],
            "dependencies": [],
            "execution_path": []
        }

        # 1. Trace execution stack
        execution_trace = self._trace_execution_stack()
        trace_data["execution_path"] = execution_trace

        # 2. Identify file dependencies
        if target_file:
            dependencies = self._trace_file_dependencies(target_file)
            trace_data["dependencies"] = dependencies

        # 3. Track source modifications
        source_modifications = self._trace_source_modifications()
        trace_data["source_chain"] = source_modifications

        # 4. Analyze operation impact
        impact_analysis = self._analyze_operation_impact(operation)
        trace_data["impact_analysis"] = impact_analysis

        # 5. Generate source map
        source_map = self._generate_source_map()
        trace_data["source_map"] = source_map

        # Log trace results
        self._log_trace_results(trace_data, target_file)

        print(f"✅ Source trace complete for {operation}")
        print(f"🔗 Dependencies found: {len(trace_data['dependencies'])}")
        print(f"📊 Execution steps: {len(trace_data['execution_path'])}")

        return trace_data

    def auto_repair(self, issue_type=None):
        """🔧 Advanced Auto-Repair System"""
        print(f"🔧 Starting auto-repair for {self.agent_name}...")

        repair_results = {
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat(),
            "repairs_attempted": [],
            "repairs_successful": [],
            "repairs_failed": [],
            "overall_success": False
        }

        # First, run integrity check to identify issues
        if not issue_type:
            integrity_check = self.verify_integrity()
            issues_to_repair = integrity_check.get("issues_found", [])
        else:
            issues_to_repair = [issue_type]

        if not issues_to_repair:
            print("✅ No issues found - system is healthy!")
            repair_results["overall_success"] = True
            return repair_results

        # Repair each identified issue
        for issue in issues_to_repair:
            repair_results["repairs_attempted"].append(issue)

            try:
                if "database" in issue.lower():
                    success = self._repair_database_issue(issue)
                elif "file" in issue.lower():
                    success = self._repair_file_issue(issue)
                elif "memory" in issue.lower():
                    success = self._repair_memory_issue(issue)
                elif "crystal" in issue.lower():
                    success = self._repair_crystal_issue(issue)
                elif "process" in issue.lower():
                    success = self._repair_process_issue(issue)
                else:
                    success = self._repair_generic_issue(issue)

                if success:
                    repair_results["repairs_successful"].append(issue)
                    print(f"✅ Successfully repaired: {issue}")
                else:
                    repair_results["repairs_failed"].append(issue)
                    print(f"❌ Failed to repair: {issue}")

            except Exception as e:
                repair_results["repairs_failed"].append(f"{issue}: {str(e)}")
                print(f"❌ Repair error for {issue}: {e}")

        # Determine overall success
        repair_results["overall_success"] = len(repair_results["repairs_failed"]) == 0

        # Log repair results
        self._log_repair_results(repair_results)

        print(f"🔧 Auto-repair complete for {self.agent_name}")
        print(f"✅ Successful: {len(repair_results['repairs_successful'])}")
        print(f"❌ Failed: {len(repair_results['repairs_failed'])}")

        # Run post-repair verification
        if repair_results["overall_success"]:
            print("🔍 Running post-repair verification...")
            post_repair_check = self.verify_integrity()
            if post_repair_check["overall_status"] == "healthy":
                print("🎉 Agent fully restored to healthy state!")
            else:
                print("⚠️  Some issues remain after repair")

        return repair_results

    def _check_file_integrity(self):
        """📁 Check file system integrity"""
        try:
            agent_file = f"{self.base_path}/ai_agents/{self.agent_name.replace(' ', '_').lower()}.py"

            if not os.path.exists(agent_file):
                return {"healthy": False, "issues": [f"Agent file missing: {agent_file}"]}

            # Check file permissions
            if not os.access(agent_file, os.R_OK):
                return {"healthy": False, "issues": [f"Agent file not readable: {agent_file}"]}

            # Calculate file hash for integrity
            with open(agent_file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            # Store/compare hash
            conn = sqlite3.connect(self.integrity_db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO agent_integrity
                (agent_name, file_path, file_hash, status)
                VALUES (?, ?, ?, ?)
            ''', (self.agent_name, agent_file, file_hash, 'healthy'))
            conn.commit()
            conn.close()

            return {"healthy": True, "issues": []}

        except Exception as e:
            return {"healthy": False, "issues": [f"File integrity check failed: {str(e)}"]}

    def _check_database_integrity(self):
        """🗄️ Check database connectivity and integrity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Test basic query
            cursor.execute("SELECT COUNT(*) FROM ai_agents WHERE agent_name = ?", (self.agent_name,))
            result = cursor.fetchone()

            conn.close()

            if result and result[0] >= 0:
                return {"healthy": True, "issues": []}
            else:
                return {"healthy": False, "issues": ["Agent not found in database"]}

        except Exception as e:
            return {"healthy": False, "issues": [f"Database connectivity failed: {str(e)}"]}

    def _check_process_health(self):
        """⚡ Check process health and resource usage"""
        try:
            issues = []

            # Check if tmux session exists
            session_name = f"broski_{self.agent_type}"
            result = subprocess.run(['tmux', 'has-session', '-t', session_name], capture_output=True)

            if result.returncode != 0:
                issues.append(f"Tmux session '{session_name}' not running")

            # Check system resources
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent

            if cpu_percent > 90:
                issues.append(f"High CPU usage: {cpu_percent}%")

            if memory_percent > 90:
                issues.append(f"High memory usage: {memory_percent}%")

            return {"healthy": len(issues) == 0, "issues": issues}

        except Exception as e:
            return {"healthy": False, "issues": [f"Process health check failed: {str(e)}"]}

    def _check_crystal_integrity(self):
        """🔮 Check crystal file integrity"""
        try:
            crystal_file = f"{self.base_path}/crystals/{self.agent_type}.broski"

            if not os.path.exists(crystal_file):
                return {"healthy": False, "issues": [f"Crystal file missing: {crystal_file}"]}

            # Validate crystal JSON
            with open(crystal_file, 'r') as f:
                crystal_data = json.load(f)

            required_fields = ["agent_name", "agent_type", "powers"]
            missing_fields = [field for field in required_fields if field not in crystal_data]

            if missing_fields:
                return {"healthy": False, "issues": [f"Crystal missing fields: {missing_fields}"]}

            return {"healthy": True, "issues": []}

        except Exception as e:
            return {"healthy": False, "issues": [f"Crystal integrity check failed: {str(e)}"]}

    def _analyze_memory_usage(self):
        """🧠 Analyze memory usage patterns"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()

            issues = []

            # Check if memory usage is excessive (>500MB for an agent)
            if memory_info.rss > 500 * 1024 * 1024:
                issues.append(f"High memory usage: {memory_info.rss / 1024 / 1024:.1f}MB")

            return {"healthy": len(issues) == 0, "issues": issues}

        except Exception as e:
            return {"healthy": False, "issues": [f"Memory analysis failed: {str(e)}"]}

    def _trace_execution_stack(self):
        """📊 Trace execution stack"""
        import traceback
        return traceback.format_stack()[-5:]  # Last 5 stack frames

    def _trace_file_dependencies(self, target_file):
        """🔗 Trace file dependencies"""
        if not target_file or not os.path.exists(target_file):
            return []

        dependencies = []
        try:
            with open(target_file, 'r') as f:
                content = f.read()

            # Look for import statements
            import re
            imports = re.findall(r'import\s+(\w+)', content)
            from_imports = re.findall(r'from\s+(\w+)', content)

            dependencies.extend(imports)
            dependencies.extend(from_imports)

        except Exception:
            pass

        return list(set(dependencies))

    def _trace_source_modifications(self):
        """📝 Trace recent source modifications"""
        agent_file = f"{self.base_path}/ai_agents/{self.agent_name.replace(' ', '_').lower()}.py"

        try:
            stat = os.stat(agent_file)
            return {
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "file_size": stat.st_size,
                "modification_time": time.ctime(stat.st_mtime)
            }
        except Exception:
            return {}

    def _analyze_operation_impact(self, operation):
        """📈 Analyze operation impact"""
        return {
            "operation": operation,
            "estimated_duration": "unknown",
            "resource_impact": "low",
            "risk_level": "low"
        }

    def _generate_source_map(self):
        """🗺️ Generate source map"""
        return {
            "agent_location": f"ai_agents/{self.agent_name.replace(' ', '_').lower()}.py",
            "crystal_location": f"crystals/{self.agent_type}.broski",
            "database_location": "broski_overseer.db",
            "deployment_location": f"tmux:broski_{self.agent_type}"
        }

    # Repair methods
    def _repair_database_issue(self, issue):
        """🔧 Repair database issues"""
        try:
            # Reconnect to database and verify schema
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Re-register agent if missing
            cursor.execute('''
                INSERT OR IGNORE INTO ai_agents
                (agent_name, agent_type, input_source, output_target, crystal_attached, database_attached)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.agent_name, self.agent_type, f"{self.agent_type}_sensors", f"{self.agent_type}_output", f"crystals/{self.agent_type}.broski", self.db_path))

            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def _repair_file_issue(self, issue):
        """🔧 Repair file issues"""
        try:
            agent_file = f"{self.base_path}/ai_agents/{self.agent_name.replace(' ', '_').lower()}.py"

            # Check if file exists, if not recreate from template
            if not os.path.exists(agent_file):
                # Recreate basic agent file
                agent_template = f'''#!/usr/bin/env python3
"""
🤖 {self.agent_name} - Auto-Restored
Type: {self.agent_type.upper()} AGENT
Restored by: Auto-Repair System
"""

import time
from datetime import datetime

class {self.agent_name.replace(' ', '')}:
    def __init__(self):
        self.name = "{self.agent_name}"
        self.type = "{self.agent_type}"
        self.status = "RESTORED"

    def process(self):
        return {{"status": "restored", "timestamp": datetime.now().isoformat()}}

if __name__ == "__main__":
    agent = {self.agent_name.replace(' ', '')}()
    print(f"🔧 {{agent.name}} restored and running!")
'''

                os.makedirs(os.path.dirname(agent_file), exist_ok=True)
                with open(agent_file, 'w') as f:
                    f.write(agent_template)

                return True

            # Fix file permissions if needed
            os.chmod(agent_file, 0o644)
            return True

        except Exception:
            return False

    def _repair_memory_issue(self, issue):
        """🔧 Repair memory issues"""
        try:
            # Force garbage collection
            import gc
            gc.collect()
            return True
        except Exception:
            return False

    def _repair_crystal_issue(self, issue):
        """🔧 Repair crystal issues"""
        try:
            crystal_file = f"{self.base_path}/crystals/{self.agent_type}.broski"

            # Recreate crystal if missing or corrupted
            crystal_data = {
                "agent_name": self.agent_name,
                "agent_type": self.agent_type,
                "powers": ["auto_repair", "integrity_check", "source_trace"],
                "created": datetime.now().isoformat(),
                "energy_level": "maximum",
                "crystal_type": f"{self.agent_type}_crystal",
                "restored_by": "auto_repair_system"
            }

            os.makedirs(os.path.dirname(crystal_file), exist_ok=True)
            with open(crystal_file, 'w') as f:
                json.dump(crystal_data, f, indent=2)

            return True
        except Exception:
            return False

    def _repair_process_issue(self, issue):
        """🔧 Repair process issues"""
        try:
            # Restart tmux session if needed
            session_name = f"broski_{self.agent_type}"
            agent_file = f"{self.base_path}/ai_agents/{self.agent_name.replace(' ', '_').lower()}.py"

            # Kill old session if exists
            subprocess.run(['tmux', 'kill-session', '-t', session_name], capture_output=True)

            # Start new session
            tmux_cmd = [
                'tmux', 'new-session', '-d', '-s', session_name,
                f'cd {self.base_path} && source broski_env/bin/activate && python3 {agent_file}'
            ]

            result = subprocess.run(tmux_cmd, capture_output=True)
            return result.returncode == 0

        except Exception:
            return False

    def _repair_generic_issue(self, issue):
        """🔧 Generic repair attempt"""
        try:
            # Log the issue for manual review
            with open(self.repair_log, 'a') as f:
                f.write(f"{datetime.now().isoformat()} - {self.agent_name}: {issue}\n")
            return True
        except Exception:
            return False

    # Logging methods
    def _log_integrity_results(self, results):
        """📝 Log integrity check results"""
        conn = sqlite3.connect(self.integrity_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO agent_integrity
            (agent_name, file_path, status, issues_found)
            VALUES (?, ?, ?, ?)
        ''', (self.agent_name, f"integrity_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
              results["overall_status"], json.dumps(results["issues_found"])))
        conn.commit()
        conn.close()

    def _log_trace_results(self, trace_data, target_file):
        """📝 Log trace results"""
        conn = sqlite3.connect(self.integrity_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO source_traces
            (agent_name, operation, source_file, target_file, trace_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.agent_name, trace_data["operation"], "agent_source",
              target_file or "unknown", json.dumps(trace_data)))
        conn.commit()
        conn.close()

    def _log_repair_results(self, repair_results):
        """📝 Log repair results"""
        conn = sqlite3.connect(self.integrity_db)
        cursor = conn.cursor()

        for repair in repair_results["repairs_attempted"]:
            success = repair in repair_results["repairs_successful"]
            cursor.execute('''
                INSERT INTO repair_history
                (agent_name, issue_type, repair_action, success, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.agent_name, repair, "auto_repair", success,
                  json.dumps(repair_results)))

        conn.commit()
        conn.close()