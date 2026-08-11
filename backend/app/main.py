import os
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine, SessionLocal
# Ensure models are loaded before table creation
from app.models import resume as resume_model
from app.models import candidate as candidate_model
from app.models import preference as preference_model
from app.models import job as job_model

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Seed initial candidate profile, preferences, and trigger initial job ingestion if empty
    db = SessionLocal()
    try:
        if not db.query(candidate_model.CandidateProfile).first():
            profile = candidate_model.CandidateProfile(
                profile_data={
                    "full_name": "Venkata Sravani Nellore",
                    "email": "nellorevenkatasravani@gmail.com",
                    "phone": "+91-7780118415",
                    "skills": ["Python", "React", "JavaScript", "HTML", "CSS", "SQL", "Java", "FastAPI", "Flask", "PostgreSQL", "Git"],
                    "target_roles": ["Software Engineer", "Full Stack Developer", "Python Developer", "Data Analyst"],
                    "years_of_experience": 2.0
                }
            )
            db.add(profile)

        if not db.query(preference_model.CandidatePreference).first():
            pref = preference_model.CandidatePreference(
                target_roles=["Software Engineer", "Full Stack Developer", "Python Developer", "Data Analyst"],
                allowed_work_modes=["REMOTE", "HYBRID", "ONSITE"],
                allowed_remote_scopes=["INDIA_ONLY", "WORLDWIDE"],
                preferred_cities=["Bangalore", "Hyderabad", "Pune", "Chennai"]
            )
            db.add(pref)

        db.commit()

        if db.query(job_model.Job).count() == 0:
            from app.api.v1.endpoints.jobs import run_ingestion_in_background
            threading.Thread(target=run_ingestion_in_background, daemon=True).start()
    except Exception:
        db.rollback()
    finally:
        db.close()

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS setup
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION
    }
