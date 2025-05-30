#!/usr/bin/env python3
"""
🧠 ChaosGenius Main Application
==============================
Clean Flask application startup
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Start the dashboard
if __name__ == '__main__':
    print("🧠 Starting ChaosGenius Dashboard...")
    print("🚀 Loading from dashboard_api.py...")

    try:
        # Import and run the dashboard
        from dashboard_api import app

        print('\n🎯 ChaosGenius Dashboard Starting...')
        print('💜 Dashboard URL: http://localhost:3000')
        print('📚 API Docs: http://localhost:3000/apidocs/')
        print('🎛️ Ultra Analytics: http://localhost:3000/ultra-analytics')
        print('\n✨ Press Ctrl+C to stop\n')

        app.run(debug=True, host='0.0.0.0', port=3000)

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("🔧 Check dashboard_api.py for issues")
        sys.exit(1)
