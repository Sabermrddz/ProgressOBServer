"""
Main entry point and scheduler for WebEtu Bot
"""
import logging
import schedule
import time
import sys
from datetime import datetime
from config import Config, validate_config
from api import WebEtuAPI
from bot import TelegramBot
from storage import GradeStorage


# ============ Setup Logging ============
def setup_logging():
    """Setup logging to file and console"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = getattr(logging, Config.LOG_LEVEL)
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Level: {Config.LOG_LEVEL}")


logger = logging.getLogger(__name__)


# ============ Global State ============
class BotState:
    """Maintains bot state"""
    def __init__(self):
        self.api = WebEtuAPI()
        self.bot = TelegramBot()
        self.storage = GradeStorage(Config.GRADES_FILE)
        self.consecutive_failures = 0
        self.alert_sent = False


bot_state = BotState()


# ============ Main Functions ============
def sync_grades():
    """
    Sync grades from WebEtu API
    """
    try:
        logger.info("=" * 60)
        logger.info(f"🔄 Starting grade synchronization at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Ensure authentication
        if not bot_state.api.ensure_authenticated():
            logger.error("❌ Failed to authenticate")
            handle_sync_failure()
            return
        
        new_exam_grades = []
        new_continuous_grades = []
        
        # Fetch exam grades
        logger.info("📝 Fetching exam grades...")
        success, exam_data = bot_state.api.get_exam_grades()
        if success:
            new_exams, count = bot_state.storage.save_exam_grades(exam_data)
            new_exam_grades = new_exams
            logger.info(f"✅ Exam grades: {count} new")
        else:
            logger.warning("⚠️ Failed to fetch exam grades")
        
        # Fetch continuous grades
        logger.info("📝 Fetching continuous assessment grades...")
        success, continuous_data = bot_state.api.get_continuous_grades()
        if success:
            new_continuous, count = bot_state.storage.save_continuous_grades(continuous_data)
            new_continuous_grades = new_continuous
            logger.info(f"✅ Continuous grades: {count} new")
        else:
            logger.warning("⚠️ Failed to fetch continuous grades")
        
        # Send notifications only after baseline sync
        total_new = len(new_exam_grades) + len(new_continuous_grades)
        logger.info(f"📊 Total new grades: {total_new}")
        
        if not bot_state.storage.is_initialized():
            logger.info("🧭 Baseline sync complete. Skipping notifications for existing grades.")
            bot_state.storage.mark_initialized()
        elif total_new > 0:
            logger.info("🔔 Sending notifications for new grades...")
            
            for grade in new_exam_grades:
                if bot_state.bot.send_new_grade_notification(grade, "exam"):
                    logger.info(f"✅ Notification sent for exam: {grade.get('mcLibelleAr')}")
                else:
                    logger.error(f"❌ Failed to send notification for exam: {grade.get('mcLibelleAr')}")
                
                # Small delay between notifications
                time.sleep(0.5)
            
            for grade in new_continuous_grades:
                if bot_state.bot.send_new_grade_notification(grade, "continuous"):
                    logger.info(f"✅ Notification sent for continuous: {grade.get('mcLibelleAr')}")
                else:
                    logger.error(f"❌ Failed to send notification for continuous: {grade.get('mcLibelleAr')}")
                
                # Small delay between notifications
                time.sleep(0.5)
        
        # Reset failure counter on successful sync
        bot_state.consecutive_failures = 0
        bot_state.alert_sent = False
        
        # Log storage stats
        stats = bot_state.storage.get_stats()
        logger.info(f"📈 Storage stats: {stats}")
        logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"❌ Sync error: {e}")
        handle_sync_failure()


def handle_sync_failure():
    """
    Handle synchronization failure
    """
    bot_state.consecutive_failures += 1
    api_failures = bot_state.api.consecutive_failures
    max_failures = Config.CONSECUTIVE_FAILURES_ALERT
    
    logger.warning(f"⚠️ Sync failure #{bot_state.consecutive_failures}")
    logger.warning(f"⚠️ API failures: {api_failures}/{max_failures}")
    
    # Send alert if too many consecutive failures
    if api_failures >= max_failures and not bot_state.alert_sent:
        error_msg = f"❌ API failed {api_failures} consecutive times. Service may be unavailable."
        bot_state.bot.send_error_alert(error_msg)
        bot_state.alert_sent = True
        logger.error("🚨 Sent error alert to Telegram")


def schedule_sync():
    """Schedule grade synchronization"""
    schedule.every(Config.CHECK_INTERVAL_MINUTES).minutes.do(sync_grades)
    logger.info(f"⏰ Scheduled grade check every {Config.CHECK_INTERVAL_MINUTES} minutes")


def run_scheduler():
    """Run the scheduler loop"""
    logger.info("🚀 Starting scheduler...")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("⏹️ Scheduler interrupted by user")
            break
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")
            time.sleep(5)


# ============ Initialization ============
def initialize_bot():
    """Initialize bot components"""
    logger.info("🤖 Initializing WebEtu Bot...")
    
    # Validate configuration
    if not validate_config():
        logger.error("❌ Configuration validation failed")
        return False
    
    # Test Telegram connection
    logger.info("📡 Testing Telegram connection...")
    if bot_state.bot.test_connection():
        logger.info("✅ Telegram connection successful")
        bot_state.bot.send_startup_notification()
    else:
        logger.warning("⚠️ Telegram connection failed - notifications may not work")
    
    # Test WebEtu authentication (don't fail if network is slow)
    logger.info("🔐 Testing WebEtu authentication...")
    try:
        if bot_state.api.authenticate():
            logger.info("✅ WebEtu authentication successful")
            
            # Test if token works with any endpoint
            logger.info("🧪 Testing token validity...")
            success, info = bot_state.api.test_token_with_info()
            if success:
                logger.info("✅ Token is valid and working")
            else:
                logger.warning("⚠️ Token not working with info endpoints - may be grades access issue")
        else:
            logger.warning("⚠️ WebEtu authentication failed - will retry during sync")
    except Exception as e:
        logger.warning(f"⚠️ WebEtu connection error: {e} - will retry during sync")
    
    logger.info("=" * 60)
    logger.info("📋 Configuration Summary:")
    logger.info(f"  • API Base URL: {Config.WEBETU_BASE_URL}")
    logger.info(f"  • Check Interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
    logger.info(f"  • Storage File: {Config.GRADES_FILE}")
    logger.info(f"  • Log File: {Config.LOG_FILE}")
    logger.info(f"  • Max Retries: {Config.MAX_RETRIES}")
    logger.info(f"  • Verbose Mode: {Config.VERBOSE_MODE}")
    logger.info("=" * 60)
    
    # Bot initialized successfully (even if auth test failed - will retry during sync)
    return True


# ============ Main Entry Point ============
def main():
    """Main entry point"""
    setup_logging()
    
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + "  🎓 WebEtu Grades Monitor Bot 🎓  ".center(58) + "║")
    logger.info("║" + "  Algerian University System (PROGRESS)  ".center(58) + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    # Initialize
    if not initialize_bot():
        logger.error("❌ Initialization failed. Exiting.")
        sys.exit(1)
    
    # Perform initial sync (optional - will retry on schedule)
    logger.info("\n🔄 Performing initial synchronization...")
    try:
        sync_grades()
    except Exception as e:
        logger.warning(f"⚠️ Initial sync failed: {e} - will retry on schedule")
    
    # Schedule and run
    schedule_sync()
    logger.info("\n✅ Bot started successfully!")
    logger.info("📌 Press Ctrl+C to stop the bot\n")
    
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down bot gracefully...")
        logger.info("✅ Bot stopped")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
