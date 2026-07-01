                     Internet
                          │
                          ▼
             https://ai-generated-text.tech
                          │
                    Cloudflare Tunnel (bare metal)
                          │
                          ▼
                  Nginx (container, :80)
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
        Static frontend (bind mount)  Flask API (container, :5001)

nginx and backend run as Docker Compose services on one shared network,
defined in ./docker-compose.yml. cloudflared runs directly on the VM
(not containerized) and reaches nginx over localhost:80, since nginx's
port is published to the host. There is no more host-run Flask process
or http.server — only cloudflared stays bare metal.

## One-time VM setup
1. Install Docker + Docker Compose plugin on the Azure VM.
2. `git clone` this repo onto the VM.
3. Copy the trained model artifacts into `./models/` (gitignored — not
   in version control, so they must be transferred separately, e.g.
   `scp -r models/ user@vm:~/ai_text_detector/`).
4. Copy `.env` (KAGGLE_API_TOKEN etc.) onto the VM — also gitignored.
5. Install `cloudflared` on the VM and set up the tunnel credentials:
   `cloudflared tunnel login` + `cloudflared tunnel create ai-generated-text-check-app`
   (or copy `~/.cloudflared/` from the existing machine). The
   `config.yml` ingress can keep pointing at `http://localhost:80`
   since cloudflared runs on the host, not in the Docker network:

   ```yaml
   tunnel: ai-generated-text-check-app
   credentials-file: /home/<user>/.cloudflared/<tunnel-id>.json

   ingress:
     - hostname: ai-generated-text.tech
       service: http://localhost:80
     - hostname: www.ai-generated-text.tech
       service: http://localhost:80
     - service: http_status:404
   ```
6. `touch audit.db` (so the bind mount attaches to a file, not a
   directory Docker would otherwise create).

## Deploy / redeploy
```
git pull
./deploy.sh
```
`deploy.sh` runs `docker compose build && docker compose up -d` for
nginx/backend, then starts `cloudflared tunnel run
ai-generated-text-check-app` in the foreground. Rebuilding only touches
the images whose inputs changed, so a backend-only code change never
recreates nginx.

## Why this fixes the versioning/breakage issues
- Backend Python deps (spacy, tensorflow, keras, etc.) are pinned and
  installed inside `backend.Dockerfile` from `requirements.linux.txt`
  (the Linux/CPU equivalent of `requirements.txt`, which pins
  `tensorflow-macos` for local Mac development) — no drift between
  what's on the VM and what's declared in the repo.
- The frontend is plain static HTML/JS with no build step, so nginx
  serves `./frontend` directly via a read-only bind mount — editing a
  file and restarting nginx is enough, no separate Node process to
  keep alive.
- nginx proxies `/api/` to `http://backend:5001` using Docker's
  built-in service-name DNS instead of `host.docker.internal` or a
  hardcoded port, so container restarts/IP changes never break routing.
- Both containers have `restart: unless-stopped`, so a VM reboot brings
  nginx/backend back without manual intervention; cloudflared needs to
  be re-run or set up as a systemd service (see below) to survive a
  reboot too.

## Optional: keep cloudflared running across reboots
Since cloudflared is bare metal now, use `cloudflared service install`
(installs a systemd unit on Linux) instead of relying on `deploy.sh`'s
foreground process staying alive in a terminal.
