FROM node:22-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    cron \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user
RUN useradd -m -s /bin/bash newsletter

# Set working directory
WORKDIR /app

# Copy entrypoint script
COPY setup/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Default command (starts as root, then drops to newsletter user)
CMD ["/entrypoint.sh"]
