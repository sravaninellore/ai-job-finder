from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class PreviousRole(BaseModel):
    title: str
    company: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class EducationItem(BaseModel):
    degree: str
    institution: Optional[str] = None
    year: Optional[str] = None
    field_of_study: Optional[str] = None

class CandidateProfileSchema(BaseModel):
    full_name: Optional[str] = Field(default=None, description="Candidate's full name if found")
    email: Optional[str] = Field(default=None, description="Candidate email if found")
    phone: Optional[str] = Field(default=None, description="Candidate phone if found")
    target_roles: List[str] = Field(default_factory=list)
    years_of_experience: float = Field(default=0.0)
    current_role: Optional[str] = None
    previous_roles: List[Dict[str, Any]] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    programming_languages: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    cloud_skills: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    education: List[Dict[str, Any]] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    preferred_work_modes: List[str] = Field(default_factory=list)
    preferred_job_types: List[str] = Field(default_factory=list)
    salary_expectation: Optional[str] = None
    notice_period: Optional[str] = None
    work_authorization: Optional[str] = None

class CandidateProfileResponse(BaseModel):
    id: str
    resume_id: str
    profile_data: CandidateProfileSchema
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}
