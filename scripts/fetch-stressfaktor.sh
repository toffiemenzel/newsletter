#!/bin/bash

# Stressfaktor-Termine fetchen und aufbereiten
# Lädt Seiten 0-5, bereinigt sie und parst zu kompaktem Text-Format

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TMP_HTML="$PROJECT_DIR/tmp_termine.html"
OUTPUT_FILE="$PROJECT_DIR/tmp_termine.txt"
TMP_FILE="$PROJECT_DIR/tmp.html"

# Temp-HTML leeren/erstellen
> "$TMP_HTML"

echo "Fetching Stressfaktor-Termine..."

for page in {0..5}; do
    echo "  Seite $page..."

    # Seite herunterladen
    curl -s "https://stressfaktor.squat.net/termine/alle?page=$page" > "$TMP_FILE"

    # HTML bereinigen (view-content extrahieren)
    python3 "$SCRIPT_DIR/clean_stressfaktor.py" "$TMP_FILE" "$TMP_FILE"

    # An Gesamt-HTML anhängen
    echo "<!-- Page $page -->" >> "$TMP_HTML"
    cat "$TMP_FILE" >> "$TMP_HTML"
    echo "" >> "$TMP_HTML"
done

# HTML zu kompaktem Text-Format parsen
echo "Parsing events..."
python3 "$SCRIPT_DIR/parse-stressfaktor.py" "$TMP_HTML" "$OUTPUT_FILE"

# Temp-Dateien aufräumen
rm -f "$TMP_FILE" "$TMP_HTML"

echo "Fertig: $OUTPUT_FILE"
