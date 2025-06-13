#!/usr/bin/env python3
"""
💼🔥 BROSKI GIG MARKETPLACE - TALENT ECONOMY SYSTEM 🔥💼
Discord-powered freelance marketplace with BROski$ integration!
By Command of Chief Lyndz - Community Talent Monetization Engine

🌟 FEATURES:
- /post-gig → Create gig postings with price & deadline
- /browse-gigs → Filter by skill categories
- /apply-gig → Apply with automatic DM notifications
- Supports design, coding, edits, voiceovers, etc.
- BROski$ escrow system for secure payments
- Rating & review system for quality control
- Role-based skill tagging and matching
"""

import asyncio
import json
import random
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set

import discord
from discord.ext import commands, tasks

# Import BROski$ token system
sys.path.append("/root/chaosgenius")

try:
    from ai_modules.broski.token_engine import BROskiTokenEngine

    TOKEN_ENGINE_AVAILABLE = True
except ImportError:
    print("⚠️ Token engine not available - Marketplace will run without payments")
    TOKEN_ENGINE_AVAILABLE = False


class GigCategory(Enum):
    """📋 Gig categories for skill classification"""

    DESIGN = "🎨 Design & Graphics"
    CODING = "💻 Programming & Development"
    WRITING = "✍️ Content & Writing"
    VOICEOVER = "🎙️ Voice & Audio"
    VIDEO = "🎬 Video & Animation"
    MARKETING = "📈 Marketing & Social Media"
    TUTORING = "🧠 Teaching & Tutoring"
    MUSIC = "🎵 Music & Sound Design"
    GAMING = "🎮 Gaming & Streaming"
    OTHER = "🔧 Other Skills"


