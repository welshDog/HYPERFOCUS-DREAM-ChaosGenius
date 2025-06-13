#!/usr/bin/env python3
"""
🌌🌟 DIGITAL UNIVERSE EXPANSION SYSTEM 🌟🌌
Neuro Stars Map + Agent Army XP System + BROski$ Token Ecosystem!
Visualize your directory like a galaxy with AI links and rewards!
"""

import json
import os
import random
import sqlite3
import subprocess
import webbrowser
from datetime import datetime


class DigitalUniverseExpansion:
    def __init__(self):
        self.universe_db = "chaosgenius_universe.db"
        self.setup_universe_database()
        self.broski_token_rate = 1.5  # BROski$ per XP point

    def setup_universe_database(self):
        """Initialize the Digital Universe database"""
        conn = sqlite3.connect(self.universe_db)
        cursor = conn.cursor()

        # Agent Army XP System
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS agent_xp (
                agent_id TEXT PRIMARY KEY,
                agent_name TEXT,
                xp_points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                missions_completed INTEGER DEFAULT 0,
                last_activity TEXT,
                specialization TEXT,
                achievements TEXT
            )
        """
        )

        # BROski$ Token Economy
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS broski_economy (
                user_id TEXT PRIMARY KEY,
                broski_tokens REAL DEFAULT 100.0,
                total_earned REAL DEFAULT 0.0,
                total_spent REAL DEFAULT 0.0,
                last_transaction TEXT,
                transaction_history TEXT
            )
        """
        )

        # Neuro Stars Map Data
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS neuro_stars (
                star_id TEXT PRIMARY KEY,
                star_name TEXT,
                star_type TEXT,
                connections TEXT,
                ai_links TEXT,
                brightness_level INTEGER DEFAULT 1,
                discovery_date TEXT
            )
        """
        )

        conn.commit()
        conn.close()

    def create_neuro_stars_map(self):
        """🌟 Generate the Neuro Stars Map visualization"""
        print("🌌 Generating Neuro Stars Map...")

        # Scan the chaosgenius directory
        stars_data = self.scan_directory_stars()

        # Create the HTML galaxy visualization
        html_content = self.generate_galaxy_html(stars_data)

        # Save and open
        with open("/root/chaosgenius/neuro_stars_galaxy.html", "w") as f:
            f.write(html_content)

        print("✅ Neuro Stars Map created! Opening galaxy visualization...")
        webbrowser.open("file:///root/chaosgenius/neuro_stars_galaxy.html")

    def scan_directory_stars(self):
        """Scan chaosgenius directory and classify files as stars"""
        stars = []
        base_path = "/root/chaosgenius"

        star_types = {
            ".py": {"type": "Agent Star", "color": "#00ff00", "size": "large"},
            ".js": {"type": "Empire Star", "color": "#ffff00", "size": "medium"},
            ".sh": {"type": "Guardian Star", "color": "#ff6600", "size": "medium"},
            ".db": {"type": "Memory Crystal", "color": "#9932cc", "size": "small"},
            ".md": {"type": "Knowledge Star", "color": "#00ffff", "size": "small"},
            ".json": {"type": "Config Nebula", "color": "#ff69b4", "size": "tiny"},
        }

        for root, dirs, files in os.walk(base_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_path)

                # Skip hidden files and __pycache__
                if file.startswith(".") or "__pycache__" in file_path:
                    continue

                ext = os.path.splitext(file)[1]
                star_info = star_types.get(
                    ext, {"type": "Unknown Star", "color": "#666666", "size": "tiny"}
                )

                # Calculate star brightness based on file size and age
                try:
                    stat = os.stat(file_path)
                    brightness = min(10, max(1, stat.st_size // 1000))
                except:
                    brightness = 1

                star = {
                    "name": file,
                    "path": relative_path,
                    "type": star_info["type"],
                    "color": star_info["color"],
                    "size": star_info["size"],
                    "brightness": brightness,
                    "x": random.randint(50, 950),
                    "y": random.randint(50, 650),
                }

                stars.append(star)

        return stars

    def generate_galaxy_html(self, stars_data):
        """Generate the interactive galaxy HTML"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>🌌 ChaosGenius Neuro Stars Galaxy 🌌</title>
    <style>
        body {{
            margin: 0;
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ff00;
            font-family: 'Courier New', monospace;
            overflow: hidden;
        }}
        .galaxy-container {{
            position: relative;
            width: 100vw;
            height: 100vh;
        }}
        .star {{
            position: absolute;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px currentColor;
        }}
        .star:hover {{
            transform: scale(1.5);
            box-shadow: 0 0 20px currentColor;
        }}
        .large {{ width: 12px; height: 12px; }}
        .medium {{ width: 8px; height: 8px; }}
        .small {{ width: 6px; height: 6px; }}
        .tiny {{ width: 4px; height: 4px; }}
        .info-panel {{
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(26, 26, 46, 0.9);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #00ff00;
            max-width: 300px;
        }}
        .constellation-line {{
            position: absolute;
            height: 1px;
            background: linear-gradient(to right, transparent, #00ff00, transparent);
            opacity: 0.3;
        }}
        .title {{
            text-align: center;
            font-size: 24px;
            margin: 20px;
            text-shadow: 0 0 10px #00ff00;
        }}
    </style>
</head>
<body>
    <div class="galaxy-container">
        <div class="title">🌌 CHAOSGENIUS NEURO STARS GALAXY 🌌</div>

        <div class="info-panel">
            <h3>🌟 Galaxy Status</h3>
            <p>⭐ Total Stars: {len(stars_data)}</p>
            <p>🤖 Agent Stars: {len([s for s in stars_data if s['type'] == 'Agent Star'])}</p>
            <p>🛡️ Guardian Stars: {len([s for s in stars_data if s['type'] == 'Guardian Star'])}</p>
            <p>💾 Memory Crystals: {len([s for s in stars_data if s['type'] == 'Memory Crystal'])}</p>
            <p>📚 Knowledge Stars: {len([s for s in stars_data if s['type'] == 'Knowledge Star'])}</p>
            <br>
            <p>🎯 <strong>Click stars to explore!</strong></p>
        </div>

        {self.generate_stars_html(stars_data)}
    </div>

    <script>
        // Add twinkling effect
        setInterval(() => {{
            const stars = document.querySelectorAll('.star');
            stars.forEach(star => {{
                if (Math.random() < 0.1) {{
                    star.style.opacity = Math.random() * 0.5 + 0.5;
                }}
            }});
        }}, 2000);

        // Star click handler
        function showStarInfo(name, type, path) {{
            alert(`🌟 Star: ${{name}}\\n🔮 Type: ${{type}}\\n📁 Path: ${{path}}`);
        }}
    </script>
</body>
</html>
"""

    def generate_stars_html(self, stars_data):
        """Generate HTML for all stars"""
        html = ""
        for star in stars_data:
            html += f"""
        <div class="star {star['size']}"
             style="left: {star['x']}px; top: {star['y']}px;
                    background-color: {star['color']};
                    opacity: {star['brightness'] / 10};"
             onclick="showStarInfo('{star['name']}', '{star['type']}', '{star['path']}')">
        </div>
"""
        return html

    def initialize_agent_army_xp(self):
        """🏆 Initialize the Agent Army XP System"""
        print("🤖 Initializing Agent Army XP System...")

        agents = [
            {
                "id": "forge_master",
                "name": "Agent Army Forge Master",
                "specialization": "Coordination",
            },
            {
                "id": "code_quality",
                "name": "Code Quality Fortress",
                "specialization": "Quality Assurance",
            },
            {
                "id": "security_fortress",
                "name": "Security Fortress Guardian",
                "specialization": "Security",
            },
            {
                "id": "money_maker",
                "name": "Money Maker Supreme",
                "specialization": "Revenue Generation",
            },
            {
                "id": "special_ops",
                "name": "Special Ops Deployer",
                "specialization": "Deployment",
            },
            {
                "id": "tactical_executor",
                "name": "Tactical Executor",
                "specialization": "Execution",
            },
            {
                "id": "brain_engine",
                "name": "Brain Data Engine",
                "specialization": "Analytics",
            },
            {
                "id": "cloaked_ideas",
                "name": "Cloaked Ideas System",
                "specialization": "Innovation",
            },
        ]

        conn = sqlite3.connect(self.universe_db)
        cursor = conn.cursor()

        for agent in agents:
            cursor.execute(
                """
                INSERT OR REPLACE INTO agent_xp
                (agent_id, agent_name, specialization, last_activity)
                VALUES (?, ?, ?, ?)
            """,
                (
                    agent["id"],
                    agent["name"],
                    agent["specialization"],
                    datetime.now().isoformat(),
                ),
            )

        conn.commit()
        conn.close()

        print("✅ Agent Army XP System initialized!")

    def award_agent_xp(self, agent_id, xp_amount, mission_type="general"):
        """Award XP to an agent and calculate BROski$ tokens"""
        conn = sqlite3.connect(self.universe_db)
        cursor = conn.cursor()

        # Update agent XP
        cursor.execute(
            """
            UPDATE agent_xp
            SET xp_points = xp_points + ?,
                missions_completed = missions_completed + 1,
                last_activity = ?
            WHERE agent_id = ?
        """,
            (xp_amount, datetime.now().isoformat(), agent_id),
        )

        # Calculate new level
        cursor.execute("SELECT xp_points FROM agent_xp WHERE agent_id = ?", (agent_id,))
        result = cursor.fetchone()
        if result:
            new_level = (result[0] // 100) + 1
            cursor.execute(
                "UPDATE agent_xp SET level = ? WHERE agent_id = ?",
                (new_level, agent_id),
            )

        conn.commit()
        conn.close()

        # Award BROski$ tokens
        broski_tokens = xp_amount * self.broski_token_rate
        self.award_broski_tokens(
            "main_user", broski_tokens, f"Agent {agent_id} mission completion"
        )

        print(
            f"🏆 Agent {agent_id} awarded {xp_amount} XP and {broski_tokens} BROski$!"
        )

    def award_broski_tokens(self, user_id, amount, reason):
        """💰 Award BROski$ tokens to user"""
        conn = sqlite3.connect(self.universe_db)
        cursor = conn.cursor()

        # Initialize user if not exists
        cursor.execute(
            """
            INSERT OR IGNORE INTO broski_economy (user_id)
            VALUES (?)
        """,
            (user_id,),
        )

        # Award tokens
        cursor.execute(
            """
            UPDATE broski_economy
            SET broski_tokens = broski_tokens + ?,
                total_earned = total_earned + ?,
                last_transaction = ?
            WHERE user_id = ?
        """,
            (amount, amount, datetime.now().isoformat(), user_id),
        )

        conn.commit()
        conn.close()

        print(f"💰 Awarded {amount} BROski$ for: {reason}")

    def display_universe_stats(self):
        """📊 Display complete universe statistics"""
        conn = sqlite3.connect(self.universe_db)
        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("🌌 DIGITAL UNIVERSE EXPANSION STATS 🌌")
        print("=" * 60)

        # Agent Army Stats
        cursor.execute(
            "SELECT agent_name, level, xp_points, missions_completed FROM agent_xp"
        )
        agents = cursor.fetchall()

        print("\n🤖 AGENT ARMY STATUS:")
        for agent in agents:
            print(
                f"  {agent[0]}: Level {agent[1]} | {agent[2]} XP | {agent[3]} missions"
            )

        # Economy Stats
        cursor.execute(
            'SELECT broski_tokens, total_earned FROM broski_economy WHERE user_id = "main_user"'
        )
        economy = cursor.fetchone()

        if economy:
            print(f"\n💰 BROSKI$ ECONOMY:")
            print(f"  Current Balance: {economy[0]:.2f} BROski$")
            print(f"  Total Earned: {economy[1]:.2f} BROski$")

        # Star Count - Fixed bug
        cursor.execute("SELECT COUNT(*) FROM neuro_stars")
        result = cursor.fetchone()
        star_count = result[0] if result else 0

        print(f"\n🌟 NEURO STARS MAP:")
        print(f"  Discovered Stars: {star_count}")
        print(f"  Galaxy Status: ACTIVE")

        conn.close()
        print("=" * 60)


def main():
    """Main Digital Universe Expansion launcher"""
    print("🌌🌟 INITIALIZING DIGITAL UNIVERSE EXPANSION 🌟🌌")

    universe = DigitalUniverseExpansion()

    # Initialize all systems
    universe.initialize_agent_army_xp()
    universe.create_neuro_stars_map()

    # Award some initial XP for demonstration
    universe.award_agent_xp("forge_master", 50, "System Initialization")
    universe.award_agent_xp("code_quality", 30, "Quality Check")
    universe.award_agent_xp("security_fortress", 40, "Security Scan")

    # Display stats
    universe.display_universe_stats()

    print("\n🚀 DIGITAL UNIVERSE EXPANSION COMPLETE!")
    print("🌟 Check out your Neuro Stars Galaxy in the browser!")


if __name__ == "__main__":
    main()
