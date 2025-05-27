#!/usr/bin/env python3
"""
🛍️ HYPERFOCUS DREAM - Etsy Connector Module
============================================
Based on HYPERFOCUSZONEGB integration notes
Simplified Etsy API testing and connection management
"""

import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import json

# Load environment variables
load_dotenv()

class EtsyConnector:
    """Simplified Etsy API connector for testing and basic operations"""
    
    def __init__(self):
        self.api_key = os.getenv("ETSY_API_KEY")
        self.shared_secret = os.getenv("ETSY_SHARED_SECRET") 
        self.shop_id = os.getenv("ETSY_SHOP_ID")
        self.redirect_uri = os.getenv("ETSY_REDIRECT_URI", "http://localhost:5000/auth/callback")
        self.base_url = "https://openapi.etsy.com/v3/application"
        
    def is_configured(self) -> bool:
        """Check if basic API credentials are set"""
        return bool(self.api_key and self.shop_id)
    
    def test_connection(self) -> Dict[str, Any]:
        """Test basic API connection - from HYPERFOCUSZONEGB notes"""
        if not self.is_configured():
            return {
                'status': 'error',
                'message': '🚨 Missing API credentials in .env file',
                'help': 'Add ETSY_API_KEY and ETSY_SHOP_ID to your .env file'
            }
        
        headers = {"x-api-key": self.api_key}
        url = f"{self.base_url}/shops/{self.shop_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                shop_data = response.json()
                return {
                    'status': 'success',
                    'message': '✅ Etsy API Connection Successful!',
                    'shop_name': shop_data.get('shop_name', 'Unknown'),
                    'shop_id': shop_data.get('shop_id'),
                    'currency': shop_data.get('currency_code', 'USD'),
                    'data': shop_data
                }
            elif response.status_code == 401:
                return {
                    'status': 'error',
                    'message': '❌ Invalid API Key - Check your ETSY_API_KEY',
                    'help': 'Get your API key from https://www.etsy.com/developers/your-account'
                }
            elif response.status_code == 404:
                return {
                    'status': 'error', 
                    'message': '❌ Shop Not Found - Check your ETSY_SHOP_ID',
                    'help': 'Verify your shop ID in the Etsy Developer Dashboard'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'❌ API Error: {response.status_code}',
                    'response': response.text[:200]
                }
                
        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'❌ Connection Failed: {str(e)}',
                'help': 'Check your internet connection and API endpoints'
            }
    
    def get_shop_details(self) -> Optional[Dict[str, Any]]:
        """Get shop details - original function from notes"""
        if not self.is_configured():
            print("🚨 Missing API credentials")
            return None
            
        headers = {"x-api-key": self.api_key}
        url = f"{self.base_url}/shops/{self.shop_id}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} – {response.text}")
                return None
                
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def get_legal_disclaimer(self) -> str:
        """Return the required legal disclaimer for Etsy API usage"""
        return """
        <p style="font-size: 12px; color: gray;">
          This application uses the Etsy API but is not endorsed or certified by Etsy. 
          The term "Etsy" is a trademark of Etsy, Inc.
        </p>
        """
    
    def get_oauth_authorization_url(self) -> str:
        """Generate OAuth URL for advanced permissions"""
        if not self.api_key:
            return ""
            
        # OAuth 2.0 flow parameters
        params = {
            'response_type': 'code',
            'client_id': self.api_key,
            'redirect_uri': self.redirect_uri,
            'scope': 'shops_r transactions_r listings_r',
            'state': 'hyperfocus_dream_oauth'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"https://www.etsy.com/oauth/connect?{query_string}"
    
    def setup_instructions(self) -> Dict[str, Any]:
        """Provide setup instructions for users"""
        return {
            'title': '🛍️ Etsy API Setup Instructions',
            'steps': [
                {
                    'step': 1,
                    'title': 'Create Etsy Developer Account',
                    'description': 'Go to https://www.etsy.com/developers/your-account',
                    'action': 'Sign in and create a new app'
                },
                {
                    'step': 2, 
                    'title': 'Get API Credentials',
                    'description': 'Copy your API Key (Keystring) and Shop ID',
                    'action': 'Add to .env file as ETSY_API_KEY and ETSY_SHOP_ID'
                },
                {
                    'step': 3,
                    'title': 'Auto-Find Shop ID',
                    'description': 'Use our Shop ID finder tool',
                    'action': 'python api/find_etsy_shop_id.py'
                },
                {
                    'step': 4,
                    'title': 'Test Connection',
                    'description': 'Run this connector to verify setup',
                    'action': 'python api/etsy_connector.py'
                }
            ],
            'env_example': {
                'ETSY_API_KEY': 'your_keystring_here',
                'ETSY_SHARED_SECRET': 'your_shared_secret_here', 
                'ETSY_SHOP_ID': 'your_etsy_shop_id_here',
                'ETSY_REDIRECT_URI': 'http://localhost:5000/auth/callback'
            },
            'auto_setup': 'Run "python api/find_etsy_shop_id.py" to automatically find your Shop ID!',
            'legal_note': 'Remember to include the Etsy legal disclaimer on your website'
        }

    def quick_setup_wizard(self) -> None:
        """Quick setup wizard that uses the Shop ID finder"""
        print("🚀 ETSY QUICK SETUP WIZARD")
        print("=" * 30)
        
        if not self.is_configured():
            print("💡 Let's get your Etsy integration set up!")
            print()
            
            # Check if API key exists
            if not self.api_key:
                print("📝 Step 1: Add your ETSY_API_KEY to the .env file")
                print("   Get it from: https://www.etsy.com/developers/your-account")
                return
            
            # Check if Shop ID exists
            if not self.shop_id:
                print("🔍 Step 2: Find your Shop ID")
                print("💡 Run the Shop ID finder: python api/find_etsy_shop_id.py")
                return
        
        # Test the connection
        print("🧪 Testing your configuration...")
        result = self.test_connection()
        
        if result['status'] == 'success':
            print("🎉 SUCCESS! Your Etsy integration is ready!")
            print(f"✅ Shop: {result.get('shop_name')}")
            print(f"✅ ID: {result.get('shop_id')}")
        else:
            print(f"❌ {result['message']}")
            if 'help' in result:
                print(f"💡 {result['help']}")

def main():
    """Main function for testing the connector"""
    print("🛍️ HYPERFOCUS DREAM - Etsy API Connector Test")
    print("=" * 50)
    
    connector = EtsyConnector()
    
    # Test basic configuration
    if not connector.is_configured():
        print("⚠️  Configuration needed!")
        instructions = connector.setup_instructions()
        print(f"\n{instructions['title']}")
        for step in instructions['steps']:
            print(f"{step['step']}. {step['title']}: {step['description']}")
            print(f"   Action: {step['action']}")
        print(f"\n💡 Quick Start: {instructions['auto_setup']}")
        print(f"\n📝 Add these to your .env file:")
        for key, value in instructions['env_example'].items():
            print(f"{key}={value}")
        
        # Offer to run the quick setup
        print("\n🚀 Want to run the quick setup wizard? (y/n): ", end="")
        try:
            if input().strip().lower() in ['y', 'yes']:
                connector.quick_setup_wizard()
        except KeyboardInterrupt:
            print("\n👋 Setup cancelled.")
        return
    
    # Test API connection
    print("🔌 Testing API connection...")
    result = connector.test_connection()
    print(f"Status: {result['status'].upper()}")
    print(f"Message: {result['message']}")
    
    if result['status'] == 'success':
        print(f"✅ Shop Name: {result.get('shop_name')}")
        print(f"✅ Shop ID: {result.get('shop_id')}")
        print(f"✅ Currency: {result.get('currency')}")
        
        # Get detailed shop info
        print("\n📊 Fetching detailed shop information...")
        shop_info = connector.get_shop_details()
        if shop_info:
            print("✅ Shop Info Retrieved:")
            print(json.dumps(shop_info, indent=2))
        
        # Show OAuth URL for advanced features
        oauth_url = connector.get_oauth_authorization_url()
        if oauth_url:
            print(f"\n🔐 OAuth URL for advanced features:")
            print(oauth_url)
    
    elif 'help' in result:
        print(f"💡 Help: {result['help']}")
    
    print(f"\n{connector.get_legal_disclaimer()}")

if __name__ == "__main__":
    main()