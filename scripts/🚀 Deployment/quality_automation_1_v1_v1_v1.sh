#!/bin/bash
# 🧹 BROSKI CODE QUALITY AUTOMATION
# Automated code formatting and quality checks

echo "🧹💜 BROSKI CODE QUALITY AUTOMATION ACTIVATED! 💜🧹"

# Format code with Black
echo "🎨 Formatting code with Black..."
black /root/chaosgenius --line-length 88 --quiet

# Sort imports with isort
echo "📋 Sorting imports with isort..."
isort /root/chaosgenius --profile black --quiet

# Run flake8 linting
echo "🔍 Running flake8 linting..."
flake8 /root/chaosgenius --max-line-length=88 --extend-ignore=E203,W503 --count

# Run security scan
echo "🛡️ Running security scan..."
bandit -r /root/chaosgenius -f txt | head -20

echo "✅ Code quality automation complete!"
