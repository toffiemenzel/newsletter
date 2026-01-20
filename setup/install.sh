#!/bin/bash
#
# Newsletter System - VPS Setup Script
# Run this on a fresh Ubuntu/Debian VPS
#

set -e

echo "=== Newsletter System Setup ==="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please don't run this script as root."
    echo "Run as normal user with sudo access."
    exit 1
fi

echo "1. Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

echo ""
echo "2. Installing dependencies..."
sudo apt-get install -y python3 python3-pip git curl

echo ""
echo "3. Installing Node.js (required for Claude CLI)..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi
echo "Node.js version: $(node --version)"

echo ""
echo "4. Installing Claude CLI..."
if ! command -v claude &> /dev/null; then
    npm install -g @anthropic-ai/claude-code
fi
echo "Claude CLI installed"

echo ""
echo "5. Setting up project directory..."
PROJECT_DIR="$HOME/newsletter"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Please clone your newsletter repository to $PROJECT_DIR"
    echo "  git clone <your-repo-url> $PROJECT_DIR"
else
    echo "Project directory exists at $PROJECT_DIR"
fi

echo ""
echo "=== Manual Steps Required ==="
echo ""
echo "1. Clone your repo (if not done):"
echo "   git clone <your-repo-url> $HOME/newsletter"
echo ""
echo "2. Configure environment:"
echo "   cd $HOME/newsletter"
echo "   cp .env.example .env"
echo "   nano .env  # Add your Gmail credentials"
echo ""
echo "3. Authenticate Claude CLI:"
echo "   claude"
echo "   # Follow the authentication prompts"
echo ""
echo "4. Test the email script:"
echo "   cd $HOME/newsletter"
echo "   python3 scripts/send-email.py 'Test newsletter'"
echo ""
echo "5. Test the full newsletter:"
echo "   cd $HOME/newsletter"
echo "   ./scripts/run-newsletter.sh"
echo ""
echo "6. Set up cron job (daily at 7:00 AM):"
echo "   crontab -e"
echo "   # Add this line:"
echo "   0 7 * * * $HOME/newsletter/scripts/run-newsletter.sh"
echo ""
echo "=== Setup Complete ==="