class GigStatus(Enum):
    """📊 Gig posting status"""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class BroskiGigMarketplace:
    """💼 The legendary talent marketplace system"""

    def __init__(self):
        self.db_path = "/root/chaosgenius/broski_gig_marketplace.db"

        # Initialize token engine if available
        if TOKEN_ENGINE_AVAILABLE:
            self.token_engine = BROskiTokenEngine()
        else:
            self.token_engine = None

        # Marketplace configuration
        self.posting_fee = 5.0  # BROski$ fee to post a gig
        self.marketplace_commission = 0.05  # 5% commission on completed gigs
        self.escrow_timeout_days = 7  # Auto-release escrow after 7 days
        self.max_gigs_per_user = 10  # Max active gigs per user

        # Skill role mapping for auto-tagging
        self.skill_roles = {
            GigCategory.DESIGN: ["Designer", "Artist", "Graphics", "UI/UX"],
            GigCategory.CODING: ["Developer", "Programmer", "Coder", "Tech"],
            GigCategory.WRITING: ["Writer", "Content Creator", "Copywriter"],
            GigCategory.VOICEOVER: ["Voice Actor", "Audio", "Narrator"],
            GigCategory.VIDEO: ["Video Editor", "Animator", "Creator"],
            GigCategory.MARKETING: ["Marketer", "Social Media", "Growth"],
            GigCategory.TUTORING: ["Teacher", "Tutor", "Mentor", "Coach"],
            GigCategory.MUSIC: ["Musician", "Producer", "Sound Designer"],
            GigCategory.GAMING: ["Gamer", "Streamer", "Content Creator"],
        }

        self.init_database()
        print("💼🔥 BROSKI GIG MARKETPLACE ACTIVATED! 🔥💼")

    def init_database(self):
        """📊 Initialize gig marketplace database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Gig postings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gig_postings (
                gig_id TEXT PRIMARY KEY,
                poster_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'broski',
                deadline DATETIME,
                status TEXT DEFAULT 'open',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                tags TEXT DEFAULT '[]',
                requirements TEXT,
                delivery_format TEXT,
                portfolio_links TEXT DEFAULT '[]',
                escrow_amount REAL DEFAULT 0.0,
                assigned_to TEXT,
                completed_at DATETIME,
                review_rating INTEGER,
                review_text TEXT
            )
        """
        )

        # Gig applications table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gig_applications (
                application_id TEXT PRIMARY KEY,
                gig_id TEXT NOT NULL,
                applicant_id TEXT NOT NULL,
                application_text TEXT NOT NULL,
                portfolio_links TEXT DEFAULT '[]',
                proposed_price REAL,
                proposed_timeline TEXT,
                status TEXT DEFAULT 'pending',
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                reviewed_at DATETIME,
                FOREIGN KEY (gig_id) REFERENCES gig_postings (gig_id)
            )
        """
        )

        # User marketplace profiles
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_marketplace_profiles (
                user_id TEXT PRIMARY KEY,
                skills TEXT DEFAULT '[]',
                portfolio_url TEXT,
                hourly_rate REAL,
                bio TEXT,
                total_gigs_completed INTEGER DEFAULT 0,
                total_earnings REAL DEFAULT 0.0,
                average_rating REAL DEFAULT 0.0,
                total_reviews INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Escrow transactions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gig_escrow (
                escrow_id TEXT PRIMARY KEY,
                gig_id TEXT NOT NULL,
                payer_id TEXT NOT NULL,
                recipient_id TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'held',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                released_at DATETIME,
                dispute_reason TEXT,
                FOREIGN KEY (gig_id) REFERENCES gig_postings (gig_id)
            )
        """
        )

        # Reviews and ratings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gig_reviews (
                review_id TEXT PRIMARY KEY,
                gig_id TEXT NOT NULL,
                reviewer_id TEXT NOT NULL,
                reviewed_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                review_text TEXT,
                review_type TEXT NOT NULL,  -- 'client_to_freelancer' or 'freelancer_to_client'
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (gig_id) REFERENCES gig_postings (gig_id)
            )
        """
        )

        conn.commit()
        conn.close()

    async def post_gig(
        self,
        user_id: str,
        title: str,
        description: str,
        category: GigCategory,
        price: float,
        deadline: datetime,
        requirements: str = "",
        tags: List[str] = None,
    ) -> Dict:
        """💼 Post a new gig to the marketplace"""

        # Check if user has exceeded max gigs
        if self.get_user_active_gigs_count(user_id) >= self.max_gigs_per_user:
            return {
                "success": False,
                "message": f"❌ Maximum {self.max_gigs_per_user} active gigs allowed per user!",
            }

        # Check if user has enough tokens for posting fee
        if self.token_engine:
            balance = self.token_engine.get_balance(user_id)
            if balance < self.posting_fee:
                return {
                    "success": False,
                    "message": f"❌ Insufficient BROski$! Need {self.posting_fee} tokens to post a gig.",
                }

        # Generate gig ID
        gig_id = f"gig_{int(time.time())}_{random.randint(1000, 9999)}"

        # Validate and process data
        if price <= 0:
            return {"success": False, "message": "❌ Price must be greater than 0!"}

        if deadline <= datetime.now():
            return {"success": False, "message": "❌ Deadline must be in the future!"}

        tags = tags or []
        if len(tags) > 10:
            tags = tags[:10]  # Limit to 10 tags

        # Deduct posting fee
        if self.token_engine:
            fee_result = self.token_engine.spend_tokens(
                user_id, self.posting_fee, f"💼 Gig posting fee for: {title[:30]}"
            )
            if not fee_result["success"]:
                return {
                    "success": False,
                    "message": f"❌ Failed to deduct posting fee: {fee_result['message']}",
                }

        # Save gig to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO gig_postings
            (gig_id, poster_id, title, description, category, price,
             deadline, requirements, tags, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open')
        """,
            (
                gig_id,
                user_id,
                title,
                description,
                category.value,
                price,
                deadline.isoformat(),
                requirements,
                json.dumps(tags),
            ),
        )

        conn.commit()
        conn.close()

        # Update user profile
        self.update_user_profile_activity(user_id)

        return {
            "success": True,
            "gig_id": gig_id,
            "message": f"✅ Gig posted successfully! ID: {gig_id}",
            "posting_fee": self.posting_fee,
        }

    def browse_gigs(
        self,
        category: Optional[GigCategory] = None,
        min_price: float = 0,
        max_price: float = float("inf"),
        search_term: str = "",
        limit: int = 10,
    ) -> Dict:
        """🔍 Browse available gigs with filtering"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build query with filters
        query = "SELECT * FROM gig_postings WHERE status = 'open'"
        params = []

        if category:
            query += " AND category = ?"
            params.append(category.value)

        if min_price > 0:
            query += " AND price >= ?"
            params.append(min_price)

        if max_price < float("inf"):
            query += " AND price <= ?"
            params.append(max_price)

        if search_term:
            query += " AND (title LIKE ? OR description LIKE ? OR tags LIKE ?)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # Format results
        gigs = []
        for row in results:
            gig = {
                "gig_id": row[0],
                "poster_id": row[1],
                "title": row[2],
                "description": row[3],
                "category": row[4],
                "price": row[5],
                "deadline": row[7],
                "created_at": row[9],
                "tags": json.loads(row[11] or "[]"),
                "requirements": row[12],
            }
            gigs.append(gig)

        return {
            "success": True,
            "gigs": gigs,
            "total_found": len(gigs),
            "filters_applied": {
                "category": category.value if category else "All",
                "price_range": f"{min_price}-{max_price}",
                "search_term": search_term,
            },
        }

    async def apply_to_gig(
        self,
        gig_id: str,
        applicant_id: str,
        application_text: str,
        proposed_price: Optional[float] = None,
        proposed_timeline: str = "",
    ) -> Dict:
        """📝 Apply to a gig posting"""

        # Check if gig exists and is open
        gig = self.get_gig_by_id(gig_id)
        if not gig:
            return {"success": False, "message": "❌ Gig not found!"}

        if gig["status"] != "open":
            return {
                "success": False,
                "message": "❌ This gig is no longer open for applications!",
            }

        if gig["poster_id"] == applicant_id:
            return {"success": False, "message": "❌ You cannot apply to your own gig!"}

        # Check if user already applied
        if self.has_user_applied(gig_id, applicant_id):
            return {
                "success": False,
                "message": "❌ You have already applied to this gig!",
            }

        # Generate application ID
        application_id = f"app_{int(time.time())}_{random.randint(1000, 9999)}"

        # Save application
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO gig_applications
            (application_id, gig_id, applicant_id, application_text,
             proposed_price, proposed_timeline, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
        """,
            (
                application_id,
                gig_id,
                applicant_id,
                application_text,
                proposed_price or gig["price"],
                proposed_timeline,
            ),
        )

        conn.commit()
        conn.close()

        return {
            "success": True,
            "application_id": application_id,
            "message": "✅ Application submitted successfully!",
            "gig_title": gig["title"],
            "gig_poster": gig["poster_id"],
        }

    def get_gig_by_id(self, gig_id: str) -> Optional[Dict]:
        """🔍 Get gig details by ID"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM gig_postings WHERE gig_id = ?", (gig_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return None

        return {
            "gig_id": result[0],
            "poster_id": result[1],
            "title": result[2],
            "description": result[3],
            "category": result[4],
            "price": result[5],
            "deadline": result[7],
            "status": result[8],
            "created_at": result[9],
            "tags": json.loads(result[11] or "[]"),
            "requirements": result[12],
        }

    def has_user_applied(self, gig_id: str, user_id: str) -> bool:
        """✅ Check if user has already applied to a gig"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 1 FROM gig_applications
            WHERE gig_id = ? AND applicant_id = ?
        """,
            (gig_id, user_id),
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def get_user_active_gigs_count(self, user_id: str) -> int:
        """📊 Get count of user's active gigs"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) FROM gig_postings
            WHERE poster_id = ? AND status IN ('open', 'in_progress')
        """,
            (user_id,),
        )

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else 0

    def get_user_applications(self, gig_id: str) -> List[Dict]:
        """📋 Get all applications for a gig"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM gig_applications
            WHERE gig_id = ?
            ORDER BY applied_at ASC
        """,
            (gig_id,),
        )

        results = cursor.fetchall()
        conn.close()

        applications = []
        for row in results:
            app = {
                "application_id": row[0],
                "gig_id": row[1],
                "applicant_id": row[2],
                "application_text": row[3],
                "proposed_price": row[5],
                "proposed_timeline": row[6],
                "status": row[7],
                "applied_at": row[8],
            }
            applications.append(app)

        return applications

    def update_user_profile_activity(self, user_id: str):
        """📊 Update user's marketplace activity timestamp"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO user_marketplace_profiles
            (user_id, last_active)
            VALUES (?, ?)
        """,
            (user_id, datetime.now().isoformat()),
        )

        conn.commit()
        conn.close()

    def get_user_profile(self, user_id: str) -> Dict:
        """👤 Get user's marketplace profile"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM user_marketplace_profiles WHERE user_id = ?
        """,
            (user_id,),
        )

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {
                "user_id": user_id,
                "total_gigs_completed": 0,
                "total_earnings": 0.0,
                "average_rating": 0.0,
                "total_reviews": 0,
            }

        return {
            "user_id": result[0],
            "skills": json.loads(result[1] or "[]"),
            "portfolio_url": result[2],
            "hourly_rate": result[3],
            "bio": result[4],
            "total_gigs_completed": result[5],
            "total_earnings": result[6],
            "average_rating": result[7],
            "total_reviews": result[8],
        }

    def get_marketplace_stats(self) -> Dict:
        """📈 Get overall marketplace statistics"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get various stats
        cursor.execute("SELECT COUNT(*) FROM gig_postings")
        total_gigs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM gig_postings WHERE status = 'open'")
        open_gigs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM gig_postings WHERE status = 'completed'")
        completed_gigs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM gig_applications")
        total_applications = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT poster_id) FROM gig_postings")
        active_posters = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT applicant_id) FROM gig_applications")
        active_applicants = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(price) FROM gig_postings WHERE status = 'completed'")
        total_value = cursor.fetchone()[0] or 0

        conn.close()

        return {
            "total_gigs": total_gigs,
            "open_gigs": open_gigs,
            "completed_gigs": completed_gigs,
            "total_applications": total_applications,
            "active_posters": active_posters,
            "active_applicants": active_applicants,
            "total_marketplace_value": total_value,
            "completion_rate": (
                (completed_gigs / total_gigs * 100) if total_gigs > 0 else 0
            ),
        }


