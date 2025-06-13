"""
🌐 CHAOSGENIUS SOCIAL MEDIA FEEDS
Real-time API integration for Etsy, TikTok, and other platforms
"""

import requests
import json
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class SocialMediaFeeds:
    def __init__(self):
        self.etsy_api_key = os.getenv('ETSY_API_KEY')
        self.etsy_shop_id = os.getenv('ETSY_SHOP_ID')
        self.tiktok_access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
        self.tiktok_client_key = os.getenv('TIKTOK_CLIENT_KEY')
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_etsy_shop_stats(self):
        """Fetch real Etsy shop statistics"""
        try:
            # Etsy API v3 endpoints
            headers = {
                'x-api-key': self.etsy_api_key,
                'Content-Type': 'application/json'
            }
            
            # Get shop stats
            shop_url = f"https://openapi.etsy.com/v3/application/shops/{self.etsy_shop_id}"
            shop_response = requests.get(shop_url, headers=headers)
            
            if shop_response.status_code == 200:
                shop_data = shop_response.json()
                
                # Get recent transactions
                transactions_url = f"https://openapi.etsy.com/v3/application/shops/{self.etsy_shop_id}/transactions"
                transactions_response = requests.get(transactions_url, headers=headers)
                
                transactions_data = transactions_response.json() if transactions_response.status_code == 200 else {}
                
                return {
                    'shop_name': shop_data.get('shop_name', 'Your Shop'),
                    'total_sales': shop_data.get('num_favorers', 0),
                    'recent_sales': len(transactions_data.get('results', [])),
                    'shop_views': shop_data.get('num_favorers', 0),
                    'listings_count': shop_data.get('listing_active_count', 0),
                    'last_updated': datetime.now().isoformat()
                }
            else:
                self.logger.error(f"Etsy API Error: {shop_response.status_code}")
                return self._get_demo_etsy_data()
                
        except Exception as e:
            self.logger.error(f"Etsy API Exception: {e}")
            return self._get_demo_etsy_data()
    
    def get_tiktok_creator_stats(self):
        """Fetch real TikTok creator statistics"""
        try:
            headers = {
                'Authorization': f'Bearer {self.tiktok_access_token}',
                'Content-Type': 'application/json'
            }
            
            # TikTok Creator API endpoints
            user_info_url = "https://open-api.tiktok.com/creator/v1/user/info/"
            video_list_url = "https://open-api.tiktok.com/creator/v1/video/list/"
            
            # Get user info
            user_response = requests.get(user_info_url, headers=headers)
            
            if user_response.status_code == 200:
                user_data = user_response.json()
                
                # Get video stats
                video_response = requests.get(video_list_url, headers=headers)
                video_data = video_response.json() if video_response.status_code == 200 else {}
                
                videos = video_data.get('data', {}).get('videos', [])
                total_views = sum(video.get('statistics', {}).get('view_count', 0) for video in videos)
                total_likes = sum(video.get('statistics', {}).get('like_count', 0) for video in videos)
                
                return {
                    'username': user_data.get('data', {}).get('display_name', 'Your TikTok'),
                    'followers': user_data.get('data', {}).get('follower_count', 0),
                    'total_views': total_views,
                    'total_likes': total_likes,
                    'video_count': len(videos),
                    'engagement_rate': (total_likes / max(total_views, 1)) * 100,
                    'last_updated': datetime.now().isoformat()
                }
            else:
                self.logger.error(f"TikTok API Error: {user_response.status_code}")
                return self._get_demo_tiktok_data()
                
        except Exception as e:
            self.logger.error(f"TikTok API Exception: {e}")
            return self._get_demo_tiktok_data()
    
    def _get_demo_etsy_data(self):
        """Demo data when API is not configured"""
        import random
        base_sales = 1250
        daily_variation = random.randint(-15, 45)
        
        return {
            'shop_name': 'ChaosGenius Creations',
            'total_sales': base_sales + daily_variation,
            'recent_sales': random.randint(5, 25),
            'shop_views': random.randint(850, 1200),
            'listings_count': random.randint(45, 78),
            'last_updated': datetime.now().isoformat(),
            'demo_mode': True
        }
    
    def _get_demo_tiktok_data(self):
        """Demo data when API is not configured"""
        import random
        
        return {
            'username': '@chaosgenius_zone',
            'followers': random.randint(12500, 15000),
            'total_views': random.randint(850000, 950000),
            'total_likes': random.randint(45000, 55000),
            'video_count': random.randint(125, 150),
            'engagement_rate': round(random.uniform(4.5, 7.2), 2),
            'last_updated': datetime.now().isoformat(),
            'demo_mode': True
        }
    
    def get_combined_analytics(self):
        """Get combined analytics from all platforms"""
        etsy_stats = self.get_etsy_shop_stats()
        tiktok_stats = self.get_tiktok_creator_stats()
        
        # Calculate cross-platform metrics
        total_revenue_estimate = etsy_stats.get('total_sales', 0) * 25  # Assuming avg $25 per sale
        social_reach = tiktok_stats.get('total_views', 0)
        conversion_rate = (etsy_stats.get('recent_sales', 0) / max(tiktok_stats.get('total_views', 1), 1)) * 100000
        
        return {
            'etsy': etsy_stats,
            'tiktok': tiktok_stats,
            'cross_platform_metrics': {
                'estimated_revenue': total_revenue_estimate,
                'social_reach': social_reach,
                'conversion_rate': round(conversion_rate, 4),
                'growth_momentum': self._calculate_growth_momentum(etsy_stats, tiktok_stats)
            },
            'last_updated': datetime.now().isoformat()
        }
    
    def _calculate_growth_momentum(self, etsy_data, tiktok_data):
        """Calculate overall growth momentum score"""
        etsy_score = min((etsy_data.get('recent_sales', 0) / 10) * 25, 100)
        tiktok_score = min((tiktok_data.get('engagement_rate', 0) / 8) * 50, 100)
        
        momentum = (etsy_score + tiktok_score) / 2
        
        if momentum >= 80:
            return {'score': momentum, 'status': '🚀 HYPERFOCUS ACTIVATED', 'color': '#00ff41'}
        elif momentum >= 60:
            return {'score': momentum, 'status': '⚡ Strong Growth', 'color': '#ffaa00'}
        elif momentum >= 40:
            return {'score': momentum, 'status': '📈 Building Momentum', 'color': '#0099ff'}
        else:
            return {'score': momentum, 'status': '🔧 Optimization Mode', 'color': '#ff6600'}

# Initialize the social media feeds
social_feeds = SocialMediaFeeds()

def get_live_social_data():
    """Main function to get live social media data"""
    return social_feeds.get_combined_analytics()

if __name__ == "__main__":
    # Test the feeds
    data = get_live_social_data()
    print(json.dumps(data, indent=2))