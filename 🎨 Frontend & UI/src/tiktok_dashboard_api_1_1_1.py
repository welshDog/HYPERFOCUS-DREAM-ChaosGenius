#!/usr/bin/env python3
"""🎵 TikTok Dashboard API - Port 5003"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from dashboard_api import app

if __name__ == "__main__":
    print("🎵 Starting TikTok Dashboard on port 5003...")
    app.run(debug=True, host="0.0.0.0", port=5003)
