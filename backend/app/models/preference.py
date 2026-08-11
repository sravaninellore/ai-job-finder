import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Float, Integer, Boolean
from app.db.base import Base

class CandidatePreference(Base):
    __tablename__ = "candidate_preferences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    allowed_work_modes = Column(JSON, nullable=False, default=lambda: ["REMOTE", "HYBRID", "ONSITE"])
    allowed_remote_scopes = Column(JSON, nullable=False, default=lambda: ["INDIA", "WORLDWIDE"])
    preferred_cities = Column(JSON, nullable=False, default=lambda: ["Bangalore", "Hyderabad", "Pune", "Chennai"])
    allowed_employment_types = Column(JSON, nullable=False, default=lambda: ["Full-time"])
    
    min_match_percentage = Column(Float, nullable=False, default=70.0) # Match threshold e.g. 70%
    max_experience_tolerance = Column(Integer, nullable=False, default=5) # Reject if job requires > 5+ yrs above candidate experience
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "allowed_work_modes": self.allowed_work_modes or ["REMOTE", "HYBRID", "ONSITE"],
            "allowed_remote_scopes": self.allowed_remote_scopes or ["INDIA", "WORLDWIDE"],
            "preferred_cities": self.preferred_cities or ["Bangalore", "Hyderabad", "Pune", "Chennai"],
            "allowed_employment_types": self.allowed_employment_types or ["Full-time"],
            "min_match_percentage": self.min_match_percentage,
            "max_experience_tolerance": self.max_experience_tolerance
        }
