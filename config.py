"""
Configuration module for WebEtu Bot
جميع الإعدادات والثوابت
"""
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (same directory as this file)
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class Config:
    """Main configuration class"""
    
    # ============ WebEtu API Configuration ============
    WEBETU_BASE_URL = "https://api-webetu.mesrs.dz"
    WEBETU_USERNAME = os.getenv("WEBETU_USERNAME", "YOUR_USERNAME")
    WEBETU_PASSWORD = os.getenv("WEBETU_PASSWORD", "YOUR_PASSWORD")
    
    # Student identifiers (dia and ind)
    DIA_ID = os.getenv("DIA_ID", "39608221")
    IND_ID = os.getenv("IND_ID", "38669075")
    
    # ============ Telegram Configuration ============
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "883784883")
    
    # ============ Schedule Configuration ============
    # Check for new grades every N minutes
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
    
    # Retry configuration
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", "5"))
    
    # Request timeout
    REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
    
    # ============ File Storage ============
    GRADES_FILE = os.getenv("GRADES_FILE", "grades.json")
    TOKEN_FILE = os.getenv("TOKEN_FILE", "token.json")
    LOG_FILE = os.getenv("LOG_FILE", "webetu_bot.log")
    
    # ============ Logging Configuration ============
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # ============ Feature Flags ============
    # Send alert if API is down for N consecutive failures
    CONSECUTIVE_FAILURES_ALERT = int(os.getenv("CONSECUTIVE_FAILURES_ALERT", "3"))
    
    # Send detailed logs to success
    VERBOSE_MODE = os.getenv("VERBOSE_MODE", "false").lower() == "true"
    
    # ============ API Headers ============
    USER_AGENT = "okhttp/4.12.0"
    ACCEPT = "application/json, text/plain, */*"
    ACCEPT_ENCODING = "gzip"
    CONTENT_TYPE = "application/json"


def validate_config() -> bool:
    """
    Validate that all required configuration values are set
    تحقق من أن جميع إعدادات المطلوبة معروضة
    """
    required_fields = [
        ("WEBETU_USERNAME", Config.WEBETU_USERNAME),
        ("WEBETU_PASSWORD", Config.WEBETU_PASSWORD),
        ("TELEGRAM_BOT_TOKEN", Config.TELEGRAM_BOT_TOKEN),
        ("TELEGRAM_CHAT_ID", Config.TELEGRAM_CHAT_ID),
    ]
    
    missing = []
    for field_name, field_value in required_fields:
        if field_value in ["YOUR_USERNAME", "YOUR_PASSWORD", "YOUR_BOT_TOKEN"]:
            missing.append(field_name)
    
    if missing:
        print(f"❌ Missing configuration: {', '.join(missing)}")
        print("❌ Please set the following environment variables or update config.py:")
        for field in missing:
            print(f"   - {field}")
        return False
    
    return True
