#!/bin/bash
#
# Newsletter Generator - Multi-Profile
# Iterates over all profiles and creates newsletters
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATE_YYMMDD=$(date +%y%m%d)
DATE_LOG=$(date +%Y-%m-%d)

cd "$PROJECT_DIR"

# Find all profiles (ignore _example)
PROFILES=$(ls -d profiles/*/ 2>/dev/null | grep -v "_example" | xargs -n1 basename 2>/dev/null || true)

if [ -z "$PROFILES" ]; then
    echo "Error: No profiles found."
    echo "Please create a profile with:"
    echo "  cp -r profiles/_example profiles/yourname"
    echo "  Edit profiles/yourname/interests.md and sources.md"
    exit 1
fi

echo "=== Newsletter Generation - $DATE_LOG ==="
echo "Profiles found: $PROFILES"
echo ""

for PROFILE in $PROFILES; do
    echo "=== Processing: $PROFILE ==="

    mkdir -p "profiles/$PROFILE/output"

    LOG_FILE="profiles/$PROFILE/output/${DATE_YYMMDD}_newsletter.log"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting newsletter generation for $PROFILE" >> "$LOG_FILE"

    PROMPT=$(cat commands/create-newsletter.md | sed "s/{{PROFILE_NAME}}/$PROFILE/g" | sed "s/{{DATE}}/$DATE_YYMMDD/g")
    claude --dangerously-skip-permissions -p "$PROMPT" 2>&1 | tee -a "$LOG_FILE"

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Newsletter generation completed for $PROFILE" >> "$LOG_FILE"
    echo ""
done

echo "=== All newsletters created ==="
