import logging
from datetime import datetime
from app.db.session import SessionLocal
from app.models.candidate import CandidateProfile
from app.models.job import Job
from app.models.application import JobApplication
from app.api.v1.endpoints.jobs import trigger_job_ingestion
from app.api.v1.endpoints.matching import run_matching_on_all_jobs
from app.services.notifications import email_notification_service, telegram_notification_service

logger = logging.getLogger(__name__)

def execute_daily_job_digest_pipeline(recipient_email: str = "") -> dict:
    """End-to-End Automated Pipeline:
       1. Ingest Jobs across all active collectors
       2. Run AI Matching Engine across ingested jobs
       3. Filter top-matched jobs (score >= 70%)
       4. Dispatch Email Digest & Telegram Alerts
    """
    logger.info(f"[{datetime.now().isoformat()}] Starting Daily AI Job Digest Pipeline...")

    db = SessionLocal()
    try:
        # 1. Trigger Ingestion
        ingest_res = trigger_job_ingestion(db)
        
        # 2. Run AI Matching Engine
        match_res = run_matching_on_all_jobs(db)

        # 3. Retrieve Top Jobs
        candidate_db = db.query(CandidateProfile).order_by(CandidateProfile.created_at.desc()).first()
        cand_name = "Candidate"
        if candidate_db and candidate_db.profile_data:
            cand_name = candidate_db.profile_data.get("full_name") or candidate_db.profile_data.get("email") or "Candidate"
            if not recipient_email and candidate_db.profile_data.get("email"):
                recipient_email = candidate_db.profile_data.get("email")

        top_apps = db.query(JobApplication).filter(JobApplication.match_score >= 70.0).order_by(JobApplication.match_score.desc()).limit(10).all()

        top_jobs = []
        for app in top_apps:
            job = db.query(Job).filter(Job.id == app.job_id).first()
            if job:
                top_jobs.append({
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "work_mode": job.work_mode,
                    "url": job.url,
                    "match_score": app.match_score
                })

        # 4. Dispatch Email & Telegram Notifications
        email_sent = False
        if recipient_email and top_jobs:
            email_sent = email_notification_service.send_digest_email(recipient_email, cand_name, top_jobs)

        telegram_sent = False
        if top_jobs and top_jobs[0].get("match_score", 0) >= 85.0:
            telegram_sent = telegram_notification_service.send_job_alert(top_jobs[0], top_jobs[0]["match_score"])

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "candidate_name": cand_name,
            "recipient_email": recipient_email,
            "jobs_ingested": ingest_res.get("ingested", 0),
            "jobs_matched": match_res.get("jobs_matched", 0),
            "top_matches_found": len(top_jobs),
            "email_sent": email_sent,
            "telegram_sent": telegram_sent
        }

    except Exception as e:
        logger.error(f"Error in daily job digest pipeline: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
