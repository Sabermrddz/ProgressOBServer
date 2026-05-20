#!/bin/bash

################################################################################
# WebEtu Bot - Linux/VPS Launcher
# تشغيل بوت ويب إيتو على نظام لينكس
################################################################################

set -e

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║  🎓 WebEtu Grades Monitor Bot - Linux Launcher 🎓     ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "📥 Please install Python 3:"
    echo "   sudo apt-get install python3 python3-pip python3-venv (Ubuntu/Debian)"
    echo "   sudo yum install python3 python3-pip (CentOS/RHEL)"
    exit 1
fi

echo "✅ Python found"
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔨 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment found"
fi

echo ""
echo "🚀 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

echo ""
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "⚙️  Checking configuration..."
python3 -c "from config import validate_config; validate_config()" || {
    echo ""
    echo "⚠️  Configuration validation warning"
    echo "📝 Please ensure you have set the following environment variables:"
    echo "   - WEBETU_USERNAME"
    echo "   - WEBETU_PASSWORD"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo ""
    echo "💡 You can set them in your shell:"
    echo "   export WEBETU_USERNAME=\"your_username\""
    echo "   export WEBETU_PASSWORD=\"your_password\""
    echo "   export TELEGRAM_BOT_TOKEN=\"your_token\""
    echo ""
    echo "💡 Or in ~/.bashrc for persistent setup:"
    echo "   echo 'export WEBETU_USERNAME=\"your_username\"' >> ~/.bashrc"
}

echo ""
echo "📋 Starting WebEtu Bot..."
echo "═════════════════════════════════════════════════════════"
echo ""

python3 main.py

echo ""
echo "═════════════════════════════════════════════════════════"
echo "❌ Bot stopped"
