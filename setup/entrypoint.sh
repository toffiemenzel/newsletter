#!/bin/bash

# Setup cron job for newsletter user (6:00 AM daily)
echo "0 3 * * * cd /app && bash scripts/run-newsletter.sh >> /app/profiles/newsletter.log 2>&1" | crontab -u newsletter -

# Start cron daemon (requires root)
cron

echo "Newsletter container started."
echo "Cron job scheduled for 3:00 AM daily."
echo ""
echo "First time setup:"
echo "  claude /login"
echo ""
echo "Manual run:"
echo "  bash scripts/run-newsletter.sh"
echo ""

# Drop to newsletter user for interactive shell
exec su - newsletter -c "cd /app && bash"
