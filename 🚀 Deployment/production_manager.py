#!/usr/bin/env python3
"""
🎬 Hyperfocus Zone - Video/Audio Production Automation
Streamlines the production workflow for all video and audio content
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
import requests
import signal
import sys

class HyperfocusProductionManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.assets_dir = self.project_root / "production_assets"
        self.exports_dir = self.project_root / "final_exports"
        self.scripts_dir = self.project_root
        
        # Create directories if they don't exist
        self.assets_dir.mkdir(exist_ok=True)
        self.exports_dir.mkdir(exist_ok=True)
        
        self.production_log = []
        self.shutdown_flag = False
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, sig, frame):
        """Handle shutdown signals gracefully"""
        print('\n🛑 Gracefully shutting down Production Manager...')
        self.shutdown_flag = True
        self.save_production_log()
        print('💜 Production state saved. Thanks for using Hyperfocus Zone!')
        sys.exit(0)
    
    def log_action(self, action, details=""):
        """Log production actions with timestamps"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "details": details
        }
        self.production_log.append(log_entry)
        print(f"✅ [{timestamp}] {action}")
        if details:
            print(f"   📋 {details}")
    
    def setup_production_environment(self):
        """Initialize the production environment"""
        self.log_action("Setting up production environment")
        
        # Create platform-specific directories
        platforms = ["tiktok", "linkedin", "instagram", "youtube", "audio_only"]
        for platform in platforms:
            (self.exports_dir / platform).mkdir(exist_ok=True)
            
        # Create working directories
        working_dirs = ["raw_audio", "processed_audio", "raw_video", "processed_video", "thumbnails", "captions"]
        for dir_name in working_dirs:
            (self.assets_dir / dir_name).mkdir(exist_ok=True)
            
        self.log_action("Production directories created", f"Assets: {self.assets_dir}, Exports: {self.exports_dir}")
    
    def load_scripts(self):
        """Load all available scripts for production"""
        scripts = {}
        
        script_files = {
            "elevenlabs": "ElevenLabs_Audio_Pitch_Script.md",
            "synthesia": "Synthesia_Video_Pitch_Script.md", 
            "chaosgenius": "ChaosGenius_Video_Pitch_Script.md",
            "marketing": "Complete_Video_Marketing_Guide.md"
        }
        
        for script_type, filename in script_files.items():
            script_path = self.scripts_dir / filename
            if script_path.exists():
                with open(script_path, 'r', encoding='utf-8') as f:
                    scripts[script_type] = f.read()
                self.log_action(f"Loaded {script_type} script", filename)
            else:
                self.log_action(f"⚠️  Missing {script_type} script", filename)
                
        return scripts
    
    def generate_platform_variants(self, base_script):
        """Generate platform-specific script variants"""
        variants = {}
        
        # TikTok variant (15-30 seconds)
        variants["tiktok"] = {
            "duration": "15-30 seconds",
            "format": "9:16 vertical",
            "hook": "First 3 seconds critical",
            "style": "Quick cuts, trending audio",
            "script": self._create_short_variant(base_script, 30)
        }
        
        # LinkedIn variant (45-90 seconds)
        variants["linkedin"] = {
            "duration": "45-90 seconds", 
            "format": "16:9 or 1:1",
            "hook": "Professional, data-driven",
            "style": "Formal tone, business focus",
            "script": self._create_professional_variant(base_script, 90)
        }
        
        # Instagram variants
        variants["instagram"] = {
            "reels": {
                "duration": "15-30 seconds",
                "format": "9:16 vertical",
                "script": self._create_short_variant(base_script, 30)
            },
            "feed": {
                "duration": "60 seconds max",
                "format": "1:1 square",
                "script": self._create_medium_variant(base_script, 60)
            }
        }
        
        # YouTube variants
        variants["youtube"] = {
            "main": {
                "duration": "90-120 seconds",
                "format": "16:9 landscape",
                "script": base_script
            },
            "shorts": {
                "duration": "60 seconds max",
                "format": "9:16 vertical", 
                "script": self._create_medium_variant(base_script, 60)
            }
        }
        
        self.log_action("Generated platform variants", f"{len(variants)} platforms configured")
        return variants
    
    def _create_short_variant(self, base_script, max_seconds):
        """Create a shortened version focusing on hook and CTA"""
        return f"[{max_seconds}s variant] Hook + Core message + Strong CTA"
    
    def _create_professional_variant(self, base_script, max_seconds):
        """Create a professional version with data focus"""
        return f"[{max_seconds}s professional] Data-driven opening + Business case + Professional CTA"
    
    def _create_medium_variant(self, base_script, max_seconds):
        """Create a medium-length version"""
        return f"[{max_seconds}s medium] Balanced hook + Key benefits + Clear CTA"
    
    def create_production_schedule(self):
        """Generate a detailed production schedule"""
        schedule = {
            "week_1_audio": {
                "day_1": ["ElevenLabs voice testing", "Voice selection"],
                "day_2": ["Generate main audio versions", "Quality review"],
                "day_3": ["Audio post-production", "EQ and mastering"],
                "day_4": ["Platform-specific adaptations", "Export optimization"],
                "day_5": ["Final audio review", "Backup creation"]
            },
            "week_2_video": {
                "day_1": ["Synthesia avatar selection", "Script input"],
                "day_2": ["Video generation", "Initial review"],
                "day_3": ["Video post-production setup", "Color correction"],
                "day_4": ["Motion graphics", "Brand integration"],
                "day_5": ["Audio sync", "Final video editing"],
                "day_6": ["Platform optimization", "Export variants"],
                "day_7": ["Quality assurance", "Final review"]
            },
            "week_3_distribution": {
                "day_1": ["Platform uploads", "Metadata setup"],
                "day_2": ["Social media scheduling", "Campaign setup"],
                "day_3": ["Community engagement prep", "Response templates"],
                "day_4": ["Launch coordination", "Team briefing"],
                "day_5": ["Go-live execution", "Real-time monitoring"],
                "day_6": ["Performance analysis", "Initial metrics"],
                "day_7": ["Week 1 optimization", "Iteration planning"]
            }
        }
        
        # Save schedule to file
        schedule_file = self.assets_dir / "production_schedule.json"
        with open(schedule_file, 'w') as f:
            json.dump(schedule, f, indent=2)
            
        self.log_action("Production schedule created", str(schedule_file))
        return schedule
    
    def create_quality_checklist(self):
        """Generate automated quality assurance checklist"""
        checklist = {
            "technical_quality": {
                "audio": [
                    "Audio levels consistent (-6dB to -3dB for voice)",
                    "No clipping or distortion",
                    "Background noise removed",
                    "EQ applied for clarity",
                    "Proper LUFS levels for platform"
                ],
                "video": [
                    "Resolution correct for platform",
                    "Aspect ratio matches requirement",
                    "Frame rate consistent (24/30fps)",
                    "Color grading applied",
                    "No visual artifacts"
                ],
                "sync": [
                    "Audio-video sync perfect",
                    "Captions synchronized", 
                    "Timing markers accurate",
                    "Transitions smooth",
                    "No dead space"
                ]
            },
            "content_quality": {
                "message": [
                    "Hook engaging within 3 seconds",
                    "Problem clearly defined",
                    "Solution compelling",
                    "Benefits specific",
                    "CTA clear and actionable"
                ],
                "brand": [
                    "Logo placement correct",
                    "Brand colors consistent",
                    "Tone matches brand voice",
                    "Visual style coherent",
                    "Contact info visible"
                ]
            },
            "platform_compliance": {
                "tiktok": [
                    "Under 60 seconds",
                    "9:16 aspect ratio",
                    "Captions readable",
                    "Trending elements included",
                    "Hook within 3 seconds"
                ],
                "linkedin": [
                    "Professional tone",
                    "Business value clear",
                    "16:9 or 1:1 ratio",
                    "Appropriate length",
                    "Industry-relevant content"
                ],
                "youtube": [
                    "SEO-optimized title",
                    "Compelling thumbnail",
                    "Detailed description",
                    "Proper tags",
                    "End screen elements"
                ]
            }
        }
        
        # Save checklist
        checklist_file = self.assets_dir / "quality_checklist.json"
        with open(checklist_file, 'w') as f:
            json.dump(checklist, f, indent=2)
            
        self.log_action("Quality checklist created", str(checklist_file))
        return checklist
    
    def generate_analytics_framework(self):
        """Create analytics tracking framework"""
        analytics = {
            "kpis": {
                "awareness": [
                    "Video views",
                    "Impression reach", 
                    "Share count",
                    "Mention tracking"
                ],
                "engagement": [
                    "Like rate",
                    "Comment rate", 
                    "Share rate",
                    "Save rate",
                    "Completion rate"
                ],
                "conversion": [
                    "Click-through rate",
                    "Website visits",
                    "Email signups",
                    "Contact form submissions"
                ]
            },
            "tracking_setup": {
                "utm_parameters": {
                    "source": "social_video",
                    "medium": "video",
                    "campaign": "hyperfocus_launch"
                },
                "platform_analytics": [
                    "TikTok Analytics",
                    "LinkedIn Page Insights", 
                    "Instagram Insights",
                    "YouTube Analytics",
                    "Google Analytics"
                ]
            },
            "reporting_schedule": {
                "daily": ["Engagement metrics", "Reach data"],
                "weekly": ["Performance summary", "Platform comparison"],
                "monthly": ["ROI analysis", "Strategy optimization"]
            }
        }
        
        # Save analytics framework
        analytics_file = self.assets_dir / "analytics_framework.json"
        with open(analytics_file, 'w') as f:
            json.dump(analytics, f, indent=2)
            
        self.log_action("Analytics framework created", str(analytics_file))
        return analytics
    
    def create_automation_scripts(self):
        """Generate helper automation scripts"""
        
        # Batch export script
        batch_export = '''#!/bin/bash
# Batch export for all platforms

echo "Starting batch export process..."

# Create platform directories
mkdir -p exports/{tiktok,linkedin,instagram,youtube,audio}

# Export video variants (pseudo-code - adapt to your video editor)
echo "Exporting video variants..."
# ffmpeg commands would go here for format conversion

echo "Exporting audio variants..."
# Audio export commands

echo "Batch export complete!"
'''
        
        # Platform upload automation
        upload_automation = '''#!/usr/bin/env python3
# Platform upload automation (pseudo-code)

import requests
import json

def upload_to_platforms(video_path, metadata):
    """Upload video to multiple platforms"""
    platforms = {
        'youtube': upload_youtube,
        'tiktok': upload_tiktok,
        'linkedin': upload_linkedin
    }
    
    results = {}
    for platform, upload_func in platforms.items():
        try:
            result = upload_func(video_path, metadata)
            results[platform] = result
        except Exception as e:
            results[platform] = f"Error: {e}"
    
    return results

if __name__ == "__main__":
    print("Platform upload automation ready")
'''
        
        # Save scripts with proper encoding
        scripts_dir = self.assets_dir / "automation_scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        with open(scripts_dir / "batch_export.sh", 'w', encoding='utf-8') as f:
            f.write(batch_export)
            
        with open(scripts_dir / "upload_automation.py", 'w', encoding='utf-8') as f:
            f.write(upload_automation)
        
        self.log_action("Automation scripts created", f"Scripts saved to {scripts_dir}")
    
    def save_production_log(self):
        """Save the complete production log"""
        log_file = self.assets_dir / f"production_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(self.production_log, f, indent=2)
        
        print(f"\n📊 Production log saved: {log_file}")
        return log_file
    
    def run_full_setup(self):
        """Execute the complete production setup"""
        print("🎬 HYPERFOCUS ZONE - Production Manager Initializing...\n")
        
        # Execute all setup steps
        self.setup_production_environment()
        scripts = self.load_scripts()
        
        if scripts:
            variants = self.generate_platform_variants(scripts.get('elevenlabs', ''))
        
        schedule = self.create_production_schedule()
        checklist = self.create_quality_checklist()
        analytics = self.generate_analytics_framework()
        self.create_automation_scripts()
        
        # Save final log
        log_file = self.save_production_log()
        
        print("\n🎯 PRODUCTION SETUP COMPLETE!")
        print("=" * 50)
        print(f"📁 Assets Directory: {self.assets_dir}")
        print(f"📁 Exports Directory: {self.exports_dir}")
        print(f"📋 Production Log: {log_file}")
        print("\n🚀 Ready to start video/audio production!")
        print("💡 Check the Video_Audio_Production_Walkthrough.md for detailed steps")

if __name__ == "__main__":
    manager = HyperfocusProductionManager()
    manager.run_full_setup()