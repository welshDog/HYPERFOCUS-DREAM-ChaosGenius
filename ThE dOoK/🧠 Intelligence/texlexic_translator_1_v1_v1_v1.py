#!/usr/bin/env python3
"""
🧬🔤 TeXlEXic™ TRANSLATOR ULTRA MODE 🔤🧬
Dyslexic-friendly text transformation system
By Command of Chief Lyndz - Read With Vibe. Feel With FIRE.
"""

class TexlexicTranslator:
    def __init__(self):
        self.translation_map = {
            'A': '@', 'B': '8', 'C': '(', 'D': ')', 'E': '3',
            'F': '=', 'G': '6', 'H': '#', 'I': '!', 'J': '_',
            'K': '<', 'L': '_', 'M': '//', 'N': '|', 'O': '0',
            'P': '>', 'Q': '0_', 'R': '2', 'S': '$', 'T': '7',
            'U': '_', 'V': '/', 'W': '//', 'X': '><', 'Y': '¥', 'Z': '2'
        }

    def to_texlexic(self, text):
        """Convert regular text to TeXlEXic™"""
        result = ""
        for char in text.upper():
            if char in self.translation_map:
                result += self.translation_map[char]
            else:
                result += char.lower()
        return result

    def demo(self):
        """Demo the TeXlEXic™ system"""
        original = "We write our truth in our own way. This is the dOoK."
        converted = self.to_texlexic(original)

        print("🧬🔤 TeXlEXic™ TRANSLATOR DEMO 🔤🧬")
        print("=" * 50)
        print(f"Original:  {original}")
        print(f"TeXlEXic:  {converted}")
        print("=" * 50)
        print("🎨 Read With Vibe. Feel With FIRE! 🔥")

if __name__ == "__main__":
    translator = TexlexicTranslator()
    translator.demo()
