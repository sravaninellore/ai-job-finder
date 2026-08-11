from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.job import Job
from app.models.application import JobApplication

router = APIRouter()

ALLOWED_STATUSES = {"NEW", "SAVED", "APPLIED", "SCREENING", "INTERVIEW", "OFFER", "REJECTED"}

class StatusUpdateRequest(BaseModel):
    status: str
    notes: Optional[str] = None

@router.put("/job/{job_id}/status")
def update_job_status(
    job_id: str,
    request: StatusUpdateRequest,
    db: Session = Depends(get_db)
):
    status_upper = request.status.upper()
    if status_upper not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status '{request.status}'. Allowed: {', '.join(ALLOWED_STATUSES)}")

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    app_entry = db.query(JobApplication).filter(JobApplication.job_id == job_id).first()
    if not app_entry:
        app_entry = JobApplication(job_id=job_id, status=status_upper, notes=request.notes)
        db.add(app_entry)
    else:
        app_entry.status = status_upper
        if request.notes is not None:
            app_entry.notes = request.notes

    if status_upper == "APPLIED" and not app_entry.applied_at:
        app_entry.applied_at = datetime.utcnow()

    db.commit()
    db.refresh(app_entry)

    return {
        "job_id": job_id,
        "status": app_entry.status,
        "notes": app_entry.notes,
        "updated_at": app_entry.updated_at.isoformat()
    }

@router.get("/summary")
def get_tracker_summary(db: Session = Depends(get_db)):
    """Get metrics counters for Dashboard."""
    total_jobs = db.query(Job).count()
    saved = db.query(JobApplication).filter(JobApplication.status == "SAVED").count()
    applied = db.query(JobApplication).filter(JobApplication.status == "APPLIED").count()
    interview = db.query(JobApplication).filter(JobApplication.status.in_(["SCREENING", "INTERVIEW"])).count()
    offer = db.query(JobApplication).filter(JobApplication.status == "OFFER").count()
    high_match = db.query(JobApplication).filter(JobApplication.match_score >= 80.0).count()

    return {
        "total_jobs": total_jobs,
        "saved_jobs": saved,
        "applied_jobs": applied,
        "interview_jobs": interview,
        "offer_jobs": offer,
        "high_match_jobs": high_match
    }

@router.get("/board")
def get_crm_board(db: Session = Depends(get_db)):
    """Get all applications grouped by pipeline status, sorted by match score."""
    applications = db.query(JobApplication).order_by(JobApplication.match_score.desc()).all()
    
    board: Dict[str, List[Any]] = {s: [] for s in ALLOWED_STATUSES}

    for app in applications:
        job = db.query(Job).filter(Job.id == app.job_id).first()
        if not job:
            continue
        item = {
            "application_id": app.id,
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "work_mode": job.work_mode,
            "remote_scope": job.remote_scope,
            "url": job.url,
            "match_score": app.match_score,
            "notes": app.notes,
            "updated_at": app.updated_at.isoformat() if app.updated_at else None
        }
        status_key = app.status if app.status in ALLOWED_STATUSES else "NEW"
        board[status_key].append(item)

    return board
