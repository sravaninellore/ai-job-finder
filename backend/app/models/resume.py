import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    raw_text = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    candidate_profile = relationship("CandidateProfile", back_populates="resume", uselist=False, cascade="all, delete-orphan")
