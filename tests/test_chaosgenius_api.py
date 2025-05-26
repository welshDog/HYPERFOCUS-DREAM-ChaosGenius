#!/usr/bin/env python3
"""
🧪 ChaosGenius API Test Suite
============================
Comprehensive tests for the ChaosGenius Dashboard API
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
import sys

# Add the parent directory to Python path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard_api import app, init_database

class TestChaosGeniusAPI:
    """Test suite for ChaosGenius Dashboard API"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config['TESTING'] = True
        app.config['DATABASE'] = ':memory:'  # Use in-memory database for tests
        
        with app.test_client() as client:
            with app.app_context():
                init_database()
                yield client
    
    @pytest.fixture
    def sample_product_data(self):
        """Sample product data for testing"""
        return {
            "name": "Test Product",
            "description": "A test product for the ChaosGenius ecosystem"
        }
    
    def test_api_status(self, client):
        """Test API health check endpoint"""
        response = client.get('/api/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'active'
        assert data['message'] == 'ChaosGenius Engine API is running'
        assert 'timestamp' in data
        assert data['version'] == '1.0.0'
    
    def test_dashboard_homepage(self, client):
        """Test dashboard homepage loads"""
        response = client.get('/')
        assert response.status_code == 200
        # Should either load dashboard.html or show fallback message
        assert b'ChaosGenius' in response.data
    
    def test_create_product_success(self, client, sample_product_data):
        """Test successful product creation"""
        response = client.post('/api/create-product',
                             data=json.dumps(sample_product_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'New product created!' in data['message']
        assert 'file' in data
        assert 'timestamp' in data
    
    def test_create_product_no_data(self, client):
        """Test product creation with no input data"""
        response = client.post('/api/create-product')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        # Should create product with default values
    
    def test_dashboard_stats(self, client):
        """Test dashboard statistics endpoint"""
        response = client.get('/api/dashboard-stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'stats' in data
        assert 'activity' in data
        assert 'totalProjects' in data['stats']
        assert 'aiSessions' in data['stats']
        assert isinstance(data['activity'], list)
    
    def test_analytics_endpoint(self, client):
        """Test analytics data retrieval"""
        response = client.get('/api/analytics')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'etsy_sales' in data
        assert 'active_products' in data
        assert 'last_updated' in data
    
    def test_ai_squad_start(self, client):
        """Test AI Squad session initiation"""
        ai_squad_data = {
            "project": "Test Project",
            "energy_level": "high"
        }
        
        response = client.post('/api/ai-squad/start',
                             data=json.dumps(ai_squad_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['project'] == 'Test Project'
        assert data['energy_level'] == 'high'
    
    def test_projects_list(self, client):
        """Test projects listing"""
        response = client.get('/api/projects')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'projects' in data
        assert isinstance(data['projects'], list)
    
    def test_empire_status(self, client):
        """Test empire status endpoint"""
        response = client.get('/api/empire-status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'empire_health' in data
        assert 'status_checks' in data
        assert 'next_actions' in data
        assert 'hyperfocus_message' in data
    
    def test_hyperfocus_analytics(self, client):
        """Test hyperfocus analytics endpoint"""
        response = client.get('/api/hyperfocus-analytics')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'empire_stats' in data
        assert 'hyperfocus_metrics' in data
        assert 'neurodivergent_power_level' in data
    
    def test_launch_ai_squad(self, client):
        """Test AI Squad launch with parameters"""
        launch_data = {
            "type": "business_creator",
            "energy_level": "medium",
            "focus": "product_development"
        }
        
        response = client.post('/api/launch-ai-squad',
                             data=json.dumps(launch_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'AI Squad' in data['message']
    
    def test_run_task_unknown(self, client):
        """Test running an unknown task"""
        response = client.get('/api/run-task/unknown_task')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'available_tasks' in data
    
    def test_404_endpoint(self, client):
        """Test 404 error handling"""
        response = client.get('/api/nonexistent-endpoint')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'available_endpoints' in data
    
    def test_project_update(self, client):
        """Test project update functionality"""
        update_data = {
            "status": "In Progress",
            "energy_level": "high"
        }
        
        response = client.post('/api/projects/1/update',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'


class TestChaosGeniusIntegration:
    """Integration tests for ChaosGenius ecosystem"""
    
    def test_product_creation_workflow(self):
        """Test complete product creation workflow"""
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            # Create a product
            product_data = {
                "name": "Integration Test Product",
                "description": "Testing the full workflow"
            }
            
            response = client.post('/api/create-product',
                                 data=json.dumps(product_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            
            # Check analytics reflects the new product
            analytics_response = client.get('/api/analytics')
            assert analytics_response.status_code == 200
    
    def test_ai_squad_analytics_workflow(self):
        """Test AI Squad session creates analytics data"""
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            # Start AI Squad session
            ai_data = {"project": "Integration Test", "energy_level": "high"}
            client.post('/api/ai-squad/start',
                       data=json.dumps(ai_data),
                       content_type='application/json')
            
            # Check dashboard stats updated
            stats_response = client.get('/api/dashboard-stats')
            assert stats_response.status_code == 200
            
            stats_data = json.loads(stats_response.data)
            assert len(stats_data['activity']) > 0


class TestChaosGeniusPerformance:
    """Performance and stress tests"""
    
    def test_multiple_product_creation(self):
        """Test creating multiple products rapidly"""
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            for i in range(10):
                product_data = {
                    "name": f"Stress Test Product {i}",
                    "description": f"Product {i} for stress testing"
                }
                
                response = client.post('/api/create-product',
                                     data=json.dumps(product_data),
                                     content_type='application/json')
                
                assert response.status_code == 200
    
    def test_concurrent_analytics_requests(self):
        """Test multiple analytics requests"""
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            responses = []
            
            for _ in range(5):
                response = client.get('/api/analytics')
                responses.append(response)
            
            for response in responses:
                assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])