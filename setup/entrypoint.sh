#!/bin/bash

# Setup cron job for newsletter (6:00 AM daily)
echo "0 6 * * * cd /app && bash scripts/run-newsletter.sh >> /var/log/newsletter.log 2>&1" | crontab -

# Start cron daemon
cron

echo "Newsletter container started."
echo "Cron job scheduled for 6:00 AM daily."
echo ""
echo "First time setup:"
echo "  claude /login"
echo ""
echo "Manual run:"
echo "  bash scripts/run-newsletter.sh"
echo ""

# Keep container running with interactive shell
exec bash
