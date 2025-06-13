module.exports = {
  apps : [{
    name   : "chaosgenius-api",
    script : "gunicorn",
    args   : "--workers 3 --bind 0.0.0.0:5000 dashboard_api:app",
    interpreter: "python3",
    cwd    : "/root/chaosgenius",
    env_production: {
      FLASK_ENV: "production",
      SECRET_KEY: "replace_with_env_or_secure_method"
    }
  }]
}
