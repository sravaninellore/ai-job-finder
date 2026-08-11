from fastapi import APIRouter
from app.api.v1.endpoints import resume, candidate, jobs, preferences, matching, tracking, alerts

api_router = APIRouter()
api_router.include_router(resume.router, prefix="/resume", tags=["Resume"])
api_router.include_router(candidate.router, prefix="/profile", tags=["Candidate Profile"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["Preferences"])
api_router.include_router(matching.router, prefix="/matching", tags=["AI Matching"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Job CRM Tracker"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts & Notifications"])
