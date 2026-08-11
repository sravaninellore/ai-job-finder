import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Float, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

# Status pipeline: NEW -> SAVED -> APPLIED -> SCREENING -> INTERVIEW -> OFFER -> REJECTED
class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(String(50), nullable=False, default="NEW") # NEW, SAVED, APPLIED, SCREENING, INTERVIEW, OFFER, REJECTED
    notes = Column(Text, nullable=True)
    
    match_score = Column(Float, nullable=True)
    match_analysis = Column(JSON, nullable=True)
    
    applied_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="applications")
