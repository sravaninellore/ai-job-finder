import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Candidate profile JSON payload matching Phase 2 spec
    profile_data = Column(JSON, nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="candidate_profile")
