from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.candidate import CandidateProfileSchema

class ResumeUploadResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    candidate_profile: Optional[CandidateProfileSchema] = None

class ResumeResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    raw_text: str
    uploaded_at: datetime

    model_config = {"from_attributes": True}
