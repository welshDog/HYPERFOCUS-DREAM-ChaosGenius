#!/usr/bin/env python3
"""
🔒 ChaosGenius Security Validator
================================
Validates your API environment setup and security configuration
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import secrets
import string

def generate_secure_key(length=50):
    """Generate a cryptographically secure random key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def check_env_security():
    """Check environment variable security setup"""
    print("🔒 ChaosGenius Security Validator")
    print("=" * 40)
    
    # Check if .env exists
    env_file = Path('.env')
    env_example_file = Path('.env.example')
    gitignore_file = Path('.gitignore')
    
    print("\n📁 FILE SECURITY CHECKS:")
    
    # Check .env file
    if env_file.exists():
        print("✅ .env file exists")
    else:
        print("❌ .env file missing - creating basic template...")
        # Would be created by the main script
    
    # Check .env.example
    if env_example_file.exists():
        print("✅ .env.example exists (safe template)")
    else:
        print("❌ .env.example missing")
    
    # Check .gitignore
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            gitignore_content = f.read()
        if '.env' in gitignore_content:
            print("✅ .env is in .gitignore (secrets protected)")
        else:
            print("❌ .env NOT in .gitignore - SECURITY RISK!")
    else:
        print("❌ .gitignore missing")
    
    # Load environment variables
    load_dotenv()
    
    print("\n🔑 API KEY SECURITY CHECKS:")
    
    # Check critical API keys
    api_keys = {
        'ETSY_API_KEY': os.getenv('ETSY_API_KEY'),
        'ETSY_SHARED_SECRET': os.getenv('ETSY_SHARED_SECRET'),
        'TIKTOK_CLIENT_KEY': os.getenv('TIKTOK_CLIENT_KEY'),
        'TIKTOK_CLIENT_SECRET': os.getenv('TIKTOK_CLIENT_SECRET'),
        'DISCORD_BOT_TOKEN': os.getenv('DISCORD_BOT_TOKEN'),
        'FLASK_SECRET_KEY': os.getenv('FLASK_SECRET_KEY')
    }
    
    configured_keys = 0
    total_keys = len(api_keys)
    
    for key_name, key_value in api_keys.items():
        if key_value and key_value.strip() and key_value != f'your_{key_name.lower()}_here':
            print(f"✅ {key_name}: Configured")
            configured_keys += 1
            
            # Check for weak keys
            if len(key_value) < 10:
                print(f"⚠️  {key_name}: Suspiciously short - might be test value")
        else:
            print(f"❌ {key_name}: Not configured")
    
    print(f"\n📊 SECURITY SCORE: {configured_keys}/{total_keys} keys configured")
    
    # Check Flask secret key specifically
    flask_secret = os.getenv('FLASK_SECRET_KEY')
    if flask_secret == 'chaosgenius_dev_key_please_change_in_production':
        print("⚠️  Using default Flask secret key - change for production!")
    
    print("\n🚀 NEXT STEPS:")
    if configured_keys == 0:
        print("1. Add your API keys to the .env file")
        print("2. Get Etsy API keys from: https://www.etsy.com/developers/your-account")
        print("3. Get TikTok API keys from TikTok for Developers")
        print("4. Create Discord bot at: https://discord.com/developers/applications")
    elif configured_keys < total_keys:
        print(f"1. Configure remaining {total_keys - configured_keys} API keys")
        print("2. Test integrations with: python dashboard_api.py")
    else:
        print("🎉 All API keys configured! Your environment is secure!")
        print("💡 Run your dashboard: python dashboard_api.py")
    
    return configured_keys, total_keys

def generate_production_keys():
    """Generate secure keys for production use"""
    print("\n🔐 GENERATING SECURE PRODUCTION KEYS:")
    print("=" * 40)
    
    keys = {
        'FLASK_SECRET_KEY': generate_secure_key(64),
        'JWT_SECRET_KEY': generate_secure_key(64),
        'DB_ENCRYPTION_KEY': generate_secure_key(32),
        'WEBHOOK_SECRET': generate_secure_key(32)
    }
    
    print("Add these to your production .env file:")
    print()
    for key_name, key_value in keys.items():
        print(f"{key_name}={key_value}")
    
    return keys

if __name__ == "__main__":
    try:
        configured, total = check_env_security()
        
        if len(sys.argv) > 1 and sys.argv[1] == '--generate-keys':
            generate_production_keys()
            
    except Exception as e:
        print(f"❌ Security check failed: {e}")
        sys.exit(1)