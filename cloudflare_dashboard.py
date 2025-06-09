#!/usr/bin/env python3
"""
🌩️💜 Cloudflare-Enhanced ChaosGenius Dashboard
Enhanced with your existing Cloudflare infrastructure
"""

import os
import json
import requests
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Cloudflare configuration
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID', 'your-zone-id')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN', 'your-api-token')
AGENT_TUNNEL_URL = 'https://agents.hyperfocuszone.com'

class CloudflareEmpireDashboard:
    def __init__(self):
        self.cloudflare_headers = {
            'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
            'Content-Type': 'application/json'
        }

    def get_cloudflare_analytics(self):
        """Get Cloudflare analytics data"""
        try:
            url = f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/analytics/dashboard'
            response = requests.get(url, headers=self.cloudflare_headers)
            return response.json() if response.status_code == 200 else None
        except:
            return None

    def get_tunnel_status(self):
        """Check if Cloudflare tunnel is active"""
        try:
            response = requests.get(f'{AGENT_TUNNEL_URL}/api/status', timeout=5)
            return response.status_code == 200
        except:
            return False

dashboard = CloudflareEmpireDashboard()

CLOUDFLARE_DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🌩️💜 ChaosGenius Cloudflare Empire</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            margin: 0; padding: 20px; color: white;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .cloudflare-badge {
            background: linear-gradient(45deg, #f38020, #f5af19);
            padding: 5px 15px; border-radius: 20px;
            font-size: 0.8em; font-weight: bold;
            display: inline-block; margin-bottom: 10px;
        }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        .metric-card {
            background: rgba(0,0,0,0.3);
            padding: 15px; border-radius: 10px;
            text-align: center;
        }
        .metric-value { font-size: 2em; font-weight: bold; color: #4ECDC4; }
        .metric-label { font-size: 0.9em; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌩️💜 ChaosGenius Cloudflare Empire</h1>
        <div class="cloudflare-badge">🚀 POWERED BY CLOUDFLARE</div>

        <div class="card">
            <h2>🏰 Empire Status</h2>
            <div class="status-grid">
                <div class="metric-card">
                    <div class="metric-value">{{ tunnel_status }}</div>
                    <div class="metric-label">Cloudflare Tunnel</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">ACTIVE</div>
                    <div class="metric-label">SSL Protection</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">ENABLED</div>
                    <div class="metric-label">DDoS Shield</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">24/7</div>
                    <div class="metric-label">Agent Army</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🌐 Cloudflare Analytics</h2>
            <p>Your domain: <strong>hyperfocuszone.com</strong></p>
            <p>CDN: <strong>Global Edge Acceleration</strong></p>
            <p>Security: <strong>Enterprise-Grade WAF</strong></p>
        </div>

        <div class="card">
            <h2>🚀 Architecture Overview</h2>
            <div style="font-family: monospace; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px;">
Internet → Cloudflare → Railway (Dashboard) → Cloudflare Tunnel → Agent Army (VPS)
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def cloudflare_dashboard():
    tunnel_status = "🟢 ONLINE" if dashboard.get_tunnel_status() else "🔴 OFFLINE"
    return render_template_string(CLOUDFLARE_DASHBOARD_HTML, tunnel_status=tunnel_status)

@app.route('/api/status')
def enhanced_status():
    return jsonify({
        "status": "success",
        "empire": "cloudflare-powered",
        "infrastructure": {
            "cdn": "cloudflare-global",
            "ssl": "cloudflare-universal",
            "security": "cloudflare-waf",
            "tunnel": dashboard.get_tunnel_status()
        },
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("🌩️💜 CLOUDFLARE-POWERED CHAOSGENIUS LAUNCHING...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
