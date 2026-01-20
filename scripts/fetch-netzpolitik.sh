#!/bin/bash

# netzpolitik.org Artikel-Index fetchen und aufbereiten

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TMP_HTML="$PROJECT_DIR/tmp_netzpolitik.html"
OUTPUT_FILE="$PROJECT_DIR/tmp_netzpolitik.txt"
TMP_FILE="$PROJECT_DIR/tmp.html"

echo "Fetching netzpolitik.org..."

# Startseite herunterladen
curl -s "https://netzpolitik.org/" > "$TMP_FILE"

# HTML bereinigen
python3 "$SCRIPT_DIR/clean_netzpolitik.py" "$TMP_FILE" "$TMP_HTML"

# HTML zu kompaktem Text-Format parsen
echo "Parsing articles..."
python3 "$SCRIPT_DIR/parse-netzpolitik.py" "$TMP_HTML" "$OUTPUT_FILE"

# Temp-Dateien aufräumen
rm -f "$TMP_FILE" "$TMP_HTML"

echo "Fertig: $OUTPUT_FILE"
