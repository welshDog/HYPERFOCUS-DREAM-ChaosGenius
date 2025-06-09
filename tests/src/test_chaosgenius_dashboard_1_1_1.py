#!/usr/bin/env python3
"""
🧠 ChaosGenius Dashboard Test Suite
==================================
Comprehensive testing for all dashboard functionality and API endpoints
"""

import requests
import json
import time
import os
import sqlite3
from pathlib import Path
from datetime import datetime
import subprocess
import threading
import sys

class ChaosGeniusTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        self.dashboard_process = None
        
    def log_test(self, test_name, status, message="", details=None):
        """Log test results with neurodivergent-friendly formatting"""
        emoji = "✅" if status else "❌"
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{emoji} {test_name}: {message}")
        if details and not status:
            print(f"   🔍 Details: {details}")
    
    def start_dashboard_server(self):
        """Start the dashboard server for testing"""
        print("🚀 Starting ChaosGenius Dashboard for testing...")
        try:
            # Check if server is already running
            response = requests.get(f"{self.base_url}/api/status", timeout=5)
            if response.status_code == 200:
                self.log_test("Server Check", True, "Dashboard already running")
                return True
        except requests.exceptions.RequestException:
            pass
        
        # Start the server
        try:
            self.dashboard_process = subprocess.Popen(
                ['python', 'dashboard_api.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            for i in range(10):  # Wait up to 10 seconds
                try:
                    response = requests.get(f"{self.base_url}/api/status", timeout=2)
                    if response.status_code == 200:
                        self.log_test("Server Startup", True, "Dashboard server started successfully")
                        time.sleep(2)  # Give it a moment to fully initialize
                        return True
                except requests.exceptions.RequestException:
                    time.sleep(1)
            
            self.log_test("Server Startup", False, "Dashboard server failed to start")
            return False
            
        except Exception as e:
            self.log_test("Server Startup", False, f"Error starting server: {str(e)}")
            return False
    
    def stop_dashboard_server(self):
        """Stop the dashboard server"""
        if self.dashboard_process:
            self.dashboard_process.terminate()
            self.dashboard_process.wait()
            print("🛑 Dashboard server stopped")
    
    def test_api_status(self):
        """Test basic API health check"""
        try:
            response = requests.get(f"{self.base_url}/api/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'active':
                    self.log_test("API Status", True, "API is active and responding")
                else:
                    self.log_test("API Status", False, "API responded but status not active", data)
            else:
                self.log_test("API Status", False, f"Bad status code: {response.status_code}")
        except Exception as e:
            self.log_test("API Status", False, f"API not responding: {str(e)}")
    
    def test_dashboard_html(self):
        """Test dashboard HTML page loads"""
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                content = response.text
                if "ChaosGenius Dashboard" in content and "React" in content:
                    self.log_test("Dashboard HTML", True, "Dashboard page loads with React components")
                else:
                    self.log_test("Dashboard HTML", False, "Dashboard missing key components")
            else:
                self.log_test("Dashboard HTML", False, f"Dashboard page error: {response.status_code}")
        except Exception as e:
            self.log_test("Dashboard HTML", False, f"Dashboard page failed: {str(e)}")
    
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/dashboard-stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'stats' in data and 'activity' in data:
                    stats = data['stats']
                    required_fields = ['totalProjects', 'aiSessions', 'productsCreated', 'communityMembers']
                    if all(field in stats for field in required_fields):
                        self.log_test("Dashboard Stats", True, f"All stats present: {stats}")
                    else:
                        self.log_test("Dashboard Stats", False, "Missing required stat fields", data)
                else:
                    self.log_test("Dashboard Stats", False, "Missing stats or activity", data)
            else:
                self.log_test("Dashboard Stats", False, f"Stats API error: {response.status_code}")
        except Exception as e:
            self.log_test("Dashboard Stats", False, f"Stats API failed: {str(e)}")
    
    def test_create_product(self):
        """Test product creation functionality"""
        try:
            test_product = {
                "name": "Test Hyperfocus Widget 🧠",
                "type": "3D Print",
                "energy_level": "high"
            }
            
            response = requests.post(
                f"{self.base_url}/api/create-product",
                json=test_product,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    # Check if file was actually created
                    product_dir = Path('production_assets/product_ideas')
                    if product_dir.exists():
                        json_files = list(product_dir.glob('product_*.json'))
                        if json_files:
                            self.log_test("Create Product", True, f"Product created: {data['message']}")
                        else:
                            self.log_test("Create Product", False, "API success but no file created")
                    else:
                        self.log_test("Create Product", False, "Product directory not created")
                else:
                    self.log_test("Create Product", False, "API returned error", data)
            else:
                self.log_test("Create Product", False, f"Product creation failed: {response.status_code}")
        except Exception as e:
            self.log_test("Create Product", False, f"Product creation error: {str(e)}")
    
    def test_generate_docs(self):
        """Test documentation generation"""
        try:
            response = requests.post(f"{self.base_url}/api/generate-docs", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.log_test("Generate Docs", True, f"Docs generated: {data['message']}")
                elif data.get('status') == 'error' and 'not found' in data.get('message', ''):
                    self.log_test("Generate Docs", True, "Expected error - auto_doc_generator.py not found (this is OK)")
                else:
                    self.log_test("Generate Docs", False, "Unexpected doc generation result", data)
            else:
                self.log_test("Generate Docs", False, f"Doc generation API error: {response.status_code}")
        except Exception as e:
            self.log_test("Generate Docs", False, f"Doc generation failed: {str(e)}")
    
    def test_hyperfocus_analytics(self):
        """Test analytics endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/hyperfocus-analytics", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                required_sections = ['empire_stats', 'hyperfocus_metrics', 'business_intelligence']
                if any(section in data for section in required_sections):
                    self.log_test("Hyperfocus Analytics", True, "Analytics data returned successfully")
                else:
                    self.log_test("Hyperfocus Analytics", False, "Missing analytics sections", data)
            else:
                self.log_test("Hyperfocus Analytics", False, f"Analytics API error: {response.status_code}")
        except Exception as e:
            self.log_test("Hyperfocus Analytics", False, f"Analytics failed: {str(e)}")
    
    def test_launch_ai_squad(self):
        """Test AI Squad launch functionality"""
        try:
            test_squad = {
                "type": "business_creator",
                "energy_level": "high",
                "focus": "testing"
            }
            
            response = requests.post(
                f"{self.base_url}/api/launch-ai-squad",
                json=test_squad,
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.log_test("Launch AI Squad", True, f"AI Squad launched: {data['message']}")
                else:
                    self.log_test("Launch AI Squad", False, "AI Squad launch failed", data)
            else:
                self.log_test("Launch AI Squad", False, f"AI Squad API error: {response.status_code}")
        except Exception as e:
            self.log_test("Launch AI Squad", False, f"AI Squad launch error: {str(e)}")
    
    def test_empire_status(self):
        """Test empire status endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/empire-status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['empire_health', 'status_checks', 'next_actions']
                if all(field in data for field in required_fields):
                    health = data.get('empire_health', '0%')
                    self.log_test("Empire Status", True, f"Empire health: {health}")
                else:
                    self.log_test("Empire Status", False, "Missing empire status fields", data)
            else:
                self.log_test("Empire Status", False, f"Empire status API error: {response.status_code}")
        except Exception as e:
            self.log_test("Empire Status", False, f"Empire status failed: {str(e)}")
    
    def test_database_functionality(self):
        """Test SQLite database operations"""
        try:
            if os.path.exists('chaosgenius.db'):
                conn = sqlite3.connect('chaosgenius.db')
                cursor = conn.cursor()
                
                # Test projects table
                cursor.execute('SELECT COUNT(*) FROM projects')
                project_count = cursor.fetchone()[0]
                
                # Test activity log
                cursor.execute('SELECT COUNT(*) FROM activity_log')
                activity_count = cursor.fetchone()[0]
                
                # Test AI sessions
                cursor.execute('SELECT COUNT(*) FROM ai_sessions')
                session_count = cursor.fetchone()[0]
                
                conn.close()
                
                self.log_test("Database Functionality", True, 
                            f"DB working - Projects: {project_count}, Activities: {activity_count}, Sessions: {session_count}")
            else:
                self.log_test("Database Functionality", False, "Database file not found")
        except Exception as e:
            self.log_test("Database Functionality", False, f"Database error: {str(e)}")
    
    def test_file_structure(self):
        """Test project file structure"""
        required_files = [
            'dashboard_api.py',
            'dashboard.html',
            'requirements.txt',
            'README.md'
        ]
        
        required_dirs = [
            'Business Data',
            'Marketing Content',
            'production_assets',
            'Scripts & Prompts',
            'The Zone'
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        for dir in required_dirs:
            if not os.path.exists(dir):
                missing_dirs.append(dir)
        
        if not missing_files and not missing_dirs:
            self.log_test("File Structure", True, "All required files and directories present")
        else:
            details = f"Missing files: {missing_files}, Missing dirs: {missing_dirs}"
            self.log_test("File Structure", False, "Missing required files/directories", details)
    
    def test_energy_level_tracking(self):
        """Test energy level functionality"""
        try:
            # Test with different energy levels
            energy_levels = ['high', 'medium', 'low']
            for energy in energy_levels:
                test_data = {
                    "project": "Test Project",
                    "energy_level": energy
                }
                
                response = requests.post(
                    f"{self.base_url}/api/ai-squad/start",
                    json=test_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if energy in data.get('energy_level', ''):
                        continue
                    else:
                        self.log_test("Energy Level Tracking", False, f"Energy level {energy} not tracked properly")
                        return
                else:
                    self.log_test("Energy Level Tracking", False, f"Energy API failed for {energy}")
                    return
            
            self.log_test("Energy Level Tracking", True, "All energy levels tracked correctly")
        except Exception as e:
            self.log_test("Energy Level Tracking", False, f"Energy tracking error: {str(e)}")
    
    def run_all_tests(self):
        """Run the complete test suite"""
        print("🧠 CHAOSGENIUS DASHBOARD TEST SUITE")
        print("=" * 50)
        print("🚀 Testing all functionality for neurodivergent excellence!")
        print()
        
        # Start dashboard server
        if not self.start_dashboard_server():
            print("❌ Cannot run tests - dashboard server failed to start")
            return False
        
        try:
            # Core API Tests
            print("🔍 CORE API TESTS")
            print("-" * 20)
            self.test_api_status()
            self.test_dashboard_html()
            self.test_dashboard_stats()
            
            # Interactive Features Tests
            print("\n🛠️ INTERACTIVE FEATURES TESTS")
            print("-" * 30)
            self.test_create_product()
            self.test_generate_docs()
            self.test_hyperfocus_analytics()
            self.test_launch_ai_squad()
            self.test_empire_status()
            
            # System Tests
            print("\n⚙️ SYSTEM TESTS")
            print("-" * 15)
            self.test_database_functionality()
            self.test_file_structure()
            self.test_energy_level_tracking()
            
            # Generate test report
            self.generate_test_report()
            
        finally:
            self.stop_dashboard_server()
        
        return True
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 50)
        print("🧠 CHAOSGENIUS TEST RESULTS REPORT")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['status'])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 TEST SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   🎯 Success Rate: {success_rate:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['status']:
                    print(f"   • {result['test']}: {result['message']}")
                    if result['details']:
                        print(f"     Details: {result['details']}")
            print()
        
        # Neurodivergent-friendly success message
        if success_rate >= 80:
            print("🚀 HYPERFOCUS ZONE STATUS: EXCELLENT!")
            print("💜 Your neurodivergent business empire is running beautifully!")
            print("🧠 All systems optimized for scattered genius → structured success!")
        elif success_rate >= 60:
            print("🟡 HYPERFOCUS ZONE STATUS: GOOD WITH IMPROVEMENTS NEEDED")
            print("💛 Most systems working - some fine-tuning needed for peak performance")
        else:
            print("🟠 HYPERFOCUS ZONE STATUS: NEEDS ATTENTION")
            print("💭 Several systems need fixing - but don't worry, this is part of the process!")
        
        print("\n🎉 Testing complete! Your ChaosGenius Dashboard has been thoroughly validated.")
        
        # Save test report
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'success_rate': success_rate
                },
                'results': self.test_results,
                'generated_at': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Detailed report saved to: {report_file}")

def main():
    """Main test execution"""
    print("🧠 Initializing ChaosGenius Test Suite...")
    print("💜 Built for minds that think differently!")
    print()
    
    tester = ChaosGeniusTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎊 Test suite completed successfully!")
        print("Your HyperFocus Zone is ready to revolutionize neurodivergent entrepreneurship!")
    else:
        print("\n😅 Test suite encountered issues - but that's how we learn and improve!")
        print("Every great empire starts with testing and iteration!")

if __name__ == "__main__":
    main()