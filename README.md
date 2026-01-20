# Newsletter Generator

Automatisierter, KI-kuratierter Newsletter basierend auf persönlichen Interessen.

## Setup (VPS)

```bash
git clone <repo> newsletter
cd newsletter

# Container im Hintergrund starten
docker compose up -d --build

# In den Container verbinden
docker compose exec newsletter bash

# Claude einloggen
claude /login
# -> URL im Browser öffnen und authentifizieren

# Container verlassen (läuft weiter!)
exit
```

Der Cronjob generiert den Newsletter täglich um 6:00 Uhr.

## Befehle

**Manueller Testlauf:**
```bash
docker compose exec newsletter bash scripts/run-newsletter.sh
```

**Logs ansehen:**
```bash
docker compose exec newsletter cat /var/log/newsletter.log
```

**In den Container verbinden:**
```bash
docker compose exec newsletter bash
```

**Container neustarten:**
```bash
docker compose restart
# Danach erneut einloggen!
```

## Profile

Profile liegen in `profiles/<name>/` mit:
- `interests.md` - Was interessiert diese Person?
- `sources.md` - Welche Quellen sollen genutzt werden?

Neues Profil erstellen:
```bash
cp -r profiles/_example profiles/meinname
# Dann interests.md und sources.md anpassen
```

## Hinweise

- Nach Container-Neustart muss `claude /login` erneut ausgeführt werden
- Newsletter werden in `profiles/<name>/output/` gespeichert
- Die `.env` Datei wird nicht benötigt (Auth läuft über Browser-Login)
