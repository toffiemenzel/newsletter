#!/bin/bash

# Berliner Zeitung Artikel-Index fetchen und aufbereiten

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TMP_HTML="$PROJECT_DIR/tmp_berliner-zeitung.html"
OUTPUT_FILE="$PROJECT_DIR/tmp_berliner-zeitung.txt"
TMP_FILE="$PROJECT_DIR/tmp.html"

echo "Fetching berliner-zeitung.de..."

# Startseite herunterladen
curl -s "https://www.berliner-zeitung.de/" > "$TMP_FILE"

# HTML bereinigen
python3 "$SCRIPT_DIR/clean_berliner-zeitung.py" "$TMP_FILE" "$TMP_HTML"

# HTML zu kompaktem Text-Format parsen
echo "Parsing articles..."
python3 "$SCRIPT_DIR/parse-berliner-zeitung.py" "$TMP_HTML" "$OUTPUT_FILE"

# Temp-Dateien aufräumen
rm -f "$TMP_FILE" "$TMP_HTML"

echo "Fertig: $OUTPUT_FILE"
