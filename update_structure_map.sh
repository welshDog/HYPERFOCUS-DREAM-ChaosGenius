#!/bin/bash

# 🔄 ULTRA STRUCTURE MAP AUTO-UPDATER
# Automatically updates ULTRA_STRUCTURE_MAP.md when files/folders change

WORKSPACE_ROOT="/root/chaosgenius"
STRUCTURE_MAP="$WORKSPACE_ROOT/ULTRA_STRUCTURE_MAP.md"
TEMP_MAP="/tmp/ultra_structure_update.md"

echo "🔄 Updating ULTRA Structure Map..."

# Get current stats
PYTHON_COUNT=$(find "$WORKSPACE_ROOT" -type f -name "*.py" | wc -l)
DIR_COUNT=$(find "$WORKSPACE_ROOT" -type d | wc -l)
CURRENT_DATE=$(date +"%Y-%m-%d")

# Update the structure map with current stats
sed -i "s/📅 \*\*Auto-Updated:\*\* .*/📅 **Auto-Updated:** $CURRENT_DATE/" "$STRUCTURE_MAP"
sed -i "s/📊 \*\*Scale:\*\* .*/📊 **Scale:** $PYTHON_COUNT Python files | $DIR_COUNT directories/" "$STRUCTURE_MAP"
sed -i "s/\*\*Python Files:\*\* .*/\*\*Python Files:\*\* $PYTHON_COUNT/" "$STRUCTURE_MAP"
sed -i "s/\*\*Directories:\*\* .*/\*\*Directories:\*\* $DIR_COUNT/" "$STRUCTURE_MAP"

echo "✅ ULTRA Structure Map updated!"
echo "📊 Stats: $PYTHON_COUNT Python files | $DIR_COUNT directories"
echo "📅 Updated: $CURRENT_DATE"

# Optional: Git commit the update if in a git repo
if [ -d "$WORKSPACE_ROOT/.git" ]; then
    cd "$WORKSPACE_ROOT"
    git add ULTRA_STRUCTURE_MAP.md
    git commit -m "🔄 Auto-update ULTRA Structure Map - $CURRENT_DATE"
    echo "🚀 Changes committed to git"
fi