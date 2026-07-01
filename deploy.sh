#!/bin/bash
set -euo pipefail

# Deploy/redeploy nginx + backend via Docker Compose, then run the
# Cloudflare tunnel on bare metal (not containerized).
# Run from the repo root on the VM after `git pull`.

# cd "$(dirname "${BASH_SOURCE[0]}")"

# sqlite file must exist before the bind mount, or Docker creates a directory instead.
# touch audit.db

# this script should be run inside a directoy that if already initialised 
# will have a directory like `ai-content-detector` which is the repo name. If it doesn't exist, it will be cloned.

# clones repo if it doesn't exist, otherwise pulls latest changes
# if [ ! -d "ai-content-detector" ]; then
#     git clone https://github.com/AshankDsouza/ai-content-detector
# fi
# cd ai-content-detector
sudo git pull origin master


sudo docker compose down

sudo docker compose build
sudo docker compose up -d

echo "All services are running."
sudo docker compose ps


# nginx is catching requests on port 85, so cloudflared can reach it directly on the host.
echo ""
echo "Starting cloudflared tunnel..."


cloudflared tunnel run ai-check-app-azure-vm

