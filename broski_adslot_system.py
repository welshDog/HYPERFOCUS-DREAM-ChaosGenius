#!/usr/bin/env python3
"""
💥 BROSKI ULTRA AD SLOT SYSTEM - FULL STACK BUILD MODE 💥
📁 File: broski_adslot_system.py (Flask + JSON storage + ULTRA FEATURES)
"""

import hashlib
import json
import os
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import discord
import requests
from discord.ext import commands
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

ADS_FILE = "adslots.json"
TOKENS_FILE = "broski_tokens.db"
ANALYTICS_DB = "broski_analytics.db"
UPLOAD_FOLDER = "ad_uploads"
MAX_SLOTS = 5
EXPIRATION_SECONDS = 3 * 24 * 3600  # 3 days
BASE_SLOT_COST = 100  # Base BROski$ cost per slot
REQUEST_TIMEOUT = 10  # Request timeout in seconds
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🏗️ ULTRA FEATURE 1: ANALYTICS DATABASE SETUP
def init_analytics_db():
    """Initialize analytics database"""
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()

    # Analytics table for tracking views, clicks, etc.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot INTEGER NOT NULL,
            event_type TEXT NOT NULL,  -- 'view', 'click', 'claim', 'expire'
            user_id TEXT,
            user_agent TEXT,
            ip_address TEXT,
            timestamp INTEGER NOT NULL,
            ad_title TEXT,
            revenue REAL DEFAULT 0,
            metadata TEXT  -- JSON string for extra data
        )
    """
    )

    # Revenue tracking table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS revenue_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_revenue REAL DEFAULT 0,
            total_claims INTEGER DEFAULT 0,
            unique_users INTEGER DEFAULT 0,
            peak_hour INTEGER DEFAULT 12
        )
    """
    )

    # Pricing history table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pricing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot INTEGER NOT NULL,
            price REAL NOT NULL,
            demand_factor REAL DEFAULT 1.0,
            time_factor REAL DEFAULT 1.0,
            timestamp INTEGER NOT NULL
        )
    """
    )

    conn.commit()
    conn.close()


# 🧠 ULTRA FEATURE 2: DYNAMIC PRICING ENGINE
def calculate_dynamic_price(slot: int) -> int:
    """Calculate dynamic pricing based on demand and time"""
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()

    # Get current hour for time-based pricing
    current_hour = datetime.now().hour

    # Peak hours (9 AM - 9 PM) cost more
    if 9 <= current_hour <= 21:
        time_multiplier = 1.5  # 50% more during peak hours
    else:
        time_multiplier = 0.8  # 20% discount during off-peak

    # Get recent claim activity for demand calculation
    week_ago = int(time.time()) - (7 * 24 * 3600)
    cursor.execute(
        """
        SELECT COUNT(*) FROM analytics
        WHERE event_type = 'claim' AND timestamp > ?
    """,
        (week_ago,),
    )

    recent_claims = cursor.fetchone()[0]

    # Demand multiplier based on recent activity
    if recent_claims > 20:
        demand_multiplier = 1.8  # High demand
    elif recent_claims > 10:
        demand_multiplier = 1.3  # Medium demand
    else:
        demand_multiplier = 0.9  # Low demand

    # Get slot-specific demand (popular slots cost more)
    cursor.execute(
        """
        SELECT COUNT(*) FROM analytics
        WHERE slot = ? AND event_type IN ('view', 'click') AND timestamp > ?
    """,
        (slot, week_ago),
    )

    slot_popularity = cursor.fetchone()[0]
    slot_multiplier = 1.0 + (slot_popularity * 0.01)  # 1% increase per view/click

    # Calculate final price
    base_price = BASE_SLOT_COST
    final_price = int(
        base_price * time_multiplier * demand_multiplier * slot_multiplier
    )

    # Ensure minimum price of 50 and maximum of 500
    final_price = max(50, min(500, final_price))

    # Log pricing decision
    cursor.execute(
        """
        INSERT INTO pricing_history
        (slot, price, demand_factor, time_factor, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """,
        (slot, final_price, demand_multiplier, time_multiplier, int(time.time())),
    )

    conn.commit()
    conn.close()

    return final_price


# 📊 ANALYTICS TRACKING FUNCTIONS
def track_event(
    event_type: str,
    slot: int = None,
    user_id: str = None,
    ad_title: str = None,
    revenue: float = 0,
    **kwargs,
):
    """Track analytics events"""
    try:
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()

        metadata = json.dumps(kwargs) if kwargs else None

        cursor.execute(
            """
            INSERT INTO analytics
            (slot, event_type, user_id, user_agent, ip_address, timestamp, ad_title, revenue, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                slot,
                event_type,
                user_id,
                request.headers.get("User-Agent", "") if request else "",
                request.remote_addr if request else "",
                int(time.time()),
                ad_title,
                revenue,
                metadata,
            ),
        )

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Analytics tracking error: {e}")


