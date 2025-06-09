#!/usr/bin/env python3
"""
🛍️ HYPERFOCUS DREAM - Etsy Shop ID Finder
==========================================
Auto-detect your Shop ID using the Etsy API and your API key
ADHD-Optimized with clear instructions and error handling
"""

import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import json

# Load environment variables
load_dotenv()

def find_shop_id_by_name(shop_name: str, api_key: str) -> Dict[str, Any]:
    """Find shop ID using shop name"""
    url = f"https://openapi.etsy.com/v3/application/shops/{shop_name}"
    headers = {"x-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'status': 'success',
                'shop_id': data.get('shop_id'),
                'shop_name': data.get('shop_name'),
                'currency': data.get('currency_code', 'USD'),
                'user_id': data.get('user_id'),
                'full_data': data
            }
        elif response.status_code == 404:
            return {
                'status': 'error',
                'message': f'❌ Shop "{shop_name}" not found. Check spelling and try again.',
                'suggestion': 'Make sure the shop name is exactly as it appears in your Etsy URL'
            }
        elif response.status_code == 401:
            return {
                'status': 'error',
                'message': '❌ Invalid API key. Check your ETSY_API_KEY in .env file',
                'suggestion': 'Get your API key from https://www.etsy.com/developers/your-account'
            }
        else:
            return {
                'status': 'error',
                'message': f'❌ API Error: {response.status_code}',
                'response_text': response.text[:200]
            }
            
    except requests.RequestException as e:
        return {
            'status': 'error',
            'message': f'❌ Connection failed: {str(e)}',
            'suggestion': 'Check your internet connection'
        }

