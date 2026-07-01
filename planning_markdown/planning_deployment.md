                     Internet
                          │
                          ▼
             https://ai-generated-text.tech
                          │
                    Cloudflare Tunnel
                          │
                          ▼
                  Nginx (localhost:80)
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
            React/Vue/HTML         Flask API
          localhost:3000       localhost:5001

Features:
1. we run cloudfare at localhost:80
2.  nginx: There is no need to have a local.nginx since we are hosting it on this laptop itself. keep nginx.conf, delete the other. 
the nginx will match localhost:80/api ( https://ai-generated-text.tech/api) to localhost:5001 and localhost:80/( https://ai-generated-text.tech/ ) to localhosta:3000

it can be something like this:

server {
    listen 80;
    server_name ai-generated-text.tech;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
    }

    # Backend
    location /api/ {
        proxy_pass http://localhost:5001/;

        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
3. run nginx on port 80 through docker containers

docker build -t ai-generated-text-nginx:latest ./nginx

docker run -d \
    --name nginx \
    -p 80:80 \
    --restart unless-stopped \
    ai-generated-text-nginx:latest

4. run the cloudfare

# cloudfare config files stored at /Users/ashankdsouza/.cloudflared
# run cloudflared tunnel in the foreground
cloudflared tunnel run ai-generated-text-check-app



