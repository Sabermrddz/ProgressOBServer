@echo off
REM ============================================================
REM WebEtu Bot - Windows Launcher
REM تشغيل بوت ويب إيتو على نظام Windows
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║  🎓 WebEtu Grades Monitor Bot - Windows Launcher 🎓   ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 📥 Please install Python from https://www.python.org
    echo 📌 Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo 🔨 Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment found
)

echo.
echo 🚀 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

echo.
echo 📦 Installing dependencies...
pip install -q --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

echo.
echo ⚙️  Checking configuration...
python -c "from config import validate_config; validate_config()"
if errorlevel 1 (
    echo.
    echo ⚠️  Configuration validation warning
    echo 📝 Please ensure you have set the following environment variables:
    echo    - WEBETU_USERNAME
    echo    - WEBETU_PASSWORD
    echo    - TELEGRAM_BOT_TOKEN
    echo.
    echo 💡 You can set them in Windows:
    echo    setx WEBETU_USERNAME "your_username"
    echo    setx WEBETU_PASSWORD "your_password"
    echo    setx TELEGRAM_BOT_TOKEN "your_token"
    echo.
)

echo.
echo 📋 Starting WebEtu Bot...
echo ═════════════════════════════════════════════════════════
echo.

python main.py

echo.
echo ═════════════════════════════════════════════════════════
echo ❌ Bot stopped
pause