def find_my_shops(api_key: str) -> Dict[str, Any]:
    """Find all shops associated with the API key (requires OAuth)"""
    # Note: This endpoint typically requires OAuth, but let's try the basic endpoint
    url = "https://openapi.etsy.com/v3/application/users/me/shops"
    headers = {"x-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            shops = data.get('results', [])
            return {
                'status': 'success',
                'shops': shops,
                'count': len(shops)
            }
        else:
            return {
                'status': 'error',
                'message': 'OAuth required for this endpoint',
                'suggestion': 'Use shop name method instead'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }

def update_env_file(shop_id: str) -> bool:
    """Update .env file with the found shop ID"""
    try:
        env_path = '.env'
        
        # Read current .env file
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Update or add ETSY_SHOP_ID
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('ETSY_SHOP_ID='):
                lines[i] = f'ETSY_SHOP_ID={shop_id}\n'
                updated = True
                break
        
        if not updated:
            lines.append(f'ETSY_SHOP_ID={shop_id}\n')
        
        # Write back to file
        with open(env_path, 'w') as f:
            f.writelines(lines)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")
        return False

def interactive_shop_finder():
    """Interactive shop ID finder with ADHD-friendly prompts"""
    print("🛍️ HYPERFOCUS DREAM - Etsy Shop ID Finder")
    print("=" * 50)
    print("🧠 Let's find your Etsy Shop ID automatically!")
    print()
    
    # Check for API key
    api_key = os.getenv("ETSY_API_KEY")
    if not api_key:
        print("🚨 Missing ETSY_API_KEY in .env file")
        print("📝 Please add your API key to .env file first:")
        print("   ETSY_API_KEY=your_api_key_here")
        print()
        print("💡 Get your API key from: https://www.etsy.com/developers/your-account")
        return
    
    print("✅ API key found!")
    print()
    
    # Method 1: Shop name lookup
    print("🔍 Method 1: Find by Shop Name")
    print("💡 This is usually the easiest method")
    print()
    
    while True:
        shop_name = input("Enter your Etsy shop name (or 'skip' to try other methods): ").strip()
        
        if shop_name.lower() == 'skip':
            break
            
        if not shop_name:
            print("❌ Please enter a shop name")
            continue
        
        print(f"🔍 Searching for shop: {shop_name}")
        result = find_shop_id_by_name(shop_name, api_key)
        
        if result['status'] == 'success':
            print("🎉 SUCCESS!")
            print(f"✅ Shop Name: {result['shop_name']}")
            print(f"✅ Shop ID: {result['shop_id']}")
            print(f"✅ Currency: {result['currency']}")
            print(f"✅ User ID: {result['user_id']}")
            print()
            
            # Ask to save to .env
            save = input("💾 Save this Shop ID to your .env file? (y/n): ").strip().lower()
            if save in ['y', 'yes']:
                if update_env_file(str(result['shop_id'])):
                    print("✅ Shop ID saved to .env file!")
                    print("🚀 Your Etsy integration is now ready to use!")
                else:
                    print("❌ Failed to save to .env file")
                    print(f"📝 Please manually add: ETSY_SHOP_ID={result['shop_id']}")
            else:
                print(f"📝 Your Shop ID is: {result['shop_id']}")
                print("💡 Add this to your .env file as: ETSY_SHOP_ID=" + str(result['shop_id']))
            
            return
        else:
            print(f"{result['message']}")
            if 'suggestion' in result:
                print(f"💡 {result['suggestion']}")
            print()
            
            retry = input("🔄 Try again with a different name? (y/n): ").strip().lower()
            if retry not in ['y', 'yes']:
                break
    
    # Method 2: Manual input with validation
    print()
    print("🔍 Method 2: Manual Shop ID Entry")
    print("💡 If you already know your Shop ID, enter it here for validation")
    print()
    
    while True:
        shop_id_input = input("Enter your Shop ID (or 'done' to finish): ").strip()
        
        if shop_id_input.lower() == 'done':
            break
            
        if not shop_id_input.isdigit():
            print("❌ Shop ID should be a number")
            continue
        
        # Validate the shop ID
        url = f"https://openapi.etsy.com/v3/application/shops/{shop_id_input}"
        headers = {"x-api-key": api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("🎉 Shop ID validated!")
                print(f"✅ Shop Name: {data.get('shop_name')}")
                print(f"✅ Shop ID: {data.get('shop_id')}")
                
                save = input("💾 Save to .env file? (y/n): ").strip().lower()
                if save in ['y', 'yes']:
                    if update_env_file(shop_id_input):
                        print("✅ Shop ID saved!")
                return
            else:
                print(f"❌ Invalid Shop ID: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error validating Shop ID: {e}")
    
    # Method 3: User ID lookup
    print()
    print("🔍 Method 3: Find by User ID")
    print("💡 This method uses your Etsy User ID to find your shop")
    print()
    
    while True:
        user_id = input("Enter your Etsy User ID (or 'skip' to try other methods): ").strip()
        
        if user_id.lower() == 'skip':
            break
            
        if not user_id:
            print("❌ Please enter a User ID")
            continue
        
        print(f"🔍 Searching for shop by User ID: {user_id}")
        result = find_shop_by_user_id(user_id, api_key)
        
        if result['status'] == 'success':
            print("🎉 SUCCESS!")
            print(f"✅ Shop Name: {result['shop_name']}")
            print(f"✅ Shop ID: {result['shop_id']}")
            print(f"✅ Currency: {result['currency']}")
            print(f"✅ User ID: {result['user_id']}")
            print()
            
            # Ask to save to .env
            save = input("💾 Save this Shop ID to your .env file? (y/n): ").strip().lower()
            if save in ['y', 'yes']:
                if update_env_file(str(result['shop_id'])):
                    print("✅ Shop ID saved to .env file!")
                    print("🚀 Your Etsy integration is now ready to use!")
                else:
                    print("❌ Failed to save to .env file")
                    print(f"📝 Please manually add: ETSY_SHOP_ID={result['shop_id']}")
            else:
                print(f"📝 Your Shop ID is: {result['shop_id']}")
                print("💡 Add this to your .env file as: ETSY_SHOP_ID=" + str(result['shop_id']))
            
            return
        else:
            print(f"{result['message']}")
            if 'suggestion' in result:
                print(f"💡 {result['suggestion']}")
            print()
            
            retry = input("🔄 Try again with a different User ID? (y/n): ").strip().lower()
            if retry not in ['y', 'yes']:
                break
    
    print()
    print("📚 Additional Help:")
    print("• Your shop name is in your Etsy URL: etsy.com/shop/YOUR_SHOP_NAME")
    print("• Your Shop ID can be found in your Etsy seller dashboard")
    print("• Contact Etsy support if you need help finding these details")

def find_shop_by_user_id(user_id: str, api_key: str) -> Dict[str, Any]:
    """Find shop information using Etsy User ID - Alternative method"""
    url = f"https://openapi.etsy.com/v3/application/users/{user_id}/shops"
    headers = {"x-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0:
                shop = data[0]  # Get first shop
                return {
                    'status': 'success',
                    'shop_id': shop.get('shop_id'),
                    'shop_name': shop.get('shop_name'),
                    'shop_url': f"https://www.etsy.com/shop/{shop.get('shop_name')}",
                    'currency': shop.get('currency_code', 'USD'),
                    'user_id': user_id,
                    'all_shops': data,  # In case user has multiple shops
                    'shop_count': len(data)
                }
            else:
                return {
                    'status': 'error',
                    'message': '⚠️ No shops found for this User ID',
                    'suggestion': 'Verify your User ID or check if you have an active shop'
                }
        elif response.status_code == 401:
            return {
                'status': 'error',
                'message': '❌ Invalid API key. Check your ETSY_API_KEY',
                'suggestion': 'Get your API key from https://www.etsy.com/developers/your-account'
            }
        elif response.status_code == 404:
            return {
                'status': 'error',
                'message': f'❌ User ID "{user_id}" not found',
                'suggestion': 'Double-check your Etsy User ID'
            }
        else:
            return {
                'status': 'error',
                'message': f'❌ API Error: {response.status_code}',
                'response_text': response.text[:200]
            }
            
    except requests.RequestException as e:
        return {
            'status': 'error',
            'message': f'❌ Connection failed: {str(e)}',
            'suggestion': 'Check your internet connection'
        }

def main():
    """Main function"""
    interactive_shop_finder()

if __name__ == "__main__":
    main()