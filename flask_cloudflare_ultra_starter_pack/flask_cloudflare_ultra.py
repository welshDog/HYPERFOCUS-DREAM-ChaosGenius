import logging
import os
from functools import wraps

from flask import Flask, jsonify, make_response, request
from flask_caching import Cache
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS for Cloudflare
CORS(app, origins=["*"])

# Configure cache
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "hyperfocus-ultra-secret-key")
cache = Cache(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Cache-control decorator
def cache_control(minutes=5):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                response = make_response(f(*args, **kwargs))
                response.headers["Cache-Control"] = f"public, max-age={minutes * 60}"
                response.headers["X-Content-Type-Options"] = "nosniff"
                response.headers["X-Frame-Options"] = "DENY"
                response.headers["X-XSS-Protection"] = "1; mode=block"
                return response
            except Exception as e:
                logger.error(f"Error in cache_control: {e}")
                return jsonify({"error": "Internal server error"}), 500

        return wrapped

    return decorator


@app.after_request
def add_default_cache_headers(response):
    if "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "public, max-age=3600"

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    return response


@app.route("/")
@cache.cached(timeout=60)
def index():
    try:
        return jsonify(
            {
                "message": "🌐 HyperFocusZone Flask App with Cloudflare Ultra Boost!",
                "status": "active",
                "version": "1.0.0",
                "features": [
                    "Cloudflare optimization",
                    "Advanced caching",
                    "Security headers",
                    "CORS enabled",
                    "Error handling",
                ],
            }
        )
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return jsonify({"error": "Failed to load home page"}), 500


@app.route("/api/data")
@cache_control(minutes=10)
def data():
    try:
        visitor_ip = request.headers.get("CF-Connecting-IP", request.remote_addr)
        country = request.headers.get("CF-IPCountry", "Unknown")
        ray_id = request.headers.get("CF-RAY", "Unknown")

        return jsonify(
            {
                "data": "Ultra Cached API Response",
                "visitor_info": {
                    "ip": visitor_ip,
                    "country": country,
                    "cloudflare_ray_id": ray_id,
                },
                "cache_status": "MISS",
                "timestamp": (
                    str(request.timestamp) if hasattr(request, "timestamp") else "N/A"
                ),
            }
        )
    except Exception as e:
        logger.error(f"Error in data route: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500


@app.route("/api/health")
@cache.cached(timeout=30)
def health_check():
    """Health check endpoint for monitoring"""
    try:
        return jsonify(
            {
                "status": "healthy",
                "service": "HyperFocusZone Flask Ultra",
                "cloudflare_ready": True,
                "cache_enabled": True,
                "uptime": "active",
            }
        )
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({"error": "Health check failed"}), 500


@app.route("/api/hyperfocus")
@cache_control(minutes=15)
def hyperfocus_data():
    """Special endpoint for hyperfocus tracking"""
    try:
        return jsonify(
            {
                "hyperfocus_mode": "active",
                "productivity_score": 95,
                "focus_state": "ultra_concentrated",
                "session_duration": "2h 30m",
                "cloudflare_optimization": "enabled",
                "performance_boost": "+340%",
            }
        )
    except Exception as e:
        logger.error(f"Error in hyperfocus route: {e}")
        return jsonify({"error": "Hyperfocus data unavailable"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development"

    logger.info(f"🚀 Starting HyperFocusZone Flask Ultra on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
