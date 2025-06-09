#!/usr/bin/env python3
"""
🔧 Etsy API Key Validator & Fixer
================================
Diagnoses and fixes API key formatting issues
"""

import os
import requests
from dotenv import load_dotenv
import re

def validate_etsy_api_key():
    """Test and validate Etsy API key format and connectivity"""
    print("🔧 Etsy API Key Validator")
    print("=" * 30)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('ETSY_API_KEY')
    
    if not api_key:
        print("❌ No ETSY_API_KEY found in .env file")
        return False
    
    # Check key format
    print(f"🔍 API Key: {api_key[:8]}...{api_key[-4:]} (length: {len(api_key)})")
    
    # Etsy API keys should be 24 characters, alphanumeric
    if len(api_key) != 24:
        print(f"⚠️  Unusual key length: {len(api_key)} (expected: 24)")
    
    if not re.match(r'^[a-z0-9]+$', api_key):
        print("⚠️  Key contains unexpected characters (should be lowercase alphanumeric)")
    
    # Test basic connectivity with simplest endpoint
    print("\n🌐 Testing API connectivity...")
    
    try:
        # Test with ping endpoint (doesn't require OAuth)
        url = "https://openapi.etsy.com/v3/application/ping"
        headers = {
            'x-api-key': api_key,
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API Key is VALID! Connection successful!")
            return True
        elif response.status_code == 401:
            print("❌ API Key is INVALID or incorrectly formatted")
            print("💡 Double-check your key from https://www.etsy.com/developers/your-account")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"🌐 Connection Error: {e}")
        return False

def suggest_fixes():
    """Suggest common fixes for API key issues"""
    print("\n🔧 COMMON FIXES:")
    print("1. Remove any quotes around your API key in .env")
    print("2. Make sure no spaces before/after the key")
    print("3. Regenerate key at https://www.etsy.com/developers/your-account")
    print("4. Ensure your Etsy app has 'Shops' permission enabled")
    print("5. Check if your key is for the correct environment (dev vs prod)")

if __name__ == "__main__":
    is_valid = validate_etsy_api_key()
    
    if not is_valid:
        suggest_fixes()
    else:
        print("\n🚀 READY FOR SHOP CONNECTION!")
        print("Your API key works - let's get your shop data!")