#!/bin/bash
# HyperFocusZone Flask Cloudflare Ultra Deployment Script

echo "🚀 Deploying HyperFocusZone Flask Cloudflare Ultra App..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set executable permissions
chmod +x deploy.sh

# Run the application
echo "🌐 Starting Flask app with Cloudflare optimization..."
python flask_cloudflare_ultra.py

echo "✅ Deployment complete! App running on http://localhost:5000"
echo "🔥 Cloudflare Ultra features enabled!"
echo "📊 Available endpoints:"
echo "  • / - Main app info"
echo "  • /api/data - Cached API data"
echo "  • /api/health - Health check"
echo "  • /api/hyperfocus - Hyperfocus tracking"