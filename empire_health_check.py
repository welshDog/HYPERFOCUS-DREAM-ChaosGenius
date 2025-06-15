#!/usr/bin/env python3
"""
🌩️💜 CHAOSGENIUS EMPIRE HEALTH CHECK
Comprehensive API verification for your Cloudflare empire
"""

import os
import requests
import json
from datetime import datetime

# Set environment from the .env file location
os.chdir('/root/chaosgenius')

class EmpireHealthChecker:
    def __init__(self):
        self.results = {}
        self.load_config()

    def load_config(self):
        """Load configuration from .env file"""
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
            print("✅ Configuration loaded from .env")
        except Exception as e:
            print(f"❌ Error loading .env: {e}")

    def check_cloudflare(self):
        """🌩️ Check Cloudflare API connectivity"""
        print("\n🌩️ CHECKING CLOUDFLARE EMPIRE...")

        api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        zone_id = os.getenv('CLOUDFLARE_ZONE_ID')

        if not api_token or 'your_' in api_token:
            self.results['cloudflare'] = {'status': 'MISSING', 'message': 'API token not configured'}
            return

        try:
            headers = {
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json'
            }

            # Test token verification
            response = requests.get(
                'https://api.cloudflare.com/client/v4/user/tokens/verify',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                token_data = response.json()
                print(f"✅ Cloudflare Token: ACTIVE")
                print(f"   Token ID: {token_data['result']['id']}")

                # Test zone access
                zone_response = requests.get(
                    f'https://api.cloudflare.com/client/v4/zones/{zone_id}',
                    headers=headers,
                    timeout=10
                )

                if zone_response.status_code == 200:
                    zone_data = zone_response.json()
                    domain = zone_data['result']['name']
                    print(f"✅ Zone Access: {domain}")
                    print(f"   Status: {zone_data['result']['status']}")

                    self.results['cloudflare'] = {
                        'status': 'OPERATIONAL',
                        'domain': domain,
                        'zone_status': zone_data['result']['status']
                    }
                else:
                    print(f"❌ Zone access failed: {zone_response.status_code}")
                    self.results['cloudflare'] = {'status': 'ZONE_ERROR', 'code': zone_response.status_code}
            else:
                print(f"❌ Token verification failed: {response.status_code}")
                self.results['cloudflare'] = {'status': 'TOKEN_ERROR', 'code': response.status_code}

        except Exception as e:
            print(f"❌ Cloudflare connection error: {e}")
            self.results['cloudflare'] = {'status': 'CONNECTION_ERROR', 'error': str(e)}

    def check_openai(self):
        """🤖 Check OpenAI API"""
        print("\n🤖 CHECKING OPENAI POWER...")

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or 'your_' in api_key:
            self.results['openai'] = {'status': 'MISSING'}
            print("⚠️  OpenAI API key not configured")
            return

        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            response = requests.get(
                'https://api.openai.com/v1/models',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                models = response.json()
                model_count = len(models.get('data', []))
                print(f"✅ OpenAI: CONNECTED")
                print(f"   Available models: {model_count}")
                self.results['openai'] = {'status': 'OPERATIONAL', 'models': model_count}
            else:
                print(f"❌ OpenAI error: {response.status_code}")
                self.results['openai'] = {'status': 'ERROR', 'code': response.status_code}

        except Exception as e:
            print(f"❌ OpenAI connection error: {e}")
            self.results['openai'] = {'status': 'CONNECTION_ERROR', 'error': str(e)}

    def check_discord(self):
        """🎮 Check Discord Bot"""
        print("\n🎮 CHECKING DISCORD BOT...")

        bot_token = os.getenv('DISCORD_BOT_TOKEN')
        if not bot_token or 'your_' in bot_token:
            self.results['discord'] = {'status': 'MISSING'}
            print("⚠️  Discord bot token not configured")
            return

        try:
            headers = {
                'Authorization': f'Bot {bot_token}',
                'Content-Type': 'application/json'
            }

            response = requests.get(
                'https://discord.com/api/v10/users/@me',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                bot_data = response.json()
                print(f"✅ Discord Bot: {bot_data['username']}")
                print(f"   Bot ID: {bot_data['id']}")
                self.results['discord'] = {
                    'status': 'OPERATIONAL',
                    'username': bot_data['username'],
                    'id': bot_data['id']
                }
            else:
                print(f"❌ Discord error: {response.status_code}")
                self.results['discord'] = {'status': 'ERROR', 'code': response.status_code}

        except Exception as e:
            print(f"❌ Discord connection error: {e}")
            self.results['discord'] = {'status': 'CONNECTION_ERROR', 'error': str(e)}

    def check_ecommerce(self):
        """🛒 Check E-commerce APIs"""
        print("\n🛒 CHECKING E-COMMERCE EMPIRE...")

        # Check Etsy
        etsy_key = os.getenv('ETSY_API_KEY')
        if etsy_key and 'your_' not in etsy_key:
            print("✅ Etsy API key configured")
            self.results['etsy'] = {'status': 'CONFIGURED'}
        else:
            print("⚠️  Etsy API key not configured")
            self.results['etsy'] = {'status': 'MISSING'}

        # Check TikTok
        tiktok_key = os.getenv('TIKTOK_CLIENT_KEY')
        if tiktok_key and 'your_' not in tiktok_key:
            print("✅ TikTok API key configured")
            self.results['tiktok'] = {'status': 'CONFIGURED'}
        else:
            print("⚠️  TikTok API key not configured")
            self.results['tiktok'] = {'status': 'MISSING'}

    def generate_empire_report(self):
        """📊 Generate comprehensive empire status report"""
        print("\n" + "="*60)
        print("🌩️💜 CHAOSGENIUS EMPIRE STATUS REPORT")
        print("="*60)

        operational_count = 0
        total_services = len(self.results)

        for service, data in self.results.items():
            status = data.get('status', 'UNKNOWN')
            if status in ['OPERATIONAL', 'CONFIGURED']:
                operational_count += 1
                status_icon = "🟢"
            elif status == 'MISSING':
                status_icon = "⚪"
            else:
                status_icon = "🔴"

            print(f"{status_icon} {service.upper()}: {status}")

        health_percentage = (operational_count / total_services) * 100 if total_services > 0 else 0

        print(f"\n💜 EMPIRE HEALTH: {health_percentage:.1f}% ({operational_count}/{total_services})")

        if health_percentage >= 80:
            print("🚀 EMPIRE STATUS: READY FOR WORLD DOMINATION!")
        elif health_percentage >= 60:
            print("⚡ EMPIRE STATUS: STRONG - MINOR OPTIMIZATIONS NEEDED")
        elif health_percentage >= 40:
            print("⚠️  EMPIRE STATUS: MODERATE - SOME CONFIGURATION REQUIRED")
        else:
            print("🔧 EMPIRE STATUS: NEEDS SETUP - MAJOR CONFIGURATION REQUIRED")

        print(f"\n📅 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return health_percentage

def main():
    print("🌩️💜 CHAOSGENIUS EMPIRE HEALTH CHECK STARTING...")
    print("=" * 60)

    checker = EmpireHealthChecker()

    # Run all checks
    checker.check_cloudflare()
    checker.check_openai()
    checker.check_discord()
    checker.check_ecommerce()

    # Generate final report
    health = checker.generate_empire_report()

    if health >= 80:
        print("\n🎊 CONGRATULATIONS! Your empire is ready to DOMINATE! 🌍💜")

    return checker.results

if __name__ == "__main__":
    main()