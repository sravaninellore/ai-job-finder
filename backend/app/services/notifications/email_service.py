import os
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class EmailNotificationService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.sender_email = os.getenv("SENDER_EMAIL", self.smtp_user or "alerts@aijobfinder.com")

    def generate_digest_html(self, candidate_name: str, top_jobs: List[Dict[str, Any]]) -> str:
        date_str = datetime.now().strftime("%d %b %Y")
        
        job_cards_html = ""
        for job in top_jobs[:10]:
            score = round(job.get("match_score", 85)) if isinstance(job.get("match_score"), (int, float)) else 85
            title = job.get("title", "Software Position")
            company = job.get("company", "Tech Company")
            location = job.get("location") or job.get("city") or "Remote India"
            url = job.get("url", "#")
            work_mode = job.get("work_mode", "REMOTE")

            job_cards_html += f"""
            <div style="background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 16px; margin-bottom: 14px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 13px;">
                  🔥 {score}% Match
                </span>
                <span style="color: #94a3b8; font-size: 11px;">{work_mode}</span>
              </div>
              <h3 style="color: #ffffff; font-size: 16px; margin: 10px 0 4px 0;">{title}</h3>
              <p style="color: #818cf8; font-size: 13px; margin: 0 0 8px 0; font-weight: 600;">{company} • {location}</p>
              <a href="{url}" target="_blank" style="display: inline-block; background-color: #4f46e5; color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: bold; margin-top: 6px;">
                View & Apply →
              </a>
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
        </head>
        <body style="background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #f8fafc; padding: 24px;">
          <div style="max-w: 600px; margin: 0 auto; background-color: #090d16; border-radius: 16px; padding: 28px; border: 1px solid #1e293b;">
            <div style="border-b: 1px solid #1e293b; padding-bottom: 16px; margin-bottom: 20px;">
              <span style="color: #6366f1; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">
                PERSONAL AI JOB FINDER DIGEST
              </span>
              <h1 style="color: #ffffff; font-size: 22px; margin: 6px 0 0 0;">Daily AI Job Digest — {date_str}</h1>
              <p style="color: #94a3b8; font-size: 13px; margin: 4px 0 0 0;">Prepared for {candidate_name}</p>
            </div>

            <p style="color: #cbd5e1; font-size: 14px; line-height: 1.5; margin-bottom: 20px;">
              Here are your top-matched job opportunities discovered and evaluated by your Personal AI Job Finder:
            </p>

            {job_cards_html}

            <div style="border-t: 1px solid #1e293b; pt: 16px; margin-top: 24px; text-align: center; color: #64748b; font-size: 11px;">
              © 2026 Personal AI Job Finder • Automated Daily Digest Engine
            </div>
          </div>
        </body>
        </html>
        """
        return html_content

    def send_digest_email(self, recipient_email: str, candidate_name: str, top_jobs: List[Dict[str, Any]]) -> bool:
        if not recipient_email:
            logger.warning("No recipient email provided for digest.")
            return False

        html_body = self.generate_digest_html(candidate_name, top_jobs)
        date_str = datetime.now().strftime("%d %b %Y")
        subject = f"🔥 Your Daily AI Job Digest — {date_str}"

        # If SMTP password/user not set, simulate clean email logging
        if not self.smtp_user or not self.smtp_password:
            logger.info(f"[EMAIL ALERT SIMULATION] Digest generated for '{recipient_email}' with {len(top_jobs)} jobs.")
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.sender_email, [recipient_email], msg.as_string())

            logger.info(f"Successfully sent daily digest email to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email digest: {e}")
            return False

email_notification_service = EmailNotificationService()
