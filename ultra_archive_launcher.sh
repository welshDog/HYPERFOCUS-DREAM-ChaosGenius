#!/bin/bash
"""
🚀💾 ULTRA ARCHIVE BUILDER AGENT - LAUNCH SCRIPT 💾🚀
🌌 Quick Launch Commands for the Master Archive System 🌌
👑 By Command of Chief Lyndz - LEGENDARY FILE MASTERY! 👑
"""

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================================================================${NC}"
echo -e "${YELLOW}💾🧬 ULTRA ARCHIVE BUILDER AGENT - LAUNCH COMMAND CENTER 🧬💾${NC}"
echo -e "${MAGENTA}🌌 Master Core System for Intelligent Archiving & Compression 🌌${NC}"
echo -e "${GREEN}👑 By Command of Chief Lyndz - LEGENDARY FILE MASTERY! 👑${NC}"
echo -e "${CYAN}================================================================================${NC}"

SCRIPT_DIR="/root/chaosgenius"
ARCHIVE_AGENT="$SCRIPT_DIR/ultra_archive_builder_agent.py"

# Function to show usage
show_usage() {
    echo -e "\n${WHITE}🎯 ULTRA ARCHIVE BUILDER COMMANDS:${NC}"
    echo -e "${GREEN}📦 CREATE ARCHIVE:${NC}"
    echo -e "  $0 create <path> [preset] [tags...]"
    echo -e "  Presets: FAST_BACKUP, LEGENDARY_ARCHIVE, SECRET_ULTRA_LOCK, HYPERFOCUS_MODE"
    echo -e "\n${GREEN}📦 RESTORE ARCHIVE:${NC}"
    echo -e "  $0 restore <archive_id> [output_path] [version]"
    echo -e "\n${GREEN}🤖 AUTO-SHRINK:${NC}"
    echo -e "  $0 auto-shrink <directory>"
    echo -e "\n${GREEN}📋 BATCH OPERATIONS:${NC}"
    echo -e "  $0 batch <job_name> <file1> <file2> ... [preset]"
    echo -e "\n${GREEN}🔍 SEARCH ARCHIVES:${NC}"
    echo -e "  $0 search <query> [tag_filter]"
    echo -e "\n${GREEN}📊 STATS & DASHBOARD:${NC}"
    echo -e "  $0 stats       - Show archive statistics"
    echo -e "  $0 dashboard   - Show comprehensive dashboard"
    echo -e "\n${YELLOW}💡 EXAMPLES:${NC}"
    echo -e "  $0 create /path/to/file.py LEGENDARY_ARCHIVE"
    echo -e "  $0 auto-shrink /tmp"
    echo -e "  $0 restore abc123def456"
    echo -e "  $0 search python #code"
}

# Check if no arguments provided
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

COMMAND=$1
shift