# 🎨 ULTRA FEATURE 3: IMAGE UPLOAD FUNCTIONS
def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_secure_filename(filename, user_id):
    """Generate a secure, unique filename"""
    timestamp = str(int(time.time()))
    hash_input = f"{user_id}_{timestamp}_{filename}"
    file_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    extension = filename.rsplit(".", 1)[1].lower()
    return f"ad_{user_id}_{timestamp}_{file_hash}.{extension}"


# 🔧 Ensure adslots file exists
def load_ads() -> List[Dict[str, Any]]:
    """Load advertisements from JSON file"""
    if not os.path.exists(ADS_FILE):
        with open(ADS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(ADS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def save_ads(data: List[Dict[str, Any]]) -> None:
    """Save advertisements to JSON file"""
    with open(ADS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# 🪙 Token balance checker
def check_user_balance(user_id: str) -> int:
    """Check user's BROski$ balance"""
    try:
        with open(TOKENS_FILE, "r", encoding="utf-8") as f:
            tokens = json.load(f)
        balance = tokens.get(str(user_id), {}).get("balance", 0)
        return int(balance) if isinstance(balance, (int, float)) else 0
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 0


def deduct_tokens(user_id: str, amount: int) -> bool:
    """Deduct tokens from user balance"""
    try:
        with open(TOKENS_FILE, "r", encoding="utf-8") as f:
            tokens = json.load(f)

        if str(user_id) not in tokens:
            tokens[str(user_id)] = {"balance": 0}

        if tokens[str(user_id)]["balance"] >= amount:
            tokens[str(user_id)]["balance"] -= amount
            with open(TOKENS_FILE, "w", encoding="utf-8") as f:
                json.dump(tokens, f, indent=2)
            return True
        return False
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return False


# 🧠 GET current ad slots
@app.route("/api/adslots", methods=["GET"])
def get_ads() -> Any:
    """Get all active advertisement slots"""
    ads = load_ads()
    current_time = int(time.time())
    active_ads = [
        ad for ad in ads if current_time - ad["timestamp"] <= EXPIRATION_SECONDS
    ]

    # Track view events for each ad
    for ad in active_ads:
        track_event("view", slot=ad["slot"], ad_title=ad["title"])

    return jsonify(active_ads)


# 🎯 NEW: GET dynamic pricing for slot
@app.route("/api/adslots/<int:slot>/price", methods=["GET"])
def get_slot_price(slot: int) -> Any:
    """Get current dynamic price for a slot"""
    if slot < 1 or slot > MAX_SLOTS:
        return jsonify({"error": "Invalid slot number"}), 400

    price = calculate_dynamic_price(slot)

    return jsonify(
        {
            "slot": slot,
            "price": price,
            "base_price": BASE_SLOT_COST,
            "timestamp": int(time.time()),
        }
    )


# 🎨 NEW: Image upload endpoint
@app.route("/api/upload", methods=["POST"])
def upload_image() -> Any:
    """Upload and process ad image"""
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    user_id = request.form.get("user_id", "anonymous")

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return (
            jsonify({"error": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP"}),
            400,
        )

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": "File too large. Maximum size: 5MB"}), 400

    # Generate secure filename and save
    filename = generate_secure_filename(file.filename, user_id)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Track upload event
    track_event("upload", user_id=user_id, file_size=file_size, filename=filename)

    return jsonify(
        {
            "status": "Image uploaded successfully",
            "filename": filename,
            "url": f"/api/images/{filename}",
            "size": file_size,
        }
    )


# 🖼️ Serve uploaded images
@app.route("/api/images/<filename>")
def uploaded_file(filename):
    """Serve uploaded images"""
    return send_from_directory(UPLOAD_FOLDER, filename)


# 🤖 POST new ad slot (UPDATED with dynamic pricing)
@app.route("/api/adslots/claim", methods=["POST"])
def claim_ad() -> Any:
    """Claim an advertisement slot with dynamic pricing"""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["slot", "title", "url", "image", "user"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field"}), 400

    ads = load_ads()
    slot = int(data["slot"])
    if slot < 1 or slot > MAX_SLOTS:
        return jsonify({"error": "Invalid slot number"}), 400

    # Calculate dynamic price for this slot
    slot_cost = calculate_dynamic_price(slot)

    # Check if user has enough tokens
    user_id = data["user"]
    if not deduct_tokens(user_id, slot_cost):
        return (
            jsonify({"error": f"Insufficient BROski$ balance. Need {slot_cost}"}),
            400,
        )

    # Remove any existing ad in that slot
    ads = [ad for ad in ads if ad["slot"] != slot]

    # Add new ad
    ad_entry = {
        "slot": slot,
        "title": data["title"],
        "url": data["url"],
        "image": data["image"],
        "user": data["user"],
        "user_name": data.get("user_name", "Anonymous"),
        "timestamp": int(time.time()),
        "expires": int(time.time()) + EXPIRATION_SECONDS,
        "cost_paid": slot_cost,  # Track actual cost paid
    }
    ads.append(ad_entry)
    save_ads(ads)

    # Track claim event and revenue
    track_event(
        "claim",
        slot=slot,
        user_id=user_id,
        ad_title=data["title"],
        revenue=slot_cost,
        cost_paid=slot_cost,
    )

    return jsonify(
        {
            "status": "Ad slot claimed!",
            "ad": ad_entry,
            "cost": slot_cost,
            "base_cost": BASE_SLOT_COST,
        }
    )


# 📊 NEW: Analytics dashboard endpoint
@app.route("/api/analytics/dashboard", methods=["GET"])
def analytics_dashboard() -> Any:
    """Get analytics dashboard data"""
    conn = sqlite3.connect(ANALYTICS_DB)
    cursor = conn.cursor()

    # Total revenue
    cursor.execute("SELECT SUM(revenue) FROM analytics WHERE revenue > 0")
    total_revenue = cursor.fetchone()[0] or 0

    # Total claims
    cursor.execute("SELECT COUNT(*) FROM analytics WHERE event_type = 'claim'")
    total_claims = cursor.fetchone()[0] or 0

    # Unique users
    cursor.execute(
        "SELECT COUNT(DISTINCT user_id) FROM analytics WHERE user_id IS NOT NULL"
    )
    unique_users = cursor.fetchone()[0] or 0

    # Recent activity (last 24 hours)
    day_ago = int(time.time()) - (24 * 3600)
    cursor.execute(
        """
        SELECT event_type, COUNT(*) FROM analytics
        WHERE timestamp > ?
        GROUP BY event_type
    """,
        (day_ago,),
    )
    recent_activity = dict(cursor.fetchall())

    # Popular slots
    cursor.execute(
        """
        SELECT slot, COUNT(*) as views FROM analytics
        WHERE event_type = 'view' AND slot IS NOT NULL
        GROUP BY slot ORDER BY views DESC LIMIT 5
    """,
    )
    popular_slots = cursor.fetchall()

    # Revenue by day (last 7 days)
    revenue_by_day = []
    for i in range(7):
        day_start = int(time.time()) - (i * 24 * 3600)
        day_end = day_start + (24 * 3600)
        cursor.execute(
            """
            SELECT SUM(revenue) FROM analytics
            WHERE revenue > 0 AND timestamp BETWEEN ? AND ?
        """,
            (day_start, day_end),
        )
        daily_revenue = cursor.fetchone()[0] or 0
        date_str = datetime.fromtimestamp(day_start).strftime("%Y-%m-%d")
        revenue_by_day.append({"date": date_str, "revenue": daily_revenue})

    conn.close()

    return jsonify(
        {
            "total_revenue": total_revenue,
            "total_claims": total_claims,
            "unique_users": unique_users,
            "recent_activity": recent_activity,
            "popular_slots": [
                {"slot": slot, "views": views} for slot, views in popular_slots
            ],
            "revenue_by_day": list(reversed(revenue_by_day)),
            "timestamp": int(time.time()),
        }
    )


# 📈 NEW: Click tracking endpoint
@app.route("/api/adslots/<int:slot>/click", methods=["POST"])
def track_click(slot: int) -> Any:
    """Track ad click"""
    data = request.json or {}
    user_id = data.get("user_id")

    # Get ad info
    ads = load_ads()
    ad = next((ad for ad in ads if ad["slot"] == slot), None)

    if not ad:
        return jsonify({"error": "Ad not found"}), 404

    # Track click event
    track_event("click", slot=slot, user_id=user_id, ad_title=ad["title"])

    return jsonify({"status": "Click tracked", "redirect_url": ad["url"]})


# Initialize analytics database on startup
init_analytics_db()

# 🤖 DISCORD BOT INTEGRATION
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    """Bot ready event handler"""
    print(f"🤖 BROski Adslot Bot is ONLINE! Logged in as {bot.user}")


@bot.command(name="adslot")
async def adslot_command(
    ctx: commands.Context,
    action: Optional[str] = None,
    slot: Optional[str] = None,
    *args: str,
) -> None:
    """
    🎯 Main adslot command
    !adslot claim 1 "My Title" "https://link" "https://image"
    !adslot status
    !adslot cancel 1 (admin only)
    """

    if action == "claim":
        await handle_claim(ctx, slot, args)
    elif action == "status":
        await handle_status(ctx)
    elif action == "cancel":
        await handle_cancel(ctx, slot)
    else:
        embed = discord.Embed(
            title="🎯 BROski Adslot System",
            description="**Available Commands:**\n"
            '`!adslot claim <slot> "title" "url" "image"`\n'
            "`!adslot status` - View all active slots\n"
            "`!adslot cancel <slot>` - Admin only",
            color=0xFF6EF7,
        )
        embed.add_field(name="💰 Cost", value=f"{SLOT_COST} BROski$", inline=True)
        embed.add_field(name="⏰ Duration", value="3 days", inline=True)
        await ctx.send(embed=embed)


async def handle_claim(ctx: commands.Context, slot: Optional[str], args: tuple) -> None:
    """Handle ad slot claiming"""
    try:
        if not slot or not slot.isdigit():
            await ctx.send("❌ Please specify a slot number (1-5)")
            return

        slot_num = int(slot)
        if slot_num < 1 or slot_num > MAX_SLOTS:
            await ctx.send(f"❌ Slot must be between 1 and {MAX_SLOTS}")
            return

        if len(args) < 3:
            await ctx.send('❌ Usage: `!adslot claim <slot> "title" "url" "image"`')
            return

        title = args[0].strip('"')
        url = args[1].strip('"')
        image = args[2].strip('"')

        # Check user balance
        balance = check_user_balance(str(ctx.author.id))
        if balance < SLOT_COST:
            embed = discord.Embed(
                title="💸 Insufficient BROski$",
                description=(f"You need {SLOT_COST} BROski$ but only have {balance}"),
                color=0xFF4444,
            )
            await ctx.send(embed=embed)
            return

        # Make API call
        payload = {
            "slot": slot_num,
            "title": title,
            "url": url,
            "image": image,
            "user": str(ctx.author.id),
            "user_name": ctx.author.display_name,
        }

        response = requests.post(
            "http://localhost:5001/api/adslots/claim",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            data = response.json()
            expires_dt = datetime.fromtimestamp(data["ad"]["expires"])

            embed = discord.Embed(
                title="🎯 Ad Slot Claimed Successfully!",
                description=f"**Slot #{slot_num}** is now yours!",
                color=0x00FF88,
            )
            embed.add_field(name="📝 Title", value=title, inline=False)
            embed.add_field(name="🔗 URL", value=url, inline=False)
            embed.add_field(name="💰 Cost", value=f"{SLOT_COST} BROski$", inline=True)
            embed.add_field(
                name="⏰ Expires",
                value=expires_dt.strftime("%Y-%m-%d %H:%M"),
                inline=True,
            )
            embed.set_thumbnail(url=image)
            embed.set_footer(text=f"Claimed by {ctx.author.display_name}")

            await ctx.send(embed=embed)
        else:
            error_data = response.json()
            error_msg = error_data.get("error", "Unknown error")
            await ctx.send(f"❌ Error: {error_msg}")

    except requests.RequestException as e:
        await ctx.send(f"❌ Network error: {str(e)}")
    except (ValueError, KeyError) as e:
        await ctx.send(f"❌ Error processing claim: {str(e)}")


async def handle_status(ctx: commands.Context) -> None:
    """Show all active ad slots"""
    try:
        response = requests.get(
            "http://localhost:5001/api/adslots", timeout=REQUEST_TIMEOUT
        )
        ads = response.json()

        embed = discord.Embed(
            title="🎯 Active Ad Slots",
            description="Current advertising lineup",
            color=0x00BFFF,
        )

        if not ads:
            embed.add_field(
                name="💭 No Active Ads", value="All slots are available!", inline=False
            )
        else:
            for ad in sorted(ads, key=lambda x: x["slot"]):
                expires_dt = datetime.fromtimestamp(ad["expires"])
                time_left = expires_dt - datetime.now()

                embed.add_field(
                    name=f"🎯 Slot #{ad['slot']} - {ad['title']}",
                    value=f"👤 {ad['user_name']}\n"
                    f"⏰ {time_left.days}d {time_left.seconds//3600}h left\n"
                    f"🔗 [Visit]({ad['url']})",
                    inline=True,
                )

        embed.set_footer(
            text=f"💰 Claim a slot for {SLOT_COST} BROski$ | " "!adslot claim <slot>"
        )
        await ctx.send(embed=embed)

    except requests.RequestException as e:
        await ctx.send(f"❌ Network error: {str(e)}")
    except (ValueError, KeyError) as e:
        await ctx.send(f"❌ Error fetching slots: {str(e)}")


async def handle_cancel(ctx: commands.Context, slot: Optional[str]) -> None:
    """Admin-only slot cancellation"""
    # Check if user is admin (fixed permission check)
    if not isinstance(ctx.author, discord.Member):
        await ctx.send("❌ This command only works in a server!")
        return

    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Admin only command!")
        return

    try:
        if not slot or not slot.isdigit():
            await ctx.send("❌ Please specify a slot number")
            return

        response = requests.delete(
            f"http://localhost:5001/api/adslots/{slot}", timeout=REQUEST_TIMEOUT
        )
        data = response.json()

        embed = discord.Embed(
            title="🗑️ Slot Cleared",
            description=f"Slot #{slot} has been cleared by admin",
            color=0xFF8800,
        )

        if data.get("deleted_ad"):
            embed.add_field(
                name="🔄 Refund Processing", value="User will be notified", inline=False
            )

        await ctx.send(embed=embed)

    except requests.RequestException as e:
        await ctx.send(f"❌ Network error: {str(e)}")
    except (ValueError, KeyError) as e:
        await ctx.send(f"❌ Error clearing slot: {str(e)}")


# 🧪 Run Flask API
def run_flask() -> None:
    """Run Flask API server"""
    app.run(debug=True, port=5001, host="0.0.0.0")


# 🤖 Run Discord Bot
def run_bot() -> None:
    """Run Discord bot"""
    # Load bot token from config
    try:
        with open("broski_token_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        bot.run(config["discord_token"])
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print("❌ Discord token not found in broski_token_config.json")


# 🚀 MAIN LAUNCHER - PRODUCTION READY
if __name__ == "__main__":
    import threading

    print("🔥💜 STARTING BROSKI ULTRA ADSLOT SYSTEM!!! 💜🔥")

    # Run Flask API in production mode (no debug for threading)
    flask_thread = threading.Thread(
        target=lambda: app.run(port=5001, host="0.0.0.0", debug=False), daemon=True
    )
    flask_thread.start()

    print("✅ Flask API started on port 5001")

    # Run Discord bot
    print("🤖 Starting Discord bot...")
    run_bot()