class BroskiGigMarketplaceCommands(commands.Cog):
    """💼 Discord commands for the Gig Marketplace"""

    def __init__(self, bot):
        self.bot = bot
        self.marketplace = BroskiGigMarketplace()

    @discord.app_commands.command(
        name="post-gig", description="💼 Post a new gig to the marketplace!"
    )
    @discord.app_commands.describe(
        title="Gig title (keep it clear and concise)",
        description="Detailed description of what you need done",
        category="Type of work/skill required",
        price="Payment amount in BROski$ tokens",
        deadline_days="How many days from now is the deadline",
        requirements="Special requirements or qualifications needed",
    )
    async def post_gig(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        category: str,
        price: float,
        deadline_days: int,
        requirements: str = "",
    ):
        """Post a new gig to the marketplace"""

        user_id = str(interaction.user.id)

        # Parse category
        try:
            gig_category = None
            for cat in GigCategory:
                if category.lower() in cat.value.lower():
                    gig_category = cat
                    break

            if not gig_category:
                # Default mapping
                category_map = {
                    "design": GigCategory.DESIGN,
                    "code": GigCategory.CODING,
                    "coding": GigCategory.CODING,
                    "programming": GigCategory.CODING,
                    "write": GigCategory.WRITING,
                    "writing": GigCategory.WRITING,
                    "voice": GigCategory.VOICEOVER,
                    "audio": GigCategory.VOICEOVER,
                    "video": GigCategory.VIDEO,
                    "marketing": GigCategory.MARKETING,
                    "teach": GigCategory.TUTORING,
                    "tutor": GigCategory.TUTORING,
                    "music": GigCategory.MUSIC,
                    "game": GigCategory.GAMING,
                    "gaming": GigCategory.GAMING,
                }

                gig_category = category_map.get(category.lower(), GigCategory.OTHER)

        except Exception:
            gig_category = GigCategory.OTHER

        # Calculate deadline
        deadline = datetime.now() + timedelta(days=deadline_days)

        # Post the gig
        result = await self.marketplace.post_gig(
            user_id, title, description, gig_category, price, deadline, requirements
        )

        if result["success"]:
            embed = discord.Embed(
                title="💼 GIG POSTED SUCCESSFULLY! 💼",
                description=f"**{title}**",
                color=0x00FF88,
            )

            embed.add_field(
                name="📋 Gig Details",
                value=(
                    f"**Category:** {gig_category.value}\n"
                    f"**Price:** {price} BROski$\n"
                    f"**Deadline:** {deadline.strftime('%Y-%m-%d %H:%M')}\n"
                    f"**ID:** `{result['gig_id']}`"
                ),
                inline=False,
            )

            embed.add_field(
                name="💰 Posting Fee",
                value=f"Deducted {result['posting_fee']} BROski$ posting fee",
                inline=True,
            )

            embed.add_field(
                name="📢 Next Steps",
                value="Applications will be sent to your DMs!\nUse `/my-gigs` to manage your postings.",
                inline=True,
            )

            embed.set_footer(text="Gig posted to BROski Marketplace! 🚀")

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(result["message"], ephemeral=True)

    @discord.app_commands.command(
        name="browse-gigs", description="🔍 Browse available gigs in the marketplace!"
    )
    @discord.app_commands.describe(
        category="Filter by gig category",
        search="Search term for title/description",
        min_price="Minimum price filter",
        max_price="Maximum price filter",
    )
    async def browse_gigs(
        self,
        interaction: discord.Interaction,
        category: str = "",
        search: str = "",
        min_price: float = 0,
        max_price: float = 999999,
    ):
        """Browse available gigs with filtering"""

        # Parse category filter
        gig_category = None
        if category:
            for cat in GigCategory:
                if category.lower() in cat.value.lower():
                    gig_category = cat
                    break

        # Browse gigs
        result = self.marketplace.browse_gigs(
            category=gig_category,
            min_price=min_price,
            max_price=max_price,
            search_term=search,
            limit=5,  # Show 5 gigs per page
        )

        if not result["gigs"]:
            embed = discord.Embed(
                title="🔍 No Gigs Found",
                description="No gigs match your search criteria.",
                color=0x9966FF,
            )
            embed.add_field(
                name="💡 Try",
                value="• Broader search terms\n• Different category\n• Wider price range",
                inline=False,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title="💼 AVAILABLE GIGS 💼",
            description=f"Found {result['total_found']} gigs matching your criteria",
            color=0x00D4AA,
        )

        for gig in result["gigs"]:
            # Get poster username
            try:
                poster = self.bot.get_user(int(gig["poster_id"]))
                poster_name = (
                    poster.display_name if poster else f"User {gig['poster_id'][:8]}"
                )
            except:
                poster_name = f"User {gig['poster_id'][:8]}"

            # Format deadline
            deadline = datetime.fromisoformat(gig["deadline"])
            deadline_str = deadline.strftime("%m/%d %H:%M")

            embed.add_field(
                name=f"💼 {gig['title']}",
                value=(
                    f"**By:** {poster_name}\n"
                    f"**Price:** {gig['price']} BROski$\n"
                    f"**Category:** {gig['category']}\n"
                    f"**Deadline:** {deadline_str}\n"
                    f"**Apply:** `/apply-gig {gig['gig_id']}`"
                ),
                inline=True,
            )

        embed.set_footer(text="Use /apply-gig <gig_id> to apply! 💜")

        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(
        name="apply-gig", description="📝 Apply to a gig posting!"
    )
    @discord.app_commands.describe(
        gig_id="The ID of the gig you want to apply to",
        application_text="Your application message and qualifications",
        proposed_price="Your proposed price (optional)",
        timeline="Your estimated timeline for completion",
    )
    async def apply_gig(
        self,
        interaction: discord.Interaction,
        gig_id: str,
        application_text: str,
        proposed_price: Optional[float] = None,
        timeline: str = "",
    ):
        """Apply to a gig posting"""

        user_id = str(interaction.user.id)

        result = await self.marketplace.apply_to_gig(
            gig_id, user_id, application_text, proposed_price, timeline
        )

        if result["success"]:
            embed = discord.Embed(
                title="📝 APPLICATION SUBMITTED! 📝",
                description=f"Applied to: **{result['gig_title']}**",
                color=0x00FF88,
            )

            embed.add_field(
                name="✅ Application Status",
                value="Your application has been sent to the gig poster!",
                inline=False,
            )

            embed.add_field(
                name="📬 Next Steps",
                value="You'll receive a DM if you're selected for the gig.",
                inline=True,
            )

            embed.add_field(
                name="🔍 Track Applications",
                value="Use `/my-applications` to see all your applications.",
                inline=True,
            )

            # Send DM to gig poster
            try:
                poster = self.bot.get_user(int(result["gig_poster"]))
                if poster:
                    applicant_name = interaction.user.display_name
                    dm_embed = discord.Embed(
                        title="🔔 NEW GIG APPLICATION! 🔔",
                        description=f"**{applicant_name}** applied to your gig!",
                        color=0xFFD700,
                    )
                    dm_embed.add_field(
                        name="📋 Gig", value=f"**{result['gig_title']}**", inline=False
                    )
                    dm_embed.add_field(
                        name="📝 Application",
                        value=application_text[:500]
                        + ("..." if len(application_text) > 500 else ""),
                        inline=False,
                    )
                    if proposed_price:
                        dm_embed.add_field(
                            name="💰 Proposed Price",
                            value=f"{proposed_price} BROski$",
                            inline=True,
                        )
                    if timeline:
                        dm_embed.add_field(
                            name="⏰ Timeline", value=timeline, inline=True
                        )
                    dm_embed.add_field(
                        name="👤 Applicant",
                        value=f"{applicant_name} ({interaction.user.mention})",
                        inline=False,
                    )

                    await poster.send(embed=dm_embed)
            except Exception as e:
                print(f"❌ Failed to send DM to gig poster: {e}")

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(result["message"], ephemeral=True)

    @discord.app_commands.command(
        name="marketplace-stats",
        description="📊 View marketplace statistics and trends",
    )
    async def marketplace_stats(self, interaction: discord.Interaction):
        """Show marketplace statistics"""

        stats = self.marketplace.get_marketplace_stats()

        embed = discord.Embed(
            title="📊 BROSKI GIG MARKETPLACE STATS 📊",
            description="The pulse of our talent economy!",
            color=0x9966FF,
        )

        embed.add_field(
            name="💼 Gig Activity",
            value=(
                f"**Total Gigs:** {stats['total_gigs']}\n"
                f"**Open Gigs:** {stats['open_gigs']}\n"
                f"**Completed:** {stats['completed_gigs']}\n"
                f"**Success Rate:** {stats['completion_rate']:.1f}%"
            ),
            inline=True,
        )

        embed.add_field(
            name="👥 Community Engagement",
            value=(
                f"**Total Applications:** {stats['total_applications']}\n"
                f"**Active Posters:** {stats['active_posters']}\n"
                f"**Active Applicants:** {stats['active_applicants']}\n"
                f"**Marketplace Value:** {stats['total_marketplace_value']:.1f} BROski$"
            ),
            inline=True,
        )

        embed.add_field(
            name="🚀 Growing Economy",
            value=(
                "💰 Earning opportunities for everyone\n"
                "🎯 Skill-based job matching\n"
                "🤝 Community-powered marketplace\n"
                "💎 BROski$ token integration"
            ),
            inline=False,
        )

        embed.set_footer(text="Building the future of work, one gig at a time! 💜")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Setup function for Discord bot"""
    await bot.add_cog(BroskiGigMarketplaceCommands(bot))


# Export classes
__all__ = [
    "BroskiGigMarketplace",
    "BroskiGigMarketplaceCommands",
    "GigCategory",
    "GigStatus",
]
