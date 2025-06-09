import os
import json
from datetime import datetime

def validate_env(path):
    """Validate environment configuration files"""
    required_keys = [
        "DISCORD_BOT_TOKEN", 
        "FLASK_SECRET_KEY", 
        "DATABASE_URL",
        "DEBUG_MODE",
        "API_PORT"
    ]
    
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return False
    
    print(f"\n🔍 Validating: {path}")
    with open(path, 'r') as f:
        content = f.read()
    
    missing_keys = []
    found_keys = []
    
    for key in required_keys:
        if key in content:
            found_keys.append(key)
            print(f"✅ Found {key}")
        else:
            missing_keys.append(key)
            print(f"❌ Missing {key}")
    
    if missing_keys:
        print(f"\n⚠️  Missing {len(missing_keys)} required configuration keys")
        return False
    else:
        print(f"\n✅ All {len(found_keys)} required keys found!")
        return True

def create_sample_env_files():
    """Create sample environment files if they don't exist"""
    env_dev_content = """# Development Environment
DEBUG_MODE=true
API_PORT=5000
FLASK_SECRET_KEY=your_dev_secret_key_here
DATABASE_URL=sqlite:///chaosgenius_dev.db
DISCORD_BOT_TOKEN=your_discord_bot_token_here
"""
    
    env_prod_content = """# Production Environment
DEBUG_MODE=false
API_PORT=8000
FLASK_SECRET_KEY=your_production_secret_key_here
DATABASE_URL=postgresql://user:pass@localhost/chaosgenius_prod
DISCORD_BOT_TOKEN=your_discord_bot_token_here
"""
    
    if not os.path.exists("./config/.env.dev"):
        with open("./config/.env.dev", "w") as f:
            f.write(env_dev_content)
        print("📝 Created sample .env.dev file")
    
    if not os.path.exists("./config/.env.prod"):
        with open("./config/.env.prod", "w") as f:
            f.write(env_prod_content)
        print("📝 Created sample .env.prod file")

def generate_validation_report():
    """Generate a validation report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "dev_valid": False,
        "prod_valid": False,
        "files_checked": []
    }
    
    if os.path.exists("./config/.env.dev"):
        report["dev_valid"] = validate_env("./config/.env.dev")
        report["files_checked"].append(".env.dev")
    
    if os.path.exists("./config/.env.prod"):
        report["prod_valid"] = validate_env("./config/.env.prod")
        report["files_checked"].append(".env.prod")
    
    # Save report
    os.makedirs("./logs", exist_ok=True)
    report_file = f"./logs/config_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Validation report saved: {report_file}")
    return report

if __name__ == "__main__":
    print("🔧 ChaosGenius Config Validator")
    print("=" * 40)
    
    # Create sample files if needed
    create_sample_env_files()
    
    # Run validation
    report = generate_validation_report()
    
    if report["dev_valid"] and report["prod_valid"]:
        print("\n🎉 All configurations are valid!")
    else:
        print("\n⚠️  Some configurations need attention")