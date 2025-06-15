#!/usr/bin/env python3
"""
📧🚀 HYPERFOCUSZONE ADVANCED EMAIL SEQUENCES 🚀📧
AI-powered email marketing automation for maximum conversions!
"""

import asyncio
import json
import logging
import sqlite3
import smtplib
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import Dict, List, Optional
import requests
import schedule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HyperFocusEmailSequences:
    """📧 Ultimate Email Marketing Automation Engine"""

    def __init__(self):
        self.base_path = "/root/chaosgenius"
        self.email_db = f"{self.base_path}/hyperfocus_email_sequences.db"

        # Email configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = "your-email@gmail.com"  # Configure with your email
        self.email_password = "your-app-password"  # Use app password for Gmail

        # Advanced email templates
        self.email_sequences = self._load_email_sequences()

        print("📧🚀 HYPERFOCUS EMAIL SEQUENCES ONLINE! 🚀📧")
        self.initialize_database()
        self.start_email_scheduler()

    def initialize_database(self):
        """🗄️ Setup email sequences database"""
        conn = sqlite3.connect(self.email_db)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                name TEXT,
                lead_score INTEGER DEFAULT 0,
                package_type TEXT,
                current_sequence TEXT,
                sequence_step INTEGER DEFAULT 0,
                subscribed_at TEXT,
                last_email_sent TEXT,
                opens INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                tags TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id TEXT UNIQUE,
                name TEXT,
                sequence_type TEXT,
                subject_line TEXT,
                email_body TEXT,
                sent_count INTEGER DEFAULT 0,
                open_rate REAL DEFAULT 0.0,
                click_rate REAL DEFAULT 0.0,
                conversion_rate REAL DEFAULT 0.0,
                created_at TEXT,
                last_sent TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_email TEXT,
                campaign_id TEXT,
                action_type TEXT,
                timestamp TEXT,
                data TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_email TEXT,
                sequence_type TEXT,
                step_number INTEGER,
                send_at TEXT,
                status TEXT DEFAULT 'pending',
                subject TEXT,
                body TEXT,
                created_at TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Email database initialized!")

    def _load_email_sequences(self) -> Dict:
        """📝 Load all email sequence templates"""
        return {
            "onboarding": {
                "name": "🎉 Customer Onboarding Sequence",
                "steps": [
                    {
                        "delay_hours": 0,
                        "subject": "🎉 Welcome to HyperFocus Zone! Your AI Empire Awaits",
                        "template": "onboarding_welcome",
                        "cta": "Access Your Dashboard"
                    },
                    {
                        "delay_hours": 24,
                        "subject": "🚀 Quick Start: Get Your First AI Agent Running",
                        "template": "onboarding_quickstart",
                        "cta": "Start Setup Wizard"
                    },
                    {
                        "delay_hours": 72,
                        "subject": "🧠 ADHD Success Story: How Sarah 10x'd Her Business",
                        "template": "onboarding_success_story",
                        "cta": "See More Results"
                    },
                    {
                        "delay_hours": 168,
                        "subject": "💡 Pro Tip: Unlock Your HyperFocus Superpower",
                        "template": "onboarding_pro_tips",
                        "cta": "Optimize Your Setup"
                    }
                ]
            },
            "nurture": {
                "name": "🌱 Lead Nurturing Sequence",
                "steps": [
                    {
                        "delay_hours": 1,
                        "subject": "🎯 Your Personalized AI Automation Assessment",
                        "template": "nurture_assessment",
                        "cta": "Take Assessment"
                    },
                    {
                        "delay_hours": 48,
                        "subject": "💰 Case Study: £50K Revenue Boost in 30 Days",
                        "template": "nurture_case_study",
                        "cta": "See Full Case Study"
                    },
                    {
                        "delay_hours": 120,
                        "subject": "🤖 Demo: Watch AI Agents Transform This Business",
                        "template": "nurture_demo",
                        "cta": "Watch Demo"
                    },
                    {
                        "delay_hours": 240,
                        "subject": "⚡ Limited Time: Enterprise Setup for Starter Price",
                        "template": "nurture_urgency",
                        "cta": "Claim Offer"
                    }
                ]
            },
            "reactivation": {
                "name": "🔄 Customer Reactivation Sequence",
                "steps": [
                    {
                        "delay_hours": 0,
                        "subject": "😢 We Miss You! Here's What You've Been Missing",
                        "template": "reactivation_miss_you",
                        "cta": "Come Back"
                    },
                    {
                        "delay_hours": 48,
                        "subject": "🎁 Exclusive Comeback Offer: 50% Off Enterprise",
                        "template": "reactivation_offer",
                        "cta": "Activate Offer"
                    },
                    {
                        "delay_hours": 168,
                        "subject": "💔 Last Chance: Your AI Empire Is Waiting",
                        "template": "reactivation_final",
                        "cta": "Reactivate Now"
                    }
                ]
            },
            "upsell": {
                "name": "⬆️ Package Upgrade Sequence",
                "steps": [
                    {
                        "delay_hours": 0,
                        "subject": "🚀 Ready for More? Unlock Advanced Features",
                        "template": "upsell_ready",
                        "cta": "Upgrade Now"
                    },
                    {
                        "delay_hours": 72,
                        "subject": "💎 See What Enterprise Customers Are Achieving",
                        "template": "upsell_enterprise_results",
                        "cta": "Join Enterprise"
                    },
                    {
                        "delay_hours": 168,
                        "subject": "⏰ Upgrade Deadline: Lock in Current Pricing",
                        "template": "upsell_deadline",
                        "cta": "Upgrade Before Price Increase"
                    }
                ]
            }
        }

    def get_email_template(self, template_name: str, contact_data: Dict) -> str:
        """📝 Get personalized email template"""
        templates = {
            "onboarding_welcome": f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; }}
        .cta-button {{ background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
        .footer {{ background: #333; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome to HyperFocus Zone, {contact_data.get('name', 'Champion')}!</h1>
            <p>Your AI-Powered Business Empire Starts NOW!</p>
        </div>

        <div class="content">
            <h2>🚀 You Just Unlocked Something LEGENDARY</h2>

            <p>Hey {contact_data.get('name', 'Champion')},</p>

            <p>CONGRATULATIONS! You just joined the most exclusive AI automation empire on the planet. You're now part of a community where ADHD entrepreneurs don't just survive - they absolutely DOMINATE! 🔥</p>

            <h3>🤖 What's Happening Right Now:</h3>
            <ul>
                <li>✅ Your AI agents are spinning up (takes 2-3 minutes)</li>
                <li>✅ Your personal dashboard is being customized</li>
                <li>✅ HyperFocus Zone is calibrating to YOUR brain patterns</li>
                <li>✅ Money-making systems are activating automatically</li>
            </ul>

            <h3>🎯 Your First Mission (Takes 5 Minutes):</h3>
            <p>Click the button below to access your command center and watch the magic happen. I've prepared a quick setup wizard that'll have your first AI agent working within minutes!</p>

            <a href="http://localhost:5000/dashboard" class="cta-button">🚀 Access Your Dashboard</a>

            <h3>💪 Why You Made the PERFECT Choice:</h3>
            <p>Unlike those boring business tools that fight against your ADHD brain, HyperFocus Zone was built BY someone with ADHD FOR ADHD entrepreneurs. Every feature, every automation, every AI agent understands how your mind works.</p>

            <h3>🔥 What's Coming in the Next 24 Hours:</h3>
            <ul>
                <li>🎪 Personal onboarding call (if you want one)</li>
                <li>📊 Your first automated revenue report</li>
                <li>🎯 Custom AI agent recommendations</li>
                <li>💎 Exclusive ADHD entrepreneur community access</li>
            </ul>

            <p><strong>Pro Tip:</strong> Check your dashboard in about 10 minutes. Your agents will have already found 3-5 optimization opportunities in your business! 🤯</p>

            <p>Welcome to the empire, {contact_data.get('name', 'Champion')}! 👑</p>

            <p>Chief Lyndz<br>
            Founder & Head AI Whisperer<br>
            HyperFocus Zone Empire</p>
        </div>

        <div class="footer">
            <p>Questions? Just reply to this email - I read every single one! 💜</p>
            <p>🌟 You're now part of something legendary! 🌟</p>
        </div>
    </div>
</body>
</html>
            """,

            "nurture_assessment": f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; }}
        .assessment-box {{ background: white; border-left: 5px solid #ff6b6b; padding: 20px; margin: 20px 0; }}
        .cta-button {{ background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Your Personalized AI Assessment, {contact_data.get('name', 'Future Empire Builder')}!</h1>
        </div>

        <div class="content">
            <p>Hey {contact_data.get('name', 'Champion')},</p>

            <p>I've been analyzing businesses like yours for 3+ years, and I can spot automation opportunities from a mile away. But here's the thing - every ADHD entrepreneur's business is unique! 🧠</p>

            <div class="assessment-box">
                <h3>🔍 What This Assessment Reveals:</h3>
                <ul>
                    <li>💰 Hidden revenue streams you're missing (usually 3-5 per business)</li>
                    <li>⚡ Time-wasting tasks that can be 100% automated</li>
                    <li>🎯 Your #1 growth bottleneck (and how to eliminate it)</li>
                    <li>🤖 Which AI agents will have the biggest impact for YOU</li>
                    <li>📈 Realistic 90-day revenue projection</li>
                </ul>
            </div>

            <p><strong>Here's what happened to Sarah (ADHD entrepreneur like you):</strong></p>
            <p>Before assessment: Struggling with inconsistent income, overwhelmed by admin work<br>
            After implementing recommendations: £15K/month recurring revenue, works 30% fewer hours</p>

            <p>The assessment takes 3 minutes and the insights are pure GOLD! 🏆</p>

            <a href="http://localhost:5000/assessment" class="cta-button">🎯 Take Your Assessment</a>

            <p>PS: This assessment usually costs £500 as part of my consulting, but it's free for you right now! 💎</p>

            <p>Chief Lyndz</p>
        </div>
    </div>
</body>
</html>
            """,

            "upsell_ready": f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; }}
        .upgrade-box {{ background: white; border: 3px solid #4facfe; padding: 20px; margin: 20px 0; border-radius: 10px; }}
        .cta-button {{ background: #4facfe; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Ready for the Next Level, {contact_data.get('name', 'Empire Builder')}?</h1>
        </div>

        <div class="content">
            <p>Hey {contact_data.get('name', 'Champion')},</p>

            <p>I've been watching your progress and I'm IMPRESSED! 🔥 You're clearly ready for more advanced automation.</p>

            <div class="upgrade-box">
                <h3>🏆 What You Unlock with Enterprise:</h3>
                <ul>
                    <li>🤖 <strong>Unlimited AI Agents</strong> - Deploy as many as you need</li>
                    <li>💰 <strong>Revenue Optimization AI</strong> - Automatically finds money opportunities</li>
                    <li>🧠 <strong>Advanced ADHD Workflows</strong> - Custom-built for your brain patterns</li>
                    <li>⚡ <strong>Priority Processing</strong> - Your agents work 5x faster</li>
                    <li>👑 <strong>VIP Support</strong> - Direct access to me personally</li>
                    <li>🔮 <strong>Predictive Analytics</strong> - See opportunities before they happen</li>
                </ul>
            </div>

            <p><strong>Real Talk:</strong> Enterprise customers typically see 500% ROI within 60 days. The advanced revenue optimization alone pays for the upgrade in the first month! 📈</p>

            <p>Plus, since you're already killing it with the Starter package, I know you'll absolutely dominate with Enterprise features!</p>

            <a href="http://localhost:5000/upgrade/enterprise" class="cta-button">🚀 Upgrade to Enterprise</a>

            <p>Questions? Just reply - I'm here to help you build something legendary! 💜</p>

            <p>Chief Lyndz<br>
            Your AI Success Partner</p>
        </div>
    </div>
</body>
</html>
            """
        }

        return templates.get(template_name, "Template not found")

    def add_contact_to_sequence(self, email: str, name: str, sequence_type: str,
                               package_type: str = None, lead_score: int = 0) -> bool:
        """📧 Add contact to email sequence"""
        try:
            conn = sqlite3.connect(self.email_db)
            cursor = conn.cursor()

            # Check if contact already exists
            cursor.execute("SELECT id FROM email_contacts WHERE email = ?", (email,))
            existing = cursor.fetchone()

            if existing:
                # Update existing contact
                cursor.execute('''
                    UPDATE email_contacts
                    SET current_sequence = ?, sequence_step = 0, lead_score = ?, package_type = ?
                    WHERE email = ?
                ''', (sequence_type, lead_score, package_type, email))
            else:
                # Add new contact
                cursor.execute('''
                    INSERT INTO email_contacts
                    (email, name, lead_score, package_type, current_sequence,
                     sequence_step, subscribed_at, status)
                    VALUES (?, ?, ?, ?, ?, 0, ?, 'active')
                ''', (email, name, lead_score, package_type, sequence_type,
                      datetime.now().isoformat()))

            conn.commit()

            # Schedule first email
            self._schedule_sequence_emails(email, sequence_type)

            conn.close()

            logger.info(f"✅ Added {email} to {sequence_type} sequence")
            return True

        except Exception as e:
            logger.error(f"Error adding contact to sequence: {e}")
            return False

    def _schedule_sequence_emails(self, email: str, sequence_type: str):
        """⏰ Schedule all emails in sequence"""
        try:
            sequence = self.email_sequences.get(sequence_type)
            if not sequence:
                return

            conn = sqlite3.connect(self.email_db)
            cursor = conn.cursor()

            for i, step in enumerate(sequence["steps"]):
                send_at = datetime.now() + timedelta(hours=step["delay_hours"])

                cursor.execute('''
                    INSERT INTO scheduled_emails
                    (contact_email, sequence_type, step_number, send_at,
                     subject, body, created_at, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
                ''', (email, sequence_type, i, send_at.isoformat(),
                      step["subject"], step["template"], datetime.now().isoformat()))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Error scheduling emails: {e}")

    def send_email(self, to_email: str, subject: str, html_body: str) -> bool:
        """📬 Send individual email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = to_email

            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()

            logger.info(f"✅ Email sent to {to_email}: {subject}")
            return True

        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False

    def process_scheduled_emails(self):
        """⚡ Process all pending scheduled emails"""
        try:
            conn = sqlite3.connect(self.email_db)
            cursor = conn.cursor()

            # Get emails ready to send
            cursor.execute('''
                SELECT se.id, se.contact_email, se.subject, se.body, se.sequence_type, se.step_number,
                       ec.name, ec.package_type, ec.lead_score
                FROM scheduled_emails se
                JOIN email_contacts ec ON se.contact_email = ec.email
                WHERE se.status = 'pending' AND se.send_at <= ?
            ''', (datetime.now().isoformat(),))

            emails_to_send = cursor.fetchall()

            for email_data in emails_to_send:
                (email_id, contact_email, subject, template_name, sequence_type,
                 step_number, name, package_type, lead_score) = email_data

                # Get contact data for personalization
                contact_data = {
                    "name": name,
                    "email": contact_email,
                    "package_type": package_type,
                    "lead_score": lead_score
                }

                # Generate personalized email
                html_body = self.get_email_template(template_name, contact_data)

                # Send email
                if self.send_email(contact_email, subject, html_body):
                    # Mark as sent
                    cursor.execute('''
                        UPDATE scheduled_emails SET status = 'sent' WHERE id = ?
                    ''', (email_id,))

                    # Update contact
                    cursor.execute('''
                        UPDATE email_contacts
                        SET sequence_step = ?, last_email_sent = ?
                        WHERE email = ?
                    ''', (step_number + 1, datetime.now().isoformat(), contact_email))

                    # Log analytics
                    cursor.execute('''
                        INSERT INTO email_analytics
                        (contact_email, campaign_id, action_type, timestamp, data)
                        VALUES (?, ?, 'sent', ?, ?)
                    ''', (contact_email, f"{sequence_type}_step_{step_number}",
                          datetime.now().isoformat(), json.dumps({"subject": subject})))

            conn.commit()
            conn.close()

            if emails_to_send:
                logger.info(f"📧 Processed {len(emails_to_send)} scheduled emails")

        except Exception as e:
            logger.error(f"Error processing scheduled emails: {e}")

    def trigger_onboarding_sequence(self, email: str, package_type: str, name: str):
        """🎉 Trigger onboarding sequence for new customer"""
        self.add_contact_to_sequence(email, name, "onboarding", package_type, 100)
        logger.info(f"🎉 Onboarding sequence triggered for {email}")

    def start_email_scheduler(self):
        """⏰ Start the email scheduler"""
        # Schedule email processing every 5 minutes
        schedule.every(5).minutes.do(self.process_scheduled_emails)

        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)

        import threading
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("⏰ Email scheduler started!")

    def get_email_analytics(self) -> Dict:
        """📊 Get comprehensive email analytics"""
        conn = sqlite3.connect(self.email_db)
        cursor = conn.cursor()

        # Overall stats
        cursor.execute("SELECT COUNT(*) FROM email_contacts WHERE status = 'active'")
        total_contacts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scheduled_emails WHERE status = 'sent'")
        total_sent = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(opens), AVG(clicks) FROM email_contacts")
        avg_stats = cursor.fetchone()

        # Sequence performance
        cursor.execute('''
            SELECT current_sequence, COUNT(*), AVG(opens), AVG(clicks)
            FROM email_contacts
            WHERE current_sequence IS NOT NULL
            GROUP BY current_sequence
        ''')
        sequence_performance = cursor.fetchall()

        conn.close()

        return {
            "total_contacts": total_contacts,
            "total_emails_sent": total_sent,
            "average_open_rate": avg_stats[0] or 0,
            "average_click_rate": avg_stats[1] or 0,
            "sequence_performance": sequence_performance,
            "sequences_available": list(self.email_sequences.keys())
        }

# Initialize email sequences
email_sequences = HyperFocusEmailSequences()

if __name__ == "__main__":
    print("📧🚀 HYPERFOCUS EMAIL SEQUENCES READY!")
    print("✅ Advanced email automation active")
    print("✅ Personalized sequences loaded")
    print("✅ Analytics tracking enabled")
    print("✅ Scheduler running")
    print("\n🎯 Ready to convert leads into customers automatically!")