#!/usr/bin/env python3
"""
Parst die Stressfaktor-Termine aus HTML und erstellt ein kompaktes Text-Format.
"""

import re
import sys
from html import unescape


def extract_text(html):
    """Entfernt HTML-Tags und gibt reinen Text zurück."""
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_events(html):
    """Extrahiert alle Events aus dem HTML."""
    events = []

    # Finde alle Event-Blöcke
    event_pattern = r'<div class="is-published views-row"[^>]*>(.*?)</div>\s*(?=<div class="is-published views-row"|<h3>|</div>\s*$|<!-- Page)'

    # Finde Datumsüberschriften
    date_pattern = r'<h3>([^<]+)</h3>'

    current_date = ""
    pos = 0

    while pos < len(html):
        # Suche nächste Datumsüberschrift
        date_match = re.search(date_pattern, html[pos:])
        # Suche nächsten Event-Block
        event_match = re.search(r'<div class="is-published views-row" id="([^"]+)">', html[pos:])

        if date_match and (not event_match or date_match.start() < event_match.start()):
            current_date = date_match.group(1).strip()
            pos += date_match.end()
            continue

        if not event_match:
            break

        event_start = pos + event_match.start()
        event_id = event_match.group(1)

        # Finde das Ende des Event-Blocks (nächster Event oder Datumsüberschrift)
        remaining = html[event_start:]

        # Finde den nächsten Event-Start oder Datum
        next_boundary = re.search(r'<div class="is-published views-row" id="(?!' + event_id + ')|<h3>', remaining[50:])
        if next_boundary:
            event_html = remaining[:50 + next_boundary.start()]
        else:
            event_html = remaining[:5000]  # Fallback

        event = parse_single_event(event_html, current_date)
        if event and event.get('status') != 'cancelled':
            events.append(event)

        pos = event_start + 100  # Weiter zum nächsten

    return events


def parse_single_event(html, date):
    """Parst einen einzelnen Event-Block."""
    event = {'date': date}

    # Status (cancelled?)
    if 'status-cancelled' in html:
        event['status'] = 'cancelled'
        return event
    event['status'] = 'confirmed'

    # Titel und URL
    title_match = re.search(r'<h4[^>]*><a href="([^"]+)"[^>]*>([^<]+)</a></h4>', html)
    if title_match:
        event['url'] = 'https://stressfaktor.squat.net' + title_match.group(1)
        event['title'] = unescape(title_match.group(2)).strip()
    else:
        return None

    # Zeit
    time_matches = re.findall(r'<time[^>]*>([^<]+)</time>', html)
    if time_matches:
        if len(time_matches) >= 2:
            event['time'] = f"{time_matches[0].strip()}-{time_matches[1].strip()}"
        else:
            event['time'] = time_matches[0].strip()

    # Ort
    org_match = re.search(r'<span class="organization">([^<]+)</span>', html)
    street_match = re.search(r'<span class="address-line1">([^<]+)</span>', html)
    plz_match = re.search(r'<span class="postal-code">([^<]+)</span>', html)
    city_match = re.search(r'<span class="locality">([^<]+)</span>', html)

    location_parts = []
    if org_match:
        location_parts.append(unescape(org_match.group(1)).strip())
    if street_match:
        location_parts.append(unescape(street_match.group(1)).strip())
    if plz_match and city_match:
        location_parts.append(f"{plz_match.group(1)} {city_match.group(1)}")
    elif city_match:
        location_parts.append(city_match.group(1))

    event['location'] = ', '.join(location_parts) if location_parts else 'Berlin'

    # Beschreibung
    desc_match = re.search(r'<span class="field-content status-confirmed">([^<].*?)</span></div><span', html, re.DOTALL)
    if desc_match:
        event['description'] = extract_text(desc_match.group(1))[:200]
    else:
        # Fallback
        desc_match2 = re.search(r'views-field-body"><span class="field-content[^"]*">(.+?)</span></div>', html, re.DOTALL)
        if desc_match2:
            event['description'] = extract_text(desc_match2.group(1))[:200]

    # Kategorie
    cat_match = re.search(r'views-field-field-category"><span class="field-content">([^<]+)</span>', html)
    if cat_match and cat_match.group(1).strip():
        event['category'] = cat_match.group(1).strip()

    # Tags/Topics
    topic_match = re.search(r'views-field-field-topic"><span class="field-content">([^<]+)</span>', html)
    if topic_match and topic_match.group(1).strip():
        event['tags'] = topic_match.group(1).strip()

    # Preis
    price_match = re.search(r'views-field-field-price-category"><span class="field-content">([^<]+)</span>', html)
    if price_match and price_match.group(1).strip():
        event['price'] = price_match.group(1).strip()

    return event


def format_events(events):
    """Formatiert Events als kompakten Text."""
    output = []
    current_date = ""

    for event in events:
        if event['date'] != current_date:
            current_date = event['date']
            output.append(f"\n## {current_date}\n")

        output.append(f"### {event.get('title', 'Unbekannt')}")

        meta = []
        if event.get('time'):
            meta.append(f"Zeit: {event['time']}")
        if event.get('location'):
            meta.append(f"Ort: {event['location']}")
        if event.get('price'):
            meta.append(f"Preis: {event['price']}")
        output.append(' | '.join(meta))

        if event.get('description'):
            output.append(event['description'])

        tags_cat = []
        if event.get('category'):
            tags_cat.append(f"Kategorie: {event['category']}")
        if event.get('tags'):
            tags_cat.append(f"Tags: {event['tags']}")
        if tags_cat:
            output.append(' | '.join(tags_cat))

        output.append(f"URL: {event.get('url', '')}")
        output.append("")

    return '\n'.join(output)


def main():
    if len(sys.argv) != 3:
        print("Usage: parse-stressfaktor.py input.html output.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    events = parse_events(html)
    output = format_events(events)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Parsed {len(events)} events -> {output_path}")


if __name__ == '__main__':
    main()
