#!/usr/bin/env python3
"""
Newsletter Email Sender
Sends HTML newsletter via Gmail SMTP using App Password
Supports multi-profile with --profile parameter
"""

import argparse
import smtplib
import sys
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path


def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / ".env"

    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        print("Please copy .env.example to .env and configure your settings.")
        sys.exit(1)

    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()

    return env_vars


def load_profile_config(profile_name: str) -> dict:
    """Load config from profile's config.txt"""
    config_path = Path(__file__).parent.parent / "profiles" / profile_name / "config.txt"

    if not config_path.exists():
        return {}

    config = {}
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()

    return config


def html_to_plain_text(html: str) -> str:
    """Convert HTML to plain text for email fallback"""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<h[12][^>]*>', '\n\n## ', text)
    text = re.sub(r'</h[12]>', '\n', text)
    text = re.sub(r'<h[3-6][^>]*>', '\n### ', text)
    text = re.sub(r'</h[3-6]>', '\n', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>', r'\2 (\1)', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def send_email(html_content: str, env: dict, profile_config: dict) -> bool:
    """Send HTML newsletter email via Gmail SMTP"""

    # EMAIL_TO comes from profile config, rest from .env
    email_to = profile_config.get("EMAIL_TO") or env.get("EMAIL_TO")
    email_from = env.get("EMAIL_FROM")
    password = env.get("GMAIL_APP_PASSWORD")

    if not email_to:
        print("Error: EMAIL_TO not set (check profile config.txt or .env)")
        return False
    if not email_from:
        print("Error: EMAIL_FROM not set in .env file")
        return False
    if not password:
        print("Error: GMAIL_APP_PASSWORD not set in .env file")
        return False

    today = datetime.now().strftime("%d.%m.%Y")
    subject = f"Dein Newsletter - {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Tagesprophet <{email_from}>"
    msg["To"] = email_to

    plain_text = html_to_plain_text(html_content)
    text_part = MIMEText(plain_text, "plain", "utf-8")
    html_part = MIMEText(html_content, "html", "utf-8")

    msg.attach(text_part)
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_from, password)
            server.sendmail(email_from, email_to, msg.as_string())

        print(f"Newsletter sent successfully to {email_to}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Error: Gmail authentication failed.")
        print("Make sure you're using an App Password, not your regular password.")
        print("Create one at: https://myaccount.google.com/apppasswords")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Send newsletter email")
    parser.add_argument("--profile", "-p", help="Profile name (reads EMAIL_TO from profile config)")
    parser.add_argument("file", nargs="?", help="Path to HTML newsletter file")
    args = parser.parse_args()

    env = load_env()
    profile_config = {}

    if args.profile:
        profile_config = load_profile_config(args.profile)
        if not profile_config:
            print(f"Warning: Could not load config for profile '{args.profile}'")

    content = None

    if args.file:
        file_path = Path(args.file)
        if file_path.exists() and file_path.suffix == ".html":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"Reading newsletter from: {file_path}")
        else:
            print(f"Error: File not found or not HTML: {args.file}")
            sys.exit(1)
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        print("Usage: python send-email.py [--profile=NAME] path/to/newsletter.html")
        print("   or: cat newsletter.html | python send-email.py [--profile=NAME]")
        print("")
        print("Options:")
        print("  --profile, -p    Profile name (uses EMAIL_TO from profiles/NAME/config.txt)")
        sys.exit(1)

    if not content or not content.strip():
        print("Error: No content provided")
        sys.exit(1)

    success = send_email(content, env, profile_config)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
