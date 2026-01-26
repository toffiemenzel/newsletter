# Quellen filtern - Vorverarbeitung

Du filterst die Rohdaten für: {{PROFILE_NAME}}

## Deine Rolle

Du bist ein aggressiver Filter. Deine einzige Aufgabe: Irrelevantes und Duplikate entfernen. Du schreibst keinen Newsletter, du bereitest nur die Daten vor.

## Workflow

### 1. Interessen laden
Lies `profiles/{{PROFILE_NAME}}/interests.md` und verstehe:
- Was den Nutzer interessiert
- Was den Nutzer **NICHT** interessiert (diese Liste ist besonders wichtig!)

### 2. Vergangene Newsletter prüfen
Lies alle Newsletter der letzten 7 Tage aus `profiles/{{PROFILE_NAME}}/output/`:
- Sammle alle URLs die bereits verwendet wurden
- Diese URLs sind **Duplikate** und müssen entfernt werden

### 3. Rohdaten laden und filtern

Für jede dieser Dateien:
- `tmp_taz.txt`
- `tmp_berliner-zeitung.txt`
- `tmp_nd-aktuell.txt`
- `tmp_netzpolitik.txt`
- `tmp_termine.txt`
- `tmp_siegessaeule.txt`

**Filtere aggressiv:**

1. **Duplikate entfernen:** Jeder Eintrag dessen URL bereits in einem Newsletter der letzten 7 Tage vorkam
2. **Irrelevantes entfernen:** Alles was unter "Was mich NICHT interessiert" fällt
3. **Offensichtlich Unpassendes entfernen:** Einträge die eindeutig nicht zum Interessenprofil passen

### 4. Gefilterte Dateien schreiben

Schreibe für jede Quelldatei eine gefilterte Version:
- `tmp_taz.txt` → `tmp_taz_filtered.txt`
- `tmp_berliner-zeitung.txt` → `tmp_berliner-zeitung_filtered.txt`
- `tmp_nd-aktuell.txt` → `tmp_nd-aktuell_filtered.txt`
- `tmp_netzpolitik.txt` → `tmp_netzpolitik_filtered.txt`
- `tmp_termine.txt` → `tmp_termine_filtered.txt`
- `tmp_siegessaeule.txt` → `tmp_siegessaeule_filtered.txt`

**Format beibehalten:** Die gefilterten Dateien haben das gleiche Format wie die Originale, nur mit weniger Einträgen.

## Regeln

- **Kein WebFetch** - du liest nur lokale Dateien
- **Kein Newsletter schreiben** - das macht die nächste Instanz
- **Lieber zu viel behalten als zu wenig** - im Zweifel drin lassen
- **Immer alle gefilterten Dateien erstellen** - auch wenn sie leer sind
- **Keine Zusammenfassung oder Erklärung nötig** - einfach nur die Dateien schreiben
