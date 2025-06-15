#!/usr/bin/env python3
"""
🧠 ChaosGenius Main Application
==============================
Clean Flask application startup with Discord Interactions Endpoint + IMMORTALITY PROTOCOL
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Start the dashboard
if __name__ == "__main__":
    print("🧠 Starting ChaosGenius Dashboard...")
    print("🚀 Loading from dashboard_api.py...")

    try:
        # Import and run the dashboard
        from dashboard_api import app

        # 🛡️💥 IMMORTALITY PROTOCOL INTEGRATION 💥🛡️
        print("🛡️ Activating IMMORTALITY PROTOCOL...")
        try:
            from immortality_dashboard_integration import init_immortality_integration

            immortality_bp = init_immortality_integration(app)
            print("✅ IMMORTALITY PROTOCOL: QUANTUM REDUNDANCY ACTIVATED!")
            print("🛡️ Immortality Dashboard: http://localhost:3000/immortality")
        except ImportError as e:
            print(f"⚠️ Immortality protocol integration skipped: {e}")
        except Exception as e:
            print(f"⚠️ Immortality protocol error: {e}")

        # 🚀💥 LEGENDARY DISCORD INTERACTIONS INTEGRATION 💥🚀
        print("🤖 Integrating Discord Interactions Endpoint...")
        try:
            from broski_discord_interactions_endpoint import setup_interactions_endpoint

            discord_endpoint = setup_interactions_endpoint(app)
            print("✅ Discord Interactions Endpoint: LEGENDARY INTEGRATION COMPLETE!")
        except ImportError as e:
            print(f"⚠️ Discord endpoint integration skipped: {e}")
        except Exception as e:
            print(f"⚠️ Discord endpoint error: {e}")

        print("\n🎯 ChaosGenius Dashboard Starting...")
        print("💜 Dashboard URL: http://localhost:3000")
        print("🛡️ Immortality Monitor: http://localhost:3000/immortality")
        print("📚 API Docs: http://localhost:3000/apidocs/")
        print("🎛️ Ultra Analytics: http://localhost:3000/ultra-analytics")
        print("🤖 Discord Interactions: http://localhost:3000/discord/interactions")
        print("📋 Discord Commands: http://localhost:3000/discord/commands")
        print("\n✨ Press Ctrl+C to stop\n")

        app.run(debug=True, host="0.0.0.0", port=3000)

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("🔧 Check dashboard_api.py for issues")
        sys.exit(1)
