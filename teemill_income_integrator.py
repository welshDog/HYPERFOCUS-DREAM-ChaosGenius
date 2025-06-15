#!/usr/bin/env python3
"""
💗❤️‍🔥 TEEMILL INCOME INTEGRATION OVERLORD ❤️‍🔥💗
🫱🏼‍🫲🏻💪🦾❤️‍🔥💯😎♾️ PASSIVE MERCH SALES EMPIRE 💯😎♾️💪🦾❤️‍🔥🫱🏼‍🫲🏻

Auto-connects Teemill sales to your infinite money portals!
"""

import asyncio
import json
import logging
import re
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import requests
from flask import Flask, jsonify, request, send_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeemillIncomeIntegrator:
    """💗 The ultimate Teemill-to-income feed connector! 💗"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.teemill_db = f"{self.base_path}/teemill_sales.db"
        self.sales_log = f"{self.base_path}/teemill_sales_feed.json"
        self.app = Flask(__name__)

        # Teemill product data
        self.product_catalog = {}
        self.sales_tracking = {
            "total_sales": 0.0,
            "daily_sales": 0.0,
            "monthly_sales": 0.0,
            "top_products": {},
            "conversion_rate": 0.0,
            "traffic_sources": {}
        }

        # Revenue integration
        self.money_maker_url = "http://localhost:5008"
        self.broski_portal_active = True

        print("💗❤️‍🔥 TEEMILL INCOME INTEGRATOR ONLINE! ❤️‍🔥💗")
        self._initialize_teemill_database()
        self._setup_flask_routes()
        self._load_existing_products()

    def _initialize_teemill_database(self):
        """🗄️ Initialize Teemill sales tracking database"""
        try:
            with sqlite3.connect(self.teemill_db) as conn:
                cursor = conn.cursor()

                # Sales transactions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS teemill_sales (
                        sale_id TEXT PRIMARY KEY,
                        timestamp REAL,
                        product_name TEXT,
                        product_id TEXT,
                        variant TEXT,
                        quantity INTEGER,
                        unit_price REAL,
                        total_amount REAL,
                        currency TEXT DEFAULT 'GBP',
                        customer_country TEXT,
                        traffic_source TEXT,
                        conversion_type TEXT DEFAULT 'organic',
                        broski_reward REAL DEFAULT 0.0,
                        status TEXT DEFAULT 'COMPLETED'
                    )
                """)

                # Product performance table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS product_performance (
                        product_id TEXT PRIMARY KEY,
                        product_name TEXT,
                        total_sales REAL DEFAULT 0.0,
                        units_sold INTEGER DEFAULT 0,
                        views INTEGER DEFAULT 0,
                        conversion_rate REAL DEFAULT 0.0,
                        last_sale REAL,
                        performance_score REAL DEFAULT 0.0,
                        trending_status TEXT DEFAULT 'stable'
                    )
                """)

                # Analytics integration table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analytics_data (
                        date_recorded TEXT,
                        total_visitors INTEGER,
                        product_views INTEGER,
                        add_to_carts INTEGER,
                        checkouts_started INTEGER,
                        sales_completed INTEGER,
                        revenue_generated REAL,
                        top_traffic_source TEXT,
                        conversion_rate REAL
                    )
                """)

                conn.commit()
                logger.info("💗 Teemill database initialized successfully!")

        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")

    def _setup_flask_routes(self):
        """🔗 Setup API routes for Teemill integration"""

        @self.app.route("/")
        def dashboard_home():
            """🏠 Serve the beautiful Teemill dashboard"""
            try:
                dashboard_path = f"{self.base_path}/teemill_dashboard.html"
                return send_file(dashboard_path)
            except Exception as e:
                return f"<h1>💗 Teemill Dashboard Loading...</h1><p>Please ensure teemill_dashboard.html exists: {e}</p>"

        @self.app.route("/api/teemill/webhook", methods=["POST"])
        def teemill_webhook():
            """📬 Receive Teemill sale notifications"""
            try:
                data = request.get_json()
                if data and "sale" in data:
                    sale_result = self.process_teemill_sale(data["sale"])
                    return jsonify({"status": "success", "sale_processed": sale_result})
                return jsonify({"error": "Invalid webhook data"}), 400
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/teemill/manual_sale", methods=["POST"])
        def manual_sale_entry():
            """✋ Manual sale entry for gamification"""
            try:
                data = request.get_json()
                sale_data = {
                    "product_name": data.get("product", "Manual Entry"),
                    "amount": float(data.get("amount", 0)),
                    "currency": data.get("currency", "GBP"),
                    "quantity": int(data.get("quantity", 1)),
                    "source": "manual_entry"
                }

                result = self.process_teemill_sale(sale_data)
                return jsonify({"status": "LEGENDARY SALE RECORDED!", "result": result})

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/teemill/dashboard")
        def teemill_dashboard():
            """📊 Get Teemill performance dashboard"""
            return jsonify(self.get_teemill_analytics())

        @self.app.route("/api/teemill/sync_products")
        def sync_products():
            """🔄 Sync product catalog"""
            result = self.sync_product_catalog()
            return jsonify({"status": "success", "products_synced": result})

    def process_teemill_sale(self, sale_data: Dict) -> Dict:
        """💰 Process a Teemill sale and integrate with income feeds"""
        try:
            sale_id = f"teemill_{int(time.time())}_{sale_data.get('product_name', 'unknown').replace(' ', '_')}"

            # Extract sale details
            product_name = sale_data.get("product_name", "Unknown Product")
            amount = float(sale_data.get("amount", 0))
            currency = sale_data.get("currency", "GBP")
            quantity = int(sale_data.get("quantity", 1))
            unit_price = amount / quantity if quantity > 0 else amount

            # Calculate BROski$ reward (10% of sale value)
            broski_reward = amount * 0.1

            # Record in database
            with sqlite3.connect(self.teemill_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO teemill_sales
                    (sale_id, timestamp, product_name, quantity, unit_price, total_amount,
                     currency, traffic_source, broski_reward, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    sale_id, time.time(), product_name, quantity, unit_price, amount,
                    currency, sale_data.get("source", "organic"), broski_reward, "COMPLETED"
                ))
                conn.commit()

            # Update tracking stats
            self.sales_tracking["total_sales"] += amount
            self.sales_tracking["daily_sales"] += amount

            # Connect to money portals
            income_result = self._send_to_income_portals(sale_id, amount, product_name, broski_reward)

            # Update product performance
            self._update_product_performance(product_name, amount, quantity)

            # Log to JSON feed
            self._log_to_sales_feed(sale_data, sale_id, broski_reward)

            logger.info(f"💗 TEEMILL SALE PROCESSED: {product_name} - £{amount:.2f} (+{broski_reward:.1f} BROski$)")

            return {
                "sale_id": sale_id,
                "amount": amount,
                "currency": currency,
                "broski_reward": broski_reward,
                "income_portal_status": income_result,
                "status": "LEGENDARY SUCCESS!"
            }

        except Exception as e:
            logger.error(f"Sale processing error: {e}")
            return {"error": str(e)}

    def _send_to_income_portals(self, sale_id: str, amount: float, product: str, broski_reward: float) -> Dict:
        """🔗 Send sale data to income portals"""
        results = {}

        try:
            # Send to Infinite Money Maker
            if self.broski_portal_active:
                money_data = {
                    "stream_name": "teemill_merch_sales",
                    "amount": amount,
                    "description": f"Teemill Sale: {product}",
                    "category": "PASSIVE_INCOME",
                    "source": "Teemill Store",
                    "broski_reward": broski_reward
                }

                # Try to post to money portal
                try:
                    response = requests.post(
                        f"{self.money_maker_url}/api/money/record_income",
                        json=money_data,
                        timeout=5
                    )
                    if response.status_code == 200:
                        results["infinite_money_maker"] = "SUCCESS"
                    else:
                        results["infinite_money_maker"] = "OFFLINE - LOGGED LOCALLY"
                except:
                    results["infinite_money_maker"] = "OFFLINE - LOGGED LOCALLY"

            # Update Broski Money Maker Portal
            try:
                broski_db = f"{self.base_path}/broski_money_maker.db"
                with sqlite3.connect(broski_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO income_transactions
                        (transaction_id, timestamp, income_source, amount, currency, category, description, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        sale_id, time.time(), "Teemill Store", amount, "GBP",
                        "PASSIVE_INCOME", f"Merch Sale: {product}", "COMPLETED"
                    ))
                    conn.commit()
                    results["broski_money_portal"] = "SUCCESS"
            except Exception as e:
                results["broski_money_portal"] = f"ERROR: {e}"

            return results

        except Exception as e:
            logger.error(f"Income portal integration error: {e}")
            return {"error": str(e)}

    def _update_product_performance(self, product_name: str, sale_amount: float, quantity: int):
        """📈 Update product performance metrics"""
        try:
            with sqlite3.connect(self.teemill_db) as conn:
                cursor = conn.cursor()

                # Check if product exists
                existing = cursor.execute(
                    "SELECT total_sales, units_sold FROM product_performance WHERE product_name = ?",
                    (product_name,)
                ).fetchone()

                if existing:
                    new_total = existing[0] + sale_amount
                    new_units = existing[1] + quantity
                    cursor.execute("""
                        UPDATE product_performance
                        SET total_sales = ?, units_sold = ?, last_sale = ?, performance_score = ?
                        WHERE product_name = ?
                    """, (new_total, new_units, time.time(), new_total * new_units, product_name))
                else:
                    cursor.execute("""
                        INSERT INTO product_performance
                        (product_name, total_sales, units_sold, last_sale, performance_score)
                        VALUES (?, ?, ?, ?, ?)
                    """, (product_name, sale_amount, quantity, time.time(), sale_amount * quantity))

                conn.commit()

        except Exception as e:
            logger.error(f"Product performance update error: {e}")

    def _log_to_sales_feed(self, sale_data: Dict, sale_id: str, broski_reward: float):
        """📝 Log sale to JSON feed for analytics"""
        try:
            feed_entry = {
                "timestamp": datetime.now().isoformat(),
                "sale_id": sale_id,
                "sale_data": sale_data,
                "broski_reward": broski_reward,
                "integration_status": "SUCCESS"
            }

            # Load existing feed
            if Path(self.sales_log).exists():
                with open(self.sales_log, 'r') as f:
                    feed = json.load(f)
            else:
                feed = {"sales": [], "total_revenue": 0.0, "total_broski_earned": 0.0}

            # Add new sale
            feed["sales"].append(feed_entry)
            feed["total_revenue"] += sale_data.get("amount", 0)
            feed["total_broski_earned"] += broski_reward

            # Keep only last 1000 sales
            if len(feed["sales"]) > 1000:
                feed["sales"] = feed["sales"][-1000:]

            # Save updated feed
            with open(self.sales_log, 'w') as f:
                json.dump(feed, f, indent=2)

        except Exception as e:
            logger.error(f"Sales feed logging error: {e}")

    def _load_existing_products(self):
        """📦 Load existing product catalog"""
        try:
            product_file = f"{self.base_path}/teemill_products.json"
            if Path(product_file).exists():
                with open(product_file, 'r') as f:
                    self.product_catalog = json.load(f)
                logger.info(f"💗 Loaded {len(self.product_catalog)} Teemill products")
            else:
                logger.info("💗 No existing product catalog found - will create on first sync")
        except Exception as e:
            logger.error(f"Product catalog loading error: {e}")

    def sync_product_catalog(self) -> int:
        """🔄 Sync product catalog from Teemill"""
        # Since we don't have direct API access, this is for manual updates
        sample_products = {
            "hyperfocus_hoodie": {
                "name": "HyperFocus Zone Hoodie",
                "price": 29.99,
                "currency": "GBP",
                "category": "apparel",
                "status": "active"
            },
            "broski_tshirt": {
                "name": "BROski Empire T-Shirt",
                "price": 19.99,
                "currency": "GBP",
                "category": "apparel",
                "status": "active"
            },
            "chaos_genius_mug": {
                "name": "ChaosGenius Coffee Mug",
                "price": 12.99,
                "currency": "GBP",
                "category": "accessories",
                "status": "active"
            }
        }

        self.product_catalog.update(sample_products)

        # Save catalog
        try:
            with open(f"{self.base_path}/teemill_products.json", 'w') as f:
                json.dump(self.product_catalog, f, indent=2)
            return len(sample_products)
        except Exception as e:
            logger.error(f"Product sync error: {e}")
            return 0

    def get_teemill_analytics(self) -> Dict:
        """📊 Get comprehensive Teemill analytics"""
        try:
            with sqlite3.connect(self.teemill_db) as conn:
                cursor = conn.cursor()

                # Total sales
                total_sales = cursor.execute(
                    "SELECT SUM(total_amount) FROM teemill_sales WHERE status = 'COMPLETED'"
                ).fetchone()[0] or 0

                # Today's sales
                today_start = time.time() - (time.time() % 86400)
                today_sales = cursor.execute(
                    "SELECT SUM(total_amount) FROM teemill_sales WHERE timestamp >= ? AND status = 'COMPLETED'",
                    (today_start,)
                ).fetchone()[0] or 0

                # Top products
                top_products = cursor.execute("""
                    SELECT product_name, SUM(total_amount) as revenue, SUM(quantity) as units
                    FROM teemill_sales WHERE status = 'COMPLETED'
                    GROUP BY product_name ORDER BY revenue DESC LIMIT 5
                """).fetchall()

                # Total BROski$ earned
                total_broski = cursor.execute(
                    "SELECT SUM(broski_reward) FROM teemill_sales WHERE status = 'COMPLETED'"
                ).fetchone()[0] or 0

                return {
                    "💗 Total Teemill Revenue": f"£{total_sales:.2f}",
                    "📈 Today's Sales": f"£{today_sales:.2f}",
                    "💰 Total BROski$ Earned": f"{total_broski:.1f} BROski$",
                    "🏆 Top Products": [
                        {"product": p[0], "revenue": f"£{p[1]:.2f}", "units": p[2]}
                        for p in top_products
                    ],
                    "📦 Products in Catalog": len(self.product_catalog),
                    "🔄 Integration Status": "LEGENDARY ACTIVE",
                    "🎯 Daily Goal": "£50.00",
                    "📊 Conversion Rate": f"{self.sales_tracking.get('conversion_rate', 0):.1f}%"
                }

        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return {"error": str(e)}

    def email_sale_parser(self, email_content: str) -> Optional[Dict]:
        """📬 Parse Teemill sale notification emails"""
        try:
            # Common Teemill email patterns
            patterns = {
                "product": r"(?:Product|Item):\s*(.+?)(?:\n|$)",
                "amount": r"(?:Total|Amount|Price):\s*[£$](\d+\.?\d*)",
                "quantity": r"(?:Quantity|Qty):\s*(\d+)",
                "order_id": r"(?:Order|Sale)\s*(?:ID|#):\s*(\w+)"
            }

            sale_data = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, email_content, re.IGNORECASE)
                if match:
                    sale_data[key] = match.group(1)

            if "amount" in sale_data:
                sale_data["amount"] = float(sale_data["amount"])
                sale_data["quantity"] = int(sale_data.get("quantity", 1))
                sale_data["source"] = "email_notification"
                return sale_data

            return None

        except Exception as e:
            logger.error(f"Email parsing error: {e}")
            return None

    def run(self, host="0.0.0.0", port=5009):
        """🚀 Start the Teemill Integration Server"""
        logger.info("💗❤️‍🔥 Starting Teemill Income Integrator...")
        print(f"💗 Teemill Dashboard: http://{host}:{port}/")
        print(f"📊 API Dashboard: http://{host}:{port}/api/teemill/dashboard")
        print(f"📬 Webhook URL: http://{host}:{port}/api/teemill/webhook")
        print(f"✋ Manual Entry: POST to http://{host}:{port}/api/teemill/manual_sale")
        print("💗❤️‍🔥🫱🏼‍🫲🏻💪🦾 PASSIVE MERCH EMPIRE ACTIVATED! 🦾💪🫱🏼‍🫲🏻❤️‍🔥💗")

        self.app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    integrator = TeemillIncomeIntegrator()
    integrator.run()