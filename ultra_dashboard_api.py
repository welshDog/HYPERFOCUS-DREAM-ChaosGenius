#!/usr/bin/env python3
"""
🔥💻🎯 ULTRA AUTO-HELP PARTY SYSTEM DASHBOARD 🎯💻🔥
🌟 REAL-TIME MONITORING & CONTROL CENTER 🌟
👑 Command Center for the Ultimate Work-Help-Party Cycle! 👑
"""

import asyncio
import json
import sqlite3
import time
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pathlib import Path
import threading
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the chaosgenius path
sys.path.append("/root/chaosgenius")

try:
    from hyperfocuszone_ultra_auto_help_party_system import HyperFocusZoneUltraAutoHelpPartySystem
    ULTRA_SYSTEM_AVAILABLE = True
    logger.info("✅ Ultra system module imported successfully")
except ImportError as e:
    ULTRA_SYSTEM_AVAILABLE = False
    logger.warning(f"⚠️ Ultra system module not available: {e}")

app = Flask(__name__)
ultra_system = None
system_thread = None
event_loop = None

def get_or_create_event_loop():
    """Get or create event loop for async operations"""
    global event_loop
    try:
        if event_loop is None or event_loop.is_closed():
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
        return event_loop
    except Exception as e:
        logger.error(f"Error creating event loop: {e}")
        return asyncio.new_event_loop()

def run_async_safely(coro):
    """Safely run async coroutine from sync context"""
    try:
        loop = get_or_create_event_loop()
        if loop.is_running():
            # If loop is running, create a new thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result(timeout=30)
        else:
            return loop.run_until_complete(coro)
    except Exception as e:
        logger.error(f"Error running async operation: {e}")
        raise

@app.route('/')
def dashboard():
    """🎯 Main dashboard page"""
    try:
        # Check if template exists, create basic one if not
        template_path = os.path.join(app.template_folder or 'templates', 'ultra_dashboard.html')
        if not os.path.exists(template_path):
            logger.warning("⚠️ Template not found, returning basic HTML")
            return """
            <!DOCTYPE html>
            <html>
            <head><title>Ultra Dashboard</title></head>
            <body>
                <h1>🔥💻🎯 ULTRA AUTO-HELP PARTY DASHBOARD 🎯💻🔥</h1>
                <p>System Status: <span id="status">Loading...</span></p>
                <button onclick="fetch('/api/system/start', {method: 'POST'})">Start System</button>
                <button onclick="fetch('/api/system/stop', {method: 'POST'})">Stop System</button>
            </body>
            </html>
            """
        return render_template('ultra_dashboard.html')
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return jsonify({'error': 'Dashboard loading failed'}), 500

