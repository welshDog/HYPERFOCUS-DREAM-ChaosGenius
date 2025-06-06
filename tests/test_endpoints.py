#!/usr/bin/env python3
"""
Quick endpoint test to verify our API endpoints are working
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from dashboard_api import app

    print("✅ Successfully imported dashboard_api")

    # Check if our endpoints are registered
    endpoints_to_check = ['/api/ai-squad/start', '/api/hyperfocus-analytics']

    print("\n🔍 Checking endpoint registration:")
    for rule in app.url_map.iter_rules():
        if any(endpoint in rule.rule for endpoint in endpoints_to_check):
            print(f"  ✅ Found: {rule.rule} -> {rule.endpoint}")

    # Test the endpoints with the test client
    print("\n🧪 Testing endpoints:")
    with app.test_client() as client:
        # Test ai-squad/start
        response = client.post('/api/ai-squad/start',
                             json={'project': 'Test Project', 'energy_level': 'high'},
                             content_type='application/json')
        print(f"  POST /api/ai-squad/start: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"    ✅ Response: {data.get('status', 'unknown')}")
        else:
            print(f"    ❌ Error: {response.status_code}")

        # Test hyperfocus-analytics
        response = client.get('/api/hyperfocus-analytics')
        print(f"  GET /api/hyperfocus-analytics: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"    ✅ Response status: {data.get('status', 'unknown')}")
        else:
            print(f"    ❌ Error: {response.status_code}")

    print("\n🎉 Endpoint test complete!")

except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
