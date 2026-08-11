from typing import Optional
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.candidate import CandidateProfile
from app.services.scheduler import execute_daily_job_digest_pipeline
from app.services.notifications import email_notification_service, telegram_notification_service

router = APIRouter()

@router.post("/trigger-daily-digest")
def trigger_daily_digest(recipient_email: Optional[str] = Body(None, embed=True)):
    """Manually trigger the full daily ingestion, AI matching, and email/telegram digest dispatch."""
    result = execute_daily_job_digest_pipeline(recipient_email or "")
    return result

@router.post("/test-email")
def send_test_email(recipient_email: str = Body(..., embed=True)):
    """Send a sample HTML AI Job Digest test email."""
    sample_jobs = [
        {
            "id": "1",
            "title": "Senior Data Analyst",
            "company": "ABC Technologies",
            "location": "Remote — India",
            "work_mode": "REMOTE",
            "url": "https://example.com/job/1",
            "match_score": 96.0
        },
        {
            "id": "2",
            "title": "BI Analyst & Engineer",
            "company": "XYZ Corp",
            "location": "Hyderabad — Hybrid",
            "work_mode": "HYBRID",
            "url": "https://example.com/job/2",
            "match_score": 93.0
        },
        {
            "id": "3",
            "title": "Full Stack Developer",
            "company": "Startup AI",
            "location": "Remote — Worldwide",
            "work_mode": "REMOTE",
            "url": "https://example.com/job/3",
            "match_score": 89.0
        }
    ]

    success = email_notification_service.send_digest_email(recipient_email, "Test User", sample_jobs)
    return {
        "status": "sent" if success else "failed",
        "recipient_email": recipient_email,
        "message": f"Test digest email dispatch completed for {recipient_email}."
    }

@router.post("/test-telegram")
def send_test_telegram():
    """Send a sample Telegram notification test message."""
    sample_job = {
        "id": "test-1",
        "title": "Senior Python & AI Engineer",
        "company": "Top Global Tech",
        "location": "Remote India",
        "url": "https://example.com/job/test-1"
    }
    success = telegram_notification_service.send_job_alert(sample_job, 95.0)
    return {
        "status": "sent" if success else "failed",
        "message": "Test Telegram alert dispatch completed."
    }
