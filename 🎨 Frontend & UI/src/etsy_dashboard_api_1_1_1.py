#!/usr/bin/env python3
"""🛍️ Etsy Dashboard API - Port 5002"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from dashboard_api import app

if __name__ == "__main__":
    print("🛍️ Starting Etsy Dashboard on port 5002...")
    app.run(debug=True, host="0.0.0.0", port=5002)
