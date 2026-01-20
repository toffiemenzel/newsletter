#!/usr/bin/env python3
"""
Parst die taz.de Artikel-Teaser aus HTML und erstellt ein kompaktes Text-Format.
"""

import re
import sys
from html import unescape


def clean_text(text):
    """Entfernt HTML-Tags, normalisiert Whitespace."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_articles(html):
    """Extrahiert alle Artikel-Teaser aus dem HTML."""
    articles = []
    seen_urls = set()

    # Pattern für Artikel-Blöcke mit Teaser-Link
    # Suche nach href, dann topline, headline und subline
    pattern = r'<a[^>]*href="(/[^"]+/!(\d+)/)"[^>]*class="[^"]*teaser-link[^"]*"[^>]*>.*?<span[^>]*typo-r-topline[^>]*>\s*([^<]+)</span>.*?<span[^>]*headline[^>]*link[^>]*typo-r-head[^>]*>\s*([^<]+)</span>.*?</a>.*?<p[^>]*typo-r-subline[^>]*>\s*([^<]+)</p>'

    for match in re.finditer(pattern, html, re.DOTALL):
        url_path = match.group(1)
        article_id = match.group(2)
        topline = clean_text(match.group(3))
        headline = clean_text(match.group(4))
        teaser = clean_text(match.group(5))

        # Duplikate vermeiden
        if article_id in seen_urls:
            continue
        seen_urls.add(article_id)

        # Werbung/Abo-Teaser filtern
        if '/abo/' in url_path or '/!v=' in url_path or '/!vn' in url_path:
            continue

        articles.append({
            'url': 'https://taz.de' + url_path,
            'topline': topline,
            'headline': headline,
            'teaser': teaser
        })

    return articles


def format_articles(articles):
    """Formatiert Artikel als kompakten Text."""
    output = ["# taz.de Artikel-Index\n"]

    for article in articles:
        title = article['headline']
        if article['topline'] and article['topline'] != article['headline']:
            title = f"{article['topline']}: {article['headline']}"

        output.append(f"### {title}")
        if article['teaser']:
            output.append(article['teaser'])
        output.append(f"URL: {article['url']}")
        output.append("")

    return '\n'.join(output)


def main():
    if len(sys.argv) != 3:
        print("Usage: parse-taz.py input.html output.txt")
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
