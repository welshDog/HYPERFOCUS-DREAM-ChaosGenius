import os
import argparse
import random
import json
from datetime import datetime
from pathlib import Path

#!/usr/bin/env python3
"""
📖 BROSKI WRITER ULTRA MODE 🧠🚀
Turns chaos into chapters. Auto-dOoK builder powered by raw memories and broski tone.

Usage:
  python broski_writer.py --input ./my-folder --output ./dook/chapters/
"""


# 🔍 Step 1: Scraper Agent
def scrape_files(folder):
    allowed = [".txt", ".md", ".mp3", ".mp4", ".docx", ".png", ".jpg"]
    memory_bank = []
    for root, _, files in os.walk(folder):
        for f in files:
            if any(f.endswith(ext) for ext in allowed):
                memory_bank.append(os.path.join(root, f))
    return memory_bank

# 🎯 Step 2: Generate Chapter Info
def generate_chapter_title(path):
    name = Path(path).stem.replace("_", " ").replace("-", " ").title()
    return f"The Tale of {name}" if len(name) < 40 else name[:40]

def broski_tags():
    tags = ["hyperfocus", "burnout", "victory", "idea", "realisation", "dopamine-surge"]
    xp = random.randint(20, 100)
    loot = random.choice(["🪛 Wrench of Wisdom", "🧠 Focus Chip", "📖 Memory Scroll", "💎 NeuroGem"])
    return {
        "tags": random.sample(tags, 2),
        "xp": xp,
        "loot": loot
    }

# ✍️ Step 3: Make Chapter Folder + Files
def create_chapter(path, out_dir):
    title = generate_chapter_title(path)
    slug = title.lower().replace(" ", "-")
    # Clean slug of special characters
    slug = "".join(c for c in slug if c.isalnum() or c == "-")[:40]
    chapter_path = os.path.join(out_dir, slug)
    os.makedirs(chapter_path, exist_ok=True)

    story_md = os.path.join(chapter_path, "story.md")
    readme_md = os.path.join(chapter_path, "README.md")
    meta_json = os.path.join(chapter_path, "tags.json")

    tags = broski_tags()

    with open(story_md, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n🚧 Raw Source: `{path}`\n\n🧠 Story loading…\n")

    with open(readme_md, "w", encoding="utf-8") as f:
        f.write("""# Ultra Magic Notes
BROski, please help enhance this story with:
- [x] Spelling fix
- [x] Flow boost
- [ ] Add intro or title if missing
- [ ] Optional AI-generated artwork
""")

    with open(meta_json, "w", encoding="utf-8") as f:
        json.dump(tags, f, indent=2)

    return title

# 🚀 Launch System
def main():
    parser = argparse.ArgumentParser(description="BROSKI WRITER ULTRA")
    parser.add_argument("--input", required=True, help="Folder with memories")
    parser.add_argument("--output", required=True, help="Where to save dOoK chapters")
    args = parser.parse_args()

    print(f"📂 Scanning: {args.input}")
    paths = scrape_files(args.input)

    print(f"🌀 Found {len(paths)} items. Creating chapters…")
    os.makedirs(args.output, exist_ok=True)

    for p in paths:
        chapter_title = create_chapter(p, args.output)
        print(f"✅ Chapter created: {chapter_title}")

    print("\n🎉 dOoK Mission Complete, BROSKI!")
    print(f"💾 Chapters saved to: {args.output}")
    print("🧠💜 Keep building your legacy!")

if __name__ == "__main__":
    main()