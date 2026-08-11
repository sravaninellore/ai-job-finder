from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict

class JobBase(BaseModel):
    source: str
    source_job_id: Optional[str] = None
    company: str
    title: str
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    employment_type: Optional[str] = "Full-time"
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: Optional[str] = "USD"
    location: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    work_mode: str = "UNKNOWN"
    remote_scope: str = "UNKNOWN"
    skills: List[str] = []
    url: str
    company_url: Optional[str] = None
    posted_at: Optional[datetime] = None

class JobCreate(JobBase):
    raw_data: Optional[Dict[str, Any]] = None

class JobResponse(JobBase):
    id: str
    discovered_at: datetime
    content_hash: str
    match_score: Optional[float] = None
    match_recommendation: Optional[str] = None
    application_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
