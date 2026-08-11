import os
import logging
import httpx
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TelegramNotificationService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    def send_job_alert(self, job: Dict[str, Any], score: float) -> bool:
        if not self.bot_token or not self.chat_id:
            logger.info(f"[TELEGRAM ALERT SIMULATION] Match {score:.0f}%: {job.get('title')} at {job.get('company')}")
            return True

        title = job.get("title", "Software Role")
        company = job.get("company", "Tech Employer")
        location = job.get("location") or job.get("city") or "Remote India"
        url = job.get("url", "https://aijobfinder.com")

        message = (
            f"🔥 *NEW HIGH MATCH JOB ALERT* ({score:.0f}% Match)\n\n"
            f"*Role:* {title}\n"
            f"*Company:* {company}\n"
            f"*Location:* {location}\n\n"
            f"[Apply Direct Here]({url})"
        )

        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(api_url, json=payload)
                if res.status_code == 200:
                    logger.info(f"Telegram alert sent successfully for job {job.get('id')}")
                    return True
                else:
                    logger.warning(f"Telegram API error: HTTP {res.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

telegram_notification_service = TelegramNotificationService()
