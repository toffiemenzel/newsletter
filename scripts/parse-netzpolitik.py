#!/usr/bin/env python3
"""
Parst die netzpolitik.org Artikel-Übersicht aus HTML und erstellt ein kompaktes Text-Format.
"""

import re
import sys
from html import unescape


def parse_articles(html):
    """Extrahiert alle Artikel aus dem HTML."""
    articles = []
    seen_urls = set()

    # Finde alle article-Blöcke
    article_pattern = r'<article[^>]*class="teaser[^"]*post-\d+[^"]*"[^>]*>(.*?)</article>'
    
    for article_match in re.finditer(article_pattern, html, re.DOTALL):
        article_html = article_match.group(1)
        
        # URL und Titel finden
        link_match = re.search(r'<a href="(https://netzpolitik\.org/\d{4}/[^"]+)"[^>]*class="[^"]*teaser__headline-link[^"]*"[^>]*title="([^"]+)"', article_html)
        if not link_match:
            continue
            
        url = link_match.group(1)
        title = unescape(link_match.group(2)).strip()
        
        # Duplikate vermeiden
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        # Kicker (Kategorie)
        kicker = ""
        kicker_match = re.search(r'<span class="teaser__kicker">([^<]+)</span>', article_html)
        if kicker_match:
            kicker = unescape(kicker_match.group(1)).strip()
        
        # Subtitle
        subtitle = ""
        subtitle_match = re.search(r'<span class="teaser__subtitle">([^<]+)<span', article_html)
        if subtitle_match:
            subtitle = unescape(subtitle_match.group(1)).strip()
        
        # Teaser
        teaser = ""
        teaser_match = re.search(r'<div class="teaser__excerpt[^"]*"><p>([^<]+)</p>', article_html)
        if teaser_match:
            teaser = unescape(teaser_match.group(1)).strip()
        
        # Autor
        author = ""
        author_matches = re.findall(r'<a href="[^"]*" title="Beiträge von ([^"]+)"[^>]*rel="author"', article_html)
        if author_matches:
            author = ", ".join(author_matches)
        
        articles.append({
            'url': url,
            'title': title,
            'kicker': kicker,
            'subtitle': subtitle,
            'teaser': teaser,
            'author': author
        })

    return articles


def format_articles(articles):
    """Formatiert Artikel als kompakten Text."""
    output = ["# netzpolitik.org - Artikel-Index\n"]

    for article in articles:
        # Titel mit Subtitle kombinieren
        if article.get('subtitle'):
            output.append(f"### {article['subtitle']}: {article['title']}")
        else:
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
        print("Usage: parse-netzpolitik.py input.html output.txt")
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
