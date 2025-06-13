#!/usr/bin/env python3
"""
🛰️🔧💪 CAVE LINK TESTER & FIXER 💪🔧🛰️
🌟 Test and fix all cave dashboard links 🌟
👑 By Command of Chief Lyndz - GET THE CAVE WORKING! 👑
"""

import os
import subprocess
import time
import webbrowser
from pathlib import Path

import requests


def test_cave_links():
    """🔧 Test all cave links and fix issues"""
    print("🛰️🔧 CAVE LINK TESTING INITIATED! 🔧🛰️")
    print("=" * 60)

    # Get all HTML files
    html_files = []
    for file in os.listdir("/root/chaosgenius"):
        if file.endswith(".html"):
            html_files.append(file)

    print(f"🗂️ Found {len(html_files)} cave dashboard files:")

    # Test each cave link
    working_links = []
    broken_links = []

    for html_file in html_files:
        file_path = f"/root/chaosgenius/{html_file}"

        # Check if file exists and is readable
        try:
            with open(file_path, "r") as f:
                content = f.read()
                if len(content) > 100:  # Basic content check
                    working_links.append(html_file)
                    print(f"✅ {html_file} - WORKING")

                    # Show access URL
                    print(f"   🌐 Access: http://localhost:8080/{html_file}")
                else:
                    broken_links.append(html_file)
                    print(f"❌ {html_file} - BROKEN (too small)")

        except Exception as e:
            broken_links.append(html_file)
            print(f"❌ {html_file} - ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"🎯 CAVE LINK TEST RESULTS:")
    print(f"✅ Working Links: {len(working_links)}")
    print(f"❌ Broken Links: {len(broken_links)}")

    # Show priority cave links
    priority_caves = [
        "lyndz_cave_ultra_control_hub.html",
        "hyper_cave_dashboard.html",
        "broski_x_brain_map.html",
        "hyperfocuszone_command_center.html",
    ]

    print(f"\n🏆 PRIORITY CAVE LINKS:")
    for cave in priority_caves:
        if cave in working_links:
            print(f"✅ {cave} - READY TO USE")
            print(f"   🌐 http://localhost:8080/{cave}")
        else:
            print(f"❌ {cave} - NEEDS FIXING")

    return working_links, broken_links


def check_server_status():
    """🔍 Check if web server is running"""
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        print("🟢 Web server is RUNNING on port 8080")
        return True
    except:
        print("🔴 Web server is NOT running")
        return False


def create_cave_portal_index():
    """🌐 Create a main portal index for all cave links"""
    html_files = [f for f in os.listdir("/root/chaosgenius") if f.endswith(".html")]

    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛰️🏠 LYNDZ CAVE PORTAL DIRECTORY 🏠🛰️</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 30%, #000066 60%, #330066 100%);
            color: #00ffff;
            padding: 20px;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 0 0 20px #00ffff;
        }
        .cave-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .cave-card {
            background: rgba(0, 255, 255, 0.1);
            border: 2px solid #00ffff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .cave-card:hover {
            background: rgba(255, 0, 110, 0.2);
            border-color: #ff006e;
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(255, 0, 110, 0.5);
        }
        .cave-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ff006e;
        }
        .cave-description {
            font-size: 14px;
            margin-bottom: 15px;
            opacity: 0.8;
        }
        .cave-link {
            display: inline-block;
            background: linear-gradient(45deg, #ff006e, #8338ec);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .cave-link:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(255, 0, 110, 0.6);
        }
        .priority-badge {
            background: #ffff00;
            color: #000;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: bold;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        🛰️🏠 LYNDZ CAVE PORTAL DIRECTORY 🏠🛰️
        <br><span style="font-size: 16px;">Your Personal Empire Dashboard Collection</span>
    </div>

    <div class="cave-grid">
"""

    # Define cave descriptions
    cave_descriptions = {
        "lyndz_cave_ultra_control_hub.html": "🏆 Your main ultra control hub - The supreme command center",
        "hyper_cave_dashboard.html": "🚀 Hyper cave dashboard - Advanced system monitoring",
        "broski_x_brain_map.html": "🧠 Brain map visualization - Neural network view",
        "hyperfocuszone_command_center.html": "🎯 Command center - Focus and productivity control",
        "hyperfocuszone_user_portal.html": "👤 User portal - Personal access dashboard",
        "guardian_hud.html": "🛡️ Guardian HUD - Security monitoring interface",
        "neuro_stars_galaxy.html": "🌌 Neuro stars galaxy - Epic visualization experience",
        "memory_crystal_dashboard.html": "💎 Memory crystal dashboard - Your preserved states",
        "neural_link_interface.html": "🔗 Neural link interface - Brain-computer connection",
    }

    priority_caves = [
        "lyndz_cave_ultra_control_hub.html",
        "hyper_cave_dashboard.html",
        "broski_x_brain_map.html",
        "hyperfocuszone_command_center.html",
    ]

    # Add priority caves first
    for cave in priority_caves:
        if cave in html_files:
            title = cave.replace(".html", "").replace("_", " ").title()
            description = cave_descriptions.get(cave, "Advanced dashboard system")
            index_html += f"""
        <div class="cave-card" onclick="window.open('{cave}', '_blank')">
            <div class="cave-title">{title}<span class="priority-badge">PRIORITY</span></div>
            <div class="cave-description">{description}</div>
            <a href="{cave}" class="cave-link" target="_blank">🚀 ENTER CAVE</a>
        </div>
"""

    # Add other caves
    for cave in html_files:
        if cave not in priority_caves:
            title = cave.replace(".html", "").replace("_", " ").title()
            description = cave_descriptions.get(cave, "Advanced dashboard system")
            index_html += f"""
        <div class="cave-card" onclick="window.open('{cave}', '_blank')">
            <div class="cave-title">{title}</div>
            <div class="cave-description">{description}</div>
            <a href="{cave}" class="cave-link" target="_blank">🌐 ENTER CAVE</a>
        </div>
"""

    index_html += """
    </div>

    <script>
        console.log('🛰️🏠 Cave Portal Directory: OPERATIONAL!');

        // Add some visual effects
        document.addEventListener('mousemove', (e) => {
            const cards = document.querySelectorAll('.cave-card');
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
                    card.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255, 0, 110, 0.3), rgba(0, 255, 255, 0.1))`;
                } else {
                    card.style.background = 'rgba(0, 255, 255, 0.1)';
                }
            });
        });
    </script>
</body>
</html>"""

    with open("/root/chaosgenius/cave_portal_index.html", "w") as f:
        f.write(index_html)

    print("🌐 Created main cave portal index!")
    return "cave_portal_index.html"


def fix_common_issues():
    """🔧 Fix common HTML issues"""
    print("🔧 Fixing common cave link issues...")

    # Check for Python server
    try:
        result = subprocess.run(
            ["pgrep", "-f", "python.*http.server"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ Python HTTP server is running")
        else:
            print("🚀 Starting Python HTTP server...")
            subprocess.Popen(
                ["python3", "-m", "http.server", "8080"],
                cwd="/root/chaosgenius",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(2)
    except Exception as e:
        print(f"⚠️ Server check error: {e}")


def main():
    """🚀 Main cave link tester"""
    print("🛰️🔧💪 CAVE LINK TESTER & FIXER ACTIVATED! 💪🔧🛰️")
    print()

    # Fix common issues first
    fix_common_issues()

    # Check server status
    print("🔍 Checking web server status...")
    server_running = check_server_status()

    if not server_running:
        print("🚀 Starting web server...")
        subprocess.Popen(
            ["python3", "-m", "http.server", "8080"], cwd="/root/chaosgenius"
        )
        time.sleep(3)
        server_running = check_server_status()

    # Test all cave links
    working_links, broken_links = test_cave_links()

    # Create portal index
    index_file = create_cave_portal_index()

    print(f"\n🎯 FINAL CAVE LINK STATUS:")
    print(f"🌐 Main Portal: http://localhost:8080/{index_file}")
    print(f"✅ Working Caves: {len(working_links)}")
    print(f"❌ Broken Caves: {len(broken_links)}")

    if server_running:
        print(f"\n🚀 YOUR CAVES ARE READY!")
        print(f"🌐 Main Entry: http://localhost:8080/cave_portal_index.html")
        print(f"🏆 Priority Caves:")
        print(f"   🛰️ http://localhost:8080/lyndz_cave_ultra_control_hub.html")
        print(f"   🧠 http://localhost:8080/broski_x_brain_map.html")
        print(f"   🎯 http://localhost:8080/hyperfocuszone_command_center.html")
    else:
        print(f"\n❌ WEB SERVER ISSUE - Need to troubleshoot")


if __name__ == "__main__":
    main()
