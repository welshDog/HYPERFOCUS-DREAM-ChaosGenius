#!/usr/bin/env python3
"""
🩺 ChaosGenius Health Check & Diagnostic Tool
============================================
Comprehensive system health monitoring for the neurodivergent business empire
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import importlib.util
from typing import Dict, List, Any

class ChaosGeniusHealthCheck:
    def __init__(self):
        self.health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "unknown",
            "systems": {},
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
    
    def check_python_environment(self) -> Dict[str, Any]:
        """Check Python and virtual environment status"""
        status = {
            "name": "Python Environment",
            "healthy": True,
            "details": {},
            "issues": []
        }
        
        try:
            # Python version check
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            status["details"]["python_version"] = python_version
            
            if sys.version_info < (3, 8):
                status["healthy"] = False
                status["issues"].append("Python 3.8+ required")
            
            # Virtual environment check
            in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
            status["details"]["virtual_environment"] = in_venv
            
            # Installed packages check
            try:
                import flask, requests, sqlite3
                status["details"]["core_packages"] = "installed"
            except ImportError as e:
                status["healthy"] = False
                status["issues"].append(f"Missing core packages: {e}")
            
        except Exception as e:
            status["healthy"] = False
            status["issues"].append(f"Environment check failed: {e}")
        
        return status
    
    def check_file_structure(self) -> Dict[str, Any]:
        """Verify critical files and directories exist"""
        status = {
            "name": "File Structure",
            "healthy": True,
            "details": {},
            "issues": []
        }
        
        critical_files = [
            "dashboard_api.py",
            "dashboard.html", 
            "requirements.txt",
            "startup_manager.py",
            "chaosgenius_discord_bot.py"
        ]
        
        critical_dirs = [
            "Business Data",
            "production_assets",
            "logs",
            "generated_docs"
        ]
        
        # Check files
        missing_files = []
        for file in critical_files:
            if not Path(file).exists():
                missing_files.append(file)
        
        status["details"]["missing_files"] = missing_files
        
        # Check directories
        missing_dirs = []
        for dir_path in critical_dirs:
            if not Path(dir_path).exists():
                missing_dirs.append(dir_path)
        
        status["details"]["missing_directories"] = missing_dirs
        
        if missing_files or missing_dirs:
            status["healthy"] = False
            status["issues"].extend([f"Missing file: {f}" for f in missing_files])
            status["issues"].extend([f"Missing directory: {d}" for d in missing_dirs])
        
        return status
    
    def check_database_health(self) -> Dict[str, Any]:
        """Check SQLite database integrity and structure"""
        status = {
            "name": "Database Health",
            "healthy": True,
            "details": {},
            "issues": []
        }
        
        try:
            if not Path("chaosgenius.db").exists():
                status["healthy"] = False
                status["issues"].append("Database file not found")
                return status
            
            conn = sqlite3.connect("chaosgenius.db")
            cursor = conn.cursor()
            
            # Check required tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ["projects", "ai_sessions", "activity_log"]
            missing_tables = [t for t in required_tables if t not in tables]
            
            status["details"]["tables_found"] = tables
            status["details"]["missing_tables"] = missing_tables
            
            if missing_tables:
                status["healthy"] = False
                status["issues"].extend([f"Missing table: {t}" for t in missing_tables])
            
            # Check data counts
            for table in required_tables:
                if table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    status["details"][f"{table}_count"] = count
            
            conn.close()
            
        except Exception as e:
            status["healthy"] = False
            status["issues"].append(f"Database error: {e}")
        
        return status
    
    def check_api_health(self) -> Dict[str, Any]:
        """Check if dashboard API is running and responsive"""
        status = {
            "name": "API Health",
            "healthy": True,
            "details": {},
            "issues": []
        }
        
        try:
            # Check if API is running
            response = requests.get("http://localhost:5000/api/status", timeout=5)
            status["details"]["status_code"] = response.status_code
            
            if response.status_code == 200:
                data = response.json()
                status["details"]["api_response"] = data
                
                if data.get("status") != "active":
                    status["healthy"] = False
                    status["issues"].append("API not in active state")
            else:
                status["healthy"] = False
                status["issues"].append(f"API returned status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            status["healthy"] = False
            status["issues"].append("API not running or not accessible")
        except Exception as e:
            status["healthy"] = False
            status["issues"].append(f"API check failed: {e}")
        
        return status
    
    def check_discord_bot_config(self) -> Dict[str, Any]:
        """Check Discord bot configuration"""
        status = {
            "name": "Discord Bot Config",
            "healthy": True,
            "details": {},
            "issues": []
        }
        
        try:
            # Check for environment file
            env_file = Path(".env")
            if env_file.exists():
                status["details"]["env_file"] = "found"
                
                # Check for Discord token (without exposing it)
                with open(env_file, 'r') as f:
                    content = f.read()
                    if "DISCORD_BOT_TOKEN=" in content:
                        status["details"]["discord_token"] = "configured"
                    else:
                        status["details"]["discord_token"] = "missing"
                        status["issues"].append("Discord bot token not configured")
            else:
                status["details"]["env_file"] = "missing"
                status["issues"].append(".env file not found")
                
            # Check Discord bot file
            if not Path("chaosgenius_discord_bot.py").exists():
                status["healthy"] = False
                status["issues"].append("Discord bot file missing")
                
        except Exception as e:
            status["healthy"] = False
            status["issues"].append(f"Discord config check failed: {e}")
        
        return status
    
    def check_dependencies(self) -> Dict[str, Any]:
        """Check if all required Python packages are installed"""
        status = {
            "name": "Python Dependencies",
            "healthy": True,
            "details": {},
            "issues": []
        }
        
        try:
            if not Path("requirements.txt").exists():
                status["healthy"] = False
                status["issues"].append("requirements.txt not found")
                return status
            
            with open("requirements.txt", 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
            installed_packages = []
            missing_packages = []
            
            for requirement in requirements[:10]:  # Check first 10 to avoid timeouts
                try:
                    package_name = requirement.split("==")[0].split(">=")[0].strip()
                    if package_name:
                        __import__(package_name.replace("-", "_"))
                        installed_packages.append(package_name)
                except ImportError:
                    missing_packages.append(package_name)
                except Exception:
                    continue  # Skip problematic package names
            
            status["details"]["total_requirements"] = len(requirements)
            status["details"]["checked_packages"] = len(installed_packages) + len(missing_packages)
            status["details"]["installed_packages"] = installed_packages
            status["details"]["missing_packages"] = missing_packages
            
            if missing_packages:
                status["healthy"] = False
                status["issues"].extend([f"Missing package: {p}" for p in missing_packages])
                
        except Exception as e:
            status["healthy"] = False
            status["issues"].append(f"Dependency check failed: {e}")
        
        return status
    
    def check_startup_scripts(self) -> Dict[str, Any]:
        """Check startup scripts and batch files"""
        status = {
            "name": "Startup Scripts",
            "healthy": True,
            "details": {},
            "issues": []
        }
        
        startup_files = ["start.bat", "startup_manager.py"]
        
        for file in startup_files:
            if Path(file).exists():
                status["details"][file] = "found"
            else:
                status["healthy"] = False
                status["issues"].append(f"Missing startup file: {file}")
        
        return status
    
    def generate_recommendations(self):
        """Generate recommendations based on health check results"""
        recommendations = []
        
        for system_name, system_status in self.health_report["systems"].items():
            if not system_status["healthy"]:
                if system_name == "Python Environment":
                    recommendations.append("🐍 Update Python to 3.8+ and create virtual environment")
                    recommendations.append("📦 Run: python -m venv venvve && venvve\\Scripts\\activate")
                
                elif system_name == "File Structure":
                    recommendations.append("📁 Run startup_manager.py to create missing directories")
                    recommendations.append("🔄 Re-run the ChaosGenius setup to restore missing files")
                
                elif system_name == "Database Health":
                    recommendations.append("🗄️ Run dashboard_api.py to initialize database")
                    recommendations.append("🔧 Database will auto-create on first API startup")
                
                elif system_name == "API Health":
                    recommendations.append("🚀 Start the dashboard: python dashboard_api.py")
                    recommendations.append("🌐 API should be available at http://localhost:5000")
                
                elif system_name == "Discord Bot Config":
                    recommendations.append("🤖 Create .env file with DISCORD_BOT_TOKEN=your_token")
                    recommendations.append("🔐 Get token from https://discord.com/developers/applications")
                
                elif system_name == "Python Dependencies":
                    recommendations.append("📦 Install dependencies: pip install -r requirements.txt")
                    recommendations.append("🔄 Or run start.bat which handles dependencies automatically")
        
        # General recommendations
        if self.health_report["overall_health"] != "excellent":
            recommendations.append("🧠 Run the complete test suite: python test_chaosgenius_dashboard.py")
            recommendations.append("📚 Check generated_docs/ for detailed setup instructions")
            recommendations.append("💜 Remember: Every great empire starts with solid foundations!")
        
        self.health_report["recommendations"] = recommendations
    
    def run_full_health_check(self) -> Dict[str, Any]:
        """Execute complete health check sequence"""
        print("🩺 ChaosGenius Health Check Starting...")
        print("=" * 50)
        
        # Run all health checks
        checks = [
            self.check_python_environment,
            self.check_file_structure,
            self.check_database_health,
            self.check_api_health,
            self.check_discord_bot_config,
            self.check_dependencies,
            self.check_startup_scripts
        ]
        
        healthy_systems = 0
        total_systems = len(checks)
        
        for check in checks:
            try:
                result = check()
                self.health_report["systems"][result["name"]] = result
                
                # Print status
                emoji = "✅" if result["healthy"] else "❌"
                print(f"{emoji} {result['name']}: {'Healthy' if result['healthy'] else 'Issues Found'}")
                
                if result["healthy"]:
                    healthy_systems += 1
                else:
                    self.health_report["errors"].extend(result["issues"])
                    
            except Exception as e:
                print(f"❌ Error checking {check.__name__}: {e}")
                self.health_report["errors"].append(f"Health check error: {e}")
        
        # Calculate overall health
        health_percentage = (healthy_systems / total_systems) * 100
        
        if health_percentage >= 90:
            self.health_report["overall_health"] = "excellent"
        elif health_percentage >= 70:
            self.health_report["overall_health"] = "good"
        elif health_percentage >= 50:
            self.health_report["overall_health"] = "fair"
        else:
            self.health_report["overall_health"] = "needs_attention"
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Print summary
        print("\n" + "=" * 50)
        print("🧠 CHAOSGENIUS HEALTH REPORT")
        print("=" * 50)
        print(f"🎯 Overall Health: {self.health_report['overall_health'].upper()}")
        print(f"✅ Healthy Systems: {healthy_systems}/{total_systems}")
        print(f"📊 Health Score: {health_percentage:.1f}%")
        
        if self.health_report["errors"]:
            print(f"\n❌ Issues Found ({len(self.health_report['errors'])}):")
            for error in self.health_report["errors"][:5]:  # Show first 5 errors
                print(f"   • {error}")
        
        if self.health_report["recommendations"]:
            print(f"\n🎯 Recommendations:")
            for rec in self.health_report["recommendations"][:3]:  # Show first 3 recommendations
                print(f"   • {rec}")
        
        # Health-based motivational message
        if health_percentage >= 80:
            print("\n🚀 HYPERFOCUS ZONE STATUS: EXCELLENT!")
            print("💜 Your neurodivergent business empire is running beautifully!")
        elif health_percentage >= 60:
            print("\n⚡ HYPERFOCUS ZONE STATUS: GOOD WITH ROOM FOR IMPROVEMENT")
            print("💛 Most systems healthy - a few tweaks for optimal performance!")
        else:
            print("\n🔧 HYPERFOCUS ZONE STATUS: NEEDS ATTENTION")
            print("💭 Several systems need fixing - but you've got this! Every empire needs maintenance!")
        
        # Save detailed report
        report_file = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.health_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed health report saved to: {report_file}")
        print("💜 Keep building your beautiful, chaotic empire!")
        
        return self.health_report

def main():
    """Main health check execution"""
    print("🩺 Initializing ChaosGenius Health Check...")
    print("💜 Ensuring your neurodivergent empire runs smoothly!")
    print()
    
    health_checker = ChaosGeniusHealthCheck()
    report = health_checker.run_full_health_check()
    
    # Exit with appropriate code
    if report["overall_health"] in ["excellent", "good"]:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()