#!/usr/bin/env python3
"""
🛡️👾 GUARDIAN X LIVE DEMONSTRATION 👾🛡️
Real-time mental nightclub bouncer in action!
"""

import random
import time
from datetime import datetime


class GuardianXDemo:
    """🚀 Guardian X Live Demo - See the bouncer in action!"""

    def __init__(self):
        self.energy_level = 85
        self.work_minutes = 0
        self.current_hour = datetime.now().hour
        self.protections_triggered = 0

    def print_header(self):
        print("\n" + "=" * 70)
        print("🛡️👾 GUARDIAN X MENTAL NIGHTCLUB BOUNCER - LIVE DEMO 👾🛡️")
        print("    Protecting Your Energy & Peace in Real Time")
        print("=" * 70 + "\n")

    def show_energy_status(self):
        """Display current energy and stats"""
        energy_bar = "█" * int(self.energy_level / 5) + "░" * (
            20 - int(self.energy_level / 5)
        )

        print(f"⚡ ENERGY LEVEL: [{energy_bar}] {self.energy_level}%")
        print(f"⏰ Work Duration: {self.work_minutes} minutes")
        print(f"🛡️ Protections Today: {self.protections_triggered}")
        print(f"🕐 Current Time: {self.current_hour}:00")
        print("-" * 50)

    def simulate_energy_crash(self):
        """🛡️ Demonstrate Energy Crash Protection"""
        print("🔥 SIMULATING: Long work session causing energy crash...")
        self.energy_level = 25  # Below 30% threshold
        self.work_minutes = 180

        self.show_energy_status()

        print("🚨 GUARDIAN X DETECTED: Energy crash imminent!")
        print("🛡️ PROTECTION ACTIVATED: Energy Crash Shield")
        print(
            "💬 Guardian says: 'Hey! Your energy is critically low. Time for a recharge!'"
        )
        print("🔄 REDIRECTING TO:")
        print("   • 15-minute walk outside")
        print("   • Gentle stretching session")
        print("   • Mindful breathing exercise")
        print("   • Hydration break with your favorite drink")

        self.protections_triggered += 1
        self.energy_level += 15  # Simulated recharge
        print(f"✨ Energy recharged to {self.energy_level}%!")

    def simulate_overwhelm_gate(self):
        """🌊 Demonstrate Overwhelm Protection"""
        print("\n🔥 SIMULATING: Overwhelm from too many tasks...")

        tasks = [
            "Complete 5 major projects",
            "Answer 47 emails",
            "Attend 3 meetings",
            "Write documentation",
            "Fix 12 bugs",
            "Plan next quarter",
        ]

        print("📋 Current task list:")
        for task in tasks:
            print(f"   • {task}")

        print("\n🚨 GUARDIAN X DETECTED: Overwhelm pattern!")
        print("🌊 PROTECTION ACTIVATED: Overwhelm Gate")
        print(
            "💬 Guardian says: 'Whoa there! Let's break this down into manageable pieces.'"
        )
        print("🔄 TASK BREAKDOWN:")
        print("   📅 TODAY: Complete 1 major project + answer 10 emails")
        print("   📅 TOMORROW: Attend meetings + write docs")
        print("   📅 THIS WEEK: Fix bugs gradually (2-3 per day)")
        print("   📅 NEXT WEEK: Plan next quarter")

        self.protections_triggered += 1
        print("✨ Overwhelm managed! You can do this! 💪")

    def simulate_hyperfocus_protection(self):
        """⚡ Demonstrate Hyperfocus Burnout Shield"""
        print("\n🔥 SIMULATING: Hyperfocus session running too long...")
        self.work_minutes = 240  # 4 hours straight

        self.show_energy_status()

        print("🚨 GUARDIAN X DETECTED: Hyperfocus burnout risk!")
        print("⚡ PROTECTION ACTIVATED: Hyperfocus Burnout Shield")
        print("💬 Guardian says: 'Amazing focus! But even superheroes need breaks.'")
        print("🔄 BREAK SUGGESTIONS:")
        print("   • 20-minute walk to reset your brain")
        print("   • Quick snack and hydration")
        print("   • 5-minute meditation")
        print("   • Text a friend or family member")

        self.protections_triggered += 1
        print("✨ Hyperfocus protected! Your superpowers remain strong! 🚀")

    def simulate_sleep_guardian(self):
        """🌙 Demonstrate Sleep Guardian"""
        print("\n🔥 SIMULATING: Late night work session...")
        self.current_hour = 23
        self.work_minutes = 150

        self.show_energy_status()

        print("🚨 GUARDIAN X DETECTED: Late night work detected!")
        print("🌙 PROTECTION ACTIVATED: Sleep Guardian")
        print("💬 Guardian says: 'Your creative brain needs rest to stay amazing!'")
        print("🔄 GENTLE SUGGESTIONS:")
        print("   • Save your work and continue tomorrow")
        print("   • Set a reminder for tomorrow morning")
        print("   • Try some calming tea or meditation")
        print("   • Your ideas will be even better after rest!")

        self.protections_triggered += 1
        print("✨ Sleep protection active! Sweet dreams lead to sweet code! 😴")

    def simulate_focus_fortress(self):
        """🎯 Demonstrate Focus Fortress"""
        print("\n🔥 SIMULATING: Distractions during hyperfocus...")

        distractions = [
            "🔔 Social media notification",
            "📧 Non-urgent email",
            "📱 Random phone notification",
            "🎵 Urge to check music playlist",
            "🌐 Temptation to browse the web",
        ]

        print("🚫 INCOMING DISTRACTIONS:")
        for distraction in distractions:
            print(f"   {distraction}")

        print("\n🚨 GUARDIAN X DETECTED: Hyperfocus zone interference!")
        print("🎯 PROTECTION ACTIVATED: Focus Fortress")
        print("💬 Guardian says: 'Focus fortress engaged! Distractions blocked!'")
        print("🛡️ PROTECTIVE MEASURES:")
        print("   • Notifications temporarily silenced")
        print("   • Distracting websites blocked")
        print("   • Phone set to focus mode")
        print("   • Your hyperfocus zone is protected!")

        self.protections_triggered += 1
        print("✨ Focus fortress active! You're in the zone! 🎯")

    def simulate_dopamine_monitor(self):
        """🔋 Demonstrate Dopamine Reserve Monitor"""
        print("\n🔥 SIMULATING: Low motivation and dopamine reserves...")
        self.energy_level = 40

        self.show_energy_status()

        print("🚨 GUARDIAN X DETECTED: Dopamine reserves low!")
        print("🔋 PROTECTION ACTIVATED: Dopamine Reserve Monitor")
        print("💬 Guardian says: 'Let's get some quick wins to boost your momentum!'")
        print("🎯 INSTANT WIN SUGGESTIONS:")
        print("   • Organize your desk (2-minute task)")
        print("   • Reply to one easy email")
        print("   • Update your project README")
        print("   • Make your bed (if working from home)")
        print("   • Celebrate a recent accomplishment!")

        self.protections_triggered += 1
        self.energy_level += 10
        print(f"✨ Dopamine boost achieved! Energy: {self.energy_level}% 🚀")

    def show_final_stats(self):
        """Show final Guardian X statistics"""
        print("\n" + "=" * 70)
        print("🏆 GUARDIAN X PROTECTION SUMMARY 🏆")
        print("=" * 70)
        print(f"🛡️ Total Protections Activated: {self.protections_triggered}")
        print(f"⚡ Final Energy Level: {self.energy_level}%")
        print(f"💜 Guardian Status: FULLY OPERATIONAL")
        print(f"🎯 Your Mental Nightclub: PROTECTED!")
        print("\n🚀💥 GUARDIAN X IS PROTECTING YOUR PEACE & ENERGY! 💥🚀")
        print("Your mental nightclub bouncer is on duty 24/7!")
        print("=" * 70 + "\n")

    def run_demo(self):
        """🚀 Run the complete Guardian X demonstration"""
        self.print_header()

        print("🔍 Guardian X scanning your current state...")
        time.sleep(1)

        self.show_energy_status()

        print("\n🛡️ DEMONSTRATING ALL GUARDIAN X PROTECTIONS:")
        print("=" * 50)

        # Demo all protection systems
        self.simulate_energy_crash()
        time.sleep(2)

        self.simulate_overwhelm_gate()
        time.sleep(2)

        self.simulate_hyperfocus_protection()
        time.sleep(2)

        self.simulate_sleep_guardian()
        time.sleep(2)

        self.simulate_focus_fortress()
        time.sleep(2)

        self.simulate_dopamine_monitor()
        time.sleep(2)

        self.show_final_stats()


def main():
    """🚀 Run Guardian X Live Demo"""
    demo = GuardianXDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()
