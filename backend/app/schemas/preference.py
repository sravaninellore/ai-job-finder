from typing import List
from pydantic import BaseModel, ConfigDict

class CandidatePreferenceSchema(BaseModel):
    allowed_work_modes: List[str] = ["REMOTE", "HYBRID", "ONSITE"]
    allowed_remote_scopes: List[str] = ["INDIA", "WORLDWIDE"]
    preferred_cities: List[str] = ["Bangalore", "Hyderabad", "Pune", "Chennai"]
    allowed_employment_types: List[str] = ["Full-time"]
    min_match_percentage: float = 70.0
    max_experience_tolerance: int = 5

    model_config = ConfigDict(from_attributes=True)
