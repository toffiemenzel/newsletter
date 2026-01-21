# Newsletter Generator

Automatisierter, KI-kuratierter Newsletter basierend auf persönlichen Interessen.

## Architektur

```
newsletter/
├── commands/
│   └── create-newsletter.md    # Prompt-Template für Claude
├── profiles/
│   ├── _example/               # Template für neue Profile
│   └── <name>/                 # Aktive Profile
│       ├── interests.md        # Interessen der Person
│       ├── sources.md          # Bevorzugte Quellen
│       ├── config.txt          # EMAIL_TO Konfiguration
│       └── output/             # Generierte Newsletter (YYMMDD_newsletter.html)
├── scripts/
│   ├── run-newsletter.sh       # Hauptskript (wird vom Cron aufgerufen)
│   ├── send-email.py           # E-Mail-Versand
│   └── ...                     # Fetch/Parse-Skripte für Quellen
├── setup/
│   └── entrypoint.sh           # Docker-Entrypoint (startet Cron)
├── .env                        # Gmail SMTP Credentials (nicht committen!)
├── docker-compose.yml
├── Dockerfile
└── template.html               # HTML-Template für Newsletter
```

## Setup (VPS)

```bash
git clone <repo> newsletter
cd newsletter

# .env erstellen (für E-Mail-Versand)
cp .env.example .env
# -> EMAIL_FROM und GMAIL_APP_PASSWORD eintragen

# Container im Hintergrund starten
docker compose up -d --build

# In den Container verbinden
docker compose exec newsletter bash

# Claude einloggen (als newsletter-User)
claude /login
# -> URL im Browser öffnen und authentifizieren

# Container verlassen (läuft weiter im Hintergrund)
exit
```

## Cron-Job

Der Cron-Job läuft **im Docker-Container** (nicht auf dem Host!) als `newsletter`-User.

- **Zeit:** 3:00 Uhr morgens täglich
- **Befehl:** `cd /app && bash scripts/run-newsletter.sh`
- **Log:** `profiles/newsletter.log`

**Cron-Status prüfen:**
```bash
# Cron-Job anzeigen
docker exec newsletter_newsletter_1 crontab -u newsletter -l

# Cron-Daemon läuft?
docker exec newsletter_newsletter_1 service cron status
```

## Befehle

**Manueller Testlauf:**
```bash
docker exec newsletter_newsletter_1 su - newsletter -c "cd /app && bash scripts/run-newsletter.sh"
```

**Logs ansehen:**
```bash
# Cron-Log
docker exec newsletter_newsletter_1 cat /app/profiles/newsletter.log

# Newsletter-Log eines bestimmten Tages
docker exec newsletter_newsletter_1 cat /app/profiles/toffie/output/260121_newsletter.log
```

**In den Container verbinden:**
```bash
docker compose exec newsletter bash
# oder
docker exec -it newsletter_newsletter_1 bash
```

**Container neustarten:**
```bash
docker compose restart
# WICHTIG: Danach erneut einloggen!
docker compose exec newsletter bash
claude /login
```

## Berechtigungen

Die Shell-Skripte müssen ausführbar sein:
```bash
chmod +x scripts/*.sh
```

Dies wird im Container automatisch übernommen (Volume-Mount), aber nach einem `git pull` mit neuen Skripten ggf. erneut nötig.

**Prüfen ob alles lesbar ist (als newsletter-User):**
```bash
docker exec newsletter_newsletter_1 su - newsletter -c "cat /app/scripts/run-newsletter.sh | head -3"
docker exec newsletter_newsletter_1 su - newsletter -c "cat /app/commands/create-newsletter.md | head -3"
```

## Profile

Profile liegen in `profiles/<name>/` mit:
- `interests.md` - Was interessiert diese Person?
- `sources.md` - Welche Quellen sollen genutzt werden?
- `config.txt` - E-Mail-Adresse (EMAIL_TO=...)

**Neues Profil erstellen:**
```bash
cp -r profiles/_example profiles/meinname
# Dann interests.md, sources.md und config.txt anpassen
```

## Troubleshooting

**Newsletter wird nicht generiert:**
1. Docker läuft? `docker ps`
2. Cron-Daemon läuft? `docker exec newsletter_newsletter_1 service cron status`
3. Claude eingeloggt? `docker exec newsletter_newsletter_1 su - newsletter -c "claude --version"`
4. Skripte ausführbar? `ls -la scripts/*.sh`

**Nach Container-Neustart:**
- Claude-Login geht verloren -> erneut `claude /login` ausführen

**E-Mail kommt nicht an:**
- `.env` korrekt konfiguriert?
- Gmail App-Passwort erstellt? (https://myaccount.google.com/apppasswords)

## Hinweise

- Auth läuft über Claude Subscription (Browser-Login), nicht API-Key
- Nach Container-Neustart muss `claude /login` erneut ausgeführt werden
- Newsletter werden in `profiles/<name>/output/` archiviert
- `.env` enthält Secrets und wird nicht committet (in .gitignore)