case $COMMAND in
    "create")
        if [ $# -lt 1 ]; then
            echo -e "${RED}❌ Error: Target path required for archive creation${NC}"
            echo -e "${YELLOW}Usage: $0 create <path> [preset] [tags...]${NC}"
            exit 1
        fi

        TARGET_PATH=$1
        PRESET=${2:-"LEGENDARY_ARCHIVE"}
        shift 2
        TAGS=("$@")

        echo -e "${CYAN}🚀 Creating archive for: ${WHITE}$TARGET_PATH${NC}"
        echo -e "${YELLOW}📊 Using preset: ${WHITE}$PRESET${NC}"

        if [ ${#TAGS[@]} -gt 0 ]; then
            echo -e "${MAGENTA}🏷️ Custom tags: ${WHITE}${TAGS[*]}${NC}"
            python3 "$ARCHIVE_AGENT" create "$TARGET_PATH" -p "$PRESET" -t "${TAGS[@]}"
        else
            python3 "$ARCHIVE_AGENT" create "$TARGET_PATH" -p "$PRESET"
        fi
        ;;

    "restore")
        if [ $# -lt 1 ]; then
            echo -e "${RED}❌ Error: Archive ID required for restore${NC}"
            echo -e "${YELLOW}Usage: $0 restore <archive_id> [output_path] [version]${NC}"
            exit 1
        fi

        ARCHIVE_ID=$1
        OUTPUT_PATH=$2
        VERSION=$3

        echo -e "${CYAN}📦 Restoring archive: ${WHITE}$ARCHIVE_ID${NC}"

        if [ -n "$OUTPUT_PATH" ] && [ -n "$VERSION" ]; then
            python3 "$ARCHIVE_AGENT" restore "$ARCHIVE_ID" -o "$OUTPUT_PATH" -v "$VERSION"
        elif [ -n "$OUTPUT_PATH" ]; then
            python3 "$ARCHIVE_AGENT" restore "$ARCHIVE_ID" -o "$OUTPUT_PATH"
        elif [ -n "$VERSION" ]; then
            python3 "$ARCHIVE_AGENT" restore "$ARCHIVE_ID" -v "$VERSION"
        else
            python3 "$ARCHIVE_AGENT" restore "$ARCHIVE_ID"
        fi
        ;;

    "auto-shrink")
        if [ $# -lt 1 ]; then
            echo -e "${RED}❌ Error: Directory path required for auto-shrink${NC}"
            echo -e "${YELLOW}Usage: $0 auto-shrink <directory>${NC}"
            exit 1
        fi

        DIRECTORY=$1

        echo -e "${CYAN}🤖 Auto-shrinking directory: ${WHITE}$DIRECTORY${NC}"
        python3 "$ARCHIVE_AGENT" auto-shrink "$DIRECTORY"
        ;;

    "batch")
        if [ $# -lt 2 ]; then
            echo -e "${RED}❌ Error: Job name and at least one file required${NC}"
            echo -e "${YELLOW}Usage: $0 batch <job_name> <file1> <file2> ... [preset]${NC}"
            exit 1
        fi

        JOB_NAME=$1
        shift

        # Check if last argument is a preset
        LAST_ARG="${@: -1}"
        if [[ "$LAST_ARG" =~ ^(FAST_BACKUP|LEGENDARY_ARCHIVE|SECRET_ULTRA_LOCK|HYPERFOCUS_MODE)$ ]]; then
            PRESET="$LAST_ARG"
            # Remove last argument from files list
            set -- "${@:1:$(($#-1))}"
        else
            PRESET="LEGENDARY_ARCHIVE"
        fi

        FILES=("$@")

        echo -e "${CYAN}📋 Creating batch job: ${WHITE}$JOB_NAME${NC}"
        echo -e "${YELLOW}📊 Files to process: ${WHITE}${#FILES[@]}${NC}"
        echo -e "${MAGENTA}🎯 Preset: ${WHITE}$PRESET${NC}"

        # Create temporary file list
        TEMP_FILE="/tmp/archive_batch_$$"
        printf '%s\n' "${FILES[@]}" > "$TEMP_FILE"

        # Execute batch job (this would need additional implementation)
        echo -e "${GREEN}🔥 Batch processing started...${NC}"
        for file in "${FILES[@]}"; do
            echo -e "${BLUE}Processing: ${WHITE}$file${NC}"
            python3 "$ARCHIVE_AGENT" create "$file" -p "$PRESET" -t "#batch_$JOB_NAME"
        done

        rm -f "$TEMP_FILE"
        echo -e "${GREEN}✅ Batch job completed!${NC}"
        ;;

    "search")
        if [ $# -lt 1 ]; then
            echo -e "${RED}❌ Error: Search query required${NC}"
            echo -e "${YELLOW}Usage: $0 search <query> [tag_filter]${NC}"
            exit 1
        fi

        QUERY=$1
        TAG_FILTER=$2

        echo -e "${CYAN}🔍 Searching archives for: ${WHITE}$QUERY${NC}"

        if [ -n "$TAG_FILTER" ]; then
            echo -e "${YELLOW}🏷️ Filtering by tag: ${WHITE}$TAG_FILTER${NC}"
            python3 "$ARCHIVE_AGENT" search -q "$QUERY" --tag-filter "$TAG_FILTER"
        else
            python3 "$ARCHIVE_AGENT" search -q "$QUERY"
        fi
        ;;

    "stats")
        echo -e "${CYAN}📊 Displaying archive statistics...${NC}"
        python3 "$ARCHIVE_AGENT" stats
        ;;

    "dashboard")
        echo -e "${CYAN}📊 Loading Ultra Archive Builder dashboard...${NC}"
        python3 "$ARCHIVE_AGENT" dashboard
        ;;

    "help"|"-h"|"--help")
        show_usage
        ;;

    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        show_usage
        exit 1
        ;;
esac

echo -e "\n${GREEN}🎉 Ultra Archive Builder operation complete!${NC}"