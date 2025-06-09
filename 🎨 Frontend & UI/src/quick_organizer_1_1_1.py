#!/usr/bin/env python3
"""
🧠 ChaosGenius Quick Project Organizer
=====================================
Simple and effective project organization
"""

import os
import shutil
from pathlib import Path
import re

class QuickOrganizer:
    def __init__(self):
        self.project_root = Path("/workspaces/HYPERFOCUS-DREAM-ChaosGenius")
        print("🧠 Quick Organizer Initialized!")

    def organize_project(self):
        """Organize the project structure"""
        print("🔧 Starting project organization...")

        # Create organized structure
        self.create_structure()

        # Fix dashboard_api.py imports
        self.fix_imports()

        # Create clean app.py
        self.create_clean_app()

        print("✅ Project organization complete!")

    def create_structure(self):
        """Create organized directory structure"""
        print("📁 Creating organized structure...")

        # Create directories
        dirs = [
            "api",
            "api/routes",
            "api/models",
            "api/utils",
            "config",
            "logs"
        ]

        for dir_path in dirs:
            (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)

        print("✅ Directory structure created!")

    def fix_imports(self):
        """Fix import issues in dashboard_api.py"""
        print("🔧 Fixing imports...")

        dashboard_file = self.project_root / "dashboard_api.py"
        if dashboard_file.exists():
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove problematic import
            content = content.replace("from api.social_media_integrations import get_live_social_metrics, SocialMediaAggregator", "# Import removed for now")
            content = content.replace("SOCIAL_INTEGRATIONS_AVAILABLE = True", "SOCIAL_INTEGRATIONS_AVAILABLE = False")

            with open(dashboard_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print("✅ Fixed imports in dashboard_api.py!")

    def create_clean_app(self):
        """Create a clean main app.py file"""
        print("📝 Creating clean app.py...")

        app_content = '''#!/usr/bin/env python3
"""
🧠 ChaosGenius Main Application
==============================
Clean Flask application startup
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Start the dashboard
if __name__ == '__main__':
    print("🧠 Starting ChaosGenius Dashboard...")
    print("🚀 Loading from dashboard_api.py...")

    try:
        # Import and run the dashboard
        from dashboard_api import app

        print('\\n🎯 ChaosGenius Dashboard Starting...')
        print('💜 Dashboard URL: http://localhost:5000')
        print('📚 API Docs: http://localhost:5000/apidocs/')
        print('🎛️ Ultra Analytics: http://localhost:5000/ultra-analytics')
        print('\\n✨ Press Ctrl+C to stop\\n')

        app.run(debug=True, host='0.0.0.0', port=5000)

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("🔧 Check dashboard_api.py for issues")
        sys.exit(1)
'''

        with open(self.project_root / "app.py", 'w', encoding='utf-8') as f:
            f.write(app_content)

        print("✅ Created clean app.py!")

    def run(self):
        """Run the organizer"""
        try:
            self.organize_project()
            print("\n🎉 Organization complete! Ready to start the dashboard.")
            print("💡 Run: python app.py")
            return True
        except Exception as e:
            print(f"❌ Organization failed: {e}")
            return False

if __name__ == "__main__":
    organizer = QuickOrganizer()
    organizer.run()
