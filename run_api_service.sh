#!/bin/bash



# Get the directory of the script
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# cd "$DIR"

# # Activate the virtual environment if it exists
# if [ -d "venv" ]; then
#     echo "Activating virtual environment..."
#     source venv/bin/activate
# fi
echo "killing apps before "
# stop the apps on port 80, 3000 and 5001
kill -9 $(lsof -t -i:80) 2>/dev/null
kill -9 $(lsof -t -i:3000) 2>/dev/null
kill -9 $(lsof -t -i:5001) 2>/dev/null


# Stop/remove any previous nginx container

# Run the Flask app in detached mode, so we can run the cloudflared tunnel in the same terminal
echo "Starting Flask API service on http://localhost:5001 ..."
nohup /opt/homebrew/bin/python3.11 app.py > flask.log 2>&1 &
disown

# Cache-bust the frontend assets so browsers don't serve a stale script.js/style.css
DEPLOY_VERSION=$(date +%s)
sed -i '' -E "s/\?v=[A-Za-z0-9_]+/?v=${DEPLOY_VERSION}/g" frontend/index.html
echo "Stamped frontend assets with version ${DEPLOY_VERSION}"

# Serve the frontend in detached mode
echo "Starting static frontend on http://localhost:3000 ..."
nohup python3 -m http.server 3000 --directory frontend > http.log 2>&1 &
disown

# Run nginx on port 80 through a Docker container, reverse-proxying
# / to the frontend (localhost:3000) and /api/ to the Flask API (localhost:5001)
echo "Building and starting nginx (Docker) on http://localhost:80 ..."
docker build -t ai-generated-text-nginx:latest ./nginx
docker run -d \
    --name nginx \
    -p 80:80 \
    --restart unless-stopped \
    ai-generated-text-nginx:latest

echo "All services are running."
echo "  API:      http://localhost:5001 (logs: flask.log)"
echo "  Frontend: http://localhost:3000 (logs: http.log)"
echo "  Nginx:    http://localhost:80   (docker container 'nginx')"
echo ""
echo "Now run the tunnel in this terminal:"
echo "  cloudflared tunnel run ai-generated-text-check-app"

# cloudfare config files stored at /Users/ashankdsouza/.cloudflared
# run cloudflared tunnel in the foreground
cloudflared tunnel run ai-generated-text-check-app
