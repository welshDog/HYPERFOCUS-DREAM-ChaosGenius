#!/usr/bin/env python3
"""
🏥 HYPERFOCUS DREAM Project Health Monitor
Automatically monitors project health and suggests optimizations
"""

import os
import json
from pathlib import Path
from datetime import datetime

class ProjectHealthMonitor:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        
    def check_project_health(self):
        """Perform comprehensive health check"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "UNKNOWN",
            "metrics": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check file count
        total_files = sum(1 for _ in self.project_root.rglob('*') if _.is_file())
        health_report["metrics"]["total_files"] = total_files
        
        # Check for large files
        large_files = []
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                try:
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    if size_mb > 50:
                        large_files.append({"path": str(file_path), "size_mb": size_mb})
                except:
                    pass
        
        health_report["metrics"]["large_files_count"] = len(large_files)
        health_report["metrics"]["large_files"] = large_files[:5]  # Top 5
        
        # Check .gitignore existence
        gitignore_exists = (self.project_root / ".gitignore").exists()
        health_report["metrics"]["gitignore_exists"] = gitignore_exists
        
        # Determine overall health
        issues_count = 0
        if total_files > 25000:
            health_report["issues"].append("Project has excessive file count")
            issues_count += 1
        if len(large_files) > 10:
            health_report["issues"].append("Too many large files detected")
            issues_count += 1
        if not gitignore_exists:
            health_report["issues"].append("Missing .gitignore file")
            issues_count += 1
            
        # Set health status
        if issues_count == 0:
            health_report["overall_health"] = "EXCELLENT"
        elif issues_count <= 2:
            health_report["overall_health"] = "GOOD"
        elif issues_count <= 4:
            health_report["overall_health"] = "FAIR"
        else:
            health_report["overall_health"] = "POOR"
            
        return health_report
    
    def save_health_report(self, report):
        """Save health report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.project_root / f"health_report_{timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return report_path

if __name__ == "__main__":
    project_root = Path(__file__).parent
    monitor = ProjectHealthMonitor(project_root)
    
    print("🔍 Running HYPERFOCUS DREAM Project Health Check...")
    health_report = monitor.check_project_health()
    
    print(f"\n🏥 HEALTH STATUS: {health_report['overall_health']}")
    print(f"📊 Total Files: {health_report['metrics']['total_files']:,}")
    print(f"💾 Large Files: {health_report['metrics']['large_files_count']}")
    
    if health_report['issues']:
        print("\n⚠️  Issues Found:")
        for issue in health_report['issues']:
            print(f"   • {issue}")
    
    report_path = monitor.save_health_report(health_report)
    print(f"\n📋 Health report saved: {report_path}")
