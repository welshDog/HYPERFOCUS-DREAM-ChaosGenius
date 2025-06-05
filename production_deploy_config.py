#!/usr/bin/env python3
"""
🌍 BROSKI X EMPIRE - PRODUCTION DEPLOYMENT CONFIGURATION
Live deployment to hyperfocuszone.com with HTTPS & Cloudflare
"""
import json
import os
import subprocess
from pathlib import Path


class BROskiProductionDeployer:
    def __init__(self):
        self.domain = "hyperfocuszone.com"
        self.production_port = 443  # HTTPS
        self.redirect_port = 5001  # Internal redirect from our dashboard

    def create_cloudflare_config(self):
        """🔒 Setup Cloudflare WAF, caching, and firewall presets"""
        cloudflare_config = {
            "domain": self.domain,
            "dns_records": [
                {
                    "type": "A",
                    "name": "@",
                    "content": "YOUR_SERVER_IP",
                    "proxied": True,
                },
                {
                    "type": "CNAME",
                    "name": "www",
                    "content": self.domain,
                    "proxied": True,
                },
            ],
            "security_settings": {
                "security_level": "high",
                "ssl_mode": "full",
                "always_use_https": True,
                "min_tls_version": "1.2",
                "automatic_https_rewrites": True,
            },
            "performance_settings": {
                "caching_level": "aggressive",
                "browser_cache_ttl": 14400,
                "development_mode": False,
                "minify": {"css": True, "html": True, "js": True},
            },
            "firewall_rules": [
                {
                    "description": "Block common attacks",
                    "expression": '(http.request.uri.path contains "/admin" and not ip.src in {YOUR_ADMIN_IPS})',
                    "action": "block",
                },
                {
                    "description": "Rate limiting",
                    "expression": '(http.request.uri.path contains "/api/")',
                    "action": "challenge",
                    "rate_limit": "10r/m",
                },
            ],
        }

        with open("cloudflare_production_config.json", "w") as f:
            json.dump(cloudflare_config, f, indent=2)

        print("🔒 Cloudflare production configuration created!")
        return cloudflare_config

    def create_nginx_config(self):
        """🌐 Setup NGINX reverse proxy with HTTPS redirect"""
        nginx_config = f"""
server {{
    listen 80;
    server_name {self.domain} www.{self.domain};
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {self.domain} www.{self.domain};

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/{self.domain}.pem;
    ssl_certificate_key /etc/ssl/private/{self.domain}.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # Reverse proxy to BROski Empire
    location / {{
        proxy_pass http://127.0.0.1:{self.redirect_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support for real-time features
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }}

    # API rate limiting
    location /api/ {{
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://127.0.0.1:{self.redirect_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}

# Rate limiting zone
http {{
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/m;
}}
"""

        with open("nginx_production.conf", "w") as f:
            f.write(nginx_config)

        print("🌐 NGINX production configuration created!")
        return nginx_config

    def create_ssl_setup_script(self):
        """🔒 Create SSL certificate setup with Let's Encrypt"""
        ssl_script = f"""#!/bin/bash
# 🔒 BROSKI X EMPIRE - SSL CERTIFICATE SETUP

echo "🔒 Setting up SSL certificates for {self.domain}..."

# Install certbot if not present
if ! command -v certbot &> /dev/null; then
    echo "📦 Installing certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
fi

# Stop nginx temporarily
sudo systemctl stop nginx

# Generate SSL certificate
sudo certbot certonly --standalone \\
    -d {self.domain} \\
    -d www.{self.domain} \\
    --email admin@{self.domain} \\
    --agree-tos \\
    --non-interactive

# Setup auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -

# Copy nginx config
sudo cp nginx_production.conf /etc/nginx/sites-available/{self.domain}
sudo ln -sf /etc/nginx/sites-available/{self.domain} /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart nginx
sudo nginx -t && sudo systemctl start nginx && sudo systemctl enable nginx

echo "🚀 SSL setup complete! {self.domain} is now live with HTTPS!"
"""

        with open("setup_ssl.sh", "w") as f:
            f.write(ssl_script)

        os.chmod("setup_ssl.sh", 0o755)
        print("🔒 SSL setup script created!")

    def create_production_service(self):
        """🚀 Create systemd service for production deployment"""
        service_config = f"""[Unit]
Description=BROski X Empire - Production Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/chaosgenius
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/root/chaosgenius
ExecStart=/usr/bin/python3 dashboard_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

        with open("broski_empire_production.service", "w") as f:
            f.write(service_config)

        print("🚀 Production service configuration created!")

    def deploy_to_production(self):
        """🌍 Execute full production deployment"""
        print("🌍 DEPLOYING BROSKI X EMPIRE TO PRODUCTION!")
        print("=" * 60)

        # Create all configuration files
        self.create_cloudflare_config()
        self.create_nginx_config()
        self.create_ssl_setup_script()
        self.create_production_service()

        print("✅ All production configurations created!")
        print(f"🌍 Ready to deploy to {self.domain}!")
        print("\n🚀 DEPLOYMENT STEPS:")
        print("1. Run: ./setup_ssl.sh")
        print("2. Configure Cloudflare DNS with your server IP")
        print("3. sudo systemctl enable broski_empire_production.service")
        print("4. sudo systemctl start broski_empire_production.service")
        print(f"5. Visit https://{self.domain} - YOUR EMPIRE IS LIVE!")


if __name__ == "__main__":
    deployer = BROskiProductionDeployer()
    deployer.deploy_to_production()
