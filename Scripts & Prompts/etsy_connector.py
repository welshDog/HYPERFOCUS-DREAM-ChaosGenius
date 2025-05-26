import os
import json
import requests
from datetime import datetime
from pathlib import Path
from flask import Blueprint, redirect, request, jsonify

#!/usr/bin/env python3
"""
🛍️ Etsy Connector Script
========================
Connects ChaosGenius Dashboard to live Etsy shop data
"""


etsy_bp = Blueprint('etsy', __name__)

# 🌐 Etsy App Config
ETSY_CLIENT_ID = os.getenv("ETSY_CLIENT_ID")
ETSY_CLIENT_SECRET = os.getenv("ETSY_CLIENT_SECRET")
ETSY_SHOP_ID = os.getenv("ETSY_SHOP_ID")
REDIRECT_URI = "http://localhost:5000/oauth-callback"

# 📁 Data storage
DATA_DIR = Path("data/etsy")
DATA_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_FILE = DATA_DIR / "etsy_token.json"

class EtsyConnector:
    def __init__(self):
        self.token = self.load_token()
    
    def load_token(self):
        """Load stored Etsy access token"""
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE) as f:
                return json.load(f)
        return None
    
    def save_token(self, token_data):
        """Save Etsy access token"""
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f, indent=2)
        self.token = token_data
    
    def get_headers(self):
        """Get authorization headers"""
        if not self.token:
            raise Exception("No Etsy token found. Please connect first.")
        return {"Authorization": f"Bearer {self.token['access_token']}"}

# 🚀 Step 1: Connect Etsy
@etsy_bp.route("/connect-etsy", methods=["GET"])
def connect_etsy():
    """Initiate Etsy OAuth flow"""
    scope = "listings_r transactions_r"
    auth_url = (
        f"https://www.etsy.com/oauth/connect?"
        f"response_type=code&redirect_uri={REDIRECT_URI}&"
        f"scope={scope}&client_id={ETSY_CLIENT_ID}"
    )
    return redirect(auth_url)

# 🔑 Step 2: Callback Handler
@etsy_bp.route("/oauth-callback", methods=["GET"])
def oauth_callback():
    """Handle OAuth callback and exchange code for token"""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No authorization code received"}), 400
    
    token_url = "https://api.etsy.com/v3/public/oauth/token"
    try:
        # Check if credentials are available before making request
        if not ETSY_CLIENT_ID or not ETSY_CLIENT_SECRET:
            return jsonify({"error": "Etsy credentials not configured"}), 400
            
        response = requests.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": ETSY_CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "code": code
            },
            auth=(ETSY_CLIENT_ID, ETSY_CLIENT_SECRET)
        )
        response.raise_for_status()
        
        token_data = response.json()
        token_data["created_at"] = datetime.now().isoformat()
        
        connector = EtsyConnector()
        connector.save_token(token_data)
        
        return jsonify({"status": "Etsy connected successfully", "timestamp": token_data["created_at"]})
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to get token: {str(e)}"}), 500

# 📦 Step 3: Get Listings
@etsy_bp.route("/api/etsy/listings", methods=["GET"])
def get_etsy_listings():
    """Fetch shop listings from Etsy API"""
    try:
        connector = EtsyConnector()
        headers = connector.get_headers()
        
        response = requests.get(
            f"https://api.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/listings",
            headers=headers
        )
        response.raise_for_status()
        
        listings_data = response.json()
        
        # Save data locally
        with open(DATA_DIR / f"listings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(listings_data, f, indent=2)
        
        return jsonify(listings_data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch listings: {str(e)}"}), 500

# 📬 Step 4: Get Orders
@etsy_bp.route("/api/etsy/orders", methods=["GET"])
def get_etsy_orders():
    """Fetch shop orders/receipts from Etsy API"""
    try:
        connector = EtsyConnector()
        headers = connector.get_headers()
        
        response = requests.get(
            f"https://api.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/receipts",
            headers=headers
        )
        response.raise_for_status()
        
        orders_data = response.json()
        
        # Save data locally
        with open(DATA_DIR / f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(orders_data, f, indent=2)
        
        return jsonify(orders_data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch orders: {str(e)}"}), 500

# 📊 Step 5: Get Shop Stats
@etsy_bp.route("/api/etsy/stats", methods=["GET"])
def get_shop_stats():
    """Get aggregated shop statistics"""
    try:
        connector = EtsyConnector()
        headers = connector.get_headers()
        
        # Get shop info
        shop_response = requests.get(
            f"https://api.etsy.com/v3/application/shops/{ETSY_SHOP_ID}",
            headers=headers
        )
        shop_response.raise_for_status()
        
        return jsonify({
            "shop": shop_response.json(),
            "last_updated": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch stats: {str(e)}"}), 500

# 🔄 Step 6: Refresh Token
@etsy_bp.route("/api/etsy/refresh", methods=["POST"])
def refresh_token():
    """Refresh Etsy access token"""
    try:
        connector = EtsyConnector()
        if not connector.token or "refresh_token" not in connector.token:
            return jsonify({"error": "No refresh token available"}), 400
        
        # Check if credentials are available before making request
        if not ETSY_CLIENT_ID or not ETSY_CLIENT_SECRET:
            return jsonify({"error": "Etsy credentials not configured"}), 400
            
        token_url = "https://api.etsy.com/v3/public/oauth/token"
        response = requests.post(
            token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": connector.token["refresh_token"]
            },
            auth=(ETSY_CLIENT_ID, ETSY_CLIENT_SECRET)
        )
        response.raise_for_status()
        
        new_token = response.json()
        new_token["created_at"] = datetime.now().isoformat()
        connector.save_token(new_token)
        
        return jsonify({"status": "Token refreshed", "timestamp": new_token["created_at"]})
    except Exception as e:
        return jsonify({"error": f"Failed to refresh token: {str(e)}"}), 500

# 🔌 Connection status
@etsy_bp.route("/api/etsy/status", methods=["GET"])
def connection_status():
    """Check Etsy connection status"""
    connector = EtsyConnector()
    if not connector.token:
        return jsonify({"connected": False, "message": "No token found"})
    
    # Check if token is still valid
    try:
        headers = connector.get_headers()
        response = requests.get(
            f"https://api.etsy.com/v3/application/shops/{ETSY_SHOP_ID}",
            headers=headers
        )
        if response.status_code == 200:
            return jsonify({"connected": True, "token_created": connector.token.get("created_at")})
        else:
            return jsonify({"connected": False, "message": "Token expired or invalid"})
    except Exception as e:
        return jsonify({"connected": False, "message": f"Connection error: {str(e)}"})

if __name__ == "__main__":
    print("🛍️ Etsy Connector Script")
    print("To use this connector, import the blueprint in your Flask app:")
    print("from etsy_connector import etsy_bp")
    print("app.register_blueprint(etsy_bp)")