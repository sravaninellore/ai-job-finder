from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.job import Job
from app.models.candidate import CandidateProfile
from app.models.application import JobApplication
from app.schemas.candidate import CandidateProfileSchema
from app.schemas.match import MatchAnalysisResult
from app.services.matching_engine import matching_engine

router = APIRouter()

@router.post("/run-all")
def run_matching_on_all_jobs(db: Session = Depends(get_db)):
    """Run AI matching engine for candidate profile across all discovered jobs."""
    candidate_db = db.query(CandidateProfile).order_by(CandidateProfile.created_at.desc()).first()
    if not candidate_db:
        raise HTTPException(status_code=400, detail="Candidate profile missing. Upload a resume first.")

    cand_schema = CandidateProfileSchema(**candidate_db.profile_data)
    jobs = db.query(Job).all()

    matched_count = 0

    for job in jobs:
        analysis = matching_engine.match(cand_schema, job)

        # Check or create JobApplication entry
        app_entry = db.query(JobApplication).filter(JobApplication.job_id == job.id).first()
        if not app_entry:
            app_entry = JobApplication(
                job_id=job.id,
                status="NEW",
                match_score=analysis.overall_score,
                match_analysis=analysis.model_dump()
            )
            db.add(app_entry)
        else:
            app_entry.match_score = analysis.overall_score
            app_entry.match_analysis = analysis.model_dump()

        matched_count += 1

    db.commit()

    return {
        "message": f"Matching engine evaluated {matched_count} jobs.",
        "candidate": cand_schema.full_name or "Candidate",
        "jobs_matched": matched_count
    }

@router.get("/job/{job_id}", response_model=MatchAnalysisResult)
def get_job_match(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    candidate_db = db.query(CandidateProfile).order_by(CandidateProfile.created_at.desc()).first()
    if not candidate_db:
        raise HTTPException(status_code=400, detail="Candidate profile missing.")

    cand_schema = CandidateProfileSchema(**candidate_db.profile_data)
    return matching_engine.match(cand_schema, job)
