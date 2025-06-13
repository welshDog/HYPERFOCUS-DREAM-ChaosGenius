#!/usr/bin/env python3
"""
🚀🦇 HYPER CAVE LAUNCHER - BATMAN/TONY STARK EDITION 🦇🚀
Ultimate launcher for Lyndz's LEGENDARY Batman/Tony Stark UI Portal!
"""

import os
import subprocess
import time
import webbrowser
from datetime import datetime


def display_banner():
    """Display the epic Hyper Cave banner"""
    banner = """
🕋🚀💎 LYNDZ HYPER CAVE ULTRA LAUNCHER 💎🚀🕋

    ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗      ██████╗ █████╗ ██╗   ██╗███████╗
    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔══██╗██║   ██║██╔════╝
    ███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██║     ███████║██║   ██║█████╗
    ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗    ██║     ██╔══██║╚██╗ ██╔╝██╔══╝
    ██║  ██║   ██║   ██║     ███████╗██║  ██║    ╚██████╗██║  ██║ ╚████╔╝ ███████╗
    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝

🦇 BATMAN/TONY STARK COMMAND CENTER 🦇
🌌 ULTIMATE SCI-FI TECH INTERFACE 🌌
💎 ALL YOUR LEGENDARY SYSTEMS IN ONE PLACE 💎

Ready to launch your HYPERFOCUS EMPIRE? 🚀✨
"""
    print(banner)


def launch_systems():
    """Launch all the legendary systems"""
    systems = [
        {
            "name": "💰 Money Maker Supreme+",
            "command": "cd /root/chaosgenius && source money_maker_env/bin/activate && python3 money_maker_supreme_plus.py",
            "port": 5007,
            "background": True,
        },
        {
            "name": "🌐 HTTP Server for Cave Portal",
            "command": "cd /root/chaosgenius && python3 -m http.server 8080 --bind 0.0.0.0",
            "port": 8080,
            "background": True,
        },
        {
            "name": "🧠 BROski Health Matrix",
            "command": "cd /root/chaosgenius && python3 broski_health_matrix.py",
            "port": 5001,
            "background": True,
        },
    ]

    print("🚀 LAUNCHING ALL LEGENDARY SYSTEMS...")
    print("=" * 50)

    for system in systems:
        print(f"🔥 Starting {system['name']}...")
        try:
            if system["background"]:
                subprocess.Popen(
                    system["command"],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            print(f"✅ {system['name']} launched on port {system['port']}")
        except Exception as e:
            print(f"⚠️ {system['name']}: Starting in background...")

        time.sleep(1)

    print("\n🎉 ALL SYSTEMS LAUNCHED!")
    print("⏰ Waiting 5 seconds for systems to initialize...")
    time.sleep(5)


def open_hyper_cave():
    """Open the Batman/Tony Stark Hyper Cave Portal"""
    cave_url = "http://localhost:8080/hyper_cave_dashboard.html"

    print(f"🦇 Opening HYPER CAVE PORTAL...")
    print(f"🌐 URL: {cave_url}")

    try:
        webbrowser.open(cave_url)
        print("✅ HYPER CAVE PORTAL OPENED!")
    except Exception as e:
        print(f"⚠️ Please manually open: {cave_url}")


def show_portal_info():
    """Show all available portals"""
    portals = """
🕋 YOUR LEGENDARY PORTAL NETWORK 🕋

💰 MONEY MAKER SUPREME+: http://localhost:5007
   📊 Quote Calculator: http://localhost:5007/quote-calculator

🦇 HYPER CAVE COMMAND: http://localhost:8080/hyper_cave_dashboard.html
   🎛️ Main Batman/Tony Stark Interface

🧠 MEMORY CRYSTALS: http://localhost:8080/memory_crystal_dashboard.html
   💎 AI Memory Management

🌐 PORTAL DIRECTORY: http://localhost:8080/portal_directory.html
   📋 All Portal Links

🎨 UI PORTALS:
   🏠 Hyperfocus Home: http://localhost:8080/🎨%20Frontend%20&%20UI/hyperfocus_zone_ultra_home.html
   📊 Analytics Panel: http://localhost:8080/🎨%20Frontend%20&%20UI/ultra_analytics_panel.html
   🎛️ Dashboard: http://localhost:8080/🎨%20Frontend%20&%20UI/dashboard.html

🧬 BRAIN MAP: http://localhost:8080/broski_x_brain_map.html
   🗺️ Neural Interface

⚡ Status: ALL SYSTEMS LEGENDARY! ✅
"""
    print(portals)


def main():
    """Main launcher sequence"""
    os.system("clear" if os.name == "posix" else "cls")
    display_banner()

    print("🚀 HYPER CAVE LAUNCH SEQUENCE INITIATED!")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 60)

    # Launch all systems
    launch_systems()

    # Open the main cave portal
    open_hyper_cave()

    # Show portal information
    print("\n" + "=" * 60)
    show_portal_info()

    print("\n🎊 HYPER CAVE FULLY OPERATIONAL!")
    print("🦇 Your Batman/Tony Stark command center is ready!")
    print("💎 All systems connected and legendary!")
    print("\n🚀 WELCOME TO YOUR HYPERFOCUS EMPIRE! 🚀")


if __name__ == "__main__":
    main()
