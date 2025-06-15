#!/usr/bin/env python3
"""
🧠 Natural Language Commander Test Script
Quick demo of the NL command processing capabilities
"""
import os
import sys

sys.path.append("/root/chaosgenius")

from broski_natural_language_commander import NaturalLanguageCommander


def test_nl_commands():
    """Test various natural language commands"""
    print("🚀 Testing Natural Language Commander!")
    print("=" * 50)

    commander = NaturalLanguageCommander()

    # Test commands
    test_commands = [
        "Deploy 3 money bots and run the NFT campaign",
        "Start security monitoring with high priority",
        "Launch 5 data miners and activate stealth mode",
        "Deploy trading bots and monitor performance",
        "Activate drone army with reconnaissance protocol",
        "Start income generation with automated trading",
    ]

    for cmd in test_commands:
        print(f"\n🧠 Testing: '{cmd}'")
        result = commander.parse_command(cmd)
        print(f"📊 Result: {result}")
        print("-" * 40)


if __name__ == "__main__":
    test_nl_commands()
