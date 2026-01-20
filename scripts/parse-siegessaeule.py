#!/usr/bin/env python3
"""
Parst die Siegessäule-Termine aus HTML und erstellt ein kompaktes Text-Format.
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
    current_category = ""

    # Verarbeite jede Sektion
    pos = 0
    while True:
        # Finde nächste Kategorie-Überschrift
        cat_match = re.search(r'<section class="content listing"><h3>([^<]+)</h3>', html[pos:])
        if not cat_match:
            break

        current_category = cat_match.group(1).strip()
        section_start = pos + cat_match.start()

        # Finde Ende der Sektion
        section_end_match = re.search(r'</section>', html[section_start + 50:])
        if section_end_match:
            section_end = section_start + 50 + section_end_match.end()
        else:
            section_end = len(html)

        section_html = html[section_start:section_end]

        # Finde alle Events in dieser Sektion
        event_pattern = r'<a sapper:prefetch href="([^"]+)"[^>]*>.*?<div class="typography--overline">([^<]+)</div>\s*<h4[^>]*>([^<]+)</h4>\s*<div class="event-description[^"]*">([^<]*)</div>.*?</span>\s*([^<]+)</div>'

        for match in re.finditer(event_pattern, section_html, re.DOTALL):
            url = match.group(1)
            datetime = match.group(2).strip()
            title = unescape(match.group(3)).strip()
            description = unescape(match.group(4)).strip()
            venue = match.group(5).strip()

            events.append({
                'url': 'https://www.siegessaeule.de' + url,
                'datetime': datetime,
                'title': title,
                'description': description,
                'venue': venue,
                'category': current_category
            })

        pos = section_end

    # Falls keine Sektionen gefunden, versuche einzelne Events zu finden
    if not events:
        event_pattern = r'<a sapper:prefetch href="([^"]+)"[^>]*>.*?<div class="typography--overline">([^<]+)</div>\s*<h4[^>]*>([^<]+)</h4>\s*<div class="event-description[^"]*">([^<]*)</div>.*?</span>\s*([^<]+)</div>'

        for match in re.finditer(event_pattern, html, re.DOTALL):
            url = match.group(1)
            datetime = match.group(2).strip()
            title = unescape(match.group(3)).strip()
            description = unescape(match.group(4)).strip()
            venue = match.group(5).strip()

            events.append({
                'url': 'https://www.siegessaeule.de' + url,
                'datetime': datetime,
                'title': title,
                'description': description,
                'venue': venue,
                'category': ''
            })

    return events


def format_events(events):
    """Formatiert Events als kompakten Text."""
    output = []
    current_category = ""

    for event in events:
        if event.get('category') and event['category'] != current_category:
            current_category = event['category']
            output.append(f"\n## {current_category}\n")

        output.append(f"### {event['title']}")

        meta = [f"Zeit: {event['datetime']}"]
        if event.get('venue'):
            meta.append(f"Ort: {event['venue']}")
        output.append(' | '.join(meta))

        if event.get('description'):
            output.append(event['description'])

        output.append(f"URL: {event['url']}")
        output.append("")

    return '\n'.join(output)


def main():
    if len(sys.argv) != 3:
        print("Usage: parse-siegessaeule.py input.html output.txt")
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
