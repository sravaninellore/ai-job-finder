from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db, SessionLocal
from app.models.job import Job
from app.models.candidate import CandidateProfile
from app.models.preference import CandidatePreference
from app.models.application import JobApplication
from app.schemas.job import JobResponse
from app.schemas.candidate import CandidateProfileSchema
from app.schemas.preference import CandidatePreferenceSchema
from app.services.collectors import (
    greenhouse_collector,
    lever_collector,
    ashby_collector,
    remoteok_collector,
    weworkremotely_collector,
    naukri_collector,
    linkedin_collector,
    wellfound_collector,
    foundit_collector,
    indeed_collector,
    glassdoor_collector,
    instahyre_collector,
    internshala_collector,
)
from app.services.job_deduplicator import job_deduplicator
from app.services.eligibility_filter import eligibility_filter
from concurrent.futures import ThreadPoolExecutor, as_completed

router = APIRouter()

DEFAULT_GREENHOUSE_BOARDS = [
    "stripe", "cloudflare", "airbnb", "datadog", "grafana",
    "openai", "anthropic", "doordash", "instacart", "rippling", "snowflake", "hashicorp"
]
DEFAULT_LEVER_COMPANIES = ["netflix", "palantir", "figma", "gitlab", "docker"]
DEFAULT_ASHBY_BOARDS = ["linear", "retool", "ramp", "supabase", "vercel", "notion", "figma", "brex", "scaleai", "canva", "postman"]

def run_ingestion_in_background():
    db = SessionLocal()
    ingested_count = 0
    duplicate_count = 0
    sources_summary = {}

    tasks = {
        "greenhouse": lambda: greenhouse_collector.fetch_jobs(DEFAULT_GREENHOUSE_BOARDS),
        "lever": lambda: lever_collector.fetch_jobs(DEFAULT_LEVER_COMPANIES),
        "ashby": lambda: ashby_collector.fetch_jobs(DEFAULT_ASHBY_BOARDS),
        "remoteok": lambda: remoteok_collector.fetch_jobs(),
        "weworkremotely": lambda: weworkremotely_collector.fetch_jobs(),
        "naukri": lambda: naukri_collector.fetch_jobs(),
        "linkedin": lambda: linkedin_collector.fetch_jobs(),
        "wellfound": lambda: wellfound_collector.fetch_jobs(),
        "foundit": lambda: foundit_collector.fetch_jobs(),
        "indeed": lambda: indeed_collector.fetch_jobs(),
        "glassdoor": lambda: glassdoor_collector.fetch_jobs(),
        "instahyre": lambda: instahyre_collector.fetch_jobs(),
        "internshala": lambda: internshala_collector.fetch_jobs(),
    }

    all_jobs = []
    with ThreadPoolExecutor(max_workers=13) as executor:
        future_to_source = {executor.submit(fn): source for source, fn in tasks.items()}
        for future in as_completed(future_to_source):
            source = future_to_source[future]
            try:
                jobs = future.result(timeout=10.0)
                sources_summary[source] = len(jobs)
                all_jobs.extend(jobs)
            except Exception:
                sources_summary[source] = 0

    seen_hashes_in_batch = set()

    for item in all_jobs:
        chash = item["content_hash"]
        if chash in seen_hashes_in_batch:
            duplicate_count += 1
            continue

        if job_deduplicator.is_duplicate(db, item["source"], item["source_job_id"], item["url"], chash):
            duplicate_count += 1
            continue

        seen_hashes_in_batch.add(chash)
        db_job = Job(**item)
        db.add(db_job)
        ingested_count += 1

    try:
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

@router.post("/trigger-ingest")
def trigger_job_ingestion(background_tasks: BackgroundTasks):
    """Trigger background job ingestion across 13 sources for fast HTTP response."""
    background_tasks.add_task(run_ingestion_in_background)
    return {
        "message": "Job ingestion task started in background across 13 sources.",
        "status": "processing",
        "ingested": 0
    }

@router.get("", response_model=List[JobResponse])
def get_jobs(
    work_mode: Optional[str] = Query(None),
    remote_scope: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    min_score: Optional[float] = Query(None),
    exclude_applied: bool = Query(True),
    db: Session = Depends(get_db)
):
    query = db.query(Job)

    if work_mode:
        query = query.filter(Job.work_mode == work_mode.upper())

    if remote_scope:
        query = query.filter(Job.remote_scope == remote_scope.upper())

    if source:
        query = query.filter(Job.source == source.lower())

    candidate_db = db.query(CandidateProfile).order_by(CandidateProfile.created_at.desc()).first()
    cand_schema = CandidateProfileSchema(**candidate_db.profile_data) if candidate_db and candidate_db.profile_data else CandidateProfileSchema()

    pref_db = db.query(CandidatePreference).first()
    pref_schema = CandidatePreferenceSchema(**pref_db.to_dict()) if pref_db else CandidatePreferenceSchema()

    jobs = query.order_by(Job.discovered_at.desc()).all()
    results = []

    for j in jobs:
        # Check eligibility
        if candidate_db and pref_db:
            res = eligibility_filter.evaluate(j, cand_schema, pref_schema)
            if not res.eligible:
                continue

        # Join match score if available
        app_entry = None
        if candidate_db:
            app_entry = db.query(JobApplication).filter(JobApplication.job_id == j.id).first()

        score = app_entry.match_score if app_entry else None
        rec = app_entry.match_analysis.get("recommendation") if app_entry and isinstance(app_entry.match_analysis, dict) else None
        app_status = app_entry.status if app_entry else "NEW"

        if exclude_applied and app_status != "NEW":
            continue

        if min_score is not None and (score is None or score < min_score):
            continue

        resp_dict = {
            "id": j.id,
            "source": j.source,
            "source_job_id": j.source_job_id,
            "company": j.company,
            "title": j.title,
            "description": j.description,
            "requirements": j.requirements,
            "responsibilities": j.responsibilities,
            "employment_type": j.employment_type,
            "experience_min": j.experience_min,
            "experience_max": j.experience_max,
            "salary_min": j.salary_min,
            "salary_max": j.salary_max,
            "salary_currency": j.salary_currency,
            "location": j.location,
            "country": j.country,
            "city": j.city,
            "work_mode": j.work_mode,
            "remote_scope": j.remote_scope,
            "skills": j.skills or [],
            "url": j.url,
            "company_url": j.company_url,
            "posted_at": j.posted_at.isoformat() if j.posted_at else None,
            "discovered_at": j.discovered_at.isoformat(),
            "content_hash": j.content_hash,
            "match_score": score,
            "match_recommendation": rec,
            "application_status": app_status
        }
        results.append(resp_dict)

    if min_score is not None or any(r["match_score"] is not None for r in results):
        results.sort(key=lambda x: (x["match_score"] if x["match_score"] is not None else -1), reverse=True)

    return results
