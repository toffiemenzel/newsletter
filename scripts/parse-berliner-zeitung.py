#!/usr/bin/env python3
"""
Parst die Berliner Zeitung Artikel-Übersicht aus HTML und erstellt ein kompaktes Text-Format.
"""

import re
import sys
from html import unescape


def parse_articles(html):
    """Extrahiert alle Artikel aus dem HTML."""
    articles = []
    seen_urls = set()

    # Finde alle Artikel-Links mit Titeln
    # Pattern: href="..." gefolgt von h3 mit Titel
    pattern = r'<a[^>]*href="(/[^"]+li\.\d+)"[^>]*>.*?<h3[^>]*>([^<]+)</h3>'
    
    for match in re.finditer(pattern, html, re.DOTALL):
        url = match.group(1)
        title = unescape(match.group(2)).strip()
        
        # Duplikate vermeiden
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        # Tag/Kategorie finden (suche rückwärts vom Match)
        tag = ""
        tag_match = re.search(r'data-topic="([^"]+)"[^>]*>\s*<span[^>]*>\s*([^<]+)</span>', html[max(0, match.start()-500):match.start()])
        if tag_match:
            tag = tag_match.group(2).strip()
        else:
            # Alternatives Pattern
            tag_match2 = re.search(r'aria-label="article-preview-tag"[^>]*>\s*<a[^>]*>([^<]+)</a>', html[max(0, match.start()-500):match.start()])
            if tag_match2:
                tag = unescape(tag_match2.group(1)).strip()
        
        # Teaser/Beschreibung finden
        teaser = ""
        # Suche nach Beschreibung in der Nähe
        teaser_match = re.search(r'<a[^>]*href="' + re.escape(url) + r'"[^>]*>\s*([^<]{20,})</a>', html)
        if teaser_match:
            teaser = unescape(teaser_match.group(1)).strip()
            # Nur wenn es kein Titel ist
            if teaser == title:
                teaser = ""
        
        articles.append({
            'url': 'https://www.berliner-zeitung.de' + url,
            'title': title,
            'tag': tag,
            'teaser': teaser
        })

    return articles


def format_articles(articles):
    """Formatiert Artikel als kompakten Text."""
    output = ["# Berliner Zeitung - Artikel-Index\n"]

    for article in articles:
        output.append(f"### {article['title']}")
        
        if article.get('tag'):
            output.append(f"Kategorie: {article['tag']}")
        
        if article.get('teaser'):
            output.append(article['teaser'])
        
        output.append(f"URL: {article['url']}")
        output.append("")

    return '\n'.join(output)


def main():
    if len(sys.argv) != 3:
        print("Usage: parse-berliner-zeitung.py input.html output.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    articles = parse_articles(html)
    output = format_articles(articles)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Parsed {len(articles)} articles -> {output_path}")


if __name__ == '__main__':
    main()
