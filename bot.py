"""
Telegram bot module for sending notifications
"""
import requests
import logging
from typing import Dict, List, Optional
from config import Config


logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram bot for sending grade notifications"""
    
    def __init__(self):
        """Initialize Telegram bot"""
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def _send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Send message to Telegram chat
        
        Args:
            text: Message text
            parse_mode: HTML or Markdown
            
        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            
            response = requests.post(
                url,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT_SECONDS
            )
            
            if response.status_code == 200:
                logger.debug("✅ Telegram message sent successfully")
                return True
            else:
                logger.error(f"❌ Failed to send Telegram message: {response.status_code}")
                logger.error(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending Telegram message: {e}")
            return False
    
    def send_new_grade_notification(self, grade: Dict, grade_type: str) -> bool:
        """
        Send new grade notification in English
        
        Args:
            grade: Grade dictionary with grade data
            grade_type: "exam" or "continuous"
            
        Returns:
            True if successful
        """
        try:
            note_value = grade.get("noteExamen", "N/A")
            subject_ar = grade.get("mcLibelleAr", "Unknown")
            subject_fr = grade.get("mcLibelleFr", "Unknown")
            coefficient = grade.get("rattachementMcCoefficient", 1)
            session = grade.get("planningSessionIntitule", "Unknown")
            is_absent = grade.get("absent", False)
            
            # Determine type text
            if grade_type.lower() == "exam":
                type_text = "Exam"
            else:
                type_text = "Continuous Assessment"
            
            # Build notification message
            message = f"""
🎓 <b>New Grade!</b>

📚 <b>Subject:</b> {subject_ar}
   <i>({subject_fr})</i>

📝 <b>Type:</b> {type_text}

✅ <b>Grade:</b> {note_value}/20
📊 <b>Coefficient:</b> {coefficient}

🗓️ <b>Session:</b> {session}
"""
            
            if is_absent:
                message += "\n⚠️ <b>Status:</b> Absent"
            
            return self._send_message(message)
            
        except Exception as e:
            logger.error(f"❌ Error creating grade notification: {e}")
            return False
    
    def send_error_alert(self, error_message: str) -> bool:
        """
        Send error alert to user
        
        Args:
            error_message: Description of the error
            
        Returns:
            True if successful
        """
        try:
            message = f"""
⚠️ <b>Error Alert</b>

{error_message}

⏰ Please try again later
"""
            return self._send_message(message)
        except Exception as e:
            logger.error(f"❌ Error sending alert: {e}")
            return False
    
    def send_startup_notification(self) -> bool:
        """Send startup confirmation notification"""
        try:
            message = f"""
✅ <b>Bot Started Successfully!</b>

🤖 <b>Grade Monitoring Service:</b> Active
⏰ <b>Check Interval:</b> Every {Config.CHECK_INTERVAL_MINUTES} minutes
📲 <b>Notifications:</b> Enabled

You will be notified of all new grades automatically
"""
            return self._send_message(message)
        except Exception as e:
            logger.error(f"❌ Error sending startup notification: {e}")
            return False
    
    def send_sync_summary(self, new_exam_count: int, new_continuous_count: int) -> bool:
        """
        Send sync summary notification
        
        Args:
            new_exam_count: Number of new exam grades
            new_continuous_count: Number of new continuous grades
            
        Returns:
            True if successful
        """
        try:
            total = new_exam_count + new_continuous_count
            
            if total == 0:
                message = "📊 <b>Update:</b> No new grades"
            else:
                message = f"""
📊 <b>Update Summary:</b>

✅ <b>New Exam Grades:</b> {new_exam_count}
✅ <b>New Continuous Assessment Grades:</b> {new_continuous_count}

📈 <b>Total New:</b> {total}
"""
            
            return self._send_message(message)
        except Exception as e:
            logger.error(f"❌ Error sending sync summary: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test connection to Telegram bot
        
        Returns:
            True if connection successful
        """
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=Config.REQUEST_TIMEOUT_SECONDS)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    bot_info = data.get("result", {})
                    logger.info(f"✅ Telegram bot connected: @{bot_info.get('username')}")
                    return True
            
            logger.error(f"❌ Telegram connection failed: {response.status_code}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error testing Telegram connection: {e}")
            return False
