#!/bin/bash

# taz.de Artikel-Index fetchen und aufbereiten

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TMP_HTML="$PROJECT_DIR/tmp_taz.html"
OUTPUT_FILE="$PROJECT_DIR/tmp_taz.txt"
TMP_FILE="$PROJECT_DIR/tmp.html"

echo "Fetching taz.de..."

# Startseite herunterladen
curl -s "https://taz.de/" > "$TMP_FILE"

# HTML bereinigen
python3 "$SCRIPT_DIR/clean_taz.py" "$TMP_FILE" "$TMP_HTML"

# HTML zu kompaktem Text-Format parsen
echo "Parsing articles..."
python3 "$SCRIPT_DIR/parse-taz.py" "$TMP_HTML" "$OUTPUT_FILE"

# Temp-Dateien aufräumen
rm -f "$TMP_FILE" "$TMP_HTML"

echo "Fertig: $OUTPUT_FILE"
