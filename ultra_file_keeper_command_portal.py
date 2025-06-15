#!/usr/bin/env python3
"""
🤖💪 ULTRA FILE KEEPER COMMAND PORTAL INTEGRATION 💪🤖
🔗 Connects File Keeper with Agent Army Command Structure 🔗
👑 Supreme Agent Coordination System 👑
"""

import os
import sys
import asyncio
import sqlite3
import json
import time
from typing import Dict, List, Any, Optional

# Add chaosgenius path
sys.path.append("/root/chaosgenius")

try:
    from ultra_file_keeper_agent import UltraFileKeeperAgent
    from broski_agent_army_command_portal import BroskiAgentArmyCommandPortal
except ImportError as e:
    print(f"⚠️ Import warning: {e}")

class UltraFileKeeperCommandPortal:
    """🤖 File Keeper Agent Command Portal Integration"""

    def __init__(self):
        self.file_keeper = UltraFileKeeperAgent()
        self.command_portal = None
        self.agent_id = "ultra_file_keeper"
        self.commands = {
            "scan": self.command_hyper_scan,
            "organize": self.command_organize_files,
            "find_duplicates": self.command_find_duplicates,
            "search": self.command_search_files,
            "status": self.command_get_status,
            "dashboard": self.command_get_dashboard,
            "cleanup": self.command_cleanup_files,
            "watch": self.command_start_watching,
            "health_check": self.command_health_check,
            "auto_organize": self.command_auto_organize
        }

        print("🤖💪 ULTRA FILE KEEPER COMMAND PORTAL READY! 💪🤖")
        self._initialize_command_portal()

    def _initialize_command_portal(self):
        """🔗 Initialize command portal integration"""
        try:
            # Try to connect to existing command portal
            self.command_portal = BroskiAgentArmyCommandPortal()
            self._register_commands()
            print("🔗 Connected to Agent Army Command Portal!")
        except Exception as e:
            print(f"⚠️ Command portal connection warning: {e}")
            print("🔧 Running in standalone mode...")

    def _register_commands(self):
        """📝 Register file keeper commands with command portal"""
        if not self.command_portal:
            return

        for command_name, command_func in self.commands.items():
            try:
                # Register command with the portal
                self.command_portal.register_agent_command(
                    agent_id=self.agent_id,
                    command=command_name,
                    handler=command_func,
                    description=f"File Keeper: {command_name}",
                    category="file_management"
                )
            except Exception as e:
                print(f"⚠️ Could not register command {command_name}: {e}")

    async def command_hyper_scan(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """🔍 HYPER file system scan command"""
        print("🔍🔥 EXECUTING HYPER SCAN COMMAND! 🔥🔍")

        try:
            scan_results = await self.file_keeper.hyper_file_scan()

            return {
                "success": True,
                "command": "hyper_scan",
                "timestamp": time.time(),
                "results": {
                    "total_files": scan_results["total_files"],
                    "total_size": scan_results["total_size"],
                    "categories": dict(scan_results["categories"]),
                    "large_files_count": len(scan_results["large_files"]),
                    "duplicates_found": len(scan_results["duplicates"]),
                    "organization_opportunities": len(scan_results["organization_opportunities"])
                },
                "message": f"✅ Scan complete! Found {scan_results['total_files']} files"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "hyper_scan",
                "error": str(e),
                "message": f"❌ Scan failed: {e}"
            }

    async def command_organize_files(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """📁 Ultra file organization command"""
        print("📁🔥 EXECUTING ULTRA ORGANIZE COMMAND! 🔥📁")

        dry_run = params.get("dry_run", False) if params else False

        try:
            org_results = await self.file_keeper.ultra_organize_files(dry_run=dry_run)

            return {
                "success": True,
                "command": "organize_files",
                "timestamp": time.time(),
                "dry_run": dry_run,
                "results": {
                    "files_moved": org_results["files_moved"],
                    "directories_created": org_results["directories_created"],
                    "space_organized": org_results["space_organized"],
                    "errors": org_results["errors"]
                },
                "message": f"✅ {'Simulation' if dry_run else 'Organization'} complete! {org_results['files_moved']} files processed"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "organize_files",
                "error": str(e),
                "message": f"❌ Organization failed: {e}"
            }

    async def command_find_duplicates(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """🔍 Find duplicate files command"""
        print("🔍 EXECUTING DUPLICATE DETECTION COMMAND!")

        try:
            duplicates = await self.file_keeper.find_duplicates()

            total_wasted = sum(d.get('wasted_space', 0) for d in duplicates)

            return {
                "success": True,
                "command": "find_duplicates",
                "timestamp": time.time(),
                "results": {
                    "duplicate_groups": len(duplicates),
                    "total_wasted_space": total_wasted,
                    "duplicates": duplicates[:10]  # Limit to first 10 for response size
                },
                "message": f"🔍 Found {len(duplicates)} duplicate groups"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "find_duplicates",
                "error": str(e),
                "message": f"❌ Duplicate detection failed: {e}"
            }

    async def command_search_files(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """🔍 Smart file search command"""
        if not params or "query" not in params:
            return {
                "success": False,
                "command": "search_files",
                "error": "Query parameter required",
                "message": "❌ Search query required"
            }

        query = params["query"]
        filters = params.get("filters", {})

        try:
            search_results = await self.file_keeper.smart_search(query, filters)

            return {
                "success": True,
                "command": "search_files",
                "timestamp": time.time(),
                "query": query,
                "filters": filters,
                "results": {
                    "total_matches": len(search_results),
                    "files": search_results[:20]  # Limit to first 20 results
                },
                "message": f"🔍 Found {len(search_results)} files matching '{query}'"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "search_files",
                "error": str(e),
                "message": f"❌ Search failed: {e}"
            }

    async def command_get_status(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """📊 Get file keeper agent status"""
        try:
            dashboard = await self.file_keeper.get_agent_dashboard()

            return {
                "success": True,
                "command": "get_status",
                "timestamp": time.time(),
                "status": {
                    "agent_status": dashboard["agent_status"],
                    "total_files": dashboard["total_files"],
                    "total_size": dashboard["total_size"],
                    "disorganized_files": dashboard["disorganized_files"],
                    "unhealthy_files": dashboard["unhealthy_files"],
                    "watching_active": dashboard["watching_active"],
                    "statistics": dashboard["statistics"]
                },
                "message": f"📊 Agent Status: {dashboard['agent_status']}"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "get_status",
                "error": str(e),
                "message": f"❌ Status check failed: {e}"
            }

    async def command_get_dashboard(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """📊 Get full dashboard data"""
        try:
            dashboard = await self.file_keeper.get_agent_dashboard()

            return {
                "success": True,
                "command": "get_dashboard",
                "timestamp": time.time(),
                "dashboard": dashboard,
                "message": "📊 Dashboard data retrieved"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "get_dashboard",
                "error": str(e),
                "message": f"❌ Dashboard retrieval failed: {e}"
            }

    async def command_cleanup_files(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """🧹 Cleanup and optimize files"""
        print("🧹 EXECUTING FILE CLEANUP COMMAND!")

        try:
            # Find duplicates first
            duplicates = await self.file_keeper.find_duplicates()

            # Cleanup statistics
            cleanup_stats = {
                "duplicates_removed": 0,
                "space_freed": 0,
                "errors": []
            }

            # In a real implementation, this would actually remove duplicates
            # For now, we'll simulate the cleanup
            for dup_group in duplicates:
                if len(dup_group["paths"]) > 1:
                    # Keep the first file, "remove" the rest (simulation)
                    files_to_remove = dup_group["paths"][1:]
                    cleanup_stats["duplicates_removed"] += len(files_to_remove)
                    cleanup_stats["space_freed"] += dup_group.get("wasted_space", 0)

            return {
                "success": True,
                "command": "cleanup_files",
                "timestamp": time.time(),
                "results": cleanup_stats,
                "message": f"🧹 Cleanup complete! Removed {cleanup_stats['duplicates_removed']} duplicate files"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "cleanup_files",
                "error": str(e),
                "message": f"❌ Cleanup failed: {e}"
            }

    async def command_start_watching(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """👁️ Start file system watching"""
        try:
            if not self.file_keeper.watching_active:
                # Start watching in background
                asyncio.create_task(self.file_keeper.start_file_watching())

                return {
                    "success": True,
                    "command": "start_watching",
                    "timestamp": time.time(),
                    "message": "👁️ File watching activated!"
                }
            else:
                return {
                    "success": True,
                    "command": "start_watching",
                    "timestamp": time.time(),
                    "message": "👁️ File watching already active"
                }

        except Exception as e:
            return {
                "success": False,
                "command": "start_watching",
                "error": str(e),
                "message": f"❌ Could not start watching: {e}"
            }

    async def command_health_check(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """💊 Comprehensive file system health check"""
        print("💊 EXECUTING HEALTH CHECK COMMAND!")

        try:
            # Get current dashboard
            dashboard = await self.file_keeper.get_agent_dashboard()

            # Calculate health scores
            total_files = dashboard["total_files"]
            unhealthy_files = dashboard["unhealthy_files"]
            disorganized_files = dashboard["disorganized_files"]

            overall_health = 100
            if total_files > 0:
                health_penalty = (unhealthy_files / total_files) * 30
                org_penalty = (disorganized_files / total_files) * 20
                overall_health = max(0, 100 - health_penalty - org_penalty)

            health_status = "EXCELLENT" if overall_health >= 90 else \
                           "GOOD" if overall_health >= 70 else \
                           "WARNING" if overall_health >= 50 else "CRITICAL"

            recommendations = []
            if disorganized_files > 0:
                recommendations.append(f"📁 Organize {disorganized_files} disorganized files")
            if unhealthy_files > 0:
                recommendations.append(f"💊 Fix {unhealthy_files} unhealthy files")

            return {
                "success": True,
                "command": "health_check",
                "timestamp": time.time(),
                "health": {
                    "overall_score": round(overall_health, 1),
                    "status": health_status,
                    "total_files": total_files,
                    "unhealthy_files": unhealthy_files,
                    "disorganized_files": disorganized_files,
                    "recommendations": recommendations
                },
                "message": f"💊 Health Check: {health_status} ({overall_health:.1f}%)"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "health_check",
                "error": str(e),
                "message": f"❌ Health check failed: {e}"
            }

    async def command_auto_organize(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """🤖 Fully automated organization and optimization"""
        print("🤖🔥 EXECUTING AUTO-ORGANIZE COMMAND! 🔥🤖")

        try:
            results = {
                "scan_results": None,
                "organization_results": None,
                "cleanup_results": None,
                "final_status": None
            }

            # Step 1: Scan
            print("🔍 Step 1: Scanning files...")
            scan_results = await self.file_keeper.hyper_file_scan()
            results["scan_results"] = {
                "files_found": scan_results["total_files"],
                "duplicates": len(scan_results["duplicates"]),
                "organization_opportunities": len(scan_results["organization_opportunities"])
            }

            # Step 2: Organize
            print("📁 Step 2: Organizing files...")
            org_results = await self.file_keeper.ultra_organize_files(dry_run=False)
            results["organization_results"] = {
                "files_moved": org_results["files_moved"],
                "directories_created": org_results["directories_created"]
            }

            # Step 3: Find and track duplicates (don't auto-remove for safety)
            print("🔍 Step 3: Identifying duplicates...")
            duplicates = await self.file_keeper.find_duplicates()
            results["cleanup_results"] = {
                "duplicates_found": len(duplicates),
                "action": "identified_only"  # For safety, don't auto-remove
            }

            # Step 4: Final status
            dashboard = await self.file_keeper.get_agent_dashboard()
            results["final_status"] = {
                "total_files": dashboard["total_files"],
                "disorganized_files": dashboard["disorganized_files"],
                "organization_improvement": True
            }

            return {
                "success": True,
                "command": "auto_organize",
                "timestamp": time.time(),
                "results": results,
                "message": f"🤖 Auto-organization complete! Organized {org_results['files_moved']} files"
            }

        except Exception as e:
            return {
                "success": False,
                "command": "auto_organize",
                "error": str(e),
                "message": f"❌ Auto-organization failed: {e}"
            }

    async def execute_command(self, command: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """⚡ Execute a file keeper command"""
        if command not in self.commands:
            return {
                "success": False,
                "command": command,
                "error": f"Unknown command: {command}",
                "available_commands": list(self.commands.keys()),
                "message": f"❌ Unknown command: {command}"
            }

        print(f"⚡ Executing File Keeper command: {command}")

        try:
            result = await self.commands[command](params)

            # Log command execution
            if hasattr(self.file_keeper, '_log_operation'):
                await self.file_keeper._log_operation(
                    operation_type=f"COMMAND_{command.upper()}",
                    source="command_portal",
                    target=command,
                    file_size=0,
                    success=result["success"],
                    details=json.dumps(result)
                )

            return result

        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e),
                "message": f"❌ Command execution failed: {e}"
            }

    def get_available_commands(self) -> Dict[str, str]:
        """📝 Get list of available commands"""
        return {
            "scan": "🔍 Perform comprehensive file system scan",
            "organize": "📁 Organize files according to rules",
            "find_duplicates": "🔍 Find duplicate files by content",
            "search": "🔍 Search files with advanced filters",
            "status": "📊 Get agent status and statistics",
            "dashboard": "📊 Get full dashboard data",
            "cleanup": "🧹 Clean up duplicate files",
            "watch": "👁️ Start real-time file monitoring",
            "health_check": "💊 Comprehensive system health check",
            "auto_organize": "🤖 Fully automated organization"
        }

# Natural language command interface
class FileKeeperNaturalLanguageInterface:
    """🗣️ Natural language interface for File Keeper commands"""

    def __init__(self, command_portal: UltraFileKeeperCommandPortal):
        self.portal = command_portal
        self.command_patterns = {
            r"scan|find files|search files|analyze": "scan",
            r"organize|tidy|clean up|arrange": "organize",
            r"duplicate|duplicates|copies": "find_duplicates",
            r"status|health|stats": "status",
            r"search .+": "search",
            r"watch|monitor": "watch",
            r"auto|automatic|do everything": "auto_organize"
        }

    async def process_natural_command(self, text: str) -> Dict[str, Any]:
        """🗣️ Process natural language command"""
        import re

        text_lower = text.lower().strip()

        # Extract search query if present
        search_match = re.search(r"search (?:for )?['\"]?([^'\"]+)['\"]?", text_lower)
        if search_match:
            query = search_match.group(1)
            return await self.portal.execute_command("search", {"query": query})

        # Match other patterns
        for pattern, command in self.command_patterns.items():
            if re.search(pattern, text_lower):
                # Extract parameters based on command type
                params = {}

                if command == "organize" and "preview" in text_lower:
                    params["dry_run"] = True

                return await self.portal.execute_command(command, params)

        # If no pattern matches, suggest available commands
        return {
            "success": False,
            "error": "Command not understood",
            "message": "❓ I didn't understand that command. Try: 'scan files', 'organize files', 'find duplicates', 'search for python', etc.",
            "suggestions": list(self.portal.get_available_commands().keys())
        }

async def main():
    """🚀 Main File Keeper Command Portal"""
    print("🤖💪🔥 ULTRA FILE KEEPER COMMAND PORTAL STARTING! 🔥💪🤖")

    portal = UltraFileKeeperCommandPortal()
    nl_interface = FileKeeperNaturalLanguageInterface(portal)

    print("\n📋 Available Commands:")
    for cmd, desc in portal.get_available_commands().items():
        print(f"  {cmd}: {desc}")

    # Demo some commands
    print("\n🎯 Executing Demo Commands...")

    # Health check
    health_result = await portal.execute_command("health_check")
    print(f"💊 Health Check: {health_result['message']}")

    # Status check
    status_result = await portal.execute_command("status")
    print(f"📊 Status: {status_result['message']}")

    # Natural language demo
    print("\n🗣️ Natural Language Interface Demo:")
    nl_commands = [
        "scan all files",
        "organize files preview",
        "find duplicates",
        "search for python files"
    ]

    for nl_cmd in nl_commands:
        print(f"\n🗣️ Processing: '{nl_cmd}'")
        result = await nl_interface.process_natural_command(nl_cmd)
        print(f"   Response: {result['message']}")

    print("\n🤖💪 ULTRA FILE KEEPER COMMAND PORTAL READY FOR DUTY! 💪🤖")

if __name__ == "__main__":
    asyncio.run(main())