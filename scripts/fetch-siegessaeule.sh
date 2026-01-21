#!/bin/bash

# Siegessäule-Termine fetchen und aufbereiten
# Lädt Events für die nächsten Tage und parst zu kompaktem Text-Format

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TMP_HTML="$PROJECT_DIR/tmp_siegessaeule.html"
OUTPUT_FILE="$PROJECT_DIR/tmp_siegessaeule.txt"
TMP_FILE="$PROJECT_DIR/tmp.html"

# Gesamt-HTML leeren/erstellen
> "$TMP_HTML"

echo "Fetching Siegessäule-Termine für die nächsten Tage..."

for day_offset in {0..6}; do
    # Datum berechnen (heute + offset)
    TARGET_DATE=$(date -d "+$day_offset days" +%Y-%m-%d)

    echo "  $TARGET_DATE..."

    # Seite herunterladen
    curl -s "https://www.siegessaeule.de/termine/?date=$TARGET_DATE" > "$TMP_FILE"

    # HTML bereinigen
    python3 "$SCRIPT_DIR/clean_siegessaeule.py" "$TMP_FILE" "$TMP_FILE"

    # An Gesamt-HTML anhängen
    echo "<!-- $TARGET_DATE -->" >> "$TMP_HTML"
    cat "$TMP_FILE" >> "$TMP_HTML"
    echo "" >> "$TMP_HTML"
done

# HTML zu kompaktem Text-Format parsen
echo "Parsing events..."
python3 "$SCRIPT_DIR/parse-siegessaeule.py" "$TMP_HTML" "$OUTPUT_FILE"

# Temp-Dateien aufräumen
rm -f "$TMP_FILE" "$TMP_HTML"

echo "Fertig: $OUTPUT_FILE"
