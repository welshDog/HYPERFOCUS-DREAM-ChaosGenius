@echo off
echo 🧠 ChaosGenius Empire Launcher
echo ================================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 📥 Download from: https://python.org/downloads/
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venvve\Scripts\activate.bat" (
    echo 📦 Creating virtual environment...
    python -m venv venvve
)

:: Activate virtual environment
echo ⚡ Activating virtual environment...
call venvve\Scripts\activate.bat

:: Install/update dependencies
echo 📚 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Create necessary directories
if not exist "logs" mkdir logs
if not exist "production_assets\product_ideas" mkdir "production_assets\product_ideas"
if not exist "generated_docs" mkdir "generated_docs"

:: Launch ChaosGenius
echo 🚀 Launching ChaosGenius Ecosystem...
echo.
echo 🎛️ Dashboard will start at: http://localhost:5000
echo 📚 API Documentation at: http://localhost:5000/apidocs/
echo.
echo ✨ Press Ctrl+C in any window to stop all services
echo 💜 Building neurodivergent empires...
echo.

python startup_manager.py

pause