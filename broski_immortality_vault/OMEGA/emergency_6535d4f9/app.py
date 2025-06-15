#!/usr/bin/env python3
"""
ChaosGenius Main Application
===========================
Clean Flask application entry point
"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

if __name__ == "__main__":
    print("🧠 Starting ChaosGenius Dashboard...")

    try:
        from api.dashboard import app

        print("💜 Dashboard URL: http://localhost:3000")
        print("📚 API Docs: http://localhost:3000/apidocs/")
        print("\n✨ Press Ctrl+C to stop\n")

        app.run(debug=True, host="0.0.0.0", port=3000)

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)
