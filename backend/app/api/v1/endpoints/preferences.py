from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.preference import CandidatePreference
from app.schemas.preference import CandidatePreferenceSchema

router = APIRouter()

@router.get("", response_model=CandidatePreferenceSchema)
def get_preferences(db: Session = Depends(get_db)):
    pref = db.query(CandidatePreference).first()
    if not pref:
        # Create default preference record
        pref = CandidatePreference()
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref

@router.put("", response_model=CandidatePreferenceSchema)
def update_preferences(data: CandidatePreferenceSchema, db: Session = Depends(get_db)):
    pref = db.query(CandidatePreference).first()
    if not pref:
        pref = CandidatePreference()

    pref.allowed_work_modes = data.allowed_work_modes
    pref.allowed_remote_scopes = data.allowed_remote_scopes
    pref.preferred_cities = data.preferred_cities
    pref.allowed_employment_types = data.allowed_employment_types
    pref.min_match_percentage = data.min_match_percentage
    pref.max_experience_tolerance = data.max_experience_tolerance

    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref
