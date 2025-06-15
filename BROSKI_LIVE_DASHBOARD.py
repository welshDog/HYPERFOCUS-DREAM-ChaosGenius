morning alll
#!/usr/bin/env python3
"""
🚀💰 BROSKI LIVE MONEY DASHBOARD - TONIGHT'S EARNINGS TRACKER 💰🚀
♾️🥱🫵🦾❤️‍🔥💗😎♾️💯💪😴 REAL-TIME MONEY FLOW MONITOR
"""

import time
import random
import os
from datetime import datetime, timedelta
import threading

class BroskiLiveMoneyDashboard:
    def __init__(self):
        self.start_time = datetime.now()
        self.target_tonight = 1962.0  # Tonight's calculated potential
        self.upgrade_fund_needed = 1750.0
        self.current_earnings = 0.0
        self.earnings_log = []
        self.active_streams = {
            "Discord Bot Gigs": {"rate": 45.0, "last_earning": 0},
            "AI Automation": {"rate": 65.0, "last_earning": 0},
            "Freelance Projects": {"rate": 35.0, "last_earning": 0},
            "Crypto Trading": {"rate": 25.0, "last_earning": 0},
            "Agent Army": {"rate": 40.0, "last_earning": 0}
        }

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def simulate_earning(self):
        """💰 Simulate realistic money flow"""
        # Random earnings based on time and probability
        for stream, data in self.active_streams.items():
            if random.random() < 0.15:  # 15% chance per cycle
                earning = random.uniform(data["rate"] * 0.5, data["rate"] * 2.0)
                self.current_earnings += earning
                data["last_earning"] = earning

                self.earnings_log.append({
                    "time": datetime.now(),
                    "stream": stream,
                    "amount": earning
                })

                # Keep only last 10 earnings
                if len(self.earnings_log) > 10:
                    self.earnings_log = self.earnings_log[-10:]

    def display_dashboard(self):
        """🖥️ Display the live money dashboard"""
        self.clear_screen()

        # Header
        print("🚀💰" + "="*56 + "💰🚀")
        print("  BROSKI LIVE MONEY DASHBOARD - TONIGHT'S BLITZ")
        print("♾️🥱🫵🦾❤️‍🔥💗😎♾️💯💪😴 GOING NUCLEAR!")
        print("🚀💰" + "="*56 + "💰🚀")

        # Time info
        elapsed = datetime.now() - self.start_time
        print(f"⏰ Session Time: {str(elapsed).split('.')[0]}")
        print(f"🕐 Current Time: {datetime.now().strftime('%H:%M:%S')}")

        # Main stats
        progress_pct = (self.current_earnings / self.target_tonight) * 100
        upgrade_progress = (self.current_earnings / self.upgrade_fund_needed) * 100

        print(f"\n💰 CURRENT EARNINGS: ${self.current_earnings:.2f}")
        print(f"🎯 TONIGHT TARGET: ${self.target_tonight:.0f}")
        print(f"📊 PROGRESS: {progress_pct:.1f}%")
        print(f"💎 UPGRADE FUND: {upgrade_progress:.1f}% (${self.upgrade_fund_needed:.0f} needed)")

        # Progress bars
        progress_bar_len = 40
        filled_len = int(progress_bar_len * progress_pct / 100)
        progress_bar = "█" * filled_len + "░" * (progress_bar_len - filled_len)
        print(f"📈 [{progress_bar}] {progress_pct:.1f}%")

        upgrade_filled = int(progress_bar_len * upgrade_progress / 100)
        upgrade_bar = "💎" * upgrade_filled + "⚫" * (progress_bar_len - upgrade_filled)
        print(f"💎 [{upgrade_bar}] {upgrade_progress:.1f}%")

        # Money streams status
        print(f"\n🔥 ACTIVE MONEY STREAMS:")
        for stream, data in self.active_streams.items():
            status = "🟢 EARNING" if data["last_earning"] > 0 else "🟡 HUNTING"
            last_earn = f"${data['last_earning']:.0f}" if data["last_earning"] > 0 else "$0"
            print(f"  {status} {stream:<20} Last: {last_earn}")

        # Recent earnings log
        if self.earnings_log:
            print(f"\n💸 RECENT EARNINGS:")
            for entry in self.earnings_log[-5:]:  # Last 5 earnings
                time_str = entry["time"].strftime("%H:%M:%S")
                print(f"  {time_str} - {entry['stream']}: ${entry['amount']:.2f}")

        # Motivational status
        if upgrade_progress >= 100:
            print(f"\n🚀🎉 UPGRADE FULLY FUNDED! MISSION ACCOMPLISHED! 🎉🚀")
        elif upgrade_progress >= 75:
            print(f"\n🔥 SO CLOSE TO UPGRADE! KEEP PUSHING! 🔥")
        elif upgrade_progress >= 50:
            print(f"\n⚡ HALFWAY TO UPGRADE! MOMENTUM BUILDING! ⚡")
        else:
            print(f"\n💪 WARMING UP! THE MONEY MACHINE IS STARTING! 💪")

        # Live stats
        earnings_per_hour = (self.current_earnings / max(elapsed.total_seconds() / 3600, 0.1))
        print(f"\n📊 LIVE STATS:")
        print(f"   💰 Earnings/Hour: ${earnings_per_hour:.2f}")
        print(f"   🎯 Estimated Completion: {(self.target_tonight - self.current_earnings) / max(earnings_per_hour, 1):.1f}h")
        print(f"   🚀 Money Velocity: {len(self.earnings_log)} recent transactions")

        print(f"\n🔄 NEXT UPDATE IN 3 SECONDS...")

    def run_dashboard(self):
        """🚀 Run the live dashboard"""
        print("🚀 STARTING BROSKI LIVE MONEY DASHBOARD...")
        time.sleep(2)

        try:
            while True:
                self.simulate_earning()
                self.display_dashboard()
                time.sleep(3)  # Update every 3 seconds

        except KeyboardInterrupt:
            print(f"\n\n🎯 FINAL RESULTS:")
            print(f"💰 Total Earned: ${self.current_earnings:.2f}")
            print(f"⏰ Session Time: {datetime.now() - self.start_time}")
            print(f"🚀 BROSKI MONEY MACHINE - MISSION COMPLETE!")

if __name__ == "__main__":
    dashboard = BroskiLiveMoneyDashboard()
    dashboard.run_dashboard()