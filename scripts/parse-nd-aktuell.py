#!/usr/bin/env python3
"""
Parst die nd-aktuell.de Artikel-Übersicht aus HTML und erstellt ein kompaktes Text-Format.
"""

import re
import sys
from html import unescape


def parse_articles(html):
    """Extrahiert alle Artikel aus dem HTML."""
    articles = []
    seen_urls = set()

    # Pattern für Artikel-Links
    pattern = r'<a href="(/artikel/[^"]+\.html)"[^>]*aria-label="([^"]+)"'
    
    for match in re.finditer(pattern, html):
        url = match.group(1)
        title = unescape(match.group(2)).strip()
        
        # Duplikate vermeiden
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        # Kontext um den Match herum für Kicker und Teaser
        start_pos = max(0, match.start() - 200)
        end_pos = min(len(html), match.end() + 1000)
        context = html[start_pos:end_pos]
        
        # Kicker (Kategorie) finden
        kicker = ""
        kicker_match = re.search(r'<div class="Kicker">([^<]+)</div>', context)
        if kicker_match:
            kicker = unescape(kicker_match.group(1)).strip()
        else:
            # Alternative: span mit Kicker
            kicker_match2 = re.search(r'<span class="Kicker">([^<]+)</span>', context)
            if kicker_match2:
                kicker = unescape(kicker_match2.group(1)).strip()
        
        # Teaser finden
        teaser = ""
        teaser_match = re.search(r'<p class="Teaser"><a[^>]*>([^<]+)</a></p>', context)
        if teaser_match:
            teaser = unescape(teaser_match.group(1)).strip()
        else:
            # Einfacher Teaser ohne Link
            teaser_match2 = re.search(r'<p class="Teaser">([^<]+)</p>', context)
            if teaser_match2:
                teaser = unescape(teaser_match2.group(1)).strip()
            else:
                # Teaser als einfaches <p> nach Title
                teaser_match3 = re.search(r'</div><p>([^<]{20,})</p>', context)
                if teaser_match3:
                    teaser = unescape(teaser_match3.group(1)).strip()
        
        # Autor finden
        author = ""
        author_match = re.search(r'<div class="Author">([^<]+)</div>', context)
        if author_match:
            author = unescape(author_match.group(1)).strip()
        
        articles.append({
            'url': 'https://www.nd-aktuell.de' + url,
            'title': title,
            'kicker': kicker,
            'teaser': teaser,
            'author': author
        })

    return articles


def format_articles(articles):
    """Formatiert Artikel als kompakten Text."""
    output = ["# nd-aktuell.de - Artikel-Index\n"]

    for article in articles:
        output.append(f"### {article['title']}")
        
        if article.get('kicker'):
            output.append(f"Kategorie: {article['kicker']}")
        
        if article.get('teaser'):
            output.append(article['teaser'])
        
        if article.get('author'):
            output.append(f"Autor: {article['author']}")
        
        output.append(f"URL: {article['url']}")
        output.append("")

    return '\n'.join(output)


def main():
    if len(sys.argv) != 3:
        print("Usage: parse-nd-aktuell.py input.html output.txt")
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
