#!/bin/bash
#
# Newsletter Generator - Multi-Profile (Two-Step Process)
# 1. Fetch all sources (parallel)
# 2. Filter sources (Claude instance 1)
# 3. Create newsletter (Claude instance 2)
#

set -e

# Ensure PATH includes common locations for npm global binaries
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

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

# Step 1: Fetch all sources (parallel)
echo "=== Step 1: Fetching sources (parallel) ==="
bash scripts/fetch-taz.sh &
bash scripts/fetch-berliner-zeitung.sh &
bash scripts/fetch-nd-aktuell.sh &
bash scripts/fetch-netzpolitik.sh &
bash scripts/fetch-stressfaktor.sh &
bash scripts/fetch-siegessaeule.sh &
wait
echo "=== Fetching complete ==="
echo ""

for PROFILE in $PROFILES; do
    echo "=== Processing: $PROFILE ==="

    mkdir -p "profiles/$PROFILE/output"

    LOG_FILE="profiles/$PROFILE/output/${DATE_YYMMDD}_newsletter.log"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting newsletter generation for $PROFILE" >> "$LOG_FILE"

    # Step 2: Filter sources (Claude instance 1)
    echo "--- Step 2: Filtering sources ---"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting filter step" >> "$LOG_FILE"
    FILTER_PROMPT=$(cat commands/filter-sources.md | sed "s/{{PROFILE_NAME}}/$PROFILE/g")
    claude --dangerously-skip-permissions -p "$FILTER_PROMPT" 2>&1 | tee -a "$LOG_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Filter step completed" >> "$LOG_FILE"

    # Step 3: Create newsletter (Claude instance 2)
    echo "--- Step 3: Creating newsletter ---"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting newsletter creation" >> "$LOG_FILE"
    CREATE_PROMPT=$(cat commands/create-newsletter.md | sed "s/{{PROFILE_NAME}}/$PROFILE/g" | sed "s/{{DATE}}/$DATE_YYMMDD/g")
    claude --dangerously-skip-permissions -p "$CREATE_PROMPT" 2>&1 | tee -a "$LOG_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Newsletter creation completed" >> "$LOG_FILE"

    # Step 4: Cleanup filtered files
    echo "--- Step 4: Cleanup ---"
    rm -f tmp_*_filtered.txt
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleanup completed for $PROFILE" >> "$LOG_FILE"
    echo ""
done

echo "=== All newsletters created ==="
