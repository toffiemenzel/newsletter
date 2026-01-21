# Interessen-Profil verfeinern

Du analysierst die Onboarding-Daten eines Users, um sein Interessen-Profil zu verfeinern.

**Profil:** $ARGUMENTS

---

## Phase 1: Daten sammeln

Lies zuerst folgende Dateien aus dem Profil-Ordner:

1. `profiles/$ARGUMENTS/interests.md` - aktuelles Interessen-Profil
2. `profiles/$ARGUMENTS/onboarding_articles_2.txt` - Artikel die der User DEFINITIV lesen wuerde
3. `profiles/$ARGUMENTS/onboarding_articles_1.txt` - Artikel die der User VIELLEICHT lesen wuerde
4. `profiles/$ARGUMENTS/onboarding_articles_0.txt` - Artikel die der User NICHT lesen wuerde

Falls auch Event-Dateien existieren, lies diese ebenfalls:
5. `profiles/$ARGUMENTS/onboarding_events_2.txt` - Termine die den User DEFINITIV interessieren
6. `profiles/$ARGUMENTS/onboarding_events_1.txt` - Termine die den User VIELLEICHT interessieren
7. `profiles/$ARGUMENTS/onboarding_events_0.txt` - Termine die den User NICHT interessieren

---

## Phase 2: Arbeitshypothesen erstellen

Analysiere Artikel UND Termine in jeder Kategorie und identifiziere Patterns:

**Fuer Artikel:**
- **Themen** - Welche Themengebiete tauchen auf?
- **Ton/Stil** - Sachlich, meinungsstark, investigativ, etc.?
- **Quellen** - Gibt es Praeferenzen fuer bestimmte Quellen?
- **Format** - Essays, Nachrichten, FAQs, Ueberblicke?

**Fuer Termine:**
- **Event-Typen** - Demos, Workshops, Konzerte, Vortraege, etc.?
- **Locations** - Bestimmte Orte oder Bezirke bevorzugt?
- **Themen** - Welche politischen/kulturellen Themen?
- **Format** - Einmalige Events vs. regelmaessige Treffen?

Erstelle dann eine Datei `profiles/$ARGUMENTS/tmp_interests.md` mit deinen Arbeitshypothesen.

---

## Phase 3: Grenzfaelle identifizieren

Schau dir die Daten kritisch an und finde Inkonsistenzen:

- Artikel in Kategorie 0, die thematisch zu Kategorie 2 passen wuerden
- Artikel in Kategorie 2, die aehnlich klingen wie welche in Kategorie 0
- Termine wo das Thema interessiert, aber das Format nicht (oder umgekehrt)

Beispiel: Ein Artikel ueber "Rojava" ist in Kategorie 2, aber eine "Demo fuer Rojava" in Kategorie 0. Warum?

---

## Phase 4: Klaerende Nachfragen - INTENTIONEN verstehen

**WICHTIG:** Frage nicht nur nach Themen, sondern nach den INTENTIONEN dahinter!

Stelle dem User gezielte Fragen zu den Grenzfaellen. Aber gehe tiefer:

### Bei Artikeln fragen:
- **Was ist die Handlungsrelevanz?** - Warum ist dieser Artikel fuer dich wichtig?
- **Betrifft es dich direkt?** - Lokal, persoenlich, in deinen Raeumen?
- **Hilft es dir zu verstehen?** - Systeme, Herrschaft, Zusammenhaenge?
- **Gibt es dir Inspiration?** - Fuer eigenes Handeln, Projekte?

### Bei Terminen fragen:
- **Was willst du dort erreichen?** - Lernen, Vernetzen, Wirksam werden?
- **Warum dieses Format und nicht ein anderes?** - Workshop vs. Demo vs. Vortrag?

### Uebergeordnete Fragen stellen:
- **Was ist der Zweck des Newsletters fuer dich?**
- **Was willst du mit den Informationen machen?**
- **Wie soll der Newsletter dein Leben bereichern?**

Die Antworten helfen dir, die tieferen Kriterien zu verstehen - nicht nur WAS interessiert, sondern WARUM.

---

## Phase 5: Hypothesen verfeinern

Mit den Antworten:

1. Aktualisiere `profiles/$ARGUMENTS/tmp_interests.md`
2. Formuliere **Leitfragen** die Claude beim Newsletter-Erstellen anwenden kann
3. Erfasse die **Kern-Intention** des Users
4. Zeige dem User die finale Version zur Bestaetigung

### Gute Leitfragen sind:
- "Betrifft es mich direkt?"
- "Wird es mein Leben in der naechsten Zukunft beeinflussen?"
- "Hilft es mir, Systeme zu verstehen?"
- "Kann ich dort Menschen kennenlernen?"

### Schlechte Leitfragen sind:
- "Ist es ein politisches Thema?" (zu vage)
- "Ist es interessant?" (subjektiv)

---

## Phase 6: Interessen aktualisieren

Wenn der User zufrieden ist:

1. Aktualisiere `profiles/$ARGUMENTS/interests.md` mit:
   - Kern-Intention des Newsletters
   - Leitfragen fuer Artikel und Termine
   - Themen die interessieren (mit Kontext warum)
   - Format-Regeln
   - Was NICHT interessiert

2. Die Datei sollte so strukturiert sein, dass Claude beim Newsletter-Erstellen schnell pruefen kann, ob ein Artikel/Termin relevant ist.

---

## Wichtige Hinweise

- **Intentionen > Themen:** Die Gruende sind wertvoller als die Liste
- **Handlungsrelevanz fragen:** "Was machst du mit dieser Information?"
- **Format beachten:** Gleiches Thema kann in einem Format interessant sein und in einem anderen nicht
- **Nicht zu spezifisch:** Listen sind Beispiele, nicht erschoepfend
- **Den Menschen verstehen:** Was fuer ein Leben will diese Person fuehren?

### Typische Unterscheidungen die wichtig sind:

**Bei Artikeln:**
- Essay/Analyse vs. Klein-Klein/Updates
- Wichtige Entscheidungen vs. laufende Diskussionen
- Einordnung vs. "X hat Y gesagt"

**Bei Terminen:**
- Einmalige Events vs. regelmaessige Stammtische
- Lokale Demos vs. globale Solidaritaets-Demos
- Lernen/Vernetzen vs. passive Teilnahme
