from typing import List, Optional
from pydantic import BaseModel

class MatchAnalysisResult(BaseModel):
    overall_score: float # 0 to 100
    skill_score: float   # 0 to 100 (30% weight)
    experience_score: float # 0 to 100 (25% weight)
    role_score: float    # 0 to 100 (20% weight)
    location_score: float # 0 to 100 (20% weight)
    education_score: float # 0 to 100 (5% weight)
    strengths: List[str] = []
    missing_skills: List[str] = []
    concerns: List[str] = []
    recommendation: str # "highly_recommended", "recommended", "possible", "poor"
    explanation: str
