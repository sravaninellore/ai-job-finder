from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.candidate import CandidateProfile
from app.schemas.candidate import CandidateProfileResponse, CandidateProfileSchema

router = APIRouter()

@router.get("/latest", response_model=CandidateProfileResponse)
def get_latest_candidate_profile(db: Session = Depends(get_db)):
    """Retrieve the candidate profile created from the latest uploaded resume."""
    profile = db.query(CandidateProfile).order_by(CandidateProfile.created_at.desc()).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No candidate profile found. Please upload a resume first.")

    return CandidateProfileResponse(
        id=profile.id,
        resume_id=profile.resume_id,
        profile_data=CandidateProfileSchema(**profile.profile_data),
        created_at=profile.created_at.isoformat(),
        updated_at=profile.updated_at.isoformat()
    )

@router.put("/latest", response_model=CandidateProfileResponse)
def update_candidate_profile(updated_data: CandidateProfileSchema, db: Session = Depends(get_db)):
    """Update active candidate profile parameters."""
    profile = db.query(CandidateProfile).order_by(CandidateProfile.created_at.desc()).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No active candidate profile found to update.")

    profile.profile_data = updated_data.model_dump()
    db.commit()
    db.refresh(profile)

    return CandidateProfileResponse(
        id=profile.id,
        resume_id=profile.resume_id,
        profile_data=CandidateProfileSchema(**profile.profile_data),
        created_at=profile.created_at.isoformat(),
        updated_at=profile.updated_at.isoformat()
    )
