#!/usr/bin/env python3
"""
🛍️ HYPERFOCUS DREAM - Quick Etsy Shop Finder
=============================================
Using your User ID method for instant shop detection
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def quick_find_shop():
    """Quick shop finder using User ID - your method"""
    ETSY_API_KEY = os.getenv("ETSY_API_KEY")
    USER_ID = "1059596248"  # Your Etsy user ID
    
    if not ETSY_API_KEY:
        print("🚨 Missing ETSY_API_KEY in .env file")
        return
    
    def get_shop_info_from_user(user_id):
        url = f"https://openapi.etsy.com/v3/application/users/{user_id}/shops"
        headers = {"x-api-key": ETSY_API_KEY}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                shop = data[0]
                print("✅ Shop Found:")
                print(f"🆔 shop_id: {shop['shop_id']}")
                print(f"🏪 shop_name: {shop['shop_name']}")
                print(f"🌍 shop_url: https://www.etsy.com/shop/{shop['shop_name']}")
                return shop
            else:
                print("⚠️ No shop data found for that user.")
                return None
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
    
    print("🛍️ HYPERFOCUS DREAM - Quick Shop Finder")
    print("=" * 40)
    print(f"🔍 Looking up User ID: {USER_ID}")
    
    shop_info = get_shop_info_from_user(USER_ID)
    
    if shop_info:
        # Auto-update .env file
        env_path = '.env'
        shop_id = shop_info['shop_id']
        
        try:
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            # Update ETSY_SHOP_ID
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('ETSY_SHOP_ID='):
                    lines[i] = f'ETSY_SHOP_ID={shop_id}\n'
                    updated = True
                    break
            
            if not updated:
                lines.append(f'ETSY_SHOP_ID={shop_id}\n')
            
            with open(env_path, 'w') as f:
                f.writelines(lines)
            
            print("💾 Shop ID automatically saved to .env file!")
            print("🚀 Your Etsy integration is now ready!")
            
        except Exception as e:
            print(f"❌ Could not update .env file: {e}")
            print(f"📝 Please manually add: ETSY_SHOP_ID={shop_id}")

if __name__ == "__main__":
    quick_find_shop()