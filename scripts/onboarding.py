#!/usr/bin/env python3
"""
Newsletter Onboarding / Interest Refinement Tool

Fetches articles from all sources and lets you rate them interactively.
Results are saved to the selected profile folder for pattern analysis.
"""

import subprocess
import sys
import os
import re
from pathlib import Path

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

# Define which sources are articles vs events
ARTICLE_SOURCES = ['taz', 'berliner-zeitung', 'nd-aktuell', 'netzpolitik']
EVENT_SOURCES = ['termine', 'siegessaeule']

def get_project_dir():
    """Get the project root directory."""
    return Path(__file__).parent.parent.resolve()

def get_available_profiles():
    """Find all available profiles (excluding _example)."""
    project_dir = get_project_dir()
    profiles_dir = project_dir / "profiles"

    if not profiles_dir.exists():
        return []

    profiles = []
    for item in profiles_dir.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            profiles.append(item.name)

    return sorted(profiles)

def select_profile():
    """Let user select a profile."""
    profiles = get_available_profiles()

    if not profiles:
        print(f"{Colors.RED}Keine Profile gefunden!{Colors.RESET}")
        print(f"Erstelle zuerst ein Profil mit: cp -r profiles/_example profiles/deinname")
        return None

    print(f"{Colors.BOLD}Verfuegbare Profile:{Colors.RESET}")
    for i, profile in enumerate(profiles, 1):
        print(f"  {Colors.GREEN}[{i}]{Colors.RESET} {profile}")
    print()

    while True:
        try:
            choice = input(f"Waehle ein Profil [1-{len(profiles)}]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(profiles):
                return profiles[idx]
            print(f"{Colors.RED}Ungueltige Auswahl{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Bitte eine Zahl eingeben{Colors.RESET}")
        except (EOFError, KeyboardInterrupt):
            return None

def fetch_all_sources():
    """Execute all fetch-*.sh scripts."""
    scripts_dir = Path(__file__).parent
    fetch_scripts = sorted(scripts_dir.glob("fetch-*.sh"))

    if not fetch_scripts:
        print(f"{Colors.RED}Keine fetch-*.sh Skripte gefunden!{Colors.RESET}")
        return False

    print(f"{Colors.BOLD}Fetching articles from {len(fetch_scripts)} sources...{Colors.RESET}\n")

    for script in fetch_scripts:
        source_name = script.stem.replace("fetch-", "")
        print(f"  {Colors.DIM}Fetching {source_name}...{Colors.RESET}", end=" ", flush=True)
        try:
            result = subprocess.run(
                ["bash", str(script)],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print(f"{Colors.GREEN}OK{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}Warning{Colors.RESET}")
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}Timeout{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")

    print()
    return True

def parse_items(source_filter):
    """Parse tmp_*.txt files and extract items, filtered by source type."""
    project_dir = get_project_dir()

    items = []

    for source_name in source_filter:
        tmp_file = project_dir / f"tmp_{source_name}.txt"

        if not tmp_file.exists():
            print(f"{Colors.DIM}  {tmp_file.name} nicht gefunden, ueberspringe...{Colors.RESET}")
            continue

        try:
            content = tmp_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"{Colors.YELLOW}Could not read {tmp_file.name}: {e}{Colors.RESET}")
            continue

        # Split by item markers (### at start of line)
        item_blocks = re.split(r'\n(?=### )', content)

        for block in item_blocks:
            block = block.strip()
            if not block.startswith("### "):
                continue

            lines = block.split("\n")

            # Extract title (first line without ###)
            title = lines[0].replace("### ", "").strip()

            # Extract URL and other metadata
            url = ""
            time_location = ""
            category = ""
            description_lines = []

            for line in lines[1:]:
                line = line.strip()
                if line.startswith("URL:"):
                    url = line.replace("URL:", "").strip()
                elif line.startswith("Zeit:"):
                    time_location = line
                elif line.startswith("Kategorie:"):
                    category = line.replace("Kategorie:", "").strip()
                elif line and not line.startswith("Tags:"):
                    description_lines.append(line)

            description = " ".join(description_lines)

            if title:
                items.append({
                    "source": source_name,
                    "title": title,
                    "description": description,
                    "time_location": time_location,
                    "category": category,
                    "url": url,
                    "raw": block
                })

    return items

def parse_articles():
    """Parse article sources."""
    return parse_items(ARTICLE_SOURCES)

def parse_events():
    """Parse event sources."""
    return parse_items(EVENT_SOURCES)

def display_item(item, index, total, is_event=False):
    """Display a single item for rating."""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.DIM}[{index+1}/{total}] Quelle: {item['source']}{Colors.RESET}")

    if is_event:
        print(f"{Colors.BOLD}{Colors.CYAN}{item['title']}{Colors.RESET}")
        if item.get('time_location'):
            print(f"{Colors.GREEN}{item['time_location']}{Colors.RESET}")
        if item.get('category'):
            print(f"{Colors.DIM}Kategorie: {item['category']}{Colors.RESET}")
    else:
        print(f"{Colors.BOLD}{Colors.BLUE}{item['title']}{Colors.RESET}")

    print()
    if item['description']:
        # Truncate long descriptions
        desc = item['description']
        if len(desc) > 300:
            desc = desc[:300] + "..."
        print(f"{desc}")
    if item['url']:
        print(f"\n{Colors.DIM}{item['url']}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

def get_rating(is_event=False):
    """Get user rating for an item."""
    print()
    if is_event:
        print(f"  {Colors.RED}[0]{Colors.RESET} Nein - wuerde ich nicht hingehen")
        print(f"  {Colors.YELLOW}[1]{Colors.RESET} Vielleicht - kommt auf die Stimmung an")
        print(f"  {Colors.GREEN}[2]{Colors.RESET} Ja - klingt interessant!")
    else:
        print(f"  {Colors.RED}[0]{Colors.RESET} Nein - wuerde ich nicht anklicken")
        print(f"  {Colors.YELLOW}[1]{Colors.RESET} Vielleicht - kommt drauf an")
        print(f"  {Colors.GREEN}[2]{Colors.RESET} Ja - wuerde ich definitiv lesen")
    print(f"  {Colors.DIM}[s]{Colors.RESET} Skip - ueberspringen")
    print(f"  {Colors.DIM}[q]{Colors.RESET} Quit - beenden und speichern")
    print()

    while True:
        try:
            choice = input(f"  Deine Wahl: ").strip().lower()
            if choice in ['0', '1', '2']:
                return int(choice)
            elif choice == 's':
                return None
            elif choice == 'q':
                return 'quit'
            else:
                print(f"  {Colors.RED}Bitte 0, 1, 2, s oder q eingeben{Colors.RESET}")
        except EOFError:
            return 'quit'
        except KeyboardInterrupt:
            print()
            return 'quit'

def save_results(rated_items, profile_dir, is_event=False):
    """Save rated items to onboarding files in profile folder."""

    prefix = "onboarding_events" if is_event else "onboarding_articles"
    item_type = "Termine" if is_event else "Artikel"

    # Group by rating
    groups = {0: [], 1: [], 2: []}
    for item, rating in rated_items:
        if rating in groups:
            groups[rating].append(item)

    # Save each group to profile folder
    for rating, items in groups.items():
        output_file = profile_dir / f"{prefix}_{rating}.txt"

        content_lines = []
        if is_event:
            if rating == 0:
                content_lines.append("# Termine die mich NICHT interessieren\n")
                content_lines.append("# Zu diesen Veranstaltungen wuerde ich nicht gehen\n\n")
            elif rating == 1:
                content_lines.append("# Termine die mich VIELLEICHT interessieren\n")
                content_lines.append("# Je nach Stimmung wuerde ich vielleicht hingehen\n\n")
            else:
                content_lines.append("# Termine die mich DEFINITIV interessieren\n")
                content_lines.append("# Diese Veranstaltungen wuerde ich besuchen\n\n")
        else:
            if rating == 0:
                content_lines.append("# Artikel die mich NICHT interessieren\n")
                content_lines.append("# Diese Artikel wuerde ich nicht anklicken\n\n")
            elif rating == 1:
                content_lines.append("# Artikel die mich VIELLEICHT interessieren\n")
                content_lines.append("# Diese Artikel wuerde ich vielleicht lesen, je nach Stimmung\n\n")
            else:
                content_lines.append("# Artikel die mich DEFINITIV interessieren\n")
                content_lines.append("# Diese Artikel wuerde ich auf jeden Fall lesen\n\n")

        for item in items:
            content_lines.append(f"[{item['source']}]\n")
            content_lines.append(f"### {item['title']}\n")
            if item.get('time_location'):
                content_lines.append(f"{item['time_location']}\n")
            if item.get('category'):
                content_lines.append(f"Kategorie: {item['category']}\n")
            if item['description']:
                content_lines.append(f"{item['description']}\n")
            if item['url']:
                content_lines.append(f"URL: {item['url']}\n")
            content_lines.append("\n")

        output_file.write_text("".join(content_lines), encoding="utf-8")
        print(f"  {output_file.name}: {len(items)} {item_type}")

def rate_items(items, is_event=False):
    """Interactive rating loop for a list of items."""
    item_type = "Termine" if is_event else "Artikel"
    rated_items = []

    for i, item in enumerate(items):
        display_item(item, i, len(items), is_event=is_event)
        rating = get_rating(is_event=is_event)

        if rating == 'quit':
            print(f"\n{Colors.YELLOW}Abgebrochen nach {i} {item_type}.{Colors.RESET}")
            break

        if rating is not None:
            rated_items.append((item, rating))

    return rated_items

def print_summary(rated_items, is_event=False):
    """Print rating summary."""
    item_type = "Termine" if is_event else "Artikel"
    counts = {0: 0, 1: 0, 2: 0}
    for _, rating in rated_items:
        counts[rating] += 1

    print(f"\n{Colors.BOLD}Zusammenfassung {item_type}:{Colors.RESET}")
    print(f"  {Colors.RED}Nein:{Colors.RESET}       {counts[0]} {item_type}")
    print(f"  {Colors.YELLOW}Vielleicht:{Colors.RESET} {counts[1]} {item_type}")
    print(f"  {Colors.GREEN}Ja:{Colors.RESET}         {counts[2]} {item_type}")

def main():
    project_dir = get_project_dir()

    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║     Newsletter Onboarding / Refinement   ║")
    print("  ╚══════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    print("Dieses Tool hilft dir, dein Interesse-Profil zu kalibrieren.")
    print("Du bewertest Artikel und Termine, und Claude lernt daraus.\n")

    # Select profile
    profile_name = select_profile()
    if not profile_name:
        print("\nAbgebrochen.")
        return

    profile_dir = project_dir / "profiles" / profile_name
    print(f"\n{Colors.GREEN}Profil ausgewaehlt: {profile_name}{Colors.RESET}\n")

    # Ask if we should fetch fresh content
    try:
        fetch_choice = input(f"Inhalte neu fetchen? [{Colors.GREEN}j{Colors.RESET}/n]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nAbgebrochen.")
        return

    if fetch_choice != 'n':
        fetch_all_sources()

    # Ask what to rate
    print(f"\n{Colors.BOLD}Was moechtest du bewerten?{Colors.RESET}")
    print(f"  {Colors.BLUE}[1]{Colors.RESET} Nur Artikel (taz, berliner-zeitung, nd-aktuell, netzpolitik)")
    print(f"  {Colors.CYAN}[2]{Colors.RESET} Nur Termine (stressfaktor, siegessaeule)")
    print(f"  {Colors.GREEN}[3]{Colors.RESET} Beides (Artikel zuerst, dann Termine)")
    print()

    try:
        mode_choice = input(f"  Deine Wahl [1/2/3]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAbgebrochen.")
        return

    do_articles = mode_choice in ['1', '3']
    do_events = mode_choice in ['2', '3']

    if not do_articles and not do_events:
        print(f"{Colors.YELLOW}Keine gueltige Auswahl, beende.{Colors.RESET}")
        return

    # === ARTICLES ===
    if do_articles:
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== ARTIKEL ==={Colors.RESET}")
        print(f"{Colors.DIM}Quellen: taz, berliner-zeitung, nd-aktuell, netzpolitik{Colors.RESET}\n")

        articles = parse_articles()

        if not articles:
            print(f"{Colors.YELLOW}Keine Artikel gefunden.{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}{len(articles)} Artikel gefunden{Colors.RESET}\n")
            print("Bewerte jeden Artikel: Wuerdest du ihn anklicken?\n")

            rated_articles = rate_items(articles, is_event=False)

            if rated_articles:
                print(f"\n{Colors.BOLD}Speichere Artikel-Ergebnisse...{Colors.RESET}")
                save_results(rated_articles, profile_dir, is_event=False)
                print_summary(rated_articles, is_event=False)

    # === EVENTS ===
    if do_events:
        print(f"\n{Colors.BOLD}{Colors.CYAN}=== TERMINE ==={Colors.RESET}")
        print(f"{Colors.DIM}Quellen: stressfaktor, siegessaeule{Colors.RESET}\n")

        events = parse_events()

        if not events:
            print(f"{Colors.YELLOW}Keine Termine gefunden.{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}{len(events)} Termine gefunden{Colors.RESET}\n")
            print("Bewerte jeden Termin: Wuerdest du hingehen?\n")

            rated_events = rate_items(events, is_event=True)

            if rated_events:
                print(f"\n{Colors.BOLD}Speichere Termin-Ergebnisse...{Colors.RESET}")
                save_results(rated_events, profile_dir, is_event=True)
                print_summary(rated_events, is_event=True)

    # Final instructions
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Fertig!{Colors.RESET}\n")
    print(f"Die Ergebnisse wurden im Profil-Ordner gespeichert:")
    print(f"  {Colors.DIM}profiles/{profile_name}/{Colors.RESET}")
    if do_articles:
        print(f"  {Colors.BLUE}onboarding_articles_0/1/2.txt{Colors.RESET}")
    if do_events:
        print(f"  {Colors.CYAN}onboarding_events_0/1/2.txt{Colors.RESET}")

    print(f"\n{Colors.BOLD}Naechster Schritt:{Colors.RESET}")
    print(f"  Fuehre den Befehl aus: {Colors.GREEN}/refine-interests {profile_name}{Colors.RESET}")
    print()

if __name__ == "__main__":
    main()