@app.route('/api/system/status')
def get_system_status():
    """📊 Get current system status"""
    try:
        if ultra_system and hasattr(ultra_system, 'get_system_dashboard'):
            dashboard_data = ultra_system.get_system_dashboard()
            return jsonify(dashboard_data)
        else:
            return jsonify({
                'system_active': False,
                'ultra_system_available': ULTRA_SYSTEM_AVAILABLE,
                'status': 'System not initialized',
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/system/start', methods=['POST'])
def start_system():
    """🚀 Start the ultra auto-help party system"""
    global ultra_system, system_thread

    try:
        if not ULTRA_SYSTEM_AVAILABLE:
            return jsonify({'error': 'Ultra system module not available'}), 400

        data = request.json or {}
        party_duration = data.get('party_duration_minutes', 5)

        if ultra_system and hasattr(ultra_system, 'system_active') and ultra_system.system_active:
            return jsonify({'error': 'System already running'}), 400

        # Create new system instance
        ultra_system = HyperFocusZoneUltraAutoHelpPartySystem(party_duration_minutes=party_duration)

        # Start system in background thread
        def run_system():
            try:
                run_async_safely(ultra_system.activate_ultra_auto_help_system())
            except Exception as e:
                logger.error(f"Error running system: {e}")

        system_thread = threading.Thread(target=run_system, daemon=True)
        system_thread.start()

        logger.info(f"✅ Ultra System started with {party_duration} minute parties!")
        return jsonify({'success': True, 'message': f'Ultra System started with {party_duration} minute parties!'})

    except Exception as e:
        logger.error(f"Error starting system: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/stop', methods=['POST'])
def stop_system():
    """🛑 Stop the ultra auto-help party system"""
    global ultra_system

    try:
        if ultra_system and hasattr(ultra_system, 'shutdown_system'):
            run_async_safely(ultra_system.shutdown_system())
            ultra_system = None

        logger.info("✅ Ultra System stopped!")
        return jsonify({'success': True, 'message': 'Ultra System stopped!'})

    except Exception as e:
        logger.error(f"Error stopping system: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/work/trigger', methods=['POST'])
def trigger_work_session():
    """🔍 Manually trigger a work session"""
    try:
        if ultra_system and hasattr(ultra_system, 'system_active') and ultra_system.system_active:
            # Simulate work detection
            run_async_safely(ultra_system.handle_work_detected(Path("manual_trigger")))
            return jsonify({'success': True, 'message': 'Work session triggered - agents summoned!'})
        else:
            return jsonify({'error': 'System not active'}), 400

    except Exception as e:
        logger.error(f"Error triggering work session: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/party/start', methods=['POST'])
def start_party():
    """🎉 Manually start a party"""
    try:
        if ultra_system and hasattr(ultra_system, 'system_active') and ultra_system.system_active:
            run_async_safely(ultra_system.start_epic_party())
            return jsonify({'success': True, 'message': 'Epic party started!'})
        else:
            return jsonify({'error': 'System not active'}), 400

    except Exception as e:
        logger.error(f"Error starting party: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/party/stop', methods=['POST'])
def stop_party():
    """🎯 Manually stop the current party"""
    try:
        if ultra_system and hasattr(ultra_system, 'party_mode_active') and ultra_system.party_mode_active:
            run_async_safely(ultra_system.end_party_mode("manual_stop"))
            return jsonify({'success': True, 'message': 'Party ended - agents back to standby!'})
        else:
            return jsonify({'error': 'No party active'}), 400

    except Exception as e:
        logger.error(f"Error stopping party: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/summon', methods=['POST'])
def summon_agents():
    """🤖 Manually summon all agents"""
    try:
        if ultra_system and hasattr(ultra_system, 'system_active') and ultra_system.system_active:
            run_async_safely(ultra_system.summon_all_agents_for_help("manual_summon"))
            return jsonify({'success': True, 'message': 'All agents summoned for help!'})
        else:
            return jsonify({'error': 'System not active'}), 400

    except Exception as e:
        logger.error(f"Error summoning agents: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/work_sessions')
def get_work_sessions():
    """📊 Get work session statistics"""
    try:
        if not ultra_system or not hasattr(ultra_system, 'system_db'):
            return jsonify({'error': 'System not initialized'}), 400

        db_path = ultra_system.system_db
        if not os.path.exists(db_path):
            return jsonify({'work_sessions': []})

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='work_sessions'")
            if not cursor.fetchone():
                return jsonify({'work_sessions': []})

            cursor.execute("""
                SELECT session_id, start_time, end_time, work_type, files_modified, agents_summoned
                FROM work_sessions
                ORDER BY start_time DESC
                LIMIT 10
            """)

            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    'session_id': row[0],
                    'start_time': datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S') if row[1] else None,
                    'end_time': datetime.fromtimestamp(row[2]).strftime('%Y-%m-%d %H:%M:%S') if row[2] else None,
                    'work_type': row[3],
                    'files_modified': row[4],
                    'agents_summoned': json.loads(row[5]) if row[5] else []
                })

            return jsonify({'work_sessions': sessions})

    except Exception as e:
        logger.error(f"Error getting work sessions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/parties')
def get_party_stats():
    """🎉 Get party statistics"""
    try:
        if not ultra_system:
            return jsonify({'error': 'System not initialized'})

        with sqlite3.connect(ultra_system.system_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT party_id, timestamp, duration_minutes, participating_agents, fun_activities, celebration_level
                FROM ultra_party_events
                ORDER BY timestamp DESC
                LIMIT 10
            """)

            parties = []
            for row in cursor.fetchall():
                parties.append({
                    'party_id': row[0],
                    'timestamp': datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S'),
                    'duration_minutes': round(row[2], 2) if row[2] else 0,
                    'participating_agents': json.loads(row[3]) if row[3] else [],
                    'fun_activities': json.loads(row[4]) if row[4] else [],
                    'celebration_level': row[5]
                })

            return jsonify({'parties': parties})

    except Exception as e:
        logger.error(f"Error getting party stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/agent_summons')
def get_agent_summon_stats():
    """🤖 Get agent summon statistics"""
    try:
        if not ultra_system:
            return jsonify({'error': 'System not initialized'})

        with sqlite3.connect(ultra_system.system_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT summon_id, timestamp, work_trigger, agents_summoned, response_time, effectiveness_score
                FROM agent_summons
                ORDER BY timestamp DESC
                LIMIT 10
            """)

            summons = []
            for row in cursor.fetchall():
                summons.append({
                    'summon_id': row[0],
                    'timestamp': datetime.fromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S'),
                    'work_trigger': row[2],
                    'agents_summoned': json.loads(row[3]) if row[3] else [],
                    'response_time': round(row[4], 2) if row[4] else 0,
                    'effectiveness_score': row[5]
                })

            return jsonify({'agent_summons': summons})

    except Exception as e:
        logger.error(f"Error getting agent summon stats: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🔥💻🎯 ULTRA AUTO-HELP PARTY DASHBOARD STARTING! 🎯💻🔥")
    print("🌐 Dashboard will be available at: http://localhost:5000")
    print("🎯 Use this dashboard to control your entire Ultra System!")

    app.run(host='0.0.0.0', port=5000, debug=True)