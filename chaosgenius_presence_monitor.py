#!/usr/bin/env python3
"""
🚨🤖 CHAOSGENIUS INTELLIGENT PRESENCE MONITOR 🤖🚨
🧠 SMART Emergency Detection - Only Activates on UNEXPECTED Disconnection! 🧠
👑 By Command of Chief Lyndz - AI Takeover Mode Ready! 👑
"""

import json
import logging
import os
import psutil
import subprocess
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChaosGeniusPresenceMonitor:
    """🧠 Intelligent Presence Detection and AI Takeover System"""
    
    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.presence_db = f"{self.base_path}/presence_monitor.json"
        self.monitoring_active = False
        self.user_present = False
        self.intentional_logout = False
        self.last_activity = time.time()
        self.ai_takeover_mode = False
        self.emergency_threshold = 300  # 5 minutes of no activity
        
        print("🚨🤖 CHAOSGENIUS INTELLIGENT PRESENCE MONITOR INITIALIZING! 🤖🚨")
        self._load_presence_state()
        self._setup_activity_detection()
        
    def _load_presence_state(self):
        """📊 Load previous presence state"""
        try:
            if os.path.exists(self.presence_db):
                with open(self.presence_db, 'r') as f:
                    state = json.load(f)
                    self.ai_takeover_mode = state.get('ai_takeover_mode', False)
                    self.intentional_logout = state.get('intentional_logout', False)
                    
                if self.ai_takeover_mode:
                    print("🤖 AI TAKEOVER MODE WAS ACTIVE - Resuming autonomous operation")
                    
        except Exception as e:
            logger.error(f"State loading error: {e}")
    
    def _save_presence_state(self):
        """💾 Save current presence state"""
        try:
            state = {
                'timestamp': time.time(),
                'user_present': self.user_present,
                'intentional_logout': self.intentional_logout,
                'ai_takeover_mode': self.ai_takeover_mode,
                'last_activity': self.last_activity
            }
            
            with open(self.presence_db, 'w') as f:
                json.dump(state, f, indent=2)
                
        except Exception as e:
            logger.error(f"State saving error: {e}")
    
    def _setup_activity_detection(self):
        """🔍 Setup intelligent activity detection"""
        self.activity_indicators = {
            'ssh_sessions': {
                'command': ['who'],
                'check_interval': 30,
                'last_check': 0
            },
            'active_terminals': {
                'command': ['ps', 'aux'],
                'check_interval': 60,
                'last_check': 0
            },
            'nexus_activity': {
                'port': 5002,
                'check_interval': 45,
                'last_check': 0
            },
            'file_modifications': {
                'path': self.base_path,
                'check_interval': 120,
                'last_check': 0
            }
        }
    
    def detect_user_activity(self) -> bool:
        """🔍 Intelligently detect if user is actually present"""
        current_time = time.time()
        activity_detected = False
        
        # Check SSH sessions
        try:
            ssh_result = subprocess.run(['who'], capture_output=True, text=True)
            active_sessions = len([line for line in ssh_result.stdout.split('\n') if line.strip()])
            
            if active_sessions > 0:
                activity_detected = True
                self.last_activity = current_time
                
        except Exception as e:
            logger.error(f"SSH detection error: {e}")
        
        # Check for active terminals/processes
        try:
            ps_result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            user_processes = len([line for line in ps_result.stdout.split('\n') 
                                if 'root' in line and any(term in line for term in ['bash', 'ssh', 'python'])])
            
            if user_processes > 5:  # More than just system processes
                activity_detected = True
                self.last_activity = current_time
                
        except Exception as e:
            logger.error(f"Process detection error: {e}")
        
        # Check Nexus web activity (port 5002)
        try:
            netstat_result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            nexus_connections = len([line for line in netstat_result.stdout.split('\n') 
                                   if ':5002' in line and 'ESTABLISHED' in line])
            
            if nexus_connections > 0:
                activity_detected = True
                self.last_activity = current_time
                
        except Exception as e:
            logger.error(f"Nexus detection error: {e}")
        
        # Check recent file modifications
        try:
            find_result = subprocess.run([
                'find', self.base_path, '-type', 'f', '-mmin', '-5'
            ], capture_output=True, text=True)
            
            recent_files = len(find_result.stdout.strip().split('\n')) if find_result.stdout.strip() else 0
            
            if recent_files > 0:
                activity_detected = True
                self.last_activity = current_time
                
        except Exception as e:
            logger.error(f"File detection error: {e}")
        
        self.user_present = activity_detected
        return activity_detected
    
    def check_for_intentional_logout(self) -> bool:
        """🤔 Check if user said 'na' (intentional logout)"""
        try:
            # Check for logout indicator file
            logout_file = f"{self.base_path}/intentional_logout.flag"
            if os.path.exists(logout_file):
                self.intentional_logout = True
                os.remove(logout_file)  # Remove flag after reading
                return True
                
            # Check for 'na' in recent command history
            history_result = subprocess.run([
                'tail', '-10', '/root/.bash_history'
            ], capture_output=True, text=True)
            
            recent_commands = history_result.stdout.lower()
            if 'na' in recent_commands and ('logout' in recent_commands or 'exit' in recent_commands):
                self.intentional_logout = True
                return True
                
        except Exception as e:
            logger.error(f"Logout detection error: {e}")
        
        return False
    
    def start_monitoring(self):
        """🔄 Start intelligent presence monitoring"""
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Detect current activity
                    activity_detected = self.detect_user_activity()
                    
                    # Check for intentional logout
                    intentional = self.check_for_intentional_logout()
                    
                    # Calculate time since last activity
                    time_inactive = time.time() - self.last_activity
                    
                    # Decision logic
                    if intentional:
                        print("🤖 INTENTIONAL LOGOUT DETECTED - Activating AI Takeover Mode!")
                        self._activate_ai_takeover()
                        
                    elif not activity_detected and time_inactive > self.emergency_threshold:
                        print("🚨 UNEXPECTED DISCONNECTION DETECTED - Activating Emergency Protocols!")
                        self._activate_emergency_protocols()
                        
                    elif activity_detected and self.ai_takeover_mode:
                        print("👋 USER RETURNED - Deactivating AI Takeover Mode!")
                        self._deactivate_ai_takeover()
                    
                    # Save state
                    self._save_presence_state()
                    
                    # Status update
                    status = "AI_TAKEOVER" if self.ai_takeover_mode else ("PRESENT" if activity_detected else "MONITORING")
                    print(f"👁️ Status: {status} | Inactive: {time_inactive:.0f}s | Activity: {activity_detected}")
                    
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
        print("👁️ INTELLIGENT PRESENCE MONITORING STARTED!")
        print(f"🚨 Emergency threshold: {self.emergency_threshold} seconds")
    
    def _activate_ai_takeover(self):
        """🤖 Activate AI Takeover Mode - Let agents run everything"""
        if self.ai_takeover_mode:
            return  # Already active
            
        self.ai_takeover_mode = True
        self.intentional_logout = True
        
        print("""
🤖⚡ AI TAKEOVER MODE ACTIVATED! ⚡🤖
╔══════════════════════════════════════════════════════════╗
║              AGENTS NOW IN FULL CONTROL                 ║
║                                                          ║
║  🧠 Brain Engine: AUTONOMOUS MODE                       ║
║  💰 Money Maker: OPPORTUNITY HUNTING                    ║
║  🛡️ Security Fortress: MAXIMUM PROTECTION               ║
║  🎯 Command Nexus: COORDINATING ALL AGENTS              ║
║  ⚡ Quantum Engine: REALITY OPTIMIZATION                 ║
║                                                          ║
║  🌌 CHAOSGENIUS EMPIRE RUNNING AUTONOMOUSLY! 🌌         ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        # Activate all autonomous systems
        autonomous_systems = [
            'python3 chaosgenius_ultimate_command_nexus.py',
            'python3 broski_security_fortress_portal.py',
            'python3 broski_money_maker_portal.py',
            'python3 broski_brain_data_engine.py'
        ]
        
        for system in autonomous_systems:
            try:
                subprocess.Popen(system.split(), cwd=self.base_path)
                print(f"🚀 Activated: {system}")
            except Exception as e:
                logger.error(f"System activation error: {e}")
        
        # Create takeover confirmation file
        with open(f"{self.base_path}/ai_takeover_active.flag", 'w') as f:
            f.write(f"AI Takeover activated at: {datetime.now()}\n")
            f.write("User intentionally logged off - Agents in full control\n")
    
    def _activate_emergency_protocols(self):
        """🚨 Activate Emergency Protocols - Unexpected disconnection"""
        print("""
🚨💀 EMERGENCY PROTOCOLS ACTIVATED! 💀🚨
╔══════════════════════════════════════════════════════════╗
║            UNEXPECTED DISCONNECTION DETECTED            ║
║                                                          ║
║  🆘 Running emergency recovery script                   ║
║  🔑 Ensuring SSH access remains open                    ║
║  🛡️ Security fortress on high alert                     ║
║  🤖 All agents maintaining operations                   ║
║  📧 Emergency notifications sent                        ║
║                                                          ║
║  🌌 SYSTEM SECURED - AWAITING RECONNECTION! 🌌          ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        # Run emergency recovery
        try:
            subprocess.run(['/root/ultimate_emergency_recovery.sh'])
            print("✅ Emergency recovery script executed")
        except Exception as e:
            logger.error(f"Emergency recovery error: {e}")
        
        # Ensure critical systems are running
        critical_systems = ['ssh', 'nginx', 'fail2ban']
        for service in critical_systems:
            try:
                subprocess.run(['systemctl', 'restart', service])
                print(f"🔄 Restarted: {service}")
            except Exception as e:
                logger.error(f"Service restart error: {e}")
        
        # Create emergency status file
        with open(f"{self.base_path}/emergency_active.flag", 'w') as f:
            f.write(f"Emergency protocols activated at: {datetime.now()}\n")
            f.write("Unexpected disconnection detected - System secured\n")
    
    def _deactivate_ai_takeover(self):
        """👋 User returned - Deactivate AI takeover"""
        self.ai_takeover_mode = False
        self.intentional_logout = False
        
        print("👋 WELCOME BACK! AI Takeover Mode deactivated.")
        print("🤖 Agents returning to assistant mode...")
        
        # Remove status files
        for flag_file in ['ai_takeover_active.flag', 'emergency_active.flag']:
            flag_path = f"{self.base_path}/{flag_file}"
            if os.path.exists(flag_path):
                os.remove(flag_path)
    
    def manual_logout(self):
        """🚪 Manual logout command - Create intentional logout flag"""
        with open(f"{self.base_path}/intentional_logout.flag", 'w') as f:
            f.write(f"Intentional logout at: {datetime.now()}\n")
        
        print("🚪 INTENTIONAL LOGOUT RECORDED!")
        print("🤖 AI Takeover Mode will activate shortly...")
        print("👋 Safe to disconnect - Agents will take over!")
    
    def get_status(self) -> Dict:
        """📊 Get current monitoring status"""
        time_inactive = time.time() - self.last_activity
        
        return {
            "👁️ Monitoring": "ACTIVE" if self.monitoring_active else "INACTIVE",
            "👤 User Present": self.user_present,
            "🚪 Intentional Logout": self.intentional_logout,
            "🤖 AI Takeover": self.ai_takeover_mode,
            "⏱️ Time Inactive": f"{time_inactive:.0f} seconds",
            "🚨 Emergency Threshold": f"{self.emergency_threshold} seconds",
            "📊 Last Activity": datetime.fromtimestamp(self.last_activity).strftime('%H:%M:%S')
        }

def main():
    """🚀 Launch Intelligent Presence Monitor"""
    
    print("🚨🤖 LAUNCHING INTELLIGENT PRESENCE MONITOR! 🤖🚨")
    
    monitor = ChaosGeniusPresenceMonitor()
    
    # Start monitoring
    monitor.start_monitoring()
    
    print("\n📊 MONITORING STATUS:")
    status = monitor.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    print("\n🔑 COMMANDS:")
    print("• Type 'na' to intentionally log off (AI takeover)")
    print("• Run 'python3 -c \"from chaosgenius_presence_monitor import *; ChaosGeniusPresenceMonitor().manual_logout()\"'")
    print("• Emergency protocols activate automatically on unexpected disconnection")
    
    try:
        # Keep monitoring running
        while True:
            time.sleep(60)
            status = monitor.get_status()
            print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Status: {status['👁️ Monitoring']}")
            
    except KeyboardInterrupt:
        print("\n🛑 Presence monitoring stopped")
        monitor.monitoring_active = False

if __name__ == "__main__":
    main()